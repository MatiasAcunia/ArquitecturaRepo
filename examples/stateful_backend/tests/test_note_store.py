from __future__ import annotations

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
        self.assertEqual(second_process.stats()["schema_version"], 1)

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


if __name__ == "__main__":
    unittest.main()
