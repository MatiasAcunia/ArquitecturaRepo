#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = REPO_ROOT / "schemas"

SCHEMA_BY_VERSION = {
    "product-state-0.1": "product-state.schema.json",
    "campaign-charter-0.1": "campaign-charter.schema.json",
    "campaign-checkpoint-0.1": "campaign-checkpoint.schema.json",
    "campaign-terminal-0.1": "campaign-terminal.schema.json",
    "identity-registry-0.1": "identity-registry.schema.json",
    "execution-authority-0.1": "execution-authority.schema.json",
    "starter-bootstrap-0.1": "current-bootstrap.schema.json",
    "starter-profiles-0.1": "profiles.schema.json",
    "starter-profile-selection-0.1": "profile-selection.schema.json",
    "campaign-runtime-0.1": "campaign-runtime.schema.json",
    "transition-journal-0.1": "transition-journal.schema.json",
}

GATE_TO_EVIDENCE_KEY = {
    "STATIC_STRUCTURAL": "static_structural",
    "UNIT_PROPERTY": "unit_property",
    "INTEGRATION": "integration",
    "DB_CURRENTNESS_LINEAGE_RECOVERY": "state_currentness_recovery",
    "RUNTIME_PHYSICAL": "runtime_physical",
    "SEMANTIC_GENERALIZATION": "semantic_generalization",
    "SECURITY_RIGHTS_PRIVACY": "security_rights_privacy",
    "PERCEPTUAL_HUMAN": "perceptual_human",
    "RELEASE_PUBLICATION": "release_live",
    "LIVE_MARKET": "release_live",
}


class ValidationError(Exception):
    pass


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def schema(name: str) -> dict[str, Any]:
    return load_json(SCHEMA_DIR / name)


def validate_instance(path: Path, data: Any, schema_name: str, errors: list[str]) -> None:
    validator = Draft202012Validator(schema(schema_name), format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        location = ".".join(str(p) for p in error.path)
        suffix = f" at {location}" if location else ""
        errors.append(f"{rel(path)}: schema validation failed{suffix}: {error.message}")


def resolve_ref(target_root: Path, value: str | None) -> bool:
    if not value:
        return False
    candidates = [
        target_root / value,
        REPO_ROOT / value,
    ]
    return any(p.exists() for p in candidates)


def scan(target_root: Path, errors: list[str]) -> dict[str, list[tuple[Path, dict[str, Any]]]]:
    buckets: dict[str, list[tuple[Path, dict[str, Any]]]] = defaultdict(list)

    for path in sorted(target_root.rglob("*.json")):
        if "schemas" in path.parts:
            continue
        try:
            data = load_json(path)
        except Exception as exc:
            errors.append(f"{rel(path)}: invalid JSON: {exc}")
            continue
        if not isinstance(data, dict):
            continue

        version = data.get("schema_version")
        if version in SCHEMA_BY_VERSION:
            validate_instance(path, data, SCHEMA_BY_VERSION[version], errors)
            buckets[version].append((path, data))
            continue

        if path.name == "STARTER_MANIFEST.json":
            validate_instance(path, data, "starter-manifest.schema.json", errors)
            buckets["starter-manifest"].append((path, data))
            continue

        if "interaction_id" in data and "intent_strength" in data:
            validate_instance(path, data, "interaction-record.schema.json", errors)
            buckets["interaction-record"].append((path, data))

    return buckets


def one_by_key(
    records: list[tuple[Path, dict[str, Any]]],
    key: str,
    label: str,
    errors: list[str],
) -> dict[str, tuple[Path, dict[str, Any]]]:
    out: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path, data in records:
        value = data.get(key)
        if not value:
            continue
        if value in out:
            errors.append(
                f"duplicate {label} {value!r}: {rel(out[value][0])} and {rel(path)}"
            )
        else:
            out[value] = (path, data)
    return out


def validate_product_state(
    target_root: Path,
    buckets: dict[str, list[tuple[Path, dict[str, Any]]]],
    errors: list[str],
) -> None:
    products = one_by_key(
        buckets.get("product-state-0.1", []),
        "product_or_workstream",
        "Product State owner",
        errors,
    )
    charters = one_by_key(
        buckets.get("campaign-charter-0.1", []),
        "campaign_id",
        "campaign charter",
        errors,
    )
    checkpoints = one_by_key(
        buckets.get("campaign-checkpoint-0.1", []),
        "checkpoint_id",
        "checkpoint",
        errors,
    )
    terminals = one_by_key(
        buckets.get("campaign-terminal-0.1", []),
        "campaign_id",
        "campaign terminal",
        errors,
    )

    for product_id, (path, state) in products.items():
        capability_ids: set[str] = set()
        for capability in state.get("capabilities", []):
            cid = capability["id"]
            if cid in capability_ids:
                errors.append(f"{rel(path)}: duplicate capability id {cid!r}")
            capability_ids.add(cid)

        for ref in state.get("currentness_set", []):
            if not resolve_ref(target_root, ref):
                errors.append(f"{rel(path)}: Currentness Set ref does not resolve: {ref}")

        active = state.get("active_campaign")
        if active is None:
            continue

        campaign_id = active["campaign_id"]
        charter_record = charters.get(campaign_id)
        if charter_record is None:
            errors.append(f"{rel(path)}: active campaign {campaign_id!r} has no charter")
            continue

        charter_path, charter = charter_record
        if charter["product_or_workstream"] != product_id:
            errors.append(
                f"{rel(path)}: campaign {campaign_id!r} product "
                f"{charter['product_or_workstream']!r} != Product State {product_id!r}"
            )
        if charter["capability"] not in capability_ids:
            errors.append(
                f"{rel(charter_path)}: capability {charter['capability']!r} "
                f"is not present in Product State {product_id!r}"
            )

        pointer = active.get("checkpoint_or_terminal_ref")
        if pointer:
            cp = checkpoints.get(pointer)
            if cp is not None:
                cp_path, cp_data = cp
                if cp_data["campaign_id"] != campaign_id:
                    errors.append(
                        f"{rel(cp_path)}: checkpoint campaign {cp_data['campaign_id']!r} "
                        f"!= active campaign {campaign_id!r}"
                    )
                if cp_data["exact_integrated_ref"] != state["current_code_ref"]:
                    errors.append(
                        f"{rel(path)}: current_code_ref {state['current_code_ref']!r} "
                        f"!= active checkpoint ref {cp_data['exact_integrated_ref']!r}"
                    )
            else:
                terminal = terminals.get(campaign_id)
                if terminal is None:
                    errors.append(
                        f"{rel(path)}: active pointer {pointer!r} resolves to neither "
                        f"a checkpoint id nor a terminal for {campaign_id!r}"
                    )
                else:
                    terminal_path, terminal_data = terminal
                    if terminal_data["exact_candidate_ref"] != state["current_code_ref"]:
                        errors.append(
                            f"{rel(path)}: current_code_ref {state['current_code_ref']!r} "
                            f"!= terminal candidate {terminal_data['exact_candidate_ref']!r}"
                        )


def validate_identity_and_authority(
    buckets: dict[str, list[tuple[Path, dict[str, Any]]]],
    errors: list[str],
) -> None:
    actors: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path, registry in buckets.get("identity-registry-0.1", []):
        for actor in registry.get("actors", []):
            actor_id = actor["actor_id"]
            if actor_id in actors:
                errors.append(
                    f"duplicate actor id {actor_id!r}: {rel(actors[actor_id][0])} and {rel(path)}"
                )
            else:
                actors[actor_id] = (path, actor)

    active_authority_by_campaign: dict[str, Path] = {}
    checkpoints = one_by_key(
        buckets.get("campaign-checkpoint-0.1", []),
        "checkpoint_id",
        "checkpoint",
        errors,
    )
    charters = one_by_key(
        buckets.get("campaign-charter-0.1", []),
        "campaign_id",
        "campaign charter",
        errors,
    )

    for path, authority in buckets.get("execution-authority-0.1", []):
        if authority["authority_status"] != "ACTIVE":
            continue

        campaign_id = authority["campaign_id"]
        if campaign_id in active_authority_by_campaign:
            errors.append(
                f"multiple ACTIVE execution authorities for {campaign_id!r}: "
                f"{rel(active_authority_by_campaign[campaign_id])} and {rel(path)}"
            )
        else:
            active_authority_by_campaign[campaign_id] = path

        charter_record = charters.get(campaign_id)
        if charter_record is None:
            errors.append(f"{rel(path)}: ACTIVE authority campaign {campaign_id!r} has no charter")
        else:
            _, charter = charter_record
            if authority["baseline_ref"] != charter["baseline_ref"]:
                errors.append(
                    f"{rel(path)}: authority baseline {authority['baseline_ref']!r} "
                    f"!= charter baseline {charter['baseline_ref']!r}"
                )

        actor_id = authority["campaign_lead_actor_id"]
        actor_record = actors.get(actor_id)
        if actor_record is None:
            errors.append(f"{rel(path)}: campaign lead actor {actor_id!r} not found")
        else:
            actor_path, actor = actor_record
            if actor["role_class"] != "I3_ENGINEERING_CAMPAIGN_LEAD":
                errors.append(
                    f"{rel(actor_path)}: actor {actor_id!r} is {actor['role_class']!r}, "
                    "not I3_ENGINEERING_CAMPAIGN_LEAD"
                )
            if actor["status"] != "ACTIVE":
                errors.append(f"{rel(actor_path)}: campaign lead actor {actor_id!r} is not ACTIVE")
            if actor.get("current_run_id") != authority.get("current_run_id"):
                errors.append(
                    f"{rel(path)}: authority run {authority.get('current_run_id')!r} "
                    f"!= actor current_run_id {actor.get('current_run_id')!r}"
                )

        checkpoint_ref = authority.get("checkpoint_ref")
        if checkpoint_ref:
            cp_record = checkpoints.get(checkpoint_ref)
            if cp_record is None:
                errors.append(f"{rel(path)}: checkpoint_ref {checkpoint_ref!r} not found")
            elif cp_record[1]["campaign_id"] != campaign_id:
                errors.append(
                    f"{rel(path)}: checkpoint {checkpoint_ref!r} belongs to "
                    f"{cp_record[1]['campaign_id']!r}, not {campaign_id!r}"
                )


def validate_bootstrap(
    target_root: Path,
    buckets: dict[str, list[tuple[Path, dict[str, Any]]]],
    errors: list[str],
) -> None:
    products = one_by_key(
        buckets.get("product-state-0.1", []),
        "product_or_workstream",
        "Product State owner",
        errors,
    )
    checkpoints = one_by_key(
        buckets.get("campaign-checkpoint-0.1", []),
        "checkpoint_id",
        "checkpoint",
        errors,
    )
    terminals = one_by_key(
        buckets.get("campaign-terminal-0.1", []),
        "campaign_id",
        "campaign terminal",
        errors,
    )

    for path, bootstrap in buckets.get("starter-bootstrap-0.1", []):
        product_id = bootstrap["product_or_workstream"]
        product_record = products.get(product_id)
        if product_record is None:
            errors.append(f"{rel(path)}: bootstrap product {product_id!r} has no Product State")
            continue

        _, state = product_record
        if bootstrap["status"] == "READY" and bootstrap.get("unresolved_currentness"):
            errors.append(f"{rel(path)}: READY bootstrap cannot have unresolved_currentness")

        if bootstrap.get("observed_code_ref") and bootstrap["observed_code_ref"] != state["current_code_ref"]:
            errors.append(
                f"{rel(path)}: observed_code_ref {bootstrap['observed_code_ref']!r} "
                f"!= Product State current_code_ref {state['current_code_ref']!r}"
            )

        if bootstrap.get("product_state_ref") and not resolve_ref(target_root, bootstrap["product_state_ref"]):
            errors.append(
                f"{rel(path)}: product_state_ref does not resolve: {bootstrap['product_state_ref']}"
            )
        if bootstrap.get("requirements_ref") and not resolve_ref(target_root, bootstrap["requirements_ref"]):
            errors.append(
                f"{rel(path)}: requirements_ref does not resolve: {bootstrap['requirements_ref']}"
            )

        active = state.get("active_campaign")
        if active is None:
            if bootstrap.get("active_campaign_ref") is not None:
                errors.append(
                    f"{rel(path)}: bootstrap names active campaign but Product State has none"
                )
            continue

        if bootstrap.get("active_campaign_ref") != active["campaign_id"]:
            errors.append(
                f"{rel(path)}: active_campaign_ref {bootstrap.get('active_campaign_ref')!r} "
                f"!= Product State active campaign {active['campaign_id']!r}"
            )

        current_pointer = bootstrap.get("active_checkpoint_or_terminal_ref")
        state_pointer = active.get("checkpoint_or_terminal_ref")
        if current_pointer != state_pointer:
            errors.append(
                f"{rel(path)}: checkpoint/terminal pointer {current_pointer!r} "
                f"!= Product State pointer {state_pointer!r}"
            )

        if current_pointer and current_pointer not in checkpoints and active["campaign_id"] not in terminals:
            errors.append(
                f"{rel(path)}: active checkpoint/terminal pointer {current_pointer!r} does not resolve"
            )


def validate_terminals(
    buckets: dict[str, list[tuple[Path, dict[str, Any]]]],
    errors: list[str],
) -> None:
    charters = one_by_key(
        buckets.get("campaign-charter-0.1", []),
        "campaign_id",
        "campaign charter",
        errors,
    )

    for path, terminal in buckets.get("campaign-terminal-0.1", []):
        campaign_id = terminal["campaign_id"]
        charter_record = charters.get(campaign_id)
        if charter_record is None:
            errors.append(f"{rel(path)}: terminal campaign {campaign_id!r} has no charter")
            continue

        _, charter = charter_record
        review = terminal.get("independent_review")
        if charter.get("independent_review_required", True):
            if terminal["terminal_type"] in {
                "CAPABILITY_READY_FOR_PLANNER_ACCEPTANCE",
                "QUALITY_GATE_READY_FOR_PLANNER_OR_HUMAN_DECISION",
            } and review is None:
                errors.append(f"{rel(path)}: readiness terminal requires independent_review")

        if review is not None and review["reviewed_candidate_ref"] != terminal["exact_candidate_ref"]:
            errors.append(
                f"{rel(path)}: reviewer candidate {review['reviewed_candidate_ref']!r} "
                f"!= terminal candidate {terminal['exact_candidate_ref']!r}"
            )

        if terminal["terminal_type"] not in {
            "CAPABILITY_READY_FOR_PLANNER_ACCEPTANCE",
            "QUALITY_GATE_READY_FOR_PLANNER_OR_HUMAN_DECISION",
        }:
            continue

        evidence = terminal.get("evidence", {})
        for gate in charter.get("verification_gates", []):
            if (
                terminal["terminal_type"] == "QUALITY_GATE_READY_FOR_PLANNER_OR_HUMAN_DECISION"
                and gate == "PERCEPTUAL_HUMAN"
            ):
                continue
            key = GATE_TO_EVIDENCE_KEY[gate]
            if not evidence.get(key):
                errors.append(
                    f"{rel(path)}: readiness terminal lacks evidence for charter gate {gate}"
                )



def runtime_write_conflict(a: str, b: str) -> bool:
    aa = a.strip().rstrip("/")
    bb = b.strip().rstrip("/")
    if aa == bb:
        return True
    if "/" in aa or "/" in bb:
        return aa.startswith(bb + "/") or bb.startswith(aa + "/")
    return False


def validate_campaign_runtime(
    buckets: dict[str, list[tuple[Path, dict[str, Any]]]],
    errors: list[str],
) -> None:
    runtimes = one_by_key(
        buckets.get("campaign-runtime-0.1", []),
        "campaign_id",
        "campaign runtime",
        errors,
    )
    charters = one_by_key(
        buckets.get("campaign-charter-0.1", []),
        "campaign_id",
        "campaign charter",
        errors,
    )
    checkpoints = one_by_key(
        buckets.get("campaign-checkpoint-0.1", []),
        "checkpoint_id",
        "checkpoint",
        errors,
    )
    products = one_by_key(
        buckets.get("product-state-0.1", []),
        "product_or_workstream",
        "Product State owner",
        errors,
    )
    authorities_by_campaign: dict[str, list[tuple[Path, dict[str, Any]]]] = defaultdict(list)
    for authority_path, authority in buckets.get("execution-authority-0.1", []):
        if authority.get("campaign_id"):
            authorities_by_campaign[authority["campaign_id"]].append(
                (authority_path, authority)
            )

    for campaign_id, (path, runtime) in runtimes.items():
        charter_record = charters.get(campaign_id)
        if charter_record is None:
            errors.append(f"{rel(path)}: runtime campaign {campaign_id!r} has no charter")
            continue
        _, charter = charter_record
        if runtime["product_or_workstream"] != charter["product_or_workstream"]:
            errors.append(
                f"{rel(path)}: runtime product {runtime['product_or_workstream']!r} "
                f"!= charter product {charter['product_or_workstream']!r}"
            )

        units: dict[str, dict[str, Any]] = {}
        for unit in runtime["work_units"]:
            unit_id = unit["id"]
            if unit_id in units:
                errors.append(f"{rel(path)}: duplicate runtime work unit id {unit_id!r}")
            units[unit_id] = unit

        visiting: set[str] = set()
        visited: set[str] = set()

        def dfs(unit_id: str) -> None:
            if unit_id in visiting:
                errors.append(f"{rel(path)}: dependency cycle includes {unit_id!r}")
                return
            if unit_id in visited or unit_id not in units:
                return
            visiting.add(unit_id)
            for dep in units[unit_id]["dependencies"]:
                if dep not in units:
                    errors.append(
                        f"{rel(path)}: {unit_id!r} dependency does not exist: {dep!r}"
                    )
                else:
                    dfs(dep)
            visiting.remove(unit_id)
            visited.add(unit_id)

        for unit_id in units:
            dfs(unit_id)

        for unit in units.values():
            if unit["status"] in {"READY", "ACTIVE", "VERIFY", "DONE"}:
                incomplete = [
                    dep
                    for dep in unit["dependencies"]
                    if dep in units and units[dep]["status"] != "DONE"
                ]
                if incomplete:
                    errors.append(
                        f"{rel(path)}: {unit['id']!r} status {unit['status']} "
                        f"has incomplete dependencies {sorted(incomplete)}"
                    )

        active = [u for u in units.values() if u["status"] == "ACTIVE"]
        for i, left in enumerate(active):
            for right in active[i + 1 :]:
                shared = set(left["shared_resources"]) & set(right["shared_resources"])
                if shared:
                    errors.append(
                        f"{rel(path)}: ACTIVE units {left['id']!r}/{right['id']!r} "
                        f"share resources {sorted(shared)}"
                    )
                for lsurf in left["allowed_write_surfaces"]:
                    for rsurf in right["allowed_write_surfaces"]:
                        if runtime_write_conflict(lsurf, rsurf):
                            errors.append(
                                f"{rel(path)}: ACTIVE units {left['id']!r}/{right['id']!r} "
                                f"have conflicting write surfaces {lsurf!r}/{rsurf!r}"
                            )

        seqs = [item["seq"] for item in runtime["event_log"]]
        if seqs != list(range(1, len(seqs) + 1)):
            errors.append(f"{rel(path)}: event_log seq must be contiguous from 1")
        if runtime["revision"] != len(runtime["event_log"]):
            errors.append(
                f"{rel(path)}: revision {runtime['revision']} "
                f"!= event count {len(runtime['event_log'])}"
            )

        checkpoint_id = runtime.get("current_checkpoint_id")
        if checkpoint_id:
            cp_record = checkpoints.get(checkpoint_id)
            if cp_record is None:
                errors.append(
                    f"{rel(path)}: current_checkpoint_id {checkpoint_id!r} not found"
                )
            else:
                cp_path, cp = cp_record
                if cp["campaign_id"] != campaign_id:
                    errors.append(
                        f"{rel(cp_path)}: runtime checkpoint belongs to "
                        f"{cp['campaign_id']!r}, not {campaign_id!r}"
                    )
                if cp["exact_integrated_ref"] != runtime["integrated_ref"]:
                    errors.append(
                        f"{rel(path)}: runtime integrated_ref {runtime['integrated_ref']!r} "
                        f"!= checkpoint ref {cp['exact_integrated_ref']!r}"
                    )

        authority_records = authorities_by_campaign.get(campaign_id, [])
        active_authorities = [
            (authority_path, authority)
            for authority_path, authority in authority_records
            if authority.get("authority_status") == "ACTIVE"
        ]
        if (
            runtime["campaign_status"] in {"ACTIVE", "HOLD", "CAPACITY_CHECKPOINT"}
            and authority_records
            and not active_authorities
        ):
            errors.append(
                f"{rel(path)}: campaign runtime is {runtime['campaign_status']} but "
                "configured execution authority is not ACTIVE"
            )
        if active_authorities and checkpoint_id:
            authority_path, authority = active_authorities[0]
            if authority.get("checkpoint_ref") != checkpoint_id:
                errors.append(
                    f"{rel(authority_path)}: active authority checkpoint "
                    f"{authority.get('checkpoint_ref')!r} != runtime checkpoint "
                    f"{checkpoint_id!r}"
                )

        product_record = products.get(runtime["product_or_workstream"])
        if product_record is not None:
            product_path, product = product_record
            active_campaign = product.get("active_campaign")
            if active_campaign and active_campaign.get("campaign_id") == campaign_id:
                if product["current_code_ref"] != runtime["integrated_ref"]:
                    errors.append(
                        f"{rel(product_path)}: Product State current_code_ref "
                        f"{product['current_code_ref']!r} != runtime integrated_ref "
                        f"{runtime['integrated_ref']!r}"
                    )
                if checkpoint_id and active_campaign.get("checkpoint_or_terminal_ref") != checkpoint_id:
                    errors.append(
                        f"{rel(product_path)}: Product State pointer "
                        f"{active_campaign.get('checkpoint_or_terminal_ref')!r} "
                        f"!= runtime checkpoint {checkpoint_id!r}"
                    )

        freeze = runtime.get("review_freeze")
        if freeze and freeze["status"] == "REVIEWED":
            if freeze["candidate_ref"] != runtime["integrated_ref"]:
                errors.append(
                    f"{rel(path)}: REVIEWED freeze candidate {freeze['candidate_ref']!r} "
                    f"!= runtime integrated_ref {runtime['integrated_ref']!r}"
                )
            producer_actors = {
                unit["actor_id"]
                for unit in units.values()
                if unit["actor_id"] and unit["status"] == "DONE"
            }
            if freeze.get("reviewer_actor_id") in producer_actors:
                errors.append(
                    f"{rel(path)}: reviewer actor {freeze.get('reviewer_actor_id')!r} "
                    "also produced DONE work"
                )

        terminal = runtime.get("terminal_request")
        if runtime["campaign_status"] == "STRATEGIC_TERMINAL" and terminal is None:
            errors.append(f"{rel(path)}: STRATEGIC_TERMINAL requires terminal_request")
        if runtime["campaign_status"] != "STRATEGIC_TERMINAL" and terminal is not None:
            errors.append(
                f"{rel(path)}: terminal_request exists while campaign_status is "
                f"{runtime['campaign_status']!r}"
            )
        if terminal and terminal["terminal_type"] in {
            "CAPABILITY_READY_FOR_PLANNER_ACCEPTANCE",
            "QUALITY_GATE_READY_FOR_PLANNER_OR_HUMAN_DECISION",
        }:
            if not freeze or freeze["status"] != "REVIEWED":
                errors.append(
                    f"{rel(path)}: readiness terminal request requires REVIEWED freeze"
                )
            unfinished = [
                unit["id"]
                for unit in units.values()
                if unit["status"] not in {"DONE", "PARKED", "SUPERSEDED", "CANCELLED"}
            ]
            if unfinished:
                errors.append(
                    f"{rel(path)}: readiness terminal has nonterminal work "
                    f"{sorted(unfinished)}"
                )


def validate_transition_journals(
    buckets: dict[str, list[tuple[Path, dict[str, Any]]]],
    errors: list[str],
) -> None:
    for path, journal in buckets.get("transition-journal-0.1", []):
        if path.name == "CURRENT_TRANSACTION.json":
            errors.append(
                f"{rel(path)}: pending multi-file transition "
                f"{journal.get('transaction_id')!r} status={journal.get('status')!r}; "
                "run campaignctl recover before accepting currentness"
            )

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Agentic SDLC JSON contracts and cross-file relationships."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project/example root to validate. Defaults to the repository root.",
    )
    args = parser.parse_args()

    target_root = (REPO_ROOT / args.root).resolve()
    if not target_root.exists():
        print(f"PROJECT VALIDATION FAILED\n- root does not exist: {target_root}")
        return 1

    errors: list[str] = []
    buckets = scan(target_root, errors)
    validate_product_state(target_root, buckets, errors)
    validate_identity_and_authority(buckets, errors)
    validate_bootstrap(target_root, buckets, errors)
    validate_terminals(buckets, errors)
    validate_campaign_runtime(buckets, errors)
    validate_transition_journals(buckets, errors)

    if errors:
        print("PROJECT VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    counts = {key: len(value) for key, value in sorted(buckets.items()) if value}
    print("PROJECT VALIDATION PASSED")
    print(json.dumps({"root": rel(target_root), "validated": counts}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
