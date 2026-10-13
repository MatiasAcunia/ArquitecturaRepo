#!/usr/bin/env python3
"""Synthetic adversarial tests for v1.2 controls; NOT a physical host gate."""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path

from goal_guard import assess, digest
from goal_plan import update, TacticalPlanError
from external_effects import transition, ExternalEffectHold, sha
from owner_task_recovery import recovery_actions, ROLES
from cognitive_i4 import due_check, consult_public_or_synthetic, CognitiveHold


def must_fail(fn, expected: type[Exception]) -> None:
    try:
        fn()
    except expected:
        return
    raise AssertionError("Expected " + expected.__name__)


def test_goal(tmp: Path) -> None:
    tmp.mkdir(parents=True, exist_ok=True)
    assert assess(tmp)["status"] == "NOT_CONFIGURED"
    (tmp / "state").mkdir()
    (tmp / "runtime").mkdir()
    charter = tmp / "state" / "CHARTER.md"
    charter.write_text("authorized charter\n")
    charter_sha = hashlib.sha256(charter.read_bytes()).hexdigest()
    goal = {
        "schema_version": "agentic-goal-contract-v1",
        "goal_id": "G1", "campaign_id": "C1",
        "charter_ref": "state/CHARTER.md", "charter_sha256": charter_sha,
        "authority_refs": {"state/CHARTER.md": charter_sha},
        "definition_of_done": "Prove a complete feature.",
        "hard_gates": ["EXACT_CANDIDATE_REVIEW"],
        "forbidden_effects": ["UNAUTHORIZED_PUBLICATION"],
        "write_envelope": ["src"],
    }
    (tmp / "state" / "GOAL_CONTRACT_CURRENT.json").write_text(json.dumps(goal))
    assert assess(tmp)["status"] == "HOLD"
    plan = update(tmp, expected_revision=-1, plan={"steps": [{"id": "A", "status": "READY"}]},
                  active_minutes=0, review_evidence_ref="synthetic-evidence")
    assert plan["goal_digest"] == digest(goal)
    assert assess(tmp)["status"] == "HOLD"
    good = assess(tmp, host_currentness_verified=True, host_invocation_binding_verified=True)
    assert good["status"] == "PASS"
    must_fail(lambda: update(tmp, expected_revision=-1, plan={"steps": []},
                             active_minutes=0, review_evidence_ref="e"), TacticalPlanError)
    charter.write_text("changed charter")
    bad = assess(tmp, host_currentness_verified=True, host_invocation_binding_verified=True)
    assert "AUTHORITY_REF_STALE" in bad["failure_codes"]
    charter.write_text("authorized charter\n")
    (tmp / "state" / "canonical.sqlite").write_bytes(b"sqlite")
    goal["canonical_store"] = {"required": True, "ref": "state/canonical.sqlite",
                               "sha256": hashlib.sha256(b"sqlite").hexdigest()}
    (tmp / "state" / "GOAL_CONTRACT_CURRENT.json").write_text(json.dumps(goal))
    assert "TACTICAL_PLAN_GOAL_DRIFT" in assess(tmp, host_currentness_verified=True,
                                                host_invocation_binding_verified=True)["failure_codes"]
    # New canonical goal needs formal reconciliation; plan update must not silently self-rebind.
    must_fail(lambda: update(tmp, expected_revision=0, plan={"steps": []}, active_minutes=0,
                             review_evidence_ref="e"), TacticalPlanError)


def test_effect(tmp: Path) -> None:
    request = {"kind": "SYNTHETIC_REMOTE", "object": "fixture"}
    a = transition(tmp, "E1", "PREPARE", request=request, authorized_ref="approved-charter")
    assert a["phase"] == "PREPARED"
    assert transition(tmp, "E1", "PREPARE", request=request,
                      authorized_ref="approved-charter") == a
    must_fail(lambda: transition(tmp, "E1", "PREPARE", request={"kind": "different"},
                                 authorized_ref="approved-charter"), ExternalEffectHold)
    b = transition(tmp, "E1", "ATTEMPT")
    assert b["phase"] == "REQUESTED_AMBIGUOUS"
    must_fail(lambda: transition(tmp, "E1", "ATTEMPT"), ExternalEffectHold)
    transition(tmp, "E1", "HOLD")
    must_fail(lambda: transition(tmp, "E1", "RECEIPT", proof={"readback_verified": True}),
              ExternalEffectHold)
    receipt = {"request_sha256": sha(request), "readback_verified": True,
               "external_receipt_sha256": "a" * 64}
    c = transition(tmp, "E1", "RECEIPT", proof=receipt)
    assert c["phase"] == "RECEIPT_VERIFIED"
    must_fail(lambda: transition(tmp, "E1", "ATTEMPT"), ExternalEffectHold)


def test_owner_pack() -> None:
    rows = [{"role": role, "id": "T" + str(i), "is_enabled": False}
            for i, role in enumerate(ROLES)]
    rows[2]["suspension_source"] = "CLIENT"
    actions = recovery_actions(rows, subject_role="Architecture")
    assert {item["id"] for item in actions["actions"]} == {"T0", "T3", "T4"}
    assert actions["actual_recovery_verified"] is False
    must_fail(lambda: recovery_actions(rows[:-1], subject_role="Architecture"), ValueError)


def test_cognitive() -> None:
    assert due_check(material_entry=False, evidence_changed=False, repeated_failures=0,
                     active_minutes_since_review=119, quota_verified=True,
                     export_authorized=True)["status"] == "NOT_DUE"
    assert due_check(material_entry=False, evidence_changed=True, repeated_failures=0,
                     active_minutes_since_review=None, quota_verified=True,
                     export_authorized=False)["status"] == "SKIPPED_PRIVACY"
    assert due_check(material_entry=True, evidence_changed=False, repeated_failures=0,
                     active_minutes_since_review=None, quota_verified=True,
                     export_authorized=True)["status"] == "DUE"
    must_fail(lambda: consult_public_or_synthetic(model="test", question="private bytes here",
                export_classification="PRIVATE"), CognitiveHold)

    class Response:
        status = 200
        def __enter__(self): return self
        def __exit__(self, *_): return None
        def read(self, _): return json.dumps({"candidates": [{"content": {
            "parts": [{"text": json.dumps({"recommendation": "test hypothesis"})}]}}]}).encode()

    prior = os.environ.get("GEMINI_API_KEY")
    try:
        os.environ["GEMINI_API_KEY"] = "synthetic-test-only"
        out = consult_public_or_synthetic(model="test-model", question="Review this public synthetic plan.",
                                         export_classification="PUBLIC_OR_SYNTHETIC",
                                         transport=lambda request, timeout: Response())
        assert out["status"] == "DELIVERY_PENDING"
        assert out["consumed_by_i3"] is False
    finally:
        if prior is None:
            os.environ.pop("GEMINI_API_KEY", None)
        else:
            os.environ["GEMINI_API_KEY"] = prior


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="operational-v12-") as tmp:
        root = Path(tmp)
        test_goal(root / "goal")
        test_effect(root / "effect")
        test_owner_pack()
        test_cognitive()
    print("OPERATIONAL V1.2 SYNTHETIC SELF-TEST PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
