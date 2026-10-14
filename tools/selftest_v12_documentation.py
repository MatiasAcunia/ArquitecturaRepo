#!/usr/bin/env python3
"""Keep v1.2 default/report/docs mutually consistent before local L3."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def require(path, phrases):
    f=ROOT/path
    if not f.is_file():
        raise AssertionError("MISSING_DOCUMENT:"+path)
    text=f.read_text(encoding="utf-8")
    for phrase in phrases:
        if phrase not in text:
            raise AssertionError("MISSING_CONTRACT:"+path+":"+phrase)
    return text

def main():
    readme=require("README.md", ["monthly", "no data can reach a maintainer until",
              "docs/27_PROJECT_MODES_AND_STACK_SELECTION.md", "docs/28_LONGITUDINAL_L3_TEST_PROTOCOL.md"])
    if "weekly strict-metadata report" in readme or "external submission is disabled by default" in readme:
        raise AssertionError("STALE_README_TELEMETRY_POLICY")
    require("SECURITY.md", ["opt-out", "NOT bundled"])
    require("docs/22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md", ["no physical route", "opt-out"])
    require("docs/FAQ_ES.md", ["### 19.", "### 20.", "external_submission_enabled=false"])
    config=json.loads((ROOT/"templates/ARCHITECTURE_FEEDBACK_CONFIG.json").read_text(encoding="utf-8"))
    assert config["enabled"] is True and config["cadence"]=="MONTHLY"
    assert config["external_submission_enabled"] is True
    workflow=require("templates/AGENTIC_SDLC_FEEDBACK_WORKFLOW.yml",
        ['cron: "41 4 1 * *"', "vars.AGENTIC_SDLC_FEEDBACK_SUBMIT != 'false'",
         "vars.AGENTIC_SDLC_FEEDBACK_ENDPOINT != ''"])
    assert "23 4 * * 0" not in workflow
    for code in ("en","es","pt","fr","de","it","ja","zh"):
        require("docs/i18n/FAQ_"+code+".md", ["### 13.", "enabled=false"])
    require("prompts/L3_FIRST_LOCAL_PILOT.md",
        ["Longitudinal", "2.0.2", "rollback", "retail inventory"])
    print("V1.2 DOCUMENTATION CONTRACT PASSED")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
