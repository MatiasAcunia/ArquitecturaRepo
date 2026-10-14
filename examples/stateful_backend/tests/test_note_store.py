from __future__ import annotations

import sqlite3
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from app.note_store import IdempotencyConflict, NoteStore


class NoteStoreReferenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="stateful-reference-")
        self.database = Path(self.temp.name) / "notes.sqlite3"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_idempotent_replay_returns_same_note(self) -> None:
        store = NoteStore(self.database)
        first = store.create_note("request-1", "alpha")
        second = store.create_note("request-1", "alpha")

        self.assertEqual(first, second)
        self.assertEqual(store.stats()["notes"], 1)
        self.assertEqual(store.stats()["idempotency_requests"], 1)

    def test_reused_key_with_different_payload_is_rejected(self) -> None:
        store = NoteStore(self.database)
        store.create_note("request-1", "alpha")

        with self.assertRaises(IdempotencyConflict):
            store.create_note("request-1", "beta")

        self.assertEqual(store.stats()["notes"], 1)
        self.assertEqual(store.get_note(1).body, "alpha")

    def test_restart_preserves_durable_note(self) -> None:
        first_process = NoteStore(self.database)
        created = first_process.create_note("request-1", "persistent")

        second_process = NoteStore(self.database)
        recovered = second_process.get_note(created.note_id)

        self.assertEqual(recovered, created)
        self.assertEqual(second_process.stats()["schema_version"], 2)

    def test_fault_after_note_insert_rolls_back_transaction(self) -> None:
        def crash(stage: str) -> None:
            if stage == "after_note_insert":
                raise RuntimeError("synthetic process failure")

        crashing = NoteStore(self.database, fault_hook=crash)
        with self.assertRaisesRegex(RuntimeError, "synthetic process failure"):
            crashing.create_note("request-crash", "must rollback")

        recovered = NoteStore(self.database)
        self.assertEqual(recovered.stats()["notes"], 0)
        self.assertEqual(recovered.stats()["idempotency_requests"], 0)

        retry = recovered.create_note("request-crash", "must rollback")
        self.assertEqual(retry.body, "must rollback")
        self.assertEqual(recovered.stats()["notes"], 1)

    def test_concurrent_replay_creates_one_note(self) -> None:
        def create() -> int:
            return NoteStore(self.database).create_note(
                "request-concurrent",
                "same payload",
            ).note_id

        with ThreadPoolExecutor(max_workers=4) as pool:
            ids = list(pool.map(lambda _: create(), range(8)))

        self.assertEqual(len(set(ids)), 1)
        stats = NoteStore(self.database).stats()
        self.assertEqual(stats["notes"], 1)
        self.assertEqual(stats["idempotency_requests"], 1)

    def test_v1_database_migrates_atomically_and_preserves_legacy_rows(self) -> None:
        connection = sqlite3.connect(self.database)
        connection.executescript(
            """
            CREATE TABLE schema_meta (
                singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
                schema_version INTEGER NOT NULL
            );
            INSERT INTO schema_meta VALUES (1, 1);
            CREATE TABLE notes (note_id INTEGER PRIMARY KEY AUTOINCREMENT, body TEXT NOT NULL);
            INSERT INTO notes(note_id, body) VALUES (17, 'legacy durable note');
            CREATE TABLE idempotency_requests (
                request_id TEXT PRIMARY KEY, payload_sha256 TEXT NOT NULL,
                note_id INTEGER NOT NULL REFERENCES notes(note_id)
            );
            """
        )
        connection.close()

        migrated = NoteStore(self.database)
        self.assertEqual(migrated.stats()["schema_version"], 2)
        self.assertEqual(migrated.stats()["notes"], 1)
        legacy = migrated.get_note(17)
        self.assertEqual(legacy.note_id, 17)
        self.assertEqual(legacy.body, "legacy durable note")
        self.assertEqual(legacy.created_at_utc, "")

        created = migrated.create_note("after-migration", "new durable note")
        self.assertTrue(created.created_at_utc.endswith("Z"))
        restarted = NoteStore(self.database)
        self.assertEqual(restarted.get_note(17), legacy)
        self.assertEqual(restarted.get_note(created.note_id), created)
        self.assertEqual(restarted.stats()["schema_version"], 2)

    def test_invalid_inputs_are_rejected_without_persistence(self) -> None:
        store = NoteStore(self.database)
        invalid = [
            ("", "body"), ("   ", "body"), ("x" * 129, "body"),
            ("request\x00id", "body"), ("request", "   "),
            ("request", "body\x00value"), ("request", "x" * 10001),
            (None, "body"), ("request", None),
        ]
        for request_id, body in invalid:
            with self.subTest(request_id=request_id, body=body):
                with self.assertRaises(ValueError):
                    store.create_note(request_id, body)
        self.assertEqual(store.stats()["notes"], 0)
        self.assertEqual(store.stats()["idempotency_requests"], 0)

    def test_invalid_note_identifiers_are_rejected(self) -> None:
        store = NoteStore(self.database)
        for value in (0, -1, True, "1", None):
            with self.subTest(note_id=value):
                with self.assertRaises(ValueError):
                    store.get_note(value)


if __name__ == "__main__":
    unittest.main()
