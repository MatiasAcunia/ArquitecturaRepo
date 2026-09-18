from __future__ import annotations

import hashlib
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


class IdempotencyConflict(ValueError):
    """Raised when one idempotency key is reused for a different payload."""


@dataclass(frozen=True)
class Note:
    note_id: int
    body: str


FaultHook = Callable[[str], None]


class NoteStore:
    """Small durable SQLite note store with request-level idempotency."""

    def __init__(
        self,
        database_path: str | Path,
        *,
        fault_hook: FaultHook | None = None,
        timeout_seconds: float = 5.0,
    ) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.fault_hook = fault_hook
        self.timeout_seconds = timeout_seconds
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.database_path,
            timeout=self.timeout_seconds,
            isolation_level=None,
        )
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS schema_meta (
                    singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
                    schema_version INTEGER NOT NULL
                )
                """
            )
            connection.execute(
                """
                INSERT INTO schema_meta(singleton, schema_version)
                VALUES (1, 1)
                ON CONFLICT(singleton) DO NOTHING
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    body TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS idempotency_requests (
                    request_id TEXT PRIMARY KEY,
                    payload_sha256 TEXT NOT NULL,
                    note_id INTEGER NOT NULL,
                    FOREIGN KEY(note_id) REFERENCES notes(note_id)
                )
                """
            )

    @staticmethod
    def _payload_hash(body: str) -> str:
        return hashlib.sha256(body.encode("utf-8")).hexdigest()

    def create_note(self, request_id: str, body: str) -> Note:
        if not request_id:
            raise ValueError("request_id must not be empty")
        if not body:
            raise ValueError("body must not be empty")

        payload_hash = self._payload_hash(body)
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            existing = connection.execute(
                """
                SELECT r.payload_sha256, n.note_id, n.body
                FROM idempotency_requests AS r
                JOIN notes AS n ON n.note_id = r.note_id
                WHERE r.request_id = ?
                """,
                (request_id,),
            ).fetchone()

            if existing is not None:
                existing_hash, note_id, existing_body = existing
                if existing_hash != payload_hash:
                    raise IdempotencyConflict(
                        f"request_id {request_id!r} was already used for a different payload"
                    )
                connection.execute("COMMIT")
                return Note(note_id=int(note_id), body=str(existing_body))

            cursor = connection.execute(
                "INSERT INTO notes(body) VALUES (?)",
                (body,),
            )
            note_id = int(cursor.lastrowid)

            if self.fault_hook is not None:
                self.fault_hook("after_note_insert")

            connection.execute(
                """
                INSERT INTO idempotency_requests(request_id, payload_sha256, note_id)
                VALUES (?, ?, ?)
                """,
                (request_id, payload_hash, note_id),
            )
            connection.execute("COMMIT")
            return Note(note_id=note_id, body=body)
        except Exception:
            try:
                connection.execute("ROLLBACK")
            except sqlite3.OperationalError:
                pass
            raise
        finally:
            connection.close()

    def get_note(self, note_id: int) -> Note | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT note_id, body FROM notes WHERE note_id = ?",
                (note_id,),
            ).fetchone()
        if row is None:
            return None
        return Note(note_id=int(row[0]), body=str(row[1]))

    def stats(self) -> dict[str, int]:
        with self._connect() as connection:
            note_count = int(connection.execute("SELECT COUNT(*) FROM notes").fetchone()[0])
            request_count = int(
                connection.execute("SELECT COUNT(*) FROM idempotency_requests").fetchone()[0]
            )
            schema_version = int(
                connection.execute(
                    "SELECT schema_version FROM schema_meta WHERE singleton = 1"
                ).fetchone()[0]
            )
        return {
            "schema_version": schema_version,
            "notes": note_count,
            "idempotency_requests": request_count,
        }
