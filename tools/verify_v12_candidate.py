#!/usr/bin/env python3
"""Assess v1.2 release readiness without converting self-asserted files to proof.

An editable JSON "PHYSICALLY_VERIFIED_EXACT" token does NOT authenticate a
Windows test, provider receipt, independent review, security audit or CLIENT
release authorization. The physical authority boundary must be implemented by
an independently verified host/release process, not fabricated CLI flags.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CRITERIA = ROOT / "state" / "V1_2_ACCEPTANCE_CRITERIA.json"
PHYSICAL_STATUS = "PHYSICALLY_VERIFIED_EXACT"


def assess_criteria(criteria: dict[str, Any], *,
                    synthetic_tests_passed: bool) -> dict[str, Any]:
    if (not isinstance(criteria, dict) or
        criteria.get("schema_version") != "agentic-v12-candidate-criteria-v1" or
        criteria.get("target_release") != "1.2.0" or
        not isinstance(criteria.get("gates"), list) or
        not criteria["gates"]):
        return {
            "status": "INVALID_RELEASE_CRITERIA_HOLD",
            "release_ready": False,
            "candidate_synthetic_tests_passed": synthetic_tests_passed,
            "failure_codes": ["MISSING_OR_MALFORMED_RELEASE_CRITERIA"],
            "physical_gates_not_yet_accepted": [],
            "unverified_physical_claims": [],
        }
    ids: set[str] = set()
    holds: list[str] = []
    claims: list[str] = []
    errors: list[str] = []
    for item in criteria["gates"]:
        if (not isinstance(item, dict) or
            not isinstance(item.get("id"), str) or
            not item["id"] or
            item["id"] in ids or
            type(item.get("required")) is not bool or
            not isinstance(item.get("status"), str)):
            errors.append("INVALID_OR_DUPLICATE_GATE")
            continue
        ident = item["id"]
        ids.add(ident)
        if item["status"] == PHYSICAL_STATUS:
            claims.append(ident)
        if item["required"] and item["status"] != PHYSICAL_STATUS:
            holds.append(ident)
    if not synthetic_tests_passed:
        errors.append("SYNTHETIC_TEST_FAILURE")
    if holds:
        errors.append("PHYSICAL_GATE_HOLDS_REMAIN")
    if claims:
        errors.append("PHYSICAL_CLAIMS_REQUIRE_INDEPENDENT_READBACK")
    # This public helper has NO trusted path to a signed host/test review
    # attestation or an accepted release authorization. A repository editor
    # can forge the data above, so the result ALWAYS remains NOT RELEASE READY.
    errors.append("TRUSTED_RELEASE_AUTHORITY_NOT_CONNECTED")
    return {
        "schema_version": "agentic-v12-release-diagnostic-v2",
        "target_release": criteria["target_release"],
        "baseline_stable_version": criteria.get("baseline_stable_version"),
        "codex_daily_control_reference": criteria.get("codex_daily_control_reference"),
        "candidate_synthetic_tests_passed": synthetic_tests_passed,
        "physical_gates_not_yet_accepted": holds,
        "unverified_physical_claims": claims,
        "independent_release_authority_verified": False,
        "release_ready": False,
        "status": "CANDIDATE_ONLY_NOT_RELEASE_READY",
        "failure_codes": sorted(set(errors)),
        "next_gate": "L3_PHYSICAL_EVIDENCE_THEN_INDEPENDENT_SIGNOFF_AND_RELEASE_PATH",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--require-release-ready", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    try:
        criteria = json.loads(CRITERIA.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        criteria = {}
    test = subprocess.run(
        [sys.executable, "tools/selftest_operational_v12.py"],
        cwd=ROOT, capture_output=True, text=True, check=False
    )
    result = assess_criteria(criteria, synthetic_tests_passed=test.returncode == 0)
    print(json.dumps(result, indent=2) if args.json else
          "V1.2 " + result["status"] + " | hold codes: " +
          ", ".join(result["failure_codes"]))
    if test.returncode:
        print(test.stdout + test.stderr, file=sys.stderr)
        return 1
    if result["status"] == "INVALID_RELEASE_CRITERIA_HOLD":
        return 2
    if args.require_release_ready:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
