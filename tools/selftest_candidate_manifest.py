#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

from candidate_manifest import (
    ManifestError,
    build_manifest,
    verify_installed_tool_parity,
    verify_manifest,
    write_new_manifest,
)
from discover_project import sha256 as discovery_sha256
from goal_guard import file_sha as goal_file_sha
from state_tx import sha256_file


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="agentic-candidate-manifest-") as temp:
        base = Path(temp)
        candidate = base / "candidate"
        candidate.mkdir()
        (candidate / "source.txt").write_text("alpha\n", encoding="utf-8")
        (candidate / "nested").mkdir()
        (candidate / "nested" / "source.py").write_text("VALUE = 7\n", encoding="utf-8")
        (candidate / ".git").mkdir()
        (candidate / ".git" / "ignored").write_text("not source\n", encoding="utf-8")
        (candidate / "__pycache__").mkdir()
        (candidate / "__pycache__" / "ignored.pyc").write_bytes(b"generated")

        first = build_manifest(candidate)
        second = build_manifest(candidate)
        if first != second or first["file_count"] != 2:
            raise AssertionError("canonical candidate manifest is not deterministic")

        portable_candidate = base / "portable-candidate"
        portable_candidate.mkdir()
        (portable_candidate / "source.txt").write_text("alpha\n", encoding="utf-8")
        (portable_candidate / "nested").mkdir()
        (portable_candidate / "nested" / "source.py").write_text(
            "VALUE = 7\n", encoding="utf-8"
        )
        (portable_candidate / ".git").write_text(
            "gitdir: D:/different/worktree/.git/worktrees/portable\n",
            encoding="utf-8",
        )
        if build_manifest(portable_candidate)["source_tree_sha256"] != first["source_tree_sha256"]:
            raise AssertionError("checkout-local .git pointer changed the source-tree digest")

        receipt = base / "evidence" / "candidate-manifest.json"
        written = write_new_manifest(candidate, receipt)
        if written != first:
            raise AssertionError("written manifest differs from canonical calculation")
        valid, problems = verify_manifest(candidate, receipt)
        if not valid or problems:
            raise AssertionError(f"new manifest did not verify: {problems}")
        try:
            write_new_manifest(candidate, receipt)
        except ManifestError as exc:
            if "refusing to overwrite" not in str(exc):
                raise
        else:
            raise AssertionError("candidate manifest silently overwrote an existing receipt")

        sample = candidate / "source.txt"
        expected = sha256_file(sample)
        if expected != discovery_sha256(sample) or expected != goal_file_sha(sample):
            raise AssertionError("source file digest implementations disagree")

        (candidate / "source.txt").write_text("changed\n", encoding="utf-8")
        valid, problems = verify_manifest(candidate, receipt)
        if valid or "FILE_SET_OR_FILE_DIGEST_MISMATCH" not in problems:
            raise AssertionError("changed candidate bytes were not detected")

        installed = base / "installed" / "tools"
        installed.mkdir(parents=True)
        for name in ("state_tx.py", "candidate_manifest.py"):
            shutil.copy2(ROOT / "tools" / name, installed / name)
        parity = verify_installed_tool_parity(ROOT, installed)
        if parity["status"] != "PASS" or len(parity["checked_tools"]) != 2:
            raise AssertionError(f"matching installed tools did not pass parity: {parity}")
        (installed / "candidate_manifest.py").write_text(
            (installed / "candidate_manifest.py").read_text(encoding="utf-8") + "\n# drift\n",
            encoding="utf-8",
        )
        parity = verify_installed_tool_parity(ROOT, installed)
        if parity["status"] != "FAIL" or not any(
            item.startswith("TOOL_DIGEST_MISMATCH:candidate_manifest.py")
            for item in parity["mismatches"]
        ):
            raise AssertionError("installed tool drift was not detected")

    print("CANDIDATE MANIFEST / TOOL PARITY SELF-TEST PASSED")
    print("- deterministic SHA-256 source-tree manifest verified")
    print("- generated directories excluded and source files bound by exact bytes")
    print("- worktree .git pointer excluded from portable source identity")
    print("- candidate manifest creation refuses receipt overwrite")
    print("- source-file hash is shared by discovery, Goal guard and transaction code")
    print("- installed/root tool parity passes and detects byte drift")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
