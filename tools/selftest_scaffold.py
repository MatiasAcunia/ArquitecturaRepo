#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from candidate_manifest import verify_installed_tool_parity

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
            parity = verify_installed_tool_parity(ROOT, control / "tools")
            if parity["status"] != "PASS":
                raise AssertionError(
                    f"{profile}: installed/root tool parity failed: {parity['mismatches']}"
                )
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
            skill = control / "skills" / "cleangarbage" / "SKILL.md"
            if not skill.is_file() or "/cleangarbage" not in skill.read_text(encoding="utf-8"):
                raise AssertionError(f"{profile}: L3 cleanup skill missing")
            agents_content = (control / "AGENTS.md").read_text(encoding="utf-8")
            if "/cleangarbage" not in agents_content or "primary owner" not in agents_content:
                raise AssertionError(f"{profile}: L3 cleanup responsibility missing")
            if not (control / "tools" / "validate_project.py").exists():
                raise AssertionError(f"{profile}: copied validator missing")
            if not (control / "requirements-validation.txt").exists():
                raise AssertionError(f"{profile}: validation requirements missing")
            if not (control / "tools" / "migrate_state.py").exists():
                raise AssertionError(f"{profile}: copied migration tool missing")
            if not (control / "tools" / "reconstruct_context.py").exists():
                raise AssertionError(f"{profile}: copied reconstruction tool missing")
            for portable_tool in (
                "state_tx.py",
                "discover_project.py",
                "apply_adoption.py",
                "repo_delta.py",
                "commit_guard.py",
                "workspace_gc.py",
                "artifact_ledger.py",
                "baseline_guard.py",
                "project_status.py",
                "architecture_feedback.py",
            ):
                if not (control / "tools" / portable_tool).exists():
                    raise AssertionError(
                        f"{profile}: copied adoption tool missing: {portable_tool}"
                    )
            for baseline_surface in (
                "state/TECHNICAL_BASELINE_CURRENT.json",
                "state/DELIVERY_PLAN_CURRENT.json",
                "governance/AGENTIC_SDLC_OPERATING_REVIEW_CURRENT.md",
                "feedback/ARCHITECTURE_FEEDBACK_CONFIG.json",
                "runtime/ARTIFACT_LIFECYCLE_CURRENT.json",
            ):
                if not (control / baseline_surface).exists():
                    raise AssertionError(
                        f"{profile}: baseline surface missing: {baseline_surface}"
                    )
            runtime_ignore = control / "runtime" / ".gitignore"
            if not runtime_ignore.is_file() or "ARTIFACT_LIFECYCLE_CURRENT.json" not in runtime_ignore.read_text(encoding="utf-8"):
                raise AssertionError(f"{profile}: local artifact index must be Git-ignored")
            if not (control / "docs" / "34_FILE_ARTIFACT_INVENTORY_AND_GC.md").is_file():
                raise AssertionError(f"{profile}: file GC manual missing from installed scaffold")
            inventory = json.loads(
                (control / "runtime" / "ARTIFACT_LIFECYCLE_CURRENT.json").read_text(encoding="utf-8")
            )
            if inventory["schema_version"] != "artifact-ledger-v1" or inventory["files"] or inventory["roots"]:
                raise AssertionError(f"{profile}: fresh lifecycle inventory must be empty and unowned")
            baseline_guard = run(
                str(control / "tools" / "baseline_guard.py"),
                "--control-root",
                str(control),
                "--json",
            )
            if baseline_guard.returncode == 0:
                raise AssertionError(
                    f"{profile}: fresh scaffold baseline must start blocked"
                )
            if not (control / "templates" / "WORKSPACE_LIFECYCLE.json").exists():
                raise AssertionError(f"{profile}: workspace lifecycle template missing")
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
            if not (
                target / ".github" / "workflows" / "agentic-sdlc-feedback.yml"
            ).exists():
                raise AssertionError(
                    f"{profile}: managed privacy feedback workflow missing by default"
                )
            if (control / "tools" / "campaignctl.py").exists():
                raise AssertionError(f"{profile}: campaign runtime installed without --with-runtime")

        small = base / "small" / ".agentic-sdlc"
        if (small / "protocols" / "MASTER_OWNER_OS.md").exists():
            raise AssertionError("SMALL profile must not install MASTER_OWNER_OS by default")
        if (small / "templates" / "CODEX_DAILY_CONTROL_ADAPTER_CONFIG.json").exists():
            raise AssertionError("SMALL cannot install an unrequested Codex adapter")
        if (small / "tools" / "cognitive_i4.py").exists():
            raise AssertionError("SMALL cannot install cognitive I4 tools")
        if (small / "templates" / "OWNER_FIVE_TASK_PACK.json").exists():
            raise AssertionError("SMALL cannot install OWNER pack")
        if (small / "state" / "EXECUTION_AUTHORITY_CURRENT.json").exists():
            raise AssertionError("SMALL profile must not create execution authority by default")

        multi = base / "multi_product" / ".agentic-sdlc"
        if not (multi / "protocols" / "MASTER_OWNER_OS.md").exists():
            raise AssertionError("MULTI_PRODUCT profile must include MASTER_OWNER_OS")
        pack_path = multi / "templates" / "OWNER_FIVE_TASK_PACK.json"
        if not pack_path.is_file() or json.loads(pack_path.read_text())["enabled"] is not False:
            raise AssertionError("OWNER task pack must be present but disabled until authorized")
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
        parity = verify_installed_tool_parity(ROOT, runtime_control / "tools")
        if parity["status"] != "PASS":
            raise AssertionError(
                f"runtime-enabled installed/root tool parity failed: {parity['mismatches']}"
            )
        runtime_profile = json.loads(
            (runtime_control / "PROFILE.json").read_text(encoding="utf-8")
        )
        if runtime_profile.get("runtime_enabled") is not True:
            raise AssertionError("runtime-enabled scaffold did not record runtime_enabled=true")
        for item in ("goal_guard.py", "goal_plan.py", "cognitive_i4.py",
                     "cognitive_ledger.py", "external_effects.py", "fenced_mutator.py",
                     "evidence_decision.py"):
            if not (runtime_control / "tools" / item).is_file():
                raise AssertionError("v1.2 optional runtime tool missing: " + item)
        for item in ("GOAL_CONTRACT_TEMPLATE.json", "TACTICAL_PLAN_TEMPLATE.json",
                     "CODEX_DAILY_CONTROL_ADAPTER_CONFIG.json"):
            if not (runtime_control / "templates" / item).is_file():
                raise AssertionError("v1.2 opt-in runtime template missing: " + item)
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

        # v1.2 forbids destructive --force even for a pristine scaffold:
        # a still-DRAFT project might contain uncommitted CLIENT theory.
        baseline_dir = base / "small" / ".agentic-sdlc"
        original_requirements = (baseline_dir / "state" / "CLIENT_REQUIREMENTS_CURRENT.md").read_bytes()
        original_profile = (baseline_dir / "PROFILE.json").read_bytes()
        pristine_force = run(str(SCAFFOLD), "--target", str(base / "small"),
                             "--profile", "SMALL", "--product-id", "EXAMPLE_SMALL",
                             "--force")
        if pristine_force.returncode == 0:
            raise AssertionError("v1.2 must refuse destructive --force on every existing layer")
        if ((baseline_dir / "state" / "CLIENT_REQUIREMENTS_CURRENT.md").read_bytes()
                != original_requirements or (baseline_dir / "PROFILE.json").read_bytes()
                != original_profile):
            raise AssertionError("refused --force modified uncommitted CLIENT theory")
        # A malicious existing marker is not permission to delete any project.
        saved = original_requirements
        edited = saved + b"\nUnsaved private CLIENT decision, must survive rejected force.\n"
        (baseline_dir / "state" / "CLIENT_REQUIREMENTS_CURRENT.md").write_bytes(edited)
        modified_force = run(str(SCAFFOLD), "--target", str(base / "small"),
                             "--profile", "SMALL", "--product-id", "EXAMPLE_SMALL",
                             "--force")
        if modified_force.returncode == 0 or (
            baseline_dir / "state" / "CLIENT_REQUIREMENTS_CURRENT.md"
        ).read_bytes() != edited:
            raise AssertionError("force destroyed an unconfirmed CLIENT requirement")
        (baseline_dir / "state" / "CLIENT_REQUIREMENTS_CURRENT.md").write_bytes(saved)

        # No output folder may be created if --force fails before install.
        never_created = base / "force-must-not-create"
        invalid_force = run(str(SCAFFOLD), "--target", str(never_created),
                            "--profile", "SMALL", "--product-id", "TEST", "--force")
        if invalid_force.returncode == 0 or never_created.exists():
            raise AssertionError("failed --force created a partial project")
        # Reject Windows device names and Git metadata on Linux CI too.
        for forbidden in (".git", ".github", ".svn", ".vscode",
                          "CON", "AUX", "NUL", "COM1", "LPT9", "controls."):
            forbidden_root = base / ("reserved-" + forbidden.replace(".", "x"))
            rejected = run(str(SCAFFOLD), "--target", str(forbidden_root),
                           "--profile", "SMALL", "--product-id", "TEST",
                           "--control-dir", forbidden)
            if rejected.returncode == 0 or forbidden_root.exists():
                raise AssertionError("reserved control directory was accepted: " + forbidden)

        # Adversarial installation path and overwrite tests.
        victim = base / "victim"
        victim.mkdir()
        sentinel = victim / "DO_NOT_DELETE"
        sentinel.write_text("protected", encoding="utf-8")
        for malicious in ("../victim", "..", ".", "/tmp/somewhere", "C:\\other", "nested/subtree"):
            unsafe = run(str(SCAFFOLD), "--target", str(base / "sandbox"),
                         "--control-dir", malicious, "--profile", "SMALL",
                         "--product-id", "TEST")
            if unsafe.returncode == 0:
                raise AssertionError("unsafe --control-dir accepted: " + malicious)
            if sentinel.read_text(encoding="utf-8") != "protected":
                raise AssertionError("unsafe install modified an unrelated directory")

        rogue_project = base / "rogue"
        rogue_control = rogue_project / ".agentic-sdlc"
        rogue_control.mkdir(parents=True)
        rogue_marker = rogue_control / "PERSONAL_NOT_STARTER"
        rogue_marker.write_text("keep", encoding="utf-8")
        illegal_force = run(str(SCAFFOLD), "--target", str(rogue_project),
                            "--profile", "SMALL", "--product-id", "TEST", "--force")
        if illegal_force.returncode == 0 or rogue_marker.read_text(encoding="utf-8") != "keep":
            raise AssertionError("--force must not delete unrecognized control directories")

        symlink_project = base / "linked-project"
        try:
            symlink_project.symlink_to(victim, target_is_directory=True)
        except (OSError, NotImplementedError):
            pass
        else:
            linked = run(str(SCAFFOLD), "--target", str(symlink_project),
                         "--profile", "SMALL", "--product-id", "TEST", "--force")
            if linked.returncode == 0:
                raise AssertionError("scaffold must refuse symlinked project roots")

        live_project = base / "small"
        live_control = live_project / ".agentic-sdlc"
        current_product = live_control / "state" / "PRODUCT_STATE_CURRENT.json"
        original = current_product.read_text(encoding="utf-8")
        modified_product = json.loads(original)
        modified_product["status"] = "ACTIVE"
        current_product.write_text(json.dumps(modified_product), encoding="utf-8")
        unsafe_live = run(str(SCAFFOLD), "--target", str(live_project),
                          "--profile", "SMALL", "--product-id", "TEST", "--force")
        if unsafe_live.returncode == 0:
            raise AssertionError("--force removed live Product State")
        if json.loads(current_product.read_text(encoding="utf-8"))["status"] != "ACTIVE":
            raise AssertionError("blocked --force nevertheless mutated the Product State")
        current_product.write_text(original, encoding="utf-8")

        linked_control_project = base / "linked-control"
        linked_control_project.mkdir()
        (linked_control_project / ".agentic-sdlc").symlink_to(
            victim, target_is_directory=True)
        linked_force = run(str(SCAFFOLD), "--target", str(linked_control_project),
                           "--profile", "SMALL", "--product-id", "TEST", "--force")
        if linked_force.returncode == 0 or sentinel.read_text(encoding="utf-8") != "protected":
            raise AssertionError("scaffold followed symlinked --force target")
        

    print("SCAFFOLD SELF-TEST PASSED")
    print(f"- generated and validated {len(PROFILES)} profiles")
    print("- SMALL remains minimal")
    print("- MULTI_PRODUCT includes MASTER OWNER + fail-closed authority")
    print("- HIGH_CONSEQUENCE includes security/privacy/rights protocol")
    print("- copied validator is self-contained")
    print("- generated bootstrap uses latest v0.2 contract")
    print("- installed/root tool byte parity verified for six profiles and runtime")
    print("- copied migration registry/tool are self-contained")
    print("- copied reconstruction tool is self-contained")
    print("- discovery/adoption/recovery tools are self-contained")
    print("- delta-sync/commit-boundary/local-GC tools are self-contained")
    print("- product-baseline/status tools are self-contained and fresh baseline starts blocked")
    print("- privacy-preserving architecture feedback exporter/workflow are installed by default")
    print("- campaign runtime remains opt-in and portable")
    print("- accidental overwrite is rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
