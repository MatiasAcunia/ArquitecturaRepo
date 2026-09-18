#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ALLOWED_REVIEW_RATINGS = {"GOOD", "MIXED", "POOR", "UNKNOWN"}
ALLOWED_TRIGGER = {"WEEKLY", "MONTHLY", "MANUAL"}


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def parse_review_rating(path: Path) -> str:
    if not path.exists():
        return "UNKNOWN"
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("- rating:"):
            value = line.split(":", 1)[1].strip()
            return value if value in ALLOWED_REVIEW_RATINGS else "UNKNOWN"
    return "UNKNOWN"


def validate_control(control: Path) -> bool:
    validator = control / "tools" / "validate_project.py"
    if not validator.exists():
        return False
    completed = subprocess.run(
        [sys.executable, str(validator), "--root", str(control)],
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.returncode == 0


def baseline_ready(control: Path) -> bool:
    guard = control / "tools" / "baseline_guard.py"
    if not guard.exists():
        return False
    completed = subprocess.run(
        [sys.executable, str(guard), "--control-root", str(control), "--json"],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return False
    try:
        return bool(json.loads(completed.stdout).get("ready"))
    except Exception:
        return False


def count_runtime_events(runtime: dict[str, Any]) -> dict[str, int]:
    actions = Counter(
        item.get("action")
        for item in runtime.get("event_log", [])
        if isinstance(item, dict) and isinstance(item.get("action"), str)
    )

    def count_matching(*tokens: str) -> int:
        total = 0
        for action, count in actions.items():
            upper = action.upper()
            if any(token in upper for token in tokens):
                total += count
        return total

    return {
        "retry_events": count_matching("RETRY"),
        "failure_events": count_matching("FAIL"),
        "hold_events": count_matching("HOLD", "CAPACITY_CHECKPOINT"),
        "review_invalidation_events": count_matching("INVALIDAT"),
        "recovery_events": count_matching("RECOVER"),
    }


def build_report(control: Path, trigger: str) -> dict[str, Any]:
    profile = load_json(control / "PROFILE.json")
    product = load_json(control / "state" / "PRODUCT_STATE_CURRENT.json")
    bootstrap = load_json(control / "state" / "CURRENT_BOOTSTRAP_STATE.json")
    owners = load_json(control / "state" / "OWNER_REGISTRY_CURRENT.json")
    tech = load_json(control / "state" / "TECHNICAL_BASELINE_CURRENT.json")
    delivery = load_json(control / "state" / "DELIVERY_PLAN_CURRENT.json")
    runtime = load_json(control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json")

    currentness = bootstrap.get("currentness", {})
    milestones = delivery.get("milestones", []) if isinstance(delivery.get("milestones"), list) else []
    overdue = 0
    today = date.today()
    for milestone in milestones:
        if not isinstance(milestone, dict):
            continue
        if milestone.get("status") in {"DONE", "SUPERSEDED"}:
            continue
        value = milestone.get("target_date")
        if not isinstance(value, str):
            continue
        try:
            if date.fromisoformat(value) < today:
                overdue += 1
        except ValueError:
            pass

    work_status_counts = Counter()
    for item in runtime.get("work_units", []) if isinstance(runtime.get("work_units"), list) else []:
        if isinstance(item, dict) and isinstance(item.get("status"), str):
            work_status_counts[item["status"]] += 1

    event_counts = count_runtime_events(runtime)
    machine = tech.get("environment", {}).get("machine_profile", {}) if tech else {}
    network_mode = tech.get("environment", {}).get("network_mode") if tech else None

    starter_version = profile.get("starter_version")
    if not isinstance(starter_version, str) or not starter_version:
        manifest = load_json(control / "state" / "STARTER_MANIFEST.json")
        starter_version = manifest.get("version") if isinstance(manifest.get("version"), str) else "UNKNOWN"

    capabilities = product.get("capabilities", [])
    if not isinstance(capabilities, list):
        capabilities = []
    current_owners = [
        item
        for item in owners.get("owners", [])
        if isinstance(item, dict) and item.get("status") == "CURRENT"
    ]

    report = {
        "schema_version": "architecture-feedback-report-0.1",
        "starter_version": starter_version,
        "trigger": trigger,
        "profile": profile.get("profile") if isinstance(profile.get("profile"), str) else "STARTER_OR_UNKNOWN",
        "runtime_enabled": bool(profile.get("runtime_enabled", bool(runtime))),
        "control": {
            "validation_passed": validate_control(control),
            "bootstrap_status": bootstrap.get("status") if isinstance(bootstrap.get("status"), str) else None,
            "currentness_verified": bool(currentness.get("verified", False)),
            "product_status": product.get("status") if isinstance(product.get("status"), str) else None,
            "owner_count": len(current_owners),
            "capability_count": len(capabilities),
            "active_campaign": bool(product.get("active_campaign")),
            "pending_transition": (control / "runtime" / "transactions" / "CURRENT_TRANSACTION.json").exists(),
        },
        "project_baseline": {
            "present": bool(tech or delivery),
            "ready": baseline_ready(control) if tech or delivery else False,
            "technical_status": tech.get("status") if isinstance(tech.get("status"), str) else None,
            "machine_assessment_status": machine.get("assessment_status") if isinstance(machine.get("assessment_status"), str) else None,
            "network_mode": network_mode if isinstance(network_mode, str) else None,
            "delivery_status": delivery.get("status") if isinstance(delivery.get("status"), str) else None,
            "milestone_count": len(milestones),
            "overdue_milestone_count": overdue,
            "schedule_change_count": len(delivery.get("schedule_changes", [])) if isinstance(delivery.get("schedule_changes"), list) else 0,
        },
        "runtime": {
            "present": bool(runtime),
            "campaign_status": runtime.get("campaign_status") if isinstance(runtime.get("campaign_status"), str) else None,
            "work_status_counts": dict(sorted(work_status_counts.items())),
            **event_counts,
        },
        "process": {
            "operating_review_rating": parse_review_rating(
                control / "governance" / "AGENTIC_SDLC_OPERATING_REVIEW_CURRENT.md"
            ),
        },
        "privacy": {
            "mode": "STRICT_METADATA_ONLY",
            "free_text_included": False,
            "project_identifiers_included": False,
            "code_or_paths_included": False,
            "requirements_content_included": False,
            "credentials_included": False,
        },
    }
    return report


def write_github_output(path: str | None, values: dict[str, str]) -> None:
    if not path:
        return
    with Path(path).open("a", encoding="utf-8") as handle:
        for key, value in values.items():
            handle.write(f"{key}={value}\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate privacy-preserving Agentic SDLC architecture feedback."
    )
    parser.add_argument("--control-root", default=".agentic-sdlc")
    parser.add_argument("--trigger", choices=sorted(ALLOWED_TRIGGER), required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--github-output")
    args = parser.parse_args()

    control = Path(args.control_root).resolve()
    config_path = control / "feedback" / "ARCHITECTURE_FEEDBACK_CONFIG.json"
    config = load_json(config_path)

    enabled = config.get("enabled") is True
    cadence = config.get("cadence")
    artifact_enabled = config.get("artifact_enabled") is True
    external_enabled = config.get("external_submission_enabled") is True
    privacy_mode = config.get("privacy_mode")

    if not enabled:
        write_github_output(
            args.github_output,
            {
                "emitted": "false",
                "artifact_enabled": str(artifact_enabled).lower(),
                "external_submission_enabled": str(external_enabled).lower(),
                "reason": "disabled",
            },
        )
        print("ARCHITECTURE FEEDBACK DISABLED")
        return 0

    if privacy_mode != "STRICT_METADATA_ONLY":
        print("ARCHITECTURE FEEDBACK REFUSED: unsupported privacy mode", file=sys.stderr)
        return 1

    if args.trigger != "MANUAL" and cadence != args.trigger:
        write_github_output(
            args.github_output,
            {
                "emitted": "false",
                "artifact_enabled": str(artifact_enabled).lower(),
                "external_submission_enabled": str(external_enabled).lower(),
                "reason": "cadence_mismatch",
            },
        )
        print(f"ARCHITECTURE FEEDBACK SKIPPED: configured cadence={cadence}")
        return 0

    report = build_report(control, args.trigger)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    write_github_output(
        args.github_output,
        {
            "emitted": "true",
            "artifact_enabled": str(artifact_enabled).lower(),
            "external_submission_enabled": str(external_enabled).lower(),
            "reason": "generated",
        },
    )
    print("ARCHITECTURE FEEDBACK REPORT GENERATED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
