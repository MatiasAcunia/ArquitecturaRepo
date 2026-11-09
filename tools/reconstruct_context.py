#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from git_currentness import observe_git_currentness

TOOL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = Path(__file__).resolve().parent / "validate_project.py"


class ReconstructionError(Exception):
    pass


def scan_json(root: Path) -> list[tuple[Path, dict[str, Any]]]:
    out: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(root.rglob("*.json")):
        if "schemas" in path.parts:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(data, dict):
            out.append((path, data))
    return out


def control_json_snapshot(root: Path) -> tuple[tuple[str, str], ...]:
    """Detect a changing control layer across validation and reconstruction.

    This is a read-only optimistic consistency check, not an execution lease or
    a substitute for CAS/transaction recovery during subsequent writes.
    """
    snapshot: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*.json")):
        if "schemas" in path.parts:
            continue
        try:
            content = path.read_bytes()
        except OSError as exc:
            raise ReconstructionError(f"control JSON changed or unreadable: {path}: {exc}") from exc
        snapshot.append((path.relative_to(root).as_posix(), hashlib.sha256(content).hexdigest()))
    return tuple(snapshot)


def one(
    records: list[tuple[Path, dict[str, Any]]],
    versions: set[str],
    label: str,
    product: str | None = None,
) -> tuple[Path, dict[str, Any]] | None:
    matches = [
        (path, data)
        for path, data in records
        if data.get("schema_version") in versions
        and (product is None or data.get("product_or_workstream") == product)
    ]
    if not matches:
        return None
    if len(matches) != 1:
        raise ReconstructionError(f"expected one {label}, found {len(matches)}")
    return matches[0]


def derive_currentness(bootstrap: dict[str, Any]) -> dict[str, Any]:
    if bootstrap["schema_version"] == "starter-bootstrap-0.2":
        currentness = bootstrap["currentness"]
        return {
            "verified": currentness["verified"],
            "verified_at": currentness["verified_at"],
            "source_refs": sorted(currentness["source_refs"]),
            "unresolved": list(currentness["unresolved"]),
        }

    unresolved = list(bootstrap.get("unresolved_currentness", []))
    verified = bootstrap.get("status") == "READY" and not unresolved
    return {
        "verified": verified,
        "verified_at": bootstrap.get("observed_at") if verified else None,
        "source_refs": sorted(
            [
                bootstrap.get("requirements_ref", ""),
                bootstrap.get("product_state_ref", ""),
            ]
        ),
        "unresolved": unresolved,
    }


def current_owners(registry: dict[str, Any] | None) -> list[dict[str, Any]]:
    if registry is None:
        return []
    return sorted(
        [
            {
                "concern_id": owner["concern_id"],
                "owner_id": owner["owner_id"],
                "surface_ref": owner["surface_ref"],
                "surface_type": owner["surface_type"],
            }
            for owner in registry.get("owners", [])
            if owner.get("status") == "CURRENT"
        ],
        key=lambda item: item["concern_id"],
    )


def authority_summary(authority: dict[str, Any] | None) -> dict[str, Any] | None:
    if authority is None:
        return None
    return {
        "status": authority.get("authority_status"),
        "campaign_id": authority.get("campaign_id"),
        "campaign_lead_actor_id": authority.get("campaign_lead_actor_id"),
        "current_run_id": authority.get("current_run_id"),
        "checkpoint_ref": authority.get("checkpoint_ref"),
    }


def runtime_summary(runtime: dict[str, Any] | None) -> dict[str, Any] | None:
    if runtime is None:
        return None
    work = runtime.get("work_units", [])
    counts: dict[str, int] = {}
    for unit in work:
        status = unit.get("status", "UNKNOWN")
        counts[status] = counts.get(status, 0) + 1
    return {
        "campaign_id": runtime.get("campaign_id"),
        "campaign_status": runtime.get("campaign_status"),
        "revision": runtime.get("revision"),
        "integrated_ref": runtime.get("integrated_ref"),
        "current_checkpoint_id": runtime.get("current_checkpoint_id"),
        "review_freeze_status": (
            runtime.get("review_freeze", {}).get("status")
            if runtime.get("review_freeze")
            else None
        ),
        "terminal_type": (
            runtime.get("terminal_request", {}).get("terminal_type")
            if runtime.get("terminal_request")
            else None
        ),
        "work_status_counts": dict(sorted(counts.items())),
    }


def canonical_handoff(
    records: list[tuple[Path, dict[str, Any]]],
    root: Path,
    active: dict[str, Any] | None,
    current_code_ref: str,
    currentness_set: list[str],
    snapshot: tuple[tuple[str, str], ...],
) -> dict[str, Any]:
    """Read the active checkpoint/terminal itself; never infer state from old chat.

    This is a transient, source-bound view of the *existing* canonical record,
    not a second mutable memory or a substitute for state transaction/recovery.
    """
    if active is None:
        return {"status": "NO_ACTIVE_CAMPAIGN", "source_ref": None}

    campaign_id = active["campaign_id"]
    pointer = active.get("checkpoint_or_terminal_ref")
    if not pointer:
        return {
            "status": "NO_CHECKPOINT_OR_TERMINAL",
            "campaign_id": campaign_id,
            "source_ref": None,
        }

    checkpoints = [
        (path, data)
        for path, data in records
        if data.get("schema_version") == "campaign-checkpoint-0.1"
        and data.get("checkpoint_id") == pointer
    ]
    if len(checkpoints) > 1:
        raise ReconstructionError(f"duplicate active checkpoint {pointer!r}")

    if checkpoints:
        path, data = checkpoints[0]
        if data["campaign_id"] != campaign_id or data["exact_integrated_ref"] != current_code_ref:
            raise ReconstructionError("active checkpoint is not bound to current campaign and code")
        status = "CHECKPOINT"
    else:
        terminals = [
            (path, data)
            for path, data in records
            if data.get("schema_version") == "campaign-terminal-0.1"
            and data.get("campaign_id") == campaign_id
        ]
        if len(terminals) != 1:
            raise ReconstructionError("active terminal pointer has no unique canonical terminal")
        path, data = terminals[0]
        relative = path.relative_to(root).as_posix()
        if pointer not in {path.stem, path.name, relative}:
            raise ReconstructionError("active terminal pointer does not name the canonical terminal")
        if data["exact_candidate_ref"] != current_code_ref:
            raise ReconstructionError("active terminal is not bound to current code")
        status = "TERMINAL"

    relative = path.relative_to(root).as_posix()
    refs = {ref.replace("\\", "/").removeprefix("./") for ref in currentness_set}
    if not ({relative, path.name} & refs):
        raise ReconstructionError(
            f"active {status.lower()} {relative!r} is not in the canonical Currentness Set"
        )
    hashes = dict(snapshot)
    if relative not in hashes:
        raise ReconstructionError("active continuation source missing from control snapshot")

    source = {
        "status": status,
        "campaign_id": campaign_id,
        "source_ref": relative,
        "source_sha256": hashes[relative],
        "code_ref": current_code_ref,
    }
    if status == "CHECKPOINT":
        source.update(
            checkpoint_id=data["checkpoint_id"],
            created_at=data["created_at"],
            charter_status=data["charter_status"],
            completed_capability_delta=data.get("completed_capability_delta"),
            tactical_dag=data["tactical_dag"],
            evidence_refs=data["evidence_refs"],
            rejected_approaches=data.get("rejected_approaches"),
            current_falsifiers=data.get("current_falsifiers"),
            resource_locks=data.get("resource_locks"),
            resume_procedure=data["resume_procedure"],
            strategic_return_required=data.get("strategic_return_required"),
        )
    else:
        source.update(
            terminal_type=data["terminal_type"],
            capability_claim=data["capability_claim"],
            evidence=data["evidence"],
            independent_review=data.get("independent_review"),
            known_limitations=data["known_limitations"],
            in_scope_rework_remaining=data.get("in_scope_rework_remaining"),
            strategic_return_reason=data["strategic_return_reason"],
        )
    return source


def posture(
    product_state: dict[str, Any],
    bootstrap: dict[str, Any],
    currentness: dict[str, Any],
    authority: dict[str, Any] | None,
    runtime: dict[str, Any] | None,
) -> str:
    if bootstrap.get("status") == "UNTRUSTED_CONTEXT" or not currentness["verified"]:
        return "UNTRUSTED_CONTEXT"
    if product_state.get("status") == "HOLD" or bootstrap.get("status") == "HOLD":
        return "HOLD"
    if (
        product_state.get("current_gate") == "PLANNER_ACCEPTANCE"
        or (runtime and runtime.get("campaign_status") == "STRATEGIC_TERMINAL")
    ):
        return "STRATEGIC_RETURN_BOUNDARY"
    if authority and authority.get("authority_status") == "ACTIVE":
        return "EXECUTION_AUTHORIZED"
    return "RECONSTRUCTED_NO_ACTIVE_EXECUTION"


def validate(root: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--root", str(root)],
        cwd=TOOL_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        message = (result.stdout + "\n" + result.stderr).strip()
        if "No module named 'jsonschema'" in message or 'No module named "jsonschema"' in message:
            raise ReconstructionError(
                "validation dependency 'jsonschema' is missing. Install the "
                "declared dependencies with: python -m pip install -r "
                f'\"{root / "requirements-validation.txt"}\"'
            )
        raise ReconstructionError("project validation failed before reconstruction:\n" + message)


def reconstruct(root: Path) -> dict[str, Any]:
    before = control_json_snapshot(root)
    validate(root)
    records = scan_json(root)
    if control_json_snapshot(root) != before:
        raise ReconstructionError("control JSON changed during validation/reconstruction; retry after writers settle")

    product_record = one(records, {"product-state-0.1"}, "Product State")
    if product_record is None:
        raise ReconstructionError("no Product State found")
    product_path, product_state = product_record
    product = product_state["product_or_workstream"]

    bootstrap_record = one(
        records,
        {"starter-bootstrap-0.1", "starter-bootstrap-0.2"},
        "current bootstrap",
        product,
    )
    if bootstrap_record is None:
        raise ReconstructionError(f"no current bootstrap found for {product!r}")
    bootstrap_path, bootstrap = bootstrap_record

    owner_record = one(records, {"owner-registry-0.1"}, "owner registry", product)
    technical_record = one(records, {"technical-baseline-0.1"}, "technical baseline", product)
    delivery_record = one(records, {"delivery-plan-0.1"}, "delivery plan", product)
    owner_registry = owner_record[1] if owner_record else None

    authority_records = [
        (path, data)
        for path, data in records
        if data.get("schema_version") == "execution-authority-0.1"
        and data.get("campaign_id") in {
            None,
            (product_state.get("active_campaign") or {}).get("campaign_id"),
        }
    ]
    if len(authority_records) > 1:
        raise ReconstructionError("multiple execution-authority records match current product")
    authority = authority_records[0][1] if authority_records else None

    runtime_records = [
        (path, data)
        for path, data in records
        if data.get("schema_version") == "campaign-runtime-0.1"
        and data.get("product_or_workstream") == product
    ]
    if len(runtime_records) > 1:
        raise ReconstructionError("multiple campaign runtimes match current product")
    runtime = runtime_records[0][1] if runtime_records else None

    currentness = derive_currentness(bootstrap)
    git_currentness = observe_git_currentness(root, product_state.get("current_code_ref", ""))
    canonical_posture = posture(product_state, bootstrap, currentness, authority, runtime)
    tracking_conflict = git_currentness["upstream"]["relation"] in {
        "LOCAL_BEHIND_TRACKING",
        "DIVERGED_OR_UNRELATED_TRACKING",
        "TRACKING_REF_UNRESOLVED",
    }
    active = product_state.get("active_campaign")
    handoff = canonical_handoff(
        records,
        root,
        active,
        product_state["current_code_ref"],
        product_state.get("currentness_set", []),
        before,
    )
    forbidden = []
    for value in list(product_state.get("forbidden_actions", [])) + list(
        bootstrap.get("forbidden_actions", [])
    ):
        if value not in forbidden:
            forbidden.append(value)

    result = {
        "schema_version": "reconstructed-context-0.1",
        "product_or_workstream": product,
        "posture": canonical_posture,
        "product_state": {
            "status": product_state.get("status"),
            "state_version": product_state.get("state_version"),
            "current_code_ref": product_state.get("current_code_ref"),
            "current_gate": product_state.get("current_gate"),
            "active_campaign_id": active.get("campaign_id") if active else None,
            "checkpoint_or_terminal_ref": (
                active.get("checkpoint_or_terminal_ref") if active else None
            ),
            "blockers": list(product_state.get("blockers", [])),
            "next_legal_boundary": product_state.get("next_legal_boundary"),
        },
        "bootstrap": {
            "schema_version": bootstrap.get("schema_version"),
            "status": bootstrap.get("status"),
            "role": bootstrap.get("role"),
            "observed_code_ref": bootstrap.get("observed_code_ref"),
            "active_campaign_ref": bootstrap.get("active_campaign_ref"),
            "active_checkpoint_or_terminal_ref": bootstrap.get(
                "active_checkpoint_or_terminal_ref"
            ),
            "next_legal_boundary": bootstrap.get("next_legal_boundary"),
        },
        "canonical_handoff": handoff,
        "currentness": currentness,
        "git_currentness": git_currentness,
        "continuation_preflight": {
            "local_source_reconciled": git_currentness["local_source_reconciled"],
            "remote_source_verified": False,
            "native_execution_authorized_by_git": False,
            "effective_posture": (
                "CURRENTNESS_RECONCILIATION_REQUIRED"
                if (not git_currentness["local_source_reconciled"] or tracking_conflict)
                and canonical_posture == "EXECUTION_AUTHORIZED"
                else canonical_posture
            ),
            "next_safe_action": (
                "RECONCILE_LOCAL_SOURCE_READ_ONLY"
                if not git_currentness["local_source_reconciled"]
                else "RECONCILE_TRACKING_CONFLICT_READ_ONLY"
                if tracking_conflict
                else "VERIFY_LIVE_REMOTE_AND_SEPARATE_EXECUTION_AUTHORITY"
            ),
            "required_reconciliation": git_currentness["reconciliation_required"],
            "rule": "Canonical authority, local Git evidence, live remote currentness and native host permissions are separate gates.",
        },
        "current_owners": current_owners(owner_registry),
        "technical_baseline": (
            {
                "status": technical_record[1].get("status"),
                "baseline_version": technical_record[1].get("baseline_version"),
                "deployment_target": technical_record[1].get("environment", {}).get("deployment_target"),
                "network_mode": technical_record[1].get("environment", {}).get("network_mode"),
                "stack": {
                    "language": technical_record[1].get("stack", {}).get("language"),
                    "backend": technical_record[1].get("stack", {}).get("backend"),
                    "frontend": technical_record[1].get("stack", {}).get("frontend"),
                    "database": technical_record[1].get("stack", {}).get("database"),
                },
                "unresolved": list(technical_record[1].get("unresolved", [])),
            }
            if technical_record
            else None
        ),
        "delivery_plan": (
            {
                "status": delivery_record[1].get("status"),
                "plan_version": delivery_record[1].get("plan_version"),
                "target_release_date": delivery_record[1].get("target_release_date"),
                "next_review_date": delivery_record[1].get("next_review_date"),
                "milestones": [
                    {
                        "id": item.get("id"),
                        "title": item.get("title"),
                        "target_date": item.get("target_date"),
                        "status": item.get("status"),
                        "forecast_confidence": item.get("forecast_confidence"),
                    }
                    for item in delivery_record[1].get("milestones", [])
                ],
                "unresolved": list(delivery_record[1].get("unresolved", [])),
            }
            if delivery_record
            else None
        ),
        "execution_authority": authority_summary(authority),
        "campaign_runtime": runtime_summary(runtime),
        "forbidden_actions": forbidden,
        "evidence": {
            "product_state_ref": str(product_path.relative_to(root)),
            "bootstrap_ref": str(bootstrap_path.relative_to(root)),
            "currentness_set": sorted(product_state.get("currentness_set", [])),
        },
    }
    if control_json_snapshot(root) != before:
        raise ReconstructionError("control JSON changed during reconstruction; retry after writers settle")
    git_after = observe_git_currentness(root, product_state.get("current_code_ref", ""))
    if git_after != git_currentness:
        raise ReconstructionError("local Git observation changed during reconstruction; reconcile source before proceeding")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and deterministically reconstruct current Agentic SDLC posture."
    )
    parser.add_argument("--root", required=True, help="Control-layer root.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    try:
        result = reconstruct(root)
    except ReconstructionError as exc:
        print(f"RECONSTRUCTION FAILED: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
