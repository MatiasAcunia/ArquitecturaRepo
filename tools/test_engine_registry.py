"""Offline engine registry identity and version admission tests."""
from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path

from engine_registry import EngineRegistryError, index, navigation_index
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

    def test_portable_navigation_resolves_registered_engine(self):
        rows = navigation_index(Path(__file__).resolve().parents[1])
        self.assertEqual([r["engine_id"] for r in rows],
                         ["arquitectura.portable-goal-engineering"])
        self.assertEqual(rows[0]["navigation_gaps"], [])
        self.assertEqual(rows[0]["scope"],
                         "READ_ONLY_PATH_NAVIGATION__NOT_LIVE_STATE_OR_RELEASE_VERIFICATION")

    def test_navigation_handles_mixed_engine_schema_and_rejects_catalog_drift(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            folder = root / "engines" / "legacy"
            folder.mkdir(parents=True)
            (root / "src").mkdir()
            (root / "src" / "engine.py").write_text("def run(): pass\n", encoding="utf-8")
            (folder / "CONTRACT.md").write_text("bounded contract\n", encoding="utf-8")
            (root / "state").mkdir()
            (root / "state" / "CURRENT.json").write_text("{}\n", encoding="utf-8")
            payload = {"schema": "tro-engine-manifest-v1", "engine_id": "CTR_AUTHORING",
                       "status": "HISTORICAL_ONLY", "contract": "engines/legacy/CONTRACT.md",
                       "implementation_paths": ["src/engine.py::run"]}
            (folder / "engine.json").write_text(json.dumps(payload), encoding="utf-8")
            catalog_path = root / "engines" / "catalog.json"
            catalog = {"schema": "engine-catalog-v1",
                       "manifests": ["engines/legacy/engine.json"],
                       "navigation": {"entrypoints": ["state/CURRENT.json"]}}
            catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
            rows = navigation_index(root)
            self.assertEqual(rows[0]["engine_id"], "CTR_AUTHORING")
            self.assertEqual(rows[0]["navigation_gaps"], ["TEST_OWNERSHIP_NOT_INDEXED"])
            self.assertEqual(rows[0]["navigation_entrypoints"], ["state/CURRENT.json"])
            new_folder = root / "engines" / "unindexed"
            new_folder.mkdir()
            (new_folder / "engine.json").write_text(json.dumps(dict(payload, engine_id="second")), encoding="utf-8")
            with self.assertRaisesRegex(EngineRegistryError, "ENGINE_DIRECTORY_UNREGISTERED"):
                navigation_index(root)
            catalog["manifests"].append("engines/unindexed/engine.json")
            catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
            self.assertEqual(len(navigation_index(root)), 2)
            catalog["navigation"]["entrypoints"] = ["../outside"]
            catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
            with self.assertRaises(EngineRegistryError):
                navigation_index(root)

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
