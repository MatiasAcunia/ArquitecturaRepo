#!/usr/bin/env python3
"""Install staging fault injection. No prior adopter state may be removed."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import scaffold_project as scaffolder


def install(target: Path, *, feedback: bool = True) -> Path:
    return scaffolder.create_scaffold(
        target=target, control_dir_name=".agentic-sdlc", profile_name="SMALL",
        product_id="SYNTHETIC", objective="Synthetic test only", force=False,
        with_runtime=False, install_feedback_workflow=feedback,
    )


def main() -> int:
    original_copy = scaffolder.copy_file
    with tempfile.TemporaryDirectory(prefix="v12-install-atomic-") as tmp:
        root = Path(tmp)
        existing = root / "existing-project"
        existing.mkdir()
        sentinel = existing / "CLIENT_PRIVATE_EXISTING_SOURCE"
        sentinel.write_bytes(b"DO_NOT_TOUCH")
        calls = 0

        def fault(source: Path, destination: Path) -> None:
            nonlocal calls
            calls += 1
            if calls == 11:
                raise OSError("INJECTED_MID_INSTALL_DISK_FAILURE")
            original_copy(source, destination)

        scaffolder.copy_file = fault
        try:
            try:
                install(existing)
            except OSError as exc:
                assert "INJECTED_MID_INSTALL" in str(exc)
            else:
                raise AssertionError("FAULT_INJECTION_WAS_IGNORED")
        finally:
            scaffolder.copy_file = original_copy
        assert sentinel.read_bytes() == b"DO_NOT_TOUCH"
        assert not (existing / ".agentic-sdlc").exists()
        assert not (existing / ".github").exists()
        assert not list(existing.glob(".agentic-sdlc-stage-*"))

        new_project = root / "new-project"
        calls = 0
        scaffolder.copy_file = fault
        try:
            try:
                install(new_project)
            except OSError:
                pass
            else:
                raise AssertionError("NEW_TARGET_FAULT_IGNORED")
        finally:
            scaffolder.copy_file = original_copy
        assert not new_project.exists(), "partial new root should be removed"

        # Installed files and workflow are published only after population.
        installed = install(existing)
        assert installed.is_dir()
        assert (existing / ".github" / "workflows" /
                "agentic-sdlc-feedback.yml").is_file()
        assert sentinel.read_bytes() == b"DO_NOT_TOUCH"
        assert not list(existing.glob(".agentic-sdlc-stage-*"))
        assert "COLLECTOR_NOT_CONFIGURED" in (
            installed / "INSTALLATION_REPORT.md").read_text(encoding="utf-8")
        try:
            install(existing)
        except FileExistsError:
            pass
        else:
            raise AssertionError("existing control unexpectedly overwritten")

        # Existing repo workflows are NEVER overwritten, including those
        # previously managed but potentially modified by the adopter.
        colliding = root / "existing-workflow-project"
        wf = colliding / ".github" / "workflows" / "agentic-sdlc-feedback.yml"
        wf.parent.mkdir(parents=True)
        wf.write_bytes(b"# USER_CUSTOM_WORKFLOW_MUST_SURVIVE\n")
        keep = wf.read_bytes()
        control = install(colliding)
        assert wf.read_bytes() == keep
        for name in ("INSTALLATION_REPORT.md", "README.md"):
            assert "PRESERVED_EXISTING_WORKFLOW" in (
                control / name).read_text(encoding="utf-8")
        assert not list(colliding.glob(".agentic-sdlc-stage-*"))

    print("INSTALL STAGING SELF-TEST PASSED: interrupted install, fresh success and preexisting workflow preservation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
