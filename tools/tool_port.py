#!/usr/bin/env python3
"""Consumer-backed portable deterministic ToolPort.

This is a disposable synthetic-workspace adapter, not a model host, sandbox,
Goal permission, or native execution permit. It supports one reversible UTF-8
file replacement operation whose target is bound to the current campaign,
Goal, Plan, actor, lease, source tree and idempotency key. Ambiguous starts are
never replayed.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

import campaignctl
import goal_guard
from candidate_manifest import ManifestError, build_manifest, canonical_tree_digest
from state_tx import atomic_json, fsync_dir, sha256_file, state_lock


class ToolDispatchHold(RuntimeError):
    pass


class ToolDispatchInterrupted(ToolDispatchHold):
    """Adapter stopped after durable start; effect status must be reconciled."""


@dataclass(frozen=True)
class ToolCommand:
    campaign_id: str
    actor_id: str
    run_id: str
    work_unit_id: str
    runtime_revision: int
    source_tree_sha256: str
    workspace_path_sha256: str
    goal_sha256: str
    plan_sha256: str
    allowed_write_surfaces: tuple[str, ...]
    idempotency_key: str
    operation_id: str
    target: str
    content_utf8: str
    expected_previous_sha256: str | None


@dataclass(frozen=True)
class ToolCapabilities:
    adapter_id: str
    adapter_version: str
    support_classification: str
    identity_evidence: str
    operations: tuple[str, ...]
    provider_invocation: bool
    cost_status: str
    effect_boundary: str
    limitations: tuple[str, ...]


class ToolPort(Protocol):
    def observe(self) -> ToolCapabilities: ...
    def execute(self, command: ToolCommand, workspace: Path) -> dict[str, Any]: ...


class PortableTestAdapter:
    """Fixed built-in adapter; it has no shell, import, or provider operation."""

    adapter_id = "portable-test-v1"

    def observe(self) -> ToolCapabilities:
        return ToolCapabilities(
            adapter_id=self.adapter_id,
            adapter_version="1",
            support_classification="PORTABLE_TEST_ADAPTER",
            identity_evidence="LOCAL_CAMPAIGN_STATE_ONLY_NOT_HUMAN_AUTHENTICATION",
            operations=("write_text",),
            provider_invocation=False,
            cost_status="NOT_APPLICABLE_NOT_MEASURED",
            effect_boundary="EXPLICIT_TEST_CHARTER_ROOTS_WITH_CONTROL_AND_WORKSPACE_WITHIN_OS_TEMP",
            limitations=(
                "synthetic test campaigns only; requires explicit charter flag and both control and workspace below OS temp root",
                "not an OS sandbox; non-cooperating local processes are outside this adapter boundary",
                "no shell, arbitrary process, network, credential, or provider operation",
            ),
        )

    def execute(self, command: ToolCommand, workspace: Path) -> dict[str, Any]:
        if command.operation_id != "write_text":
            raise ToolDispatchHold("TOOL_OPERATION_NOT_REGISTERED")
        target = _safe_target(workspace, command.target, command.allowed_write_surfaces)
        previous = _regular_file_sha(target) if target.exists() else None
        if previous != command.expected_previous_sha256:
            raise ToolDispatchHold("TOOL_TARGET_PRECONDITION_FAILED")
        encoded = command.content_utf8.encode("utf-8", errors="strict")
        if len(encoded) > 2 * 1024 * 1024:
            raise ToolDispatchHold("TOOL_CONTENT_LIMIT_EXCEEDED")
        target.parent.mkdir(parents=True, exist_ok=True)
        _verify_parent_chain(workspace, target.parent)
        if target.exists():
            _regular_file_sha(target)
        temp = target.with_name(f".{target.name}.{uuid.uuid4().hex}.tooltmp")
        try:
            fd = os.open(temp, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            with os.fdopen(fd, "wb") as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            _verify_parent_chain(workspace, target.parent)
            if target.exists() and _regular_file_sha(target) != command.expected_previous_sha256:
                raise ToolDispatchHold("TOOL_TARGET_CHANGED_BEFORE_REPLACE")
            os.replace(temp, target)
            fsync_dir(target.parent)
        finally:
            temp.unlink(missing_ok=True)
        observed = _regular_file_sha(target)
        if observed != hashlib.sha256(encoded).hexdigest():
            raise ToolDispatchHold("TOOL_PHYSICAL_READBACK_MISMATCH")
        return {"status": "completed", "effect": "file_replaced", "target": command.target,
                "previous_sha256": previous, "content_sha256": observed,
                "bytes_written": len(encoded)}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _read_json(path: Path, max_bytes: int = 32 * 1024 * 1024) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > max_bytes:
        raise ToolDispatchHold("UNTRUSTED_OR_MISSING_CONTROL_FILE")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ToolDispatchHold("CONTROL_FILE_NOT_OBJECT")
    return value


def _control_file(control: Path, relative: str) -> Path:
    try:
        return goal_guard.fixed_control_path(control, relative)
    except goal_guard.GoalGuardError as exc:
        raise ToolDispatchHold("UNTRUSTED_CONTROL_PATH") from exc


def _safe_target(workspace: Path, target: str, roots: tuple[str, ...]) -> Path:
    if (not isinstance(target, str) or not target or len(target) > 500 or "\\" in target
        or ":" in target or Path(target).is_absolute()
        or any(part in {"", ".", ".."} for part in target.split("/"))):
        raise ToolDispatchHold("INVALID_TOOL_TARGET")
    if not any(target == root or target.startswith(root.rstrip("/") + "/") for root in roots):
        raise ToolDispatchHold("TOOL_TARGET_OUTSIDE_AUTHORIZED_ROOT")
    root = workspace.resolve(strict=True)
    result = root / target
    _verify_parent_chain(root, result.parent)
    if result.is_symlink():
        raise ToolDispatchHold("SYMLINKED_TOOL_TARGET")
    if result.exists():
        _regular_file_sha(result)
    if not result.resolve(strict=False).is_relative_to(root):
        raise ToolDispatchHold("TOOL_TARGET_ESCAPES_WORKSPACE")
    return result


def _verify_parent_chain(root: Path, parent: Path) -> None:
    root = root.resolve(strict=True)
    try:
        rel = parent.relative_to(root)
    except ValueError as exc:
        raise ToolDispatchHold("TOOL_TARGET_ESCAPES_WORKSPACE") from exc
    cursor = root
    for component in rel.parts:
        cursor = cursor / component
        if cursor.is_symlink():
            raise ToolDispatchHold("SYMLINKED_TOOL_PARENT")
        if cursor.exists() and not cursor.is_dir():
            raise ToolDispatchHold("NON_DIRECTORY_TOOL_PARENT")
        if cursor.exists() and not cursor.resolve(strict=True).is_relative_to(root):
            raise ToolDispatchHold("TOOL_PARENT_ESCAPES_WORKSPACE")


def _regular_file_sha(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise ToolDispatchHold("TOOL_TARGET_NOT_REGULAR_FILE")
    stat = path.stat()
    if stat.st_nlink != 1:
        raise ToolDispatchHold("HARDLINKED_TOOL_TARGET")
    digest = sha256_file(path)
    if digest is None:
        raise ToolDispatchHold("TOOL_TARGET_UNREADABLE")
    return digest


def _source_tree_digest(workspace: Path, control: Path, *,
                        exclude_target: str | None = None,
                        allowed_roots: tuple[str, ...] = ()) -> str:
    """Bind product source while excluding the canonical embedded control root."""
    workspace = workspace.resolve(strict=True)
    control = control.resolve(strict=True)
    try:
        control_relative = control.relative_to(workspace).as_posix().rstrip("/")
    except ValueError:
        manifest = build_manifest(workspace)
        control_exclusions: tuple[str, ...] = ()
    else:
        if not control_relative:
            raise ToolDispatchHold("CONTROL_ROOT_CANNOT_BE_WORKSPACE_ROOT")
        if control_relative.casefold() != ".agentic-sdlc":
            raise ToolDispatchHold("NONCANONICAL_EMBEDDED_CONTROL_ROOT")
        control_exclusions = (".agentic-sdlc",)
        manifest = build_manifest(workspace, exclude_paths=control_exclusions)
    if exclude_target is not None:
        target_path = _safe_target(workspace, exclude_target, allowed_roots)
        target_key = os.path.normcase(str(target_path.resolve(strict=False)))
        entries = [entry for entry in manifest["files"]
                   if os.path.normcase(str(workspace / entry["path"])) != target_key]
        return canonical_tree_digest(entries)
    return manifest["source_tree_sha256"]


def _validate_command_shape(command: ToolCommand) -> None:
    for name in ("campaign_id", "actor_id", "run_id", "work_unit_id", "source_tree_sha256",
                 "goal_sha256", "plan_sha256", "idempotency_key", "operation_id", "target",
                 "content_utf8"):
        value = getattr(command, name)
        if not isinstance(value, str) or not value or len(value) > 2 * 1024 * 1024:
            raise ToolDispatchHold("TOOL_COMMAND_FIELD_INVALID:" + name)
    if type(command.runtime_revision) is not int or command.runtime_revision < 0:
        raise ToolDispatchHold("TOOL_RUNTIME_REVISION_INVALID")
    if (not isinstance(command.allowed_write_surfaces, tuple) or not command.allowed_write_surfaces
        or any(not isinstance(root, str) or not root for root in command.allowed_write_surfaces)
        or len(set(command.allowed_write_surfaces)) != len(command.allowed_write_surfaces)):
        raise ToolDispatchHold("TOOL_WRITE_SURFACES_INVALID")
    for digest in (command.source_tree_sha256, command.workspace_path_sha256,
                   command.goal_sha256, command.plan_sha256):
        if not re.fullmatch(r"[a-f0-9]{64}", digest):
            raise ToolDispatchHold("INVALID_SOURCE_OR_AUTHORITY_DIGEST")
    if (command.expected_previous_sha256 is not None
        and (not isinstance(command.expected_previous_sha256, str)
             or not re.fullmatch(r"[a-f0-9]{64}", command.expected_previous_sha256))):
        raise ToolDispatchHold("TOOL_PRECONDITION_DIGEST_INVALID")
    if len(command.idempotency_key) > 200 or command.operation_id != "write_text":
        raise ToolDispatchHold("TOOL_COMMAND_OPERATION_OR_IDEMPOTENCY_INVALID")


def _authority_binding(control: Path, workspace: Path, command: ToolCommand,
                       *, expected_revision: int, verify_source: bool = True) -> dict[str, Any]:
    if (not re.fullmatch(r"[a-f0-9]{64}", command.source_tree_sha256)
        or not re.fullmatch(r"[a-f0-9]{64}", command.goal_sha256)
        or not re.fullmatch(r"[a-f0-9]{64}", command.plan_sha256)):
        raise ToolDispatchHold("INVALID_SOURCE_OR_AUTHORITY_DIGEST")
    runtime = _read_json(_control_file(control, "runtime/CAMPAIGN_RUNTIME_CURRENT.json"))
    authority = _read_json(_control_file(control, "state/EXECUTION_AUTHORITY_CURRENT.json"))
    identity = _read_json(_control_file(control, "state/IDENTITY_REGISTRY_CURRENT.json"))
    _validate_runtime_event_log(runtime)
    campaignctl.require_campaign_active(runtime)
    _control_file(control, "state/PRODUCT_STATE_CURRENT.json")
    campaignctl.require_product_state_matches_runtime(control, runtime)
    charter_ref = runtime.get("charter_ref")
    if not isinstance(charter_ref, str):
        raise ToolDispatchHold("CHARTER_REFERENCE_INVALID")
    charter_safe_path = _control_file(control, charter_ref)
    charter_path, charter = campaignctl.read_charter(control, runtime)
    if charter_path.resolve(strict=True) != charter_safe_path.resolve(strict=True):
        raise ToolDispatchHold("CHARTER_REFERENCE_ESCAPES_CONTROL_ROOT")
    if charter.get("resource_envelope", {}).get("portable_test_adapter_only") is not True:
        raise ToolDispatchHold("PORTABLE_ADAPTER_NOT_EXPLICITLY_TEST_ONLY")
    if (runtime.get("campaign_id") != command.campaign_id
        or runtime.get("revision") != expected_revision
        or authority.get("campaign_id") != command.campaign_id
        or authority.get("authority_status") != "ACTIVE"
        or authority.get("campaign_lead_actor_id") != command.actor_id
        or authority.get("current_run_id") != command.run_id
        or authority.get("baseline_ref") != charter.get("baseline_ref")
        or authority.get("checkpoint_ref") != runtime.get("current_checkpoint_id")):
        raise ToolDispatchHold("CAMPAIGN_OR_AUTHORITY_BINDING_MISMATCH")
    try:
        expires = datetime.fromisoformat(authority["expires_at"].replace("Z", "+00:00"))
    except (KeyError, TypeError, ValueError) as exc:
        raise ToolDispatchHold("EXECUTION_LEASE_EXPIRY_INVALID") from exc
    if expires.tzinfo is None or expires.utcoffset() is None or expires <= datetime.now(timezone.utc):
        raise ToolDispatchHold("EXECUTION_LEASE_EXPIRED")
    actors = [entry for entry in identity.get("actors", []) if entry.get("actor_id") == command.actor_id]
    if (len(actors) != 1 or actors[0].get("role_class") != "I3_ENGINEERING_CAMPAIGN_LEAD"
        or actors[0].get("status") != "ACTIVE" or actors[0].get("current_run_id") != command.run_id):
        raise ToolDispatchHold("ACTOR_IDENTITY_OR_RUN_MISMATCH")
    units = [entry for entry in runtime.get("work_units", []) if entry.get("id") == command.work_unit_id]
    if (len(units) != 1 or units[0].get("status") != "ACTIVE"
        or units[0].get("actor_id") != command.actor_id or units[0].get("run_id") != command.run_id):
        raise ToolDispatchHold("WORK_UNIT_NOT_ACTIVE_FOR_ACTOR_RUN")
    unit = units[0]
    charter_roots = set(charter.get("resource_envelope", {}).get("allowed_write_surfaces", []))
    allowed = (set(command.allowed_write_surfaces)
               & set(unit.get("allowed_write_surfaces", []))
               & set(authority.get("allowed_write_surfaces", [])) & charter_roots)
    if not command.allowed_write_surfaces or set(command.allowed_write_surfaces) != allowed:
        raise ToolDispatchHold("WRITE_SURFACE_OUTSIDE_AUTHORIZED_INTERSECTION")
    _safe_target(workspace, command.target, tuple(allowed))
    operations = charter.get("resource_envelope", {}).get("allowed_tool_operations", [])
    if command.operation_id not in operations or command.operation_id != "write_text":
        raise ToolDispatchHold("TOOL_OPERATION_NOT_AUTHORIZED_BY_CHARTER")
    source = _source_tree_digest(workspace, control)
    source_without_target = _source_tree_digest(workspace, control,
        exclude_target=command.target, allowed_roots=tuple(allowed))
    if verify_source and source != command.source_tree_sha256:
        raise ToolDispatchHold("SOURCE_TREE_DRIFT")
    goal_path = _control_file(control, "state/GOAL_CONTRACT_CURRENT.json")
    plan_path = _control_file(control, "runtime/TACTICAL_PLAN_CURRENT.json")
    goal = _read_json(goal_path, 1024 * 1024)
    plan = _read_json(plan_path, 1024 * 1024)
    goal_digest = goal_guard.goal_fingerprint(goal)
    for reference, expected_sha in goal.get("authority_refs", {}).items():
        try:
            authority_ref = goal_guard.confined(control, reference)
        except (goal_guard.GoalGuardError, TypeError) as exc:
            raise ToolDispatchHold("GOAL_AUTHORITY_REFERENCE_INVALID") from exc
        if not authority_ref.is_file() or sha256_file(authority_ref) != expected_sha:
            raise ToolDispatchHold("GOAL_AUTHORITY_REFERENCE_STALE")
    if hashlib.sha256(goal_path.read_bytes()).hexdigest() != command.goal_sha256:
        raise ToolDispatchHold("GOAL_SOURCE_DRIFT")
    if hashlib.sha256(plan_path.read_bytes()).hexdigest() != command.plan_sha256:
        raise ToolDispatchHold("PLAN_SOURCE_DRIFT")
    if (goal_digest != plan.get("goal_digest") or goal.get("campaign_id") != command.campaign_id
        or plan.get("campaign_id") != command.campaign_id
        or plan.get("schema_version") != goal_guard.PLAN_SCHEMA
        or type(plan.get("revision")) is not int or plan["revision"] < 0
        or plan.get("reviewed_runtime_revision") != command.runtime_revision
        or plan.get("reviewed_runtime_event_seq") != command.runtime_revision
        or plan.get("invocation_permit_issued") is not False):
        raise ToolDispatchHold("GOAL_PLAN_BINDING_INVALID")
    if not set(command.allowed_write_surfaces) <= set(goal.get("write_envelope", [])):
        raise ToolDispatchHold("TOOL_WRITE_SURFACE_OUTSIDE_GOAL_ENVELOPE")
    steps = plan.get("steps")
    if not isinstance(steps, list) or not any(
        isinstance(step, dict) and step.get("tool_operation") == command.operation_id
        and step.get("target") == command.target for step in steps
    ):
        raise ToolDispatchHold("TOOL_ACTION_NOT_IN_CURRENT_TACTICAL_PLAN")
    evidence_ref = plan.get("review_evidence_ref")
    evidence_digest = plan.get("review_evidence_sha256")
    try:
        evidence = goal_guard.confined(control, evidence_ref)
    except (goal_guard.GoalGuardError, TypeError) as exc:
        raise ToolDispatchHold("TACTICAL_REVIEW_EVIDENCE_INVALID") from exc
    if not evidence.is_file() or sha256_file(evidence) != evidence_digest:
        raise ToolDispatchHold("TACTICAL_REVIEW_EVIDENCE_STALE")
    charter_bytes = charter_path.read_bytes()
    if (goal.get("charter_ref") != runtime.get("charter_ref")
        or goal.get("charter_sha256") != hashlib.sha256(charter_bytes).hexdigest()):
        raise ToolDispatchHold("GOAL_CHARTER_BINDING_MISMATCH")
    workspace_digest = _workspace_path_sha256(workspace)
    if command.workspace_path_sha256 != workspace_digest:
        raise ToolDispatchHold("WORKSPACE_PATH_BINDING_MISMATCH")
    return {
        "campaign_id": command.campaign_id, "actor_id": command.actor_id,
        "run_id": command.run_id, "work_unit_id": command.work_unit_id,
        "runtime_revision": expected_revision,
        "source_tree_sha256": source,
        "source_tree_excluding_target_sha256": source_without_target,
        "workspace_path_sha256": workspace_digest,
        "goal_sha256": hashlib.sha256(goal_path.read_bytes()).hexdigest(),
        "goal_digest": goal_digest,
        "plan_sha256": hashlib.sha256(plan_path.read_bytes()).hexdigest(),
        "plan_revision": plan["revision"],
        "charter_sha256": hashlib.sha256(charter_bytes).hexdigest(),
        "authority_sha256": hashlib.sha256((control / "state" / "EXECUTION_AUTHORITY_CURRENT.json").read_bytes()).hexdigest(),
        "identity_sha256": hashlib.sha256((control / "state" / "IDENTITY_REGISTRY_CURRENT.json").read_bytes()).hexdigest(),
        "allowed_write_surfaces": sorted(allowed),
    }


def _append_event(runtime: dict[str, Any], action: str, receipt: dict[str, Any]) -> None:
    runtime["revision"] += 1
    runtime["updated_at"] = _now()
    runtime.setdefault("event_log", []).append({
        "seq": max((entry.get("seq", 0) for entry in runtime["event_log"]), default=0) + 1,
        "at": runtime["updated_at"],
        "action": action, "work_unit_id": receipt["binding"]["work_unit_id"],
        "actor_id": receipt["binding"]["actor_id"], "details": receipt,
    })


def _validate_runtime_event_log(runtime: dict[str, Any]) -> list[dict[str, Any]]:
    """Reject recovery against a journal whose revision/sequence binding is broken."""
    events = runtime.get("event_log")
    if (not isinstance(events, list) or type(runtime.get("revision")) is not int
        or runtime["revision"] != len(events)
        or any(not isinstance(entry, dict) or entry.get("seq") != index
               or not isinstance(entry.get("details"), dict)
               for index, entry in enumerate(events, start=1))):
        raise ToolDispatchHold("CAMPAIGN_RUNTIME_CURRENTNESS_INVALID")
    return events


def _command_digest(command: ToolCommand) -> str:
    return hashlib.sha256(json.dumps(asdict(command), sort_keys=True,
        separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def _workspace_path_sha256(workspace: Path) -> str:
    canonical = os.path.normcase(str(workspace.resolve(strict=True)))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _require_disposable_test_roots(control: Path, workspace: Path | None = None) -> None:
    control = control.resolve(strict=True)
    temp_root = Path(tempfile.gettempdir()).resolve(strict=True)
    roots = [control]
    if workspace is not None:
        roots.append(workspace.resolve(strict=True))
    if any(root == temp_root or not root.is_relative_to(temp_root) for root in roots):
        raise ToolDispatchHold("PORTABLE_ADAPTER_REQUIRES_DISPOSABLE_TEMP_ROOTS")


def _dispatch_tool(control: Path, workspace: Path, command: ToolCommand,
                   adapter: ToolPort) -> dict[str, Any]:
    """Private adapter injection seam for deterministic fault testing only."""
    control = control.resolve(strict=True)
    workspace = workspace.resolve(strict=True)
    if not workspace.is_dir() or workspace == control or workspace.is_relative_to(control):
        raise ToolDispatchHold("INVALID_OR_NESTED_WORKSPACE_BOUNDARY")
    _require_disposable_test_roots(control, workspace)
    _validate_command_shape(command)
    capabilities = adapter.observe()
    if (capabilities.support_classification != "PORTABLE_TEST_ADAPTER"
        or capabilities.provider_invocation is not False
        or command.operation_id not in capabilities.operations):
        raise ToolDispatchHold("UNSUPPORTED_TOOL_CAPABILITY")
    if len(command.content_utf8.encode("utf-8")) > 2 * 1024 * 1024:
        raise ToolDispatchHold("INVALID_TOOL_COMMAND")
    runtime_path = _control_file(control, "runtime/CAMPAIGN_RUNTIME_CURRENT.json")
    with state_lock(control, timeout=10.0):
        try:
            campaignctl.require_no_pending_transaction(control)
        except campaignctl.CampaignError as exc:
            raise ToolDispatchHold("PENDING_CAMPAIGN_TRANSACTION") from exc
        runtime = _read_json(runtime_path)
        command_digest = _command_digest(command)
        prior = []
        for entry in runtime.get("event_log", []):
            details = entry.get("details", {})
            if details.get("idempotency_key") == command.idempotency_key:
                if details.get("command_sha256") != command_digest:
                    raise ToolDispatchHold("IDEMPOTENCY_KEY_COMMAND_CONFLICT")
                prior.append((entry.get("action"), details))
        if prior:
            terminal = [details for action, details in prior
                        if action in {"TOOL_DISPATCH_OBSERVED", "TOOL_DISPATCH_UNKNOWN"}]
            if terminal:
                return terminal[-1]
            raise ToolDispatchHold("IDEMPOTENCY_KEY_OUTCOME_UNKNOWN_NO_REPLAY")
        if runtime.get("revision") != command.runtime_revision:
            raise ToolDispatchHold("CAMPAIGN_RUNTIME_REVISION_STALE")
        try:
            binding = _authority_binding(control, workspace, command, expected_revision=command.runtime_revision)
        except (OSError, ValueError, TypeError, campaignctl.CampaignError, ManifestError) as exc:
            if isinstance(exc, ToolDispatchHold):
                raise
            raise ToolDispatchHold("AUTHORITY_OR_SOURCE_BINDING_INVALID:" + type(exc).__name__) from exc
        _safe_target(workspace, command.target, tuple(binding["allowed_write_surfaces"]))
        execution_started_ns = time.perf_counter_ns()
        receipt = {
            "schema_version": "agent-tool-dispatch-receipt-v1",
            "dispatch_id": str(uuid.uuid4()), "idempotency_key": command.idempotency_key,
            "phase": "DISPATCHING", "observed_at": _now(), "binding": binding,
            "command_sha256": command_digest,
            "capabilities": asdict(capabilities), "provider_cost": "NOT_APPLICABLE_NOT_MEASURED",
            "cancellation_supported": False,
            "result": "UNKNOWN_UNTIL_OBSERVED",
        }
        _append_event(runtime, "TOOL_DISPATCH_STARTED", receipt)
        atomic_json(runtime_path, runtime)
    try:
        with state_lock(control, timeout=10.0):
            current = _read_json(runtime_path)
            events = current.get("event_log", [])
            if (current.get("revision") != command.runtime_revision + 1
                or len(events) != command.runtime_revision + 1
                or events[-1].get("action") != "TOOL_DISPATCH_STARTED"
                or events[-1].get("details", {}).get("dispatch_id") != receipt["dispatch_id"]):
                raise ToolDispatchHold("TOOL_INTENT_CURRENTNESS_CHANGED_BEFORE_EFFECT")
            try:
                campaignctl.require_no_pending_transaction(control)
            except campaignctl.CampaignError as exc:
                raise ToolDispatchHold("PENDING_CAMPAIGN_TRANSACTION") from exc
            # Recheck exact Goal, Plan, source, lease and actor at the effect boundary.
            binding_now = _authority_binding(control, workspace, command,
                                             expected_revision=command.runtime_revision + 1)
            binding_now["runtime_revision"] = binding["runtime_revision"]
            if binding_now != binding:
                raise ToolDispatchHold("AUTHORITY_OR_SOURCE_BINDING_CHANGED_AT_EFFECT_BOUNDARY")
            effect = adapter.execute(command, workspace)
        receipt["effect"] = effect
        receipt["bytes_written"] = effect.get("bytes_written")
        receipt["elapsed_ms"] = max(0, (time.perf_counter_ns() - execution_started_ns) // 1_000_000)
        receipt["completed_at"] = _now()
        receipt["phase"] = "OBSERVED" if effect.get("status") == "completed" else "UNKNOWN"
        receipt["source_tree_sha256_after"] = _source_tree_digest(workspace, control)
        receipt["source_tree_excluding_target_sha256_after"] = _source_tree_digest(
            workspace, control, exclude_target=command.target,
            allowed_roots=tuple(binding["allowed_write_surfaces"]))
        receipt["physical_target_sha256"] = _regular_file_sha(workspace / command.target)
        if (receipt["source_tree_excluding_target_sha256_after"]
            != binding["source_tree_excluding_target_sha256"]):
            receipt["phase"] = "UNKNOWN"
            receipt["result"] = "UNRELATED_SOURCE_DRIFT_DURING_EFFECT"
        elif receipt["physical_target_sha256"] != effect.get("content_sha256"):
            receipt["phase"] = "UNKNOWN"
            receipt["result"] = "PHYSICAL_READBACK_MISMATCH"
        else:
            receipt["result"] = "EFFECT_PHYSICALLY_OBSERVED"
    except ToolDispatchInterrupted as exc:
        receipt["phase"] = "UNKNOWN"
        receipt["result"] = "INTERRUPTED_EFFECT_REQUIRES_RECONCILIATION"
        receipt["error_class"] = type(exc).__name__
        receipt["elapsed_ms"] = max(0, (time.perf_counter_ns() - execution_started_ns) // 1_000_000)
        receipt["completed_at"] = _now()
        receipt["recovery_required"] = True
        raise
    except Exception as exc:
        receipt["phase"] = "UNKNOWN"
        receipt["result"] = "EFFECT_OR_RECEIPT_AMBIGUOUS_NO_REPLAY"
        receipt["error_class"] = type(exc).__name__
        receipt["elapsed_ms"] = max(0, (time.perf_counter_ns() - execution_started_ns) // 1_000_000)
        receipt["completed_at"] = _now()
        receipt["recovery_required"] = True
        raise
    with state_lock(control, timeout=10.0):
        runtime = _read_json(runtime_path)
        starts = [entry for entry in runtime.get("event_log", [])
                  if entry.get("action") == "TOOL_DISPATCH_STARTED"
                  and entry.get("details", {}).get("dispatch_id") == receipt["dispatch_id"]]
        if len(starts) != 1:
            receipt["phase"] = "UNKNOWN"
            receipt["result"] = "START_RECEIPT_MISSING_OR_DUPLICATE"
        try:
            binding_after = _authority_binding(control, workspace, command,
                expected_revision=command.runtime_revision + 1, verify_source=False)
            binding_before = dict(binding)
            binding_after["source_tree_sha256"] = binding_before["source_tree_sha256"]
            binding_after["runtime_revision"] = binding_before["runtime_revision"]
            if binding_after != binding_before and receipt["phase"] == "OBSERVED":
                receipt["phase"] = "UNKNOWN"
                receipt["result"] = "AUTHORITY_OR_PLAN_CHANGED_DURING_EFFECT"
        except ToolDispatchHold as exc:
            receipt["phase"] = "UNKNOWN"
            receipt["result"] = "AUTHORITY_OR_PLAN_CHANGED_DURING_EFFECT"
            receipt["completion_binding_failure"] = str(exc)
        except Exception as exc:
            receipt["phase"] = "UNKNOWN"
            receipt["result"] = "AUTHORITY_OR_PLAN_CHANGED_DURING_EFFECT"
            receipt["completion_binding_failure"] = type(exc).__name__
        _append_event(runtime, "TOOL_DISPATCH_OBSERVED" if receipt["phase"] == "OBSERVED"
                      else "TOOL_DISPATCH_UNKNOWN", receipt)
        atomic_json(runtime_path, runtime)
    return json.loads(json.dumps(receipt, sort_keys=True, ensure_ascii=False))


def dispatch_tool(control: Path, workspace: Path, command: ToolCommand) -> dict[str, Any]:
    """Public API exposes only the fixed, registered portable adapter."""
    return _dispatch_tool(control, workspace, command, PortableTestAdapter())


def recover_tool_dispatch(control: Path, dispatch_id: str) -> dict[str, Any]:
    if not re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", dispatch_id or ""):
        raise ToolDispatchHold("INVALID_DISPATCH_ID")
    control = control.resolve(strict=True)
    _require_disposable_test_roots(control)
    runtime_path = _control_file(control, "runtime/CAMPAIGN_RUNTIME_CURRENT.json")
    with state_lock(control, timeout=10.0):
        try:
            campaignctl.require_no_pending_transaction(control)
        except campaignctl.CampaignError as exc:
            raise ToolDispatchHold("PENDING_CAMPAIGN_TRANSACTION") from exc
        runtime = _read_json(runtime_path)
        events = _validate_runtime_event_log(runtime)
        starts = [entry for entry in events
                  if entry.get("action") == "TOOL_DISPATCH_STARTED"
                  and entry["details"].get("dispatch_id") == dispatch_id]
        if len(starts) != 1:
            raise ToolDispatchHold("DISPATCH_START_MISSING_OR_DUPLICATE")
        completed = [entry for entry in events
                     if entry.get("action") in {"TOOL_DISPATCH_OBSERVED", "TOOL_DISPATCH_UNKNOWN"}
                     and entry["details"].get("dispatch_id") == dispatch_id]
        if len(completed) > 1:
            raise ToolDispatchHold("DISPATCH_TERMINAL_DUPLICATE_OR_AMBIGUOUS")
        if completed:
            return completed[-1]["details"]
        receipt = dict(starts[0]["details"])
        receipt.update({"phase": "UNKNOWN", "result": "INTERRUPTED_RECEIPT_NOT_OBSERVED_NO_REPLAY",
                        "recovered_at": _now(), "provider_cost": "NOT_APPLICABLE_NOT_MEASURED"})
        _append_event(runtime, "TOOL_DISPATCH_UNKNOWN", receipt)
        atomic_json(runtime_path, runtime)
        return receipt
