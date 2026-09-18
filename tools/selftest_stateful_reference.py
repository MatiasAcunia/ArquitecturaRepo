#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "examples" / "stateful_backend"
CONTROL = REFERENCE / "control"
VALIDATOR = ROOT / "tools" / "validate_project.py"
RECONSTRUCT = ROOT / "tools" / "reconstruct_context.py"


def run(
    *args: str,
    cwd: Path = ROOT,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    evidence = json.loads(
        (REFERENCE / "evidence" / "STATEFUL_REFERENCE_EVIDENCE.json").read_text(
            encoding="utf-8"
        )
    )

    app_tests = run(
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests",
        "-v",
        cwd=REFERENCE,
    )
    test_output = app_tests.stdout + "\n" + app_tests.stderr
    if app_tests.returncode != 0:
        raise AssertionError("stateful app tests failed\n" + test_output)
    expected = evidence["expected_test_count"]
    if f"Ran {expected} tests" not in test_output:
        raise AssertionError(
            f"stateful evidence expected {expected} tests but unittest output differed\n"
            + test_output
        )

    validation = run(str(VALIDATOR), "--root", str(CONTROL))
    if validation.returncode != 0:
        raise AssertionError(
            "stateful control-layer validation failed\n"
            + validation.stdout
            + "\n"
            + validation.stderr
        )

    first = run(str(RECONSTRUCT), "--root", str(CONTROL))
    second = run(str(RECONSTRUCT), "--root", str(CONTROL))
    if first.returncode != 0 or second.returncode != 0:
        raise AssertionError(
            "stateful reconstruction failed\n"
            + first.stdout
            + first.stderr
            + second.stdout
            + second.stderr
        )
    if first.stdout != second.stdout:
        raise AssertionError("stateful fresh-context reconstruction is not deterministic")

    reconstructed = json.loads(first.stdout)
    if reconstructed["posture"] != "RECONSTRUCTED_NO_ACTIVE_EXECUTION":
        raise AssertionError(
            f"unexpected stateful posture: {reconstructed['posture']}"
        )
    if reconstructed["currentness"]["verified"] is not True:
        raise AssertionError("stateful reference did not reconstruct verified currentness")
    if reconstructed["currentness"]["unresolved"] != []:
        raise AssertionError("stateful reference reconstructed unresolved currentness")
    if reconstructed["product_state"]["current_gate"] != "REFERENCE_VALIDATED":
        raise AssertionError("stateful reference current gate changed")
    if reconstructed["execution_authority"] is not None:
        raise AssertionError("stateful reference invented execution authority")
    if reconstructed["campaign_runtime"] is not None:
        raise AssertionError("stateful reference invented campaign runtime")

    owner_concerns = {
        item["concern_id"]: item for item in reconstructed["current_owners"]
    }
    for concern in {
        "CLIENT_REQUIREMENTS",
        "PRODUCT_STATE",
        "CURRENT_BOOTSTRAP",
        "CANONICAL_OWNER_REGISTRY",
        "APPLICATION_STATE_MECHANISM",
        "REFERENCE_EVIDENCE",
    }:
        if concern not in owner_concerns:
            raise AssertionError(f"stateful reconstruction missing owner {concern}")

    if (
        owner_concerns["APPLICATION_STATE_MECHANISM"]["surface_ref"]
        != "../app/note_store.py"
    ):
        raise AssertionError("stateful app mechanism owner drifted")

    with tempfile.TemporaryDirectory(prefix="stateful-reference-negative-") as tmp:
        broken = Path(tmp) / "stateful_backend"
        shutil.copytree(REFERENCE, broken)
        (broken / "app" / "note_store.py").unlink()

        broken_validation = run(
            str(VALIDATOR),
            "--root",
            str(broken / "control"),
        )
        broken_output = broken_validation.stdout + "\n" + broken_validation.stderr
        if broken_validation.returncode == 0:
            raise AssertionError(
                "validator accepted stateful reference without canonical app mechanism"
            )
        if (
            "OWNER_STATEFUL_APP_MECHANISM_001" not in broken_output
            or "../app/note_store.py" not in broken_output
        ):
            raise AssertionError(
                "missing app mechanism did not identify the canonical owner/surface\n"
                + broken_output
            )

        broken_reconstruction = run(
            str(RECONSTRUCT),
            "--root",
            str(broken / "control"),
        )
        if broken_reconstruction.returncode == 0:
            raise AssertionError(
                "reconstruction accepted stateful reference after canonical mechanism removal"
            )

    print("STATEFUL REFERENCE SELF-TEST PASSED")
    print(f"- {expected} physical SQLite tests passed")
    print("- idempotency/conflict/restart/rollback/concurrency evidenced")
    print("- control layer validated")
    print("- fresh-context reconstruction deterministic")
    print("- posture reconstructed without active execution")
    print("- custom application/evidence owners reconstructed")
    print("- removing canonical state mechanism fails closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
