#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTL = ROOT / "tools" / "campaignctl.py"
VALIDATOR = ROOT / "tools" / "validate_project.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def ctl(control: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return run(str(CTL), "--control-root", str(control), *args)


def must_pass(control: Path, *args: str) -> str:
    result = ctl(control, *args)
    if result.returncode != 0:
        raise AssertionError(
            f"campaignctl unexpectedly failed: {' '.join(args)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result.stdout


def must_fail(control: Path, fragment: str, *args: str) -> None:
    result = ctl(control, *args)
    combined = result.stdout + "\n" + result.stderr
    if result.returncode == 0:
        raise AssertionError(f"campaignctl unexpectedly passed: {' '.join(args)}")
    if fragment not in combined:
        raise AssertionError(
            f"expected failure fragment {fragment!r} for {' '.join(args)}\n{combined}"
        )


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="agentic-sdlc-runtime-") as tmp:
        control = Path(tmp) / "control"
        shutil.copytree(ROOT / "examples" / "active_campaign", control)

        registry_path = control / "IDENTITY_REGISTRY_CURRENT.json"
        registry = load(registry_path)
        registry["actors"].append(
            {
                "actor_id": "REVIEWER_NOTE_API_001",
                "role_class": "I4_EXECUTION_TEAM_MEMBER",
                "scope": "CAMPAIGN_API_001",
                "status": "ACTIVE",
                "current_run_id": "RUN_REVIEW_001",
                "supersedes_actor_id": None,
            }
        )
        save(registry_path, registry)

        # campaignctl expects canonical state/ paths; normalize the synthetic fixture.
        state_dir = control / "state"
        state_dir.mkdir()
        for name in [
            "PRODUCT_STATE_CURRENT.json",
            "CURRENT_BOOTSTRAP_STATE.json",
            "IDENTITY_REGISTRY_CURRENT.json",
            "EXECUTION_AUTHORITY_CURRENT.json",
        ]:
            shutil.move(str(control / name), str(state_dir / name))

        # Keep Currentness Set references valid after moving canonical state.
        ps_path = state_dir / "PRODUCT_STATE_CURRENT.json"
        ps = load(ps_path)
        ps["currentness_set"] = [
            "state/PRODUCT_STATE_CURRENT.json",
            "state/CURRENT_BOOTSTRAP_STATE.json",
            "state/IDENTITY_REGISTRY_CURRENT.json",
            "state/EXECUTION_AUTHORITY_CURRENT.json",
            "CLIENT_REQUIREMENTS_CURRENT.md",
            "CAMPAIGN_API_001_CHARTER.json",
            "CHECKPOINT_API_002.json",
        ]
        save(ps_path, ps)

        bs_path = state_dir / "CURRENT_BOOTSTRAP_STATE.json"
        bs = load(bs_path)
        bs["requirements_ref"] = "CLIENT_REQUIREMENTS_CURRENT.md"
        bs["product_state_ref"] = "state/PRODUCT_STATE_CURRENT.json"
        save(bs_path, bs)

        must_pass(
            control,
            "init",
            "--charter",
            "CAMPAIGN_API_001_CHARTER.json",
        )

        lock_path = control / "runtime" / ".campaignctl.lock"
        lock_handle = open(lock_path, "a+b")
        try:
            if os.name == "nt":
                import msvcrt

                lock_handle.seek(0, os.SEEK_END)
                if lock_handle.tell() == 0:
                    lock_handle.write(b"0")
                    lock_handle.flush()
                lock_handle.seek(0)
                msvcrt.locking(lock_handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

            must_fail(
                control,
                "campaign lock busy",
                "--lock-timeout",
                "0.10",
                "add",
                "--id",
                "LOCK_PROBE",
                "--title",
                "Must not mutate while another controller holds the lock",
            )
        finally:
            if os.name == "nt":
                import msvcrt

                lock_handle.seek(0)
                msvcrt.locking(lock_handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)
            lock_handle.close()

        must_pass(
            control,
            "add",
            "--id",
            "W1",
            "--title",
            "Implement storage-safe create path",
            "--priority",
            "100",
            "--write",
            "src/note.py",
            "--resource",
            "db:notes",
        )
        must_pass(
            control,
            "add",
            "--id",
            "W2",
            "--title",
            "Integrate read path",
            "--priority",
            "90",
            "--write",
            "src/note.py",
        )
        must_pass(
            control,
            "add",
            "--id",
            "W_RESOURCE",
            "--title",
            "Independent shared-resource mutation",
            "--priority",
            "85",
            "--write",
            "src/other.py",
            "--resource",
            "db:notes",
        )
        must_pass(
            control,
            "start",
            "--id",
            "W1",
            "--actor",
            "BUILDER_A",
            "--run",
            "RUN_BUILD_001",
        )
        must_fail(
            control,
            "write-surface conflict",
            "start",
            "--id",
            "W2",
            "--actor",
            "BUILDER_B",
            "--run",
            "RUN_BUILD_002",
        )
        must_fail(
            control,
            "shared-resource conflict",
            "start",
            "--id",
            "W_RESOURCE",
            "--actor",
            "BUILDER_RESOURCE",
            "--run",
            "RUN_BUILD_RESOURCE",
        )
        must_pass(
            control,
            "cancel",
            "--id",
            "W_RESOURCE",
            "--note",
            "Synthetic resource-conflict probe completed.",
        )
        must_pass(
            control,
            "verify",
            "--id",
            "W1",
            "--evidence",
            "evidence/w1-unit",
        )
        must_pass(
            control,
            "done",
            "--id",
            "W1",
            "--result-ref",
            "result/w1",
            "--evidence",
            "evidence/w1-integration",
        )

        must_pass(
            control,
            "authority-release",
            "--actor",
            "CAMPAIGN_LEAD_NOTE_API_001",
            "--run",
            "RUN_I3_002",
        )
        must_fail(
            control,
            "execution authority exists but is not ACTIVE",
            "add",
            "--id",
            "W3",
            "--title",
            "Dependent runtime verification",
        )
        must_pass(
            control,
            "authority-acquire",
            "--actor",
            "CAMPAIGN_LEAD_NOTE_API_001",
            "--run",
            "RUN_I3_002",
        )

        must_pass(
            control,
            "add",
            "--id",
            "W3",
            "--title",
            "Dependent runtime verification",
            "--priority",
            "80",
            "--depends",
            "W2",
        )
        must_fail(
            control,
            "expected READY, found BLOCKED_DEPENDENCY",
            "start",
            "--id",
            "W3",
            "--actor",
            "BUILDER_C",
            "--run",
            "RUN_BUILD_003",
        )

        must_pass(control, "capacity", "--reason", "synthetic capacity interruption")
        must_fail(
            control,
            "campaign is not ACTIVE",
            "start",
            "--id",
            "W2",
            "--actor",
            "BUILDER_B",
            "--run",
            "RUN_BUILD_002",
        )
        must_pass(control, "resume")

        must_pass(
            control,
            "start",
            "--id",
            "W2",
            "--actor",
            "BUILDER_B",
            "--run",
            "RUN_BUILD_002",
        )
        must_pass(
            control,
            "verify",
            "--id",
            "W2",
            "--evidence",
            "evidence/w2-unit",
        )
        must_pass(
            control,
            "done",
            "--id",
            "W2",
            "--result-ref",
            "result/w2",
            "--evidence",
            "evidence/w2-integration",
        )
        must_pass(
            control,
            "cancel",
            "--id",
            "W3",
            "--note",
            "Synthetic branch no longer needed after integration evidence.",
        )

        must_pass(
            control,
            "checkpoint",
            "--integrated-ref",
            "candidate/ref-runtime-003",
            "--summary",
            "Create/read integration complete on synthetic candidate.",
        )

        authority = load(state_dir / "EXECUTION_AUTHORITY_CURRENT.json")
        if authority["checkpoint_ref"] != "CHECKPOINT_0001":
            raise AssertionError("checkpoint did not reconcile active execution authority")

        must_pass(
            control,
            "freeze",
            "--candidate-ref",
            "candidate/ref-runtime-003",
        )
        must_pass(
            control,
            "review",
            "--reviewer",
            "REVIEWER_NOTE_API_001",
            "--run",
            "RUN_REVIEW_001",
            "--verdict",
            "PASS_FOR_STRATEGIC_RETURN",
            "--evidence",
            "evidence/review-001",
        )

        # Any new tactical work after review must invalidate the favorable freeze.
        must_pass(
            control,
            "add",
            "--id",
            "W4",
            "--title",
            "Late discovered cleanup work",
            "--priority",
            "10",
        )
        must_fail(
            control,
            "readiness terminal requires REVIEWED exact-candidate freeze",
            "terminal",
            "--type",
            "CAPABILITY_READY_FOR_PLANNER_ACCEPTANCE",
            "--reason",
            "Should fail because review was invalidated.",
        )
        must_pass(
            control,
            "cancel",
            "--id",
            "W4",
            "--note",
            "Synthetic late work intentionally cancelled.",
        )

        must_pass(
            control,
            "freeze",
            "--candidate-ref",
            "candidate/ref-runtime-003",
        )
        must_pass(
            control,
            "review",
            "--reviewer",
            "REVIEWER_NOTE_API_001",
            "--run",
            "RUN_REVIEW_001",
            "--verdict",
            "PASS_FOR_STRATEGIC_RETURN",
            "--evidence",
            "evidence/review-002",
        )
        must_pass(
            control,
            "terminal",
            "--type",
            "CAPABILITY_READY_FOR_PLANNER_ACCEPTANCE",
            "--reason",
            "Synthetic exact candidate is ready for Planner review.",
        )
        must_pass(
            control,
            "authority-release",
            "--actor",
            "CAMPAIGN_LEAD_NOTE_API_001",
            "--run",
            "RUN_I3_002",
        )

        validation = run(str(VALIDATOR), "--root", str(control))
        if validation.returncode != 0:
            raise AssertionError(
                "final runtime fixture failed independent validation\n"
                + validation.stdout
                + "\n"
                + validation.stderr
            )

        runtime = load(control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json")
        if runtime["campaign_status"] != "STRATEGIC_TERMINAL":
            raise AssertionError("runtime did not reach strategic terminal")
        if runtime["review_freeze"]["status"] != "REVIEWED":
            raise AssertionError("final review freeze is not REVIEWED")
        if runtime["terminal_request"]["terminal_type"] != (
            "CAPABILITY_READY_FOR_PLANNER_ACCEPTANCE"
        ):
            raise AssertionError("wrong terminal type")
        if runtime["revision"] != len(runtime["event_log"]):
            raise AssertionError("runtime revision/event-log invariant broken")

    print("CAMPAIGN RUNTIME SELF-TEST PASSED")
    print("- concurrent mutation lock enforced")
    print("- write-surface conflict rejected")
    print("- shared-resource conflict rejected")
    print("- dependency blocking/release verified")
    print("- capacity checkpoint/resume verified")
    print("- authority release/reacquire verified")
    print("- checkpoint currentness reconciled")
    print("- review freeze invalidation verified")
    print("- exact-candidate strategic terminal verified")
    print("- final runtime passed independent project validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
