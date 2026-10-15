#!/usr/bin/env python3
"""Validate public v1.2 documentation policy and navigation without leaking maintainer plans."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(path, phrases):
    target = ROOT / path
    if not target.is_file():
        raise AssertionError("MISSING_DOCUMENT:" + path)
    body = target.read_text(encoding="utf-8")
    for phrase in phrases:
        if phrase not in body:
            raise AssertionError("MISSING_CONTRACT:" + path + ":" + phrase)
    return body


def main():
    readme = require("README.md", [
        "monthly",
        "no data can reach a maintainer until",
        "docs/27_PROJECT_MODES_AND_STACK_SELECTION.md",
        "docs/README.md",
        "v1.2.0",
    ])
    # Maintainer-only pilot references belong in the documentation index, not the
    # adopter's quick-start journey. Preserve discoverability for contributors.
    require("docs/README.md", [
        "ordinary adopter",
        "28_LONGITUDINAL_L3_TEST_PROTOCOL.md",
        "41_V1_3_EXECUTION_ROUTE_ACCEPTANCE_AND_MILESTONES.md",
    ])
    require("docs/28_LONGITUDINAL_L3_TEST_PROTOCOL.md", [
        "Longitudinal",
    ])
    if ("weekly strict-metadata report" in readme
            or "external submission is disabled by default" in readme):
        raise AssertionError("STALE_README_TELEMETRY_POLICY")
    require("SECURITY.md", ["opt-out", "NOT bundled"])
    require("docs/22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md",
            ["no physical route", "opt-out"])
    require("docs/FAQ_ES.md", ["### 19.", "### 20.", "external_submission_enabled=false"])
    require("docs/24_OPERATIONAL_AGENTIC_SDLC_V1_2_ES.md", ["v1.2.0", "Proveedores y agentes"])

    config = json.loads((ROOT / "templates/ARCHITECTURE_FEEDBACK_CONFIG.json").read_text(encoding="utf-8"))
    assert config["enabled"] is True and config["cadence"] == "MONTHLY"
    assert config["external_submission_enabled"] is True
    workflow = require("templates/AGENTIC_SDLC_FEEDBACK_WORKFLOW.yml", [
        'cron: "41 4 1 * *"',
        "vars.AGENTIC_SDLC_FEEDBACK_SUBMIT != 'false'",
        "vars.AGENTIC_SDLC_FEEDBACK_ENDPOINT != ''",
    ])
    assert "23 4 * * 0" not in workflow
    for code in ("en", "es", "pt", "fr", "de", "it", "ja", "zh"):
        require("docs/i18n/FAQ_" + code + ".md", ["### 13.", "enabled=false"])
    require("prompts/L3_FIRST_LOCAL_PILOT.md", [
        "Longitudinal", "2.0.2", "rollback", "retail inventory",
    ])
    print("V1.2 PUBLIC DOCUMENTATION CONTRACT PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
