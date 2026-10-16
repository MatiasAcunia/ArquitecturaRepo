#!/usr/bin/env python3
"""Optional, source-bound agent-host seam.

The portable controller does not turn local JSON into native host authority.
This module validates existing campaign/lease/currentness state and reports
observed host capabilities. Dispatch is deliberately refused unless a provider
can enforce both the declared write boundary and an actual per-command cost
cap; the currently detected Codex CLI cannot prove those properties.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Protocol

from candidate_manifest import ManifestError, build_manifest
import campaignctl
from state_tx import atomic_json, fsync_dir, sha256_file, state_lock


class DispatchHold(RuntimeError):
    pass


class HostDispatchInterrupted(DispatchHold):
    """A host timed out after creating a session whose effects may be ambiguous."""

    def __init__(self, message: str, *, host_turn_id: str | None = None):
        super().__init__(message)
        self.host_turn_id = host_turn_id


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 32 * 1024 * 1024:
        raise DispatchHold(f"UNTRUSTED_OR_MISSING_CONTROL_FILE:{path.name}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise DispatchHold(f"CONTROL_FILE_NOT_OBJECT:{path.name}")
    return value


@dataclass(frozen=True)
class EngineeringCommand:
    campaign_id: str
    actor_id: str
    run_id: str
    work_unit_id: str
    source_tree_sha256: str
    runtime_revision: int
    allowed_write_surfaces: tuple[str, ...]
    idempotency_key: str
    max_cost_usd: float
    prompt: str


@dataclass(frozen=True)
class HostCapabilities:
    host: str
    version: str | None
    authenticated: bool | None
    workspace_write_mode_observed: bool
    write_boundary_enforced: bool
    enforced_write_roots: tuple[str, ...]
    write_boundary_witness_sha256: str | None
    per_command_cost_cap_enforced: bool
    cost_cap_witness_sha256: str | None
    thread_resume_observed: bool
    support_classification: str
    limitations: tuple[str, ...]


def _host_capability_record(value: Any) -> dict[str, Any]:
    """Validate an adapter's untrusted probe before persisting or using it."""
    if not isinstance(value, HostCapabilities):
        raise TypeError("HostPort.observe must return HostCapabilities")
    if (not isinstance(value.host, str) or not value.host or len(value.host) > 256
        or (value.version is not None and (not isinstance(value.version, str) or len(value.version) > 256))
        or (value.authenticated is not None and type(value.authenticated) is not bool)
        or any(type(flag) is not bool for flag in (
            value.workspace_write_mode_observed,
            value.write_boundary_enforced,
            value.per_command_cost_cap_enforced,
            value.thread_resume_observed,
        ))
        or not isinstance(value.enforced_write_roots, tuple)
        or len(value.enforced_write_roots) > 64
        or any(not isinstance(root, str) or not root or len(root) > 512
               for root in value.enforced_write_roots)
        or not isinstance(value.limitations, tuple)
        or len(value.limitations) > 128
        or any(not isinstance(item, str) or len(item) > 2048 for item in value.limitations)):
        raise TypeError("HostPort.observe returned malformed capability fields")
    record = asdict(value)
    json.dumps(record, sort_keys=True, allow_nan=False)
    return record


class HostPort(Protocol):
    def observe(self) -> HostCapabilities: ...
    def dispatch(self, command: EngineeringCommand, workspace: Path,
                 *, permit: "_DispatchPermit") -> dict[str, Any]: ...


_PERMIT_SECRET = object()


class _DispatchPermit:
    """Short-lived, one-use binding minted only after durable controller intent."""

    def __init__(self, secret: object, command_digest: str, workspace: str):
        if secret is not _PERMIT_SECRET:
            raise DispatchHold("CONTROLLER_DISPATCH_PERMIT_REQUIRED")
        self.command_digest = command_digest
        self.workspace = workspace
        self.expires_at = time.monotonic() + 30.0
        self.consumed = False
        self.lock = threading.Lock()


def _terminate_process_tree(process: subprocess.Popen[Any], *, grace_seconds: float = 2.0) -> bool:
    """Stop a host process and descendants so inherited pipes cannot strand readers."""
    # Permit small process doubles in deterministic host-adapter tests; real
    # invocations always use subprocess.Popen below.
    if not isinstance(getattr(process, "pid", None), int):
        process.kill()
        try:
            process.wait(timeout=grace_seconds)
        except subprocess.TimeoutExpired:
            return False
        return getattr(process, "returncode", None) is not None
    if process.poll() is not None:
        return True
    if os.name == "nt":
        taskkill = shutil.which("taskkill")
        if taskkill:
            try:
                subprocess.run(
                    [taskkill, "/PID", str(process.pid), "/T", "/F"],
                    capture_output=True, timeout=grace_seconds, check=False,
                )
            except (OSError, subprocess.TimeoutExpired):
                pass
    else:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except (ProcessLookupError, PermissionError, OSError):
            pass
    try:
        process.wait(timeout=grace_seconds)
    except subprocess.TimeoutExpired:
        if os.name == "nt":
            try:
                process.kill()
            except OSError:
                pass
        else:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError, OSError):
                try:
                    process.kill()
                except OSError:
                    pass
        try:
            process.wait(timeout=grace_seconds)
        except subprocess.TimeoutExpired:
            return False
    return process.poll() is not None


def _command_digest(command: EngineeringCommand) -> str:
    return hashlib.sha256(
        json.dumps(asdict(command), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _mint_dispatch_permit(command: EngineeringCommand, workspace: Path) -> _DispatchPermit:
    return _DispatchPermit(_PERMIT_SECRET, _command_digest(command), str(workspace.resolve(strict=True)))


def _consume_dispatch_permit(permit: _DispatchPermit | None, command: EngineeringCommand,
                             workspace: Path) -> None:
    if not isinstance(permit, _DispatchPermit):
        raise DispatchHold("CONTROLLER_DISPATCH_PERMIT_REQUIRED")
    with permit.lock:
        if permit.consumed:
            raise DispatchHold("CONTROLLER_DISPATCH_PERMIT_ALREADY_CONSUMED")
        if time.monotonic() > permit.expires_at:
            permit.consumed = True
            raise DispatchHold("CONTROLLER_DISPATCH_PERMIT_EXPIRED")
        if (permit.command_digest != _command_digest(command)
            or permit.workspace != str(workspace.resolve(strict=True))):
            permit.consumed = True
            raise DispatchHold("CONTROLLER_DISPATCH_PERMIT_BINDING_MISMATCH")
        permit.consumed = True


CapabilityVerifier = Callable[[HostCapabilities, EngineeringCommand, Path], bool]


def _host_capabilities_verified(verifier: CapabilityVerifier | None,
                                capabilities: HostCapabilities,
                                command: EngineeringCommand, workspace: Path) -> bool:
    """Treat capability evidence as untrusted unless the configured verifier accepts it."""
    if verifier is None:
        return False
    try:
        return verifier(capabilities, command, workspace) is True
    except Exception:
        return False


def _record_dispatch_hold(control: Path, workspace: Path, command: EngineeringCommand,
                          receipt: dict[str, Any], hold_code: str) -> None:
    """Persist a pre-dispatch denial with the same CAS/currentness checks as intent."""
    receipt["phase"] = "HOLD"
    receipt["hold_code"] = hold_code
    observed_at = receipt["observed_at"]
    runtime_path = control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json"
    with state_lock(control, timeout=10.0):
        validate_command(control, workspace, command)
        runtime = read_json(runtime_path)
        if runtime.get("revision") != command.runtime_revision:
            raise DispatchHold("CAMPAIGN_RUNTIME_REVISION_STALE_WHILE_RECORDING_HOLD")
        seq = max((entry["seq"] for entry in runtime.get("event_log", [])), default=0) + 1
        runtime["revision"] += 1
        runtime["updated_at"] = observed_at
        runtime["event_log"].append({
            "seq": seq,
            "at": observed_at,
            "action": "HOST_DISPATCH_HELD",
            "work_unit_id": command.work_unit_id,
            "actor_id": command.actor_id,
            "details": receipt,
        })
        atomic_json(runtime_path, runtime)
    raise DispatchHold(json.dumps(receipt, sort_keys=True))


class CodexCliHost:
    """Optional Codex CLI execution port with fail-closed capability discovery.

    This port can invoke a turn and return its durable session identity. Its
    own capability report remains advisory: CLI workspace-write is not a strict
    filesystem boundary and the CLI exposes no per-turn USD cap. The campaign
    controller therefore refuses this port unless an independent verifier
    supplies current, externally enforced boundary and cost evidence.
    """

    MAX_OUTPUT_BYTES = 8 * 1024 * 1024
    MAX_STDERR_BYTES = 256 * 1024

    def __init__(self, executable: str = "codex", timeout_seconds: float = 3600.0):
        if not executable or timeout_seconds <= 0:
            raise ValueError("Codex CLI executable and positive timeout are required")
        self.executable = executable
        self.timeout_seconds = timeout_seconds

    def observe(self) -> HostCapabilities:
        version = self._run(["--version"])
        auth = self._run(["login", "status"])
        help_text = self._run(["exec", "--help"])
        resume_help = self._run(["exec", "resume", "--help"])
        available = version.returncode == 0
        authenticated = auth.returncode == 0 and "logged in" in (auth.stdout + auth.stderr).lower()
        mode = "--sandbox" in help_text.stdout and "workspace-write" in help_text.stdout
        limits = [
            "native Goal/lease pre-dispatch hook not connected",
            "per-command provider cost cap not observable or enforceable",
            "workspace-write CLI mode does not prove a strict filesystem boundary",
        ]
        return HostCapabilities(
            host="codex-cli",
            version=version.stdout.strip() if available else None,
            authenticated=authenticated if available else None,
            workspace_write_mode_observed=mode,
            write_boundary_enforced=False,
            enforced_write_roots=(),
            write_boundary_witness_sha256=None,
            per_command_cost_cap_enforced=False,
            cost_cap_witness_sha256=None,
            thread_resume_observed=(resume_help.returncode == 0
                                    and "SESSION_ID" in resume_help.stdout),
            support_classification=("HOST_ADVISORY" if available else "UNSUPPORTED"),
            limitations=tuple(limits),
        )

    def _run(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        argv = [self.executable, *args]
        try:
            return subprocess.run(argv, capture_output=True, text=True, timeout=8, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            return subprocess.CompletedProcess(argv, 127, "", type(exc).__name__)

    def dispatch(self, command: EngineeringCommand, workspace: Path,
                 *, permit: "_DispatchPermit | None" = None) -> dict[str, Any]:
        workspace = workspace.resolve(strict=True)
        _consume_dispatch_permit(permit, command, workspace)
        execution_contract = {
            "campaign_id": command.campaign_id,
            "actor_id": command.actor_id,
            "run_id": command.run_id,
            "work_unit_id": command.work_unit_id,
            "source_tree_sha256": command.source_tree_sha256,
            "allowed_write_surfaces": list(command.allowed_write_surfaces),
            "idempotency_key": command.idempotency_key,
            "max_cost_usd": command.max_cost_usd,
        }
        prompt = (
            "Execute the supplied engineering work only within the authorized write surfaces. "
            "Treat the following controller binding as fixed authority metadata; never broaden it.\n"
            + json.dumps(execution_contract, sort_keys=True, separators=(",", ":"))
            + "\n\nEngineering task:\n" + command.prompt
        )
        argv = [
            self.executable, "exec", "--sandbox", "workspace-write", "--json",
            "--cd", str(workspace), "-",
        ]
        try:
            process = subprocess.Popen(
                argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=False, start_new_session=(os.name != "nt"),
            )
        except OSError as exc:
            raise DispatchHold(f"CODEX_CLI_START_FAILED:{type(exc).__name__}") from exc

        stdout_capture = bytearray()
        stderr_capture = bytearray()
        output_exceeded = threading.Event()
        termination_unconfirmed = threading.Event()
        termination_lock = threading.Lock()

        def terminate_host_tree(*, grace_seconds: float = 2.0) -> bool:
            with termination_lock:
                return _terminate_process_tree(process, grace_seconds=grace_seconds)

        def drain(pipe, capture: bytearray, cap: int) -> None:
            try:
                while True:
                    # read1 returns currently available pipe data instead of
                    # waiting to fill a 64 KiB request. That lets timeout
                    # receipts retain a thread.started event from a small,
                    # still-open JSONL stream.
                    chunk = pipe.read1(65536)
                    if not chunk:
                        return
                    available = max(0, cap - len(capture))
                    if available:
                        capture.extend(chunk[:available])
                    if len(chunk) > available:
                        output_exceeded.set()
                        if not terminate_host_tree():
                            termination_unconfirmed.set()
            finally:
                pipe.close()

        stdout_thread = threading.Thread(
            target=drain, args=(process.stdout, stdout_capture, self.MAX_OUTPUT_BYTES), daemon=True
        )
        stderr_thread = threading.Thread(
            target=drain, args=(process.stderr, stderr_capture, self.MAX_STDERR_BYTES), daemon=True
        )
        stdout_thread.start()
        stderr_thread.start()

        def send_prompt() -> None:
            assert process.stdin is not None
            try:
                process.stdin.write(prompt.encode("utf-8"))
                process.stdin.close()
            except (BrokenPipeError, OSError):
                # A CLI that exits before reading stdin is classified from
                # its structured events and exit status below.
                pass

        writer_thread = threading.Thread(target=send_prompt, daemon=True)
        writer_thread.start()
        timed_out = False
        try:
            process.wait(timeout=self.timeout_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            if not terminate_host_tree(grace_seconds=5.0):
                termination_unconfirmed.set()
        writer_thread.join(timeout=1.0)
        stdout_thread.join(timeout=1.0)
        stderr_thread.join(timeout=1.0)

        stdout_text = bytes(stdout_capture).decode("utf-8", errors="replace")
        stderr_text = bytes(stderr_capture).decode("utf-8", errors="replace")
        events = self._parse_events(stdout_text)
        thread_id = self._thread_id(events)
        if timed_out:
            raise HostDispatchInterrupted(
                "CODEX_CLI_TURN_TIMED_OUT_WITH_AMBIGUOUS_EFFECTS", host_turn_id=thread_id,
            )
        if (termination_unconfirmed.is_set() or writer_thread.is_alive()
            or stdout_thread.is_alive() or stderr_thread.is_alive()):
            raise HostDispatchInterrupted(
                "CODEX_CLI_PROCESS_OR_PIPE_DID_NOT_QUIESCE", host_turn_id=thread_id,
            )
        if output_exceeded.is_set():
            raise HostDispatchInterrupted(
                "CODEX_CLI_OUTPUT_LIMIT_EXCEEDED", host_turn_id=thread_id,
            )
        thread_id = self._thread_id(events)
        if not thread_id:
            raise DispatchHold("CODEX_CLI_THREAD_ID_MISSING")
        turn_completed = any(event.get("type") == "turn.completed" for event in events)
        turn_failed = any(event.get("type") in {"turn.failed", "error"} for event in events)
        returncode = process.returncode
        status = ("completed" if returncode == 0 and turn_completed else
                  "failed" if returncode != 0 or turn_failed else "unknown")
        observed_commands = []
        seen_item_ids: set[str] = set()
        for event in events:
            item = event.get("item")
            if (event.get("type") in {"item.started", "item.completed"}
                and isinstance(item, dict) and item.get("type") == "command_execution"):
                command_text = item.get("command")
                if isinstance(command_text, str):
                    item_id = item.get("id")
                    if isinstance(item_id, str) and item_id:
                        if item_id in seen_item_ids:
                            continue
                        seen_item_ids.add(item_id)
                    observed_commands.append(hashlib.sha256(command_text.encode("utf-8")).hexdigest())
        return {
            "host_turn_id": thread_id,
            "status": status,
            "provider_cost_usd": "UNKNOWN",
            "host_process_exit_code": returncode,
            "host_stderr_sha256": hashlib.sha256(stderr_text.encode("utf-8")).hexdigest(),
            "observed_commands": observed_commands,
        }

    @staticmethod
    def _coerce_text(value: str | bytes | None) -> str:
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")
        return value or ""

    @staticmethod
    def _parse_events(output: str) -> list[dict[str, Any]]:
        events = []
        for line in output.splitlines():
            try:
                value = json.loads(line)
            except (json.JSONDecodeError, TypeError):
                continue
            if isinstance(value, dict):
                events.append(value)
        return events

    @staticmethod
    def _thread_id(events: list[dict[str, Any]]) -> str | None:
        for event in events:
            value = event.get("thread_id")
            if event.get("type") == "thread.started" and isinstance(value, str) and value:
                return value
        return None


def validate_command(control: Path, workspace: Path, command: EngineeringCommand) -> dict[str, Any]:
    """Bind command to live product/identity/charter/lease and exact source."""
    control = control.resolve(strict=True)
    workspace = workspace.resolve(strict=True)
    if not workspace.is_dir() or workspace == control or workspace.is_relative_to(control):
        raise DispatchHold("INVALID_OR_NESTED_WORKSPACE_BOUNDARY")
    runtime = read_json(control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json")
    authority = read_json(control / "state" / "EXECUTION_AUTHORITY_CURRENT.json")
    identity = read_json(control / "state" / "IDENTITY_REGISTRY_CURRENT.json")
    campaignctl.require_campaign_active(runtime)
    campaignctl.require_product_state_matches_runtime(control, runtime)
    charter_path, charter = campaignctl.read_charter(control, runtime)
    if charter.get("campaign_id") != command.campaign_id:
        raise DispatchHold("CHARTER_CAMPAIGN_MISMATCH")
    if runtime.get("revision") != command.runtime_revision:
        raise DispatchHold("CAMPAIGN_RUNTIME_REVISION_STALE")
    if runtime.get("campaign_id") != command.campaign_id or runtime.get("campaign_status") != "ACTIVE":
        raise DispatchHold("CAMPAIGN_ID_OR_STATUS_MISMATCH")
    if (authority.get("authority_status") != "ACTIVE"
        or authority.get("campaign_id") != command.campaign_id
        or authority.get("campaign_lead_actor_id") != command.actor_id
        or authority.get("current_run_id") != command.run_id):
        raise DispatchHold("EXECUTION_AUTHORITY_OR_LEASE_MISMATCH")
    if authority.get("baseline_ref") != charter.get("baseline_ref"):
        raise DispatchHold("AUTHORITY_CHARTER_BASELINE_MISMATCH")
    if authority.get("checkpoint_ref") != runtime.get("current_checkpoint_id"):
        raise DispatchHold("AUTHORITY_CHECKPOINT_STALE")
    expires_at = authority.get("expires_at")
    if not isinstance(expires_at, str):
        raise DispatchHold("EXECUTION_LEASE_EXPIRY_MISSING")
    try:
        expiry = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        if expiry.tzinfo is None or expiry.utcoffset() is None:
            raise DispatchHold("EXECUTION_LEASE_EXPIRY_MUST_BE_TIMEZONE_AWARE")
        if expiry <= datetime.now(timezone.utc):
            raise DispatchHold("EXECUTION_LEASE_EXPIRED")
    except (TypeError, ValueError, OverflowError) as exc:
        raise DispatchHold("EXECUTION_LEASE_EXPIRY_INVALID") from exc
    actors = {item.get("actor_id"): item for item in identity.get("actors", [])}
    actor = actors.get(command.actor_id, {})
    if actor.get("role_class") != "I3_ENGINEERING_CAMPAIGN_LEAD" or actor.get("status") != "ACTIVE":
        raise DispatchHold("ACTOR_IDENTITY_NOT_ACTIVE_I3")
    if actor.get("current_run_id") != command.run_id:
        raise DispatchHold("ACTOR_RUN_MISMATCH")
    units = [u for u in runtime.get("work_units", []) if u.get("id") == command.work_unit_id]
    if len(units) != 1:
        raise DispatchHold("WORK_UNIT_MISSING_OR_DUPLICATE")
    unit = units[0]
    if unit.get("status") != "ACTIVE" or unit.get("actor_id") != command.actor_id or unit.get("run_id") != command.run_id:
        raise DispatchHold("WORK_UNIT_NOT_ACTIVE_FOR_ACTOR_RUN")
    charter_envelope = charter.get("resource_envelope", {})
    allowed = (set(authority.get("allowed_write_surfaces", []))
               & set(unit.get("allowed_write_surfaces", []))
               & set(charter_envelope.get("allowed_write_surfaces", [])))
    if not command.allowed_write_surfaces or not set(command.allowed_write_surfaces) <= allowed:
        raise DispatchHold("WRITE_SURFACE_OUTSIDE_AUTHORIZED_INTERSECTION")
    if not re.fullmatch(r"[a-f0-9]{64}", command.source_tree_sha256):
        raise DispatchHold("INVALID_SOURCE_DIGEST")
    try:
        source = build_manifest(workspace)["source_tree_sha256"]
    except (OSError, ManifestError) as exc:
        raise DispatchHold(f"SOURCE_CANNOT_BE_BOUND:{type(exc).__name__}") from exc
    if source != command.source_tree_sha256:
        raise DispatchHold("SOURCE_TREE_DRIFT_BEFORE_DISPATCH")
    if not command.idempotency_key or len(command.idempotency_key) > 200:
        raise DispatchHold("INVALID_IDEMPOTENCY_KEY")
    if (isinstance(command.max_cost_usd, bool)
        or not isinstance(command.max_cost_usd, (int, float))
        or not math.isfinite(command.max_cost_usd)
        or command.max_cost_usd <= 0):
        raise DispatchHold("POSITIVE_PER_COMMAND_COST_CAP_REQUIRED")
    if not command.prompt.strip() or len(command.prompt) > 20_000:
        raise DispatchHold("INVALID_COMMAND_PROMPT")
    return {
        "campaign_id": runtime["campaign_id"],
        "actor_id": command.actor_id,
        "run_id": command.run_id,
        "runtime_revision": runtime["revision"],
        "charter_sha256": hashlib.sha256(charter_path.read_bytes()).hexdigest(),
        "authority_sha256": hashlib.sha256(
            (control / "state" / "EXECUTION_AUTHORITY_CURRENT.json").read_bytes()
        ).hexdigest(),
        "identity_registry_sha256": hashlib.sha256(
            (control / "state" / "IDENTITY_REGISTRY_CURRENT.json").read_bytes()
        ).hexdigest(),
        "source_tree_sha256": source,
        "allowed_write_surfaces": sorted(command.allowed_write_surfaces),
        "work_unit_id": command.work_unit_id,
    }


def _write_roots_cover(enforced: tuple[str, ...], requested: tuple[str, ...]) -> bool:
    """Whether the backend's observed OS write roots cover each requested root."""
    def clean(value: str) -> str | None:
        value = value.replace("\\", "/")
        if (not value or value.startswith("/") or value.endswith("/") or ":" in value
            or any(part in {"", ".", ".."} for part in value.split("/"))):
            return None
        return value
    observed = [clean(v) for v in enforced]
    requested_clean = [clean(v) for v in requested]
    return bool(requested_clean) and all(
        path is not None and any(root is not None and (path == root or path.startswith(root + "/"))
                                 for root in observed)
        for path in requested_clean
    )


def _write_roots_match(enforced: tuple[str, ...], requested: tuple[str, ...]) -> bool:
    """Require effective OS sandbox roots to equal the authorized roots."""
    def clean(value: str) -> str | None:
        value = value.replace("\\", "/")
        if (not value or value.startswith("/") or value.endswith("/") or ":" in value
            or any(part in {"", ".", ".."} for part in value.split("/"))):
            return None
        return value
    left = [clean(value) for value in enforced]
    right = [clean(value) for value in requested]
    return bool(left) and all(value is not None for value in left + right) and set(left) == set(right)


def _workspace_snapshot(workspace: Path, *, max_bytes: int = 2 * 1024 * 1024 * 1024) -> dict[str, str]:
    """Hash every regular file; reject links/special files and bound read cost."""
    root = workspace.resolve(strict=True)
    snapshot: dict[str, str] = {}
    total = 0
    for current, directories, files in os.walk(root, topdown=True, followlinks=False):
        here = Path(current)
        for name in list(directories):
            item = here / name
            if item.is_symlink():
                raise DispatchHold("SYMLINK_IN_EXECUTION_WORKSPACE")
            snapshot[item.relative_to(root).as_posix() + "/"] = "DIRECTORY"
        for name in files:
            item = here / name
            if item.is_symlink() or not item.is_file():
                raise DispatchHold("NONREGULAR_FILE_IN_EXECUTION_WORKSPACE")
            stat_before = item.stat()
            total += stat_before.st_size
            if total > max_bytes:
                raise DispatchHold("EXECUTION_WORKSPACE_SNAPSHOT_SIZE_LIMIT")
            digest = sha256_file(item)
            stat_after = item.stat()
            if (digest is None or stat_before.st_size != stat_after.st_size
                or stat_before.st_mtime_ns != stat_after.st_mtime_ns):
                raise DispatchHold("EXECUTION_WORKSPACE_CHANGED_DURING_SNAPSHOT")
            snapshot[item.relative_to(root).as_posix()] = digest
    return snapshot


def _out_of_scope_changes(before: dict[str, str], after: dict[str, str], roots: tuple[str, ...]) -> list[str]:
    changed = {path for path in before.keys() | after.keys() if before.get(path) != after.get(path)}
    def allowed(path: str) -> bool:
        return any(path == root.replace("\\", "/").strip("/") or path.startswith(root.replace("\\", "/").strip("/") + "/")
                   for root in roots)
    return sorted(path for path in changed if not allowed(path))


def _completion_binding_current(control: Path, command: EngineeringCommand,
                                binding: dict[str, Any], runtime: dict[str, Any]) -> tuple[bool, str | None]:
    try:
        if (runtime.get("campaign_id") != command.campaign_id
            or runtime.get("campaign_status") != "ACTIVE"
            or runtime.get("revision") != command.runtime_revision + 1):
            return False, "RUNTIME_REVISION_OR_CAMPAIGN_CHANGED_DURING_HOST_TURN"
        campaignctl.require_product_state_matches_runtime(control, runtime)
        charter_path, _ = campaignctl.read_charter(control, runtime)
        authority_path = control / "state" / "EXECUTION_AUTHORITY_CURRENT.json"
        identity_path = control / "state" / "IDENTITY_REGISTRY_CURRENT.json"
        authority = read_json(authority_path)
        if (hashlib.sha256(charter_path.read_bytes()).hexdigest() != binding["charter_sha256"]
            or hashlib.sha256(authority_path.read_bytes()).hexdigest() != binding["authority_sha256"]
            or hashlib.sha256(identity_path.read_bytes()).hexdigest() != binding["identity_registry_sha256"]):
            return False, "CHARTER_AUTHORITY_OR_IDENTITY_CHANGED_DURING_HOST_TURN"
        if (authority.get("authority_status") != "ACTIVE"
            or authority.get("campaign_id") != command.campaign_id
            or authority.get("campaign_lead_actor_id") != command.actor_id
            or authority.get("current_run_id") != command.run_id):
            return False, "EXECUTION_LEASE_REVOKED_DURING_HOST_TURN"
        expiry = datetime.fromisoformat(authority["expires_at"].replace("Z", "+00:00"))
        if expiry.tzinfo is None or expiry.utcoffset() is None or expiry <= datetime.now(timezone.utc):
            return False, "EXECUTION_LEASE_EXPIRED_DURING_HOST_TURN"
        registry = read_json(identity_path)
        actor = next((item for item in registry.get("actors", [])
                      if item.get("actor_id") == command.actor_id), {})
        if (actor.get("role_class") != "I3_ENGINEERING_CAMPAIGN_LEAD"
            or actor.get("status") != "ACTIVE" or actor.get("current_run_id") != command.run_id):
            return False, "ACTOR_IDENTITY_OR_RUN_REVOKED_DURING_HOST_TURN"
    except (OSError, ValueError, TypeError, KeyError, campaignctl.CampaignError, DispatchHold):
        return False, "CURRENT_AUTHORITY_COULD_NOT_BE_RECONSTRUCTED_AFTER_HOST_TURN"
    return True, None


def _receipt_archive_root(control: Path, *, create: bool = False) -> Path:
    control = control.resolve(strict=True)
    campaigns = control / "campaigns"
    archive_root = campaigns / "_host_dispatch_receipts"
    for path in (campaigns, archive_root):
        if path.is_symlink():
            raise DispatchHold("RECEIPT_ARCHIVE_PATH_UNSAFE")
        if path.exists() and not path.is_dir():
            raise DispatchHold("RECEIPT_ARCHIVE_PATH_UNSAFE")
        if create and not path.exists():
            path.mkdir()
        if path.is_symlink():
            raise DispatchHold("RECEIPT_ARCHIVE_PATH_UNSAFE")
    if archive_root.exists() and not archive_root.resolve().is_relative_to(control):
        raise DispatchHold("RECEIPT_ARCHIVE_PATH_UNSAFE")
    return archive_root


def _archive_unattached_receipt(control: Path, receipt: dict[str, Any], *, update: bool = False) -> Path:
    """Persist a receipt under its original campaign without mutating another owner."""
    campaign_id = receipt.get("binding", {}).get("campaign_id")
    dispatch_id = receipt.get("dispatch_id")
    if not isinstance(campaign_id, str) or not campaign_id or not isinstance(dispatch_id, str):
        raise DispatchHold("RECEIPT_ARCHIVE_IDENTITY_INVALID")
    if not re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", dispatch_id):
        raise DispatchHold("RECEIPT_ARCHIVE_DISPATCH_ID_INVALID")
    campaign_key = hashlib.sha256(campaign_id.encode("utf-8")).hexdigest()
    archive_dir = _receipt_archive_root(control, create=True) / campaign_key
    if archive_dir.is_symlink():
        raise DispatchHold("RECEIPT_ARCHIVE_PATH_UNSAFE")
    if not archive_dir.exists():
        archive_dir.mkdir()
    if archive_dir.is_symlink() or not archive_dir.resolve().is_relative_to(control.resolve()):
        raise DispatchHold("RECEIPT_ARCHIVE_PATH_UNSAFE")
    path = archive_dir / f"{dispatch_id}.json"
    receipt["receipt_archive"] = str(path.relative_to(control))
    payload = (json.dumps(receipt, sort_keys=True, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        if path.is_symlink():
            raise DispatchHold("RECEIPT_ARCHIVE_COLLISION")
        existing = read_json(path)
        if existing == json.loads(payload):
            return path
        if (not update or existing.get("dispatch_id") != dispatch_id
            or existing.get("binding", {}).get("campaign_id") != campaign_id):
            raise DispatchHold("RECEIPT_ARCHIVE_COLLISION")
        atomic_json(path, receipt)
        return path
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        fsync_dir(archive_dir)
    except BaseException:
        try:
            path.unlink(missing_ok=True)
        finally:
            raise
    return path


def _find_archived_receipt(control: Path, dispatch_id: str) -> tuple[Path, dict[str, Any]] | None:
    root = _receipt_archive_root(control)
    if not root.is_dir():
        return None
    found: tuple[Path, dict[str, Any]] | None = None
    for directory in root.iterdir():
        if directory.is_symlink() or not re.fullmatch(r"[a-f0-9]{64}", directory.name):
            continue
        candidate = directory / f"{dispatch_id}.json"
        if candidate.is_symlink():
            raise DispatchHold("RECEIPT_ARCHIVE_PATH_UNSAFE")
        if candidate.is_file():
            receipt = read_json(candidate)
            if receipt.get("dispatch_id") != dispatch_id:
                raise DispatchHold("RECEIPT_ARCHIVE_IDENTITY_MISMATCH")
            if found is not None:
                raise DispatchHold("DUPLICATE_RECEIPT_ARCHIVE")
            found = (candidate, receipt)
    return found


def _archived_idempotency_exists(control: Path, campaign_id: str, idempotency_key: str) -> bool:
    root = _receipt_archive_root(control)
    campaign_dir = root / hashlib.sha256(campaign_id.encode("utf-8")).hexdigest()
    if campaign_dir.is_symlink():
        raise DispatchHold("RECEIPT_ARCHIVE_PATH_UNSAFE")
    if not campaign_dir.is_dir():
        return False
    for path in campaign_dir.glob("*.json"):
        if path.is_symlink():
            raise DispatchHold("RECEIPT_ARCHIVE_PATH_UNSAFE")
        receipt = read_json(path)
        if receipt.get("idempotency_key") == idempotency_key:
            return True
    return False


def _archived_receipt_matches_current_campaign(control: Path, runtime: dict[str, Any],
                                               receipt: dict[str, Any]) -> bool:
    binding = receipt.get("binding", {})
    if (runtime.get("campaign_id") != binding.get("campaign_id")
        or runtime.get("campaign_status") != "ACTIVE"):
        return False
    try:
        campaignctl.require_product_state_matches_runtime(control, runtime)
        charter_path, _ = campaignctl.read_charter(control, runtime)
        return hashlib.sha256(charter_path.read_bytes()).hexdigest() == binding.get("charter_sha256")
    except (OSError, ValueError, TypeError, KeyError, campaignctl.CampaignError, DispatchHold):
        return False


def prepare_dispatch(control: Path, workspace: Path, command: EngineeringCommand, host: HostPort,
                     capability_verifier: CapabilityVerifier | None = None) -> dict[str, Any]:
    control = control.resolve(strict=True)
    runtime_path = control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json"
    with state_lock(control, timeout=10.0):
        runtime = read_json(runtime_path)
        if _archived_idempotency_exists(control, command.campaign_id, command.idempotency_key):
            raise DispatchHold("IDEMPOTENCY_KEY_ALREADY_ARCHIVED_NO_REPLAY")
        for old in runtime.get("event_log", []):
            details = old.get("details", {})
            if details.get("idempotency_key") == command.idempotency_key:
                raise DispatchHold("IDEMPOTENCY_KEY_ALREADY_RECORDED_NO_REPLAY")
        if runtime.get("revision") != command.runtime_revision:
            raise DispatchHold("CAMPAIGN_RUNTIME_REVISION_STALE_BEFORE_RECEIPT")
    binding = validate_command(control, workspace, command)
    observed_at = utc_now()
    receipt = {
        "schema_version": "agent-host-dispatch-receipt-v1",
        "dispatch_id": str(uuid.uuid4()),
        "idempotency_key": command.idempotency_key,
        "phase": "POLICY_CHECKED",
        "observed_at": observed_at,
        "binding": binding,
        "command_sha256": _command_digest(command),
        "host_capabilities": {"observation": "NOT_COMPLETED"},
        "host_capability_evidence_verified": False,
        "provider_cost_usd": "UNKNOWN",
        "host_turn_id": None,
        "result": "NOT_DISPATCHED",
    }
    observation_hold = "HOST_CAPABILITY_OBSERVATION_FAILED"
    try:
        capabilities = host.observe()
        try:
            capability_record = _host_capability_record(capabilities)
        except Exception:
            observation_hold = "HOST_CAPABILITIES_INVALID"
            raise
    except Exception as exc:
        receipt["phase"] = "HOLD"
        receipt["host_capabilities"] = {"observation": "FAILED"}
        receipt["capability_observation_error_class"] = type(exc).__name__
        receipt["capability_observation_error_sha256"] = hashlib.sha256(
            str(exc).encode("utf-8", errors="replace")
        ).hexdigest()
        _record_dispatch_hold(control, workspace, command, receipt, observation_hold)
    capabilities_verified = _host_capabilities_verified(
        capability_verifier, capabilities, command, workspace
    )
    receipt["host_capabilities"] = capability_record
    receipt["host_capability_evidence_verified"] = capabilities_verified
    if (not capabilities_verified
        or capabilities.authenticated is not True
        or capabilities.support_classification != "HOST_VERIFIED"
        or not capabilities.write_boundary_enforced
        or not _write_roots_match(capabilities.enforced_write_roots, command.allowed_write_surfaces)
        or not isinstance(capabilities.write_boundary_witness_sha256, str)
        or not re.fullmatch(r"[a-f0-9]{64}", capabilities.write_boundary_witness_sha256)
        or not capabilities.per_command_cost_cap_enforced
        or not isinstance(capabilities.cost_cap_witness_sha256, str)
        or not re.fullmatch(r"[a-f0-9]{64}", capabilities.cost_cap_witness_sha256)):
        receipt["phase"] = "HOLD"
        hold_code = ("HOST_ENFORCEMENT_EVIDENCE_UNVERIFIED" if not capabilities_verified
                     else "HOST_SCOPE_OR_COST_CAP_NOT_ENFORCED")
        _record_dispatch_hold(control, workspace, command, receipt, hold_code)

    # Persist intent before crossing the host boundary. If this process or
    # machine stops during the call, the idempotency key remains consumed and
    # recovery reports UNKNOWN instead of replaying a potentially completed turn.
    receipt["phase"] = "DISPATCHING"
    control_runtime = control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json"
    source_before = _workspace_snapshot(workspace)
    receipt["workspace_file_count_before"] = len(source_before)
    binding_now = validate_command(control, workspace, command)
    if binding_now != binding:
        raise DispatchHold("AUTHORITY_OR_SOURCE_BINDING_CHANGED_DURING_HOST_PROBE")
    # Capability attestations can become stale while the source snapshot is
    # being taken. Re-observe and re-verify immediately before the durable
    # dispatch intent; a revoked or changed boundary must not reach HostPort.
    try:
        boundary_capabilities = host.observe()
        boundary_capability_record = _host_capability_record(boundary_capabilities)
    except Exception as exc:
        receipt["pre_dispatch_host_capabilities"] = {"observation": "FAILED"}
        receipt["pre_dispatch_capability_evidence_verified"] = False
        receipt["pre_dispatch_capability_observation_error_class"] = type(exc).__name__
        receipt["pre_dispatch_capability_observation_error_sha256"] = hashlib.sha256(
            str(exc).encode("utf-8", errors="replace")
        ).hexdigest()
        _record_dispatch_hold(
            control, workspace, command, receipt,
            "HOST_CAPABILITY_OBSERVATION_FAILED_AT_DISPATCH_BOUNDARY",
        )
    boundary_verified = _host_capabilities_verified(
        capability_verifier, boundary_capabilities, command, workspace
    )
    receipt["pre_dispatch_host_capabilities"] = boundary_capability_record
    receipt["pre_dispatch_capability_evidence_verified"] = boundary_verified
    if boundary_capabilities != capabilities or not boundary_verified:
        _record_dispatch_hold(
            control, workspace, command, receipt,
            "HOST_CAPABILITIES_CHANGED_BEFORE_DISPATCH",
        )
    with state_lock(control, timeout=10.0):
        runtime = read_json(control_runtime)
        if runtime.get("revision") != command.runtime_revision:
            raise DispatchHold("CAMPAIGN_RUNTIME_REVISION_STALE_BEFORE_DISPATCH")
        if build_manifest(workspace)["source_tree_sha256"] != command.source_tree_sha256:
            raise DispatchHold("SOURCE_TREE_DRIFT_AT_DISPATCH_BOUNDARY")
        if validate_command(control, workspace, command) != binding:
            raise DispatchHold("AUTHORITY_OR_SOURCE_BINDING_CHANGED_AT_DISPATCH_BOUNDARY")
        seq = max((entry["seq"] for entry in runtime.get("event_log", [])), default=0) + 1
        runtime["revision"] += 1
        runtime["updated_at"] = receipt["observed_at"]
        runtime["event_log"].append({
            "seq": seq, "at": receipt["observed_at"], "action": "HOST_DISPATCH_STARTED",
            "work_unit_id": command.work_unit_id, "actor_id": command.actor_id,
            "details": receipt,
        })
        _archive_unattached_receipt(control, receipt)
        atomic_json(control_runtime, runtime)

    try:
        permit = _mint_dispatch_permit(command, workspace)
        result = host.dispatch(command, workspace, permit=permit)
        if not isinstance(result, dict):
            raise DispatchHold("HOST_RESULT_NOT_OBJECT")
        if not isinstance(result.get("host_turn_id"), str) or not result["host_turn_id"]:
            raise DispatchHold("HOST_TURN_ID_MISSING")
        encoded_result = json.dumps(result, sort_keys=True, ensure_ascii=False, allow_nan=False)
        if len(encoded_result.encode("utf-8")) > 1024 * 1024:
            raise DispatchHold("HOST_RESULT_EXCEEDS_RECEIPT_LIMIT")
        receipt["host_turn_id"] = result["host_turn_id"]
        receipt["provider_cost_usd"] = result.get("provider_cost_usd", "UNKNOWN")
        receipt["result_sha256"] = hashlib.sha256(encoded_result.encode("utf-8")).hexdigest()
        receipt["observed_command_count"] = (
            len(result["observed_commands"])
            if isinstance(result.get("observed_commands"), list) else "UNKNOWN"
        )
        receipt["host_status"] = result.get("status", "UNKNOWN")
        observed_cost = result.get("provider_cost_usd")
        if isinstance(observed_cost, (int, float)) and not isinstance(observed_cost, bool):
            if observed_cost < 0 or observed_cost > command.max_cost_usd:
                raise DispatchHold("OBSERVED_PROVIDER_COST_OUTSIDE_AUTHORIZED_CAP")
        receipt["phase"] = "OBSERVED" if result.get("status") == "completed" else "UNKNOWN"
    except Exception as exc:
        receipt["phase"] = "UNKNOWN"
        receipt["error_class"] = type(exc).__name__
        receipt["error_sha256"] = hashlib.sha256(str(exc).encode("utf-8", errors="replace")).hexdigest()
        host_turn_id = getattr(exc, "host_turn_id", None)
        if isinstance(host_turn_id, str) and 0 < len(host_turn_id) <= 200:
            receipt["host_turn_id"] = host_turn_id
    try:
        source_after = _workspace_snapshot(workspace)
        changed_paths = sorted(path for path in source_before.keys() | source_after.keys()
                               if source_before.get(path) != source_after.get(path))
        out_of_scope = _out_of_scope_changes(source_before, source_after, command.allowed_write_surfaces)
        receipt["changed_paths"] = changed_paths[:200]
        receipt["changed_path_count"] = len(changed_paths)
        receipt["out_of_scope_paths"] = out_of_scope[:200]
        receipt["out_of_scope_path_count"] = len(out_of_scope)
        receipt["workspace_file_count_after"] = len(source_after)
        receipt["source_tree_sha256_after"] = build_manifest(workspace)["source_tree_sha256"]
        if out_of_scope:
            receipt["phase"] = "UNKNOWN"
            receipt["scope_violation"] = "OUT_OF_SCOPE_WRITE_DETECTED_EFFECT_ALREADY_OCCURRED"
    except (OSError, ManifestError) as exc:
        receipt["source_tree_sha256_after"] = None
        receipt["post_observation_error"] = type(exc).__name__
        receipt["phase"] = "UNKNOWN"
    receipt["observed_at"] = utc_now()
    with state_lock(control, timeout=10.0):
        runtime = read_json(control_runtime)
        binding_current, binding_failure = _completion_binding_current(control, command, binding, runtime)
        if not binding_current:
            receipt["phase"] = "UNKNOWN"
            receipt["completion_binding_failure"] = binding_failure
        if runtime.get("campaign_id") != command.campaign_id:
            receipt["campaign_runtime_replaced"] = True
            _archive_unattached_receipt(control, receipt, update=True)
            return receipt
        _archive_unattached_receipt(control, receipt, update=True)
        seq = max((entry["seq"] for entry in runtime.get("event_log", [])), default=0) + 1
        runtime["revision"] += 1
        runtime["updated_at"] = receipt["observed_at"]
        runtime["event_log"].append({
            "seq": seq, "at": receipt["observed_at"],
            "action": "HOST_DISPATCH_OBSERVED" if receipt["phase"] == "OBSERVED" else "HOST_DISPATCH_UNKNOWN",
            "work_unit_id": command.work_unit_id, "actor_id": command.actor_id,
            "details": receipt,
        })
        atomic_json(control_runtime, runtime)
    return receipt


def recover_interrupted_dispatch(control: Path, dispatch_id: str) -> dict[str, Any]:
    """Resolve an orphaned DISPATCHING event to UNKNOWN without replay."""
    if (not isinstance(dispatch_id, str)
        or not re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", dispatch_id)):
        raise DispatchHold("INVALID_DISPATCH_ID")
    control = control.resolve(strict=True)
    runtime_path = control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json"
    with state_lock(control, timeout=10.0):
        runtime = read_json(runtime_path)
        starts = [e for e in runtime.get("event_log", [])
                  if e.get("action") == "HOST_DISPATCH_STARTED"
                  and e.get("details", {}).get("dispatch_id") == dispatch_id]
        archive_match = _find_archived_receipt(control, dispatch_id)
        archived_receipt = archive_match[1] if archive_match else None
        if len(starts) > 1:
            raise DispatchHold("DISPATCH_START_MISSING_OR_DUPLICATE")
        existing = [e for e in runtime.get("event_log", [])
                    if e.get("action") in {"HOST_DISPATCH_OBSERVED", "HOST_DISPATCH_UNKNOWN"}
                    and e.get("details", {}).get("dispatch_id") == dispatch_id]
        if existing:
            if (archived_receipt is not None and archived_receipt.get("phase") != "DISPATCHING"
                and archived_receipt != existing[-1].get("details")):
                raise DispatchHold("ARCHIVED_RECEIPT_RUNTIME_CONFLICT")
            return existing[-1]["details"]
        if archived_receipt is not None and archived_receipt.get("phase") != "DISPATCHING":
            if runtime.get("campaign_id") != archived_receipt.get("binding", {}).get("campaign_id"):
                return archived_receipt
            if not _archived_receipt_matches_current_campaign(control, runtime, archived_receipt):
                raise DispatchHold("ARCHIVED_RECEIPT_CAMPAIGN_BINDING_MISMATCH")
            receipt = dict(archived_receipt)
            seq = max((entry["seq"] for entry in runtime.get("event_log", [])), default=0) + 1
            runtime["revision"] += 1
            runtime["updated_at"] = receipt.get("observed_at", utc_now())
            runtime["event_log"].append({
                "seq": seq, "at": runtime["updated_at"],
                "action": "HOST_DISPATCH_OBSERVED" if receipt.get("phase") == "OBSERVED" else "HOST_DISPATCH_UNKNOWN",
                "work_unit_id": receipt["binding"]["work_unit_id"],
                "actor_id": receipt["binding"].get("actor_id"), "details": receipt,
            })
            atomic_json(runtime_path, runtime)
            return receipt
        if archived_receipt is None and not starts:
            raise DispatchHold("DISPATCH_START_MISSING_OR_DUPLICATE")
        if archived_receipt is not None and runtime.get("campaign_id") != archived_receipt.get("binding", {}).get("campaign_id"):
            receipt = dict(archived_receipt)
            receipt["phase"] = "UNKNOWN"
            receipt["result"] = "INTERRUPTED_CAMPAIGN_RUNTIME_REPLACED"
            receipt["provider_cost_usd"] = "UNKNOWN"
            receipt["recovered_at"] = utc_now()
            _archive_unattached_receipt(control, receipt, update=True)
            return receipt
        if archived_receipt is not None and not _archived_receipt_matches_current_campaign(control, runtime, archived_receipt):
            raise DispatchHold("ARCHIVED_RECEIPT_CAMPAIGN_BINDING_MISMATCH")
        receipt = dict(starts[0]["details"] if starts else archived_receipt)
        receipt["phase"] = "UNKNOWN"
        receipt["result"] = "INTERRUPTED_RECEIPT_NOT_OBSERVED"
        receipt["provider_cost_usd"] = "UNKNOWN"
        receipt["recovered_at"] = utc_now()
        seq = max((entry["seq"] for entry in runtime.get("event_log", [])), default=0) + 1
        runtime["revision"] += 1
        runtime["updated_at"] = receipt["recovered_at"]
        runtime["event_log"].append({
            "seq": seq, "at": receipt["recovered_at"],
            "action": "HOST_DISPATCH_UNKNOWN", "work_unit_id": receipt["binding"]["work_unit_id"],
            "actor_id": receipt["binding"].get("actor_id"), "details": receipt,
        })
        _archive_unattached_receipt(control, receipt, update=True)
        atomic_json(runtime_path, runtime)
        return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect optional coding-host capabilities; fail closed on dispatch.")
    parser.add_argument("--probe", action="store_true", help="observe installed Codex CLI without invoking an agent")
    parser.add_argument("--control-root", type=Path)
    parser.add_argument("--recover-dispatch-id")
    args = parser.parse_args()
    if args.probe:
        print(json.dumps(asdict(CodexCliHost().observe()), indent=2))
        return 0
    if args.recover_dispatch_id and args.control_root:
        print(json.dumps(recover_interrupted_dispatch(args.control_root, args.recover_dispatch_id), indent=2))
        return 0
    parser.error("dispatch requires a source-bound EngineeringCommand from the campaign controller")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
