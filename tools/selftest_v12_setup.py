#!/usr/bin/env python3
"""Bounded offline proof: combinable modes, no fake authority, theory owners."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from jsonschema import Draft202012Validator

from project_setup import (
    WORK_SCOPE, EXECUTION, COLLABORATION, PROJECT_TYPES,
    defaults, evaluate, recommend, detect_os, SetupError,
)
from theory_guard import check as check_theory


ROOT = Path(__file__).resolve().parents[1]


def expect_error(call, error_type: type) -> None:
    try:
        call()
    except error_type:
        return
    raise AssertionError("EXPECTED_" + error_type.__name__)


def main() -> int:
    schema = json.loads((ROOT / "schemas" / "operating-preferences.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    combinations = 0
    for scope in WORK_SCOPE:
        for execution in EXECUTION:
            for team in COLLABORATION:
                config = defaults(profile_name="STATEFUL", runtime_installed=False, os_name="LINUX")
                config.update(work_scope=scope, execution_mode=execution, collaboration=team)
                Draft202012Validator(schema).validate(config)
                result = evaluate(config)
                assert result["execution_ready"] is False
                if execution != "SYNCHRONOUS" or team == "TEAM":
                    assert result["status"] == "HOLD_UNPROVEN_INTEGRATION"
                else:
                    assert result["status"] == "CONFIGURATION_VALID_NOT_PRODUCT_ACCEPTANCE"
                if team == "TEAM":
                    assert "TEAM_ACTOR_AUTHORITY_NOT_PHYSICALLY_VERIFIED" in result["blockers"]
                if execution != "SYNCHRONOUS":
                    assert "ASYNC_SCHEDULER_NOT_PHYSICALLY_VERIFIED" in result["blockers"]
                combinations += 1
    assert combinations == 18
    expect_error(lambda: evaluate({**defaults(profile_name="SMALL"),"status":"ACCEPTED"}), SetupError)
    expect_error(lambda: evaluate({**defaults(profile_name="SMALL"),"plugins":[
        {"name":"anything","purpose":"change all files","access":"ADMIN"}]}), SetupError)
    assert detect_os("Darwin") == "MACOS"
    assert detect_os("Linux") == "LINUX"
    assert detect_os("Windows") == "WINDOWS"
    assert detect_os("AIX") == "OTHER"
    for kind in PROJECT_TYPES:
        advice = recommend(project_type=kind)
        assert advice["status"] == "NON_AUTHORITATIVE_DISCOVERY_SUGGESTIONS"
        assert "I2_STACK_DECISION" in advice["hard_gates"]
        assert len(advice["options_to_evaluate"]) == 3
    strict = recommend(project_type="CRUD",risk="HIGH",deployment="INTERNET",data_sensitivity="PERSONAL")
    assert "ACCESS_CONTROL" in strict["hard_gates"]
    assert "NETWORK_THREAT_MODEL" in strict["hard_gates"]
    expect_error(lambda: recommend(project_type="MADE_UP"), SetupError)

    with tempfile.TemporaryDirectory(prefix="agentic-v12-operating-") as tmp:
        target = Path(tmp) / "synthetic"
        run = subprocess.run([
            sys.executable, str(ROOT / "tools" / "scaffold_project.py"),
            "--target",str(target),"--profile","SMALL","--product-id","SYNTHETIC",
            "--execution-mode","HYBRID","--collaboration","TEAM",
            "--work-scope","MIXED","--project-type","CRUD","--language","es",
        ],cwd=ROOT,capture_output=True,text=True,check=False)
        if run.returncode:
            raise AssertionError("scaffold failed: "+run.stderr)
        control = target / ".agentic-sdlc"
        prefs = json.loads((control / "configuration" / "OPERATING_PREFERENCES.json").read_text(encoding="utf-8"))
        assert prefs["execution_mode"] == "HYBRID"
        assert prefs["collaboration"] == "TEAM"
        assert prefs["work_scope"] == "MIXED"
        assert prefs["project_type"] == "CRUD"
        assert evaluate(prefs)["status"] == "HOLD_UNPROVEN_INTEGRATION"
        assert (control / "tools" / "project_setup.py").is_file()
        assert (control / "tools" / "theory_guard.py").is_file()
        result = check_theory(control)
        assert result["status"] == "HOLD"
        assert result["may_authorize_campaign"] is False
        assert "CURRENTNESS_OR_BOOTSTRAP_UNTRUSTED" in result["failure_codes"]
        validation = subprocess.run([sys.executable,str(control / "tools" / "validate_project.py"),
                                     "--root",str(control)],cwd=ROOT,capture_output=True,text=True,check=False)
        assert validation.returncode == 0, validation.stderr + validation.stdout
        bad = subprocess.run([sys.executable,str(ROOT / "tools" / "scaffold_project.py"),
                              "--target",str(Path(tmp)/"bad"),"--profile","SMALL",
                              "--product-id","BAD","--execution-mode","INVALID"],
                             cwd=ROOT,capture_output=True,text=True,check=False)
        assert bad.returncode != 0 and not (Path(tmp)/"bad").exists()
    print("V1.2 OPERATING CONFIG SELF-TEST PASSED: 18 combinations, 14 project types, theory HOLD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
