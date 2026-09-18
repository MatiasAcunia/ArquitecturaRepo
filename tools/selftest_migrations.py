#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATOR = ROOT / "tools" / "migrate_state.py"
VALIDATOR = ROOT / "tools" / "validate_project.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def migrate(
    control: Path,
    command: str,
    *args: str,
) -> subprocess.CompletedProcess[str]:
    return run(
        str(MIGRATOR),
        "--control-root",
        str(control),
        command,
        "--file",
        "CURRENT_BOOTSTRAP_STATE.json",
        *args,
    )


def must_pass(result: subprocess.CompletedProcess[str], label: str) -> str:
    if result.returncode != 0:
        raise AssertionError(
            f"{label} unexpectedly failed\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result.stdout


def must_fail(
    result: subprocess.CompletedProcess[str],
    label: str,
    fragment: str,
) -> str:
    combined = result.stdout + "\n" + result.stderr
    if result.returncode == 0:
        raise AssertionError(f"{label} unexpectedly passed")
    if fragment not in combined:
        raise AssertionError(
            f"{label}: expected {fragment!r}\nstdout/stderr:\n{combined}"
        )
    return combined


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def validate_project(control: Path, label: str) -> None:
    result = run(str(VALIDATOR), "--root", str(control))
    if result.returncode != 0:
        raise AssertionError(
            f"{label}: project validation failed\n{result.stdout}\n{result.stderr}"
        )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="agentic-sdlc-migration-") as tmp:
        control = Path(tmp) / "control"
        shutil.copytree(ROOT / "examples" / "active_campaign", control)

        target = control / "CURRENT_BOOTSTRAP_STATE.json"
        original = load(target)
        original_bytes = target.read_bytes()

        plan = must_pass(migrate(control, "plan"), "forward plan")
        parsed_plan = json.loads(plan)
        if parsed_plan["current_version"] != "starter-bootstrap-0.1":
            raise AssertionError("plan did not identify bootstrap v0.1")
        if parsed_plan["target_version"] != "starter-bootstrap-0.2":
            raise AssertionError("plan did not select bootstrap v0.2 as latest")
        if len(parsed_plan["steps"]) != 1:
            raise AssertionError("expected one forward migration step")
        if target.read_bytes() != original_bytes:
            raise AssertionError("plan mutated the migration target")

        forward = must_pass(migrate(control, "apply"), "forward apply")
        forward_report = json.loads(forward)
        if forward_report["status"] != "MIGRATED":
            raise AssertionError("forward migration did not report MIGRATED")

        migrated = load(target)
        if migrated["schema_version"] != "starter-bootstrap-0.2":
            raise AssertionError("forward migration did not produce bootstrap v0.2")
        if "unresolved_currentness" in migrated:
            raise AssertionError("legacy unresolved_currentness survived v0.2 migration")
        currentness = migrated["currentness"]
        expected_verified = (
            original["status"] == "READY"
            and not original["unresolved_currentness"]
        )
        if currentness["verified"] is not expected_verified:
            raise AssertionError("bootstrap verified semantics changed during migration")
        expected_verified_at = original["observed_at"] if expected_verified else None
        if currentness["verified_at"] != expected_verified_at:
            raise AssertionError("bootstrap verified_at semantics changed during migration")
        if currentness["unresolved"] != original["unresolved_currentness"]:
            raise AssertionError("unresolved currentness semantics changed during migration")
        if currentness["source_refs"] != [
            original["requirements_ref"],
            original["product_state_ref"],
        ]:
            raise AssertionError("v0.2 source_refs were not deterministically derived")

        validate_project(control, "forward migrated fixture")

        before_idempotent = target.read_bytes()
        idempotent = must_pass(migrate(control, "apply"), "idempotent apply")
        idempotent_report = json.loads(idempotent)
        if idempotent_report["status"] != "ALREADY_AT_TARGET":
            raise AssertionError("second apply should be ALREADY_AT_TARGET")
        if target.read_bytes() != before_idempotent:
            raise AssertionError("idempotent apply rewrote the target")

        reverse = must_pass(
            migrate(
                control,
                "apply",
                "--target-version",
                "starter-bootstrap-0.1",
            ),
            "reverse apply",
        )
        reverse_report = json.loads(reverse)
        if reverse_report["status"] != "MIGRATED":
            raise AssertionError("reverse migration did not report MIGRATED")
        reversed_data = load(target)
        if reversed_data != original:
            raise AssertionError("reversible bootstrap migration did not restore original semantics")
        validate_project(control, "reverse migrated fixture")

        must_pass(migrate(control, "apply"), "second forward apply")
        richer = load(target)
        richer["currentness"]["source_refs"].append("CUSTOM_NEW_SOURCE.json")
        save(target, richer)
        must_fail(
            migrate(
                control,
                "apply",
                "--target-version",
                "starter-bootstrap-0.1",
            ),
            "lossy reverse",
            "not representable by v0.1",
        )
        if "CUSTOM_NEW_SOURCE.json" not in load(target)["currentness"]["source_refs"]:
            raise AssertionError("failed reverse overwrote richer v0.2 state")

        must_fail(
            migrate(
                control,
                "plan",
                "--target-version",
                "starter-bootstrap-9.9",
            ),
            "unsupported target",
            "no registered migration path",
        )

        # Restore a representable v0.2 state, then prove campaign transaction currentness blocks migration.
        richer["currentness"]["source_refs"] = [
            richer["requirements_ref"],
            richer["product_state_ref"],
        ]
        save(target, richer)
        journal = control / "runtime" / "transactions" / "CURRENT_TRANSACTION.json"
        journal.parent.mkdir(parents=True, exist_ok=True)
        journal.write_text("{}\n", encoding="utf-8")
        must_fail(
            migrate(
                control,
                "apply",
                "--target-version",
                "starter-bootstrap-0.1",
            ),
            "pending transaction block",
            "pending campaign transaction blocks schema migration",
        )
        journal.unlink()

        final_reverse = must_pass(
            migrate(
                control,
                "apply",
                "--target-version",
                "starter-bootstrap-0.1",
            ),
            "final reverse",
        )
        if json.loads(final_reverse)["status"] != "MIGRATED":
            raise AssertionError("final reverse did not migrate")
        validate_project(control, "final legacy fixture")

    print("SCHEMA MIGRATION SELF-TEST PASSED")
    print("- plan is read-only")
    print("- bootstrap v0.1 -> v0.2 validated")
    print("- apply is idempotent at target")
    print("- representable v0.2 -> v0.1 round-trip is exact")
    print("- richer v0.2 downgrade fails closed")
    print("- unsupported target fails closed")
    print("- pending campaign transaction blocks migration")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
