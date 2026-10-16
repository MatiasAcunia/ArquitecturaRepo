#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from baseline_guard import evaluate_baseline

from state_tx import (
    StateTransactionError,
    atomic_json,
    journal_path,
    recover as recover_pending_transaction,
    sha256_file,
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
        return path.resolve().relative_to(control.resolve()).as_posix()
    except ValueError as exc:
        raise CampaignError("canonical campaign reference must be inside the control root") from exc


def evidence_file(control: Path, value: str) -> Path:
    reference = Path(value)
    project_root = control.resolve().parent
    candidates = [reference] if reference.is_absolute() else [control / reference, project_root / reference]
    for candidate in candidates:
        resolved = candidate.resolve()
        if (
            (resolved == project_root or resolved.is_relative_to(project_root))
            and resolved.is_file()
        ):
            return resolved
    raise CampaignError(
        f"review evidence must resolve to a regular file inside the project: {value!r}"
    )


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
    event(
        state,
        "REVIEW_FREEZE_INVALIDATED",
        details={"reason": reason, "freeze": dict(freeze)},
    )


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


def rank_ready_work_units(state: dict[str, Any]) -> list[tuple[dict[str, Any], int]]:
    """Rank ready units by the longest still-open dependency path, then priority.

    This is an advisory next-action projection over the canonical campaign
    runtime. It does not mutate the tactical plan or grant execution authority.
    """
    units = work_map(state)
    terminal = TERMINAL_WORK_STATUSES
    dependents: dict[str, list[str]] = {unit_id: [] for unit_id in units}
    for unit_id, unit in units.items():
        for dependency in unit["dependencies"]:
            if dependency not in units:
                raise CampaignError(f"{unit_id}: dependency does not exist: {dependency}")
            dependents[dependency].append(unit_id)

    memo: dict[str, int] = {}
    visiting: set[str] = set()

    def remaining_path(unit_id: str) -> int:
        if unit_id in terminal or units[unit_id]["status"] in terminal:
            return 0
        if unit_id in memo:
            return memo[unit_id]
        if unit_id in visiting:
            raise CampaignError(f"dependency cycle detected at {unit_id}")
        visiting.add(unit_id)
        children = [child for child in dependents[unit_id] if units[child]["status"] not in terminal]
        score = 1 + max((remaining_path(child) for child in children), default=0)
        visiting.remove(unit_id)
        memo[unit_id] = score
        return score

    ready = [unit for unit in state["work_units"] if unit["status"] == "READY"]
    ranked = [(unit, remaining_path(unit["id"])) for unit in ready]
    return sorted(ranked, key=lambda item: (-item[1], -item[0]["priority"], item[0]["id"]))


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


def active_conflicts(state: dict[str, Any], candidate: dict[str, Any]) -> list[dict[str, Any]]:
    """Describe active work that currently prevents a candidate from starting."""
    conflicts: list[dict[str, Any]] = []
    for unit in state["work_units"]:
        if unit["id"] == candidate["id"] or unit["status"] != "ACTIVE":
            continue
        shared = set(unit["shared_resources"]) & set(candidate["shared_resources"])
        if shared:
            conflicts.append({"work_unit_id": unit["id"], "kind": "shared_resource",
                              "surfaces": sorted(shared)})
        write_conflicts: set[str] = set()
        for left in unit["allowed_write_surfaces"]:
            for right in candidate["allowed_write_surfaces"]:
                if pathish_conflict(left, right):
                    write_conflicts.add(right)
        if write_conflicts:
            conflicts.append({"work_unit_id": unit["id"], "kind": "write_surface",
                              "surfaces": sorted(write_conflicts)})
    return conflicts


def assert_no_active_conflict(state: dict[str, Any], candidate: dict[str, Any]) -> None:
    conflicts = active_conflicts(state, candidate)
    if not conflicts:
        return
    first = conflicts[0]
    if first["kind"] == "shared_resource":
        raise CampaignError(
            f"{candidate['id']}: shared-resource conflict with {first['work_unit_id']}: "
            f"{first['surfaces']}"
        )
    active = next(unit for unit in state["work_units"] if unit["id"] == first["work_unit_id"])
    overlapping = [
        (candidate_surface, active_surface)
        for candidate_surface in first["surfaces"]
        for active_surface in active["allowed_write_surfaces"]
        if pathish_conflict(candidate_surface, active_surface)
    ]
    raise CampaignError(
        f"{candidate['id']}: write-surface conflict with {first['work_unit_id']}: "
        f"{[(left, right) for left, right in overlapping]}"
    )


def require_campaign_active(state: dict[str, Any]) -> None:
    if state["campaign_status"] != "ACTIVE":
        raise CampaignError(f"campaign is not ACTIVE: {state['campaign_status']}")


def require_product_state_matches_runtime(control: Path, state: dict[str, Any]) -> None:
    path = product_state_path(control)
    if not path.exists():
        raise CampaignError(f"Product State is missing: {path}")
    product = load_json(path)
    if product.get("product_or_workstream") != state.get("product_or_workstream"):
        raise CampaignError("Product State and campaign runtime product/workstream differ")
    active = product.get("active_campaign")
    if not isinstance(active, dict) or active.get("campaign_id") != state.get("campaign_id"):
        raise CampaignError("Product State active campaign does not match campaign runtime")
    if product.get("current_code_ref") != state.get("integrated_ref"):
        raise CampaignError(
            f"Product State current_code_ref {product.get('current_code_ref')!r} "
            f"!= campaign runtime integrated_ref {state.get('integrated_ref')!r}"
        )
    if active.get("checkpoint_or_terminal_ref") != state.get("current_checkpoint_id"):
        raise CampaignError(
            "Product State checkpoint pointer does not match runtime current checkpoint"
        )
    checkpoint_id = state.get("current_checkpoint_id")
    if checkpoint_id:
        checkpoint_path = control / "campaigns" / state["campaign_id"] / "CHECKPOINT_CURRENT.json"
        if not checkpoint_path.is_file():
            raise CampaignError(f"current checkpoint file is missing: {checkpoint_path}")
        checkpoint = load_json(checkpoint_path)
        if (
            checkpoint.get("campaign_id") != state["campaign_id"]
            or checkpoint.get("checkpoint_id") != checkpoint_id
            or checkpoint.get("exact_integrated_ref") != state.get("integrated_ref")
        ):
            raise CampaignError("current checkpoint does not match Product State/runtime identity")

    currentness = set(product.get("currentness_set", []))
    required_refs = {"runtime/CAMPAIGN_RUNTIME_CURRENT.json"}
    if state.get("current_checkpoint_id"):
        required_refs.add(
            f"campaigns/{state['campaign_id']}/CHECKPOINT_CURRENT.json"
        )
    if authority_path(control).exists():
        required_refs.add("state/EXECUTION_AUTHORITY_CURRENT.json")
    if identity_path(control).exists():
        required_refs.add("state/IDENTITY_REGISTRY_CURRENT.json")
    missing_refs = sorted(required_refs - currentness)
    if missing_refs:
        raise CampaignError(
            f"Product State Currentness Set omits runtime owner(s): {missing_refs}"
        )


def require_authority_if_present(
    control: Path, state: dict[str, Any], *, actor: str | None = None,
    run: str | None = None,
) -> None:
    """Check the local authority owner, finite lease and registered current I3 run.

    The control-plane CLI cannot authenticate an operating-system caller; the
    actor/run supplied here are claims checked against the canonical registry.
    This is not proof of native provider identity or a host execution permit.
    """
    require_product_state_matches_runtime(control, state)
    path = authority_path(control)
    if not path.exists():
        return  # Legacy portable campaigns without execution authority.
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
    expires = authority.get("expires_at")
    try:
        expiry = datetime.fromisoformat(expires.replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError) as exc:
        raise CampaignError("ACTIVE_AUTHORITY_LEASE_MISSING_OR_INVALID") from exc
    if expiry.tzinfo is None or expiry.utcoffset() is None:
        raise CampaignError("ACTIVE_AUTHORITY_LEASE_MISSING_OR_INVALID")
    if expiry <= datetime.now(timezone.utc):
        raise CampaignError("ACTIVE_AUTHORITY_LEASE_EXPIRED")
    leader = authority.get("campaign_lead_actor_id")
    live_run = authority.get("current_run_id")
    if not isinstance(leader, str) or not leader or not isinstance(live_run, str) or not live_run:
        raise CampaignError("ACTIVE_AUTHORITY_ACTOR_OR_RUN_MISSING")
    if not identity_path(control).is_file():
        raise CampaignError("ACTIVE_AUTHORITY_IDENTITY_REGISTRY_MISSING")
    registry = load_json(identity_path(control))
    lead = next((r for r in registry.get("actors", []) if isinstance(r, dict) and r.get("actor_id") == leader), None)
    if not lead or lead.get("status") != "ACTIVE" or lead.get("current_run_id") != live_run or lead.get("role_class") != "I3_ENGINEERING_CAMPAIGN_LEAD":
        raise CampaignError("ACTIVE_AUTHORITY_LEADER_IDENTITY_STALE")
    if actor is not None or run is not None:
        if actor != leader or run != live_run:
            raise CampaignError("ACTIVE_AUTHORITY_ACTOR_RUN_MISMATCH")


def require_work_unit_owner(control: Path, state: dict[str, Any], unit: dict[str, Any]) -> None:
    """A work unit's recorded producer may not silently outlive the current I3 run.

    Explicit I4 delegation requires a separately enforced charter/lease path;
    self-written actor strings are not a delegated capability.
    """
    if authority_path(control).is_file() and unit.get("actor_id"):
        require_authority_if_present(
            control, state, actor=unit.get("actor_id"), run=unit.get("run_id")
        )


def require_current_review_evidence(control: Path, freeze: dict[str, Any]) -> None:
    refs = freeze.get("evidence_refs")
    bindings = freeze.get("evidence_bindings")
    if not isinstance(refs, list) or not refs or not isinstance(bindings, list) or len(refs) != len(bindings):
        raise CampaignError("REVIEW_EVIDENCE_BINDINGS_MISSING_OR_MISMATCHED")
    if len(refs) != len(set(refs)):
        raise CampaignError("REVIEW_EVIDENCE_DUPLICATE_REFS")
    for ref, binding in zip(refs, bindings):
        if not isinstance(ref, str) or not isinstance(binding, dict) or binding.get("ref") != ref:
            raise CampaignError("REVIEW_EVIDENCE_BINDINGS_MISSING_OR_MISMATCHED")
        expected = binding.get("sha256")
        if not isinstance(expected, str) or len(expected) != 64:
            raise CampaignError("REVIEW_EVIDENCE_BINDINGS_MISSING_OR_MISMATCHED")
        try:
            actual = sha256_file(evidence_file(control, ref))
        except CampaignError as exc:
            raise CampaignError(f"REVIEW_EVIDENCE_MISSING_OR_UNSAFE: {ref}") from exc
        if actual != expected:
            raise CampaignError(f"REVIEW_EVIDENCE_STALE: {ref}")


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
    if rt_path.exists():
        raise CampaignError(
            f"runtime already exists and cannot be replaced by init (including --force): {rt_path}"
        )

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
    elif not isinstance(active, dict):
        raise CampaignError("Product State active_campaign must be an object or null")
    elif active.get("campaign_id") != charter["campaign_id"]:
        raise CampaignError(
            f"Product State already has different active campaign: {active.get('campaign_id')}"
        )
    elif active.get("checkpoint_or_terminal_ref") is not None:
        raise CampaignError(
            "runtime is missing but Product State names an existing checkpoint/terminal; "
            "the checkpoint does not contain a complete runtime recovery snapshot, so init "
            "cannot reconstruct or replace campaign history"
        )
    elif (control / "campaigns" / charter["campaign_id"] / "CHECKPOINT_CURRENT.json").exists():
        raise CampaignError(
            "runtime is missing but an unreferenced current checkpoint exists; init cannot "
            "discard or reinterpret campaign history"
        )

    authority_path_current = authority_path(control)
    if authority_path_current.exists():
        authority = load_json(authority_path_current)
        if authority.get("authority_status") == "ACTIVE":
            if authority.get("campaign_id") != charter["campaign_id"]:
                raise CampaignError("active execution authority belongs to a different campaign")
            if authority.get("checkpoint_ref") is not None:
                raise CampaignError(
                    "runtime is missing but active execution authority names a checkpoint; "
                    "init cannot reconstruct or replace campaign history"
                )

    integrated_ref = args.integrated_ref or ps["current_code_ref"]
    if integrated_ref != ps.get("current_code_ref"):
        raise CampaignError(
            "init integrated_ref must match Product State current_code_ref; reconcile Product State first"
        )
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
    require_authority_if_present(control, state, actor=args.actor, run=args.run)
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
    require_work_unit_owner(control, state, unit)
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
    require_work_unit_owner(control, state, unit)
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
    require_work_unit_owner(control, state, unit)
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
    previous_freeze = state.get("review_freeze")
    if previous_freeze is not None:
        event(
            state,
            "REVIEW_FREEZE_SUPERSEDED",
            details={"freeze": dict(previous_freeze)},
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
        "evidence_bindings": [],
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
    require_authority_if_present(control, state)
    freeze = state.get("review_freeze")
    if not freeze or freeze["status"] != "FROZEN":
        raise CampaignError("independent review requires an active FROZEN review freeze")

    producer_actors = {unit["actor_id"] for unit in state["work_units"] if unit["actor_id"]}
    if args.reviewer in producer_actors:
        raise CampaignError(
            f"reviewer {args.reviewer!r} produced work in this candidate and is not independent"
        )

    id_path = identity_path(control)
    _, charter = read_charter(control, state)
    if charter.get("independent_review_required") is True and not id_path.exists():
        raise CampaignError("charter requires independent review but identity registry is missing")
    if id_path.exists():
        registry = load_json(id_path)
        actors = {item["actor_id"]: item for item in registry.get("actors", [])}
        actor = actors.get(args.reviewer)
        if actor is None:
            raise CampaignError(f"reviewer actor not found in identity registry: {args.reviewer}")
        if actor.get("status") != "ACTIVE":
            raise CampaignError(f"reviewer actor is not ACTIVE: {args.reviewer}")
        if actor.get("current_run_id") != args.run:
            raise CampaignError(
                f"reviewer run {args.run!r} != registry current_run_id "
                f"{actor.get('current_run_id')!r}"
            )

    refs = args.evidence or []
    if args.verdict == "PASS_FOR_STRATEGIC_RETURN" and not refs:
        raise CampaignError("PASS review requires at least one existing evidence file")
    bindings = []
    for ref in refs:
        evidence = evidence_file(control, ref)
        digest = sha256_file(evidence)
        if digest is None:
            raise CampaignError(f"review evidence is unavailable: {ref}")
        bindings.append({"ref": ref, "sha256": digest})

    freeze["status"] = "REVIEWED"
    freeze["reviewer_actor_id"] = args.reviewer
    freeze["reviewer_run_id"] = args.run
    freeze["verdict"] = args.verdict
    freeze["evidence_refs"] = refs
    freeze["evidence_bindings"] = bindings
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
    require_authority_if_present(control, state)
    if state["campaign_status"] == "STRATEGIC_TERMINAL":
        raise CampaignError("campaign already has a strategic terminal request")

    if args.type in READINESS_TERMINALS:
        freeze = state.get("review_freeze")
        if not freeze or freeze["status"] != "REVIEWED":
            raise CampaignError("readiness terminal requires REVIEWED exact-candidate freeze")
        if freeze["candidate_ref"] != state["integrated_ref"]:
            raise CampaignError("reviewed candidate is not current integrated_ref")
        if freeze.get("verdict") != "PASS_FOR_STRATEGIC_RETURN":
            raise CampaignError(
                "readiness terminal requires verdict PASS_FOR_STRATEGIC_RETURN"
            )
        if not freeze.get("reviewer_actor_id") or not freeze.get("reviewer_run_id"):
            raise CampaignError("readiness terminal requires bound reviewer identity and run")
        if not freeze.get("evidence_refs"):
            raise CampaignError("readiness terminal requires independent review evidence refs")
        # A PASS is not transferable: the same reviewed bytes must still exist.
        require_current_review_evidence(control, freeze)
        registry_path = identity_path(control)
        if registry_path.is_file():
            actors = {item.get("actor_id"): item for item in load_json(registry_path).get("actors", []) if isinstance(item, dict)}
            reviewer = actors.get(freeze["reviewer_actor_id"])
            if not reviewer or reviewer.get("status") != "ACTIVE" or reviewer.get("current_run_id") != freeze["reviewer_run_id"]:
                raise CampaignError("REVIEWER_IDENTITY_OR_RUN_STALE_AT_TERMINAL")
        _, charter = read_charter(control, state)
        if charter.get("independent_review_required") is True and not registry_path.is_file():
            raise CampaignError("INDEPENDENT_REVIEW_REGISTRY_MISSING_AT_TERMINAL")
        if any(unit.get("actor_id") == freeze["reviewer_actor_id"] for unit in state["work_units"]):
            raise CampaignError("REVIEWER_BECAME_PRODUCER_AFTER_REVIEW")
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
    lease_minutes = args.lease_minutes
    if type(lease_minutes) is not int or not 1 <= lease_minutes <= 120:
        raise CampaignError("authority lease must be an integer from 1 to 120 minutes")
    state = load_runtime(control)
    require_product_state_matches_runtime(control, state)
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
                expires_at = existing.get("expires_at")
                try:
                    expiry = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
                except (AttributeError, TypeError, ValueError):
                    raise CampaignError("active execution authority has no valid finite lease; release before reacquiring")
                if expiry.tzinfo is None or expiry.utcoffset() is None or expiry <= datetime.now(timezone.utc):
                    raise CampaignError("active execution authority lease is expired or timezone-naive; release before reacquiring")
                print("AUTHORITY ALREADY ACTIVE")
                return
            raise CampaignError("another ACTIVE execution authority already exists")

    acquired_at = datetime.now(timezone.utc)
    envelope = charter.get("resource_envelope", {})
    authority = {
        "schema_version": "execution-authority-0.1",
        "updated_at": acquired_at.isoformat().replace("+00:00", "Z"),
        "authority_status": "ACTIVE",
        "campaign_id": state["campaign_id"],
        "campaign_lead_actor_id": args.actor,
        "current_run_id": args.run,
        "baseline_ref": charter["baseline_ref"],
        "checkpoint_ref": state.get("current_checkpoint_id"),
        "allowed_write_surfaces": list(envelope.get("allowed_write_surfaces", [])),
        "protected_surfaces": list(envelope.get("protected_surfaces", [])),
        "expires_at": (acquired_at + timedelta(minutes=lease_minutes)).isoformat().replace("+00:00", "Z"),
        "lease_duration_minutes": lease_minutes,
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
    require_product_state_matches_runtime(control, state)
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


def cmd_host_probe(args: argparse.Namespace) -> None:
    from dataclasses import asdict
    from host_dispatch import CodexCliHost

    print(json.dumps(asdict(CodexCliHost().observe()), indent=2))


def cmd_host_dispatch(args: argparse.Namespace) -> None:
    from host_dispatch import CodexCliHost, DispatchHold, EngineeringCommand, prepare_dispatch
    from goal_guard import assess as assess_goal_guard

    goal_assessment = assess_goal_guard(control_root(args))
    if goal_assessment.get("may_execute_material_goal") is not True:
        print(json.dumps({"phase": "HOLD", "reason": "GOAL_GUARD_DENIED_OR_UNAVAILABLE",
                          "goal_guard": goal_assessment}, sort_keys=True), file=sys.stderr)
        raise CampaignError("Goal Guard did not issue a native material-execution permit")

    command_path = Path(args.command)
    if command_path.is_symlink() or not command_path.is_file() or command_path.stat().st_size > 64 * 1024:
        raise CampaignError("host command must be a regular non-symlink JSON file under 64 KiB")
    try:
        payload = json.loads(command_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or set(payload) != set(EngineeringCommand.__dataclass_fields__):
            raise CampaignError("host command JSON fields do not match EngineeringCommand")
        if not isinstance(payload.get("allowed_write_surfaces"), list):
            raise CampaignError("host command allowed_write_surfaces must be an array")
        payload["allowed_write_surfaces"] = tuple(payload["allowed_write_surfaces"])
        command = EngineeringCommand(**payload)
        result = prepare_dispatch(control_root(args), Path(args.workspace), command, CodexCliHost())
    except (OSError, ValueError, TypeError, json.JSONDecodeError, DispatchHold) as exc:
        print(f"HOST DISPATCH HOLD: {exc}", file=sys.stderr)
        raise CampaignError("host dispatch did not complete") from exc
    print(json.dumps(result, indent=2))


def cmd_host_recover(args: argparse.Namespace) -> None:
    from host_dispatch import DispatchHold, recover_interrupted_dispatch

    try:
        result = recover_interrupted_dispatch(control_root(args), args.dispatch_id)
    except DispatchHold as exc:
        print(f"HOST RECOVERY HOLD: {exc}", file=sys.stderr)
        raise CampaignError("host dispatch recovery did not complete") from exc
    print(json.dumps(result, indent=2))


def cmd_tool_dispatch(args: argparse.Namespace) -> None:
    from dataclasses import fields
    from tool_port import PortableTestAdapter, ToolCommand, ToolDispatchHold, dispatch_tool

    command_path = Path(args.command_file)
    if command_path.is_symlink() or not command_path.is_file() or command_path.stat().st_size > 3 * 1024 * 1024:
        raise CampaignError("tool command must be a regular non-symlink JSON file under 3 MiB")
    try:
        payload = json.loads(command_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or set(payload) != {field.name for field in fields(ToolCommand)}:
            raise CampaignError("tool command JSON fields do not match ToolCommand")
        if not isinstance(payload.get("allowed_write_surfaces"), list):
            raise CampaignError("tool command allowed_write_surfaces must be an array")
        payload["allowed_write_surfaces"] = tuple(payload["allowed_write_surfaces"])
        command = ToolCommand(**payload)
        if args.adapter != PortableTestAdapter.adapter_id:
            raise CampaignError("unknown adapter; only the fixed portable-test-v1 adapter is registered")
        result = dispatch_tool(control_root(args), Path(args.workspace), command)
    except (OSError, ValueError, TypeError, json.JSONDecodeError, ToolDispatchHold) as exc:
        print(f"TOOL DISPATCH HOLD: {exc}", file=sys.stderr)
        raise CampaignError("tool dispatch did not complete") from exc
    print(json.dumps(result, indent=2))


def cmd_tool_recover(args: argparse.Namespace) -> None:
    from tool_port import ToolDispatchHold, recover_tool_dispatch

    try:
        result = recover_tool_dispatch(control_root(args), args.dispatch_id)
    except ToolDispatchHold as exc:
        print(f"TOOL RECOVERY HOLD: {exc}", file=sys.stderr)
        raise CampaignError("tool recovery did not complete") from exc
    print(json.dumps(result, indent=2))


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
    ready = rank_ready_work_units(state)
    campaign_status = state.get("campaign_status", "UNKNOWN")
    projected = []
    for unit, critical_path_remaining in ready:
        conflicts = active_conflicts(state, unit)
        status_blocked = campaign_status != "ACTIVE"
        projected.append((unit, critical_path_remaining, conflicts, status_blocked))
    # Do not direct I3 toward READY work whose lease cannot currently be
    # acquired. Keep blocked candidates visible with their exact conflict so
    # the controller can choose independent work or plan a safe handoff.
    projected.sort(key=lambda item: (
        bool(item[2]) or item[3], -item[1], -item[0]["priority"], item[0]["id"]
    ))
    print(
        json.dumps(
            [
                {
                    "id": u["id"],
                    "title": u["title"],
                    "priority": u["priority"],
                    "critical_path_remaining": critical_path_remaining,
                    "writes": u["allowed_write_surfaces"],
                    "resources": u["shared_resources"],
                    "available_now": not conflicts and not status_blocked,
                    "active_conflicts": conflicts,
                    "blocked_by_campaign_status": campaign_status if status_blocked else None,
                }
                for u, critical_path_remaining, conflicts, status_blocked in projected
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
    p.add_argument("--lease-minutes", type=int, default=120,
                   help="Bounded authority lease duration (1-120 minutes; default 120).")
    p.set_defaults(func=cmd_authority_acquire)

    p = sub.add_parser("authority-release")
    p.add_argument("--actor", required=True)
    p.add_argument("--run", required=True)
    p.set_defaults(func=cmd_authority_release)

    p = sub.add_parser("host-probe", help="observe optional Codex CLI capabilities without dispatch")
    p.set_defaults(func=cmd_host_probe)

    p = sub.add_parser("host-dispatch", help="attempt source-bound dispatch through the installed Codex adapter; holds without enforced scope and cost cap")
    p.add_argument("--workspace", required=True)
    p.add_argument("--command", required=True, help="JSON EngineeringCommand file")
    p.set_defaults(func=cmd_host_dispatch)

    p = sub.add_parser("host-recover", help="mark an interrupted host dispatch UNKNOWN without replay")
    p.add_argument("--dispatch-id", required=True)
    p.set_defaults(func=cmd_host_recover)

    p = sub.add_parser("tool-dispatch", help="execute a typed local operation through the fixed portable ToolPort")
    p.add_argument("--workspace", required=True)
    p.add_argument("--command", dest="command_file", required=True, help="JSON ToolCommand file")
    p.add_argument("--adapter", default="portable-test-v1", help="registered deterministic adapter ID")
    p.set_defaults(func=cmd_tool_dispatch)

    p = sub.add_parser("tool-recover", help="mark an interrupted tool dispatch UNKNOWN without replay")
    p.add_argument("--dispatch-id", required=True)
    p.set_defaults(func=cmd_tool_recover)

    p = sub.add_parser("recover")
    p.set_defaults(func=cmd_recover)

    p = sub.add_parser("next")
    p.set_defaults(func=cmd_next)

    p = sub.add_parser("show")
    p.set_defaults(func=cmd_show)

    args = parser.parse_args()
    try:
        if args.command in {"next", "show", "host-probe", "host-dispatch", "host-recover", "tool-dispatch", "tool-recover"}:
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
