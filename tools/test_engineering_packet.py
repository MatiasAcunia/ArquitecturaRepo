"""Offline conformance tests; never contact providers or load private user Desktop."""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from engineering_packet import build, verify, l2_input_preflight, two_zip_preflight, PacketHold
from gemini_keyfile import resolve_key, GeminiCredentialHold


def git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(root), *args],
                       capture_output=True, text=True, check=True)
    return p.stdout.strip()


class EngineeringHandoffTests(unittest.TestCase):
    def make_repo(self, root: Path) -> tuple[Path, dict]:
        repo = root / "repo"
        repo.mkdir()
        git(repo, "init", "-q")
        git(repo, "config", "user.name", "Offline Test")
        git(repo, "config", "user.email", "offline@example.test")
        (repo / "bootstrap.md").write_text("verified synthetic source\n")
        git(repo, "add", "bootstrap.md")
        git(repo, "commit", "-qm", "fixture baseline")
        spec = {
            "goal_id": "G-1", "project": "FIXTURE",
            "head_sha": git(repo, "rev-parse", "HEAD"),
            "charter_ref": "bootstrap.md", "engine_ids": ["fixture.engine"],
            "first_l4_work_order": {"goal": "implement unit output",
                                    "write_set": ["bootstrap.md"], "gate": "real test"},
            "bootstrap_text": "Synthetic full bootstrap: " + ("A" * 100),
            "files": ["bootstrap.md"],
            "cycles_proposed": [{"cycle_id": "C1", "l4_invocations_estimate": 2}],
            "authority_refs": ["bootstrap.md"], "currentness_refs": ["bootstrap.md"],
            "gates": ["unit + physical"], "unknowns": [],
        }
        return repo, spec

    def test_complete_sip_and_two_distinct_zip_readbacks(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            repo, spec = self.make_repo(root)
            sip = root / "sip.zip"
            build(repo, spec, sip)
            self.assertTrue(verify(sip)["verified"])
            self.assertEqual(two_zip_preflight(sip, None)["goal_progress"], "EXPLICITLY_ABSENT")
            historical = root / "daypack.zip"
            with zipfile.ZipFile(historical, "w") as z:
                z.writestr("CONVERSATION.md", "historical not canonical")
            result = l2_input_preflight(historical, None)
            self.assertEqual(result["daypack"]["entries"], 1)
            self.assertEqual(result["daypack"]["authority"], "HISTORICAL_EVIDENCE_ONLY")

    def test_missing_first_order_and_secret_source_fail_closed(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            repo, spec = self.make_repo(root)
            spec["first_l4_work_order"] = {}
            with self.assertRaises(PacketHold):
                build(repo, spec, root / "rejected.zip")
            spec["first_l4_work_order"] = {"goal": "a real unit"}
            spec["files"] = ["gemini4.txt"]
            with self.assertRaises(PacketHold):
                build(repo, spec, root / "rejected2.zip")

    def test_dirty_source_and_goal_mismatch_fail_closed(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            repo, spec = self.make_repo(root)
            (repo / "bootstrap.md").write_text("unsaved work")
            with self.assertRaises(PacketHold):
                build(repo, spec, root / "dirty.zip")

    def test_key_file_selection_is_explicit_not_quota_rotation(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            with patch.dict(os.environ, {"GEMINI_API_KEY": "",
                                        "AGENTIC_GEMINI_API_KEY_FILE": "",
                                        "AGENTIC_GEMINI_KEY_DIRECTORY": str(root)}):
                with self.assertRaises(GeminiCredentialHold):
                    resolve_key()
                (root / "gemini1.txt").write_text("A" * 40)
                (root / "gemini2.txt").write_text("B" * 40)
                with self.assertRaises(GeminiCredentialHold):
                    resolve_key()
                os.environ["AGENTIC_GEMINI_API_KEY_FILE"] = str(root / "gemini1.txt")
                self.assertEqual(resolve_key(), "A" * 40)


if __name__ == "__main__":
    unittest.main()
