#!/usr/bin/env python3
"""I3-owned tactical plan revisions; immutable Goal stays untouched."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from goal_guard import (
    goal_fingerprint, read, confined, file_sha, fixed_control_path,
    GoalGuardError,
)
from sqlite_currentness import inspect_store
from state_tx import state_lock, write_json_set


class TacticalPlanError(ValueError):
    pass


def _runtime_review_snapshot(control: Path) -> tuple[int | None, int | None]:
    """Bind a Plan review to a structurally consistent campaign event head."""
    try:
        path = fixed_control_path(control, "runtime/CAMPAIGN_RUNTIME_CURRENT.json")
    except GoalGuardError as exc:
        raise TacticalPlanError("PLAN_RUNTIME_CONTROL_PATH_INVALID:" + str(exc)) from None
    if not path.exists():
        return None, None
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 32 * 1024 * 1024:
        raise TacticalPlanError("PLAN_RUNTIME_SNAPSHOT_UNTRUSTED")
    try:
        runtime = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise TacticalPlanError("PLAN_RUNTIME_SNAPSHOT_INVALID:" + type(exc).__name__) from None
    events = runtime.get("event_log") if isinstance(runtime, dict) else None
    revision = runtime.get("revision") if isinstance(runtime, dict) else None
    if (not isinstance(events, list) or type(revision) is not int
        or revision != len(events)
        or any(not isinstance(item, dict) or type(item.get("seq")) is not int
               or item["seq"] != index for index, item in enumerate(events, start=1))):
        raise TacticalPlanError("PLAN_RUNTIME_SNAPSHOT_CURRENTNESS_INVALID")
    return revision, (events[-1]["seq"] if events else 0)


def update(control: Path, *, expected_revision: int, plan: dict,
           review_evidence_ref: str) -> dict:
    if not isinstance(review_evidence_ref, str) or not review_evidence_ref:
        raise TacticalPlanError("REVIEW_EVIDENCE_REQUIRED")
    if (not isinstance(plan, dict)
        or not isinstance(plan.get("steps"), list)
        or any(not isinstance(step, dict) for step in plan["steps"])
        or not isinstance(plan.get("hypotheses", []), list)
        or not isinstance(plan.get("blockers", []), list)
        or not isinstance(plan.get("plan_mode", "UNVERIFIED"), str)
        or not plan.get("plan_mode", "UNVERIFIED")):
        raise TacticalPlanError("TACTICAL_PLAN_STEPS_INVALID")
    control = control.resolve()
    try:
        fixed_control_path(control, "state/GOAL_CONTRACT_CURRENT.json")
        fixed_control_path(control, "runtime/TACTICAL_PLAN_CURRENT.json")
        fixed_control_path(control, "runtime/.campaignctl.lock")
    except GoalGuardError as exc:
        raise TacticalPlanError("PLAN_CONTROL_PATH_INVALID:" + str(exc)) from None
    try:
        review_evidence = confined(control, review_evidence_ref)
        if not review_evidence.is_file():
            raise TacticalPlanError("REVIEW_EVIDENCE_MISSING")
        review_evidence_sha = file_sha(review_evidence)
    except GoalGuardError as exc:
        raise TacticalPlanError("REVIEW_EVIDENCE_INVALID:" + str(exc)) from None
    with state_lock(control):
        try:
            goal_path = fixed_control_path(control, "state/GOAL_CONTRACT_CURRENT.json")
            current_path = fixed_control_path(control, "runtime/TACTICAL_PLAN_CURRENT.json")
            goal = read(goal_path)
        except GoalGuardError as exc:
            raise TacticalPlanError("PLAN_GOAL_INTEGRITY_HOLD:" + str(exc)) from None
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
        reviewed_runtime_revision, reviewed_runtime_event_seq = _runtime_review_snapshot(control)
        old = read(current_path) if current_path.is_file() else None
        old_revision = old["revision"] if old else -1
        if old_revision != expected_revision:
            raise TacticalPlanError("TACTICAL_PLAN_REVISION_CONFLICT")
        if old and (old.get("goal_digest") != fingerprint or old.get("campaign_id") != goal["campaign_id"]):
            raise TacticalPlanError("GOAL_CHANGED_REPLAN_REQUIRES_I2_RECONCILIATION")
        try:
            if file_sha(confined(control, review_evidence_ref)) != review_evidence_sha:
                raise TacticalPlanError("REVIEW_EVIDENCE_CHANGED_DURING_UPDATE")
        except GoalGuardError as exc:
            raise TacticalPlanError("REVIEW_EVIDENCE_INVALID:" + str(exc)) from None
        try:
            if (fixed_control_path(control, "state/GOAL_CONTRACT_CURRENT.json") != goal_path
                or fixed_control_path(control, "runtime/TACTICAL_PLAN_CURRENT.json") != current_path):
                raise TacticalPlanError("PLAN_CONTROL_PATH_CHANGED_DURING_UPDATE")
        except GoalGuardError as exc:
            raise TacticalPlanError("PLAN_CONTROL_PATH_CHANGED_DURING_UPDATE:" + str(exc)) from None
        result = {
            "schema_version": "agentic-tactical-plan-v1",
            "campaign_id": goal["campaign_id"],
            "goal_digest": fingerprint,
            "revision": old_revision + 1,
            "steps": plan["steps"],
            "hypotheses": plan.get("hypotheses", []),
            "blockers": plan.get("blockers", []),
            "review_evidence_ref": review_evidence_ref,
            "review_evidence_sha256": review_evidence_sha,
            "reviewed_runtime_revision": reviewed_runtime_revision,
            "reviewed_runtime_event_seq": reviewed_runtime_event_seq,
            # Local Python callers cannot attest real active time or cause an
            # inseparable native pre-dispatch checkpoint. Unknown must remain
            # unknown so goal_guard keeps the host invocation on HOLD.
            "active_progress_minutes_since_review": None,
            "progress_clock": "HOST_UNVERIFIED_ADVISORY",
            "invocation_permit_issued": False,
            "plan_mode": plan.get("plan_mode", "UNVERIFIED"),
            "progress_tool": "NATIVE_HOST_PROGRESS_UNAVAILABLE",
        }
        write_json_set(control, "I3_TACTICAL_PLAN_REVISION", [(current_path, result)])
        return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--control-root", type=Path, required=True)
    parser.add_argument("--expected-revision", type=int, required=True)
    parser.add_argument("--plan-file", type=Path, required=True)
    parser.add_argument("--review-evidence-ref", required=True)
    args = parser.parse_args()
    try:
        result = update(args.control_root, expected_revision=args.expected_revision,
                        plan=json.loads(args.plan_file.read_text(encoding="utf-8")),
                        review_evidence_ref=args.review_evidence_ref)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f"PLAN HOLD: {type(exc).__name__}: {exc}\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
