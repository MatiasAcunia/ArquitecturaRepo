#!/usr/bin/env python3
"""Create and verify unique, byte-bound source manifests for local candidates."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

from state_tx import sha256_file


SCHEMA = "agentic-candidate-source-manifest-v1"
ALGORITHM = "sha256(path-nul-bytes-nul-file-sha256-newline)"
EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache", ".hypothesis", ".mypy_cache", ".ruff_cache", ".venv", "venv", "node_modules"}
SHA256 = re.compile(r"^[0-9a-f]{64}$")


class ManifestError(ValueError):
    pass


def canonical_tree_digest(entries: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    seen: set[str] = set()
    for entry in sorted(entries, key=lambda item: item["path"]):
        relative = entry.get("path")
        size = entry.get("bytes")
        file_digest = entry.get("sha256")
        if not isinstance(relative, str) or not relative or "\\" in relative:
            raise ManifestError("manifest path must be a non-empty POSIX relative path")
        path = Path(relative)
        if path.is_absolute() or any(part in {"", ".", ".."} for part in relative.split("/")):
            raise ManifestError(f"unsafe manifest path: {relative!r}")
        folded = relative.casefold()
        if folded in seen:
            raise ManifestError(f"duplicate/case-colliding manifest path: {relative!r}")
        seen.add(folded)
        if not isinstance(size, int) or size < 0 or not isinstance(file_digest, str) or not SHA256.fullmatch(file_digest):
            raise ManifestError(f"invalid size or SHA-256 for {relative!r}")
        digest.update(relative.encode("utf-8") + b"\0")
        digest.update(str(size).encode("ascii") + b"\0")
        digest.update(file_digest.encode("ascii") + b"\n")
    return digest.hexdigest()


def build_manifest(root: Path, *, exclude_paths: tuple[str, ...] = ()) -> dict[str, Any]:
    root = root.resolve()
    if not root.is_dir():
        raise ManifestError(f"candidate root is not a directory: {root}")
    for excluded in exclude_paths:
        if (not isinstance(excluded, str) or not excluded or "\\" in excluded
            or Path(excluded).is_absolute()
            or any(part in {"", ".", ".."} for part in excluded.split("/"))):
            raise ManifestError(f"unsafe excluded path: {excluded!r}")
    excluded_paths = tuple(exclude_paths)

    def excluded(relative: str) -> bool:
        return any(relative == item or relative.startswith(item + "/") for item in excluded_paths)

    entries: list[dict[str, Any]] = []
    for current, directories, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        kept: list[str] = []
        for name in sorted(directories):
            directory = current_path / name
            relative_directory = directory.relative_to(root).as_posix()
            if excluded(relative_directory):
                continue
            if name.casefold() in EXCLUDED_DIRS:
                continue
            if directory.is_symlink():
                raise ManifestError(f"symlinked candidate directory is unsupported: {directory.relative_to(root)}")
            kept.append(name)
        directories[:] = kept
        for name in sorted(files):
            path = current_path / name
            relative = path.relative_to(root).as_posix()
            if excluded(relative):
                continue
            if relative.casefold() == ".git":
                # Worktrees store a location-specific gitdir pointer as a file;
                # it is checkout metadata, not candidate source.
                continue
            if path.is_symlink():
                raise ManifestError(f"symlinked candidate file is unsupported: {relative}")
            if path.suffix.casefold() == ".pyc":
                continue
            before = path.stat()
            file_digest = sha256_file(path)
            after = path.stat()
            if file_digest is None or (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                raise ManifestError(f"candidate file changed during manifesting: {relative}")
            entries.append({"path": relative, "bytes": after.st_size, "sha256": file_digest})
    entries.sort(key=lambda item: item["path"])
    total_bytes = sum(item["bytes"] for item in entries)
    return {
        "schema_version": SCHEMA,
        "algorithm": ALGORITHM,
        "file_count": len(entries),
        "total_bytes": total_bytes,
        "source_tree_sha256": canonical_tree_digest(entries),
        "files": entries,
    }


def write_new_manifest(root: Path, output: Path) -> dict[str, Any]:
    root = root.resolve()
    output = output.resolve()
    try:
        output.relative_to(root)
    except ValueError:
        pass
    else:
        raise ManifestError("manifest output must be outside the candidate root")
    manifest = build_manifest(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with output.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(manifest, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise ManifestError(f"refusing to overwrite existing manifest: {output}") from exc
    return manifest


def verify_manifest(root: Path, manifest_path: Path) -> tuple[bool, list[str]]:
    try:
        expected = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ManifestError(f"cannot read manifest: {exc}") from exc
    if not isinstance(expected, dict) or expected.get("schema_version") != SCHEMA:
        raise ManifestError("unsupported candidate manifest schema")
    if expected.get("algorithm") != ALGORITHM:
        raise ManifestError("unsupported candidate manifest algorithm")
    actual = build_manifest(root)
    problems: list[str] = []
    if expected.get("files") != actual["files"]:
        problems.append("FILE_SET_OR_FILE_DIGEST_MISMATCH")
    if expected.get("source_tree_sha256") != actual["source_tree_sha256"]:
        problems.append("SOURCE_TREE_DIGEST_MISMATCH")
    if expected.get("file_count") != actual["file_count"]:
        problems.append("FILE_COUNT_MISMATCH")
    if expected.get("total_bytes") != actual["total_bytes"]:
        problems.append("TOTAL_BYTES_MISMATCH")
    return not problems, problems


def verify_installed_tool_parity(root: Path, installed_tools: Path) -> dict[str, Any]:
    root_tools = root.resolve() / "tools"
    installed_tools = installed_tools.resolve()
    if not root_tools.is_dir() or not installed_tools.is_dir():
        raise ManifestError("root and installed tools directories must exist")
    checked: list[str] = []
    mismatches: list[str] = []
    for installed in sorted(installed_tools.glob("*.py")):
        if installed.is_symlink() or not installed.is_file():
            mismatches.append(f"UNSAFE_INSTALLED_TOOL:{installed.name}")
            continue
        canonical = root_tools / installed.name
        if not canonical.is_file() or canonical.is_symlink():
            mismatches.append(f"NO_CANONICAL_ROOT_TOOL:{installed.name}")
            continue
        installed_digest = sha256_file(installed)
        canonical_digest = sha256_file(canonical)
        checked.append(installed.name)
        if not installed_digest or installed_digest != canonical_digest:
            mismatches.append(f"TOOL_DIGEST_MISMATCH:{installed.name}")
    return {
        "status": "PASS" if checked and not mismatches else "FAIL",
        "checked_tools": checked,
        "mismatches": mismatches,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("create")
    create.add_argument("--root", required=True)
    create.add_argument("--output", required=True)
    verify = sub.add_parser("verify")
    verify.add_argument("--root", required=True)
    verify.add_argument("--manifest", required=True)
    parity = sub.add_parser("parity")
    parity.add_argument("--root", required=True)
    parity.add_argument("--installed-tools", required=True)
    args = parser.parse_args()
    try:
        if args.command == "create":
            result = write_new_manifest(Path(args.root), Path(args.output))
            print(json.dumps({"status": "CREATED", "file_count": result["file_count"],
                              "source_tree_sha256": result["source_tree_sha256"]}, indent=2))
            return 0
        if args.command == "verify":
            valid, problems = verify_manifest(Path(args.root), Path(args.manifest))
            print(json.dumps({"status": "PASS" if valid else "FAIL", "problems": problems}, indent=2))
            return 0 if valid else 1
        result = verify_installed_tool_parity(Path(args.root), Path(args.installed_tools))
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "PASS" else 1
    except (ManifestError, OSError) as exc:
        print(f"CANDIDATE MANIFEST FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
