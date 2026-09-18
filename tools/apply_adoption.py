#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from state_tx import (
    StateTransactionError,
    journal_path,
    state_lock,
    write_state_set,
)

TOOL_DIR = Path(__file__).resolve().parent
CONTROL_ROOT_DEFAULT = TOOL_DIR.parent
SCHEMA_DIR = CONTROL_ROOT_DEFAULT / "schemas"
VALIDATOR = TOOL_DIR / "validate_project.py"


class AdoptionError(Exception):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise AdoptionError(f"cannot read JSON {path}: {exc}")
    if not isinstance(data, dict):
        raise AdoptionError(f"expected JSON object at {path}")
    return data


def atomic_id(concern_id: str, surface_ref: str) -> str:
    token = hashlib.sha256(f"{concern_id}\0{surface_ref}".encode("utf-8")).hexdigest()[:16]
    return f"OWNER_ADOPTED_{token.upper()}"


def resolve_ref(control: Path, value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    return (control / candidate).resolve()


def validate_spec(spec: dict[str, Any]) -> None:
    schema = load_json(SCHEMA_DIR / "adoption-spec.schema.json")
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    problems = sorted(validator.iter_errors(spec), key=lambda e: list(e.path))
    if problems:
        rendered = []
        for problem in problems:
            location = ".".join(str(p) for p in problem.path)
            suffix = f" at {location}" if location else ""
            rendered.append(f"{problem.message}{suffix}")
        raise AdoptionError("adoption spec validation failed: " + "; ".join(rendered))


def unique(values: list[str]) -> list[str]:
    out: list[str] = []
    for value in values:
        if value not in out:
            out.append(value)
    return out


def render_requirements(spec: dict[str, Any]) -> str:
    rows = [
        "# CLIENT Requirements — CURRENT",
        "",
        "Status: CURRENT",
        "",
        "## Product objective",
        "",
        spec["product_objective"],
        "",
        "## Active decisions",
        "",
        "| ID | Strength | Decision |",
        "|---|---|---|",
    ]
    for item in spec["requirements"]:
        decision = item["decision"].replace("|", "\\|").replace("\n", " ")
        rows.append(f"| {item['id']} | {item['strength']} | {decision} |")

    rows.extend(["", "## Open product questions", ""])
    if spec["open_product_questions"]:
        rows.extend(f"- {item}" for item in spec["open_product_questions"])
    else:
        rows.append("- None.")

    rows.extend(
        [
            "",
            "## External authority",
            "",
        ]
    )
    if spec["external_authority"]:
        rows.extend(f"- {item}" for item in spec["external_authority"])
    else:
        rows.append("- No external authority is granted by this adoption spec.")

    rows.extend(
        [
            "",
            "## Interpretation rule",
            "",
            "This file was normalized from an explicit adoption spec. "
            "Implementation details do not silently redefine these product decisions.",
            "",
        ]
    )
    return "\n".join(rows)


def render_overlay(spec: dict[str, Any]) -> str:
    lines = [
        "# Project / Workstream Overlay",
        "",
        "Status: CURRENT",
        "",
        "## Identity",
        "",
        f"- product/workstream: {spec['product_or_workstream']}",
        f"- current code ref: {spec['current_code_ref']}",
        "- current Product State: state/PRODUCT_STATE_CURRENT.json",
        "- current requirements: state/CLIENT_REQUIREMENTS_CURRENT.md",
        "- canonical owners: state/OWNER_REGISTRY_CURRENT.json",
        "",
        "## Product objective",
        "",
        spec["product_objective"],
        "",
        "## Architecture invariants",
        "",
    ]
    lines.extend(
        [f"- {item}" for item in spec["architecture_invariants"]]
        or ["- None declared."]
    )
    lines.extend(["", "## State semantics", ""])
    lines.extend([f"- {item}" for item in spec["state_semantics"]] or ["- None declared."])
    lines.extend(["", "## Verification gates", ""])
    lines.extend(f"- {item}" for item in spec["verification_gates"])
    lines.extend(["", "## External authority", ""])
    lines.extend(
        [f"- {item}" for item in spec["external_authority"]]
        or ["- No external authority granted."]
    )
    lines.extend(
        [
            "",
            "## Next legal boundary",
            "",
            spec["next_legal_boundary"],
            "",
            "## Forbidden actions",
            "",
        ]
    )
    lines.extend(
        [f"- {item}" for item in spec["forbidden_actions"]]
        or ["- None beyond global starter boundaries."]
    )
    lines.append("")
    return "\n".join(lines)


def custom_owner_entries(
    spec: dict[str, Any],
    existing_concerns: set[str],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen = set(existing_concerns)
    for owner in spec["custom_owners"]:
        concern = owner["concern_id"]
        if concern in seen:
            raise AdoptionError(
                f"custom owner concern already exists in canonical registry: {concern}"
            )
        seen.add(concern)
        out.append(
            {
                "owner_id": atomic_id(concern, owner["surface_ref"]),
                "concern_id": concern,
                "scope": spec["product_or_workstream"],
                "status": "CURRENT",
                "surface_ref": owner["surface_ref"],
                "surface_type": owner["surface_type"],
                "required_in_currentness_set": owner["required_in_currentness_set"],
                "supersedes_owner_ids": [],
                "superseded_by_owner_id": None,
            }
        )
    return out


def ensure_refs(control: Path, spec: dict[str, Any]) -> None:
    for ref in spec["currentness_refs"] + spec["evidence_refs"]:
        if not resolve_ref(control, ref).exists():
            raise AdoptionError(f"adoption ref does not resolve: {ref}")

    for owner in spec["custom_owners"]:
        if owner["surface_type"] == "EXTERNAL":
            continue
        if not resolve_ref(control, owner["surface_ref"]).exists():
            raise AdoptionError(
                f"custom owner surface does not resolve: {owner['surface_ref']}"
            )


def planned_state(
    control: Path,
    spec: dict[str, Any],
) -> dict[Path, dict[str, Any] | str]:
    product_path = control / "state" / "PRODUCT_STATE_CURRENT.json"
    bootstrap_path = control / "state" / "CURRENT_BOOTSTRAP_STATE.json"
    owners_path = control / "state" / "OWNER_REGISTRY_CURRENT.json"
    requirements_path = control / "state" / "CLIENT_REQUIREMENTS_CURRENT.md"
    overlay_path = control / "governance" / "PROJECT_OVERLAY.md"

    product = load_json(product_path)
    bootstrap = load_json(bootstrap_path)
    owners = load_json(owners_path)

    product_id = spec["product_or_workstream"]
    for label, value in [
        ("Product State", product.get("product_or_workstream")),
        ("bootstrap", bootstrap.get("product_or_workstream")),
        ("owner registry", owners.get("product_or_workstream")),
    ]:
        if value != product_id:
            raise AdoptionError(
                f"{label} product/workstream {value!r} != adoption spec {product_id!r}"
            )

    if product.get("active_campaign") is not None:
        raise AdoptionError("adoption promotion requires no active campaign")

    if bootstrap.get("active_campaign_ref") is not None:
        raise AdoptionError("adoption promotion requires no active campaign in bootstrap")

    if bootstrap.get("status") == "READY" and product.get("current_code_ref") == spec["current_code_ref"]:
        raise AdoptionError("control layer is already READY at the requested current_code_ref")

    existing_concerns = {
        owner["concern_id"]
        for owner in owners.get("owners", [])
        if owner.get("status") == "CURRENT"
    }
    additions = custom_owner_entries(spec, existing_concerns)

    currentness = list(product.get("currentness_set", []))
    currentness.extend(spec["currentness_refs"])
    for owner in additions:
        if owner["required_in_currentness_set"]:
            currentness.append(owner["surface_ref"])
    product["status"] = "CURRENT"
    product["state_version"] = str(int(product.get("state_version", "0")) + 1)
    product["updated_at"] = spec["verified_at"]
    product["current_code_ref"] = spec["current_code_ref"]
    product["product_objective"] = spec["product_objective"]
    product["requirement_refs"] = [item["id"] for item in spec["requirements"]]
    product["open_product_questions"] = list(spec["open_product_questions"])
    product["currentness_set"] = unique(currentness)
    product["capabilities"] = list(spec["capabilities"])
    product["active_campaign"] = None
    product["current_gate"] = spec["current_gate"]
    product["strongest_evidence_refs"] = list(spec["evidence_refs"])
    product["blockers"] = []
    product["next_legal_boundary"] = spec["next_legal_boundary"]
    product["forbidden_actions"] = list(spec["forbidden_actions"])

    bootstrap["schema_version"] = "starter-bootstrap-0.2"
    bootstrap["status"] = "READY"
    bootstrap["observed_code_ref"] = spec["current_code_ref"]
    bootstrap["observed_at"] = spec["verified_at"]
    bootstrap["role"] = spec["role"]
    bootstrap["active_campaign_ref"] = None
    bootstrap["active_checkpoint_or_terminal_ref"] = None
    bootstrap["current_gate"] = spec["current_gate"]
    bootstrap["strongest_evidence_refs"] = list(spec["evidence_refs"])
    bootstrap["next_legal_boundary"] = spec["next_legal_boundary"]
    bootstrap["forbidden_actions"] = list(spec["forbidden_actions"])
    bootstrap.pop("unresolved_currentness", None)
    bootstrap["currentness"] = {
        "verified": True,
        "verified_at": spec["verified_at"],
        "source_refs": unique(
            [
                bootstrap["requirements_ref"],
                bootstrap["product_state_ref"],
                "state/OWNER_REGISTRY_CURRENT.json",
                "governance/PROJECT_OVERLAY.md",
                *spec["currentness_refs"],
            ]
        ),
        "unresolved": [],
    }

    owners["updated_at"] = spec["verified_at"]
    owners["owners"].extend(additions)

    return {
        requirements_path: render_requirements(spec),
        overlay_path: render_overlay(spec),
        product_path: product,
        bootstrap_path: bootstrap,
        owners_path: owners,
    }


def validate_control(control: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--root", str(control)],
        cwd=CONTROL_ROOT_DEFAULT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AdoptionError(
            "control layer validation failed:\n"
            + result.stdout
            + "\n"
            + result.stderr
        )


def already_adopted(control: Path, spec: dict[str, Any]) -> bool:
    product = load_json(control / "state" / "PRODUCT_STATE_CURRENT.json")
    bootstrap = load_json(control / "state" / "CURRENT_BOOTSTRAP_STATE.json")
    owners = load_json(control / "state" / "OWNER_REGISTRY_CURRENT.json")

    if product.get("status") != "CURRENT" or bootstrap.get("status") != "READY":
        return False
    if product.get("active_campaign") is not None or bootstrap.get("active_campaign_ref") is not None:
        return False

    expected_product = {
        "current_code_ref": spec["current_code_ref"],
        "product_objective": spec["product_objective"],
        "requirement_refs": [item["id"] for item in spec["requirements"]],
        "open_product_questions": list(spec["open_product_questions"]),
        "capabilities": list(spec["capabilities"]),
        "current_gate": spec["current_gate"],
        "strongest_evidence_refs": list(spec["evidence_refs"]),
        "next_legal_boundary": spec["next_legal_boundary"],
        "forbidden_actions": list(spec["forbidden_actions"]),
    }
    for key, expected in expected_product.items():
        if product.get(key) != expected:
            return False

    expected_bootstrap = {
        "observed_code_ref": spec["current_code_ref"],
        "role": spec["role"],
        "current_gate": spec["current_gate"],
        "strongest_evidence_refs": list(spec["evidence_refs"]),
        "next_legal_boundary": spec["next_legal_boundary"],
        "forbidden_actions": list(spec["forbidden_actions"]),
    }
    for key, expected in expected_bootstrap.items():
        if bootstrap.get(key) != expected:
            return False

    currentness = bootstrap.get("currentness", {})
    if currentness.get("verified") is not True or currentness.get("unresolved") != []:
        return False

    current_owners = {
        item["concern_id"]: item
        for item in owners.get("owners", [])
        if item.get("status") == "CURRENT"
    }
    for item in spec["custom_owners"]:
        current = current_owners.get(item["concern_id"])
        if current is None:
            return False
        if (
            current.get("surface_ref") != item["surface_ref"]
            or current.get("surface_type") != item["surface_type"]
            or current.get("required_in_currentness_set")
            != item["required_in_currentness_set"]
        ):
            return False

    requirements_path = control / "state" / "CLIENT_REQUIREMENTS_CURRENT.md"
    overlay_path = control / "governance" / "PROJECT_OVERLAY.md"
    if requirements_path.read_text(encoding="utf-8") != render_requirements(spec):
        return False
    if overlay_path.read_text(encoding="utf-8") != render_overlay(spec):
        return False

    return True


def preflight(control: Path, writes: dict[Path, dict[str, Any] | str]) -> None:
    with tempfile.TemporaryDirectory(prefix="agentic-sdlc-adoption-preflight-") as tmp:
        candidate = Path(tmp) / "control"
        shutil.copytree(control, candidate)

        for target, payload in writes.items():
            relative = target.resolve().relative_to(control.resolve())
            destination = candidate / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(payload, dict):
                destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            else:
                destination.write_text(payload, encoding="utf-8")

        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "--root", str(candidate)],
            cwd=CONTROL_ROOT_DEFAULT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            raise AdoptionError(
                "candidate adoption state failed validation before commit:\n"
                + result.stdout
                + "\n"
                + result.stderr
            )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Promote a fail-closed scaffold using an explicit, validated adoption spec."
    )
    parser.add_argument("--control-root", required=True)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--lock-timeout", type=float, default=10.0)
    args = parser.parse_args()

    control = Path(args.control_root).resolve()
    spec_path = Path(args.spec).resolve()

    try:
        spec = load_json(spec_path)
        validate_spec(spec)
        ensure_refs(control, spec)

        with state_lock(control, args.lock_timeout):
            if journal_path(control).exists():
                raise AdoptionError(
                    "pending control-state transaction blocks adoption; recover it first"
                )

            if already_adopted(control, spec):
                validate_control(control)
                status = "ALREADY_ADOPTED"
                transaction_id = None
            else:
                writes = planned_state(control, spec)
                preflight(control, writes)
                transaction_id = write_state_set(
                    control,
                    "ADOPTION_PROMOTION",
                    list(writes.items()),
                )
                validate_control(control)
                status = "ADOPTED"
    except (AdoptionError, StateTransactionError) as exc:
        print(f"ADOPTION FAILED: {exc}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "status": status,
                "product_or_workstream": spec["product_or_workstream"],
                "current_code_ref": spec["current_code_ref"],
                "transaction_id": transaction_id,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
