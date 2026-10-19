#!/usr/bin/env python3
"""Portable engine product registry/receipt validator.

A read-only projection of code-owned engine manifests, not a new Product State.
It cannot mark an engine RELEASED, ADOPTED or promote an active Goal.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ENGINE_ID = re.compile(r"^[a-z][a-z0-9-]*\.[a-z][a-z0-9-]*$")
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?$")
LIFECYCLES = {"DISCOVERED_LEGACY", "DEFINED", "CANDIDATE", "EVALUATED",
              "RELEASED", "ADOPTED", "REJECTED", "SUPERSEDED", "RETIRED"}


class EngineRegistryError(ValueError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise EngineRegistryError("BAD_PATH:" + str(relative))
    p = Path(relative)
    if p.is_absolute() or ".." in p.parts:
        raise EngineRegistryError("ESCAPE_PATH:" + relative)
    root = root.resolve(strict=True)
    target = (root / p).resolve(strict=True)
    if not target.is_relative_to(root) or not target.is_file():
        raise EngineRegistryError("UNSAFE_OR_MISSING_PATH:" + relative)
    return target


def _load(root: Path, relative: str) -> dict:
    value = json.loads(_path(root, relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise EngineRegistryError("JSON_OBJECT_REQUIRED:" + relative)
    return value


def verify_candidate(root: Path, value: dict, *, engine_id: str, source_paths: list[str]) -> dict:
    """Verify a source-pinned pre-release; never upgrade it to RELEASED."""
    root = Path(root).resolve(strict=True)
    version = value.get("version")
    commit = value.get("source_commit_sha")
    blobs = value.get("source_git_blob_sha1")
    if not isinstance(version, str) or not SEMVER.fullmatch(version) or "-" not in version:
        raise EngineRegistryError("PRE_RELEASE_VERSION_REQUIRED:" + engine_id)
    if not isinstance(commit, str) or not re.fullmatch("[a-f0-9]{40}", commit):
        raise EngineRegistryError("CANDIDATE_EXACT_COMMIT_REQUIRED")
    if not isinstance(blobs, dict) or set(blobs) != set(source_paths):
        raise EngineRegistryError("CANDIDATE_CODE_COVERAGE_MISMATCH")
    if value.get("promotable_to_release") is not False:
        raise EngineRegistryError("UNPROVEN_CANDIDATE_CANNOT_PROMOTE")
    for path in source_paths:
        _path(root, path)
        result = subprocess.run(["git", "-C", str(root), "show", commit + ":" + path],
                                capture_output=True, timeout=15, check=False)
        if result.returncode:
            raise EngineRegistryError("CANDIDATE_HISTORICAL_SOURCE_MISSING:" + path)
        raw = result.stdout
        git_sha = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") +
                               bytes([0]) + raw).hexdigest()
        if git_sha != blobs[path]:
            raise EngineRegistryError("CANDIDATE_BLOB_SHA_MISMATCH:" + path)
    return value


def index(root: Path) -> list[dict[str, Any]]:
    root = Path(root).resolve(strict=True)
    catalog = _load(root, "engines/catalog.json")
    if catalog.get("schema") != "engine-catalog-v1":
        raise EngineRegistryError("CATALOG_SCHEMA_UNSUPPORTED")
    ids: set[str] = set()
    records = []
    for manifest_ref in catalog.get("manifests", []):
        row = _load(root, manifest_ref)
        engine_id = row.get("engine_id")
        if not isinstance(engine_id, str) or not ENGINE_ID.fullmatch(engine_id):
            raise EngineRegistryError("INVALID_ENGINE_ID")
        if engine_id in ids:
            raise EngineRegistryError("DUPLICATE_ENGINE_ID:" + engine_id)
        ids.add(engine_id)
        if not isinstance(row.get("name"), str) or not row["name"].strip():
            raise EngineRegistryError("ENGINE_NAME_REQUIRED:" + engine_id)
        if row.get("lifecycle") not in LIFECYCLES:
            raise EngineRegistryError("INVALID_ENGINE_LIFECYCLE:" + engine_id)
        if not isinstance(row.get("owner"), str) or not row["owner"]:
            raise EngineRegistryError("ENGINE_OWNER_REQUIRED:" + engine_id)
        sources = row.get("source_paths")
        if not isinstance(sources, list) or not sources:
            raise EngineRegistryError("ENGINE_CODE_REQUIRED:" + engine_id)
        for ref in sources:
            _path(root, ref)
        for ref_field in ("design_ref", "contract_ref"):
            _path(root, row.get(ref_field))
        tests = row.get("test_refs")
        if not isinstance(tests, list) or not tests:
            raise EngineRegistryError("ENGINE_TEST_OWNER_REQUIRED:" + engine_id)
        for ref in tests:
            _path(root, ref)
        candidates = row.get("candidates", [])
        if not isinstance(candidates, list):
            raise EngineRegistryError("INVALID_CANDIDATE_LIST")
        candidate_versions = []
        for c in candidates:
            if not isinstance(c, dict):
                raise EngineRegistryError("MALFORMED_ENGINE_CANDIDATE")
            verified = verify_candidate(root, c, engine_id=engine_id, source_paths=sources)
            candidate_versions.append(verified["version"])
        if len(candidate_versions) != len(set(candidate_versions)):
            raise EngineRegistryError("DUPLICATE_ENGINE_CANDIDATE_VERSION")
        adopted = row.get("adopted_version")
        receipts = row.get("release_receipts", [])
        if not isinstance(receipts, list):
            raise EngineRegistryError("BAD_RECEIPT_LIST")
        released_versions = set()
        for rr in receipts:
            release = verify_release(root, rr, expected_id=engine_id)
            if release["version"] in released_versions:
                raise EngineRegistryError("DUPLICATE_RELEASE_VERSION")
            released_versions.add(release["version"])
        if adopted is not None and adopted not in released_versions:
            raise EngineRegistryError("UNPROVEN_ADOPTED_VERSION:" + engine_id)
        if row.get("lifecycle") in {"RELEASED", "ADOPTED"} and not receipts:
            raise EngineRegistryError("RELEASE_WITHOUT_RECEIPT:" + engine_id)
        records.append({"engine_id": engine_id, "name": row["name"],
                        "lifecycle": row["lifecycle"],
                        "adopted_version": adopted,
                        "manifest_ref": manifest_ref,
                        "source_paths": sources,
                        "design_ref": row["design_ref"],
                        "contract_ref": row["contract_ref"],
                        "releases": sorted(released_versions),
                        "candidates": sorted(candidate_versions)})
    return sorted(records, key=lambda x: x["engine_id"])


def verify_release(root: Path, receipt_ref: str, *, expected_id: str | None = None) -> dict:
    root = Path(root).resolve(strict=True)
    release = _load(root, receipt_ref)
    engine_id = release.get("engine_id")
    version = release.get("version")
    if engine_id != expected_id and expected_id is not None:
        raise EngineRegistryError("RECEIPT_WRONG_ENGINE")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        raise EngineRegistryError("INVALID_RELEASE_VERSION")
    commit = release.get("source_commit_sha")
    digests = release.get("source_file_sha256")
    if not isinstance(commit, str) or not re.fullmatch("[a-f0-9]{40}", commit):
        raise EngineRegistryError("IMMUTABLE_SOURCE_COMMIT_REQUIRED")
    if not isinstance(digests, dict) or not digests:
        raise EngineRegistryError("SOURCE_HASHES_REQUIRED")
    for path, expected in digests.items():
        _path(root, path)
        result = subprocess.run(["git", "-C", str(root), "show", commit + ":" + path],
                                capture_output=True, timeout=15, check=False)
        if result.returncode or sha256(result.stdout) != expected:
            raise EngineRegistryError("SOURCE_RELEASE_HASH_MISMATCH:" + path)
    for field in ("contract_sha256", "evidence_ref", "promoted_by", "previous_version",
                  "rollback_ref"):
        if field not in release:
            raise EngineRegistryError("RECEIPT_FIELD_MISSING:" + field)
    if release["evidence_ref"]:
        _path(root, release["evidence_ref"])
    if release["rollback_ref"]:
        _path(root, release["rollback_ref"])
    return release


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["list", "show", "validate", "verify-release", "history", "diff"])
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--engine-id")
    parser.add_argument("--receipt")
    parser.add_argument("--from-receipt")
    parser.add_argument("--to-receipt")
    args = parser.parse_args()
    try:
        if args.command == "verify-release":
            if not args.receipt:
                parser.error("--receipt is required")
            result: Any = verify_release(args.root, args.receipt)
        elif args.command == "diff":
            if not args.from_receipt or not args.to_receipt:
                parser.error("--from-receipt and --to-receipt are required")
            before = verify_release(args.root, args.from_receipt)
            after = verify_release(args.root, args.to_receipt)
            if before["engine_id"] != after["engine_id"]:
                raise EngineRegistryError("DIFF_ENGINE_ID_MISMATCH")
            left = before["source_file_sha256"]
            right = after["source_file_sha256"]
            result = {"engine_id": before["engine_id"],
                      "from": before["version"], "to": after["version"],
                      "previous_version_declared": after.get("previous_version"),
                      "contract_changed": before["contract_sha256"] != after["contract_sha256"],
                      "paths_added": sorted(set(right) - set(left)),
                      "paths_removed": sorted(set(left) - set(right)),
                      "paths_changed": sorted(k for k in set(left) & set(right) if left[k] != right[k]),
                      "source_commits": [before["source_commit_sha"], after["source_commit_sha"]]}
        elif args.command == "history":
            if not args.engine_id:
                parser.error("--engine-id is required")
            matches = [row for row in index(args.root) if row["engine_id"] == args.engine_id]
            if not matches:
                raise EngineRegistryError("ENGINE_NOT_FOUND")
            manifest = _load(args.root, matches[0]["manifest_ref"])
            result = [{"version": r["version"], "commit": r["source_commit_sha"],
                       "previous_version": r.get("previous_version"),
                       "evidence_ref": r.get("evidence_ref")}
                      for r in [verify_release(args.root, ref, expected_id=args.engine_id)
                                for ref in manifest.get("release_receipts", [])]]
        else:
            records = index(args.root)
            if args.command == "list":
                result = records
            elif args.command == "show":
                result = next((r for r in records if r["engine_id"] == args.engine_id), None)
                if result is None:
                    raise EngineRegistryError("ENGINE_NOT_FOUND")
            else:
                result = {"valid": True, "engine_count": len(records)}
        print(json.dumps(result, indent=2, sort_keys=True))
    except (EngineRegistryError, OSError, ValueError) as e:
        parser.exit(2, "HOLD_ENGINE_REGISTRY:" + str(e) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
