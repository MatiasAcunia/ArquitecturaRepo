#!/usr/bin/env python3
"""A first-time user's real CLI path, including ungoverned and governed repos."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD = ROOT / "tools" / "scaffold_project.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def require_success(result: subprocess.CompletedProcess[str], label: str) -> None:
    if result.returncode:
        raise AssertionError(f"{label} failed:\n{result.stdout}\n{result.stderr}")


def fingerprint(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def install(project: Path, *, product: str) -> subprocess.CompletedProcess[str]:
    return run(
        str(SCAFFOLD),
        "--target", str(project),
        "--profile", "SMALL",
        "--product-id", product,
        "--objective", "A tiny synthetic app with a documented source owner.",
        "--language", "en",
        "--no-feedback-workflow",
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ar-v14-adopter-") as temp:
        root = Path(temp)
        project = root / "existing_ungoverned"
        source = project / "src" / "main.py"
        source.parent.mkdir(parents=True)
        source.write_text("def greet():\n    return 'hello'\n", encoding="utf-8")
        workflow = project / ".github" / "workflows" / "agentic-sdlc-feedback.yml"
        workflow.parent.mkdir(parents=True)
        workflow.write_text("# User-owned workflow. Never replace.\n", encoding="utf-8")
        before_source, before_workflow = fingerprint(source), fingerprint(workflow)

        outside = root / "outside_private.txt"
        outside.write_text("private-source-must-not-be-inventoried", encoding="utf-8")
        symlink_supported = True
        try:
            os.symlink(outside, project / "src" / "outside.txt")
        except (NotImplementedError, OSError):
            symlink_supported = False

        scaffold = install(project, product="ONBOARDING_EXAMPLE")
        require_success(scaffold, "existing ungoverned installation")
        control = project / ".agentic-sdlc"
        if not all(
            marker in scaffold.stdout
            for marker in (
                "STATUS: HOLD / UNTRUSTED_CONTEXT",
                "NEXT (read-only",
                "project_status.py",
                "discover_project.py",
                "reconstruct_context.py",
                "collector_endpoint=NOT_CONFIGURED_BY_STARTER",
            )
        ):
            raise AssertionError("installed scaffold did not give clear next read-only commands and privacy posture")
        if not (control / "tools" / "git_currentness.py").is_file():
            raise AssertionError("portable E2 source probe was not installed")
        readme = (control / "README.md").read_text(encoding="utf-8")
        for expected in (
            '".agentic-sdlc/requirements-validation.txt"',
            '".agentic-sdlc/tools/validate_project.py" --root "."',
            '".agentic-sdlc/tools/project_status.py" --control-root ".agentic-sdlc"',
            '".agentic-sdlc/tools/discover_project.py" --project-root "."',
            '".agentic-sdlc/tools/reconstruct_context.py" --root ".agentic-sdlc"',
            '".agentic-sdlc/tools/artifact_ledger.py" --project "."',
            "read-only existing-governance attachment",
        ):
            if expected not in readme:
                raise AssertionError(f"generated readme has missing or invalid first-step guidance: {expected}")
        if '".agentic-sdlc/tools/validate_project.py" --root ".agentic-sdlc"' in readme:
            raise AssertionError("generated readme doubles the validator's installed root")
        if (control / "tools" / "campaignctl.py").exists():
            raise AssertionError("optional runtime installed in no-runtime SMALL")
        if fingerprint(source) != before_source or fingerprint(workflow) != before_workflow:
            raise AssertionError("installer modified existing application or user-owned workflow")

        status = run(
            str(control / "tools" / "project_status.py"),
            "--control-root", str(control),
        )
        require_success(status, "first project status")
        if "PROJECT: ONBOARDING_EXAMPLE" not in status.stdout or "BASELINE READY: False" not in status.stdout:
            raise AssertionError("new installation incorrectly reported ready state")

        validation = run(str(control / "tools" / "validate_project.py"), "--root", ".")
        if validation.returncode:
            if "No module named 'jsonschema'" not in validation.stderr:
                raise AssertionError(f"documented installed-control validation failed: {validation.stderr}")
        elif "PROJECT VALIDATION PASSED" not in validation.stdout:
            raise AssertionError("installed-control validator returned success without validating")

        discovery = run(
            str(control / "tools" / "discover_project.py"),
            "--project-root", str(project),
        )
        require_success(discovery, "read-only discovery")
        inventory = json.loads(discovery.stdout)
        names = {item["path"] for item in inventory["files"]}
        if "src/main.py" not in names or any(name.startswith(".agentic-sdlc/") for name in names):
            raise AssertionError("discovery did not isolate application from installed control state")
        if symlink_supported and "src/outside.txt" in names:
            raise AssertionError("discovery followed a symlink to an external private file")
        if symlink_supported:
            directory_outside = root / "private_folder"
            directory_outside.mkdir()
            (directory_outside / "secret.txt").write_text("not-public", encoding="utf-8")
            try:
                os.symlink(directory_outside, project / "src" / "linked_folder", target_is_directory=True)
            except (NotImplementedError, OSError):
                pass  # Windows link privileges may differ for files and directories.
            else:
                dir_check = run(
                    str(control / "tools" / "discover_project.py"),
                    "--project-root", str(project),
                )
                require_success(dir_check, "symlinked directory inventory")
                dir_names = {item["path"] for item in json.loads(dir_check.stdout)["files"]}
                if "src/linked_folder/secret.txt" in dir_names:
                    raise AssertionError("discovery followed a symlinked directory outside project")
        if symlink_supported:
            link = control / "discovery" / "inventory-link.json"
            link.parent.mkdir(parents=True, exist_ok=True)
            os.symlink(outside, link)
            blocked_output = run(
                str(control / "tools" / "discover_project.py"),
                "--project-root", str(project),
                "--output", str(link),
            )
            if blocked_output.returncode == 0 or "symlinked output path refused" not in blocked_output.stderr:
                raise AssertionError("discovery overwrote an external target through symlinked output")
            if outside.read_text(encoding="utf-8") != "private-source-must-not-be-inventoried":
                raise AssertionError("discovery changed an external file")

        reconstructed = run(
            str(control / "tools" / "reconstruct_context.py"),
            "--root", str(control),
        )
        if reconstructed.returncode:
            if "validation dependency 'jsonschema' is missing" not in reconstructed.stderr:
                raise AssertionError(f"unhelpful fresh-context failure: {reconstructed.stderr}")
        else:
            projection = json.loads(reconstructed.stdout)
            if projection["posture"] != "UNTRUSTED_CONTEXT":
                raise AssertionError("scaffold incorrectly claimed reconstructed authority")
            if projection["git_currentness"]["code_ref_relation"] != "NO_GIT_REPOSITORY":
                raise AssertionError("scaffold invented a local Git HEAD")

        canonical_file = control / "state" / "PRODUCT_STATE_CURRENT.json"
        before_state = fingerprint(canonical_file)
        duplicate = install(project, product="ONBOARDING_EXAMPLE")
        if duplicate.returncode == 0 or "EXISTING_CONTROL_PRESERVED" not in duplicate.stderr:
            raise AssertionError("reinstall did not refuse overwriting an existing control layer")
        if fingerprint(canonical_file) != before_state:
            raise AssertionError("failed reinstall mutated canonical Product State")

        governed = root / "existing_governed"
        canonical = governed / "legacy" / "state" / "PRODUCT_STATE_CURRENT.json"
        canonical.parent.mkdir(parents=True)
        canonical.write_text('{"schema_version":"product-state-0.1"}\n', encoding="utf-8")
        before_governed = fingerprint(canonical)
        refused = install(governed, product="SHOULD_NOT_INSTALL")
        if refused.returncode == 0 or "EXISTING_CANONICAL_PRODUCT_STATE_HOLD" not in refused.stderr:
            raise AssertionError("generic scaffold created a shadow authority in governed repo")
        if (governed / ".agentic-sdlc").exists() or fingerprint(canonical) != before_governed:
            raise AssertionError("existing governed repository was mutated")

        empty = root / "brand_new_project"
        created = install(empty, product="EMPTY_EXAMPLE")
        require_success(created, "brand-new empty project installation")
        if not (empty / ".agentic-sdlc" / "state" / "PRODUCT_STATE_CURRENT.json").is_file():
            raise AssertionError("brand-new project has no canonical starter state")
        if (empty / ".github" / "workflows" / "agentic-sdlc-feedback.yml").exists():
            raise AssertionError("opted-out new project received a scheduler")

    print("E4 ADOPTER FIRST-STEPS SELF-TEST PASSED")
    print("- empty and existing ungoverned install, actionable status/discovery/reconstruction")
    print("- existing code/workflow preserved and duplicate/shadow governance refused")
    print("- no-runtime profile, explicit feedback-scheduler opt-out and untrusted posture")
    print("- symlink inventory/output guards:", "PASS" if symlink_supported else "SKIPPED (host permissions)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
