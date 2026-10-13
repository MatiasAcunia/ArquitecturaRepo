#!/usr/bin/env python3
"""Candidate verifier. A passing local suite is never a v1.2 release certificate."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CRITERIA = ROOT / "state" / "V1_2_ACCEPTANCE_CRITERIA.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-release-ready", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    criteria = json.loads(CRITERIA.read_text(encoding="utf-8"))
    test = subprocess.run([sys.executable, "tools/selftest_operational_v12.py"],
                          cwd=ROOT, capture_output=True, text=True, check=False)
    holds = [row["id"] for row in criteria["gates"] if row["status"] != "PHYSICALLY_VERIFIED_EXACT"]
    output = {
        "schema_version": "agentic-v12-candidate-verification-v1",
        "candidate_synthetic_tests_passed": test.returncode == 0,
        "release_ready": test.returncode == 0 and not holds,
        "physical_gates_not_yet_accepted": holds,
        "baseline_stable_version": criteria["baseline_stable_version"],
        "codex_daily_control_reference": criteria["codex_daily_control_reference"],
        "status": "RELEASE_READY" if test.returncode == 0 and not holds else
                  ("CODE_TEST_FAILURE" if test.returncode else "CANDIDATE_ONLY_NOT_RELEASE_READY"),
    }
    print(json.dumps(output, indent=2) if args.json else
          "V1.2 " + output["status"] + " | outstanding physical gates: " + ", ".join(holds))
    if test.returncode:
        print(test.stdout + test.stderr, file=sys.stderr)
        return 1
    if args.require_release_ready and holds:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
