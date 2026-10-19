"""Offline engine registry identity and version admission tests."""
from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path

from engine_registry import EngineRegistryError, index
from cognitive_i4 import CognitiveHold, consult_public_or_synthetic


class EngineRegistryTests(unittest.TestCase):
    def test_registered_portable_engine(self):
        root = Path(__file__).resolve().parents[1]
        rows = index(root)
        self.assertTrue(any(row["engine_id"] == "arquitectura.portable-goal-engineering" for row in rows))
        record = next(row for row in rows if row["engine_id"] == "arquitectura.portable-goal-engineering")
        self.assertIsNone(record["adopted_version"])
        self.assertFalse(record["releases"])
        self.assertEqual(record["candidates"], ["0.1.0-candidate.1", "0.1.0-candidate.2"])

    def test_invalid_catalog_file_is_not_authority(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / "engines").mkdir()
            (root / "engines" / "catalog.json").write_text(json.dumps({
                "schema": "engine-catalog-v1", "manifests": ["../../outside.json"]
            }))
            with self.assertRaises(EngineRegistryError):
                index(root)

    def test_provider_effect_fails_closed_without_cost_attestation(self):
        with self.assertRaises(CognitiveHold) as e:
            consult_public_or_synthetic(
                model="gemini-synthetic-test",
                question="Propose a safe synthetic unit test suite",
                export_classification="PUBLIC_OR_SYNTHETIC",
                engineering_role="test_generation",
                transport=lambda request, timeout: self.fail("MUST_NOT_CONTACT_PROVIDER"),
            )
        self.assertIn("HOLD_GEMINI_COST_NOT_VERIFIED", str(e.exception))


if __name__ == "__main__":
    unittest.main()
