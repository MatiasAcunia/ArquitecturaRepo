#!/usr/bin/env python3
"""Fail-closed Goal boundary *diagnostic*. It never grants host execution.

Canonical Goal/charter and I3 Plan are project-local data. Only a separately
validated, actual host pre-dispatch hook with canonical remote authority can
issue an invocation permit. A CLI switch or Python caller must not forge it.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from sqlite_currentness import inspect_store
from state_tx import sha256_file


SCHEMA = "agentic-goal-contract-v1"
PLAN_SCHEMA = "agentic-tactical-plan-v1"
MAX_ACTIVE_MINUTES = 120
MAX_JSON_BYTES = 1024 * 1024
MAX_AUTHORITY_BYTES = 32 * 1024 * 1024
MAX_REFS = 64
SHA = re.compile(r"^[0-9a-f]{64}$")


class GoalGuardError(ValueError):
    pass


def digest(data: Any) -> str:
    return hashlib.sha256(json.dumps(
        data, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")).hexdigest()


def read(path: Path) -> dict[str, Any]:
    if path.is_symlink():
        raise GoalGuardError("SYMLINKED_CONTROL_FILE")
    if path.stat().st_size > MAX_JSON_BYTES:
        raise GoalGuardError("CONTROL_JSON_TOO_LARGE")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise GoalGuardError("EXPECTED_JSON_OBJECT")
    return data


def confined(root: Path, relative: str) -> Path:
    if (not isinstance(relative, str) or not relative
        or len(relative) > 300 or "\\" in relative or ":" in relative
        or Path(relative).is_absolute() or any(
            part in {"", ".", ".."} for part in relative.split("/")
        )):
        raise GoalGuardError("INVALID_CONTROL_REFERENCE")
    root = root.resolve()
    candidate = root / relative
    if candidate.is_symlink():
        raise GoalGuardError("SYMLINKED_CONTROL_REFERENCE")
    path = candidate.resolve()
    if not path.is_relative_to(root):
        raise GoalGuardError("CONTROL_REFERENCE_ESCAPES_ROOT")
    return path


def fixed_control_path(root: Path, relative: str) -> Path:
    """Resolve a fixed control path while rejecting symlinked components."""
    root = root.resolve()
    if (not isinstance(relative, str) or not relative or "\\" in relative
        or Path(relative).is_absolute()
        or any(part in {"", ".", ".."} for part in relative.split("/"))):
        raise GoalGuardError("INVALID_FIXED_CONTROL_PATH")
    path = root
    for part in relative.split("/"):
        path = path / part
        if path.is_symlink():
            raise GoalGuardError("SYMLINKED_CONTROL_PATH")
    if not path.resolve().is_relative_to(root):
        raise GoalGuardError("CONTROL_PATH_ESCAPES_ROOT")
    return path


def file_sha(path: Path) -> str:
    if not path.is_file() or path.stat().st_size > MAX_AUTHORITY_BYTES:
        raise GoalGuardError("AUTHORITY_REFERENCE_UNREADABLE_OR_TOO_LARGE")
    digest = sha256_file(path)
    if digest is None:
        raise GoalGuardError("AUTHORITY_REFERENCE_UNREADABLE_OR_TOO_LARGE")
    return digest


def goal_fingerprint(goal: dict[str, Any]) -> str:
    if goal.get("schema_version") != SCHEMA:
        raise GoalGuardError("UNSUPPORTED_GOAL_SCHEMA")
    required = ("goal_id", "campaign_id", "charter_ref", "charter_sha256",
                "authority_refs", "definition_of_done", "hard_gates",
                "forbidden_effects", "write_envelope")
    if any(key not in goal for key in required):
        raise GoalGuardError("INCOMPLETE_GOAL_CONTRACT")
    for name in ("goal_id", "campaign_id", "charter_ref", "definition_of_done"):
        if not isinstance(goal[name], str) or not (1 <= len(goal[name]) <= 2000):
            raise GoalGuardError("GOAL_IDENTITY_INCOMPLETE")
    for name in ("hard_gates", "forbidden_effects", "write_envelope"):
        if (not isinstance(goal[name], list)
            or any(not isinstance(v, str) or not v or len(v) > 1024
                   for v in goal[name])):
            raise GoalGuardError("INVALID_GOAL_ENVELOPE")
    refs = goal["authority_refs"]
    if not isinstance(refs, dict) or not (1 <= len(refs) <= MAX_REFS):
        raise GoalGuardError("GOAL_AUTHORITY_UNPINNED")
    if any(not isinstance(k, str) or not isinstance(v, str) or
           not SHA.fullmatch(v) for k, v in refs.items()):
        raise GoalGuardError("AUTHORITY_DIGEST_INVALID")
    if goal["charter_ref"] not in refs or refs[goal["charter_ref"]] != goal["charter_sha256"]:
        raise GoalGuardError("CHARTER_DIGEST_INCONSISTENT")
    if "canonical_store" in goal:
        store = goal["canonical_store"]
        if (not isinstance(store, dict) or store.get("required") is not True
            or not isinstance(store.get("ref"), str)):
            raise GoalGuardError("CANONICAL_STORE_CONTRACT_INVALID")
        if "sha256" in store and not SHA.fullmatch(str(store["sha256"])):
            raise GoalGuardError("CANONICAL_STORE_DIGEST_INVALID")
    return digest(goal)


def tactical_review_assessment(control: Path, plan: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Project material campaign events since the exact runtime head reviewed by I3."""
    failures: list[str] = []
    projection: dict[str, Any] = {
        "event_triggered": False,
        "trigger_events": [],
        "max_verified_active_minutes": MAX_ACTIVE_MINUTES,
        "active_minutes_since_review": None,
        "active_time_status": "UNKNOWN_NATIVE_ACTIVE_CLOCK_UNAVAILABLE",
        # Unknown active time cannot be treated as under the 120-minute limit.
        "review_required": True,
    }
    try:
        runtime_path = fixed_control_path(control, "runtime/CAMPAIGN_RUNTIME_CURRENT.json")
        reviewed_revision = plan.get("reviewed_runtime_revision")
        reviewed_seq = plan.get("reviewed_runtime_event_seq")
        if reviewed_revision is None or reviewed_seq is None:
            failures.append("TACTICAL_PLAN_RUNTIME_REVIEW_UNBOUND")
            return projection, failures
        if type(reviewed_revision) is not int or reviewed_revision < 0 or type(reviewed_seq) is not int or reviewed_seq < 0:
            failures.append("TACTICAL_PLAN_RUNTIME_REVIEW_BINDING_INVALID")
            return projection, failures
        if runtime_path.is_symlink() or not runtime_path.is_file() or runtime_path.stat().st_size > MAX_AUTHORITY_BYTES:
            failures.append("TACTICAL_PLAN_RUNTIME_MISSING_OR_UNTRUSTED")
            return projection, failures
        runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
        if not isinstance(runtime, dict):
            failures.append("TACTICAL_PLAN_RUNTIME_CURRENTNESS_INVALID")
            return projection, failures
        events = runtime.get("event_log")
        revision = runtime.get("revision")
        if (not isinstance(events, list) or type(revision) is not int
            or revision != len(events)
            or any(not isinstance(item, dict) or type(item.get("seq")) is not int
                   or item["seq"] != index for index, item in enumerate(events, start=1))
            or reviewed_seq > revision or reviewed_revision != reviewed_seq):
            failures.append("TACTICAL_PLAN_RUNTIME_CURRENTNESS_INVALID")
            return projection, failures
        triggers = [
            {"seq": item["seq"], "action": item.get("action", "UNKNOWN_EVENT"),
             "work_unit_id": item.get("work_unit_id")}
            for item in events[reviewed_seq:]
            if item.get("action") != "HOST_DISPATCH_COMMAND_OBSERVED"
        ]
        projection["event_triggered"] = bool(triggers)
        projection["trigger_events"] = triggers
        if triggers:
            failures.append("TACTICAL_PLAN_EVENT_REVIEW_REQUIRED")
    except (OSError, ValueError, TypeError, KeyError, GoalGuardError):
        failures.append("TACTICAL_PLAN_RUNTIME_CURRENTNESS_INVALID")
    return projection, failures


def assess(control: Path) -> dict[str, Any]:
    """Return local integrity evidence; *never* authorize the host."""
    control = control.resolve()
    try:
        goal_path = fixed_control_path(control, "state/GOAL_CONTRACT_CURRENT.json")
        plan_path = fixed_control_path(control, "runtime/TACTICAL_PLAN_CURRENT.json")
        fixed_control_path(control, "runtime/.campaignctl.lock")
    except GoalGuardError as exc:
        return {
            "schema_version": "goal-invocation-attestation-v1",
            "status": "HOLD",
            "local_integrity_passed": False,
            "may_execute_material_goal": False,
            "failure_codes": ["UNTRUSTED_GOAL_OR_REFERENCE:" + type(exc).__name__],
        }
    if not goal_path.is_file():
        return {"schema_version": "goal-invocation-attestation-v1",
                "status": "NOT_CONFIGURED",
                "local_integrity_passed": False,
                "failure_codes": ["NO_AUTHORIZED_GOAL_CONTRACT"],
                "may_execute_material_goal": False}
    failures: list[str] = []
    current_goal_digest = None
    tactical_review: dict[str, Any] = {
        "event_triggered": False,
        "trigger_events": [],
        "max_verified_active_minutes": MAX_ACTIVE_MINUTES,
        "active_minutes_since_review": None,
        "active_time_status": "UNKNOWN_NATIVE_ACTIVE_CLOCK_UNAVAILABLE",
        "review_required": True,
    }
    try:
        goal = read(goal_path)
        current_goal_digest = goal_fingerprint(goal)
        for relative, expected in goal["authority_refs"].items():
            actual = confined(control, relative)
            if not actual.is_file():
                failures.append("AUTHORITY_REF_MISSING")
            elif file_sha(actual) != expected:
                failures.append("AUTHORITY_REF_STALE")
        if "canonical_store" in goal:
            store = goal["canonical_store"]
            store_ref = confined(control, store["ref"])
            if not store_ref.is_file() or store_ref.stat().st_size == 0:
                failures.append("CANONICAL_STORE_MISSING")
            else:
                if "sha256" in store and file_sha(store_ref) != store["sha256"]:
                    failures.append("CANONICAL_STORE_IDENTITY_STALE")
                # A bare database-file hash can remain unchanged while
                # committed transactions exist only in SQLite WAL.
                failures.extend(inspect_store(store_ref, store))
        if not plan_path.is_file():
            failures.append("TACTICAL_PLAN_MISSING")
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
            evidence_ref = plan.get("review_evidence_ref")
            evidence_digest = plan.get("review_evidence_sha256")
            if not isinstance(evidence_digest, str) or not SHA.fullmatch(evidence_digest):
                failures.append("TACTICAL_REVIEW_EVIDENCE_DIGEST_INVALID")
            else:
                try:
                    evidence_path = confined(control, evidence_ref)
                    if not evidence_path.is_file() or file_sha(evidence_path) != evidence_digest:
                        failures.append("TACTICAL_REVIEW_EVIDENCE_STALE_OR_MISSING")
                except (GoalGuardError, OSError, ValueError, TypeError):
                    failures.append("TACTICAL_REVIEW_EVIDENCE_INVALID")
            active = plan.get("active_progress_minutes_since_review")
            # No authenticated native progress-attestation path is connected
            # in this candidate. Only the local writer's explicitly unknown
            # state is representable; native-looking JSON fields are not proof.
            if (active is not None
                or plan.get("progress_clock") != "HOST_UNVERIFIED_ADVISORY"
                or plan.get("invocation_permit_issued") is not False
                or plan.get("progress_tool") != "NATIVE_HOST_PROGRESS_UNAVAILABLE"):
                failures.append("TACTICAL_PROGRESS_CLAIM_UNTRUSTED")
            tactical_review, review_failures = tactical_review_assessment(control, plan)
            failures.extend(review_failures)
            # The only accepted local state is unknown; unknown active time
            # cannot clear a host-enforced review checkpoint.
            failures.append("TACTICAL_REVIEW_DUE_OR_UNVERIFIED")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        failures.append("UNTRUSTED_GOAL_OR_REFERENCE:" + type(exc).__name__)

    # The guard is not an actual, inseparable Goal host hook. It cannot
    # independently attest host identity, remote HEAD or model invocation.
    return {
        "schema_version": "goal-invocation-attestation-v1",
        "status": "HOLD",
        "local_integrity_passed": not failures,
        "may_execute_material_goal": False,
        "goal_digest": current_goal_digest,
        "tactical_review": tactical_review,
        "failure_codes": sorted(set(failures + [
            "HOST_INVOCATION_HOOK_NOT_PROVEN",
            "HOST_REMOTE_CURRENTNESS_UNVERIFIED",
        ])),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only local Goal integrity diagnostic, never an execution permit."
    )
    parser.add_argument("--control-root", type=Path, required=True)
    args = parser.parse_args()
    result = assess(args.control_root)
    print(json.dumps(result, indent=2))
    return 2 if not result["may_execute_material_goal"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
