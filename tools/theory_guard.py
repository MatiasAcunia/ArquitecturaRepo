#!/usr/bin/env python3
"""Read-only guard over EXISTING canonical CLIENT/Product State surfaces.

No duplicate current truth and no automatic rewrite of CLIENT words.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = (
    "state/CLIENT_REQUIREMENTS_CURRENT.md",
    "state/PRODUCT_STATE_CURRENT.json",
    "state/CURRENT_BOOTSTRAP_STATE.json",
    "governance/PROJECT_OVERLAY.md",
)
MAX_SOURCE_BYTES = 4 * 1024 * 1024


def check(control: Path) -> dict:
    control = control.resolve()
    failures: list[str] = []
    for relative in REQUIRED:
        path = control / relative
        if (not path.is_file() or path.is_symlink()
            or not path.resolve().is_relative_to(control)
            or path.stat().st_size == 0
            or path.stat().st_size > MAX_SOURCE_BYTES):
            failures.append("MISSING_OR_UNSAFE_CANONICAL_SURFACE:" + relative)
    if failures:
        return {"status": "HOLD", "failure_codes": failures,
                "may_authorize_campaign": False,
                "canonical_owner": list(REQUIRED)}
    try:
        product = json.loads((control / REQUIRED[1]).read_text(encoding="utf-8"))
        bootstrap = json.loads((control / REQUIRED[2]).read_text(encoding="utf-8"))
        requirements = (control / REQUIRED[0]).read_text(encoding="utf-8")
        overlay = (control / REQUIRED[3]).read_text(encoding="utf-8")
        if not isinstance(product, dict) or not isinstance(bootstrap, dict):
            raise ValueError("JSON_CANONICAL_OBJECT_REQUIRED")
        currentness = bootstrap.get("currentness")
        if not isinstance(currentness, dict):
            failures.append("CURRENTNESS_CONTRACT_MALFORMED")
            currentness = {}
        if product.get("status") in {None, "HOLD", "UNKNOWN"}:
            failures.append("PRODUCT_STATE_NOT_BASELINED")
        if bootstrap.get("status") == "UNTRUSTED_CONTEXT" or currentness.get("verified") is not True:
            failures.append("CURRENTNESS_OR_BOOTSTRAP_UNTRUSTED")
        if len(requirements.strip()) < 30 or len(overlay.strip()) < 30:
            failures.append("CANONICAL_THEORY_INCOMPLETE")
        if ("CLIENT confirmation: PENDING" in requirements or
            "Baseline status: DRAFT" in requirements):
            failures.append("CLIENT_THEORY_UNCONFIRMED")
        if "TO_BE_DISCOVERED" in requirements:
            failures.append("CLIENT_REQUIREMENTS_STILL_PLACEHOLDERS")
        # Presence of interaction evidence does not equal updated requirements;
        # there is no reliable semantic comparison without explicit reconciliation.
        # Interactions are evidence, never proof of L1 reconciliation.
        # No filesystem marker may certify CLIENT semantic acceptance.
        interactions = control / "interactions"
        evidence_present = interactions.is_dir() and any(
            f.suffix in {".json", ".md"} and f.name != "README.md"
            for f in interactions.iterdir() if f.is_file())
    except (OSError, TypeError, ValueError, KeyError) as exc:
        failures.append("CANONICAL_READ_FAILURE:" + type(exc).__name__)
        evidence_present = False
    return {
        "status": "HOLD" if failures else "CANONICAL_SURFACES_STRUCTURALLY_READY",
        "may_authorize_campaign": False,
        "failure_codes": sorted(failures),
        "material_interaction_evidence_present": evidence_present,
        "material_client_reconciliation": "REQUIRES_L0_TO_L1_EVIDENCE",
        "canonical_owner": list(REQUIRED),
        "semantic_consistency": "NOT_AUTOMATICALLY_CERTIFIED",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--control-root", type=Path, required=True)
    a = p.parse_args()
    result = check(a.control_root)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] != "HOLD" else 2


if __name__ == "__main__":
    raise SystemExit(main())
