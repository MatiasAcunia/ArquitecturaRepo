#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

from baseline_guard import evaluate_baseline, load_json, requirements_metadata


def build_status(control: Path) -> dict[str, Any]:
    control = control.resolve()
    product = load_json(control / "state" / "PRODUCT_STATE_CURRENT.json")
    plan_path = control / "state" / "DELIVERY_PLAN_CURRENT.json"
    tech_path = control / "state" / "TECHNICAL_BASELINE_CURRENT.json"
    plan = load_json(plan_path) if plan_path.exists() else {}
    tech = load_json(tech_path) if tech_path.exists() else {}
    req = requirements_metadata(control / "state" / "CLIENT_REQUIREMENTS_CURRENT.md")
    baseline = evaluate_baseline(control)

    today = date.today()
    overdue = []
    next_milestone = None
    for milestone in sorted(plan.get("milestones", []), key=lambda item: item.get("target_date", "9999-12-31")):
        if milestone.get("status") not in {"DONE", "SUPERSEDED"}:
            if next_milestone is None:
                next_milestone = {
                    "id": milestone.get("id"),
                    "title": milestone.get("title"),
                    "target_date": milestone.get("target_date"),
                    "status": milestone.get("status"),
                }
            try:
                if date.fromisoformat(milestone.get("target_date", "")) < today:
                    overdue.append(milestone.get("id"))
            except ValueError:
                pass

    return {
        "schema_version": "project-status-view-0.1",
        "product_or_workstream": product.get("product_or_workstream"),
        "product_status": product.get("status"),
        "current_code_ref": product.get("current_code_ref"),
        "current_gate": product.get("current_gate"),
        "active_campaign_id": (product.get("active_campaign") or {}).get("campaign_id"),
        "requirements_baseline": req,
        "baseline_ready": baseline.get("ready", False),
        "baseline_errors": baseline.get("errors", []),
        "technical_baseline_status": tech.get("status"),
        "network_mode": (tech.get("environment") or {}).get("network_mode"),
        "deployment_target": (tech.get("environment") or {}).get("deployment_target"),
        "target_release_date": plan.get("target_release_date"),
        "next_schedule_review": plan.get("next_review_date"),
        "next_milestone": next_milestone,
        "overdue_milestone_ids": overdue,
        "blockers": product.get("blockers", []),
        "open_product_questions": product.get("open_product_questions", []),
        "next_legal_boundary": product.get("next_legal_boundary"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a derived project status from canonical Agentic SDLC state.")
    parser.add_argument("--control-root", default=".agentic-sdlc")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    status = build_status(Path(args.control_root))
    if args.json:
        print(json.dumps(status, indent=2))
    else:
        print(f"PROJECT: {status['product_or_workstream']}")
        print(f"STATUS/GATE: {status['product_status']} / {status['current_gate']}")
        print(f"BASELINE READY: {status['baseline_ready']}")
        print(f"TARGET RELEASE: {status['target_release_date']}")
        print(f"NEXT MILESTONE: {status['next_milestone']}")
        print(f"OVERDUE: {status['overdue_milestone_ids']}")
        print(f"ACTIVE CAMPAIGN: {status['active_campaign_id']}")
        print(f"NEXT LEGAL BOUNDARY: {status['next_legal_boundary']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
