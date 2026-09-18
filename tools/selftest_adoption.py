#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD = ROOT / "tools" / "scaffold_project.py"


def run(
    *args: str,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )


def is_managed_feedback_workflow(project: Path, path: Path) -> bool:
    try:
        relative = str(path.relative_to(project)).replace(os.sep, "/")
    except ValueError:
        return False
    if relative != ".github/workflows/agentic-sdlc-feedback.yml":
        return False
    try:
        return "Managed by Agentic SDLC starter" in path.read_text(encoding="utf-8")[:512]
    except Exception:
        return False


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def application_snapshot(project: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(project.rglob("*")):
        if not path.is_file():
            continue
        if ".agentic-sdlc" in path.parts or ".git" in path.parts:
            continue
        if is_managed_feedback_workflow(project, path):
            continue
        result[str(path.relative_to(project))] = sha256(path)
    return result


def write_fixture(project: Path, files: dict[str, str]) -> None:
    for relative, content in files.items():
        path = project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def profile_cases() -> list[dict[str, Any]]:
    return [
        {
            "profile": "SMALL",
            "files": {
                "src/main.py": "def greet(name):\n    return f'hello {name}'\n",
                "README.md": "# Tiny synthetic app\n",
            },
            "surface": "../src/main.py",
            "concern": "APPLICATION_ENTRYPOINT",
            "gates": ["UNIT_PROPERTY"],
        },
        {
            "profile": "STATEFUL",
            "files": {
                "service/store.py": "SCHEMA_VERSION = 1\n",
                "migrations/001.sql": "CREATE TABLE notes(id INTEGER PRIMARY KEY);\n",
            },
            "surface": "../service/store.py",
            "concern": "APPLICATION_STATE_MECHANISM",
            "gates": ["UNIT_PROPERTY", "DB_CURRENTNESS_LINEAGE_RECOVERY"],
        },
        {
            "profile": "ARTIFACT_HEAVY",
            "files": {
                "pipeline/render.py": "def render(value):\n    return value.upper()\n",
                "inputs/example.txt": "synthetic input\n",
            },
            "surface": "../pipeline/render.py",
            "concern": "ARTIFACT_PIPELINE",
            "gates": ["UNIT_PROPERTY", "RUNTIME_PHYSICAL"],
        },
        {
            "profile": "MULTI_WORKSTREAM",
            "files": {
                "api/app.py": "API_VERSION = 1\n",
                "web/app.js": "export const uiVersion = 1;\n",
                "shared/schema.json": "{\"version\": 1}\n",
            },
            "surface": "../shared/schema.json",
            "concern": "WORKSTREAM_INTEGRATION_CONTRACT",
            "gates": ["INTEGRATION", "RUNTIME_PHYSICAL"],
        },
        {
            "profile": "MULTI_PRODUCT",
            "files": {
                "product_a/main.py": "PRODUCT = 'A'\n",
                "product_b/main.py": "PRODUCT = 'B'\n",
                "portfolio.json": "{\"products\": [\"A\", \"B\"]}\n",
            },
            "surface": "../portfolio.json",
            "concern": "PORTFOLIO_PRODUCT_REGISTRY",
            "gates": ["INTEGRATION"],
        },
        {
            "profile": "HIGH_CONSEQUENCE",
            "files": {
                "actions/plan.py": "ALLOW_EXTERNAL_ACTION = False\n",
                "policy/constraints.md": "# Synthetic external-action constraints\n",
            },
            "surface": "../policy/constraints.md",
            "concern": "EXTERNAL_ACTION_POLICY",
            "gates": ["SECURITY_RIGHTS_PRIVACY", "RUNTIME_PHYSICAL"],
        },
    ]


def build_spec(
    case: dict[str, Any],
    product_id: str,
    inventory_ref: str,
    inventory_hash: str,
) -> dict[str, Any]:
    return {
        "schema_version": "adoption-spec-0.1",
        "product_or_workstream": product_id,
        "current_code_ref": f"inventory/{inventory_hash[:16]}",
        "product_objective": f"Adopt the synthetic {case['profile']} project without mutating application files.",
        "role": "I2_PROJECT_WORKSTREAM_PLANNER",
        "current_gate": "ADOPTION_VERIFIED",
        "verified_at": "2031-01-01T00:00:00Z",
        "requirements": [
            {
                "id": f"REQ-{case['profile']}-001",
                "strength": "HARD_REQUIREMENT",
                "decision": "Preserve the existing synthetic application while establishing reconstructible Agentic SDLC control state.",
            }
        ],
        "open_product_questions": [],
        "capabilities": [
            {
                "id": f"CAPABILITY_{case['profile']}_BASELINE",
                "owner": "EXISTING_APPLICATION",
                "physical_state": "OBSERVED_BASELINE",
                "gate": case["gates"][-1],
                "dependencies": [],
                "evidence_refs": [inventory_ref],
            }
        ],
        "evidence_refs": [inventory_ref],
        "currentness_refs": [inventory_ref],
        "custom_owners": [
            {
                "concern_id": "DISCOVERY_INVENTORY",
                "surface_ref": inventory_ref,
                "surface_type": "FILE",
                "required_in_currentness_set": True,
            },
            {
                "concern_id": case["concern"],
                "surface_ref": case["surface"],
                "surface_type": "FILE",
                "required_in_currentness_set": True,
            },
        ],
        "architecture_invariants": [
            "Existing application files are evidence and are not rewritten by adoption tooling."
        ],
        "state_semantics": (
            ["Persistent state changes require explicit migration/recovery evidence."]
            if case["profile"] == "STATEFUL"
            else []
        ),
        "verification_gates": case["gates"],
        "external_authority": (
            ["No external action is authorized by this synthetic adoption."]
            if case["profile"] == "HIGH_CONSEQUENCE"
            else []
        ),
        "next_legal_boundary": "Open a strategic campaign only for a new or falsified capability.",
        "forbidden_actions": [
            "Rewrite existing application files as part of control-layer adoption.",
            "Treat adoption as production release authority.",
        ],
    }


def adopt_case(base: Path, case: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    profile = case["profile"]
    product_id = f"ADOPTION_{profile}"
    project = base / profile.lower()
    write_fixture(project, case["files"])
    before = application_snapshot(project)

    scaffold = run(
        str(SCAFFOLD),
        "--target",
        str(project),
        "--profile",
        profile,
        "--product-id",
        product_id,
        "--objective",
        f"Synthetic {profile} adoption target.",
    )
    if scaffold.returncode != 0:
        raise AssertionError(
            f"{profile}: scaffold failed\n{scaffold.stdout}\n{scaffold.stderr}"
        )

    control = project / ".agentic-sdlc"
    discover = control / "tools" / "discover_project.py"
    inventory_path = control / "discovery" / "PROJECT_INVENTORY.json"
    discovery = run(
        str(discover),
        "--project-root",
        str(project),
        "--output",
        str(inventory_path),
    )
    if discovery.returncode != 0:
        raise AssertionError(
            f"{profile}: discovery failed\n{discovery.stdout}\n{discovery.stderr}"
        )
    first_inventory = inventory_path.read_bytes()

    discovery_repeat = run(
        str(discover),
        "--project-root",
        str(project),
        "--output",
        str(inventory_path),
    )
    if discovery_repeat.returncode != 0:
        raise AssertionError(f"{profile}: repeated discovery failed")
    if inventory_path.read_bytes() != first_inventory:
        raise AssertionError(f"{profile}: project inventory is not deterministic")

    inventory = json.loads(first_inventory)
    if inventory["file_count"] != len(before):
        raise AssertionError(
            f"{profile}: discovery counted control/generated files as application files"
        )
    inventory_hash = hashlib.sha256(first_inventory).hexdigest()
    inventory_ref = "discovery/PROJECT_INVENTORY.json"
    spec = build_spec(case, product_id, inventory_ref, inventory_hash)
    spec_path = control / "adoption" / "ADOPTION_SPEC.json"
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")

    apply_tool = control / "tools" / "apply_adoption.py"
    adoption = run(
        str(apply_tool),
        "--control-root",
        str(control),
        "--spec",
        str(spec_path),
    )
    if adoption.returncode != 0:
        raise AssertionError(
            f"{profile}: adoption failed\n{adoption.stdout}\n{adoption.stderr}"
        )
    report = json.loads(adoption.stdout)
    if report["status"] != "ADOPTED":
        raise AssertionError(f"{profile}: unexpected adoption status {report['status']}")

    product_state_path = control / "state" / "PRODUCT_STATE_CURRENT.json"
    product_state_before_retry = product_state_path.read_bytes()
    retry = run(
        str(apply_tool),
        "--control-root",
        str(control),
        "--spec",
        str(spec_path),
    )
    if retry.returncode != 0:
        raise AssertionError(
            f"{profile}: idempotent adoption retry failed\n"
            + retry.stdout
            + "\n"
            + retry.stderr
        )
    retry_report = json.loads(retry.stdout)
    if retry_report["status"] != "ALREADY_ADOPTED":
        raise AssertionError(
            f"{profile}: adoption retry returned {retry_report['status']!r}"
        )
    if product_state_path.read_bytes() != product_state_before_retry:
        raise AssertionError(f"{profile}: idempotent adoption retry rewrote Product State")

    validator = control / "tools" / "validate_project.py"
    validation = run(str(validator), "--root", str(control))
    if validation.returncode != 0:
        raise AssertionError(
            f"{profile}: adopted control failed validation\n"
            + validation.stdout
            + "\n"
            + validation.stderr
        )

    reconstruct = control / "tools" / "reconstruct_context.py"
    reconstructed_run = run(str(reconstruct), "--root", str(control))
    if reconstructed_run.returncode != 0:
        raise AssertionError(
            f"{profile}: adopted reconstruction failed\n"
            + reconstructed_run.stdout
            + "\n"
            + reconstructed_run.stderr
        )
    reconstructed = json.loads(reconstructed_run.stdout)
    if reconstructed["posture"] != "RECONSTRUCTED_NO_ACTIVE_EXECUTION":
        raise AssertionError(
            f"{profile}: wrong adopted posture {reconstructed['posture']}"
        )
    if reconstructed["currentness"]["verified"] is not True:
        raise AssertionError(f"{profile}: adoption did not verify currentness")
    if reconstructed["product_state"]["current_code_ref"] != spec["current_code_ref"]:
        raise AssertionError(f"{profile}: current code ref drift after adoption")

    after = application_snapshot(project)
    if after != before:
        raise AssertionError(f"{profile}: adoption mutated original application files")

    return control, spec


def assert_profile_burden(control: Path, profile: str) -> None:
    protocols = {path.name for path in (control / "protocols").glob("*.md")}
    has_runtime = (control / "tools" / "campaignctl.py").exists()

    if profile == "SMALL":
        if "MASTER_OWNER_OS.md" in protocols:
            raise AssertionError("SMALL adoption installed MASTER OWNER")
        if "STATE_DB_LINEAGE_AND_IDEMPOTENCY.md" in protocols:
            raise AssertionError("SMALL adoption installed stateful protocol")
        if has_runtime:
            raise AssertionError("SMALL adoption installed runtime without opt-in")
    elif profile == "STATEFUL":
        if "STATE_DB_LINEAGE_AND_IDEMPOTENCY.md" not in protocols:
            raise AssertionError("STATEFUL adoption missing state/lineage protocol")
    elif profile == "ARTIFACT_HEAVY":
        for required in {
            "STORAGE_AND_ARTIFACT_LIFECYCLE.md",
            "COST_CAPACITY_AND_EXTERNAL_SERVICES.md",
        }:
            if required not in protocols:
                raise AssertionError(f"ARTIFACT_HEAVY adoption missing {required}")
    elif profile == "MULTI_PRODUCT":
        if "MASTER_OWNER_OS.md" not in protocols:
            raise AssertionError("MULTI_PRODUCT adoption missing MASTER OWNER")
    elif profile == "HIGH_CONSEQUENCE":
        if "SECURITY_PRIVACY_RIGHTS_AND_EXTERNAL_ACTIONS.md" not in protocols:
            raise AssertionError("HIGH_CONSEQUENCE adoption missing security/rights protocol")


def crash_recovery_probe(base: Path) -> None:
    case = next(item for item in profile_cases() if item["profile"] == "STATEFUL")
    project = base / "crash_recovery"
    write_fixture(project, case["files"])
    scaffold = run(
        str(SCAFFOLD),
        "--target",
        str(project),
        "--profile",
        "STATEFUL",
        "--product-id",
        "ADOPTION_CRASH_RECOVERY",
        "--objective",
        "Synthetic crash-recovery adoption target.",
    )
    if scaffold.returncode != 0:
        raise AssertionError("crash fixture scaffold failed")
    control = project / ".agentic-sdlc"
    inventory_path = control / "discovery" / "PROJECT_INVENTORY.json"
    discover = run(
        str(control / "tools" / "discover_project.py"),
        "--project-root",
        str(project),
        "--output",
        str(inventory_path),
    )
    if discover.returncode != 0:
        raise AssertionError("crash fixture discovery failed")
    inventory_bytes = inventory_path.read_bytes()
    spec = build_spec(
        case,
        "ADOPTION_CRASH_RECOVERY",
        "discovery/PROJECT_INVENTORY.json",
        hashlib.sha256(inventory_bytes).hexdigest(),
    )
    spec_path = control / "adoption" / "ADOPTION_SPEC.json"
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")

    env = os.environ.copy()
    env["AGENTIC_SDLC_TX_CRASH_AFTER_APPLY"] = "2"
    crashed = run(
        str(control / "tools" / "apply_adoption.py"),
        "--control-root",
        str(control),
        "--spec",
        str(spec_path),
        env=env,
    )
    if crashed.returncode != 92:
        raise AssertionError(
            "adoption fault injection did not terminate after two canonical writes\n"
            + crashed.stdout
            + "\n"
            + crashed.stderr
        )

    reconstruct_before = run(
        str(control / "tools" / "reconstruct_context.py"),
        "--root",
        str(control),
    )
    if reconstruct_before.returncode == 0:
        raise AssertionError("reconstruction accepted a partially committed adoption")

    recovery = run(
        str(control / "tools" / "state_tx.py"),
        "--control-root",
        str(control),
        "recover",
    )
    if recovery.returncode != 0:
        raise AssertionError(
            "generic adoption recovery failed\n" + recovery.stdout + recovery.stderr
        )

    reconstruct_after = run(
        str(control / "tools" / "reconstruct_context.py"),
        "--root",
        str(control),
    )
    if reconstruct_after.returncode != 0:
        raise AssertionError(
            "reconstruction failed after generic adoption recovery\n"
            + reconstruct_after.stdout
            + reconstruct_after.stderr
        )
    if json.loads(reconstruct_after.stdout)["posture"] != "RECONSTRUCTED_NO_ACTIVE_EXECUTION":
        raise AssertionError("recovered adoption has wrong posture")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="agentic-sdlc-adoption-") as tmp:
        base = Path(tmp)
        for case in profile_cases():
            control, _ = adopt_case(base, case)
            assert_profile_burden(control, case["profile"])

        crash_recovery_probe(base)

    print("TRANSFER / ADOPTION SELF-TEST PASSED")
    print("- six unrelated project shapes scaffolded without application mutation")
    print("- discovery inventory deterministic and excludes control state")
    print("- explicit adoption spec promoted currentness transactionally")
    print("- repeated adoption is validation-only and idempotent")
    print("- all adopted projects validate and reconstruct without active execution")
    print("- SMALL remains minimal")
    print("- stateful/artifact/multi/high-consequence profiles retain required mechanisms")
    print("- adoption crash recovered through generic state transaction journal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
