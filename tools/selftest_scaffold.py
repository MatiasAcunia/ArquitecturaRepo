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
            if bootstrap["schema_version"] != "starter-bootstrap-0.2":
                raise AssertionError(f"{profile}: scaffold must emit bootstrap v0.2")
            if bootstrap["currentness"]["verified"] is not False:
                raise AssertionError(f"{profile}: fresh scaffold must not claim verified currentness")
            if not bootstrap["currentness"]["unresolved"]:
                raise AssertionError(f"{profile}: fresh scaffold must retain unresolved currentness")

            profile_state = json.loads(
                (control / "PROFILE.json").read_text(encoding="utf-8")
            )
            selected = set(profile_state["selected_protocols"])
            expected_optional = set(PROFILES[profile]["optional_protocols"])
            if not expected_optional.issubset(selected):
                raise AssertionError(f"{profile}: missing selected optional protocol")
            if profile_state.get("runtime_enabled") is not False:
                raise AssertionError(f"{profile}: runtime must remain opt-in")
            if not (control / "tools" / "validate_project.py").exists():
                raise AssertionError(f"{profile}: copied validator missing")
            if not (control / "requirements-validation.txt").exists():
                raise AssertionError(f"{profile}: validation requirements missing")
            if not (control / "tools" / "migrate_state.py").exists():
                raise AssertionError(f"{profile}: copied migration tool missing")
            if not (control / "tools" / "reconstruct_context.py").exists():
                raise AssertionError(f"{profile}: copied reconstruction tool missing")
            if not (control / "migrations" / "registry.json").exists():
                raise AssertionError(f"{profile}: migration registry missing")
            migration_plan = run(
                str(control / "tools" / "migrate_state.py"),
                "--control-root",
                str(control),
                "plan",
                "--file",
                "state/CURRENT_BOOTSTRAP_STATE.json",
            )
            if migration_plan.returncode != 0:
                raise AssertionError(
                    f"{profile}: copied migration tool cannot plan current bootstrap\n"
                    f"{migration_plan.stdout}\n{migration_plan.stderr}"
                )
            if json.loads(migration_plan.stdout)["steps"] != []:
                raise AssertionError(f"{profile}: fresh bootstrap should already be latest")
            reconstruction = run(
                str(control / "tools" / "reconstruct_context.py"),
                "--root",
                str(control),
            )
            if reconstruction.returncode != 0:
                raise AssertionError(
                    f"{profile}: copied reconstruction tool failed\n"
                    f"{reconstruction.stdout}\n{reconstruction.stderr}"
                )
            if json.loads(reconstruction.stdout)["posture"] != "UNTRUSTED_CONTEXT":
                raise AssertionError(f"{profile}: fresh reconstruction posture is not UNTRUSTED_CONTEXT")
            if (control / "tools" / "campaignctl.py").exists():
                raise AssertionError(f"{profile}: campaign runtime installed without --with-runtime")

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

        runtime_target = base / "runtime_enabled"
        runtime_result = run(
            str(SCAFFOLD),
            "--target",
            str(runtime_target),
            "--profile",
            "STATEFUL",
            "--product-id",
            "EXAMPLE_RUNTIME",
            "--objective",
            "Synthetic runtime-enabled product.",
            "--with-runtime",
        )
        if runtime_result.returncode != 0:
            raise AssertionError(
                "runtime-enabled scaffold failed\n"
                + runtime_result.stdout
                + "\n"
                + runtime_result.stderr
            )
        runtime_control = runtime_target / ".agentic-sdlc"
        runtime_profile = json.loads(
            (runtime_control / "PROFILE.json").read_text(encoding="utf-8")
        )
        if runtime_profile.get("runtime_enabled") is not True:
            raise AssertionError("runtime-enabled scaffold did not record runtime_enabled=true")
        if not (runtime_control / "tools" / "campaignctl.py").exists():
            raise AssertionError("runtime-enabled scaffold missing campaignctl.py")
        copied_validation = run(
            str(runtime_control / "tools" / "validate_project.py"),
            "--root",
            ".",
        )
        if copied_validation.returncode != 0:
            raise AssertionError(
                "copied validator failed inside runtime-enabled scaffold\n"
                + copied_validation.stdout
                + "\n"
                + copied_validation.stderr
            )

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
    print("- copied validator is self-contained")
    print("- generated bootstrap uses latest v0.2 contract")
    print("- copied migration registry/tool are self-contained")
    print("- copied reconstruction tool is self-contained")
    print("- campaign runtime remains opt-in and portable")
    print("- accidental overwrite is rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
