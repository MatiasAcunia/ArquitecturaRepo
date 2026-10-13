#!/usr/bin/env python3
"""Real files, persisted categories, failed producers and safe GC boundaries."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from artifact_ledger import initial

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "artifact_ledger.py"


def run(project: Path, *params: str, code: int = 0) -> dict:
    result = subprocess.run(
        [sys.executable, str(TOOL), "--project", str(project), *params],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == code, (params, result.stdout, result.stderr)
    return json.loads(result.stdout)


def git(project: Path, *params: str) -> None:
    result = subprocess.run(
        ["git", "-C", str(project), *params],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="artifact-ledger-") as tmp:
        project = Path(tmp) / "repo"
        project.mkdir()
        git(project, "init", "-b", "main")
        git(project, "config", "user.name", "Example")
        git(project, "config", "user.email", "example.invalid")
        (project / "source.txt").write_text("PRODUCT_SOURCE_PRESERVED")
        git(project, "add", "source.txt")
        git(project, "commit", "-m", "initial")
        ledger = project / ".agentic-sdlc" / "runtime" / "ARTIFACT_LIFECYCLE_CURRENT.json"
        ledger.parent.mkdir(parents=True)
        ledger.write_text(json.dumps(initial()), encoding="utf-8")
        root = ".agentic-sdlc-scratch/campaign-A"
        assert run(project, "init-root", "--root", root,
                   "--owner", "I3", "--campaign", "CAMP_A")["status"] == "ROOT_REGISTERED"

        sample = project / root / "sample.bin"
        command = [sys.executable, "-c",
                   f"from pathlib import Path;Path({str(sample)!r}).write_bytes(b'sample')"]
        captured = run(project, "capture", "--root", root,
                       "--category", "DERIVED_REBUILDABLE", "--safe-delete",
                       "--ttl-hours", "-1", "--", *command)
        assert captured["registered"] == 1
        data = json.loads(ledger.read_text(encoding="utf-8"))
        assert data["files"][root + "/sample.bin"]["safe_delete"]
        assert run(project, "gc")["ready_count"] == 1 and sample.exists()
        assert run(project, "gc", "--execute")["deleted_count"] == 1
        assert not sample.exists()
        assert run(project, "gc", "--execute")["deleted_count"] == 0
        assert json.loads(ledger.read_text())["files"][root + "/sample.bin"]["status"] == "DELETED"

        failed_sample = project / root / "failed.txt"
        failing = [sys.executable, "-c",
                   f"from pathlib import Path;Path({str(failed_sample)!r}).write_text('error');raise SystemExit(7)"]
        response = run(project, "capture", "--root", root,
                       "--category", "DERIVED_REBUILDABLE", "--safe-delete",
                       "--ttl-hours", "-1", "--", *failing, code=7)
        assert response["status"] == "FAILED_OUTPUTS_QUARANTINED"
        assert failed_sample.exists()
        assert json.loads(ledger.read_text())["files"][root + "/failed.txt"]["category"] == "QUARANTINE_UNRESOLVED"

        orphan = project / root / "unregistered.bin"
        orphan.write_bytes(b"UNREGISTERED")
        assert root in run(project, "gc")["unregistered_roots"]
        assert run(project, "reconcile", "--root", root)["registered"] == 1
        assert json.loads(ledger.read_text())["files"][root + "/unregistered.bin"]["safe_delete"] is False

        mutable = project / root / "changed.txt"
        mutable.write_bytes(b"old")
        run(project, "reconcile", "--root", root)
        run(project, "classify", "--path", root + "/changed.txt",
            "--owner", "I3", "--campaign", "CAMP_A",
            "--category", "DERIVED_REBUILDABLE", "--safe-delete",
            "--ttl-hours", "-1", "--review-closed")
        mutable.write_bytes(b"NEW FILE CONTENT")
        assert run(project, "gc")["ready_count"] == 0 and mutable.exists()
        assert run(project, "reconcile", "--root", root)["changed_quarantined"] >= 1

        db = project / root / "canonical.sqlite"
        db.write_bytes(b"synthetic_fixture")
        run(project, "reconcile", "--root", root)
        run(project, "classify", "--path", root + "/canonical.sqlite",
            "--owner", "I3", "--campaign", "CAMP_A",
            "--category", "TEMP_TRANSACTION", "--safe-delete",
            "--ttl-hours", "-1", "--review-closed")
        assert run(project, "gc", "--execute")["deleted_count"] == 0
        assert db.exists()

        tracked = project / root / "tracked.bin"
        tracked.write_bytes(b"versioned")
        run(project, "reconcile", "--root", root)
        run(project, "classify", "--path", root + "/tracked.bin",
            "--owner", "I3", "--campaign", "CAMP_A",
            "--category", "DERIVED_REBUILDABLE", "--safe-delete",
            "--ttl-hours", "-1", "--review-closed")
        git(project, "add", "-f", root + "/tracked.bin")
        assert run(project, "gc", "--execute")["deleted_count"] == 0
        assert tracked.exists()

        outside = project / "secret_outside"
        outside.write_bytes(b"PRIVATE")
        link = project / root / "symlinked"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError):
            pass
        else:
            assert run(project, "gc", code=2)["status"] == "HOLD"
            assert outside.read_bytes() == b"PRIVATE"
            link.unlink()

        # Real Spanish filenames often contain accents and spaces.
        localized = project / root / "música y voz 01.mp4"
        localized.write_bytes(b"SAFE_REBUILDABLE_SAMPLE")
        run(project, "reconcile", "--root", root)
        run(project, "classify", "--path", root + "/música y voz 01.mp4",
            "--owner", "I3", "--campaign", "CAMP_A",
            "--category", "DERIVED_REBUILDABLE", "--safe-delete",
            "--ttl-hours", "-1", "--review-closed")
        assert run(project, "gc")["ready_count"] == 1
        assert run(project, "gc", "--execute")["deleted_count"] == 1
        assert not localized.exists()
        # Samples awaiting review remain protected regardless of age.
        review = project / root / "editorial_preview.mp4"
        review.write_bytes(b"PENDING_HUMAN_REVIEW")
        run(project, "reconcile", "--root", root)
        assert run(project, "gc", "--execute")["deleted_count"] == 0
        assert review.exists()
        # A crashed/other writer lock blocks mutating GC, but not read-only inspection.
        before_lock = ledger.read_bytes()
        lock = ledger.with_name(ledger.name + ".lock")
        lock.write_text("unresolved previous writer")
        assert run(project, "gc", "--execute", code=2)["status"] == "HOLD"
        assert ledger.read_bytes() == before_lock
        assert run(project, "gc")["mode"] == "dry-run"
        lock.unlink()
        # Marker corruption is never interpreted as an opportunity to clean.
        marker = project / root / ".agentic-artifact-root.json"
        original_marker = marker.read_bytes()
        marker.write_bytes(b"{}")
        assert run(project, "gc", code=2)["status"] == "HOLD"
        marker.write_bytes(original_marker)
        # Reject forged owner in ledger even though the file hash is unchanged.
        saved = ledger.read_bytes()
        forged = json.loads(saved)
        forged["files"][root + "/tracked.bin"]["owner"] = "FOREIGN"
        ledger.write_text(json.dumps(forged), encoding="utf-8")
        assert run(project, "gc", code=2)["status"] == "HOLD"
        ledger.write_bytes(saved)
        # A broken JSON file must fail closed without deleting/reconstructing it.
        ledger.write_bytes(b"{not valid JSON")
        assert run(project, "gc", code=2)["status"] == "HOLD"
        ledger.write_bytes(saved)
        assert run(project, "init-root", "--root", root,
                   "--owner", "I4", "--campaign", "FOREIGN",
                   code=2)["status"] == "HOLD"
        assert (project / "source.txt").read_text() == "PRODUCT_SOURCE_PRESERVED"
    print("ARTIFACT LEDGER PASS: persisted entries, failure quarantine, exact deletion and protected files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
