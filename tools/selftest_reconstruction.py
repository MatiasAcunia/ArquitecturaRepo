#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
