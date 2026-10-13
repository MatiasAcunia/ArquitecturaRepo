#!/usr/bin/env python3
"""I3-owned tactical plan revisions; immutable Goal stays untouched."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from goal_guard import goal_fingerprint, read, confined, file_sha, GoalGuardError
from sqlite_currentness import inspect_store
from state_tx import state_lock, write_json_set


class TacticalPlanError(ValueError):
    pass


def update(control: Path, *, expected_revision: int, plan: dict,
           active_minutes: int, review_evidence_ref: str) -> dict:
    if type(active_minutes) is not int or active_minutes < 0 or active_minutes > 120:
        raise TacticalPlanError("ACTIVE_MINUTES_OUT_OF_RANGE")
    if not isinstance(review_evidence_ref, str) or not review_evidence_ref:
        raise TacticalPlanError("REVIEW_EVIDENCE_REQUIRED")
    if not isinstance(plan, dict) or not isinstance(plan.get("steps"), list):
        raise TacticalPlanError("TACTICAL_PLAN_STEPS_INVALID")
    control = control.resolve()
    with state_lock(control):
        goal = read(control / "state" / "GOAL_CONTRACT_CURRENT.json")
        fingerprint = goal_fingerprint(goal)
        # The Plan is not an invocation authorization. Even this local
        # revision must not be persisted against a stale charter, an invalid
        # Goal authority reference, or a missing required canonical store.
        try:
            for relative, expected_sha in goal["authority_refs"].items():
                reference = confined(control, relative)
                if not reference.is_file() or file_sha(reference) != expected_sha:
                    raise TacticalPlanError("PLAN_AUTHORITY_REF_STALE_OR_MISSING")
            if "canonical_store" in goal:
                source = goal["canonical_store"]
                store = confined(control, source["ref"])
                if not store.is_file() or store.stat().st_size == 0:
                    raise TacticalPlanError("PLAN_CANONICAL_STORE_MISSING")
                if "sha256" in source and file_sha(store) != source["sha256"]:
                    raise TacticalPlanError("PLAN_CANONICAL_STORE_CHANGED")
                failures = inspect_store(store, source)
                if failures:
                    raise TacticalPlanError("PLAN_CANONICAL_STORE_HOLD:" + ",".join(failures))
        except GoalGuardError as exc:
            raise TacticalPlanError("PLAN_GOAL_INTEGRITY_HOLD:" + str(exc)) from None
        current_path = control / "runtime" / "TACTICAL_PLAN_CURRENT.json"
        old = read(current_path) if current_path.is_file() else None
        old_revision = old["revision"] if old else -1
        if old_revision != expected_revision:
            raise TacticalPlanError("TACTICAL_PLAN_REVISION_CONFLICT")
        if old and (old.get("goal_digest") != fingerprint or old.get("campaign_id") != goal["campaign_id"]):
            raise TacticalPlanError("GOAL_CHANGED_REPLAN_REQUIRES_I2_RECONCILIATION")
        result = {
            "schema_version": "agentic-tactical-plan-v1",
            "campaign_id": goal["campaign_id"],
            "goal_digest": fingerprint,
            "revision": old_revision + 1,
            "steps": plan["steps"],
            "hypotheses": plan.get("hypotheses", []),
            "blockers": plan.get("blockers", []),
            "review_evidence_ref": review_evidence_ref,
            "active_progress_minutes_since_review": active_minutes,
            "plan_mode": plan.get("plan_mode", "UNVERIFIED"),
            "progress_tool": plan.get("progress_tool", "UNVERIFIED"),
        }
        write_json_set(control, "I3_TACTICAL_PLAN_REVISION", [(current_path, result)])
        return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--control-root", type=Path, required=True)
    parser.add_argument("--expected-revision", type=int, required=True)
    parser.add_argument("--plan-file", type=Path, required=True)
    parser.add_argument("--active-minutes", type=int, required=True)
    parser.add_argument("--review-evidence-ref", required=True)
    args = parser.parse_args()
    try:
        result = update(args.control_root, expected_revision=args.expected_revision,
                        plan=json.loads(args.plan_file.read_text(encoding="utf-8")),
                        active_minutes=args.active_minutes,
                        review_evidence_ref=args.review_evidence_ref)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f"PLAN HOLD: {type(exc).__name__}: {exc}\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
