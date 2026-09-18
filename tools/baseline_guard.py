#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

REQ_REF = "state/CLIENT_REQUIREMENTS_CURRENT.md"
TECH_REF = "state/TECHNICAL_BASELINE_CURRENT.json"
PLAN_REF = "state/DELIVERY_PLAN_CURRENT.json"
PS_REF = "state/PRODUCT_STATE_CURRENT.json"
PLACEHOLDERS = {"", "UNDECIDED", "TO_BE_DECIDED", "TO_BE_RECORDED", "UNKNOWN"}


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected object: {path}")
    return data


def requirements_metadata(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    if not path.exists():
        return result
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        for key in ("Baseline status", "Baseline version", "CLIENT confirmation", "Confirmed at"):
            prefix = key + ":"
            if line.startswith(prefix):
                result[key] = line[len(prefix):].strip()
    return result


def evaluate_baseline(control: Path) -> dict[str, Any]:
    control = control.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    req_path = control / REQ_REF
    tech_path = control / TECH_REF
    plan_path = control / PLAN_REF
    ps_path = control / PS_REF

    for ref, path in ((REQ_REF, req_path), (TECH_REF, tech_path), (PLAN_REF, plan_path), (PS_REF, ps_path)):
        if not path.exists():
            errors.append(f"missing baseline surface: {ref}")
    if errors:
        return {"ready": False, "errors": errors, "warnings": warnings}

    req = requirements_metadata(req_path)
    if req.get("Baseline status") != "CLIENT_CONFIRMED":
        errors.append("requirements baseline is not CLIENT_CONFIRMED")
    if req.get("CLIENT confirmation") != "CONFIRMED":
        errors.append("CLIENT confirmation is not CONFIRMED")
    confirmed_at = req.get("Confirmed at")
    if not confirmed_at or confirmed_at == "PENDING":
        errors.append("requirements confirmation timestamp is missing")
    else:
        try:
            datetime.fromisoformat(confirmed_at.replace("Z", "+00:00"))
        except ValueError:
            errors.append("requirements confirmation timestamp is not ISO-8601")

    ps = load_json(ps_path)
    product = ps.get("product_or_workstream")
    tech = load_json(tech_path)

    if tech.get("schema_version") != "technical-baseline-0.1":
        errors.append("unsupported technical baseline schema")
    if tech.get("product_or_workstream") != product:
        errors.append("technical baseline product/workstream differs from Product State")
    if tech.get("status") != "CURRENT":
        errors.append("technical baseline is not CURRENT")
    if tech.get("unresolved"):
        errors.append("technical baseline still has unresolved items")

    environment = tech.get("environment", {})
    machine = environment.get("machine_profile", {})
    if environment.get("network_mode") == "UNDECIDED":
        errors.append("network exposure mode is UNDECIDED")
    if str(environment.get("deployment_target", "")).strip() in PLACEHOLDERS:
        errors.append("deployment target is not decided")
    if machine.get("assessment_status") == "UNASSESSED":
        errors.append("machine/environment capability has not been assessed")

    stack = tech.get("stack", {})
    for key in ("language", "runtime", "backend", "frontend", "database", "test_stack", "deployment", "rationale"):
        if str(stack.get(key, "")).strip() in PLACEHOLDERS:
            errors.append(f"technical stack field is not decided: {key}")

    security = tech.get("security", {})
    for key in ("authentication_model", "authorization_model", "secrets_management", "data_classification", "backup_recovery"):
        if str(security.get(key, "")).strip() in PLACEHOLDERS:
            errors.append(f"security field is not decided: {key}")
    if not security.get("exposure_controls"):
        errors.append("security exposure controls are empty")

    if not tech.get("ui_quality", {}).get("required_checks"):
        errors.append("UI quality checks are empty")

    plan = load_json(plan_path)
    if plan.get("schema_version") != "delivery-plan-0.1":
        errors.append("unsupported delivery plan schema")
    if plan.get("product_or_workstream") != product:
        errors.append("delivery plan product/workstream differs from Product State")
    if plan.get("status") != "CURRENT":
        errors.append("delivery plan is not CURRENT")
    if plan.get("unresolved"):
        errors.append("delivery plan still has unresolved items")
    if not plan.get("target_release_date"):
        errors.append("delivery plan has no target release date")
    if not plan.get("next_review_date"):
        errors.append("delivery plan has no next schedule review date")

    milestones = plan.get("milestones", [])
    if not milestones:
        errors.append("delivery plan has no milestones")
    seen: set[str] = set()
    for milestone in milestones:
        mid = milestone.get("id")
        if not mid:
            errors.append("delivery milestone missing id")
            continue
        if mid in seen:
            errors.append(f"duplicate delivery milestone id: {mid}")
        seen.add(mid)
        if not milestone.get("target_date"):
            errors.append(f"{mid}: target date missing")
        if not milestone.get("done_when"):
            errors.append(f"{mid}: done condition missing")
        if milestone.get("forecast_confidence") not in {"HIGH", "MEDIUM", "LOW"}:
            errors.append(f"{mid}: forecast confidence invalid")

    try:
        start = date.fromisoformat(plan["planning_start_date"])
        target = date.fromisoformat(plan["target_release_date"]) if plan.get("target_release_date") else None
        if target and target < start:
            errors.append("target release date precedes planning start date")
    except (KeyError, ValueError):
        errors.append("delivery plan contains invalid planning/release date")

    if plan.get("next_review_date"):
        try:
            if date.fromisoformat(plan["next_review_date"]) < date.today():
                warnings.append("next schedule review date is overdue")
        except ValueError:
            errors.append("next schedule review date is invalid")

    return {
        "ready": not errors,
        "product_or_workstream": product,
        "requirements": req,
        "technical_status": tech.get("status"),
        "delivery_status": plan.get("status"),
        "target_release_date": plan.get("target_release_date"),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check pre-campaign product/technical/delivery baseline readiness.")
    parser.add_argument("--control-root", default=".agentic-sdlc")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = evaluate_baseline(Path(args.control_root))
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("PROJECT BASELINE " + ("READY" if report["ready"] else "BLOCKED"))
        for item in report.get("errors", []):
            print(f"- ERROR: {item}")
        for item in report.get("warnings", []):
            print(f"- WARNING: {item}")
        if report.get("target_release_date"):
            print(f"- target release: {report['target_release_date']}")
    return 0 if report["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
