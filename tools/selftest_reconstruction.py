#!/usr/bin/env python3
from __future__ import annotations

import json
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from state_tx import state_lock, write_json_set

ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD = ROOT / "tools" / "scaffold_project.py"
RECONSTRUCT = ROOT / "tools" / "reconstruct_context.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def reconstruct(root: Path) -> subprocess.CompletedProcess[str]:
    return run(str(RECONSTRUCT), "--root", str(root))


def must_reconstruct(root: Path, label: str) -> dict:
    result = reconstruct(root)
    if result.returncode != 0:
        raise AssertionError(
            f"{label}: reconstruction failed\n{result.stdout}\n{result.stderr}"
        )
    return json.loads(result.stdout)


def must_fail(root: Path, label: str, fragment: str) -> None:
    result = reconstruct(root)
    combined = result.stdout + "\n" + result.stderr
    if result.returncode == 0:
        raise AssertionError(f"{label}: reconstruction unexpectedly passed")
    if fragment not in combined:
        raise AssertionError(
            f"{label}: expected {fragment!r}\nreconstruction output:\n{combined}"
        )


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def superseding_checkpoint(root: Path) -> list[tuple[Path, dict]]:
    old = load(root / "CHECKPOINT_API_002.json")
    old["checkpoint_id"] = "CHECKPOINT_API_003"
    old["created_at"] = "2030-02-02T12:00:00Z"
    old["completed_capability_delta"] = "Integration corrected; independent review is next."
    old["rejected_approaches"] = ["Retrying the stale read identity without checking storage lineage"]
    old["current_falsifiers"] = ["fresh process cannot read the accepted note identity"]
    old["evidence_refs"].append("evidence/integration-corrected")
    old["resume_procedure"] = "Validate the corrected integration and request independent review."
    state = load(root / "PRODUCT_STATE_CURRENT.json")
    state["state_version"] = "3"
    state["active_campaign"]["checkpoint_or_terminal_ref"] = "CHECKPOINT_API_003"
    state["currentness_set"] = [
        "CHECKPOINT_API_003.json" if ref == "CHECKPOINT_API_002.json" else ref
        for ref in state["currentness_set"]
    ]
    bootstrap = load(root / "CURRENT_BOOTSTRAP_STATE.json")
    bootstrap["active_checkpoint_or_terminal_ref"] = "CHECKPOINT_API_003"
    return [
        (root / "CHECKPOINT_API_003.json", old),
        (root / "PRODUCT_STATE_CURRENT.json", state),
        (root / "CURRENT_BOOTSTRAP_STATE.json", bootstrap),
    ]


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="agentic-sdlc-reconstruct-") as tmp:
        base = Path(tmp)

        project = base / "fresh_project"
        scaffold = run(
            str(SCAFFOLD),
            "--target",
            str(project),
            "--profile",
            "STATEFUL",
            "--product-id",
            "EXAMPLE_RECONSTRUCT",
            "--objective",
            "Synthetic stateful product for fresh-context reconstruction.",
        )
        if scaffold.returncode != 0:
            raise AssertionError(
                "fresh scaffold failed\n" + scaffold.stdout + "\n" + scaffold.stderr
            )

        fresh = project / ".agentic-sdlc"
        first_result = reconstruct(fresh)
        second_result = reconstruct(fresh)
        if first_result.returncode != 0 or second_result.returncode != 0:
            raise AssertionError(
                "fresh reconstruction failed\n"
                + first_result.stdout
                + first_result.stderr
                + second_result.stdout
                + second_result.stderr
            )
        if first_result.stdout != second_result.stdout:
            raise AssertionError("reconstruction output is not deterministic")

        fresh_state = json.loads(first_result.stdout)
        if fresh_state["posture"] != "UNTRUSTED_CONTEXT":
            raise AssertionError("fresh scaffold must reconstruct UNTRUSTED_CONTEXT")
        if fresh_state["currentness"]["verified"] is not False:
            raise AssertionError("fresh scaffold reconstruction claimed verified currentness")
        if not fresh_state["currentness"]["unresolved"]:
            raise AssertionError("fresh scaffold reconstruction lost unresolved currentness")
        source = fresh_state["git_currentness"]
        if source["code_ref_relation"] != "NO_GIT_REPOSITORY":
            raise AssertionError("non-Git scaffold must not invent a repository HEAD")
        if fresh_state["continuation_preflight"]["local_source_reconciled"]:
            raise AssertionError("non-Git scaffold incorrectly passed source preflight")
        if fresh_state["continuation_preflight"]["remote_source_verified"]:
            raise AssertionError("reconstruction must not infer live remote freshness")
        owner_concerns = {
            item["concern_id"] for item in fresh_state["current_owners"]
        }
        for concern in {
            "CLIENT_REQUIREMENTS",
            "PRODUCT_STATE",
            "CURRENT_BOOTSTRAP",
            "CANONICAL_OWNER_REGISTRY",
            "TECHNICAL_BASELINE",
            "DELIVERY_PLAN",
        }:
            if concern not in owner_concerns:
                raise AssertionError(f"fresh reconstruction missing owner concern {concern}")

        if fresh_state["technical_baseline"]["status"] != "DRAFT":
            raise AssertionError("fresh scaffold technical baseline must start DRAFT")
        if fresh_state["delivery_plan"]["status"] != "DRAFT":
            raise AssertionError("fresh scaffold delivery plan must start DRAFT")

        active = must_reconstruct(
            ROOT / "examples" / "active_campaign",
            "legacy active campaign",
        )
        if active["posture"] != "EXECUTION_AUTHORIZED":
            raise AssertionError(
                f"active campaign reconstructed wrong posture: {active['posture']}"
            )
        if active["currentness"]["verified"] is not True:
            raise AssertionError("legacy READY bootstrap did not derive verified currentness")
        if active["product_state"]["active_campaign_id"] != "CAMPAIGN_API_001":
            raise AssertionError("active campaign id not reconstructed")
        if active["execution_authority"]["status"] != "ACTIVE":
            raise AssertionError("active execution authority not reconstructed")
        if active["continuation_preflight"]["remote_source_verified"]:
            raise AssertionError("legacy ACTIVE authority cannot certify live remote freshness")
        if active["continuation_preflight"]["effective_posture"] != "CURRENTNESS_RECONCILIATION_REQUIRED":
            raise AssertionError("symbolic legacy source must hold effective execution")
        handoff = active["canonical_handoff"]
        if handoff["status"] != "CHECKPOINT" or handoff["checkpoint_id"] != "CHECKPOINT_API_002":
            raise AssertionError("fresh context did not consume active checkpoint identity")
        if handoff["current_falsifiers"] != [
            "created note cannot be read by returned identity",
            "restart loses accepted note state",
        ]:
            raise AssertionError("fresh context lost active checkpoint falsifiers")
        if handoff["resume_procedure"] != (
            "Reconstruct campaign authority, verify candidate/ref-002 remains current, "
            "then continue integration verification."
        ):
            raise AssertionError("fresh context lost canonical resume procedure")
        checkpoint_path = ROOT / "examples" / "active_campaign" / handoff["source_ref"]
        if handoff["source_sha256"] != hashlib.sha256(checkpoint_path.read_bytes()).hexdigest():
            raise AssertionError("fresh context checkpoint source hash does not match readback")

        terminal = must_reconstruct(
            ROOT / "examples" / "terminal_candidate",
            "terminal candidate",
        )
        if terminal["posture"] != "STRATEGIC_RETURN_BOUNDARY":
            raise AssertionError(
                f"terminal candidate reconstructed wrong posture: {terminal['posture']}"
            )
        if terminal["product_state"]["current_gate"] != "PLANNER_ACCEPTANCE":
            raise AssertionError("terminal candidate gate not reconstructed")
        if terminal["execution_authority"]["status"] != "SUPERSEDED":
            raise AssertionError("terminal authority status not reconstructed")
        if terminal["canonical_handoff"]["status"] != "TERMINAL":
            raise AssertionError("fresh context did not consume the active terminal")
        if terminal["canonical_handoff"]["known_limitations"] != [
            "External deployment is outside this campaign."
        ]:
            raise AssertionError("fresh context lost terminal limitations")

        superseded = base / "superseded"
        shutil.copytree(ROOT / "examples" / "active_campaign", superseded)
        with state_lock(superseded):
            write_json_set(
                superseded,
                "REPLACE_ACTIVE_CHECKPOINT_E4",
                superseding_checkpoint(superseded),
            )
        latest = must_reconstruct(superseded, "checkpoint supersession/new process")
        latest_handoff = latest["canonical_handoff"]
        if latest_handoff["checkpoint_id"] != "CHECKPOINT_API_003":
            raise AssertionError("new context followed superseded checkpoint")
        if latest_handoff["rejected_approaches"] != [
            "Retrying the stale read identity without checking storage lineage"
        ]:
            raise AssertionError("rejected experiment not persisted through fresh context")
        if latest_handoff["current_falsifiers"] != [
            "fresh process cannot read the accepted note identity"
        ]:
            raise AssertionError("superseding falsifiers lost in readback")
        if latest["product_state"]["state_version"] != "3":
            raise AssertionError("Product State version not recovered")
        if latest_handoff["source_sha256"] != hashlib.sha256(
            (superseded / "CHECKPOINT_API_003.json").read_bytes()
        ).hexdigest():
            raise AssertionError("superseded source hash not bound to canonical file")

        unbound = base / "unbound"
        shutil.copytree(superseded, unbound)
        bad_state = load(unbound / "PRODUCT_STATE_CURRENT.json")
        bad_state["currentness_set"].remove("CHECKPOINT_API_003.json")
        save(unbound / "PRODUCT_STATE_CURRENT.json", bad_state)
        must_fail(unbound, "unbound checkpoint fail closed", "not in the canonical Currentness Set")

        mismatched = base / "mismatched"
        shutil.copytree(superseded, mismatched)
        old_bootstrap = load(mismatched / "CURRENT_BOOTSTRAP_STATE.json")
        old_bootstrap["active_checkpoint_or_terminal_ref"] = "CHECKPOINT_API_002"
        save(mismatched / "CURRENT_BOOTSTRAP_STATE.json", old_bootstrap)
        must_fail(mismatched, "mixed-version bootstrap fail closed", "checkpoint/terminal pointer")

        crashed = base / "crashed"
        shutil.copytree(ROOT / "examples" / "active_campaign", crashed)
        py = (
            "import sys; from pathlib import Path; "
            f"sys.path.insert(0, {str(ROOT / 'tools')!r}); "
            "from state_tx import state_lock, write_json_set; "
            f"sys.path.insert(0, {str(ROOT / 'tools')!r}); "
            "from selftest_reconstruction import superseding_checkpoint; "
            f"root = Path({str(crashed)!r}); "
            "write_json_set(root, 'CRASHED_E4', superseding_checkpoint(root))"
        )
        crashed_result = subprocess.run(
            [sys.executable, "-c", py],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            env={**os.environ, "AGENTIC_SDLC_TX_CRASH_AFTER_APPLY": "1"},
        )
        if crashed_result.returncode != 92:
            raise AssertionError(f"expected simulated crash exit 92: {crashed_result.stderr}")
        must_fail(crashed, "pending supersession fail closed", "pending multi-file transition")
        recovered = run(
            str(ROOT / "tools" / "state_tx.py"),
            "--control-root", str(crashed),
            "recover",
        )
        if recovered.returncode != 0 or "RECOVERED" not in recovered.stdout:
            raise AssertionError(f"durable state recovery failed: {recovered.stderr}")
        resumed = must_reconstruct(crashed, "post-crash new context")
        if resumed["canonical_handoff"] != latest_handoff:
            raise AssertionError("crash recovery did not restore identical continuation state")

        duplicate = base / "duplicate_owner"
        shutil.copytree(fresh, duplicate)
        registry_path = duplicate / "state" / "OWNER_REGISTRY_CURRENT.json"
        registry = load(registry_path)
        original = next(
            item
            for item in registry["owners"]
            if item["concern_id"] == "PRODUCT_STATE" and item["status"] == "CURRENT"
        )
        extra = dict(original)
        extra["owner_id"] = "OWNER_PRODUCT_STATE_DUPLICATE"
        registry["owners"].append(extra)
        save(registry_path, registry)
        must_fail(
            duplicate,
            "duplicate owner fail-closed",
            "project validation failed before reconstruction",
        )

        pending = base / "pending_transaction"
        shutil.copytree(fresh, pending)
        journal = pending / "runtime" / "transactions" / "CURRENT_TRANSACTION.json"
        journal.parent.mkdir(parents=True, exist_ok=True)
        journal.write_text(
            json.dumps(
                {
                    "schema_version": "transition-journal-0.1",
                    "transaction_id": "TX_PENDING",
                    "label": "SYNTHETIC_PENDING",
                    "status": "PREPARED",
                    "created_at": "2030-01-01T00:00:00Z",
                    "updated_at": "2030-01-01T00:00:00Z",
                    "operations": [
                        {
                            "path": "state/PRODUCT_STATE_CURRENT.json",
                            "before_exists": True,
                            "before_sha256": "0" * 64,
                            "after_sha256": "1" * 64,
                            "stage_ref": "runtime/transactions/TX_PENDING/op_0001.json",
                            "applied": False,
                        }
                    ],
                    "conflict_reason": None,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        must_fail(
            pending,
            "pending transaction fail-closed",
            "pending multi-file transition",
        )

    print("FRESH-CONTEXT RECONSTRUCTION SELF-TEST PASSED")
    print("- repeated reconstruction is deterministic")
    print("- fresh scaffold reconstructs UNTRUSTED_CONTEXT")
    print("- legacy active campaign reconstructs EXECUTION_AUTHORIZED")
    print("- terminal candidate reconstructs STRATEGIC_RETURN_BOUNDARY")
    print("- duplicate owner fails before reconstruction")
    print("- pending transaction fails before reconstruction")
    print("- non-Git source remains explicitly unverified")
    print("- canonical checkpoint/terminal facts consumed by a fresh process")
    print("- atomic checkpoint supersession preserves decisions and falsifiers")
    print("- source hashing, stale pointers and unbound currentness fail closed")
    print("- crash during multi-file supersession recovers before re-entry")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
