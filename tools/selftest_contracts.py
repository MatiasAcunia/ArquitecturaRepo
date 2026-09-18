#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_project.py"
ROOTS = [
    "state",
    "profiles",
    "migrations",
    "examples/minimal",
    "examples/active_campaign",
    "examples/terminal_candidate",
    "examples/stateful_backend/control",
]


def main() -> int:
    for relative in ROOTS:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "--root", relative],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            print(f"CONTRACT INSTANCE SELF-TEST FAILED: {relative}")
            print(result.stdout)
            print(result.stderr)
            return 1

    print("CONTRACT INSTANCE SELF-TEST PASSED")
    for relative in ROOTS:
        print(f"- {relative}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
