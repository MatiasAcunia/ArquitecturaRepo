#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD = ROOT / "tools" / "scaffold_project.py"
VALIDATOR = ROOT / "tools" / "validate_project.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def validate(control: Path) -> subprocess.CompletedProcess[str]:
    return run(str(VALIDATOR), "--root", str(control))


def must_validate(control: Path, label: str) -> None:
    result = validate(control)
    if result.returncode != 0:
        raise AssertionError(
            f"{label}: expected validation success\n{result.stdout}\n{result.stderr}"
        )


def must_reject(control: Path, label: str, fragment: str) -> None:
    result = validate(control)
    combined = result.stdout + "\n" + result.stderr
    if result.returncode == 0:
        raise AssertionError(f"{label}: validator unexpectedly passed")
    if fragment not in combined:
        raise AssertionError(
            f"{label}: expected {fragment!r}\nvalidator output:\n{combined}"
        )


def clone(source: Path, destination: Path) -> Path:
    shutil.copytree(source, destination)
    return destination


def owner(registry: dict, concern: str) -> dict:
    matches = [
        item
        for item in registry["owners"]
        if item["concern_id"] == concern and item["status"] == "CURRENT"
    ]
    if len(matches) != 1:
        raise AssertionError(f"fixture concern {concern} does not have one current owner")
    return matches[0]


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="agentic-sdlc-ownership-") as tmp:
        base = Path(tmp)
        project = base / "baseline_project"
        scaffold = run(
            str(SCAFFOLD),
            "--target",
            str(project),
            "--profile",
            "SMALL",
            "--product-id",
            "EXAMPLE_OWNER_PRODUCT",
            "--objective",
            "Synthetic product for canonical-owner validation.",
        )
        if scaffold.returncode != 0:
            raise AssertionError(
                "baseline scaffold failed\n"
                + scaffold.stdout
                + "\n"
                + scaffold.stderr
            )

        baseline = project / ".agentic-sdlc"
        must_validate(baseline, "baseline owner registry")

        registry_path = baseline / "state" / "OWNER_REGISTRY_CURRENT.json"
        registry = load(registry_path)
        if registry["schema_version"] != "owner-registry-0.1":
            raise AssertionError("scaffold did not emit owner-registry-0.1")
        concerns = {item["concern_id"] for item in registry["owners"]}
        required = {
            "AGENT_ENTRYPOINT",
            "CLIENT_REQUIREMENTS",
            "PRODUCT_STATE",
            "CURRENT_BOOTSTRAP",
            "PROJECT_OVERLAY",
            "CANONICAL_OWNER_REGISTRY",
        }
        if not required.issubset(concerns):
            raise AssertionError(
                f"baseline owner registry missing concerns: {sorted(required - concerns)}"
            )

        duplicate = clone(baseline, base / "duplicate_current")
        duplicate_registry_path = duplicate / "state" / "OWNER_REGISTRY_CURRENT.json"
        duplicate_registry = load(duplicate_registry_path)
        second = dict(owner(duplicate_registry, "CLIENT_REQUIREMENTS"))
        second["owner_id"] = "OWNER_CLIENT_REQUIREMENTS_002"
        duplicate_registry["owners"].append(second)
        save(duplicate_registry_path, duplicate_registry)
        must_reject(
            duplicate,
            "duplicate current owner",
            "must have exactly one CURRENT owner; found 2",
        )

        missing_currentness = clone(baseline, base / "missing_currentness")
        product_path = missing_currentness / "state" / "PRODUCT_STATE_CURRENT.json"
        product = load(product_path)
        product["currentness_set"].remove("state/OWNER_REGISTRY_CURRENT.json")
        save(product_path, product)
        must_reject(
            missing_currentness,
            "owner missing from currentness set",
            "is required in Product State Currentness Set but is absent",
        )

        dangling = clone(baseline, base / "dangling_supersession")
        dangling_path = dangling / "state" / "OWNER_REGISTRY_CURRENT.json"
        dangling_registry = load(dangling_path)
        old = {
            "owner_id": "OWNER_OLD_CUSTOM_001",
            "concern_id": "CUSTOM_CONCERN",
            "scope": "EXAMPLE_OWNER_PRODUCT",
            "status": "SUPERSEDED",
            "surface_ref": "legacy/custom.json",
            "surface_type": "FILE",
            "required_in_currentness_set": False,
            "supersedes_owner_ids": [],
            "superseded_by_owner_id": "OWNER_DOES_NOT_EXIST",
        }
        current = {
            "owner_id": "OWNER_CURRENT_CUSTOM_001",
            "concern_id": "CUSTOM_CONCERN",
            "scope": "EXAMPLE_OWNER_PRODUCT",
            "status": "CURRENT",
            "surface_ref": "state/PRODUCT_STATE_CURRENT.json",
            "surface_type": "FILE",
            "required_in_currentness_set": False,
            "supersedes_owner_ids": [],
            "superseded_by_owner_id": None,
        }
        dangling_registry["owners"].extend([old, current])
        save(dangling_path, dangling_registry)
        must_reject(
            dangling,
            "dangling supersession",
            "points to unknown successor",
        )

        cycle = clone(baseline, base / "cycle")
        cycle_path = cycle / "state" / "OWNER_REGISTRY_CURRENT.json"
        cycle_registry = load(cycle_path)
        cycle_registry["owners"].extend(
            [
                {
                    "owner_id": "OWNER_CYCLE_CURRENT",
                    "concern_id": "CYCLE_CONCERN",
                    "scope": "EXAMPLE_OWNER_PRODUCT",
                    "status": "CURRENT",
                    "surface_ref": "state/PRODUCT_STATE_CURRENT.json",
                    "surface_type": "FILE",
                    "required_in_currentness_set": False,
                    "supersedes_owner_ids": [],
                    "superseded_by_owner_id": None,
                },
                {
                    "owner_id": "OWNER_CYCLE_A",
                    "concern_id": "CYCLE_CONCERN",
                    "scope": "EXAMPLE_OWNER_PRODUCT",
                    "status": "SUPERSEDED",
                    "surface_ref": "legacy/a.json",
                    "surface_type": "FILE",
                    "required_in_currentness_set": False,
                    "supersedes_owner_ids": ["OWNER_CYCLE_B"],
                    "superseded_by_owner_id": "OWNER_CYCLE_B",
                },
                {
                    "owner_id": "OWNER_CYCLE_B",
                    "concern_id": "CYCLE_CONCERN",
                    "scope": "EXAMPLE_OWNER_PRODUCT",
                    "status": "SUPERSEDED",
                    "surface_ref": "legacy/b.json",
                    "surface_type": "FILE",
                    "required_in_currentness_set": False,
                    "supersedes_owner_ids": ["OWNER_CYCLE_A"],
                    "superseded_by_owner_id": "OWNER_CYCLE_A",
                },
            ]
        )
        save(cycle_path, cycle_registry)
        must_reject(cycle, "supersession cycle", "supersession cycle detected")

        valid = clone(baseline, base / "valid_supersession")
        valid_registry_path = valid / "state" / "OWNER_REGISTRY_CURRENT.json"
        valid_registry = load(valid_registry_path)
        old_owner = owner(valid_registry, "CLIENT_REQUIREMENTS")
        old_owner["status"] = "SUPERSEDED"
        old_owner["required_in_currentness_set"] = False
        old_owner["superseded_by_owner_id"] = "OWNER_CLIENT_REQUIREMENTS_002"

        new_requirements_ref = "state/CLIENT_REQUIREMENTS_V2.md"
        (valid / new_requirements_ref).write_text(
            "# CLIENT Requirements — CURRENT\n\nSynthetic successor requirements owner.\n",
            encoding="utf-8",
        )
        valid_registry["owners"].append(
            {
                "owner_id": "OWNER_CLIENT_REQUIREMENTS_002",
                "concern_id": "CLIENT_REQUIREMENTS",
                "scope": "EXAMPLE_OWNER_PRODUCT",
                "status": "CURRENT",
                "surface_ref": new_requirements_ref,
                "surface_type": "FILE",
                "required_in_currentness_set": True,
                "supersedes_owner_ids": [old_owner["owner_id"]],
                "superseded_by_owner_id": None,
            }
        )
        save(valid_registry_path, valid_registry)

        valid_product_path = valid / "state" / "PRODUCT_STATE_CURRENT.json"
        valid_product = load(valid_product_path)
        valid_product["currentness_set"] = [
            new_requirements_ref if ref == "state/CLIENT_REQUIREMENTS_CURRENT.md" else ref
            for ref in valid_product["currentness_set"]
        ]
        save(valid_product_path, valid_product)

        valid_bootstrap_path = valid / "state" / "CURRENT_BOOTSTRAP_STATE.json"
        valid_bootstrap = load(valid_bootstrap_path)
        valid_bootstrap["requirements_ref"] = new_requirements_ref
        valid_bootstrap["currentness"]["source_refs"] = [
            new_requirements_ref
            if ref == "state/CLIENT_REQUIREMENTS_CURRENT.md"
            else ref
            for ref in valid_bootstrap["currentness"]["source_refs"]
        ]
        save(valid_bootstrap_path, valid_bootstrap)
        must_validate(valid, "valid requirements-owner supersession")

        cross = clone(valid, base / "cross_concern")
        cross_path = cross / "state" / "OWNER_REGISTRY_CURRENT.json"
        cross_registry = load(cross_path)
        product_owner = owner(cross_registry, "PRODUCT_STATE")
        requirements_old = next(
            item
            for item in cross_registry["owners"]
            if item["owner_id"] == "OWNER_CLIENT_REQUIREMENTS_001"
        )
        product_owner["supersedes_owner_ids"].append(requirements_old["owner_id"])
        requirements_old["superseded_by_owner_id"] = product_owner["owner_id"]
        save(cross_path, cross_registry)
        must_reject(
            cross,
            "cross-concern supersession",
            "from a different concern",
        )

    print("OWNER REGISTRY SELF-TEST PASSED")
    print("- generated core owner graph validates")
    print("- duplicate CURRENT owner rejected")
    print("- required owner missing from Currentness Set rejected")
    print("- dangling successor rejected")
    print("- supersession cycle rejected")
    print("- valid owner supersession accepted")
    print("- cross-concern supersession rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
