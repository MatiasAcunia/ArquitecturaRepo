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
    good = assess(tmp)
    assert good["local_integrity_passed"] is True
    assert good["may_execute_material_goal"] is False
    assert "HOST_INVOCATION_HOOK_NOT_PROVEN" in good["failure_codes"]
    must_fail(lambda: update(tmp, expected_revision=-1, plan={"steps": []},
                             active_minutes=0, review_evidence_ref="e"), TacticalPlanError)
    charter.write_text("changed charter")
    bad = assess(tmp)
    assert "AUTHORITY_REF_STALE" in bad["failure_codes"]
    charter.write_text("authorized charter\n")
    (tmp / "state" / "canonical.sqlite").write_bytes(b"sqlite")
    goal["canonical_store"] = {"required": True, "ref": "state/canonical.sqlite",
                               "sha256": hashlib.sha256(b"sqlite").hexdigest()}
    (tmp / "state" / "GOAL_CONTRACT_CURRENT.json").write_text(json.dumps(goal))
    assert "TACTICAL_PLAN_GOAL_DRIFT" in assess(tmp)["failure_codes"]
    # Traversal and symlinks never become authorized control refs.
    goal["authority_refs"] = {"../outside": "a" * 64}
    goal["charter_ref"] = "../outside"
    goal["charter_sha256"] = "a" * 64
    (tmp / "state" / "GOAL_CONTRACT_CURRENT.json").write_text(json.dumps(goal))
    assert any("UNTRUSTED_GOAL" in c for c in assess(tmp)["failure_codes"])
    goal["authority_refs"] = {"state/CHARTER.md": charter_sha}
    goal["charter_ref"] = "state/CHARTER.md"
    goal["charter_sha256"] = charter_sha
    (tmp / "state" / "GOAL_CONTRACT_CURRENT.json").write_text(json.dumps(goal))
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
    assert c["phase"] == "RECEIPT_ATTESTED_UNVERIFIED"
    assert "verified_receipt" not in c
    must_fail(lambda: transition(tmp, "E1", "ATTEMPT"), ExternalEffectHold)


def test_owner_pack() -> None:
    rows = [{"role": role, "id": "T" + str(i), "is_enabled": False}
            for i, role in enumerate(ROLES)]
    rows[2]["suspension_source"] = "CLIENT"
    unknown = recovery_actions(rows, subject_role="Architecture")
    assert unknown["actions"] == []
    assert unknown["client_suspension_authority_verified"] is False
    actions = recovery_actions(rows, subject_role="Architecture", client_disabled=set())
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
    prior_enabled = os.environ.get("AGENTIC_SDLC_GEMINI_ENABLED")
    try:
        os.environ["GEMINI_API_KEY"] = "synthetic-test-only"
        must_fail(lambda: consult_public_or_synthetic(
            model="test-model", question="Review this public synthetic plan.",
            export_classification="PUBLIC_OR_SYNTHETIC"), CognitiveHold)
        os.environ["AGENTIC_SDLC_GEMINI_ENABLED"] = "true"
        must_fail(lambda: consult_public_or_synthetic(
            model="../evil", question="Review this public synthetic plan.",
            export_classification="PUBLIC_OR_SYNTHETIC"), CognitiveHold)
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
        if prior_enabled is None:
            os.environ.pop("AGENTIC_SDLC_GEMINI_ENABLED", None)
        else:
            os.environ["AGENTIC_SDLC_GEMINI_ENABLED"] = prior_enabled



def test_fencing_and_decision(tmp: Path) -> None:
    from fenced_mutator import fenced_local_write, StaleMutatorHold
    from evidence_decision import bind_candidate, review, EvidenceHold

    (tmp / "state").mkdir(parents=True, exist_ok=True)
    authority = {
        "schema_version": "execution-authority-0.1",
        "authority_status": "ACTIVE",
        "mutator_epoch": 9,
        "current_mutator": {"actor_id": "I3", "run_id": "RUN9", "epoch": 9},
    }
    path = tmp / "state" / "EXECUTION_AUTHORITY_CURRENT.json"
    path.write_text(json.dumps(authority))
    with fenced_local_write(tmp, actor_id="I3", run_id="RUN9", mutator_epoch=9):
        assert path.is_file()
    def stale_run() -> None:
        with fenced_local_write(tmp, actor_id="I3", run_id="RUN8", mutator_epoch=8):
            raise AssertionError("Stale run was improperly authorized")
    must_fail(stale_run, StaleMutatorHold)
    authority["current_mutator"] = None
    path.write_text(json.dumps(authority))
    def revoked() -> None:
        with fenced_local_write(tmp, actor_id="I3", run_id="RUN9", mutator_epoch=9):
            raise AssertionError("Revoked authority was improperly authorized")
    must_fail(revoked, StaleMutatorHold)
    candidate = bind_candidate(source_hashes={"source": "a" * 64},
                               payload={"decision": "example"}, author_actor="I3")
    must_fail(lambda: review(candidate, reviewer_actor="I3",
              original_sources={"source": "a" * 64}, review_result="HOLD",
              falsifier_refs=[]), EvidenceHold)
    must_fail(lambda: review(candidate, reviewer_actor="I4",
              original_sources={"source": "b" * 64}, review_result="HOLD",
              falsifier_refs=[]), EvidenceHold)
    critique = review(candidate, reviewer_actor="I4",
                      original_sources={"source": "a" * 64},
                      review_result="SUPPORTED_FOR_FURTHER_GATE", falsifier_refs=["test-1"])
    assert critique["product_acceptance"] == "NOT_CLAIMED"



def test_consultation_ledger(tmp: Path) -> None:
    from cognitive_ledger import register, advance, ConsultationHold
    kw = {"consultation_id": "C001", "campaign_id": "CAMPAIGN",
          "source_digest": "a" * 64, "question_digest": "b" * 64,
          "model": "synthetic", "export_classification": "PUBLIC_OR_SYNTHETIC"}
    row = register(tmp, **kw)
    assert register(tmp, **kw) == row
    must_fail(lambda: register(tmp, **{**kw, "source_digest": "c" * 64}), ConsultationHold)
    must_fail(lambda: advance(tmp, "C001", "REQUEST", current_source_digest="a" * 64),
              ConsultationHold)
    assert advance(tmp, "C001", "CLAIM", current_source_digest="a" * 64)["phase"] == "CLAIMED"
    assert advance(tmp, "C001", "REQUEST", current_source_digest="a" * 64)["network_attempt_count"] == 1
    must_fail(lambda: advance(tmp, "C001", "REQUEST", current_source_digest="a" * 64),
              ConsultationHold)
    must_fail(lambda: advance(tmp, "C001", "RESPONSE", current_source_digest="c" * 64,
                              response_sha256="d" * 64), ConsultationHold)
    advance(tmp, "C001", "RESPONSE", current_source_digest="a" * 64, response_sha256="d" * 64)
    advance(tmp, "C001", "DELIVER", current_source_digest="a" * 64,
            evidence_ref="host/receipt.json")
    must_fail(lambda: advance(tmp, "C001", "ADOPT", current_source_digest="a" * 64,
                              evidence_ref="test"), ConsultationHold)
    advance(tmp, "C001", "CONSUME", current_source_digest="a" * 64,
            evidence_ref="host/later-i3-event.json")
    result = advance(tmp, "C001", "ADOPT", current_source_digest="a" * 64,
                     evidence_ref="tests/causal-proof.json")
    assert result["phase"] == "ADOPTED_PENDING_GATE"



def test_new_schemas(root: Path) -> None:
    from jsonschema import Draft202012Validator
    schema_root = Path(__file__).resolve().parents[1] / "schemas"
    pairs = (
        (schema_root / "goal-contract.schema.json", root / "goal/state/GOAL_CONTRACT_CURRENT.json"),
        (schema_root / "tactical-plan.schema.json", root / "goal/runtime/TACTICAL_PLAN_CURRENT.json"),
        (schema_root / "external-effect.schema.json", root / "effect/runtime/external_effects/E1.json"),
        (schema_root / "cognitive-consultation.schema.json", root / "consultation/runtime/cognitive_i4/C001.json"),
    )
    for schema_path, sample_path in pairs:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        instance = json.loads(sample_path.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(instance)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="operational-v12-") as tmp:
        root = Path(tmp)
        test_goal(root / "goal")
        test_effect(root / "effect")
        test_fencing_and_decision(root / "fencing")
        test_consultation_ledger(root / "consultation")
        test_new_schemas(root)
        test_owner_pack()
        test_cognitive()
    print("OPERATIONAL V1.2 SYNTHETIC SELF-TEST PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
