#!/usr/bin/env python3
"""Adversarial gate review: editable PASS tokens cannot release v1.2."""
from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

from verify_v12_candidate import assess_criteria

ROOT=Path(__file__).resolve().parents[1]


def main() -> int:
    criteria=json.loads((ROOT/"state"/"V1_2_ACCEPTANCE_CRITERIA.json").read_text(encoding="utf-8"))
    sample=assess_criteria(criteria,synthetic_tests_passed=True)
    assert sample["release_ready"] is False
    assert "TRUSTED_RELEASE_AUTHORITY_NOT_CONNECTED" in sample["failure_codes"]
    forged=deepcopy(criteria)
    for row in forged["gates"]:
        row["status"]="PHYSICALLY_VERIFIED_EXACT"
    report=assess_criteria(forged,synthetic_tests_passed=True)
    assert report["physical_gates_not_yet_accepted"] == []
    assert report["unverified_physical_claims"]
    assert report["independent_release_authority_verified"] is False
    assert report["release_ready"] is False
    assert "PHYSICAL_CLAIMS_REQUIRE_INDEPENDENT_READBACK" in report["failure_codes"]
    assert not assess_criteria(forged,synthetic_tests_passed=False)["release_ready"]
    duplicate=deepcopy(criteria)
    duplicate["gates"].append(dict(duplicate["gates"][0]))
    assert "INVALID_OR_DUPLICATE_GATE" in assess_criteria(
        duplicate,synthetic_tests_passed=True)["failure_codes"]
    malformed=assess_criteria({"gates":[]},synthetic_tests_passed=True)
    assert malformed["status"]=="INVALID_RELEASE_CRITERIA_HOLD"
    cmd=subprocess.run(
        [sys.executable,str(ROOT/"tools"/"verify_v12_candidate.py"),
         "--require-release-ready","--json"],
        cwd=ROOT,capture_output=True,text=True,check=False
    )
    assert cmd.returncode==2, cmd.stderr+cmd.stdout
    actual=json.loads(cmd.stdout)
    assert actual["release_ready"] is False
    assert actual["independent_release_authority_verified"] is False
    print("RELEASE FALSIFIERS PASSED: no editable JSON PASS can authorize release")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
