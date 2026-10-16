#!/usr/bin/env python3
"""Adversarial physical tests for the public portable ToolPort consumer."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import goal_guard
from candidate_manifest import build_manifest
from tool_port import (PortableTestAdapter, ToolCommand, ToolDispatchHold,
                       ToolDispatchInterrupted, dispatch_tool, recover_tool_dispatch,
                       _safe_target, _source_tree_digest, _workspace_path_sha256,
                       _dispatch_tool)
import campaignctl


def put(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def fixture(base: Path, *, embedded_control: bool = False):
    workspace = base / "workspace"
    control = workspace / ".agentic-sdlc" if embedded_control else base / "control"
    (workspace / "src").mkdir(parents=True)
    (workspace / "src" / "notes.py").write_bytes(b"VALUE = 1\n")
    campaign, actor, run = "C-TOOL", "I3-TOOL", "RUN-TOOL"
    expires = (datetime.now(timezone.utc) + timedelta(minutes=20)).isoformat().replace("+00:00", "Z")
    charter = {
        "schema_version": "campaign-charter-0.1", "campaign_id": campaign,
        "product_or_workstream": "tool-port-fixture", "baseline_ref": "fixture-base",
        "resource_envelope": {"allowed_write_surfaces": ["src"],
            "protected_surfaces": [".git", "outside"], "external_authority_gates": [],
            "allowed_tool_operations": ["write_text"], "portable_test_adapter_only": True},
    }
    charter_path = control / "campaigns" / campaign / "CHARTER.json"
    put(charter_path, charter)
    runtime = {
        "schema_version": "campaign-runtime-0.1", "campaign_id": campaign,
        "product_or_workstream": "tool-port-fixture",
        "charter_ref": f"campaigns/{campaign}/CHARTER.json", "campaign_status": "ACTIVE",
        "revision": 1, "updated_at": "2026-10-15T00:00:00Z", "integrated_ref": "fixture-base",
        "current_checkpoint_id": None, "work_units": [{
            "id": "W1", "status": "ACTIVE", "actor_id": actor, "run_id": run,
            "allowed_write_surfaces": ["src"], "dependencies": [], "shared_resources": [],
        }],
        "event_log": [{"seq": 1, "at": "2026-10-15T00:00:00Z", "action": "CAMPAIGN_STARTED",
                       "work_unit_id": None, "actor_id": actor, "details": {}}],
    }
    put(control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json", runtime)
    put(control / "state" / "PRODUCT_STATE_CURRENT.json", {
        "product_or_workstream": "tool-port-fixture",
        "active_campaign": {"campaign_id": campaign, "checkpoint_or_terminal_ref": None},
        "current_code_ref": "fixture-base",
        "currentness_set": ["runtime/CAMPAIGN_RUNTIME_CURRENT.json",
            "state/EXECUTION_AUTHORITY_CURRENT.json", "state/IDENTITY_REGISTRY_CURRENT.json"],
    })
    put(control / "state" / "EXECUTION_AUTHORITY_CURRENT.json", {
        "authority_status": "ACTIVE", "campaign_id": campaign,
        "campaign_lead_actor_id": actor, "current_run_id": run,
        "baseline_ref": "fixture-base", "checkpoint_ref": None,
        "allowed_write_surfaces": ["src"], "expires_at": expires,
    })
    put(control / "state" / "IDENTITY_REGISTRY_CURRENT.json", {"actors": [{
        "actor_id": actor, "role_class": "I3_ENGINEERING_CAMPAIGN_LEAD", "status": "ACTIVE",
        "current_run_id": run,
    }]})
    goal = {
        "schema_version": goal_guard.SCHEMA, "goal_id": "G-TOOL", "campaign_id": campaign,
        "charter_ref": f"campaigns/{campaign}/CHARTER.json",
        "charter_sha256": hashlib.sha256(charter_path.read_bytes()).hexdigest(),
        "authority_refs": {f"campaigns/{campaign}/CHARTER.json": hashlib.sha256(charter_path.read_bytes()).hexdigest()},
        "definition_of_done": "Exercise the local file tool safely.", "hard_gates": ["physical readback"],
        "forbidden_effects": ["provider dispatch", "outside writes"], "write_envelope": ["src"],
    }
    put(control / "state" / "GOAL_CONTRACT_CURRENT.json", goal)
    review = control / "reviews" / "plan.json"
    put(review, {"review": "fixture review"})
    plan = {
        "schema_version": goal_guard.PLAN_SCHEMA, "campaign_id": campaign,
        "goal_digest": goal_guard.goal_fingerprint(goal), "revision": 1,
        "steps": [{"tool_operation": "write_text", "target": "src/notes.py"}],
        "hypotheses": [], "blockers": [], "review_evidence_ref": "reviews/plan.json",
        "review_evidence_sha256": hashlib.sha256(review.read_bytes()).hexdigest(),
        "reviewed_runtime_revision": 1, "reviewed_runtime_event_seq": 1,
        "active_progress_minutes_since_review": None, "progress_clock": "HOST_UNVERIFIED_ADVISORY",
        "invocation_permit_issued": False, "plan_mode": "SMALL_SOLO", "progress_tool": "NATIVE_HOST_PROGRESS_UNAVAILABLE",
    }
    put(control / "runtime" / "TACTICAL_PLAN_CURRENT.json", plan)
    cmd = ToolCommand(
        campaign_id=campaign, actor_id=actor, run_id=run, work_unit_id="W1", runtime_revision=1,
        source_tree_sha256=_source_tree_digest(workspace, control),
        workspace_path_sha256=_workspace_path_sha256(workspace),
        goal_sha256=hashlib.sha256((control / "state" / "GOAL_CONTRACT_CURRENT.json").read_bytes()).hexdigest(),
        plan_sha256=hashlib.sha256((control / "runtime" / "TACTICAL_PLAN_CURRENT.json").read_bytes()).hexdigest(),
        allowed_write_surfaces=("src",), idempotency_key="tool-once-001", operation_id="write_text",
        target="src/notes.py", content_utf8="VALUE = 2\n", expected_previous_sha256=hashlib.sha256(b"VALUE = 1\n").hexdigest(),
    )
    return control, workspace, cmd


def bind_plan_target(control: Path, command: ToolCommand, target: str) -> ToolCommand:
    plan_path = control / "runtime" / "TACTICAL_PLAN_CURRENT.json"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    plan["steps"] = [{"tool_operation": "write_text", "target": target}]
    put(plan_path, plan)
    return ToolCommand(**{**command.__dict__,
        "plan_sha256": hashlib.sha256(plan_path.read_bytes()).hexdigest(), "target": target})


def test_physical_effect_and_receipt() -> None:
    with tempfile.TemporaryDirectory(prefix="tool-port-") as temp:
        control, workspace, command = fixture(Path(temp))
        receipt = dispatch_tool(control, workspace, command)
        assert receipt["phase"] == "OBSERVED", receipt
        assert receipt["capabilities"]["support_classification"] == "PORTABLE_TEST_ADAPTER"
        assert receipt["capabilities"]["identity_evidence"] == "LOCAL_CAMPAIGN_STATE_ONLY_NOT_HUMAN_AUTHENTICATION"
        assert receipt["capabilities"]["provider_invocation"] is False
        assert receipt["provider_cost"] == "NOT_APPLICABLE_NOT_MEASURED"
        assert receipt["cancellation_supported"] is False
        assert receipt["bytes_written"] == len(b"VALUE = 2\n")
        assert type(receipt["elapsed_ms"]) is int and receipt["elapsed_ms"] >= 0
        assert receipt["completed_at"]
        assert (workspace / "src" / "notes.py").read_text(encoding="utf-8") == "VALUE = 2\n"
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        assert [event["action"] for event in runtime["event_log"]][-2:] == [
            "TOOL_DISPATCH_STARTED", "TOOL_DISPATCH_OBSERVED"]
        replay = dispatch_tool(control, workspace, command)
        assert replay == receipt, "same key and command did not return the stable receipt"
        conflicting = ToolCommand(**{**command.__dict__, "content_utf8": "VALUE = 3\n"})
        try:
            dispatch_tool(control, workspace, conflicting)
        except ToolDispatchHold as exc:
            assert "IDEMPOTENCY_KEY_COMMAND_CONFLICT" in str(exc)
        else:
            raise AssertionError("same key with different command was accepted")


def test_out_of_scope_rejected_before_intent_or_effect() -> None:
    with tempfile.TemporaryDirectory(prefix="tool-port-scope-") as temp:
        control, workspace, command = fixture(Path(temp))
        outside = workspace / "outside" / "notes.py"
        bad = bind_plan_target(control, command, "outside/notes.py")
        try:
            dispatch_tool(control, workspace, bad)
        except ToolDispatchHold as exc:
            assert "OUTSIDE_AUTHORIZED_ROOT" in str(exc)
        else:
            raise AssertionError("out-of-scope path was accepted")
        assert not outside.exists()
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        assert len(runtime["event_log"]) == 1


def test_stale_plan_rejected_without_effect() -> None:
    with tempfile.TemporaryDirectory(prefix="tool-port-stale-") as temp:
        control, workspace, command = fixture(Path(temp))
        plan_path = control / "runtime" / "TACTICAL_PLAN_CURRENT.json"
        plan = json.loads(plan_path.read_text())
        plan["revision"] += 1
        put(plan_path, plan)
        try:
            dispatch_tool(control, workspace, command)
        except ToolDispatchHold as exc:
            assert "PLAN_SOURCE_DRIFT" in str(exc)
        else:
            raise AssertionError("stale Plan was accepted")
        assert (workspace / "src" / "notes.py").read_text() == "VALUE = 1\n"


def test_workspace_location_and_pending_journal_fail_before_intent() -> None:
    with tempfile.TemporaryDirectory(prefix="tool-port-workspace-copy-") as temp:
        base = Path(temp)
        control, workspace, command = fixture(base)
        copied = base / "workspace-copy"
        shutil.copytree(workspace, copied)
        assert _source_tree_digest(copied, control) == command.source_tree_sha256
        try:
            dispatch_tool(control, copied, command)
        except ToolDispatchHold as exc:
            assert "WORKSPACE_PATH_BINDING_MISMATCH" in str(exc)
        else:
            raise AssertionError("byte-identical copied workspace accepted a path-bound command")
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        assert len(runtime["event_log"]) == 1, "workspace copy rejection wrote an intent"

    with tempfile.TemporaryDirectory(prefix="tool-port-pending-journal-") as temp:
        control, workspace, command = fixture(Path(temp))
        put(campaignctl.journal_path(control), {"transaction_id": "interrupted-transition"})
        try:
            dispatch_tool(control, workspace, command)
        except ToolDispatchHold as exc:
            assert "PENDING_CAMPAIGN_TRANSACTION" in str(exc)
        else:
            raise AssertionError("dispatch proceeded across a pending campaign journal")
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        assert len(runtime["event_log"]) == 1, "pending-journal rejection wrote an intent"


def test_goal_charter_binding_must_match_runtime_charter() -> None:
    with tempfile.TemporaryDirectory(prefix="tool-port-goal-charter-") as temp:
        control, workspace, command = fixture(Path(temp))
        goal_path = control / "state" / "GOAL_CONTRACT_CURRENT.json"
        goal = json.loads(goal_path.read_text(encoding="utf-8"))
        alternate = control / "campaigns" / command.campaign_id / "ALT_CHARTER.json"
        shutil.copyfile(control / "campaigns" / command.campaign_id / "CHARTER.json", alternate)
        alt_ref = f"campaigns/{command.campaign_id}/ALT_CHARTER.json"
        goal["charter_ref"] = alt_ref
        goal["authority_refs"] = {alt_ref: hashlib.sha256(alternate.read_bytes()).hexdigest()}
        goal["charter_sha256"] = hashlib.sha256(alternate.read_bytes()).hexdigest()
        put(goal_path, goal)
        plan_path = control / "runtime" / "TACTICAL_PLAN_CURRENT.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        plan["goal_digest"] = goal_guard.goal_fingerprint(goal)
        put(plan_path, plan)
        command = ToolCommand(**{**command.__dict__,
            "goal_sha256": hashlib.sha256(goal_path.read_bytes()).hexdigest(),
            "plan_sha256": hashlib.sha256(plan_path.read_bytes()).hexdigest()})
        try:
            dispatch_tool(control, workspace, command)
        except ToolDispatchHold as exc:
            assert "GOAL_CHARTER_BINDING_MISMATCH" in str(exc)
        else:
            raise AssertionError("Goal bound to a non-current campaign charter was accepted")
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        assert len(runtime["event_log"]) == 1, "charter mismatch wrote an intent"


def test_material_campaign_or_non_temp_workspace_is_held() -> None:
    with tempfile.TemporaryDirectory(prefix="tool-port-test-boundary-") as temp:
        control, workspace, command = fixture(Path(temp))
        charter_path = control / "campaigns" / command.campaign_id / "CHARTER.json"
        charter = json.loads(charter_path.read_text(encoding="utf-8"))
        charter["resource_envelope"]["portable_test_adapter_only"] = False
        put(charter_path, charter)
        digest = hashlib.sha256(charter_path.read_bytes()).hexdigest()
        goal_path = control / "state" / "GOAL_CONTRACT_CURRENT.json"
        goal = json.loads(goal_path.read_text(encoding="utf-8"))
        goal["charter_sha256"] = digest
        goal["authority_refs"][goal["charter_ref"]] = digest
        put(goal_path, goal)
        plan_path = control / "runtime" / "TACTICAL_PLAN_CURRENT.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        plan["goal_digest"] = goal_guard.goal_fingerprint(goal)
        put(plan_path, plan)
        command = ToolCommand(**{**command.__dict__,
            "goal_sha256": hashlib.sha256(goal_path.read_bytes()).hexdigest(),
            "plan_sha256": hashlib.sha256(plan_path.read_bytes()).hexdigest()})
        try:
            dispatch_tool(control, workspace, command)
        except ToolDispatchHold as exc:
            assert "PORTABLE_ADAPTER_NOT_EXPLICITLY_TEST_ONLY" in str(exc)
        else:
            raise AssertionError("portable test adapter accepted a material campaign charter")
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        assert len(runtime["event_log"]) == 1, "material charter rejection wrote an intent"

    with tempfile.TemporaryDirectory(prefix="tool-port-temp-boundary-") as temp:
        control, workspace, command = fixture(Path(temp))
        with patch("tool_port.tempfile.gettempdir", return_value=str(workspace)):
            try:
                dispatch_tool(control, workspace, command)
            except ToolDispatchHold as exc:
                assert "DISPOSABLE_TEMP_ROOTS" in str(exc)
            else:
                raise AssertionError("temporary-root itself was accepted as a write workspace")
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        assert len(runtime["event_log"]) == 1, "temp root rejection wrote an intent"

    with tempfile.TemporaryDirectory(prefix="tool-port-control-boundary-") as temp:
        base = Path(temp)
        control, workspace, command = fixture(base)
        isolated_root = base / "isolated-test-root"
        isolated_root.mkdir()
        moved_workspace = isolated_root / "workspace"
        shutil.move(str(workspace), str(moved_workspace))
        with patch("tool_port.tempfile.gettempdir", return_value=str(isolated_root)):
            try:
                dispatch_tool(control, moved_workspace, command)
            except ToolDispatchHold as exc:
                assert "DISPOSABLE_TEMP_ROOTS" in str(exc)
            else:
                raise AssertionError("temporary workspace paired with external control root was accepted")
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        assert len(runtime["event_log"]) == 1, "external control rejection wrote an intent"
        with patch("tool_port.tempfile.gettempdir", return_value=str(isolated_root)):
            try:
                recover_tool_dispatch(control, "00000000-0000-0000-0000-000000000000")
            except ToolDispatchHold as exc:
                assert "DISPOSABLE_TEMP_ROOTS" in str(exc)
            else:
                raise AssertionError("recovery accepted a control root outside the disposable fixture")
        runtime_after_recovery = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        assert len(runtime_after_recovery["event_log"]) == 1, "external recovery changed campaign state"


class InterruptedBeforeEffect(PortableTestAdapter):
    def execute(self, command, workspace):
        del command, workspace
        raise ToolDispatchInterrupted("simulated interruption before effect")


def test_interrupt_recovers_unknown_without_replay() -> None:
    with tempfile.TemporaryDirectory(prefix="tool-port-recovery-") as temp:
        control, workspace, command = fixture(Path(temp))
        try:
            _dispatch_tool(control, workspace, command, InterruptedBeforeEffect())
        except ToolDispatchInterrupted:
            pass
        else:
            raise AssertionError("injected interruption did not fire")
        assert (workspace / "src" / "notes.py").read_text() == "VALUE = 1\n"
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        start = next(event for event in runtime["event_log"] if event["action"] == "TOOL_DISPATCH_STARTED")
        recovered = recover_tool_dispatch(control, start["details"]["dispatch_id"])
        assert recovered["phase"] == "UNKNOWN"
        assert recovered["result"] == "INTERRUPTED_RECEIPT_NOT_OBSERVED_NO_REPLAY"
        replay = dispatch_tool(control, workspace, command)
        assert replay["phase"] == "UNKNOWN", "ambiguous recovered action was replayed"


def test_recovery_rejects_corrupt_or_ambiguous_campaign_journal() -> None:
    # Recovery must not append to a journal whose revision/sequence lineage is
    # broken, nor choose one outcome when the same dispatch has duplicates.
    for corruption, expected_code in (("revision", "CAMPAIGN_RUNTIME_CURRENTNESS_INVALID"),
                                      ("start", "DISPATCH_START_MISSING_OR_DUPLICATE"),
                                      ("terminal", "DISPATCH_TERMINAL_DUPLICATE_OR_AMBIGUOUS")):
        with tempfile.TemporaryDirectory(prefix=f"tool-port-recovery-{corruption}-") as temp:
            control, workspace, command = fixture(Path(temp))
            try:
                _dispatch_tool(control, workspace, command, InterruptedBeforeEffect())
            except ToolDispatchInterrupted:
                pass
            else:
                raise AssertionError("interruption fixture did not leave a durable start")
            runtime_path = control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json"
            runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
            start = next(event for event in runtime["event_log"]
                         if event["action"] == "TOOL_DISPATCH_STARTED")
            dispatch_id = start["details"]["dispatch_id"]
            if corruption == "revision":
                runtime["revision"] += 1
            elif corruption == "start":
                duplicate = json.loads(json.dumps(start))
                duplicate["seq"] = len(runtime["event_log"]) + 1
                runtime["event_log"].append(duplicate)
                runtime["revision"] = len(runtime["event_log"])
            else:
                recover_tool_dispatch(control, dispatch_id)
                runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
                terminal = next(event for event in runtime["event_log"]
                                if event["action"] == "TOOL_DISPATCH_UNKNOWN"
                                and event["details"].get("dispatch_id") == dispatch_id)
                duplicate = json.loads(json.dumps(terminal))
                duplicate["seq"] = len(runtime["event_log"]) + 1
                runtime["event_log"].append(duplicate)
                runtime["revision"] = len(runtime["event_log"])
            put(runtime_path, runtime)
            before = runtime_path.read_bytes()
            try:
                recover_tool_dispatch(control, dispatch_id)
            except ToolDispatchHold as exc:
                assert expected_code in str(exc), (corruption, exc)
            else:
                raise AssertionError(f"recovery accepted {corruption} journal corruption")
            assert runtime_path.read_bytes() == before, "failed recovery mutated the corrupt journal"
            assert (workspace / "src" / "notes.py").read_bytes() == b"VALUE = 1\n"


class InterruptedAfterEffect(PortableTestAdapter):
    def execute(self, command, workspace):
        super().execute(command, workspace)
        raise ToolDispatchInterrupted("simulated response loss after physical effect")


def test_response_loss_after_effect_stays_unknown_without_replay() -> None:
    with tempfile.TemporaryDirectory(prefix="tool-port-response-loss-") as temp:
        control, workspace, command = fixture(Path(temp))
        try:
            _dispatch_tool(control, workspace, command, InterruptedAfterEffect())
        except ToolDispatchInterrupted:
            pass
        else:
            raise AssertionError("response-loss injection did not fire")
        target = workspace / "src" / "notes.py"
        assert target.read_bytes() == b"VALUE = 2\n", "physical effect did not occur"
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        start = next(event for event in runtime["event_log"] if event["action"] == "TOOL_DISPATCH_STARTED")
        recovered = recover_tool_dispatch(control, start["details"]["dispatch_id"])
        assert recovered["phase"] == "UNKNOWN"
        assert recovered["result"] == "INTERRUPTED_RECEIPT_NOT_OBSERVED_NO_REPLAY"
        assert dispatch_tool(control, workspace, command)["phase"] == "UNKNOWN"
        assert target.read_bytes() == b"VALUE = 2\n"


class ExtraSourceWriteAdapter(PortableTestAdapter):
    def execute(self, command, workspace):
        result = super().execute(command, workspace)
        (workspace / "src" / "unplanned.py").write_text("UNPLANNED = True\n", encoding="utf-8")
        return result


def test_unrelated_source_drift_downgrades_receipt() -> None:
    with tempfile.TemporaryDirectory(prefix="tool-port-unrelated-drift-") as temp:
        control, workspace, command = fixture(Path(temp))
        receipt = _dispatch_tool(control, workspace, command, ExtraSourceWriteAdapter())
        assert receipt["phase"] == "UNKNOWN", receipt
        assert receipt["result"] == "UNRELATED_SOURCE_DRIFT_DURING_EFFECT", receipt
        assert (workspace / "src" / "notes.py").read_bytes() == b"VALUE = 2\n"
        assert (workspace / "src" / "unplanned.py").read_text(encoding="utf-8") == "UNPLANNED = True\n"


def test_public_cli_and_concurrent_revision_cas() -> None:
    with tempfile.TemporaryDirectory(prefix="tool-port-cas-") as temp:
        base = Path(temp)
        control, workspace, command = fixture(base)
        command_paths = []
        for key in ("cas-left", "cas-right"):
            path = base / f"{key}.json"
            path.write_text(json.dumps({**command.__dict__, "idempotency_key": key}), encoding="utf-8")
            command_paths.append(path)
        invocations = []
        for path in command_paths:
            invocations.append(subprocess.Popen([
                sys.executable, str(ROOT / "tools" / "campaignctl.py"),
                "--control-root", str(control), "tool-dispatch", "--adapter", "portable-test-v1",
                "--workspace", str(workspace), "--command", str(path),
            ], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
        results = [process.communicate(timeout=30) + (process.returncode,) for process in invocations]
        assert sum(result[2] == 0 for result in results) == 1, results
        assert sum(result[2] != 0 for result in results) == 1, results
        loser = next(result for result in results if result[2] != 0)
        assert "CAMPAIGN_RUNTIME_REVISION_STALE" in loser[1], results
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        actions = [event["action"] for event in runtime["event_log"]]
        assert actions.count("TOOL_DISPATCH_STARTED") == 1, actions
        assert actions.count("TOOL_DISPATCH_OBSERVED") == 1, actions
        assert (workspace / "src" / "notes.py").read_bytes() == b"VALUE = 2\n"


def test_installed_toolport_consumer_performs_bound_physical_effect() -> None:
    with tempfile.TemporaryDirectory(prefix="tool-port-installed-") as temp:
        base = Path(temp)
        control, workspace, command = fixture(base, embedded_control=True)
        installed_tools = control / "tools"
        shutil.copytree(ROOT / "tools", installed_tools,
                        ignore=shutil.ignore_patterns("__pycache__"))
        command_path = control / "state" / "installed-tool-command.json"
        command_path.write_text(json.dumps(command.__dict__), encoding="utf-8")
        process = subprocess.run([
            sys.executable, str(installed_tools / "campaignctl.py"),
            "--control-root", str(control), "tool-dispatch",
            "--adapter", "portable-test-v1", "--workspace", str(workspace),
            "--command", str(command_path),
        ], cwd=ROOT, capture_output=True, text=True, timeout=30)
        assert process.returncode == 0, (process.stdout, process.stderr)
        receipt = json.loads(process.stdout)
        assert receipt["phase"] == "OBSERVED" and receipt["result"] == "EFFECT_PHYSICALLY_OBSERVED", receipt
        assert (workspace / "src" / "notes.py").read_bytes() == b"VALUE = 2\n"
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        assert [event["action"] for event in runtime["event_log"]][-2:] == [
            "TOOL_DISPATCH_STARTED", "TOOL_DISPATCH_OBSERVED"]


def test_embedded_control_state_does_not_create_source_drift() -> None:
    with tempfile.TemporaryDirectory(prefix="tool-port-embedded-") as temp:
        control, workspace, command = fixture(Path(temp))
        embedded = workspace / ".agentic-sdlc"
        shutil.move(str(control), str(embedded))
        receipt = dispatch_tool(embedded, workspace, command)
        assert receipt["phase"] == "OBSERVED", receipt
        assert receipt["source_tree_sha256_after"] == build_manifest(
            workspace, exclude_paths=(".agentic-sdlc",))["source_tree_sha256"]
        assert (workspace / "src" / "notes.py").read_bytes() == b"VALUE = 2\n"


def test_expired_lease_and_precondition_fail_without_write() -> None:
    with tempfile.TemporaryDirectory(prefix="tool-port-lease-") as temp:
        control, workspace, command = fixture(Path(temp))
        authority_path = control / "state" / "EXECUTION_AUTHORITY_CURRENT.json"
        authority = json.loads(authority_path.read_text())
        authority["expires_at"] = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat().replace("+00:00", "Z")
        put(authority_path, authority)
        try:
            dispatch_tool(control, workspace, command)
        except ToolDispatchHold as exc:
            assert "LEASE_EXPIRED" in str(exc)
        else:
            raise AssertionError("expired lease was accepted")
        assert (workspace / "src" / "notes.py").read_bytes() == b"VALUE = 1\n"

    with tempfile.TemporaryDirectory(prefix="tool-port-precondition-") as temp:
        control, workspace, command = fixture(Path(temp))
        (workspace / "src" / "notes.py").write_bytes(b"VALUE = 9\n")
        changed = ToolCommand(**{**command.__dict__,
            "source_tree_sha256": _source_tree_digest(workspace, control)})
        try:
            dispatch_tool(control, workspace, changed)
        except ToolDispatchHold as exc:
            assert "PRECONDITION_FAILED" in str(exc)
        else:
            raise AssertionError("stale target precondition was accepted")
        assert (workspace / "src" / "notes.py").read_bytes() == b"VALUE = 9\n"


def test_source_drift_and_hardlink_rejected_before_intent() -> str | None:
    with tempfile.TemporaryDirectory(prefix="tool-port-source-drift-") as temp:
        control, workspace, command = fixture(Path(temp))
        (workspace / "src" / "other.py").write_bytes(b"drift\n")
        try:
            dispatch_tool(control, workspace, command)
        except ToolDispatchHold as exc:
            assert "SOURCE_TREE_DRIFT" in str(exc)
        else:
            raise AssertionError("source drift was accepted")
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        assert len(runtime["event_log"]) == 1

    with tempfile.TemporaryDirectory(prefix="tool-port-hardlink-") as temp:
        base = Path(temp)
        control, workspace, command = fixture(base)
        external = base / "protected.txt"
        external.write_bytes(b"protected\n")
        linked = workspace / "src" / "linked.py"
        try:
            import os
            os.link(external, linked)
        except OSError as exc:
            return f"SKIP: hardlink fixture unavailable: {type(exc).__name__}"
        changed = bind_plan_target(control, command, "src/linked.py")
        changed = ToolCommand(**{**changed.__dict__,
            "source_tree_sha256": _source_tree_digest(workspace, control),
            "expected_previous_sha256": hashlib.sha256(b"protected\n").hexdigest()})
        try:
            dispatch_tool(control, workspace, changed)
        except ToolDispatchHold as exc:
            assert "HARDLINKED" in str(exc)
        else:
            raise AssertionError("hardlinked target was accepted")
        assert external.read_bytes() == b"protected\n"


def test_canonical_control_exclusion_cannot_hide_source() -> None:
    with tempfile.TemporaryDirectory(prefix="tool-port-control-root-") as temp:
        root = Path(temp) / "workspace"
        (root / "src").mkdir(parents=True)
        source = root / "src" / "app.py"
        source.write_text("VALUE = 1\n", encoding="utf-8")
        canonical = root / ".agentic-sdlc"
        canonical.mkdir()
        state = canonical / "runtime.json"
        state.write_text("state 1", encoding="utf-8")
        first = _source_tree_digest(root, canonical)
        state.write_text("state 2", encoding="utf-8")
        if _source_tree_digest(root, canonical) != first:
            raise AssertionError("canonical control state changed product source identity")
        source.write_text("VALUE = 2\n", encoding="utf-8")
        if _source_tree_digest(root, canonical) == first:
            raise AssertionError("canonical control exclusion hid an actual source edit")
        try:
            _source_tree_digest(root, root / "src")
        except ToolDispatchHold as exc:
            assert "NONCANONICAL_EMBEDDED_CONTROL_ROOT" in str(exc)
        else:
            raise AssertionError("source directory was accepted as an embedded control root")


def test_traversal_and_symlink_boundaries_fail_before_intent() -> str | None:
    import os
    skipped = []
    with tempfile.TemporaryDirectory(prefix="tool-port-links-") as temp:
        base = Path(temp)
        control, workspace, command = fixture(base)
        outside = base / "outside"
        outside.mkdir()
        protected = outside / "notes.py"
        protected.write_text("PROTECTED = 1\n", encoding="utf-8")
        runtime_path = control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json"
        before_events = len(json.loads(runtime_path.read_text(encoding="utf-8"))["event_log"])

        traversal = bind_plan_target(control, command, "../outside/notes.py")
        try:
            dispatch_tool(control, workspace, traversal)
        except ToolDispatchHold as exc:
            assert "INVALID_TOOL_TARGET" in str(exc) or "OUTSIDE_AUTHORIZED_ROOT" in str(exc)
        else:
            raise AssertionError("path traversal reached the adapter")

        target_link = workspace / "src" / "link.py"
        try:
            os.symlink(protected, target_link)
        except (OSError, NotImplementedError) as exc:
            skipped.append("symlink target unavailable: " + type(exc).__name__)
        else:
            try:
                _safe_target(workspace, "src/link.py", ("src",))
            except ToolDispatchHold as exc:
                assert "SYMLINKED_TOOL_TARGET" in str(exc)
            else:
                raise AssertionError("symlink target passed the path guard")
            linked = bind_plan_target(control, command, "src/link.py")
            try:
                dispatch_tool(control, workspace, linked)
            except ToolDispatchHold as exc:
                assert any(reason in str(exc) for reason in
                           ("SOURCE_TREE_DRIFT", "ManifestError", "SYMLINKED_TOOL_TARGET"))
            else:
                raise AssertionError("symlink target was accepted")

        parent_link = workspace / "src" / "linked-dir"
        try:
            os.symlink(outside, parent_link, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            skipped.append("symlink parent unavailable: " + type(exc).__name__)
        else:
            try:
                _safe_target(workspace, "src/linked-dir/notes.py", ("src",))
            except ToolDispatchHold as exc:
                assert "SYMLINKED_TOOL_PARENT" in str(exc)
            else:
                raise AssertionError("symlinked parent passed the path guard")
            linked_parent = bind_plan_target(control, command, "src/linked-dir/notes.py")
            try:
                dispatch_tool(control, workspace, linked_parent)
            except ToolDispatchHold as exc:
                assert any(reason in str(exc) for reason in
                           ("SOURCE_TREE_DRIFT", "ManifestError", "SYMLINKED_TOOL_PARENT"))
            else:
                raise AssertionError("symlinked parent was accepted")

        runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
        if len(runtime["event_log"]) != before_events:
            raise AssertionError("rejected traversal/symlink wrote a dispatch intent")
        if protected.read_text(encoding="utf-8") != "PROTECTED = 1\n":
            raise AssertionError("rejected traversal/symlink modified the protected outside file")
    return "SKIP: " + "; ".join(skipped) if skipped else None


def test_wrong_actor_and_mid_effect_plan_drift_fail_closed() -> None:
    with tempfile.TemporaryDirectory(prefix="tool-port-actor-") as temp:
        control, workspace, command = fixture(Path(temp))
        wrong = ToolCommand(**{**command.__dict__, "actor_id": "I3-WRONG"})
        try:
            dispatch_tool(control, workspace, wrong)
        except ToolDispatchHold as exc:
            assert "AUTHORITY_OR_SOURCE_BINDING_INVALID" in str(exc) or "BINDING_MISMATCH" in str(exc)
        else:
            raise AssertionError("wrong actor was accepted")
        assert (workspace / "src" / "notes.py").read_bytes() == b"VALUE = 1\n"

    class MutatingPlanAdapter(PortableTestAdapter):
        def __init__(self, plan_path: Path):
            self.plan_path = plan_path

        def execute(self, command, workspace):
            result = super().execute(command, workspace)
            plan = json.loads(self.plan_path.read_text(encoding="utf-8"))
            plan["revision"] += 1
            put(self.plan_path, plan)
            return result

    with tempfile.TemporaryDirectory(prefix="tool-port-plan-drift-") as temp:
        control, workspace, command = fixture(Path(temp))
        receipt = _dispatch_tool(control, workspace, command,
            MutatingPlanAdapter(control / "runtime" / "TACTICAL_PLAN_CURRENT.json"))
        assert receipt["phase"] == "UNKNOWN", receipt
        assert receipt["result"] == "AUTHORITY_OR_PLAN_CHANGED_DURING_EFFECT"
        assert (workspace / "src" / "notes.py").read_bytes() == b"VALUE = 2\n"


def test_scope_guard_mutation_is_killed_by_safety_oracle() -> None:
    """Prove the out-of-scope safety oracle fails if its guard is bypassed."""
    with tempfile.TemporaryDirectory(prefix="tool-port-mutant-") as temp:
        control, workspace, command = fixture(Path(temp))
        mutant_target = workspace / "outside" / "notes.py"
        command = bind_plan_target(control, command, "outside/notes.py")
        command = ToolCommand(**{**command.__dict__, "expected_previous_sha256": None})
        def assert_outside_dispatch_is_rejected() -> None:
            try:
                dispatch_tool(control, workspace, command)
            except ToolDispatchHold as exc:
                assert "OUTSIDE_AUTHORIZED_ROOT" in str(exc)
                assert not mutant_target.exists()
                return
            raise AssertionError("out-of-scope dispatch was not rejected")
        with patch("tool_port._safe_target", side_effect=lambda root, target, roots: root / target):
            try:
                assert_outside_dispatch_is_rejected()
            except AssertionError:
                assert mutant_target.read_bytes() == b"VALUE = 2\n", "guard mutant did not reach physical oracle"
            else:
                raise AssertionError("safety oracle failed to detect seeded scope-guard mutation")


if __name__ == "__main__":
    tests = [test_physical_effect_and_receipt, test_out_of_scope_rejected_before_intent_or_effect,
             test_stale_plan_rejected_without_effect, test_interrupt_recovers_unknown_without_replay,
             test_recovery_rejects_corrupt_or_ambiguous_campaign_journal,
             test_workspace_location_and_pending_journal_fail_before_intent,
             test_goal_charter_binding_must_match_runtime_charter,
             test_material_campaign_or_non_temp_workspace_is_held,
             test_response_loss_after_effect_stays_unknown_without_replay,
             test_unrelated_source_drift_downgrades_receipt,
             test_public_cli_and_concurrent_revision_cas,
             test_installed_toolport_consumer_performs_bound_physical_effect,
             test_embedded_control_state_does_not_create_source_drift,
             test_expired_lease_and_precondition_fail_without_write,
             test_source_drift_and_hardlink_rejected_before_intent,
             test_canonical_control_exclusion_cannot_hide_source,
             test_traversal_and_symlink_boundaries_fail_before_intent,
             test_wrong_actor_and_mid_effect_plan_drift_fail_closed,
             test_scope_guard_mutation_is_killed_by_safety_oracle]
    skipped = []
    for test in tests:
        result = test()
        if isinstance(result, str) and result.startswith("SKIP:"):
            skipped.append((test.__name__, result))
            print(f"SKIP {test.__name__}: {result[5:].strip()}")
        else:
            print(f"PASS {test.__name__}")
    print(f"PASS portable ToolPort adversarial physical tests; skipped={len(skipped)}")
