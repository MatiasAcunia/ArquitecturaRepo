#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD = ROOT / "tools" / "scaffold_project.py"
VALIDATOR = ROOT / "tools" / "validate_project.py"
PROFILES = json.loads((ROOT / "profiles" / "profiles.json").read_text(encoding="utf-8"))["profiles"]


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="agentic-sdlc-scaffold-") as tmp:
        base = Path(tmp)

        for profile in sorted(PROFILES):
            target = base / profile.lower()
            result = run(
                str(SCAFFOLD),
                "--target",
                str(target),
                "--profile",
                profile,
                "--product-id",
                f"EXAMPLE_{profile}",
                "--objective",
                f"Synthetic objective for {profile}.",
            )
            if result.returncode != 0:
                raise AssertionError(
                    f"scaffold failed for {profile}\n{result.stdout}\n{result.stderr}"
                )

            control = target / ".agentic-sdlc"
            validation = run(str(VALIDATOR), "--root", str(control))
            if validation.returncode != 0:
                raise AssertionError(
                    f"generated scaffold failed validation for {profile}\n"
                    f"{validation.stdout}\n{validation.stderr}"
                )

            product_state = json.loads(
                (control / "state" / "PRODUCT_STATE_CURRENT.json").read_text(encoding="utf-8")
            )
            bootstrap = json.loads(
                (control / "state" / "CURRENT_BOOTSTRAP_STATE.json").read_text(encoding="utf-8")
            )
            if product_state["status"] != "HOLD":
                raise AssertionError(f"{profile}: scaffold must start Product State in HOLD")
            if bootstrap["status"] != "UNTRUSTED_CONTEXT":
                raise AssertionError(f"{profile}: scaffold must start UNTRUSTED_CONTEXT")

            selected = set(
                json.loads((control / "PROFILE.json").read_text(encoding="utf-8"))[
                    "selected_protocols"
                ]
            )
            expected_optional = set(PROFILES[profile]["optional_protocols"])
            if not expected_optional.issubset(selected):
                raise AssertionError(f"{profile}: missing selected optional protocol")

        small = base / "small" / ".agentic-sdlc"
        if (small / "protocols" / "MASTER_OWNER_OS.md").exists():
            raise AssertionError("SMALL profile must not install MASTER_OWNER_OS by default")
        if (small / "state" / "EXECUTION_AUTHORITY_CURRENT.json").exists():
            raise AssertionError("SMALL profile must not create execution authority by default")

        multi = base / "multi_product" / ".agentic-sdlc"
        if not (multi / "protocols" / "MASTER_OWNER_OS.md").exists():
            raise AssertionError("MULTI_PRODUCT profile must include MASTER_OWNER_OS")
        if not (multi / "state" / "EXECUTION_AUTHORITY_CURRENT.json").exists():
            raise AssertionError("MULTI_PRODUCT profile must create fail-closed execution authority")

        high = base / "high_consequence" / ".agentic-sdlc"
        if not (
            high / "protocols" / "SECURITY_PRIVACY_RIGHTS_AND_EXTERNAL_ACTIONS.md"
        ).exists():
            raise AssertionError("HIGH_CONSEQUENCE profile must include security/privacy protocol")

        rerun = run(
            str(SCAFFOLD),
            "--target",
            str(base / "small"),
            "--profile",
            "SMALL",
            "--product-id",
            "EXAMPLE_SMALL",
        )
        if rerun.returncode == 0:
            raise AssertionError("scaffold must refuse overwrite without --force")

    print("SCAFFOLD SELF-TEST PASSED")
    print(f"- generated and validated {len(PROFILES)} profiles")
    print("- SMALL remains minimal")
    print("- MULTI_PRODUCT includes MASTER OWNER + fail-closed authority")
    print("- HIGH_CONSEQUENCE includes security/privacy/rights protocol")
    print("- accidental overwrite is rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
