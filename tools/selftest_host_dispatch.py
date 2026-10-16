#!/usr/bin/env python3
"""Focused failure tests for source-bound optional host dispatch."""
from __future__ import annotations

import json
import sys
import tempfile
import argparse
import contextlib
import io
import os
import shutil
import signal
import subprocess
import time
from io import BytesIO
from dataclasses import replace
from unittest.mock import patch
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from candidate_manifest import build_manifest
import campaignctl
from host_dispatch import (
    CodexCliHost,
    DispatchHold,
    EngineeringCommand,
    HostDispatchInterrupted,
    HostCapabilities,
    prepare_dispatch,
    recover_interrupted_dispatch,
    validate_command,
    _out_of_scope_changes,
    _write_roots_match,
    _archived_idempotency_exists,
    _find_archived_receipt,
    _terminate_process_tree,
    _mint_dispatch_permit,
    _consume_dispatch_permit,
)


def put(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def fixture(base: Path):
    control = base / "control"
    workspace = base / "workspace"
    workspace.mkdir()
    (workspace / "app.py").write_text("VALUE = 1\n", encoding="utf-8")
    (workspace / "src").mkdir()
    expires = (datetime.now(timezone.utc) + timedelta(minutes=20)).isoformat().replace("+00:00", "Z")
    campaign = "C-TEST"
    actor = "I3-TEST"
    run = "RUN-TEST"
    charter = {
        "schema_version": "campaign-charter-0.1",
        "campaign_id": campaign,
        "product_or_workstream": "fixture",
        "baseline_ref": "test-baseline",
        "resource_envelope": {
            "allowed_write_surfaces": ["src"],
            "protected_surfaces": [".git", "qa"],
            "external_authority_gates": [],
        },
    }
    charter_path = control / "campaigns" / campaign / "CHARTER.json"
    put(charter_path, charter)
    runtime = {
        "schema_version": "campaign-runtime-0.1",
        "campaign_id": campaign,
        "product_or_workstream": "fixture",
        "charter_ref": f"campaigns/{campaign}/CHARTER.json",
        "campaign_status": "ACTIVE",
        "revision": 3,
        "updated_at": "2026-10-14T00:00:00Z",
        "integrated_ref": "test-baseline",
        "current_checkpoint_id": None,
        "checkpoint_counter": 0,
        "review_freeze_counter": 0,
        "review_freeze": None,
        "terminal_request": None,
        "campaign_falsifiers": [],
        "work_units": [{
            "id": "W1", "title": "test work", "status": "ACTIVE", "priority": 1,
            "dependencies": [], "allowed_write_surfaces": ["src"], "shared_resources": [],
            "actor_id": actor, "run_id": run, "evidence_refs": [], "result_ref": None, "notes": [],
        }],
        "event_log": [],
    }
    put(control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json", runtime)
    put(control / "state" / "PRODUCT_STATE_CURRENT.json", {
        "product_or_workstream": "fixture",
        "active_campaign": {"campaign_id": campaign, "checkpoint_or_terminal_ref": None},
        "current_code_ref": "test-baseline",
        "currentness_set": [
            "runtime/CAMPAIGN_RUNTIME_CURRENT.json",
            "state/EXECUTION_AUTHORITY_CURRENT.json",
            "state/IDENTITY_REGISTRY_CURRENT.json",
        ],
    })
    put(control / "state" / "EXECUTION_AUTHORITY_CURRENT.json", {
        "schema_version": "execution-authority-0.1",
        "updated_at": "2026-10-14T00:00:00Z",
        "authority_status": "ACTIVE", "campaign_id": campaign,
        "campaign_lead_actor_id": actor, "current_run_id": run,
        "baseline_ref": "test-baseline", "checkpoint_ref": None,
        "allowed_write_surfaces": ["src"], "protected_surfaces": [".git", "qa"],
        "expires_at": expires,
    })
    put(control / "state" / "IDENTITY_REGISTRY_CURRENT.json", {
        "actors": [{"actor_id": actor, "role_class": "I3_ENGINEERING_CAMPAIGN_LEAD",
                    "status": "ACTIVE", "current_run_id": run}],
    })
    cmd = EngineeringCommand(
        campaign_id=campaign, actor_id=actor, run_id=run, work_unit_id="W1",
        source_tree_sha256=build_manifest(workspace)["source_tree_sha256"], runtime_revision=3,
        allowed_write_surfaces=("src",), idempotency_key="dispatch-1",
        max_cost_usd=1.0, prompt="Implement the approved local change.",
    )
    return control, workspace, cmd


class RefusingHost:
    def observe(self):
        return HostCapabilities(
            host="fixture", version="test", authenticated=True,
            workspace_write_mode_observed=True, write_boundary_enforced=False,
            enforced_write_roots=(), write_boundary_witness_sha256=None,
            per_command_cost_cap_enforced=False, thread_resume_observed=False,
            cost_cap_witness_sha256=None,
            support_classification="HOST_ADVISORY", limitations=("no enforced cap",),
        )

    def dispatch(self, command, workspace, *, permit=None):
        raise AssertionError("unsupported host must never receive a dispatch call")


class FailedProbeHost:
    def __init__(self, *, result=None, error=None):
        self.result = result
        self.error = error
        self.dispatch_called = False

    def observe(self):
        if self.error is not None:
            raise self.error
        return self.result

    def dispatch(self, command, workspace, *, permit=None):
        self.dispatch_called = True
        raise AssertionError("dispatch must not follow an invalid capability probe")


class ContractHost:
    """Interface-level test double; never counted as native host evidence."""
    def observe(self):
        return HostCapabilities(
            host="contract-test-double", version="1", authenticated=True,
            workspace_write_mode_observed=True, write_boundary_enforced=True,
            enforced_write_roots=("src",), write_boundary_witness_sha256="a" * 64,
            per_command_cost_cap_enforced=True, cost_cap_witness_sha256="b" * 64,
            thread_resume_observed=True,
            support_classification="HOST_VERIFIED", limitations=(),
        )

    def dispatch(self, command, workspace, *, permit=None):
        (workspace / "src" / "feature.py").write_text("def answer(): return 42\n", encoding="utf-8")
        return {
            "host_turn_id": "test-turn-001", "status": "completed",
            "provider_cost_usd": 0.0, "observed_commands": ["python -m pytest"],
        }


class FlappingProbeHost(ContractHost):
    def __init__(self, *, second_result=None, second_error=None):
        self.observations = 0
        self.second_result = second_result
        self.second_error = second_error
        self.dispatch_called = False

    def observe(self):
        self.observations += 1
        if self.observations == 1:
            return super().observe()
        if self.second_error is not None:
            raise self.second_error
        return self.second_result

    def dispatch(self, command, workspace, *, permit=None):
        self.dispatch_called = True
        return super().dispatch(command, workspace, permit=permit)


class SpyHost(ContractHost):
    def __init__(self):
        self.called = False

    def dispatch(self, command, workspace, *, permit=None):
        self.called = True
        return super().dispatch(command, workspace, permit=permit)


class RevokingHost(SpyHost):
    """Test double whose sandbox attestation is revoked before dispatch."""
    def __init__(self):
        super().__init__()
        self.observations = 0

    def observe(self):
        self.observations += 1
        capabilities = ContractHost.observe(self)
        if self.observations == 1:
            return capabilities
        return HostCapabilities(
            host=capabilities.host, version=capabilities.version,
            authenticated=capabilities.authenticated,
            workspace_write_mode_observed=capabilities.workspace_write_mode_observed,
            write_boundary_enforced=False, enforced_write_roots=(),
            write_boundary_witness_sha256=None,
            per_command_cost_cap_enforced=capabilities.per_command_cost_cap_enforced,
            cost_cap_witness_sha256=capabilities.cost_cap_witness_sha256,
            thread_resume_observed=capabilities.thread_resume_observed,
            support_classification="HOST_ADVISORY",
            limitations=("write boundary revoked during preparation",),
        )


class InterruptedHost(ContractHost):
    def dispatch(self, command, workspace, *, permit=None):
        del command, workspace
        raise HostDispatchInterrupted(
            "synthetic interruption after remote session started",
            host_turn_id="11111111-2222-4333-8444-555555555555",
        )


class SimulatedProcessCrash(BaseException):
    pass


class CrashingHost(ContractHost):
    def dispatch(self, command, workspace, *, permit=None):
        raise SimulatedProcessCrash("simulated process termination during host call")


class EscapingHost(ContractHost):
    def dispatch(self, command, workspace, *, permit=None):
        (workspace / "README.md").write_text("unauthorized change\n", encoding="utf-8")
        return {
            "host_turn_id": "escape-turn", "status": "completed",
            "provider_cost_usd": 0.0,
        }


class BroadSandboxHost(ContractHost):
    def observe(self):
        return HostCapabilities(
            host="too-broad-sandbox", version="1", authenticated=True,
            workspace_write_mode_observed=True, write_boundary_enforced=True,
            enforced_write_roots=(".",), write_boundary_witness_sha256="c" * 64,
            per_command_cost_cap_enforced=True, cost_cap_witness_sha256="d" * 64,
            thread_resume_observed=True, support_classification="HOST_VERIFIED", limitations=(),
        )


class StaleRuntimeHost(ContractHost):
    def __init__(self, control: Path):
        self.control = control

    def dispatch(self, command, workspace, *, permit=None):
        path = self.control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json"
        state = json.loads(path.read_text(encoding="utf-8"))
        state["revision"] += 1
        put(path, state)
        return {"host_turn_id": "stale-turn", "status": "completed", "provider_cost_usd": 0.0}


class ReplacementCampaignHost(ContractHost):
    def __init__(self, control: Path):
        self.control = control

    def dispatch(self, command, workspace, *, permit=None):
        replacement = {
            "schema_version": "campaign-runtime-0.1",
            "campaign_id": "C-REPLACEMENT", "campaign_status": "ACTIVE",
            "revision": 11,
            "event_log": [{"seq": 1, "action": "REPLACEMENT_SENTINEL", "details": {"keep": True}}],
            "work_units": [],
        }
        put(self.control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json", replacement)
        return {"host_turn_id": "replacement-turn", "status": "completed", "provider_cost_usd": 0.0}


class ReplacementCrashHost(ReplacementCampaignHost):
    def dispatch(self, command, workspace, *, permit=None):
        super().dispatch(command, workspace, permit=permit)
        raise SimulatedProcessCrash("interrupted after campaign runtime replacement")


class IdentityRevokingHost(ContractHost):
    def __init__(self, control: Path):
        self.control = control

    def dispatch(self, command, workspace, *, permit=None):
        path = self.control / "state" / "IDENTITY_REGISTRY_CURRENT.json"
        registry = json.loads(path.read_text(encoding="utf-8"))
        registry["actors"][0]["role_class"] = "I4_BUILDER"
        put(path, registry)
        return {"host_turn_id": "identity-revoked", "status": "completed", "provider_cost_usd": 0.0}


def verify_fixture_capabilities(capabilities, command, workspace) -> bool:
    """Test-only verifier; never a native-host enforcement claim."""
    del command, workspace
    return (capabilities.host in {"contract-test-double", "too-broad-sandbox", "codex-test-double"}
            and capabilities.authenticated is True
            and capabilities.write_boundary_enforced
            and capabilities.per_command_cost_cap_enforced)


def dispatch_with_fixture_verifier(control, workspace, command, host):
    return prepare_dispatch(control, workspace, command, host,
                            capability_verifier=verify_fixture_capabilities)


class CaptureInput(BytesIO):
    def close(self):
        self.was_closed = True


class FakeCliProcess:
    def __init__(self, stdout=b"", stderr=b"", returncode=0, timeout=False):
        self.stdin = CaptureInput()
        self.stdin.was_closed = False
        self.stdout = BytesIO(stdout)
        self.stderr = BytesIO(stderr)
        self.returncode = returncode
        self.timeout = timeout
        self.wait_calls = 0

    def wait(self, timeout=None):
        self.wait_calls += 1
        if self.timeout and self.wait_calls == 1:
            raise subprocess.TimeoutExpired(["codex-test-double"], timeout)
        return self.returncode

    def kill(self):
        self.returncode = -9


def main() -> int:
    # The descendant inherits both host pipes. Termination must stop the
    # whole tree, otherwise communicate() remains blocked after the parent exits.
    with tempfile.TemporaryDirectory(prefix="host-dispatch-process-tree-") as temp:
        marker = Path(temp) / "child.pid"
        child_code = "import time; time.sleep(120)"
        parent_code = (
            "import pathlib,subprocess,sys,time; "
            "child=subprocess.Popen([sys.executable,'-c',sys.argv[2]]); "
            "pathlib.Path(sys.argv[1]).write_text(str(child.pid)); time.sleep(120)"
        )
        process = subprocess.Popen(
            [sys.executable, "-c", parent_code, str(marker), child_code],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            start_new_session=(os.name != "nt"),
        )
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline and not marker.is_file():
            time.sleep(0.02)
        if not marker.is_file():
            process.kill()
            process.wait(timeout=5)
            raise AssertionError("process-tree fixture failed to start its descendant")
        child_pid = int(marker.read_text(encoding="utf-8"))
        if not _terminate_process_tree(process):
            raise AssertionError("host process-tree termination was not confirmed")
        try:
            process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            if os.name == "nt":
                taskkill = shutil.which("taskkill")
                if taskkill:
                    subprocess.run([taskkill, "/PID", str(child_pid), "/T", "/F"],
                                   capture_output=True, timeout=5, check=False)
            else:
                try:
                    os.kill(child_pid, signal.SIGKILL)
                except OSError:
                    pass
            raise AssertionError("descendant retained inherited host pipes after tree termination")

    # A failed/malformed probe occurs before the host boundary, but must still
    # produce a durable HOLD receipt without exposing raw provider error text.
    for suffix, host, expected_hold in (
        ("raises", FailedProbeHost(error=RuntimeError("private-token-must-not-leak")),
         "HOST_CAPABILITY_OBSERVATION_FAILED"),
        ("wrong-type", FailedProbeHost(result={"authenticated": True}),
         "HOST_CAPABILITIES_INVALID"),
    ):
        with tempfile.TemporaryDirectory(prefix=f"host-dispatch-probe-{suffix}-") as temp:
            control, workspace, cmd = fixture(Path(temp))
            try:
                dispatch_with_fixture_verifier(control, workspace, cmd, host)
            except DispatchHold as exc:
                receipt = json.loads(str(exc))
            else:
                raise AssertionError(f"{suffix} capability probe did not fail closed")
            assert receipt["phase"] == "HOLD"
            assert receipt["hold_code"] == expected_hold
            assert receipt["result"] == "NOT_DISPATCHED"
            assert receipt["host_turn_id"] is None
            assert receipt["host_capabilities"] == {"observation": "FAILED"}
            assert receipt["capability_observation_error_sha256"]
            assert "private-token-must-not-leak" not in str(receipt)
            assert host.dispatch_called is False
            assert (workspace / "app.py").read_text(encoding="utf-8") == "VALUE = 1\n"
            runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
            assert [event["action"] for event in runtime["event_log"]] == ["HOST_DISPATCH_HELD"]
            persisted = runtime["event_log"][0]["details"]
            assert persisted["dispatch_id"] == receipt["dispatch_id"]
            assert persisted["idempotency_key"] == cmd.idempotency_key

    for suffix, host in (
        ("raises", FlappingProbeHost(second_error=RuntimeError("second-probe-private-token"))),
        ("wrong-type", FlappingProbeHost(second_result={"authenticated": True})),
        ("malformed-fields", FlappingProbeHost(
            second_result=replace(ContractHost().observe(), enforced_write_roots=(42,))
        )),
    ):
        with tempfile.TemporaryDirectory(prefix=f"host-dispatch-boundary-probe-{suffix}-") as temp:
            control, workspace, cmd = fixture(Path(temp))
            try:
                dispatch_with_fixture_verifier(control, workspace, cmd, host)
            except DispatchHold as exc:
                receipt = json.loads(str(exc))
            else:
                raise AssertionError(f"{suffix} boundary probe did not fail closed")
            assert receipt["phase"] == "HOLD"
            assert receipt["hold_code"] == "HOST_CAPABILITY_OBSERVATION_FAILED_AT_DISPATCH_BOUNDARY"
            assert receipt["pre_dispatch_host_capabilities"] == {"observation": "FAILED"}
            assert receipt["pre_dispatch_capability_observation_error_sha256"]
            assert "second-probe-private-token" not in str(receipt)
            assert host.observations == 2 and host.dispatch_called is False
            assert (workspace / "app.py").read_text(encoding="utf-8") == "VALUE = 1\n"
            runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
            assert [event["action"] for event in runtime["event_log"]] == ["HOST_DISPATCH_HELD"]

    with tempfile.TemporaryDirectory(prefix="host-dispatch-a-") as temp:
        control, workspace, cmd = fixture(Path(temp))
        binding = validate_command(control, workspace, cmd)
        assert binding["source_tree_sha256"] == cmd.source_tree_sha256

        permit = _mint_dispatch_permit(cmd, workspace)
        try:
            _consume_dispatch_permit(permit, replace(cmd, prompt="changed command"), workspace)
        except DispatchHold as exc:
            assert "CONTROLLER_DISPATCH_PERMIT_BINDING_MISMATCH" in str(exc)
        else:
            raise AssertionError("controller permit accepted a changed command")
        try:
            _consume_dispatch_permit(permit, cmd, workspace)
        except DispatchHold as exc:
            assert "CONTROLLER_DISPATCH_PERMIT_ALREADY_CONSUMED" in str(exc)
        else:
            raise AssertionError("failed binding attempt left permit reusable")

        permit = _mint_dispatch_permit(cmd, workspace)
        _consume_dispatch_permit(permit, cmd, workspace)
        try:
            _consume_dispatch_permit(permit, cmd, workspace)
        except DispatchHold as exc:
            assert "CONTROLLER_DISPATCH_PERMIT_ALREADY_CONSUMED" in str(exc)
        else:
            raise AssertionError("controller permit was replayed")

        (workspace / "app.py").write_text("VALUE = 2\n", encoding="utf-8")
        try:
            validate_command(control, workspace, cmd)
        except DispatchHold as exc:
            assert "SOURCE_TREE_DRIFT" in str(exc)
        else:
            raise AssertionError("source drift was accepted")
        (workspace / "app.py").write_text("VALUE = 1\n", encoding="utf-8")

        expired = json.loads((control / "state" / "EXECUTION_AUTHORITY_CURRENT.json").read_text())
        expired["expires_at"] = "2020-01-01T00:00:00Z"
        put(control / "state" / "EXECUTION_AUTHORITY_CURRENT.json", expired)
        try:
            validate_command(control, workspace, cmd)
        except DispatchHold as exc:
            assert "LEASE_EXPIRED" in str(exc)
        else:
            raise AssertionError("expired authority lease was accepted")
        expired["expires_at"] = (datetime.now(timezone.utc) + timedelta(minutes=20)).isoformat().replace("+00:00", "Z")
        put(control / "state" / "EXECUTION_AUTHORITY_CURRENT.json", expired)
        naive = dict(expired)
        naive["expires_at"] = "2026-10-14T16:10:00"
        put(control / "state" / "EXECUTION_AUTHORITY_CURRENT.json", naive)
        try:
            validate_command(control, workspace, cmd)
        except DispatchHold as exc:
            assert "TIMEZONE_AWARE" in str(exc)
        else:
            raise AssertionError("timezone-naive lease expiry was accepted")
        put(control / "state" / "EXECUTION_AUTHORITY_CURRENT.json", expired)

        for bad_cost in (float("nan"), float("inf"), float("-inf"), 0.0, -1.0):
            bad = EngineeringCommand(**{**cmd.__dict__, "max_cost_usd": bad_cost})
            try:
                validate_command(control, workspace, bad)
            except DispatchHold as exc:
                assert "COST_CAP_REQUIRED" in str(exc)
            else:
                raise AssertionError(f"invalid cost cap was accepted: {bad_cost}")
        for bad_cost in (True, "1.0", None):
            bad = EngineeringCommand(**{**cmd.__dict__, "max_cost_usd": bad_cost})
            try:
                validate_command(control, workspace, bad)
            except DispatchHold:
                pass
            else:
                raise AssertionError(f"non-numeric or boolean cost cap was accepted: {bad_cost!r}")
        assert not _write_roots_match(("SRC",), ("src",))
        assert _out_of_scope_changes({"SRC/file.txt": "before"}, {"SRC/file.txt": "after"}, ("src",))

        denied = EngineeringCommand(**{**cmd.__dict__, "allowed_write_surfaces": ("src", "qa")})
        try:
            validate_command(control, workspace, denied)
        except DispatchHold as exc:
            assert "WRITE_SURFACE_OUTSIDE" in str(exc)
        else:
            raise AssertionError("out-of-envelope write surface was accepted")

        try:
            prepare_dispatch(control, workspace, cmd, RefusingHost())
        except DispatchHold as exc:
            assert "HOST_ENFORCEMENT_EVIDENCE_UNVERIFIED" in str(exc)
        else:
            raise AssertionError("host without permissions/cost cap was dispatched")
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        assert runtime["revision"] == 4
        assert runtime["event_log"][-1]["action"] == "HOST_DISPATCH_HELD"
        assert runtime["event_log"][-1]["details"]["provider_cost_usd"] == "UNKNOWN"

        current_revision = runtime["revision"]
        broad = EngineeringCommand(**{**cmd.__dict__, "runtime_revision": current_revision,
                                      "idempotency_key": "broad-sandbox"})
        try:
            dispatch_with_fixture_verifier(control, workspace, broad, BroadSandboxHost())
        except DispatchHold as exc:
            assert "HOST_SCOPE_OR_COST_CAP_NOT_ENFORCED" in str(exc)
        else:
            raise AssertionError("overbroad OS write roots were accepted")

        retry = EngineeringCommand(**{**cmd.__dict__, "runtime_revision": runtime["revision"]})
        try:
            prepare_dispatch(control, workspace, retry, RefusingHost())
        except DispatchHold as exc:
            assert "IDEMPOTENCY_KEY_ALREADY_RECORDED" in str(exc)
        else:
            raise AssertionError("ambiguous prior attempt was replayed")

        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        accepted_test_contract = EngineeringCommand(**{
            **cmd.__dict__, "runtime_revision": runtime["revision"], "idempotency_key": "dispatch-2",
        })
        observed = dispatch_with_fixture_verifier(control, workspace, accepted_test_contract, ContractHost())
        assert observed["phase"] == "OBSERVED"
        assert observed["host_turn_id"] == "test-turn-001"
        assert observed["source_tree_sha256_after"] != cmd.source_tree_sha256
        assert (workspace / "src" / "feature.py").read_text(encoding="utf-8").startswith("def answer")
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        actions = [entry["action"] for entry in runtime["event_log"]]
        assert actions[-2:] == ["HOST_DISPATCH_STARTED", "HOST_DISPATCH_OBSERVED"]

        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        escaped_command = EngineeringCommand(**{
            **accepted_test_contract.__dict__, "runtime_revision": runtime["revision"],
            "idempotency_key": "dispatch-escape",
            "source_tree_sha256": build_manifest(workspace)["source_tree_sha256"],
        })
        escaped = dispatch_with_fixture_verifier(control, workspace, escaped_command, EscapingHost())
        assert escaped["phase"] == "UNKNOWN"
        assert escaped["scope_violation"] == "OUT_OF_SCOPE_WRITE_DETECTED_EFFECT_ALREADY_OCCURRED"
        assert "README.md" in escaped["out_of_scope_paths"]

        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        stale_command = EngineeringCommand(**{
            **cmd.__dict__, "runtime_revision": runtime["revision"],
            "idempotency_key": "stale-revision",
            "source_tree_sha256": build_manifest(workspace)["source_tree_sha256"],
        })
        stale_result = dispatch_with_fixture_verifier(control, workspace, stale_command, StaleRuntimeHost(control))
        assert stale_result["phase"] == "UNKNOWN"
        assert stale_result["completion_binding_failure"] == "RUNTIME_REVISION_OR_CAMPAIGN_CHANGED_DURING_HOST_TURN"

        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        identity_command = EngineeringCommand(**{
            **cmd.__dict__, "runtime_revision": runtime["revision"],
            "idempotency_key": "identity-role-drift",
            "source_tree_sha256": build_manifest(workspace)["source_tree_sha256"],
        })
        identity_result = dispatch_with_fixture_verifier(control, workspace, identity_command, IdentityRevokingHost(control))
        assert identity_result["phase"] == "UNKNOWN"
        assert identity_result["completion_binding_failure"] == "CHARTER_AUTHORITY_OR_IDENTITY_CHANGED_DURING_HOST_TURN"
        put(control / "state" / "IDENTITY_REGISTRY_CURRENT.json", {
            "actors": [{"actor_id": "I3-TEST", "role_class": "I3_ENGINEERING_CAMPAIGN_LEAD",
                        "status": "ACTIVE", "current_run_id": "RUN-TEST"}],
        })

        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        crash_command = EngineeringCommand(**{
            **cmd.__dict__, "runtime_revision": runtime["revision"], "idempotency_key": "dispatch-crash",
            "source_tree_sha256": build_manifest(workspace)["source_tree_sha256"],
        })
        try:
            dispatch_with_fixture_verifier(control, workspace, crash_command, CrashingHost())
        except SimulatedProcessCrash:
            pass
        else:
            raise AssertionError("simulated process interruption did not interrupt")
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        orphan = runtime["event_log"][-1]["details"]
        assert runtime["event_log"][-1]["action"] == "HOST_DISPATCH_STARTED"
        recovered = recover_interrupted_dispatch(control, orphan["dispatch_id"])
        assert recovered["phase"] == "UNKNOWN"
        assert recovered["provider_cost_usd"] == "UNKNOWN"
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        assert runtime["event_log"][-1]["action"] == "HOST_DISPATCH_UNKNOWN"
        assert runtime["event_log"][-1]["details"]["result"] == "INTERRUPTED_RECEIPT_NOT_OBSERVED"
        try:
            retry_after_crash = EngineeringCommand(**{
                **crash_command.__dict__, "runtime_revision": runtime["revision"],
            })
            dispatch_with_fixture_verifier(control, workspace, retry_after_crash, ContractHost())
        except DispatchHold as exc:
            assert "IDEMPOTENCY_KEY_ALREADY_" in str(exc)
        else:
            raise AssertionError("interrupted host effect was replayed after recovery")

        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        replacement_command = EngineeringCommand(**{
            **cmd.__dict__, "runtime_revision": runtime["revision"],
            "idempotency_key": "campaign-replaced-during-host-turn",
            "source_tree_sha256": build_manifest(workspace)["source_tree_sha256"],
        })
        replaced = dispatch_with_fixture_verifier(control, workspace, replacement_command, ReplacementCampaignHost(control))
        assert replaced["phase"] == "UNKNOWN"
        assert replaced["campaign_runtime_replaced"] is True
        replacement_runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        assert replacement_runtime["campaign_id"] == "C-REPLACEMENT"
        assert replacement_runtime["revision"] == 11
        assert replacement_runtime["event_log"] == [{"seq": 1, "action": "REPLACEMENT_SENTINEL", "details": {"keep": True}}]
        archived = json.loads((control / replaced["receipt_archive"]).read_text(encoding="utf-8"))
        assert archived == json.loads(json.dumps(replaced))

        (workspace / "linked.py").symlink_to(workspace / "app.py")
        try:
            build_manifest(workspace)
        except Exception as exc:
            assert "symlink" in str(exc).lower()
        else:
            raise AssertionError("symlinked source escaped source binding")

    with tempfile.TemporaryDirectory(prefix="host-dispatch-replaced-recovery-") as temp:
        control, workspace, cmd = fixture(Path(temp))
        try:
            dispatch_with_fixture_verifier(control, workspace, cmd, ReplacementCrashHost(control))
        except SimulatedProcessCrash:
            pass
        else:
            raise AssertionError("runtime replacement interruption did not interrupt")
        replacement_runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        assert replacement_runtime["campaign_id"] == "C-REPLACEMENT"
        archived_path = next((control / "campaigns" / "_host_dispatch_receipts").glob("*/*.json"))
        interrupted_receipt = json.loads(archived_path.read_text(encoding="utf-8"))
        recovered = recover_interrupted_dispatch(control, interrupted_receipt["dispatch_id"])
        assert recovered["phase"] == "UNKNOWN"
        assert recovered["result"] == "INTERRUPTED_CAMPAIGN_RUNTIME_REPLACED"
        replacement_runtime_after = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        assert replacement_runtime_after == replacement_runtime

    with tempfile.TemporaryDirectory(prefix="host-dispatch-archive-reconcile-") as temp:
        control, workspace, cmd = fixture(Path(temp))
        completed = dispatch_with_fixture_verifier(control, workspace, cmd, ContractHost())
        assert completed["phase"] == "OBSERVED"
        assert _archived_idempotency_exists(control, "C-TEST", cmd.idempotency_key)
        assert not _archived_idempotency_exists(control, "C-OTHER", cmd.idempotency_key)
        runtime_path = control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json"
        runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
        start = next(event for event in runtime["event_log"] if event["action"] == "HOST_DISPATCH_STARTED")
        runtime["revision"] = cmd.runtime_revision + 1
        runtime["event_log"] = [start]
        put(runtime_path, runtime)
        recovered = recover_interrupted_dispatch(control, completed["dispatch_id"])
        assert recovered["phase"] == "OBSERVED"
        runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
        assert runtime["event_log"][-1]["action"] == "HOST_DISPATCH_OBSERVED"

        runtime["event_log"][-1]["details"]["host_turn_id"] = "tampered-runtime-receipt"
        put(runtime_path, runtime)
        try:
            recover_interrupted_dispatch(control, completed["dispatch_id"])
        except DispatchHold as exc:
            assert "ARCHIVED_RECEIPT_RUNTIME_CONFLICT" in str(exc)
        else:
            raise AssertionError("runtime receipt diverging from the durable archive was accepted")

        runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
        runtime["event_log"] = []
        put(runtime_path, runtime)
        retry = EngineeringCommand(**{
            **cmd.__dict__, "runtime_revision": runtime["revision"],
            "source_tree_sha256": build_manifest(workspace)["source_tree_sha256"],
        })
        try:
            dispatch_with_fixture_verifier(control, workspace, retry, ContractHost())
        except DispatchHold as exc:
            assert "IDEMPOTENCY_KEY_ALREADY_ARCHIVED" in str(exc)
        else:
            raise AssertionError("archived idempotency key was replayed after log reset")

        charter_path = control / "campaigns" / "C-TEST" / "CHARTER.json"
        charter = json.loads(charter_path.read_text(encoding="utf-8"))
        charter["baseline_ref"] = "same-id-new-charter-incarnation"
        put(charter_path, charter)
        runtime_before_recovery = json.loads(runtime_path.read_text(encoding="utf-8"))
        try:
            recover_interrupted_dispatch(control, completed["dispatch_id"])
        except DispatchHold as exc:
            assert "ARCHIVED_RECEIPT_CAMPAIGN_BINDING_MISMATCH" in str(exc)
        else:
            raise AssertionError("archived receipt attached to a same-id campaign with a different charter")
        assert json.loads(runtime_path.read_text(encoding="utf-8")) == runtime_before_recovery

    with tempfile.TemporaryDirectory(prefix="host-dispatch-unverified-witness-") as temp:
        control, workspace, cmd = fixture(Path(temp))
        for invalid_id in ("../runtime/escape", "..\\..\\runtime\\escape", "a" * 36):
            try:
                recover_interrupted_dispatch(control, invalid_id)
            except DispatchHold as exc:
                assert "INVALID_DISPATCH_ID" in str(exc)
            else:
                raise AssertionError("non-UUID dispatch id was accepted")
        host = SpyHost()
        try:
            prepare_dispatch(control, workspace, cmd, host)
        except DispatchHold as exc:
            assert "HOST_ENFORCEMENT_EVIDENCE_UNVERIFIED" in str(exc)
        else:
            raise AssertionError("self-asserted host witnesses were accepted without a trusted verifier")
        assert not host.called

    with tempfile.TemporaryDirectory(prefix="host-dispatch-revoked-capability-") as temp:
        control, workspace, cmd = fixture(Path(temp))
        host = RevokingHost()
        try:
            dispatch_with_fixture_verifier(control, workspace, cmd, host)
        except DispatchHold as exc:
            denial = json.loads(str(exc))
            assert denial["hold_code"] == "HOST_CAPABILITIES_CHANGED_BEFORE_DISPATCH"
            assert denial["pre_dispatch_capability_evidence_verified"] is False
        else:
            raise AssertionError("revoked host boundary reached dispatch")
        assert host.observations == 2
        assert not host.called
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        assert runtime["event_log"][-1]["action"] == "HOST_DISPATCH_HELD"
        assert runtime["event_log"][-1]["details"]["hold_code"] == "HOST_CAPABILITIES_CHANGED_BEFORE_DISPATCH"

    with tempfile.TemporaryDirectory(prefix="host-dispatch-cli-adapter-") as temp:
        control, workspace, cmd = fixture(Path(temp))
        cli = CodexCliHost(executable="codex-test-double", timeout_seconds=3)
        test_caps = HostCapabilities(
            host="codex-test-double", version="test", authenticated=True,
            workspace_write_mode_observed=True, write_boundary_enforced=True,
            enforced_write_roots=("src",), write_boundary_witness_sha256="a" * 64,
            per_command_cost_cap_enforced=True, cost_cap_witness_sha256="b" * 64,
            thread_resume_observed=True, support_classification="HOST_VERIFIED", limitations=(),
        )
        cli_events = "\n".join((
            json.dumps({"type": "thread.started", "thread_id": "11111111-2222-4333-8444-555555555555"}),
            json.dumps({"type": "item.started", "item": {"id": "cmd-1", "type": "command_execution", "command": "python -c secret"}}),
            json.dumps({"type": "item.completed", "item": {"id": "cmd-1", "type": "command_execution", "command": "python -c secret"}}),
            json.dumps({"type": "turn.completed"}),
        )).encode("utf-8")
        with patch("host_dispatch.subprocess.Popen") as invoke:
            invoke.return_value = FakeCliProcess(stdout=cli_events)
            try:
                cli.dispatch(cmd, workspace)
            except DispatchHold as exc:
                assert "CONTROLLER_DISPATCH_PERMIT_REQUIRED" in str(exc)
            else:
                raise AssertionError("direct CLI dispatch bypassed the controller permit")
            invoke.assert_not_called()
            invoke.return_value = FakeCliProcess(stdout=cli_events)
            with patch.object(cli, "observe", return_value=test_caps):
                result = dispatch_with_fixture_verifier(control, workspace, cmd, cli)
        argv = invoke.call_args.args[0]
        agent_prompt = invoke.return_value.stdin.getvalue().decode("utf-8")
        assert result["host_turn_id"] == "11111111-2222-4333-8444-555555555555"
        assert result["phase"] == "OBSERVED" and result["provider_cost_usd"] == "UNKNOWN"
        assert result["observed_command_count"] == 1
        assert "workspace-write" in argv and "--json" in argv and "-" == argv[-1]
        assert "--dangerously-bypass-approvals-and-sandbox" not in argv
        assert cmd.source_tree_sha256 in agent_prompt and "src" in agent_prompt

    with tempfile.TemporaryDirectory(prefix="host-dispatch-cli-incomplete-turn-") as temp:
        control, workspace, cmd = fixture(Path(temp))
        cli = CodexCliHost(executable="codex-test-double", timeout_seconds=3)
        test_caps = HostCapabilities(
            host="codex-test-double", version="test", authenticated=True,
            workspace_write_mode_observed=True, write_boundary_enforced=True,
            enforced_write_roots=("src",), write_boundary_witness_sha256="a" * 64,
            per_command_cost_cap_enforced=True, cost_cap_witness_sha256="b" * 64,
            thread_resume_observed=True, support_classification="HOST_VERIFIED", limitations=(),
        )
        with patch("host_dispatch.subprocess.Popen") as invoke:
            invoke.return_value = FakeCliProcess(stdout=(json.dumps({
                "type": "thread.started", "thread_id": "incomplete-turn",
            }) + "\n").encode())
            with patch.object(cli, "observe", return_value=test_caps):
                incomplete = dispatch_with_fixture_verifier(control, workspace, cmd, cli)
        assert incomplete["phase"] == "UNKNOWN" and incomplete["host_status"] == "unknown"

    with tempfile.TemporaryDirectory(prefix="host-dispatch-cli-output-cap-") as temp:
        control, workspace, cmd = fixture(Path(temp))
        cli = CodexCliHost(executable="codex-test-double", timeout_seconds=3)
        test_caps = HostCapabilities(
            host="codex-test-double", version="test", authenticated=True,
            workspace_write_mode_observed=True, write_boundary_enforced=True,
            enforced_write_roots=("src",), write_boundary_witness_sha256="a" * 64,
            per_command_cost_cap_enforced=True, cost_cap_witness_sha256="b" * 64,
            thread_resume_observed=True, support_classification="HOST_VERIFIED", limitations=(),
        )
        over_limit = (json.dumps({
            "type": "thread.started", "thread_id": "overflow-session",
        }) + "\n").encode() + b"x" * (cli.MAX_OUTPUT_BYTES + 1)
        with patch("host_dispatch.subprocess.Popen") as invoke:
            invoke.return_value = FakeCliProcess(stdout=over_limit)
            with patch.object(cli, "observe", return_value=test_caps):
                overflow = dispatch_with_fixture_verifier(control, workspace, cmd, cli)
        assert overflow["phase"] == "UNKNOWN"
        assert overflow["host_turn_id"] == "overflow-session"
        assert overflow["error_class"] == "HostDispatchInterrupted"
        assert invoke.return_value.returncode == -9

        timeout_output = json.dumps({
            "type": "thread.started", "thread_id": "11111111-2222-4333-8444-555555555555",
        }).encode("utf-8") + b"\n"
        with tempfile.TemporaryDirectory(prefix="host-dispatch-cli-timeout-recovery-") as temp:
            control, workspace, cmd = fixture(Path(temp))
            with patch("host_dispatch.subprocess.Popen") as invoke:
                invoke.return_value = FakeCliProcess(stdout=timeout_output, timeout=True)
                with patch.object(cli, "observe", return_value=test_caps):
                    interrupted = dispatch_with_fixture_verifier(control, workspace, cmd, cli)
            assert interrupted["phase"] == "UNKNOWN"
            assert interrupted["host_turn_id"] == "11111111-2222-4333-8444-555555555555"
            recovered = recover_interrupted_dispatch(control, interrupted["dispatch_id"])
            assert recovered["host_turn_id"] == "11111111-2222-4333-8444-555555555555"
            assert recovered["phase"] == "UNKNOWN"

    with tempfile.TemporaryDirectory(prefix="host-dispatch-interruption-session-receipt-") as temp:
        control, workspace, cmd = fixture(Path(temp))
        result = dispatch_with_fixture_verifier(control, workspace, cmd, InterruptedHost())
        assert result["phase"] == "UNKNOWN"
        assert result["host_turn_id"] == "11111111-2222-4333-8444-555555555555"
        recovered = recover_interrupted_dispatch(control, result["dispatch_id"])
        assert recovered["host_turn_id"] == "11111111-2222-4333-8444-555555555555"

    with tempfile.TemporaryDirectory(prefix="host-dispatch-verifier-revoked-") as temp:
        control, workspace, cmd = fixture(Path(temp))
        host = SpyHost()
        verifier_calls = 0

        def revoking_verifier(capabilities, command, target):
            nonlocal verifier_calls
            verifier_calls += 1
            if verifier_calls == 1:
                return verify_fixture_capabilities(capabilities, command, target)
            return False

        try:
            prepare_dispatch(control, workspace, cmd, host, capability_verifier=revoking_verifier)
        except DispatchHold as exc:
            denial = json.loads(str(exc))
            assert denial["hold_code"] == "HOST_CAPABILITIES_CHANGED_BEFORE_DISPATCH"
            assert denial["pre_dispatch_capability_evidence_verified"] is False
        else:
            raise AssertionError("revoked capability verifier still allowed dispatch")
        assert verifier_calls == 2
        assert not host.called
        runtime = json.loads((control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_text())
        assert [event["action"] for event in runtime["event_log"]] == ["HOST_DISPATCH_HELD"]
        assert (workspace / "app.py").read_text(encoding="utf-8") == "VALUE = 1\n"

    with tempfile.TemporaryDirectory(prefix="host-dispatch-goal-guard-") as temp:
        control, workspace, _ = fixture(Path(temp))
        args = argparse.Namespace(control_root=str(control), workspace=str(workspace),
                                  command=str(control / "unused-command.json"))
        captured = io.StringIO()
        try:
            with contextlib.redirect_stderr(captured):
                campaignctl.cmd_host_dispatch(args)
        except campaignctl.CampaignError as exc:
            assert "Goal Guard did not issue" in str(exc)
            assert "GOAL_GUARD_DENIED_OR_UNAVAILABLE" in captured.getvalue()
        else:
            raise AssertionError("campaignctl host route bypassed unavailable Goal Guard")

    with tempfile.TemporaryDirectory(prefix="host-dispatch-archive-symlink-") as temp:
        control, workspace, _ = fixture(Path(temp))
        campaigns = control / "campaigns"
        campaigns.rename(control / "campaigns-original")
        external = Path(temp) / "external-campaigns"
        external.mkdir()
        campaigns.symlink_to(external, target_is_directory=True)
        for check in (
            lambda: _find_archived_receipt(control, "00000000-0000-0000-0000-000000000000"),
            lambda: _archived_idempotency_exists(control, "C-TEST", "archive-key"),
        ):
            try:
                check()
            except DispatchHold as exc:
                assert "RECEIPT_ARCHIVE_PATH_UNSAFE" in str(exc)
            else:
                raise AssertionError("receipt archive reader followed an ancestor symlink")

    caps = CodexCliHost().observe()
    assert caps.support_classification in {"HOST_ADVISORY", "UNSUPPORTED"}
    assert not caps.write_boundary_enforced and not caps.per_command_cost_cap_enforced
    print("HOST DISPATCH BINDING / RECOVERY / RECEIPT SELF-TEST PASSED (native host remains unproven)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
