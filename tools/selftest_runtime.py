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
        evidence_dir = control / "evidence"
        evidence_dir.mkdir()
        for name in (
            "review-001",
            "review-002",
            "review-003",
            "review-fail",
            "review-stale-run",
        ):
            (evidence_dir / name).write_text(
                f"Synthetic review evidence for candidate/ref-runtime-003: {name}\n",
                encoding="utf-8",
            )

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
        ps["active_campaign"]["checkpoint_or_terminal_ref"] = None
        ps["currentness_set"].remove("CHECKPOINT_API_002.json")
        save(ps_path, ps)

        authority_path = state_dir / "EXECUTION_AUTHORITY_CURRENT.json"
        authority = load(authority_path)
        authority["checkpoint_ref"] = None
        save(authority_path, authority)

        bs_path = state_dir / "CURRENT_BOOTSTRAP_STATE.json"
        bs = load(bs_path)
        bs["requirements_ref"] = "CLIENT_REQUIREMENTS_CURRENT.md"
        bs["product_state_ref"] = "state/PRODUCT_STATE_CURRENT.json"
        bs["active_checkpoint_or_terminal_ref"] = None
        save(bs_path, bs)

        # A checkpoint-only pointer cannot recreate the full runtime, so missing
        # runtime history must be preserved for an explicit recovery decision.
        orphan_control = Path(tmp) / "orphan_control"
        shutil.copytree(control, orphan_control)
        orphan_ps_path = orphan_control / "state" / "PRODUCT_STATE_CURRENT.json"
        orphan_ps = load(orphan_ps_path)
        orphan_ps["active_campaign"]["checkpoint_or_terminal_ref"] = "CHECKPOINT_API_002"
        save(orphan_ps_path, orphan_ps)
        orphan_init = ctl(
            orphan_control,
            "init",
            "--charter",
            "CAMPAIGN_API_001_CHARTER.json",
            "--force",
        )
        if orphan_init.returncode == 0 or (
            "does not contain a complete runtime recovery snapshot"
            not in orphan_init.stdout + orphan_init.stderr
        ):
            raise AssertionError("init accepted an orphaned checkpoint without runtime history")
        if (orphan_control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").exists():
            raise AssertionError("failed orphaned init created a replacement runtime")

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
                "lock busy",
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
        runtime_path = control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json"
        runtime_before_forced_init = runtime_path.read_bytes()
        must_fail(
            control,
            "cannot be replaced by init",
            "init",
            "--charter",
            "CAMPAIGN_API_001_CHARTER.json",
            "--force",
        )
        if runtime_path.read_bytes() != runtime_before_forced_init:
            raise AssertionError("--force init overwrote an existing campaign runtime")
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

        # I3 checkpointing must not promote the strategic/Product State gate
        # merely because one unit reached DONE.
        gate_control = Path(tmp) / "gate_control"
        shutil.copytree(control, gate_control)
        gate_ps_path = gate_control / "state" / "PRODUCT_STATE_CURRENT.json"
        gate_ps = load(gate_ps_path)
        gate_ps["current_gate"] = "STATIC_STRUCTURAL"
        save(gate_ps_path, gate_ps)
        must_pass(gate_control, "checkpoint", "--summary", "mixed work gate probe")
        if load(gate_ps_path)["current_gate"] != "STATIC_STRUCTURAL":
            raise AssertionError("checkpoint advanced Product State gate from DONE work")

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

        conflict_control = Path(tmp) / "conflict_control"
        shutil.copytree(control, conflict_control)

        crash_env = os.environ.copy()
        crash_env["AGENTIC_SDLC_TEST_CRASH_AFTER_APPLY"] = "2"
        crashed = subprocess.run(
            [
                sys.executable,
                str(CTL),
                "--control-root",
                str(control),
                "checkpoint",
                "--integrated-ref",
                "candidate/ref-runtime-003",
                "--summary",
                "Create/read integration complete on synthetic candidate.",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            env=crash_env,
        )
        if crashed.returncode != 91:
            raise AssertionError(
                "checkpoint fault injection did not terminate at the requested boundary\n"
                + crashed.stdout
                + "\n"
                + crashed.stderr
            )

        journal = control / "runtime" / "transactions" / "CURRENT_TRANSACTION.json"
        if not journal.exists():
            raise AssertionError("fault-injected checkpoint did not leave a recovery journal")

        pending_validation = run(str(VALIDATOR), "--root", str(control))
        pending_output = pending_validation.stdout + "\n" + pending_validation.stderr
        if pending_validation.returncode == 0:
            raise AssertionError("validator accepted a pending multi-file transaction")
        if "pending multi-file transition" not in pending_output:
            raise AssertionError(
                "validator did not identify the pending transition journal\n"
                + pending_output
            )

        must_fail(
            control,
            "pending transition journal",
            "show",
        )
        must_pass(control, "recover")
        if journal.exists():
            raise AssertionError("successful recovery left CURRENT_TRANSACTION.json behind")

        recovered_validation = run(str(VALIDATOR), "--root", str(control))
        if recovered_validation.returncode != 0:
            raise AssertionError(
                "recovered checkpoint failed independent validation\n"
                + recovered_validation.stdout
                + "\n"
                + recovered_validation.stderr
            )

        # Stale/missing canonical Product State must block all lifecycle writes
        # before runtime or authority records are touched.
        stale_control = Path(tmp) / "stale_product_control"
        shutil.copytree(control, stale_control)
        stale_ps_path = stale_control / "state" / "PRODUCT_STATE_CURRENT.json"
        stale_ps = load(stale_ps_path)
        stale_ps["current_code_ref"] = "stale/product-ref"
        save(stale_ps_path, stale_ps)
        stale_runtime_path = stale_control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json"
        stale_runtime_before = stale_runtime_path.read_bytes()
        stale_mutations = [
            ("add", "--id", "STALE_ADD", "--title", "Must not write"),
            ("checkpoint",),
            ("review", "--reviewer", "REVIEWER_NOTE_API_001", "--run", "RUN_REVIEW_001", "--verdict", "PASS_FOR_STRATEGIC_RETURN"),
            ("terminal", "--type", "CAPABILITY_READY_FOR_PLANNER_ACCEPTANCE", "--reason", "Must not write"),
            ("authority-acquire", "--actor", "CAMPAIGN_LEAD_NOTE_API_001", "--run", "RUN_I3_002"),
            ("authority-release", "--actor", "CAMPAIGN_LEAD_NOTE_API_001", "--run", "RUN_I3_002"),
        ]
        for command in stale_mutations:
            must_fail(stale_control, "Product State current_code_ref", *command)
            if stale_runtime_path.read_bytes() != stale_runtime_before:
                raise AssertionError(f"stale Product State command mutated runtime: {command[0]}")
        missing_ps_control = Path(tmp) / "missing_product_control"
        shutil.copytree(control, missing_ps_control)
        (missing_ps_control / "state" / "PRODUCT_STATE_CURRENT.json").unlink()
        must_fail(
            missing_ps_control,
            "Product State is missing",
            "add",
            "--id",
            "NO_PRODUCT_STATE",
            "--title",
            "Must fail closed",
        )

        authority = load(state_dir / "EXECUTION_AUTHORITY_CURRENT.json")
        if authority["checkpoint_ref"] != "CHECKPOINT_0001":
            raise AssertionError("checkpoint did not reconcile active execution authority")

        conflict_env = os.environ.copy()
        conflict_env["AGENTIC_SDLC_TEST_CRASH_AFTER_APPLY"] = "1"
        conflict_crash = subprocess.run(
            [
                sys.executable,
                str(CTL),
                "--control-root",
                str(conflict_control),
                "checkpoint",
                "--integrated-ref",
                "candidate/ref-conflict-004",
                "--summary",
                "Synthetic conflict recovery probe.",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            env=conflict_env,
        )
        if conflict_crash.returncode != 91:
            raise AssertionError("conflict fixture did not crash after the first applied target")

        conflict_runtime_path = (
            conflict_control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json"
        )
        external_runtime = load(conflict_runtime_path)
        external_runtime["campaign_falsifiers"].append("EXTERNAL_INTERFERENCE_PROBE")
        save(conflict_runtime_path, external_runtime)

        conflict_recovery = ctl(conflict_control, "recover")
        conflict_output = conflict_recovery.stdout + "\n" + conflict_recovery.stderr
        if conflict_recovery.returncode == 0:
            raise AssertionError("recovery overwrote an externally modified transaction target")
        if "neither transaction before nor after state" not in conflict_output:
            raise AssertionError(
                "recovery did not report the external-hash conflict\n" + conflict_output
            )

        preserved = load(conflict_runtime_path)
        if "EXTERNAL_INTERFERENCE_PROBE" not in preserved["campaign_falsifiers"]:
            raise AssertionError("conflict recovery overwrote external runtime state")

        conflict_journal = load(
            conflict_control
            / "runtime"
            / "transactions"
            / "CURRENT_TRANSACTION.json"
        )
        if conflict_journal["status"] != "CONFLICT":
            raise AssertionError("conflicted transaction was not persisted as CONFLICT")

        must_pass(
            control,
            "freeze",
            "--candidate-ref",
            "candidate/ref-runtime-003",
        )
        must_fail(
            control,
            "!= registry current_run_id",
            "review",
            "--reviewer",
            "REVIEWER_NOTE_API_001",
            "--run",
            "RUN_REVIEW_STALE",
            "--verdict",
            "PASS_FOR_STRATEGIC_RETURN",
            "--evidence",
            "evidence/review-stale-run",
        )
        must_fail(
            control,
            "review evidence must resolve to a regular file",
            "review",
            "--reviewer",
            "REVIEWER_NOTE_API_001",
            "--run",
            "RUN_REVIEW_001",
            "--verdict",
            "PASS_FOR_STRATEGIC_RETURN",
            "--evidence",
            "evidence/missing-review-file",
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

        evidence_drift_control = Path(tmp) / "evidence_drift_control"
        shutil.copytree(control, evidence_drift_control)
        drifted_evidence = evidence_drift_control / "evidence" / "review-001"
        drifted_evidence.write_text(
            drifted_evidence.read_text(encoding="utf-8") + "changed after review\n",
            encoding="utf-8",
        )
        evidence_drift_validation = run(
            str(VALIDATOR), "--root", str(evidence_drift_control)
        )
        if evidence_drift_validation.returncode == 0 or (
            "REVIEWED freeze evidence digest mismatch"
            not in evidence_drift_validation.stdout + evidence_drift_validation.stderr
        ):
            raise AssertionError(
                "independent validator did not reject changed review evidence"
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
            "FAIL",
            "--evidence",
            "evidence/review-fail",
        )
        must_fail(
            control,
            "verdict PASS_FOR_STRATEGIC_RETURN",
            "terminal",
            "--type",
            "CAPABILITY_READY_FOR_PLANNER_ACCEPTANCE",
            "--reason",
            "A failed exact-candidate review cannot authorize readiness.",
        )
        failed_terminal_control = Path(tmp) / "failed_review_terminal_control"
        shutil.copytree(control, failed_terminal_control)
        failed_runtime_path = (
            failed_terminal_control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json"
        )
        failed_runtime = load(failed_runtime_path)
        failed_runtime["campaign_status"] = "STRATEGIC_TERMINAL"
        failed_runtime["terminal_request"] = {
            "terminal_type": "CAPABILITY_READY_FOR_PLANNER_ACCEPTANCE",
            "reason": "Adversarial validator fixture with a failed review.",
            "created_at": failed_runtime["updated_at"],
        }
        failed_runtime["event_log"].append(
            {
                "seq": len(failed_runtime["event_log"]) + 1,
                "at": failed_runtime["updated_at"],
                "action": "STRATEGIC_TERMINAL_REQUESTED",
                "work_unit_id": None,
                "actor_id": None,
                "details": {
                    "terminal_type": "CAPABILITY_READY_FOR_PLANNER_ACCEPTANCE",
                    "reason": "Adversarial validator fixture with a failed review.",
                },
            }
        )
        failed_runtime["revision"] = len(failed_runtime["event_log"])
        save(failed_runtime_path, failed_runtime)
        failed_validation = run(
            str(VALIDATOR), "--root", str(failed_terminal_control)
        )
        failed_validation_output = failed_validation.stdout + failed_validation.stderr
        if failed_validation.returncode == 0 or (
            "verdict PASS_FOR_STRATEGIC_RETURN" not in failed_validation_output
        ):
            raise AssertionError(
                "independent validator accepted a readiness terminal backed by failed review\n"
                + failed_validation_output
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
            "evidence/review-003",
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
        if runtime["review_freeze"]["verdict"] != "PASS_FOR_STRATEGIC_RETURN":
            raise AssertionError("final freeze has no favorable exact-candidate verdict")
        superseded = [
            item
            for item in runtime["event_log"]
            if item["action"] == "REVIEW_FREEZE_SUPERSEDED"
            and item["details"].get("freeze", {}).get("verdict") == "FAIL"
        ]
        invalidated = [
            item
            for item in runtime["event_log"]
            if item["action"] == "REVIEW_FREEZE_INVALIDATED"
            and item["details"].get("freeze", {}).get("evidence_refs") == ["evidence/review-001"]
        ]
        if not superseded or not invalidated:
            raise AssertionError("prior reviewer verdict/evidence was lost from append-only history")
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
    print("- fault-injected checkpoint recovered by durable journal")
    print("- pending transaction rejected by independent validator")
    print("- external recovery conflict failed closed without overwrite")
    print("- checkpoint currentness reconciled")
    print("- review freeze invalidation verified")
    print("- reviewer evidence files must exist and remain byte-bound")
    print("- append-only prior reviewer identity/verdict/evidence retained")
    print("- independent validator rejects readiness terminal after failed review")
    print("- exact-candidate strategic terminal verified")
    print("- final runtime passed independent project validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
