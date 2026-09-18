#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_project.py"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def run_validator(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--root", str(root)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def expect_failure(
    source: Path,
    mutate,
    expected_fragment: str,
    label: str,
) -> None:
    with tempfile.TemporaryDirectory(prefix="agentic-sdlc-selftest-") as tmp:
        target = Path(tmp) / "fixture"
        shutil.copytree(source, target)
        mutate(target)
        result = run_validator(target)
        combined = result.stdout + "\n" + result.stderr
        if result.returncode == 0:
            raise AssertionError(f"{label}: validator unexpectedly passed")
        if expected_fragment not in combined:
            raise AssertionError(
                f"{label}: expected {expected_fragment!r} in validator output\n{combined}"
            )


def break_checkpoint_ref(target: Path) -> None:
    path = target / "PRODUCT_STATE_CURRENT.json"
    data = load(path)
    data["current_code_ref"] = "candidate/ref-does-not-match-checkpoint"
    save(path, data)


def break_authority_run(target: Path) -> None:
    path = target / "EXECUTION_AUTHORITY_CURRENT.json"
    data = load(path)
    data["current_run_id"] = "RUN_WRONG"
    save(path, data)


def break_terminal_evidence(target: Path) -> None:
    path = target / "TERMINAL_LABEL_001.json"
    data = load(path)
    data["evidence"]["runtime_physical"] = []
    save(path, data)


def break_currentness_ref(target: Path) -> None:
    path = target / "PRODUCT_STATE_CURRENT.json"
    data = load(path)
    data["currentness_set"].append("MISSING_CURRENT_OWNER.json")
    save(path, data)


def main() -> int:
    positive_roots = [
        ROOT / "examples" / "minimal",
        ROOT / "examples" / "active_campaign",
        ROOT / "examples" / "terminal_candidate",
    ]
    for source in positive_roots:
        result = run_validator(source)
        if result.returncode != 0:
            raise AssertionError(
                f"positive fixture failed: {source}\n{result.stdout}\n{result.stderr}"
            )

    expect_failure(
        ROOT / "examples" / "active_campaign",
        break_checkpoint_ref,
        "active checkpoint ref",
        "checkpoint/current-code mismatch",
    )
    expect_failure(
        ROOT / "examples" / "active_campaign",
        break_authority_run,
        "authority run",
        "actor/run authority mismatch",
    )
    expect_failure(
        ROOT / "examples" / "terminal_candidate",
        break_terminal_evidence,
        "lacks evidence for charter gate RUNTIME_PHYSICAL",
        "missing terminal gate evidence",
    )
    expect_failure(
        ROOT / "examples" / "active_campaign",
        break_currentness_ref,
        "Currentness Set ref does not resolve",
        "missing currentness owner",
    )

    print("VALIDATION SELF-TEST PASSED")
    print("- positive lifecycle fixtures accepted")
    print("- checkpoint/current-ref mismatch rejected")
    print("- actor/run authority mismatch rejected")
    print("- missing terminal gate evidence rejected")
    print("- missing Currentness Set owner rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
