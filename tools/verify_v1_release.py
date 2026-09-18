#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CRITERIA = ROOT / "state" / "V1_RELEASE_CRITERIA.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute the complete Agentic SDLC v1 release evidence suite.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable result.")
    args = parser.parse_args()

    criteria = json.loads(CRITERIA.read_text(encoding="utf-8"))
    results = []

    for gate in criteria["gates"]:
        parts = shlex.split(gate["command"])
        if not parts or parts[0] not in {"python", "python3"}:
            raise SystemExit(f"unsupported release command: {gate['command']}")
        command = [sys.executable, *parts[1:]]
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        results.append(
            {
                "id": gate["id"],
                "purpose": gate["purpose"],
                "command": gate["command"],
                "passed": completed.returncode == 0,
                "returncode": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            }
        )
        if completed.returncode != 0:
            break

    passed = len(results) == len(criteria["gates"]) and all(item["passed"] for item in results)
    report = {
        "schema_version": "v1-release-evidence-0.1",
        "release": criteria["release"],
        "passed": passed,
        "gates_total": len(criteria["gates"]),
        "gates_executed": len(results),
        "results": results,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("V1 RELEASE GATE " + ("PASSED" if passed else "FAILED"))
        for item in results:
            print(f"- {item['id']}: {'PASS' if item['passed'] else 'FAIL'}")
            if not item["passed"]:
                if item["stdout"]:
                    print(item["stdout"])
                if item["stderr"]:
                    print(item["stderr"])
        if passed:
            print(f"- {len(results)}/{len(criteria['gates'])} required gates passed")

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
