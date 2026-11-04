#!/usr/bin/env python3
"""Build or verify the exact v1.4.0 public archive, checksum, and source receipt.

All work derives from committed HEAD. No network, provider credentials, or
GitHub publication is performed by this script.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from selftest_v14_public_readiness import SOURCE, PREFIX, test_archive, test_first_time_use

VERSION = "1.4.0"
ARCHIVE = f"ArquitecturaRepo-v{VERSION}-portable.zip"
CHECKSUM = f"{ARCHIVE}.sha256"
RECEIPT = f"ArquitecturaRepo-v{VERSION}-release-manifest.json"


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(SOURCE), *args],
        capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=45, check=False,
    )
    if result.returncode:
        raise AssertionError(f"git {' '.join(args)} failed: {result.stderr[-450:]}")
    return result.stdout.strip()


def source_identity() -> dict[str, str]:
    if (SOURCE / "VERSION").read_text(encoding="utf-8").strip() != VERSION:
        raise AssertionError("release helper is not bound to version 1.4.0")
    manifest = json.loads((SOURCE / "state/STARTER_MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("version") != VERSION or manifest.get("status") != "PUBLIC_STARTER_STABLE":
        raise AssertionError("release source manifest is not the v1.4.0 stable contract")
    if git("status", "--porcelain=v1"):
        raise AssertionError("release source is dirty; commit and verify before packaging")
    return {"source_commit_sha1": git("rev-parse", "HEAD"), "source_tree_sha1": git("rev-parse", "HEAD^{tree}")}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assert_archive(source_zip: Path) -> int:
    with tempfile.TemporaryDirectory(prefix="ar-v14-release-verify-") as tmp:
        work = Path(tmp)
        # Test from a disposable path, including extraction and a real install.
        checked = work / ARCHIVE
        shutil.copyfile(source_zip, checked)
        extracted, count = test_archive(checked, generate=False)
        test_first_time_use(extracted, work)
        return count


def build(directory: Path) -> None:
    identity = source_identity()
    directory.mkdir(parents=True, exist_ok=True)
    for name in (ARCHIVE, CHECKSUM, RECEIPT):
        if (directory / name).exists():
            raise AssertionError(f"refusing to overwrite a release output: {name}")
    with tempfile.TemporaryDirectory(prefix="ar-v14-release-build-") as tmp:
        work = Path(tmp)
        source_zip = work / ARCHIVE
        extracted, count = test_archive(source_zip)
        test_first_time_use(extracted, work)
        final = directory / ARCHIVE
        shutil.copyfile(source_zip, final)
    digest = sha256(final)
    receipt = {
        "schema_version": "architecturarepo-public-release-receipt-v1",
        "version": VERSION,
        **identity,
        "archive": ARCHIVE,
        "archive_root": PREFIX,
        "archive_sha256": digest,
        "archive_size_bytes": final.stat().st_size,
        "committed_public_file_count": count,
        "physical_gates": ["GIT_BLOB_BYTE_PARITY", "ZIP_CRC_READBACK", "FRESH_EXTRACTED_INSTALL", "NO_USER_FILE_OVERWRITE"],
        "unverified_capabilities": ["NATIVE_CODEX_DESKTOP", "THIRD_PARTY_USER_USABILITY", "PUBLIC_GHCR_VISIBILITY"],
    }
    (directory / CHECKSUM).write_text(f"{digest}  {ARCHIVE}\n", encoding="utf-8")
    (directory / RECEIPT).write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    verify(directory)
    print(f"v1.4.0 release source prepared: {count} blobs, sha256={digest}, commit={identity['source_commit_sha1']}")


def verify(directory: Path) -> None:
    identity = source_identity()
    archive = directory / ARCHIVE
    checksum = directory / CHECKSUM
    receipt = directory / RECEIPT
    if not all(path.is_file() for path in (archive, checksum, receipt)):
        raise AssertionError("published release is missing ZIP, SHA-256 or manifest")
    digest = sha256(archive)
    if checksum.read_text(encoding="utf-8") != f"{digest}  {ARCHIVE}\n":
        raise AssertionError("release checksum does not match downloaded ZIP")
    data = json.loads(receipt.read_text(encoding="utf-8"))
    if (data.get("version") != VERSION
        or any(data.get(key) != value for key, value in identity.items())
        or data.get("archive") != ARCHIVE
        or data.get("archive_root") != PREFIX
        or data.get("archive_sha256") != digest
        or data.get("archive_size_bytes") != archive.stat().st_size):
        raise AssertionError("release manifest does not bind the exact source and ZIP")
    count = assert_archive(archive)
    if data.get("committed_public_file_count") != count:
        raise AssertionError("release manifest file count differs from Git")
    print(f"v1.4.0 release download verified: {count} blobs, sha256={digest}, commit={identity['source_commit_sha1']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--build", action="store_true")
    group.add_argument("--verify", action="store_true")
    parser.add_argument("--directory", type=Path, required=True)
    args = parser.parse_args()
    if args.build:
        build(args.directory)
    else:
        verify(args.directory)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
