#!/usr/bin/env python3
"""Regression tests for public-starter source and privacy boundaries."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate_structure


class StructurePolicyTests(unittest.TestCase):
    def check(self, files: dict[str, str]) -> list[str]:
        with tempfile.TemporaryDirectory(prefix="starter-structure-policy-") as tmp:
            root = Path(tmp)
            for relative, content in files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            errors: list[str] = []
            with patch.object(validate_structure, "ROOT", root):
                validate_structure.validate_structure_only(errors)
            return errors

    def test_reserved_email_in_test_only(self):
        self.assertEqual(self.check({"tools/test_fixture.py": "offline@example.test"}), [])
        self.assertEqual(self.check({"tools/selftest_fixture.py": "offline@example.invalid"}), [])
        for path, address in (
            ("tools/test_fixture.py", "owner@" + "example.com"),
            ("docs/README.md", "offline@example.test"),
            ("tools/production.py", "offline@example.test"),
        ):
            with self.subTest(path=path):
                self.assertTrue(any("personal email" in error for error in self.check({path: address})))

    def test_first_party_source_history_is_precisely_scoped(self):
        commit = "a" * 40
        blob = "b" * 40
        manifest = {
            "candidates": [{
                "source_commit_sha": commit,
                "source_git_blob_sha1": {"tools/source.py": blob},
            }],
        }
        allowed = {
            "engines/portable-goal/engine.json": json.dumps(manifest, indent=2),
            "engines/portable-goal/CHANGELOG.md": f"- Exact baseline Git commit: `{commit}`.\n",
        }
        self.assertEqual(self.check(allowed), [])
        for relative, changed in (
            ("docs/source.md", f"Unrelated source identity: {commit}"),
            ("engines/portable-goal/CHANGELOG.md", f"- Arbitrary source: `{commit}`"),
            ("engines/portable-goal/engine.json", json.dumps({**manifest, "private": commit})),
        ):
            with self.subTest(relative=relative):
                self.assertTrue(any("40-char" in error for error in self.check({**allowed, relative: changed})))

    def test_root_policy_and_credentials_stay_protected(self):
        self.assertTrue(any("project-specific" in error for error in self.check({"AGENTS.md": "MUSIC"})))
        self.assertTrue(any("project-specific" in error for error in self.check({
            "templates/EXAMPLE.json": '{"unrelated_gate":"G007"}',
        })))
        self.assertTrue(any("private-key" in error for error in self.check({
            "docs/README.md": "BEGIN " + "PRIVATE KEY",
        })))


if __name__ == "__main__":
    unittest.main()
