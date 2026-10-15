#!/usr/bin/env python3
"""Validate published v1.2 documentation boundaries; not a runtime QA verdict."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def contains(path, terms):
    target = ROOT / path
    assert target.is_file(), f"MISSING_PUBLIC_DOCUMENT {path}"
    body = target.read_text(encoding="utf-8")
    for term in terms:
        assert term in body, f"MISSING_DOCUMENT_CONTRACT {path} {term}"
    return body


def main():
    gates = json.loads((ROOT / "state/V1_2_ACCEPTANCE_CRITERIA.json").read_text(encoding="utf-8"))
    assert gates["target_release"] == "1.2.0" and gates["gates"]

    contains("README.md", ("v1.2.0", "docs/README.md", "--force"))
    contains("docs/README.md", ("ordinary adopter", "PRIVATE", "M0", "M7"))
    contains("docs/23_OPERATIONAL_AGENTIC_SDLC_V1_2.md", ("v1.2.0", "portable"))
    contains("docs/24_OPERATIONAL_AGENTIC_SDLC_V1_2_ES.md", ("v1.2.0", "Proveedores y agentes"))
    contains("docs/25_V1_2_SECURITY_HARDENING_AUDIT.md", ("refuses --force",))

    historical_private = (
        "30_V1_2_STABILIZATION_MASTER_PLAN.md",
        "31_V1_2_L3_TERMINAL_INTAKE.md",
        "33_V12_CAPABILITY_TRUTH_AND_PORTFOLIO_ADOPTION_DESIGN.md",
        "35_ENGINEERING_FIRST_EXECUTION_MASTER_ROUTE.md",
        "36_CODEX_DAILY_CONTROL_202_NATIVE_INTEGRATION_GATE.md",
        "37_CODEX_DAILY_CONTROL_21_INTEGRATION.md",
    )
    for name in historical_private:
        assert not (ROOT / "docs" / name).exists(), f"PRIVATE_MAINTAINER_DOC_IN_PUBLIC_TREE {name}"
    print("V1.2 PUBLIC DOCUMENTATION BOUNDARY SELFTEST PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
