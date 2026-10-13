#!/usr/bin/env python3
"""Read-only logical SQLite currentness witness.

A main-file hash is NOT a full SQLite state witness with active WAL. The backup
API copies a transactionally consistent view including WAL entries into a
temporary *external* output. This helper does not checkpoint the source.
The digest is local evidence and never grants host/CLIENT execution authority.
"""
from __future__ import annotations

import hashlib
import re
import sqlite3
import tempfile
from pathlib import Path
from typing import Any

SQLITE_MAGIC = b"SQLite format 3\x00"
SHA256 = re.compile(r"^[0-9a-f]{64}$")
MAX_SOURCE_BYTES = 512 * 1024 * 1024


class SQLiteCurrentnessHold(ValueError):
    pass


def is_sqlite_database(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            return handle.read(16) == SQLITE_MAGIC
    except (OSError, ValueError):
        return False


def wal_nonempty(path: Path) -> bool:
    wal = Path(str(path) + "-wal")
    try:
        if wal.is_symlink():
            raise SQLiteCurrentnessHold("SQLITE_WAL_SYMLINK_REFUSED")
        return wal.is_file() and wal.stat().st_size > 0
    except OSError:
        raise SQLiteCurrentnessHold("SQLITE_WAL_UNREADABLE") from None


def snapshot_sha256(path: Path) -> str:
    """A bounded SQLite online-backup witness, not a file-only copy/checkpoint.

    Read-only mode is mandatory, and snapshots are ephemeral. SQLite may use
    existing shared-memory WAL coordination on a live source. For a protected
    project, run against an explicitly authorized disposable source copy.
    """
    if path.is_symlink() or not path.is_file() or not is_sqlite_database(path):
        raise SQLiteCurrentnessHold("SQLITE_SOURCE_MISSING_OR_INVALID")
    if path.stat().st_size > MAX_SOURCE_BYTES:
        raise SQLiteCurrentnessHold("SQLITE_SOURCE_EXCEEDS_BOUNDED_AUDIT")
    try:
        with tempfile.TemporaryDirectory(prefix="agentic-sqlite-snapshot-") as temp:
            output = Path(temp) / "currentness.sqlite"
            with sqlite3.connect(path.resolve().as_uri() + "?mode=ro",
                                 uri=True, timeout=2.0) as source:
                source.execute("PRAGMA query_only=ON")
                source.execute("PRAGMA busy_timeout=2000")
                with sqlite3.connect(output, timeout=2.0) as destination:
                    attempts = [0]
                    def bounded_progress(status: int, remaining: int, total: int) -> None:
                        attempts[0] += 1
                        if attempts[0] > 200000:
                            raise SQLiteCurrentnessHold("SQLITE_BACKUP_BOUND_EXCEEDED")
                    source.backup(destination, pages=256, progress=bounded_progress,
                                  sleep=0.01)
                    result = destination.execute("PRAGMA quick_check").fetchone()
                    if result != ("ok",):
                        raise SQLiteCurrentnessHold("SQLITE_SNAPSHOT_INTEGRITY_HOLD")
            digest = hashlib.sha256()
            with output.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            return digest.hexdigest()
    except (sqlite3.Error, OSError, RuntimeError) as exc:
        raise SQLiteCurrentnessHold(
            "SQLITE_SNAPSHOT_UNVERIFIABLE:" + type(exc).__name__
        ) from None


def inspect_store(path: Path, record: dict[str, Any]) -> list[str]:
    """Return exact local failure codes; caller owns Goal validity and HOLD."""
    failures: list[str] = []
    try:
        expected = record.get("sqlite_snapshot_sha256")
        has_snapshot = expected is not None
        valid_db = is_sqlite_database(path)
        wal_exists = wal_nonempty(path)
        if wal_exists and not has_snapshot:
            failures.append("SQLITE_WAL_CURRENTNESS_UNBOUND")
        if has_snapshot:
            if not isinstance(expected, str) or not SHA256.fullmatch(expected):
                failures.append("SQLITE_SNAPSHOT_DIGEST_INVALID")
            elif not valid_db:
                failures.append("SQLITE_SNAPSHOT_SOURCE_INVALID")
            else:
                actual = snapshot_sha256(path)
                if actual != expected:
                    failures.append("SQLITE_SNAPSHOT_STALE")
    except SQLiteCurrentnessHold as exc:
        failures.append(str(exc))
    return failures


if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument("--sqlite-source", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = {
            "status": "LOCAL_SNAPSHOT_OBSERVED_NOT_HOST_AUTHORIZED",
            "sqlite_snapshot_sha256": snapshot_sha256(args.sqlite_source),
            "may_execute_material_goal": False,
        }
    except SQLiteCurrentnessHold as exc:
        result = {"status": "HOLD", "failure_codes": [str(exc)],
                  "may_execute_material_goal": False}
    print(json.dumps(result, indent=2))
    raise SystemExit(2 if result["status"] == "HOLD" else 0)
