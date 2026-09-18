#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from baseline_guard import evaluate_baseline

from state_tx import (
    StateTransactionError,
    atomic_json,
    journal_path,
    recover as recover_pending_transaction,
    state_lock as campaign_lock,
    write_json_set as transaction_write_json,
)

TERMINAL_WORK_STATUSES = {"DONE", "PARKED", "SUPERSEDED", "CANCELLED"}
READINESS_TERMINALS = {
    "CAPABILITY_READY_FOR_PLANNER_ACCEPTANCE",
    "QUALITY_GATE_READY_FOR_PLANNER_OR_HUMAN_DECISION",
}
TERMINAL_TYPES = [
    "CAPABILITY_READY_FOR_PLANNER_ACCEPTANCE",
    "QUALITY_GATE_READY_FOR_PLANNER_OR_HUMAN_DECISION",
    "REPLAN_REQUIRED__CHARTER_INVALIDATED",
    "BLOCKED_EXTERNAL_OR_AUTHORITY",
    "CAPACITY_CHECKPOINT__RESUMABLE",
    "NO_FUNCTIONAL_UNLOCK__CAMPAIGN_EXHAUSTED",
]


class CampaignError(Exception):
    pass


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise CampaignError(f"missing required file: {path}")
    except Exception as exc:
        raise CampaignError(f"invalid JSON at {path}: {exc}")
    if not isinstance(data, dict):
        raise CampaignError(f"expected JSON object at {path}")
    return data


def require_no_pending_transaction(control: Path) -> None:
    if journal_path(control).exists():
        journal = load_json(journal_path(control))
        raise CampaignError(
            f"pending transition journal {journal.get('transaction_id')}; "
            "run campaignctl recover before read-only inspection"
        )


def control_root(args: argparse.Namespace) -> Path:
    return Path(args.control_root).resolve()


def runtime_path(control: Path) -> Path:
    return control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json"


def product_state_path(control: Path) -> Path:
    return control / "state" / "PRODUCT_STATE_CURRENT.json"


def bootstrap_path(control: Path) -> Path:
    return control / "state" / "CURRENT_BOOTSTRAP_STATE.json"


def authority_path(control: Path) -> Path:
    return control / "state" / "EXECUTION_AUTHORITY_CURRENT.json"


def identity_path(control: Path) -> Path:
    return control / "state" / "IDENTITY_REGISTRY_CURRENT.json"


def resolve(control: Path, value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    inside = control / candidate
    if inside.exists():
        return inside
    return candidate.resolve()


def relative_to_control(control: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(control.resolve()))
    except ValueError:
        return str(path.resolve())


def load_runtime(control: Path) -> dict[str, Any]:
    return load_json(runtime_path(control))


def save_runtime(control: Path, state: dict[str, Any]) -> None:
    atomic_json(runtime_path(control), state)


def work_map(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for unit in state["work_units"]:
        if unit["id"] in result:
            raise CampaignError(f"duplicate work unit id in runtime: {unit['id']}")
        result[unit["id"]] = unit
    return result


def find_unit(state: dict[str, Any], unit_id: str) -> dict[str, Any]:
    unit = work_map(state).get(unit_id)
    if unit is None:
        raise CampaignError(f"unknown work unit: {unit_id}")
    return unit


def event(
    state: dict[str, Any],
    action: str,
    *,
    work_unit_id: str | None = None,
    actor_id: str | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    state["revision"] += 1
    state["updated_at"] = now()
    seq = max((item["seq"] for item in state["event_log"]), default=0) + 1
    state["event_log"].append(
        {
            "seq": seq,
            "at": state["updated_at"],
            "action": action,
            "work_unit_id": work_unit_id,
            "actor_id": actor_id,
            "details": details or {},
        }
    )


def invalidate_freeze(state: dict[str, Any], reason: str) -> None:
    freeze = state.get("review_freeze")
    if not freeze or freeze["status"] == "INVALIDATED":
        return
    freeze["status"] = "INVALIDATED"
    freeze["invalidated_at"] = now()
    freeze["invalidation_reason"] = reason
    freeze["reviewer_actor_id"] = None
    freeze["reviewer_run_id"] = None
    freeze["verdict"] = None
    freeze["evidence_refs"] = []
    event(state, "REVIEW_FREEZE_INVALIDATED", details={"reason": reason})


def dependencies_done(state: dict[str, Any], unit: dict[str, Any]) -> bool:
    units = work_map(state)
    for dep in unit["dependencies"]:
        if dep not in units:
            raise CampaignError(f"{unit['id']}: dependency does not exist: {dep}")
        if units[dep]["status"] != "DONE":
            return False
    return True


def recompute_ready(state: dict[str, Any]) -> None:
    changed = True
    while changed:
        changed = False
        for unit in state["work_units"]:
            if unit["status"] == "BLOCKED_DEPENDENCY" and dependencies_done(state, unit):
                unit["status"] = "READY"
                changed = True


def assert_acyclic(state: dict[str, Any]) -> None:
    units = work_map(state)
    visiting: set[str] = set()
    visited: set[str] = set()

    def dfs(unit_id: str) -> None:
        if unit_id in visiting:
            raise CampaignError(f"dependency cycle detected at {unit_id}")
        if unit_id in visited:
            return
        visiting.add(unit_id)
        for dep in units[unit_id]["dependencies"]:
            if dep not in units:
                raise CampaignError(f"{unit_id}: dependency does not exist: {dep}")
            dfs(dep)
        visiting.remove(unit_id)
        visited.add(unit_id)

    for unit_id in units:
        dfs(unit_id)


def pathish_conflict(a: str, b: str) -> bool:
    aa = a.strip().rstrip("/")
    bb = b.strip().rstrip("/")
    if aa == bb:
        return True
    if "/" in aa or "/" in bb:
        return aa.startswith(bb + "/") or bb.startswith(aa + "/")
    return False


def assert_no_active_conflict(state: dict[str, Any], candidate: dict[str, Any]) -> None:
    for unit in state["work_units"]:
        if unit["id"] == candidate["id"] or unit["status"] != "ACTIVE":
            continue
        shared = set(unit["shared_resources"]) & set(candidate["shared_resources"])
        if shared:
            raise CampaignError(
                f"{candidate['id']}: shared-resource conflict with {unit['id']}: {sorted(shared)}"
            )
        for left in unit["allowed_write_surfaces"]:
            for right in candidate["allowed_write_surfaces"]:
                if pathish_conflict(left, right):
                    raise CampaignError(
                        f"{candidate['id']}: write-surface conflict with {unit['id']}: "
                        f"{right!r} vs {left!r}"
                    )


def require_campaign_active(state: dict[str, Any]) -> None:
    if state["campaign_status"] != "ACTIVE":
        raise CampaignError(f"campaign is not ACTIVE: {state['campaign_status']}")


def require_authority_if_present(control: Path, state: dict[str, Any]) -> None:
    path = authority_path(control)
    if not path.exists():
        return
    authority = load_json(path)
    if authority.get("authority_status") != "ACTIVE":
        raise CampaignError(
            f"execution authority exists but is not ACTIVE: {authority.get('authority_status')}"
        )
    if authority.get("campaign_id") != state["campaign_id"]:
        raise CampaignError(
            f"execution authority campaign {authority.get('campaign_id')!r} "
            f"!= runtime campaign {state['campaign_id']!r}"
        )


def read_charter(control: Path, state: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    path = resolve(control, state["charter_ref"])
    charter = load_json(path)
    if charter.get("schema_version") != "campaign-charter-0.1":
        raise CampaignError(f"unsupported charter schema at {path}")
    if charter.get("campaign_id") != state["campaign_id"]:
        raise CampaignError("runtime campaign_id does not match charter")
    return path, charter


def update_product_and_bootstrap_checkpoint(
    control: Path,
    state: dict[str, Any],
    checkpoint_id: str,
) -> None:
    ps_path = product_state_path(control)
    if not ps_path.exists():
        return
    ps = load_json(ps_path)
    active = ps.get("active_campaign")
    if not active or active.get("campaign_id") != state["campaign_id"]:
        raise CampaignError("Product State active campaign does not match runtime campaign")
    ps["current_code_ref"] = state["integrated_ref"]
    active["checkpoint_or_terminal_ref"] = checkpoint_id
    canonical_checkpoint_ref = (
        f"campaigns/{state['campaign_id']}/CHECKPOINT_CURRENT.json"
    )
    if canonical_checkpoint_ref not in ps.get("currentness_set", []):
        ps.setdefault("currentness_set", []).append(canonical_checkpoint_ref)
    ps["updated_at"] = now()
    atomic_json(ps_path, ps)

    bs_path = bootstrap_path(control)
    if bs_path.exists():
        bs = load_json(bs_path)
        bs["observed_code_ref"] = state["integrated_ref"]
        bs["observed_at"] = now()
        bs["active_campaign_ref"] = state["campaign_id"]
        bs["active_checkpoint_or_terminal_ref"] = checkpoint_id
        bs["current_gate"] = ps.get("current_gate", bs.get("current_gate", ""))
        bs["next_legal_boundary"] = ps.get(
            "next_legal_boundary", bs.get("next_legal_boundary", "")
        )
        atomic_json(bs_path, bs)


def require_project_baseline_if_present(control: Path) -> None:
    refs = [
        control / "state" / "CLIENT_REQUIREMENTS_CURRENT.md",
        control / "state" / "TECHNICAL_BASELINE_CURRENT.json",
        control / "state" / "DELIVERY_PLAN_CURRENT.json",
    ]
    if not any(path.exists() for path in refs[1:]):
        return
    report = evaluate_baseline(control)
    if not report.get("ready"):
        detail = "; ".join(report.get("errors", []))
        raise CampaignError(f"PROJECT_BASELINE_NOT_READY: {detail}")


def cmd_init(args: argparse.Namespace) -> None:
    control = control_root(args)
    require_project_baseline_if_present(control)
    rt_path = runtime_path(control)
    if rt_path.exists() and not args.force:
        raise CampaignError(f"runtime already exists: {rt_path}")

    charter_path = resolve(control, args.charter)
    charter = load_json(charter_path)
    if charter.get("schema_version") != "campaign-charter-0.1":
        raise CampaignError("init requires campaign-charter-0.1")

    ps_path = product_state_path(control)
    ps = load_json(ps_path)
    if ps.get("product_or_workstream") != charter.get("product_or_workstream"):
        raise CampaignError("Product State and charter product/workstream differ")
    capability_ids = {item["id"] for item in ps.get("capabilities", [])}
    if charter["capability"] not in capability_ids:
        raise CampaignError("charter capability is not present in Product State")

    active = ps.get("active_campaign")
    if active is None:
        if not args.activate_product_state:
            raise CampaignError(
                "Product State has no active campaign; use --activate-product-state "
                "only after Planner has authorized this charter"
            )
        ps["active_campaign"] = {
            "campaign_id": charter["campaign_id"],
            "charter_ref": relative_to_control(control, charter_path),
            "checkpoint_or_terminal_ref": None,
        }
        for capability in ps["capabilities"]:
            if capability["id"] == charter["capability"]:
                capability["physical_state"] = "ACTIVE_CAMPAIGN"
    elif active.get("campaign_id") != charter["campaign_id"]:
        raise CampaignError(
            f"Product State already has different active campaign: {active.get('campaign_id')}"
        )

    integrated_ref = args.integrated_ref or ps["current_code_ref"]
    state = {
        "schema_version": "campaign-runtime-0.1",
        "campaign_id": charter["campaign_id"],
        "product_or_workstream": charter["product_or_workstream"],
        "charter_ref": relative_to_control(control, charter_path),
        "campaign_status": "ACTIVE",
        "revision": 0,
        "updated_at": now(),
        "integrated_ref": integrated_ref,
        "current_checkpoint_id": None,
        "checkpoint_counter": 0,
        "review_freeze_counter": 0,
        "review_freeze": None,
        "terminal_request": None,
        "campaign_falsifiers": [],
        "work_units": [],
        "event_log": [],
    }
    event(
        state,
        "CAMPAIGN_RUNTIME_INITIALIZED",
        details={"integrated_ref": integrated_ref},
    )

    runtime_ref = "runtime/CAMPAIGN_RUNTIME_CURRENT.json"
    if runtime_ref not in ps.get("currentness_set", []):
        ps.setdefault("currentness_set", []).append(runtime_ref)
    if authority_path(control).exists():
        authority_ref = "state/EXECUTION_AUTHORITY_CURRENT.json"
        if authority_ref not in ps["currentness_set"]:
            ps["currentness_set"].append(authority_ref)
    if identity_path(control).exists():
        identity_ref = "state/IDENTITY_REGISTRY_CURRENT.json"
        if identity_ref not in ps["currentness_set"]:
            ps["currentness_set"].append(identity_ref)
    ps["updated_at"] = now()

    writes: list[tuple[Path, dict[str, Any]]] = [
        (rt_path, state),
        (ps_path, ps),
    ]

    bs_path = bootstrap_path(control)
    if bs_path.exists():
        bs = load_json(bs_path)
        bs["observed_code_ref"] = integrated_ref
        bs["observed_at"] = now()
        bs["active_campaign_ref"] = state["campaign_id"]
        bs["active_checkpoint_or_terminal_ref"] = None
        bs["next_legal_boundary"] = (
            "Continue the same campaign through the durable campaign runtime."
        )
        writes.append((bs_path, bs))

    transaction_write_json(control, "CAMPAIGN_INIT", writes)
    print(f"INITIALIZED {state['campaign_id']} at {rt_path}")

def cmd_add(args: argparse.Namespace) -> None:
    control = control_root(args)
    state = load_runtime(control)
    require_campaign_active(state)
    require_authority_if_present(control, state)
    invalidate_freeze(state, "tactical work graph changed after review freeze")

    if args.id in work_map(state):
        raise CampaignError(f"work unit already exists: {args.id}")

    unit = {
        "id": args.id,
        "title": args.title,
        "status": "BLOCKED_DEPENDENCY",
        "priority": args.priority,
        "dependencies": args.depends or [],
        "allowed_write_surfaces": args.write or [],
        "shared_resources": args.resource or [],
        "actor_id": None,
        "run_id": None,
        "evidence_refs": [],
        "result_ref": None,
        "notes": [],
    }
    state["work_units"].append(unit)
    assert_acyclic(state)
    if dependencies_done(state, unit):
        unit["status"] = "READY"
    event(state, "WORK_UNIT_ADDED", work_unit_id=args.id, details={"title": args.title})
    save_runtime(control, state)
    print(f"ADDED {args.id} status={unit['status']}")


def cmd_reprioritize(args: argparse.Namespace) -> None:
    control = control_root(args)
    state = load_runtime(control)
    require_campaign_active(state)
    require_authority_if_present(control, state)
    invalidate_freeze(state, "tactical priority changed after review freeze")
    unit = find_unit(state, args.id)
    old = unit["priority"]
    unit["priority"] = args.priority
    event(
        state,
        "WORK_UNIT_REPRIORITIZED",
        work_unit_id=args.id,
        details={"from": old, "to": args.priority},
    )
    save_runtime(control, state)
    print(f"REPRIORITIZED {args.id} {old}->{args.priority}")


def cmd_start(args: argparse.Namespace) -> None:
    control = control_root(args)
    state = load_runtime(control)
    require_campaign_active(state)
    require_authority_if_present(control, state)
    invalidate_freeze(state, "producer work resumed after review freeze")
    unit = find_unit(state, args.id)
    if unit["status"] != "READY":
        raise CampaignError(f"{args.id}: expected READY, found {unit['status']}")
    if not dependencies_done(state, unit):
        raise CampaignError(f"{args.id}: dependencies are not DONE")
    assert_no_active_conflict(state, unit)
    unit["status"] = "ACTIVE"
    unit["actor_id"] = args.actor
    unit["run_id"] = args.run
    event(
        state,
        "WORK_UNIT_STARTED",
        work_unit_id=args.id,
        actor_id=args.actor,
        details={"run_id": args.run},
    )
    save_runtime(control, state)
    print(f"STARTED {args.id}")


def cmd_verify(args: argparse.Namespace) -> None:
    control = control_root(args)
    state = load_runtime(control)
    require_campaign_active(state)
    require_authority_if_present(control, state)
    invalidate_freeze(state, "producer verification changed after review freeze")
    unit = find_unit(state, args.id)
    if unit["status"] != "ACTIVE":
        raise CampaignError(f"{args.id}: expected ACTIVE, found {unit['status']}")
    unit["status"] = "VERIFY"
    unit["evidence_refs"].extend(args.evidence or [])
    event(
        state,
        "WORK_UNIT_VERIFY",
        work_unit_id=args.id,
        actor_id=unit["actor_id"],
        details={"evidence": args.evidence or []},
    )
    save_runtime(control, state)
    print(f"VERIFY {args.id}")


def cmd_done(args: argparse.Namespace) -> None:
    control = control_root(args)
    state = load_runtime(control)
    require_campaign_active(state)
    require_authority_if_present(control, state)
    invalidate_freeze(state, "producer completion changed after review freeze")
    unit = find_unit(state, args.id)
    if unit["status"] != "VERIFY":
        raise CampaignError(f"{args.id}: expected VERIFY, found {unit['status']}")
    unit["status"] = "DONE"
    unit["result_ref"] = args.result_ref
    unit["evidence_refs"].extend(args.evidence or [])
    event(
        state,
        "WORK_UNIT_DONE",
        work_unit_id=args.id,
        actor_id=unit["actor_id"],
        details={"result_ref": args.result_ref, "evidence": args.evidence or []},
    )
    recompute_ready(state)
    save_runtime(control, state)
    print(f"DONE {args.id}")


def cmd_fail(args: argparse.Namespace) -> None:
    control = control_root(args)
    state = load_runtime(control)
    require_campaign_active(state)
    require_authority_if_present(control, state)
    invalidate_freeze(state, "producer failure changed after review freeze")
    unit = find_unit(state, args.id)
    if unit["status"] not in {"ACTIVE", "VERIFY"}:
        raise CampaignError(f"{args.id}: cannot fail from {unit['status']}")
    unit["status"] = "FAILED"
    unit["notes"].append(args.note)
    event(
        state,
        "WORK_UNIT_FAILED",
        work_unit_id=args.id,
        actor_id=unit["actor_id"],
        details={"note": args.note},
    )
    save_runtime(control, state)
    print(f"FAILED {args.id}")


def cmd_retry(args: argparse.Namespace) -> None:
    control = control_root(args)
    state = load_runtime(control)
    require_campaign_active(state)
    require_authority_if_present(control, state)
    invalidate_freeze(state, "retry opened after review freeze")
    unit = find_unit(state, args.id)
    if unit["status"] != "FAILED":
        raise CampaignError(f"{args.id}: expected FAILED, found {unit['status']}")
    unit["status"] = "READY" if dependencies_done(state, unit) else "BLOCKED_DEPENDENCY"
    unit["actor_id"] = None
    unit["run_id"] = None
    unit["result_ref"] = None
    event(state, "WORK_UNIT_RETRY", work_unit_id=args.id)
    save_runtime(control, state)
    print(f"RETRY {args.id} status={unit['status']}")


def transition_terminal_work(args: argparse.Namespace, status: str, action: str) -> None:
    control = control_root(args)
    state = load_runtime(control)
    require_campaign_active(state)
    require_authority_if_present(control, state)
    invalidate_freeze(state, f"work-unit {status.lower()} after review freeze")
    unit = find_unit(state, args.id)
    if unit["status"] in {"ACTIVE", "VERIFY", "DONE"}:
        raise CampaignError(f"{args.id}: cannot {status.lower()} from {unit['status']}")
    unit["status"] = status
    if args.note:
        unit["notes"].append(args.note)
    event(state, action, work_unit_id=args.id, details={"note": args.note})
    recompute_ready(state)
    save_runtime(control, state)
    print(f"{status} {args.id}")


def cmd_checkpoint(args: argparse.Namespace) -> None:
    control = control_root(args)
    state = load_runtime(control)
    require_authority_if_present(control, state)
    if state["campaign_status"] not in {"ACTIVE", "HOLD", "CAPACITY_CHECKPOINT"}:
        raise CampaignError(f"cannot checkpoint from {state['campaign_status']}")

    if args.integrated_ref and args.integrated_ref != state["integrated_ref"]:
        invalidate_freeze(state, "integrated candidate changed after review freeze")
        state["integrated_ref"] = args.integrated_ref

    state["checkpoint_counter"] += 1
    checkpoint_id = f"CHECKPOINT_{state['checkpoint_counter']:04d}"
    state["current_checkpoint_id"] = checkpoint_id

    units = state["work_units"]
    evidence = sorted({ref for unit in units for ref in unit["evidence_refs"]})
    active_locks: list[str] = []
    for unit in units:
        if unit["status"] == "ACTIVE":
            active_locks.extend(f"write:{x}" for x in unit["allowed_write_surfaces"])
            active_locks.extend(f"resource:{x}" for x in unit["shared_resources"])

    checkpoint = {
        "schema_version": "campaign-checkpoint-0.1",
        "campaign_id": state["campaign_id"],
        "checkpoint_id": checkpoint_id,
        "exact_integrated_ref": state["integrated_ref"],
        "charter_status": "VALID",
        "created_at": now(),
        "completed_capability_delta": args.summary or "",
        "tactical_dag": {
            "done": [u["id"] for u in units if u["status"] == "DONE"],
            "active": [u["id"] for u in units if u["status"] in {"ACTIVE", "VERIFY"}],
            "ready": [u["id"] for u in units if u["status"] == "READY"],
            "blocked": [
                u["id"]
                for u in units
                if u["status"] in {"BLOCKED_DEPENDENCY", "FAILED", "PARKED"}
            ],
        },
        "evidence_refs": evidence,
        "rejected_approaches": [
            u["id"] for u in units if u["status"] in {"SUPERSEDED", "CANCELLED"}
        ],
        "resource_locks": sorted(set(active_locks)),
        "current_falsifiers": list(state["campaign_falsifiers"]),
        "resume_procedure": (
            "Reconstruct Product State, charter, execution authority and this checkpoint; "
            "then continue READY work in the same campaign if the charter remains valid."
        ),
        "strategic_return_required": False,
    }

    cp_path = control / "campaigns" / state["campaign_id"] / "CHECKPOINT_CURRENT.json"
    event(
        state,
        "CHECKPOINT_WRITTEN",
        details={
            "checkpoint_id": checkpoint_id,
            "integrated_ref": state["integrated_ref"],
            "path": relative_to_control(control, cp_path),
        },
    )

    ps_path = product_state_path(control)
    ps = load_json(ps_path)
    active = ps.get("active_campaign")
    if not active or active.get("campaign_id") != state["campaign_id"]:
        raise CampaignError("Product State active campaign does not match runtime campaign")
    ps["current_code_ref"] = state["integrated_ref"]
    active["checkpoint_or_terminal_ref"] = checkpoint_id
    canonical_checkpoint_ref = f"campaigns/{state['campaign_id']}/CHECKPOINT_CURRENT.json"
    if canonical_checkpoint_ref not in ps.get("currentness_set", []):
        ps.setdefault("currentness_set", []).append(canonical_checkpoint_ref)
    ps["updated_at"] = now()

    writes: list[tuple[Path, dict[str, Any]]] = [
        (cp_path, checkpoint),
        (runtime_path(control), state),
        (ps_path, ps),
    ]

    bs_path = bootstrap_path(control)
    if bs_path.exists():
        bs = load_json(bs_path)
        bs["observed_code_ref"] = state["integrated_ref"]
        bs["observed_at"] = now()
        bs["active_campaign_ref"] = state["campaign_id"]
        bs["active_checkpoint_or_terminal_ref"] = checkpoint_id
        bs["current_gate"] = ps.get("current_gate", bs.get("current_gate", ""))
        bs["next_legal_boundary"] = ps.get(
            "next_legal_boundary", bs.get("next_legal_boundary", "")
        )
        writes.append((bs_path, bs))

    auth_path = authority_path(control)
    if auth_path.exists():
        authority = load_json(auth_path)
        if (
            authority.get("authority_status") == "ACTIVE"
            and authority.get("campaign_id") == state["campaign_id"]
        ):
            authority["checkpoint_ref"] = checkpoint_id
            authority["updated_at"] = now()
            writes.append((auth_path, authority))

    transaction_write_json(control, "CAMPAIGN_CHECKPOINT", writes)
    print(f"CHECKPOINT {checkpoint_id} ref={state['integrated_ref']}")

def set_campaign_status(
    args: argparse.Namespace,
    status: str,
    action: str,
) -> None:
    control = control_root(args)
    state = load_runtime(control)
    require_authority_if_present(control, state)
    if status == "ACTIVE":
        if state["campaign_status"] not in {"HOLD", "CAPACITY_CHECKPOINT"}:
            raise CampaignError(f"cannot resume from {state['campaign_status']}")
    else:
        if state["campaign_status"] != "ACTIVE":
            raise CampaignError(f"cannot enter {status} from {state['campaign_status']}")
    state["campaign_status"] = status
    event(state, action, details={"reason": getattr(args, "reason", None)})
    save_runtime(control, state)
    print(f"CAMPAIGN {status}")


def cmd_freeze(args: argparse.Namespace) -> None:
    control = control_root(args)
    state = load_runtime(control)
    require_campaign_active(state)
    require_authority_if_present(control, state)
    nonterminal = [
        u["id"] for u in state["work_units"] if u["status"] not in TERMINAL_WORK_STATUSES
    ]
    if nonterminal:
        raise CampaignError(
            f"cannot freeze review while nonterminal work remains: {sorted(nonterminal)}"
        )
    if args.candidate_ref != state["integrated_ref"]:
        raise CampaignError(
            f"freeze candidate {args.candidate_ref!r} != integrated_ref {state['integrated_ref']!r}"
        )
    state["review_freeze_counter"] += 1
    state["review_freeze"] = {
        "freeze_id": f"FREEZE_{state['review_freeze_counter']:04d}",
        "candidate_ref": args.candidate_ref,
        "status": "FROZEN",
        "created_at": now(),
        "invalidated_at": None,
        "invalidation_reason": None,
        "reviewer_actor_id": None,
        "reviewer_run_id": None,
        "verdict": None,
        "evidence_refs": [],
    }
    event(
        state,
        "REVIEW_FREEZE_CREATED",
        details={
            "freeze_id": state["review_freeze"]["freeze_id"],
            "candidate_ref": args.candidate_ref,
        },
    )
    save_runtime(control, state)
    print(f"FROZEN {state['review_freeze']['freeze_id']} candidate={args.candidate_ref}")


def cmd_review(args: argparse.Namespace) -> None:
    control = control_root(args)
    state = load_runtime(control)
    freeze = state.get("review_freeze")
    if not freeze or freeze["status"] != "FROZEN":
        raise CampaignError("independent review requires an active FROZEN review freeze")

    producer_actors = {
        unit["actor_id"]
        for unit in state["work_units"]
        if unit["actor_id"] and unit["status"] == "DONE"
    }
    if args.reviewer in producer_actors:
        raise CampaignError(
            f"reviewer {args.reviewer!r} produced work in this candidate and is not independent"
        )

    id_path = identity_path(control)
    if id_path.exists():
        registry = load_json(id_path)
        actors = {item["actor_id"]: item for item in registry.get("actors", [])}
        actor = actors.get(args.reviewer)
        if actor is None:
            raise CampaignError(f"reviewer actor not found in identity registry: {args.reviewer}")
        if actor.get("status") != "ACTIVE":
            raise CampaignError(f"reviewer actor is not ACTIVE: {args.reviewer}")
        if actor.get("current_run_id") not in {None, args.run}:
            raise CampaignError(
                f"reviewer run {args.run!r} != registry current_run_id "
                f"{actor.get('current_run_id')!r}"
            )

    freeze["status"] = "REVIEWED"
    freeze["reviewer_actor_id"] = args.reviewer
    freeze["reviewer_run_id"] = args.run
    freeze["verdict"] = args.verdict
    freeze["evidence_refs"] = args.evidence or []
    event(
        state,
        "INDEPENDENT_REVIEW_RECORDED",
        actor_id=args.reviewer,
        details={"run_id": args.run, "verdict": args.verdict},
    )
    save_runtime(control, state)
    print(f"REVIEWED {freeze['freeze_id']} verdict={args.verdict}")


def cmd_terminal(args: argparse.Namespace) -> None:
    control = control_root(args)
    state = load_runtime(control)
    if state["campaign_status"] == "STRATEGIC_TERMINAL":
        raise CampaignError("campaign already has a strategic terminal request")

    if args.type in READINESS_TERMINALS:
        freeze = state.get("review_freeze")
        if not freeze or freeze["status"] != "REVIEWED":
            raise CampaignError("readiness terminal requires REVIEWED exact-candidate freeze")
        if freeze["candidate_ref"] != state["integrated_ref"]:
            raise CampaignError("reviewed candidate is not current integrated_ref")
        unfinished = [
            u["id"] for u in state["work_units"] if u["status"] not in TERMINAL_WORK_STATUSES
        ]
        if unfinished:
            raise CampaignError(
                f"readiness terminal cannot leave nonterminal work: {sorted(unfinished)}"
            )

    state["campaign_status"] = "STRATEGIC_TERMINAL"
    state["terminal_request"] = {
        "terminal_type": args.type,
        "reason": args.reason,
        "created_at": now(),
    }
    event(
        state,
        "STRATEGIC_TERMINAL_REQUESTED",
        details={"terminal_type": args.type, "reason": args.reason},
    )

    writes: list[tuple[Path, dict[str, Any]]] = [
        (runtime_path(control), state),
    ]
    bs_path = bootstrap_path(control)
    if bs_path.exists():
        bs = load_json(bs_path)
        bs["next_legal_boundary"] = (
            f"Strategic terminal requested: {args.type}. Return to Planner/authority owner."
        )
        bs["observed_at"] = now()
        writes.append((bs_path, bs))

    transaction_write_json(control, "STRATEGIC_TERMINAL", writes)
    print(f"STRATEGIC_TERMINAL {args.type}")

def cmd_authority_acquire(args: argparse.Namespace) -> None:
    control = control_root(args)
    state = load_runtime(control)
    _, charter = read_charter(control, state)
    registry = load_json(identity_path(control))
    actors = {item["actor_id"]: item for item in registry.get("actors", [])}
    actor = actors.get(args.actor)
    if actor is None:
        raise CampaignError(f"actor not found: {args.actor}")
    if actor.get("role_class") != "I3_ENGINEERING_CAMPAIGN_LEAD":
        raise CampaignError("execution authority requires I3_ENGINEERING_CAMPAIGN_LEAD")
    if actor.get("status") != "ACTIVE":
        raise CampaignError("campaign lead actor is not ACTIVE")
    if actor.get("current_run_id") != args.run:
        raise CampaignError(
            f"actor current_run_id {actor.get('current_run_id')!r} != {args.run!r}"
        )

    path = authority_path(control)
    if path.exists():
        existing = load_json(path)
        if existing.get("authority_status") == "ACTIVE":
            if (
                existing.get("campaign_id") == state["campaign_id"]
                and existing.get("campaign_lead_actor_id") == args.actor
                and existing.get("current_run_id") == args.run
            ):
                print("AUTHORITY ALREADY ACTIVE")
                return
            raise CampaignError("another ACTIVE execution authority already exists")

    envelope = charter.get("resource_envelope", {})
    authority = {
        "schema_version": "execution-authority-0.1",
        "updated_at": now(),
        "authority_status": "ACTIVE",
        "campaign_id": state["campaign_id"],
        "campaign_lead_actor_id": args.actor,
        "current_run_id": args.run,
        "baseline_ref": charter["baseline_ref"],
        "checkpoint_ref": state.get("current_checkpoint_id"),
        "allowed_write_surfaces": list(envelope.get("allowed_write_surfaces", [])),
        "protected_surfaces": list(envelope.get("protected_surfaces", [])),
        "expires_at": None,
    }
    event(
        state,
        "EXECUTION_AUTHORITY_ACQUIRED",
        actor_id=args.actor,
        details={"run_id": args.run},
    )
    transaction_write_json(
        control,
        "EXECUTION_AUTHORITY_ACQUIRE",
        [(path, authority), (runtime_path(control), state)],
    )
    print(f"AUTHORITY ACTIVE actor={args.actor} run={args.run}")

def cmd_authority_release(args: argparse.Namespace) -> None:
    control = control_root(args)
    state = load_runtime(control)
    path = authority_path(control)
    authority = load_json(path)
    if authority.get("authority_status") != "ACTIVE":
        raise CampaignError("execution authority is not ACTIVE")
    if authority.get("campaign_id") != state["campaign_id"]:
        raise CampaignError("authority campaign does not match runtime")
    if authority.get("campaign_lead_actor_id") != args.actor:
        raise CampaignError("actor does not own current authority")
    if authority.get("current_run_id") != args.run:
        raise CampaignError("run does not own current authority")

    authority["authority_status"] = "SUPERSEDED"
    authority["updated_at"] = now()
    authority["expires_at"] = authority["updated_at"]
    event(
        state,
        "EXECUTION_AUTHORITY_RELEASED",
        actor_id=args.actor,
        details={"run_id": args.run},
    )
    transaction_write_json(
        control,
        "EXECUTION_AUTHORITY_RELEASE",
        [(path, authority), (runtime_path(control), state)],
    )
    print("AUTHORITY SUPERSEDED")


def cmd_recover(args: argparse.Namespace) -> None:
    control = control_root(args)
    txid = recover_pending_transaction(control)
    if txid is None:
        print("NO PENDING TRANSACTION")
    else:
        print(f"RECOVERED {txid}")

def cmd_next(args: argparse.Namespace) -> None:
    control = control_root(args)
    require_no_pending_transaction(control)
    state = load_runtime(control)
    recompute_ready(state)
    ready = sorted(
        (u for u in state["work_units"] if u["status"] == "READY"),
        key=lambda u: (-u["priority"], u["id"]),
    )
    print(
        json.dumps(
            [
                {
                    "id": u["id"],
                    "title": u["title"],
                    "priority": u["priority"],
                    "writes": u["allowed_write_surfaces"],
                    "resources": u["shared_resources"],
                }
                for u in ready
            ],
            indent=2,
        )
    )


def cmd_show(args: argparse.Namespace) -> None:
    control = control_root(args)
    require_no_pending_transaction(control)
    print(json.dumps(load_runtime(control), indent=2))


def add_common_parser_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--control-root",
        default=".agentic-sdlc",
        help="Project-local Agentic SDLC control root.",
    )
    parser.add_argument(
        "--lock-timeout",
        type=float,
        default=10.0,
        help="Seconds to wait for the exclusive campaign mutation lock.",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Minimal durable Campaign Lead runtime/controller."
    )
    add_common_parser_options(parser)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init")
    p.add_argument("--charter", required=True)
    p.add_argument("--integrated-ref")
    p.add_argument("--activate-product-state", action="store_true")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("add")
    p.add_argument("--id", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--priority", type=int, default=0)
    p.add_argument("--depends", action="append")
    p.add_argument("--write", action="append")
    p.add_argument("--resource", action="append")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("reprioritize")
    p.add_argument("--id", required=True)
    p.add_argument("--priority", type=int, required=True)
    p.set_defaults(func=cmd_reprioritize)

    p = sub.add_parser("start")
    p.add_argument("--id", required=True)
    p.add_argument("--actor", required=True)
    p.add_argument("--run", required=True)
    p.set_defaults(func=cmd_start)

    p = sub.add_parser("verify")
    p.add_argument("--id", required=True)
    p.add_argument("--evidence", action="append")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("done")
    p.add_argument("--id", required=True)
    p.add_argument("--result-ref", required=True)
    p.add_argument("--evidence", action="append")
    p.set_defaults(func=cmd_done)

    p = sub.add_parser("fail")
    p.add_argument("--id", required=True)
    p.add_argument("--note", required=True)
    p.set_defaults(func=cmd_fail)

    p = sub.add_parser("retry")
    p.add_argument("--id", required=True)
    p.set_defaults(func=cmd_retry)

    for name, status, action in [
        ("park", "PARKED", "WORK_UNIT_PARKED"),
        ("cancel", "CANCELLED", "WORK_UNIT_CANCELLED"),
        ("supersede", "SUPERSEDED", "WORK_UNIT_SUPERSEDED"),
    ]:
        p = sub.add_parser(name)
        p.add_argument("--id", required=True)
        p.add_argument("--note", default="")
        p.set_defaults(
            func=lambda args, s=status, a=action: transition_terminal_work(args, s, a)
        )

    p = sub.add_parser("checkpoint")
    p.add_argument("--integrated-ref")
    p.add_argument("--summary", default="")
    p.set_defaults(func=cmd_checkpoint)

    p = sub.add_parser("hold")
    p.add_argument("--reason", required=True)
    p.set_defaults(
        func=lambda args: set_campaign_status(args, "HOLD", "CAMPAIGN_HOLD")
    )

    p = sub.add_parser("capacity")
    p.add_argument("--reason", required=True)
    p.set_defaults(
        func=lambda args: set_campaign_status(
            args, "CAPACITY_CHECKPOINT", "CAMPAIGN_CAPACITY_CHECKPOINT"
        )
    )

    p = sub.add_parser("resume")
    p.set_defaults(
        func=lambda args: set_campaign_status(args, "ACTIVE", "CAMPAIGN_RESUMED")
    )

    p = sub.add_parser("freeze")
    p.add_argument("--candidate-ref", required=True)
    p.set_defaults(func=cmd_freeze)

    p = sub.add_parser("review")
    p.add_argument("--reviewer", required=True)
    p.add_argument("--run", required=True)
    p.add_argument("--verdict", required=True)
    p.add_argument("--evidence", action="append")
    p.set_defaults(func=cmd_review)

    p = sub.add_parser("terminal")
    p.add_argument("--type", choices=TERMINAL_TYPES, required=True)
    p.add_argument("--reason", required=True)
    p.set_defaults(func=cmd_terminal)

    p = sub.add_parser("authority-acquire")
    p.add_argument("--actor", required=True)
    p.add_argument("--run", required=True)
    p.set_defaults(func=cmd_authority_acquire)

    p = sub.add_parser("authority-release")
    p.add_argument("--actor", required=True)
    p.add_argument("--run", required=True)
    p.set_defaults(func=cmd_authority_release)

    p = sub.add_parser("recover")
    p.set_defaults(func=cmd_recover)

    p = sub.add_parser("next")
    p.set_defaults(func=cmd_next)

    p = sub.add_parser("show")
    p.set_defaults(func=cmd_show)

    args = parser.parse_args()
    try:
        if args.command in {"next", "show"}:
            args.func(args)
        else:
            control = control_root(args)
            with campaign_lock(control, args.lock_timeout):
                if args.command != "recover" and journal_path(control).exists():
                    raise CampaignError(
                        "pending transition exists; run campaignctl recover before another mutation"
                    )
                args.func(args)
    except (CampaignError, StateTransactionError) as exc:
        print(f"CAMPAIGNCTL FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
