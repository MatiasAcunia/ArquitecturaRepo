#!/usr/bin/env python3
"""Malformed/stale CLIENT theory surfaces must HOLD without uncaught crashes."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from theory_guard import check


def main():
    with tempfile.TemporaryDirectory(prefix="theory-hardening-") as tmp:
        control=Path(tmp)
        (control/"state").mkdir()
        (control/"governance").mkdir()
        requirements=control/"state"/"CLIENT_REQUIREMENTS_CURRENT.md"
        product=control/"state"/"PRODUCT_STATE_CURRENT.json"
        bootstrap=control/"state"/"CURRENT_BOOTSTRAP_STATE.json"
        overlay=control/"governance"/"PROJECT_OVERLAY.md"
        requirements.write_text("CLIENT confirmation: PENDING\nBaseline status: DRAFT\nTO_BE_DISCOVERED\n")
        product.write_text(json.dumps({"status":"ACTIVE"}))
        bootstrap.write_text(json.dumps({"status":"READY","currentness":{"verified":True}}))
        overlay.write_text("Authoritative long-enough test overlay with owner.")
        base=check(control)
        assert base["status"]=="HOLD"
        assert "CLIENT_THEORY_UNCONFIRMED" in base["failure_codes"]
        assert "CLIENT_REQUIREMENTS_STILL_PLACEHOLDERS" in base["failure_codes"]
        bootstrap.write_text(json.dumps({"status":"READY","currentness":"CORRUPT"}))
        malformed=check(control)
        assert malformed["status"]=="HOLD"
        assert "CURRENTNESS_CONTRACT_MALFORMED" in malformed["failure_codes"]
        bootstrap.write_text("[]")
        non_object=check(control)
        assert non_object["status"]=="HOLD"
        assert any(c.startswith("CANONICAL_READ_FAILURE") for c in non_object["failure_codes"])
        bootstrap.write_text(json.dumps({"status":"READY","currentness":{"verified":True}}))
        requirements.write_text("# Requirements\nCLIENT confirmation: CONFIRMED\nFunctional: product catalog, inventory and sales\n")
        clean=check(control)
        assert clean["status"]=="CANONICAL_SURFACES_STRUCTURALLY_READY"
        assert clean["may_authorize_campaign"] is False
        assert clean["semantic_consistency"]=="NOT_AUTOMATICALLY_CERTIFIED"
        product.write_text("INVALID_JSON")
        fail=check(control)
        assert fail["status"]=="HOLD"
    print("THEORY FAIL-CLOSED SELFTEST PASSED")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
