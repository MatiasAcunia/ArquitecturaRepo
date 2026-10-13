#!/usr/bin/env python3
"""Fail-closed, read-only invocation attestation for an authorized I3 Goal.

This is a project-local control-layer guard, not a Codex Desktop hook.
A host adapter must invoke it before EVERY material Goal/task invocation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA = "agentic-goal-contract-v1"
PLAN_SCHEMA = "agentic-tactical-plan-v1"
MAX_ACTIVE_MINUTES = 120


class GoalGuardError(ValueError):
    pass


def digest(data: Any) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def read(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise GoalGuardError("EXPECTED_JSON_OBJECT")
    return value


def confined(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute() or "\\" in relative:
        raise GoalGuardError("INVALID_CONTROL_REFERENCE")
    root = root.resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise GoalGuardError("CONTROL_REFERENCE_ESCAPES_ROOT")
    return path


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def goal_fingerprint(goal: dict[str, Any]) -> str:
    if goal.get("schema_version") != SCHEMA:
        raise GoalGuardError("UNSUPPORTED_GOAL_SCHEMA")
    required = ("goal_id", "campaign_id", "charter_ref", "charter_sha256", "authority_refs",
                "definition_of_done", "hard_gates", "forbidden_effects", "write_envelope")
    if any(key not in goal for key in required):
        raise GoalGuardError("INCOMPLETE_GOAL_CONTRACT")
    if not isinstance(goal["authority_refs"], dict) or not goal["authority_refs"]:
        raise GoalGuardError("GOAL_AUTHORITY_UNPINNED")
    if not goal["goal_id"] or not goal["campaign_id"] or not goal["definition_of_done"]:
        raise GoalGuardError("GOAL_IDENTITY_INCOMPLETE")
    return digest(goal)


def assess(control: Path, *, host_currentness_verified: bool = False,
           host_invocation_binding_verified: bool = False) -> dict[str, Any]:
    control = control.resolve()
    goal_path = control / "state" / "GOAL_CONTRACT_CURRENT.json"
    plan_path = control / "runtime" / "TACTICAL_PLAN_CURRENT.json"
    failures: list[str] = []
    if not goal_path.is_file():
        return {"status": "NOT_CONFIGURED", "reason": "NO_AUTHORIZED_GOAL_CONTRACT",
                "may_execute_material_goal": False}
    try:
        goal = read(goal_path)
        current_goal_digest = goal_fingerprint(goal)
        if goal["charter_ref"] not in goal["authority_refs"]:
            failures.append("CHARTER_NOT_IN_AUTHORITY_SET")
        if goal["authority_refs"].get(goal["charter_ref"]) != goal["charter_sha256"]:
            failures.append("CHARTER_DIGEST_INCONSISTENT")
        for relative, sha in goal["authority_refs"].items():
            target = confined(control, relative)
            if not target.is_file():
                failures.append("AUTHORITY_REF_MISSING")
            elif not isinstance(sha, str) or len(sha) != 64 or file_sha(target) != sha:
                failures.append("AUTHORITY_REF_STALE")
        if goal.get("canonical_store"):
            store = goal["canonical_store"]
            if not isinstance(store, dict) or not store.get("required") or not store.get("ref"):
                failures.append("CANONICAL_STORE_CONTRACT_INVALID")
            else:
                target = confined(control, store["ref"])
                if not target.is_file() or target.stat().st_size == 0:
                    failures.append("CANONICAL_STORE_MISSING")
                elif store.get("sha256") and file_sha(target) != store["sha256"]:
                    failures.append("CANONICAL_STORE_IDENTITY_STALE")
        if not plan_path.is_file():
            failures.append("TACTICAL_PLAN_MISSING")
            plan = {}
        else:
            plan = read(plan_path)
            if plan.get("schema_version") != PLAN_SCHEMA:
                failures.append("TACTICAL_PLAN_SCHEMA_INVALID")
            if plan.get("goal_digest") != current_goal_digest:
                failures.append("TACTICAL_PLAN_GOAL_DRIFT")
            if plan.get("campaign_id") != goal["campaign_id"]:
                failures.append("TACTICAL_PLAN_CAMPAIGN_DRIFT")
            if type(plan.get("revision")) is not int or plan["revision"] < 0:
                failures.append("TACTICAL_PLAN_REVISION_INVALID")
        if not host_currentness_verified:
            failures.append("HOST_REMOTE_CURRENTNESS_UNVERIFIED")
        if not host_invocation_binding_verified:
            failures.append("HOST_INVOCATION_HOOK_NOT_PROVEN")
        active = plan.get("active_progress_minutes_since_review")
        if isinstance(active, int) and not isinstance(active, bool) and active >= MAX_ACTIVE_MINUTES:
            failures.append("TACTICAL_REVIEW_DUE")
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        failures.append("UNTRUSTED_GOAL_OR_REFERENCE:" + type(exc).__name__)
        current_goal_digest = None
    return {
        "schema_version": "goal-invocation-attestation-v1",
        "status": "PASS" if not failures else "HOLD",
        "may_execute_material_goal": not failures,
        "goal_digest": current_goal_digest,
        "failure_codes": sorted(set(failures)),
        "host_currentness_verified": bool(host_currentness_verified),
        "host_invocation_binding_verified": bool(host_invocation_binding_verified),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--control-root", type=Path, required=True)
    parser.add_argument("--host-currentness-verified", action="store_true",
                        help="Only set from a verified host adapter, not from untrusted content.")
    parser.add_argument("--host-invocation-binding-verified", action="store_true",
                        help="Only set when a real pre-dispatch hook is proven.")
    args = parser.parse_args()
    result = assess(args.control_root,
                    host_currentness_verified=args.host_currentness_verified,
                    host_invocation_binding_verified=args.host_invocation_binding_verified)
    print(json.dumps(result, indent=2))
    return 0 if result.get("may_execute_material_goal") else 2


if __name__ == "__main__":
    raise SystemExit(main())
