#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "state" / "STARTER_MANIFEST.json").read_text(encoding="utf-8"))
PROFILES = json.loads((ROOT / "profiles" / "profiles.json").read_text(encoding="utf-8"))["profiles"]


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    write_text(path, json.dumps(data, indent=2) + "\n")


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def protocol_filename(protocol_id: str) -> str:
    return f"{protocol_id}.md"


def build_currentness_set(include_identity: bool) -> list[str]:
    refs = [
        "AGENTS.md",
        "state/CLIENT_REQUIREMENTS_CURRENT.md",
        "state/PRODUCT_STATE_CURRENT.json",
        "state/CURRENT_BOOTSTRAP_STATE.json",
        "state/OWNER_REGISTRY_CURRENT.json",
        "governance/PROJECT_OVERLAY.md",
    ]
    if include_identity:
        refs.extend(
            [
                "state/IDENTITY_REGISTRY_CURRENT.json",
                "state/EXECUTION_AUTHORITY_CURRENT.json",
            ]
        )
    return refs


def create_scaffold(
    target: Path,
    control_dir_name: str,
    profile_name: str,
    product_id: str,
    objective: str,
    force: bool,
    with_runtime: bool,
) -> Path:
    if not target.exists():
        target.mkdir(parents=True, exist_ok=True)
    if not target.is_dir():
        raise ValueError(f"target is not a directory: {target}")

    control = target / control_dir_name
    if control.exists():
        if not force:
            raise FileExistsError(
                f"{control} already exists; refuse to overwrite without --force"
            )
        shutil.rmtree(control)

    profile = PROFILES[profile_name]
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    version = MANIFEST["version"]

    core_protocols = list(MANIFEST["core_protocols"])
    optional_protocols = list(profile["optional_protocols"])
    selected_protocols = core_protocols + [
        p for p in optional_protocols if p not in core_protocols
    ]

    for protocol_id in selected_protocols:
        source = ROOT / "protocols" / protocol_filename(protocol_id)
        if not source.exists():
            raise FileNotFoundError(f"protocol declared but missing: {source}")
        copy_file(source, control / "protocols" / source.name)

    for schema_path in sorted((ROOT / "schemas").glob("*.schema.json")):
        copy_file(schema_path, control / "schemas" / schema_path.name)

    copy_file(
        ROOT / "prompts" / "FRESH_CONTEXT_PROBE.md",
        control / "prompts" / "FRESH_CONTEXT_PROBE.md",
    )
    copy_file(
        ROOT / "templates" / "CAMPAIGN_CHARTER.md",
        control / "templates" / "CAMPAIGN_CHARTER.md",
    )
    copy_file(
        ROOT / "templates" / "CAMPAIGN_CHECKPOINT.md",
        control / "templates" / "CAMPAIGN_CHECKPOINT.md",
    )
    copy_file(
        ROOT / "templates" / "CAMPAIGN_TERMINAL.md",
        control / "templates" / "CAMPAIGN_TERMINAL.md",
    )
    copy_file(
        ROOT / "tools" / "validate_project.py",
        control / "tools" / "validate_project.py",
    )
    copy_file(
        ROOT / "requirements-validation.txt",
        control / "requirements-validation.txt",
    )
    copy_file(
        ROOT / "tools" / "migrate_state.py",
        control / "tools" / "migrate_state.py",
    )
    copy_file(
        ROOT / "tools" / "reconstruct_context.py",
        control / "tools" / "reconstruct_context.py",
    )
    copy_file(
        ROOT / "migrations" / "registry.json",
        control / "migrations" / "registry.json",
    )
    if with_runtime:
        copy_file(
            ROOT / "tools" / "campaignctl.py",
            control / "tools" / "campaignctl.py",
        )

    include_identity = any(
        item in profile["recommended_current_contracts"]
        for item in ("IDENTITY_REGISTRY", "EXECUTION_AUTHORITY")
    )
    currentness_set = build_currentness_set(include_identity)

    requirements = f"""# CLIENT Requirements — CURRENT

Status: CURRENT

## Product objective

{objective}

## Active decisions

No normalized material decisions have been captured yet beyond the initial objective.

## Open product questions

- Confirm or refine product requirements during product discovery when they materially affect product/business behavior.

## Superseded decisions

- None.

## External authority

- No external, paid, publication or destructive authority is implied by this scaffold.

## Interpretation rule

This file is a fail-closed starting point. Do not convert placeholders or implementation suggestions into hard requirements.
"""
    write_text(control / "state" / "CLIENT_REQUIREMENTS_CURRENT.md", requirements)

    product_state = {
        "schema_version": "product-state-0.1",
        "product_or_workstream": product_id,
        "state_version": "0",
        "status": "HOLD",
        "updated_at": now,
        "current_code_ref": "UNRECONSTRUCTED",
        "product_objective": objective,
        "requirement_refs": [],
        "open_product_questions": [
            "Current product/code/runtime authority must be reconstructed from live evidence."
        ],
        "currentness_set": currentness_set,
        "capabilities": [],
        "active_campaign": None,
        "current_gate": "DISCOVERY",
        "strongest_evidence_refs": [],
        "blockers": [
            "Live code/runtime authority has not been reconstructed."
        ],
        "next_legal_boundary": (
            "Perform read-only discovery, establish exact current authority, "
            "then replace HOLD/UNRECONSTRUCTED state with evidence-bound current state."
        ),
        "forbidden_actions": [
            "Material implementation mutation before currentness reconstruction.",
            "Claiming capability acceptance from scaffold files.",
            "External spend/publication/destructive action without explicit authority."
        ],
    }
    write_json(control / "state" / "PRODUCT_STATE_CURRENT.json", product_state)

    bootstrap = {
        "schema_version": "starter-bootstrap-0.2",
        "status": "UNTRUSTED_CONTEXT",
        "product_or_workstream": product_id,
        "observed_code_ref": "UNRECONSTRUCTED",
        "observed_at": now,
        "role": "I2_PROJECT_WORKSTREAM_PLANNER",
        "kernel_version": f"agentic-sdlc-{version}",
        "requirements_ref": "state/CLIENT_REQUIREMENTS_CURRENT.md",
        "product_state_ref": "state/PRODUCT_STATE_CURRENT.json",
        "active_campaign_ref": None,
        "active_checkpoint_or_terminal_ref": None,
        "current_gate": "DISCOVERY",
        "strongest_evidence_refs": [],
        "next_legal_boundary": "Complete read-only discovery and currentness reconstruction.",
        "forbidden_actions": [
            "Material mutation while bootstrap status is UNTRUSTED_CONTEXT."
        ],
        "currentness": {
            "verified": False,
            "verified_at": None,
            "source_refs": [
                "state/CLIENT_REQUIREMENTS_CURRENT.md",
                "state/PRODUCT_STATE_CURRENT.json"
            ],
            "unresolved": [
                "Exact live code/runtime authority is unknown."
            ]
        },
    }
    write_json(control / "state" / "CURRENT_BOOTSTRAP_STATE.json", bootstrap)

    if include_identity:
        write_json(
            control / "state" / "IDENTITY_REGISTRY_CURRENT.json",
            {
                "schema_version": "identity-registry-0.1",
                "updated_at": now,
                "actors": [],
            },
        )
        write_json(
            control / "state" / "EXECUTION_AUTHORITY_CURRENT.json",
            {
                "schema_version": "execution-authority-0.1",
                "updated_at": now,
                "authority_status": "NONE",
                "campaign_id": None,
                "campaign_lead_actor_id": None,
                "current_run_id": None,
                "baseline_ref": None,
                "checkpoint_ref": None,
                "allowed_write_surfaces": [],
                "protected_surfaces": [],
                "expires_at": None,
            },
        )

    owner_entries = [
        {
            "owner_id": "OWNER_AGENT_ENTRYPOINT_001",
            "concern_id": "AGENT_ENTRYPOINT",
            "scope": product_id,
            "status": "CURRENT",
            "surface_ref": "AGENTS.md",
            "surface_type": "FILE",
            "required_in_currentness_set": True,
            "supersedes_owner_ids": [],
            "superseded_by_owner_id": None,
        },
        {
            "owner_id": "OWNER_CLIENT_REQUIREMENTS_001",
            "concern_id": "CLIENT_REQUIREMENTS",
            "scope": product_id,
            "status": "CURRENT",
            "surface_ref": "state/CLIENT_REQUIREMENTS_CURRENT.md",
            "surface_type": "FILE",
            "required_in_currentness_set": True,
            "supersedes_owner_ids": [],
            "superseded_by_owner_id": None,
        },
        {
            "owner_id": "OWNER_PRODUCT_STATE_001",
            "concern_id": "PRODUCT_STATE",
            "scope": product_id,
            "status": "CURRENT",
            "surface_ref": "state/PRODUCT_STATE_CURRENT.json",
            "surface_type": "FILE",
            "required_in_currentness_set": True,
            "supersedes_owner_ids": [],
            "superseded_by_owner_id": None,
        },
        {
            "owner_id": "OWNER_CURRENT_BOOTSTRAP_001",
            "concern_id": "CURRENT_BOOTSTRAP",
            "scope": product_id,
            "status": "CURRENT",
            "surface_ref": "state/CURRENT_BOOTSTRAP_STATE.json",
            "surface_type": "FILE",
            "required_in_currentness_set": True,
            "supersedes_owner_ids": [],
            "superseded_by_owner_id": None,
        },
        {
            "owner_id": "OWNER_PROJECT_OVERLAY_001",
            "concern_id": "PROJECT_OVERLAY",
            "scope": product_id,
            "status": "CURRENT",
            "surface_ref": "governance/PROJECT_OVERLAY.md",
            "surface_type": "FILE",
            "required_in_currentness_set": True,
            "supersedes_owner_ids": [],
            "superseded_by_owner_id": None,
        },
        {
            "owner_id": "OWNER_CANONICAL_REGISTRY_001",
            "concern_id": "CANONICAL_OWNER_REGISTRY",
            "scope": product_id,
            "status": "CURRENT",
            "surface_ref": "state/OWNER_REGISTRY_CURRENT.json",
            "surface_type": "FILE",
            "required_in_currentness_set": True,
            "supersedes_owner_ids": [],
            "superseded_by_owner_id": None,
        },
    ]
    if include_identity:
        owner_entries.extend(
            [
                {
                    "owner_id": "OWNER_IDENTITY_REGISTRY_001",
                    "concern_id": "IDENTITY_REGISTRY",
                    "scope": product_id,
                    "status": "CURRENT",
                    "surface_ref": "state/IDENTITY_REGISTRY_CURRENT.json",
                    "surface_type": "FILE",
                    "required_in_currentness_set": True,
                    "supersedes_owner_ids": [],
                    "superseded_by_owner_id": None,
                },
                {
                    "owner_id": "OWNER_EXECUTION_AUTHORITY_001",
                    "concern_id": "EXECUTION_AUTHORITY",
                    "scope": product_id,
                    "status": "CURRENT",
                    "surface_ref": "state/EXECUTION_AUTHORITY_CURRENT.json",
                    "surface_type": "FILE",
                    "required_in_currentness_set": True,
                    "supersedes_owner_ids": [],
                    "superseded_by_owner_id": None,
                },
            ]
        )

    write_json(
        control / "state" / "OWNER_REGISTRY_CURRENT.json",
        {
            "schema_version": "owner-registry-0.1",
            "product_or_workstream": product_id,
            "updated_at": now,
            "owners": owner_entries,
        },
    )

    overlay = f"""# Project / Workstream Overlay

Status: DRAFT / HOLD

## Identity

- product/workstream: {product_id}
- starter version: {version}
- installation profile: {profile_name}
- current Product State: state/PRODUCT_STATE_CURRENT.json
- current requirements: state/CLIENT_REQUIREMENTS_CURRENT.md
- currentness set: declared by Product State

## Product objective

{objective}

## Domain theory

UNRECONSTRUCTED. Load material product/domain theory from live project evidence before strategic planning.

## Canonical owners

| Concern | Owner |
|---|---|
| Product State | state/PRODUCT_STATE_CURRENT.json |
| Client requirements | state/CLIENT_REQUIREMENTS_CURRENT.md |
| Bootstrap/currentness | state/CURRENT_BOOTSTRAP_STATE.json |
| Canonical owner graph | state/OWNER_REGISTRY_CURRENT.json |
| Active campaign authority | UNSET |
| Acceptance evidence | UNSET |

## Architecture invariants

UNRECONSTRUCTED.

## State / DB semantics

UNRECONSTRUCTED.

## Verification gates

UNRECONSTRUCTED. Select only gates materially required by the product.

## External authority

No external authority is granted by this scaffold.

## Supersession

This overlay becomes CURRENT only after discovery/reconstruction establishes product-specific truth.
"""
    write_text(control / "governance" / "PROJECT_OVERLAY.md", overlay)

    agents = f"""# Project Agent Bootstrap

This project uses Agentic SDLC starter {version} with profile {profile_name}.

Start every fresh authority-bearing context as UNTRUSTED_CONTEXT.

Before material mutation read:

1. state/CLIENT_REQUIREMENTS_CURRENT.md
2. state/PRODUCT_STATE_CURRENT.json
3. state/CURRENT_BOOTSTRAP_STATE.json
4. state/OWNER_REGISTRY_CURRENT.json
5. governance/PROJECT_OVERLAY.md
6. applicable files under protocols/
7. live project code/state/runtime evidence

Do not treat this scaffold as evidence that the product is implemented.

Material mutation remains forbidden while Product State is HOLD or bootstrap status is UNTRUSTED_CONTEXT unless a narrowly scoped recovery action is explicitly authorized.

Planner owns strategy. Campaign Lead owns tactics inside a valid charter. Worker PASS is evidence, not acceptance.
"""
    write_text(control / "AGENTS.md", agents)

    runtime_report_line = (
        "- optional campaign runtime/controller;"
        if with_runtime
        else "- reference campaign runtime not installed;"
    )
    identity_report_line = (
        "- identity registry and execution-authority placeholders;"
        if include_identity
        else "- no identity/execution current state because this profile does not require it by default;"
    )

    report = f"""# Agentic SDLC Installation Report

## Target

- product/workstream: {product_id}
- installation profile: {profile_name}
- starter version: {version}
- baseline ref: UNRECONSTRUCTED
- generated at: {now}

## What was physically created

- profile-selected protocol set;
- machine-readable schemas;
- CLIENT requirements owner;
- Product State owner;
- bootstrap/currentness state;
- canonical owner registry;
- project overlay;
- campaign templates;
- fresh-context probe;
{runtime_report_line}\n{identity_report_line}

## Mechanization status

- durable state structure: MATERIALIZED
- live project currentness: DECLARED_ONLY / HOLD
- fresh-context reconstruction: NOT_YET_EXERCISED
- campaign execution: NOT_YET_AUTHORIZED
- product acceptance: NOT_ESTABLISHED

## Open HOLDs

- exact code/runtime authority has not been reconstructed;
- product-specific capability map and gates are not yet established.

## First legal boundary

Perform read-only discovery and currentness reconstruction. Do not start a material engineering campaign yet.

## Falsifiers

This installation is not ready if a fresh context cannot reconstruct one coherent posture without chat memory or technical CLIENT rescue.
"""
    write_text(control / "INSTALLATION_REPORT.md", report)

    write_text(
        control / "campaigns" / "README.md",
        "# Campaigns\n\nCreate campaign directories only after Planner authorizes a strategic charter.\n",
    )
    write_text(
        control / "interactions" / "README.md",
        "# Interactions\n\nStore only material interaction evidence needed for product authority/provenance.\n",
    )

    write_json(
        control / "PROFILE.json",
        {
            "schema_version": "starter-profile-selection-0.1",
            "starter_version": version,
            "profile": profile_name,
            "description": profile["description"],
            "selected_protocols": selected_protocols,
            "recommended_current_contracts": profile["recommended_current_contracts"],
            "runtime_enabled": with_runtime,
        },
    )

    runtime_readme_line = (
        f"Optional runtime installed at {control_dir_name}/tools/campaignctl.py."
        if with_runtime
        else "The optional reference runtime was not installed."
    )

    readme = f"""# Local Agentic SDLC Control Layer

Generated from Agentic SDLC starter {version}.

- profile: {profile_name}
- product/workstream: {product_id}
- initial state: HOLD / UNTRUSTED_CONTEXT

Next action: perform read-only discovery and currentness reconstruction.

Install the validation dependency:

```bash
python -m pip install -r {control_dir_name}/requirements-validation.txt
```

Validate this control layer with its copied validator:

```bash
python {control_dir_name}/tools/validate_project.py --root .
```

{runtime_readme_line}

Do not claim installation success until the fresh-context probe has been exercised and the installation report is updated with physical evidence.
"""
    write_text(control / "README.md", readme)

    return control


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a fail-closed project-local Agentic SDLC scaffold."
    )
    parser.add_argument("--target", required=True, help="Target project directory.")
    parser.add_argument(
        "--control-dir",
        default=".agentic-sdlc",
        help="Control-layer directory inside the target project.",
    )
    parser.add_argument(
        "--profile",
        required=True,
        choices=sorted(PROFILES),
        help="Starter operating profile.",
    )
    parser.add_argument("--product-id", required=True, help="Synthetic/project-local product id.")
    parser.add_argument(
        "--objective",
        default="TO_BE_CONFIRMED_DURING_PRODUCT_DISCOVERY",
        help="Initial client-visible product objective.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace only the generated control directory if it already exists.",
    )
    parser.add_argument(
        "--with-runtime",
        action="store_true",
        help="Copy the optional campaign runtime/controller into the generated control layer.",
    )
    args = parser.parse_args()

    try:
        control = create_scaffold(
            target=Path(args.target).resolve(),
            control_dir_name=args.control_dir,
            profile_name=args.profile,
            product_id=args.product_id,
            objective=args.objective,
            force=args.force,
            with_runtime=args.with_runtime,
        )
    except Exception as exc:
        print(f"SCAFFOLD FAILED: {exc}", file=sys.stderr)
        return 1

    print(f"SCAFFOLD CREATED: {control}")
    print("STATUS: HOLD / UNTRUSTED_CONTEXT")
    print("NEXT: read-only discovery -> currentness reconstruction -> fresh-context probe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
