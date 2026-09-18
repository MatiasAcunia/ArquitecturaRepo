#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

TOOL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = Path(__file__).resolve().parent / "validate_project.py"


class ReconstructionError(Exception):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ReconstructionError(f"cannot read JSON {path}: {exc}")
    if not isinstance(data, dict):
        raise ReconstructionError(f"expected JSON object: {path}")
    return data


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
        raise ReconstructionError("project validation failed before reconstruction:\n" + message)


def reconstruct(root: Path) -> dict[str, Any]:
    validate(root)
    records = scan_json(root)

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
    active = product_state.get("active_campaign")
    forbidden = []
    for value in list(product_state.get("forbidden_actions", [])) + list(
        bootstrap.get("forbidden_actions", [])
    ):
        if value not in forbidden:
            forbidden.append(value)

    result = {
        "schema_version": "reconstructed-context-0.1",
        "product_or_workstream": product,
        "posture": posture(product_state, bootstrap, currentness, authority, runtime),
        "product_state": {
            "status": product_state.get("status"),
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
        "currentness": currentness,
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
