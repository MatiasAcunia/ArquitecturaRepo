#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD = ROOT / "tools" / "scaffold_project.py"
REPORT_SCHEMA = ROOT / "schemas" / "architecture-feedback-report.schema.json"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    synthetic_email = "owner" + "@" + "example.invalid"
    synthetic_hex40 = ("0123456789abcdef" * 2) + "01234567"
    sensitive_fragments = [
        "PRIVATE_PRODUCT_X",
        synthetic_email,
        "C:/secret/project/path",
        "TOP_SECRET_REQUIREMENT",
        synthetic_hex40,
    ]

    with tempfile.TemporaryDirectory(prefix="agentic-feedback-") as tmp:
        project = Path(tmp) / "project"
        result = run(
            str(SCAFFOLD),
            "--target", str(project),
            "--profile", "STATEFUL",
            "--product-id", sensitive_fragments[0],
            "--objective", (
                "TOP_SECRET_REQUIREMENT "
                + synthetic_email
                + " C:/secret/project/path "
                + synthetic_hex40
            ),
            "--with-runtime",
        )
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)

        control = project / ".agentic-sdlc"
        workflow = project / ".github" / "workflows" / "agentic-sdlc-feedback.yml"
        if not workflow.exists():
            raise AssertionError("default scaffold did not install managed feedback workflow")

        config_path = control / "feedback" / "ARCHITECTURE_FEEDBACK_CONFIG.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if config.get("enabled") is not True:
            raise AssertionError("feedback must default enabled")
        if config.get("external_submission_enabled") is not False:
            raise AssertionError("external submission must default disabled")
        if config.get("privacy_mode") != "STRICT_METADATA_ONLY":
            raise AssertionError("feedback privacy mode is not strict metadata only")

        report_path = Path(tmp) / "report.json"
        generated = run(
            str(control / "tools" / "architecture_feedback.py"),
            "--control-root", str(control),
            "--trigger", "MANUAL",
            "--output", str(report_path),
        )
        if generated.returncode != 0:
            raise AssertionError(generated.stdout + generated.stderr)
        if not report_path.exists():
            raise AssertionError("manual feedback report was not generated")

        report_text = report_path.read_text(encoding="utf-8")
        for fragment in sensitive_fragments:
            if fragment in report_text:
                raise AssertionError(f"sensitive fragment leaked into report: {fragment}")

        report = json.loads(report_text)
        schema = json.loads(REPORT_SCHEMA.read_text(encoding="utf-8"))
        problems = list(
            Draft202012Validator(
                schema,
                format_checker=FormatChecker(),
            ).iter_errors(report)
        )
        if problems:
            raise AssertionError("feedback report schema validation failed: " + problems[0].message)

        if report["privacy"] != {
            "mode": "STRICT_METADATA_ONLY",
            "free_text_included": False,
            "project_identifiers_included": False,
            "code_or_paths_included": False,
            "requirements_content_included": False,
            "credentials_included": False,
        }:
            raise AssertionError("privacy declaration changed unexpectedly")

        config["cadence"] = "MONTHLY"
        config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        cadence_path = Path(tmp) / "cadence.json"
        cadence = run(
            str(control / "tools" / "architecture_feedback.py"),
            "--control-root", str(control),
            "--trigger", "WEEKLY",
            "--output", str(cadence_path),
        )
        if cadence.returncode != 0 or cadence_path.exists():
            raise AssertionError("cadence mismatch should skip emission without failure")

        config["enabled"] = False
        config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        disabled_path = Path(tmp) / "disabled.json"
        disabled = run(
            str(control / "tools" / "architecture_feedback.py"),
            "--control-root", str(control),
            "--trigger", "MANUAL",
            "--output", str(disabled_path),
        )
        if disabled.returncode != 0 or disabled_path.exists():
            raise AssertionError("disabled feedback should emit nothing")

        no_feedback_project = Path(tmp) / "no-feedback"
        no_feedback = run(
            str(SCAFFOLD),
            "--target", str(no_feedback_project),
            "--profile", "SMALL",
            "--product-id", "NO_FEEDBACK_TEST",
            "--no-feedback-workflow",
        )
        if no_feedback.returncode != 0:
            raise AssertionError(no_feedback.stdout + no_feedback.stderr)
        if (
            no_feedback_project
            / ".github"
            / "workflows"
            / "agentic-sdlc-feedback.yml"
        ).exists():
            raise AssertionError("--no-feedback-workflow still installed scheduled workflow")

    print("ARCHITECTURE FEEDBACK PRIVACY SELF-TEST PASSED")
    print("- scheduled feedback is installed by default")
    print("- local report generation defaults enabled")
    print("- external submission defaults disabled")
    print("- strict allowlisted metadata report validates")
    print("- product identifiers, requirements, paths, emails and SHA-like values do not leak")
    print("- cadence mismatch skips emission")
    print("- enabled=false disables emission")
    print("- --no-feedback-workflow prevents schedule installation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
