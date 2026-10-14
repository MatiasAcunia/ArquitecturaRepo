#!/usr/bin/env python3
"""Physical WAL currentness test on a disposable SQLite fixture only."""
from __future__ import annotations

import hashlib
import sqlite3
import tempfile
from pathlib import Path

from sqlite_currentness import inspect_store, snapshot_sha256


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="sqlite-wal-currentness-") as temp:
        db = Path(temp) / "disposable.sqlite"
        connection = sqlite3.connect(db, isolation_level=None)
        try:
            assert connection.execute("PRAGMA journal_mode=WAL").fetchone()[0].lower() == "wal"
            connection.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, body TEXT NOT NULL)")
            connection.execute("INSERT INTO events(body) VALUES ('first committed transaction')")
            wal = Path(str(db) + "-wal")
            assert wal.is_file() and wal.stat().st_size > 0
            main_sha_before = sha(db)
            wal_size_before = wal.stat().st_size
            first_snapshot = snapshot_sha256(db)
            first_record = {"sqlite_snapshot_sha256": first_snapshot}
            assert inspect_store(db, first_record) == []

            connection.execute("INSERT INTO events(body) VALUES ('second WAL-only commit')")
            assert sha(db) == main_sha_before, "fixture must exercise a changed WAL with stable main-file bytes"
            assert wal.stat().st_size > wal_size_before
            second_snapshot = snapshot_sha256(db)
            assert second_snapshot != first_snapshot
            assert inspect_store(db, first_record) == ["SQLITE_SNAPSHOT_STALE"]
            assert inspect_store(db, {"sqlite_snapshot_sha256": second_snapshot}) == []

            connection.execute("BEGIN IMMEDIATE")
            connection.execute("INSERT INTO events(body) VALUES ('must roll back')")
            connection.execute("ROLLBACK")
            assert snapshot_sha256(db) == second_snapshot
            missing = Path(temp) / "missing.sqlite"
            assert inspect_store(missing, {}) == ["SQLITE_SNAPSHOT_SOURCE_INVALID"]
            assert not missing.exists(), "inspection must not synthesize a missing canonical DB"
        finally:
            connection.close()
    print("SQLITE WAL CURRENTNESS PASS: committed WAL invalidates pinned snapshot; rollback and missing-source HOLD verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
