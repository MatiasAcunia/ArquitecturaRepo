#!/usr/bin/env python3
"""Three synthetic process boundaries. No provider calls, no actual host runtime.

This does NOT substitute for a real-world, multi-hour local L3 evaluation.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from branch_guard import assess as branch_assess
from project_setup import evaluate
from architecture_feedback import bounded_diagnostics


ROOT = Path(__file__).resolve().parents[1]


def invoke(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True,
                          text=True, check=False)


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for justification in ("EACH_TASK", "MODEL_SESSION", "RETRY", "TEST_FAILURE"):
        candidate = branch_assess(reason=justification, affected_surfaces=["src"],
                                  owner="I3", baseline_sha="a" * 40,
                                  isolation_or_rollback_ref="synthetic")
        assert candidate["status"] == "HOLD"
        assert candidate["may_create_branch"] is False
    justified = branch_assess(reason="RISK_EXPERIMENT", affected_surfaces=["src"],
                              owner="I3", baseline_sha="a" * 40,
                              isolation_or_rollback_ref="rollback/existing-proof")
    assert justified["isolation_candidate"] is True
    assert justified["may_create_branch"] is False

    observations = bounded_diagnostics({
        "event_log": [
            {"action": "AGENT_LOOP_DETECTED"},
            {"action": "AGENT_FABRICATED_GATE"},
            {"action": "CONFIG_INVALID"},
            {"action": "STALE_AUTHORITY"},
            {"action": "EXTERNAL_EFFECT_AMBIGUOUS"},
            {"action": "CUSTOMER_SECRET_TODO_DELETE"},
        ]
    })
    assert observations["erratic_agent_observations"] == 2
    assert observations["misconfiguration_observations"] == 1
    assert observations["stale_authority_observations"] == 1
    assert observations["ambiguous_external_effect_observations"] == 1
    assert "CUSTOMER_SECRET" not in json.dumps(observations)

    with tempfile.TemporaryDirectory(prefix="agentic-longitudinal-") as temp:
        target = Path(temp) / "throwaway-pilot"
        create = invoke(str(ROOT / "tools" / "scaffold_project.py"),
                        "--target", str(target), "--profile", "STATEFUL",
                        "--product-id", "SYNTHETIC_INVENTORY",
                        "--with-runtime", "--execution-mode", "SYNCHRONOUS")
        assert create.returncode == 0, create.stderr
        control = target / ".agentic-sdlc"
        prefs = read(control / "configuration" / "OPERATING_PREFERENCES.json")
        assert evaluate(prefs)["status"] == "CONFIGURATION_VALID_NOT_PRODUCT_ACCEPTANCE"
        assert not (control / "state" / "GOAL_CONTRACT_CURRENT.json").exists()

        # Invocation A: I2-authorized synthetic charter/Goal is only an
        # exact local specimen. No host-binding permission can be fabricated.
        charter = control / "state" / "SYNTHETIC_CHARTER.md"
        charter.write_text("Synthetic offline charter; no external authority.\n", encoding="utf-8")
        charter_hash = hashlib.sha256(charter.read_bytes()).hexdigest()
        goal = {
            "schema_version": "agentic-goal-contract-v1",
            "goal_id": "GOAL_SYNTHETIC", "campaign_id": "SAME_I3_CAMPAIGN",
            "charter_ref": "state/SYNTHETIC_CHARTER.md", "charter_sha256": charter_hash,
            "authority_refs": {"state/SYNTHETIC_CHARTER.md": charter_hash},
            "definition_of_done": "Synthetic continuity proof, no public output.",
            "hard_gates": ["EXACT_REVIEW"], "forbidden_effects": ["EXTERNAL_ACTION"],
            "write_envelope": ["runtime"],
        }
        (control / "state" / "GOAL_CONTRACT_CURRENT.json").write_text(
            json.dumps(goal), encoding="utf-8")
        plan_file = Path(temp) / "tactical-proposal.json"
        plan_file.write_text(json.dumps({"steps": [{"id": "A", "status": "READY"}]}),
                             encoding="utf-8")
        first = invoke(str(control / "tools" / "goal_plan.py"), "--control-root",
                       str(control), "--expected-revision", "-1", "--plan-file",
                       str(plan_file), "--active-minutes", "0",
                       "--review-evidence-ref", "synthetic/checkpoint0")
        assert first.returncode == 0, first.stdout + first.stderr
        assert read(control / "runtime" / "TACTICAL_PLAN_CURRENT.json")["revision"] == 0

        # Invocation B: a separate interpreter sees same durable identity.
        hold = invoke(str(control / "tools" / "goal_guard.py"),
                      "--control-root", str(control))
        assert hold.returncode == 2
        assert json.loads(hold.stdout)["may_execute_material_goal"] is False
        second = invoke(str(control / "tools" / "goal_plan.py"), "--control-root",
                        str(control), "--expected-revision", "0", "--plan-file",
                        str(plan_file), "--active-minutes", "40",
                        "--review-evidence-ref", "synthetic/checkpoint1")
        assert second.returncode == 0, second.stdout + second.stderr
        assert read(control / "runtime" / "TACTICAL_PLAN_CURRENT.json")["revision"] == 1
        conflict = invoke(str(control / "tools" / "goal_plan.py"), "--control-root",
                          str(control), "--expected-revision", "0", "--plan-file",
                          str(plan_file), "--active-minutes", "45",
                          "--review-evidence-ref", "synthetic/stale")
        assert conflict.returncode == 2

        # External effect crash simulation: mark the request before any
        # transport. Resume MUST refuse replay of ambiguous action.
        request_file = Path(temp) / "effect-request.json"
        request_file.write_text(json.dumps({"synthetic": "never-send"}), encoding="utf-8")
        prepared = invoke(str(control / "tools" / "external_effects.py"),
                          "--control-root", str(control),
                          "--effect-id", "SYNTHETIC1", "--event", "PREPARE",
                          "--request-file", str(request_file),
                          "--authorized-ref", "synthetic-charter")
        assert prepared.returncode == 0, prepared.stderr
        first_attempt = invoke(str(control / "tools" / "external_effects.py"),
                               "--control-root", str(control),
                               "--effect-id", "SYNTHETIC1", "--event", "ATTEMPT")
        assert first_attempt.returncode == 0, first_attempt.stderr
        replay = invoke(str(control / "tools" / "external_effects.py"),
                        "--control-root", str(control),
                        "--effect-id", "SYNTHETIC1", "--event", "ATTEMPT")
        assert replay.returncode == 2
        artifact = read(control / "runtime" / "external_effects" / "SYNTHETIC1.json")
        assert artifact["phase"] == "REQUESTED_AMBIGUOUS" and artifact["attempts"] == 1

        # Invocation C: changed charter makes old Goal locally stale;
        # no new plan may silently redefine the accepted product theory.
        charter.write_text("Synthetic changed charter invalidates authority.\n", encoding="utf-8")
        stale = invoke(str(control / "tools" / "goal_guard.py"),
                       "--control-root", str(control))
        assert stale.returncode == 2
        assert "AUTHORITY_REF_STALE" in json.loads(stale.stdout)["failure_codes"]
        stale_plan = invoke(
            str(control / "tools" / "goal_plan.py"), "--control-root", str(control),
            "--expected-revision", "1", "--plan-file", str(plan_file),
            "--active-minutes", "41", "--review-evidence-ref", "synthetic/stale-plan",
        )
        assert stale_plan.returncode == 2, stale_plan.stdout + stale_plan.stderr
        assert "PLAN_AUTHORITY_REF_STALE_OR_MISSING" in stale_plan.stderr
        assert read(control / "runtime" / "TACTICAL_PLAN_CURRENT.json")["revision"] == 1

        # Reporter must be small, own project, no private event payload.
        report = Path(temp) / "feedback.json"
        sent = invoke(str(control / "tools" / "architecture_feedback.py"),
                      "--control-root", str(control), "--trigger", "MANUAL",
                      "--output", str(report))
        assert sent.returncode == 0, sent.stdout + sent.stderr
        assert report.is_file() and report.stat().st_size < 32768
        feedback = read(report)
        assert feedback["privacy"]["free_text_included"] is False
        assert feedback["diagnostics"]["source"] == "ENUM_EVENT_COUNTS_ONLY"

    print("V1.2 LONGITUDINAL OFFLINE TEST PASSED: 3 processes, stale charter, revision conflict and no replay")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
