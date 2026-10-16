#!/usr/bin/env python3
"""Property and boundary regressions for v1.3 host/path controls."""
from __future__ import annotations

import sys
import json
import hashlib
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

from hypothesis import given, settings, strategies as st

ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from campaignctl import pathish_conflict
from external_effects import ExternalEffectHold, transition
from host_dispatch import _out_of_scope_changes, _write_roots_cover, _write_roots_match
from goal_plan import TacticalPlanError, update
from goal_guard import assess


SAFE_COMPONENT = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyz0123456789_-",
    min_size=1,
    max_size=16,
).filter(lambda value: value not in {".", ".."})
RELATIVE_PATH = st.lists(SAFE_COMPONENT, min_size=1, max_size=5).map(lambda parts: "/".join(parts))


class PathConflictProperties(unittest.TestCase):
    @settings(max_examples=300, deadline=None)
    @given(RELATIVE_PATH, RELATIVE_PATH)
    def test_conflict_is_symmetric(self, left: str, right: str) -> None:
        self.assertEqual(pathish_conflict(left, right), pathish_conflict(right, left))

    @settings(max_examples=200, deadline=None)
    @given(RELATIVE_PATH, SAFE_COMPONENT)
    def test_parent_conflicts_with_descendant_but_not_sibling_prefix(self, parent: str, suffix: str) -> None:
        descendant = parent + "/child"
        self.assertTrue(pathish_conflict(parent, descendant))
        sibling = parent + "-" + suffix
        self.assertFalse(pathish_conflict(parent, sibling))


class HostBoundaryProperties(unittest.TestCase):
    @settings(max_examples=250, deadline=None)
    @given(RELATIVE_PATH)
    def test_exact_roots_match_and_cover_themselves(self, root: str) -> None:
        self.assertTrue(_write_roots_match((root,), (root,)))
        self.assertTrue(_write_roots_cover((root,), (root,)))

    @settings(max_examples=250, deadline=None)
    @given(RELATIVE_PATH, SAFE_COMPONENT)
    def test_cover_requires_component_boundary(self, root: str, component: str) -> None:
        self.assertTrue(_write_roots_cover((root,), (root + "/child",)))
        self.assertFalse(_write_roots_cover((root,), (root + "-" + component,)))
        self.assertFalse(_write_roots_match((root,), (root + "/child",)))

    def test_absolute_and_traversal_roots_are_rejected(self) -> None:
        for unsafe in ("/src", "src/", "../src", "src/../private", "C:/src", "./src", ""):
            with self.subTest(unsafe=unsafe):
                self.assertFalse(_write_roots_match((unsafe,), ("src",)))
                self.assertFalse(_write_roots_match(("src",), (unsafe,)))
                self.assertFalse(_write_roots_cover((unsafe,), ("src",)))

    @settings(max_examples=200, deadline=None)
    @given(RELATIVE_PATH, RELATIVE_PATH)
    def test_changed_deleted_or_added_path_is_out_of_scope_unless_descendant(self, root: str, leaf: str) -> None:
        changed_inside = root + "/" + leaf
        changed_sibling = root + "-outside/" + leaf
        self.assertEqual(_out_of_scope_changes({}, {changed_inside: "new"}, (root,)), [])
        self.assertEqual(_out_of_scope_changes({changed_inside: "old"}, {}, (root,)), [])
        self.assertEqual(
            _out_of_scope_changes({changed_sibling: "old"}, {changed_sibling: "new"}, (root,)),
            [changed_sibling],
        )


class TacticalPlanConcurrency(unittest.TestCase):
    def test_same_expected_revision_has_one_cross_process_winner(self) -> None:
        with tempfile.TemporaryDirectory(prefix="v13-plan-cas-") as temp:
            control = Path(temp)
            (control / "state").mkdir()
            (control / "runtime").mkdir()
            charter = control / "state" / "CHARTER.md"
            charter.write_text("frozen test charter\n", encoding="utf-8")
            charter_sha = hashlib.sha256(charter.read_bytes()).hexdigest()
            goal_path = control / "state" / "GOAL_CONTRACT_CURRENT.json"
            goal_path.write_text(
                json.dumps({
                    "schema_version": "agentic-goal-contract-v1",
                    "goal_id": "G-CAS", "campaign_id": "C-CAS",
                    "charter_ref": "state/CHARTER.md", "charter_sha256": charter_sha,
                    "authority_refs": {"state/CHARTER.md": charter_sha},
                    "definition_of_done": "Persist one plan revision.",
                    "hard_gates": ["REVIEW"], "forbidden_effects": ["EXTERNAL"],
                    "write_envelope": ["src"],
                }), encoding="utf-8")
            review = control / "runtime" / "review.json"
            review.write_text('{"independent_review":"frozen"}\n', encoding="utf-8")
            ready_dir = control / "ready"
            ready_dir.mkdir()
            go = control / "go"
            child = (
                "import json,sys,time\nfrom pathlib import Path\n"
                "sys.path.insert(0," + repr(str(ROOT / "tools")) + ")\n"
                "from goal_plan import update\n"
                "control=Path(sys.argv[1]); ready=Path(sys.argv[2]); go=Path(sys.argv[3]); label=sys.argv[4]\n"
                "ready.write_text('ready')\n"
                "deadline=time.monotonic()+10\n"
                "while not go.exists() and time.monotonic()<deadline: time.sleep(.005)\n"
                "try:\n"
                " result=update(control,expected_revision=-1,plan={'steps':[{'id':label}]},"
                "review_evidence_ref='runtime/review.json')\n"
                " print(json.dumps({'status':'WON','revision':result['revision'],'label':label}))\n"
                "except Exception as exc:\n"
                " print(json.dumps({'status':'CONFLICT','error':str(exc),'type':type(exc).__name__}))\n"
            )
            children = []
            for label in ("A", "B"):
                process = subprocess.Popen(
                    [sys.executable, "-c", child, str(control), str(ready_dir / label), str(go), label],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                )
                children.append((label, process))
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline and not all((ready_dir / label).exists() for label, _ in children):
                time.sleep(.01)
            self.assertTrue(all((ready_dir / label).exists() for label, _ in children), "CAS contenders did not reach barrier")
            go.write_text("release\n", encoding="utf-8")
            outcomes = []
            for _, process in children:
                stdout, stderr = process.communicate(timeout=15)
                self.assertEqual(process.returncode, 0, stderr)
                outcomes.append(json.loads(stdout.strip().splitlines()[-1]))
            winners = [item for item in outcomes if item["status"] == "WON"]
            conflicts = [item for item in outcomes if item["status"] == "CONFLICT"]
            self.assertEqual(len(winners), 1, outcomes)
            self.assertEqual(winners[0]["revision"], 0)
            self.assertEqual(len(conflicts), 1, outcomes)
            self.assertEqual(conflicts[0]["type"], TacticalPlanError.__name__)
            self.assertIn("TACTICAL_PLAN_REVISION_CONFLICT", conflicts[0]["error"])
            final = json.loads((control / "runtime" / "TACTICAL_PLAN_CURRENT.json").read_text(encoding="utf-8"))
            self.assertEqual(final["revision"], 0)
            self.assertEqual(final["steps"][0]["id"], winners[0]["label"])

    def test_plan_review_binds_runtime_and_material_events_retrigger_review(self) -> None:
        with tempfile.TemporaryDirectory(prefix="v13-plan-review-events-") as temp:
            control = Path(temp)
            (control / "state").mkdir()
            (control / "runtime").mkdir()
            charter = control / "state" / "CHARTER.md"
            charter.write_text("frozen review charter\n", encoding="utf-8")
            charter_sha = hashlib.sha256(charter.read_bytes()).hexdigest()
            goal_path = control / "state" / "GOAL_CONTRACT_CURRENT.json"
            goal_path.write_text(
                json.dumps({
                    "schema_version": "agentic-goal-contract-v1",
                    "goal_id": "G-REVIEW", "campaign_id": "C-REVIEW",
                    "charter_ref": "state/CHARTER.md", "charter_sha256": charter_sha,
                    "authority_refs": {"state/CHARTER.md": charter_sha},
                    "definition_of_done": "Refresh tactical review when material events occur.",
                    "hard_gates": ["REVIEW"], "forbidden_effects": ["EXTERNAL"],
                    "write_envelope": ["src"],
                }), encoding="utf-8")
            (control / "runtime" / "review.json").write_text(
                '{"independent_review":"frozen"}\n', encoding="utf-8")
            runtime_path = control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json"
            runtime = {"revision": 1, "event_log": [
                {"seq": 1, "action": "CAMPAIGN_RUNTIME_INITIALIZED"}
            ]}
            runtime_path.write_text(json.dumps(runtime), encoding="utf-8")

            plan = update(
                control, expected_revision=-1,
                plan={"steps": [{"id": "implement"}], "plan_mode": "UNVERIFIED",
                      "hard_gates": [], "forbidden_effects": [], "write_envelope": ["*"]},
                review_evidence_ref="runtime/review.json",
            )
            self.assertNotIn("hard_gates", plan)
            self.assertNotIn("forbidden_effects", plan)
            self.assertNotIn("write_envelope", plan)
            self.assertIn('"hard_gates": ["REVIEW"]', goal_path.read_text(encoding="utf-8"))
            self.assertEqual(plan["reviewed_runtime_revision"], 1)
            self.assertEqual(plan["reviewed_runtime_event_seq"], 1)
            initial = assess(control)
            self.assertFalse(initial["tactical_review"]["event_triggered"])
            self.assertTrue(initial["tactical_review"]["review_required"])
            self.assertEqual(initial["tactical_review"]["active_time_status"],
                             "UNKNOWN_NATIVE_ACTIVE_CLOCK_UNAVAILABLE")
            self.assertIn("TACTICAL_REVIEW_DUE_OR_UNVERIFIED", initial["failure_codes"])

            runtime["revision"] = 2
            runtime["event_log"].append(
                {"seq": 2, "action": "HOST_DISPATCH_COMMAND_OBSERVED"}
            )
            runtime_path.write_text(json.dumps(runtime), encoding="utf-8")
            observer_only = assess(control)
            self.assertFalse(observer_only["tactical_review"]["event_triggered"])

            runtime["revision"] = 3
            runtime["event_log"].append(
                {"seq": 3, "action": "WORK_UNIT_FAILED", "work_unit_id": "W1"}
            )
            runtime_path.write_text(json.dumps(runtime), encoding="utf-8")
            after_failure = assess(control)
            self.assertTrue(after_failure["tactical_review"]["event_triggered"])
            self.assertEqual(after_failure["tactical_review"]["trigger_events"], [
                {"seq": 3, "action": "WORK_UNIT_FAILED", "work_unit_id": "W1"}
            ])
            self.assertIn("TACTICAL_PLAN_EVENT_REVIEW_REQUIRED", after_failure["failure_codes"])
            self.assertFalse(after_failure["may_execute_material_goal"])

            runtime["revision"] = 4  # Deliberately inconsistent with the three durable events.
            runtime_path.write_text(json.dumps(runtime), encoding="utf-8")
            corrupt_runtime = assess(control)
            self.assertIn("TACTICAL_PLAN_RUNTIME_CURRENTNESS_INVALID", corrupt_runtime["failure_codes"])
            self.assertFalse(corrupt_runtime["may_execute_material_goal"])


class AmbiguousExternalEffectRecovery(unittest.TestCase):
    def test_restart_cannot_replay_ambiguous_attempt(self) -> None:
        with tempfile.TemporaryDirectory(prefix="v13-effect-recovery-") as temp:
            control = Path(temp)
            request = {"kind": "SYNTHETIC_ONLY", "record": "fixture-1"}
            prepared = transition(
                control, "effect-1", "PREPARE", request=request,
                authorized_ref="fixture-authority-not-a-permit",
            )
            self.assertEqual(prepared["phase"], "PREPARED")
            attempted = transition(control, "effect-1", "ATTEMPT")
            self.assertEqual(attempted["phase"], "REQUESTED_AMBIGUOUS")
            self.assertEqual(attempted["attempts"], 1)
            resumed = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "external_effects.py"),
                 "--control-root", str(control), "--effect-id", "effect-1", "--event", "ATTEMPT"],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(resumed.returncode, 2, resumed.stdout + resumed.stderr)
            self.assertIn("DUPLICATE_OR_AMBIGUOUS_EFFECT_DISPATCH", resumed.stderr)
            record = json.loads((control / "runtime" / "external_effects" / "effect-1.json").read_text(encoding="utf-8"))
            self.assertEqual(record["phase"], "REQUESTED_AMBIGUOUS")
            self.assertEqual(record["attempts"], 1)
            with self.assertRaisesRegex(ExternalEffectHold, "DUPLICATE_OR_AMBIGUOUS_EFFECT_DISPATCH"):
                transition(control, "effect-1", "ATTEMPT")
            self.assertEqual(json.loads((control / "runtime" / "external_effects" / "effect-1.json").read_text(encoding="utf-8")), record)


if __name__ == "__main__":
    unittest.main(verbosity=2)
