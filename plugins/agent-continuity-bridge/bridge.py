#!/usr/bin/env python3
"""Agent Continuity Bridge (ACB): optional, offline-only controller preflight.

Never launches PowerShell, Codex, Goals, GUI, network or external effects.
Native operations intentionally unavailable until separate physical acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import platform
import shutil
import re
import stat
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

PLUGIN_ID = "agent-continuity-bridge"
PLUGIN_VERSION = "0.2.1"
SUPPORTED_CONTROLLER = re.compile(r"^3\.1\.0(?:-[0-9A-Za-z.-]+)?$")
MAX_ENTRIES = 1000
MAX_UNCOMPRESSED = 60 * 1024 * 1024
MAX_ENTRY_BYTES = 12 * 1024 * 1024
MANIFEST_LINE = re.compile(r"^([a-fA-F0-9]{64})  ([^\r\n]+)$")
REQUIRED = {
    "VERSION.txt", "release.json", "config/slots.json",
    "bin/codex-daily-control.ps1", "bin/install.ps1",
    "src/CodexDailyControl/Private/96-V3Orchestrator.ps1",
    "src/CodexDailyControl/Private/97-V3Quota.ps1",
    "src/CodexDailyControl/Private/98-V31DesktopHandoff.ps1",
    "SOURCE_SHA256SUMS.txt",
}
MARKER_NAME = "acb-registration.json"
PROTOCOL = "arquitecturarepo.optional-bridge.v1"


class BridgeHold(ValueError):
    """Controlled, descriptive refusal; not evidence of a native host failure."""


def _safe_path(raw: str) -> str:
    if not raw or "\\" in raw or "\x00" in raw or ":" in raw or raw.startswith("/"):
        raise BridgeHold("UNSAFE_ARCHIVE_PATH")
    parts = raw.split("/")
    reserved = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}
    if any(not p or p in {".", ".."} or p.rstrip(" .") != p or p.split(".", 1)[0].upper() in reserved for p in parts):
        raise BridgeHold("UNSAFE_ARCHIVE_PATH")
    return raw


def _contents(archive: Path) -> tuple[dict[str, bytes], str]:
    if not archive.is_file() or archive.is_symlink():
        raise BridgeHold("PACKAGE_UNAVAILABLE_OR_SYMLINK")
    if archive.stat().st_size > 25 * 1024 * 1024:
        raise BridgeHold("PACKAGE_COMPRESSED_SIZE_LIMIT")
    # Hash exactly the bytes that will be parsed; a controller replaced between
    # hash and ZIP-open cannot be certified under the first digest.
    try:
        raw = archive.read_bytes()
        if len(raw) > 25 * 1024 * 1024:
            raise BridgeHold("PACKAGE_COMPRESSED_SIZE_LIMIT")
        physical_digest = hashlib.sha256(raw).hexdigest()
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            members = z.infolist()
            if len(members) > MAX_ENTRIES or sum(i.file_size for i in members) > MAX_UNCOMPRESSED:
                raise BridgeHold("PACKAGE_SIZE_LIMIT")
            files = [i for i in members if not i.is_dir()]
            if len(files) != len(members):
                # The distributed 3.1 package has no directory entries.
                # Explicit directories can be safe but are not necessary for this protocol.
                raise BridgeHold("UNEXPECTED_DIRECTORY_ENTRY")
            paths = [i.filename for i in files]
            for i in files:
                if i.file_size > MAX_ENTRY_BYTES:
                    raise BridgeHold("PACKAGE_ENTRY_TOO_LARGE")
                kind = stat.S_IFMT((i.external_attr >> 16) & 0xffff)
                if kind not in (0, stat.S_IFREG):
                    raise BridgeHold("UNTRUSTED_ARCHIVE_ENTRY_KIND")
                _safe_path(i.filename)
            if len({n.casefold() for n in paths}) != len(paths):
                raise BridgeHold("DUPLICATE_ARCHIVE_PATH")
            prefixes = {n.split("/", 1)[0] for n in paths}
            if len(prefixes) != 1 or any("/" not in n for n in paths):
                raise BridgeHold("PACKAGE_ROOT_AMBIGUOUS")
            pref = next(iter(prefixes)) + "/"
            entries = {n.removeprefix(pref): z.read(n) for n in paths}
            if z.testzip() is not None:
                raise BridgeHold("ARCHIVE_CRC_FAILURE")
            return entries, physical_digest
    except (zipfile.BadZipFile, OSError, RuntimeError) as exc:
        raise BridgeHold("PACKAGE_UNREADABLE") from exc


def inspect(package: Path, expected_sha256: str | None = None) -> dict:
    """Require exact immutable package hashes; never import or execute package files."""
    entries, digest = _contents(package)
    if expected_sha256 is not None and (not re.fullmatch(r"[0-9a-f]{64}", expected_sha256) or digest != expected_sha256):
        raise BridgeHold("EXPECTED_PACKAGE_SHA256_MISMATCH")
    if REQUIRED - entries.keys():
        raise BridgeHold("REQUIRED_COMPONENT_MISSING")
    try:
        lines = entries["SOURCE_SHA256SUMS.txt"].decode("utf-8-sig").splitlines()
        declared: dict[str, str] = {}
        for line in lines:
            if not line.strip():
                continue
            m = MANIFEST_LINE.fullmatch(line)
            if not m:
                raise BridgeHold("MANIFEST_FORMAT_INVALID")
            hash_, name = m.groups()
            _safe_path(name)
            if name.casefold() in (x.casefold() for x in declared):
                raise BridgeHold("MANIFEST_DUPLICATE_PATH")
            declared[name] = hash_.lower()
        if set(declared) != set(entries) - {"SOURCE_SHA256SUMS.txt"}:
            raise BridgeHold("MANIFEST_INVENTORY_MISMATCH")
        wrong = [name for name, hash_ in declared.items()
                 if hashlib.sha256(entries[name]).hexdigest() != hash_]
        if wrong:
            raise BridgeHold("MANIFEST_CONTENT_MISMATCH")
        version = entries["VERSION.txt"].decode("utf-8-sig").strip()
        release = json.loads(entries["release.json"].decode("utf-8-sig"))
        slot_data = json.loads(entries["config/slots.json"].decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise BridgeHold("PACKAGE_METADATA_INVALID") from exc
    if not isinstance(release, dict) or not isinstance(slot_data, dict):
        raise BridgeHold("PACKAGE_METADATA_INVALID")
    if not SUPPORTED_CONTROLLER.fullmatch(version) or release.get("version") != version:
        raise BridgeHold("UNSUPPORTED_OR_MISMATCHED_CONTROLLER_VERSION")
    claimed_slots = release.get("goal_slots")
    if not isinstance(claimed_slots, list) or len(claimed_slots) > 256 or any(not isinstance(k, str) for k in claimed_slots):
        raise BridgeHold("CONTROLLER_SLOT_SET_INVALID")
    slots = slot_data.get("slots")
    if not isinstance(slots, list) or not slots or len(slots) > 256:
        raise BridgeHold("CONTROLLER_SLOT_SET_INVALID")
    keys = [s.get("key") if isinstance(s, dict) else None for s in slots]
    if any(not isinstance(k, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", k) for k in keys):
        raise BridgeHold("CONTROLLER_SLOT_SET_INVALID")
    if len({k.casefold() for k in keys}) != len(keys) or set(keys) != set(claimed_slots):
        raise BridgeHold("CONTROLLER_SLOT_SET_MISMATCH")
    return {
        "protocol": PROTOCOL,
        "plugin_id": PLUGIN_ID,
        "plugin_version": PLUGIN_VERSION,
        "status": "PACKAGE_VERIFIED_HOST_UNVERIFIED",
        "controller_kind": "codex-daily-control",
        "controller_version": version,
        "controller_package_sha256": digest,
        "manifest_verified": True,
        "manifest_files": len(declared),
        "configured_slot_count": len(keys),  # Never expose personal slot names.
        "native_host_verified": False,
        "external_effects_enabled": False,
        "capabilities": {
            "package_integrity": "VERIFIED_OFFLINE",
            "configuration_structure": "VERIFIED_OFFLINE",
            "native_goal_execution": "UNVERIFIED_DISABLED",
            "desktop_handoff": "UNVERIFIED_DISABLED",
            "quota_reactivation": "UNVERIFIED_DISABLED",
            "cloud_delivery": "UNVERIFIED_DISABLED",
        },
        "limitations": [
            "No Windows Desktop or app-server native execution has been performed by this plugin.",
            "The controller's release candidate does not constitute native acceptance.",
            "Controller is installed, configured and operated separately. No credentials are collected.",
        ],
    }


def _registration_dir(project: Path) -> Path:
    if project.is_symlink() or not project.is_dir():
        raise BridgeHold("PROJECT_ROOT_UNTRUSTED")
    control = project / ".agentic-sdlc"
    if not control.is_dir() or control.is_symlink():
        raise BridgeHold("ARQUITECTURAREPO_CONTROL_NOT_INSTALLED")
    registration = control / "plugins"
    for part in (registration, registration / PLUGIN_ID):
        if part.is_symlink():
            raise BridgeHold("PLUGIN_DIRECTORY_SYMLINK")
    return registration / PLUGIN_ID


def _expected_registration(result: dict) -> dict:
    return {"protocol": PROTOCOL, "plugin_id": PLUGIN_ID, "plugin_version": PLUGIN_VERSION,
            "controller_kind": result["controller_kind"], "controller_version": result["controller_version"],
            "controller_package_sha256": result["controller_package_sha256"],
            "enabled_native_effects": False,
            "installation_scope": "READ_ONLY_OPT_IN"}


def install(project: Path, package: Path, expected_sha256: str | None = None) -> dict:
    result = inspect(package, expected_sha256)
    dest = _registration_dir(project)
    if dest.exists() or dest.is_symlink():
        raise BridgeHold("PLUGIN_ALREADY_REGISTERED_OR_CONFLICT")
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        dest.mkdir(mode=0o700)
        record = _expected_registration(result)
        final = dest / MARKER_NAME
        # Exclusive create; do not accidentally replace user-owned plugin files.
        with final.open("x", encoding="utf-8") as f:
            f.write(json.dumps(record, sort_keys=True, indent=2) + "\n")
    except BaseException:
        # The parent marker belongs to this newly created directory; do not
        # strand a half-written JSON file after an IO failure.
        if dest.is_dir() and not dest.is_symlink():
            marker = dest / MARKER_NAME
            if marker.is_file() and not marker.is_symlink():
                marker.unlink()
            if not any(dest.iterdir()):
                dest.rmdir()
        raise
    return {"status": "REGISTERED_READ_ONLY", "plugin": PLUGIN_ID,
            "controller_version": result["controller_version"], "native_effects_enabled": False}


def _read_record(project: Path) -> tuple[Path, dict]:
    dest = _registration_dir(project)
    if not dest.is_dir() or dest.is_symlink():
        raise BridgeHold("PLUGIN_NOT_REGISTERED")
    record_path = dest / MARKER_NAME
    if record_path.is_symlink() or not record_path.is_file():
        raise BridgeHold("PLUGIN_REGISTRATION_MISSING_OR_SYMLINK")
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise BridgeHold("PLUGIN_REGISTRATION_INVALID") from exc
    if not isinstance(record, dict):
        raise BridgeHold("PLUGIN_REGISTRATION_INVALID")
    if record.get("protocol") != PROTOCOL or record.get("plugin_id") != PLUGIN_ID or record.get("enabled_native_effects") is not False:
        raise BridgeHold("PLUGIN_REGISTRATION_OUT_OF_SCOPE")
    if set(record) != {"protocol", "plugin_id", "plugin_version", "controller_kind", "controller_version",
                       "controller_package_sha256", "enabled_native_effects", "installation_scope"}:
        raise BridgeHold("PLUGIN_REGISTRATION_MODIFIED")
    if record.get("plugin_version") != PLUGIN_VERSION or record.get("controller_kind") != "codex-daily-control" or record.get("installation_scope") != "READ_ONLY_OPT_IN":
        raise BridgeHold("PLUGIN_REGISTRATION_MODIFIED")
    if not isinstance(record.get("controller_package_sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", record["controller_package_sha256"]):
        raise BridgeHold("PLUGIN_REGISTRATION_MODIFIED")
    if not isinstance(record.get("controller_version"), str) or not SUPPORTED_CONTROLLER.fullmatch(record["controller_version"]):
        raise BridgeHold("PLUGIN_REGISTRATION_MODIFIED")
    return record_path, record


def status(project: Path, package: Path | None = None) -> dict:
    _, record = _read_record(project)
    result = {"plugin_id": PLUGIN_ID, "status": "REGISTERED_HOST_UNVERIFIED", "native_effects_enabled": False,
              "controller_kind": record.get("controller_kind"), "controller_version": record.get("controller_version")}
    if package is not None:
        scan = inspect(package, record.get("controller_package_sha256"))
        result["controller_package_current"] = True
        result["manifest_verified"] = scan["manifest_verified"]
    else:
        result["controller_package_current"] = "UNKNOWN_NOT_SUPPLIED"
    return result


def uninstall(project: Path) -> dict:
    path, record = _read_record(project)
    if any(x.name != MARKER_NAME for x in path.parent.iterdir()):
        raise BridgeHold("PLUGIN_CONTENT_CHANGED_REFUSE_REMOVE")
    # Original record is intentionally deterministic and has no private paths.
    expected = {"protocol": PROTOCOL, "plugin_id": PLUGIN_ID, "plugin_version": PLUGIN_VERSION,
                "controller_kind": "codex-daily-control", "controller_version": record.get("controller_version"),
                "controller_package_sha256": record.get("controller_package_sha256"),
                "enabled_native_effects": False, "installation_scope": "READ_ONLY_OPT_IN"}
    if record != expected:
        raise BridgeHold("PLUGIN_REGISTRATION_MODIFIED")
    path.unlink()
    path.parent.rmdir()
    # Keep shared /plugins directory; it may have unrelated owner files.
    return {"status": "UNREGISTERED", "plugin": PLUGIN_ID, "controller_uninstalled": False}


def doctor(package: Path | None = None) -> dict:
    """Read-only dependency inventory, never a proof of native acceptance."""
    deps = {"python_3_10_plus": sys.version_info >= (3, 10),
            "windows": platform.system().lower() == "windows",
            "windows_powershell": shutil.which("powershell.exe") is not None,
            "codex_cli": shutil.which("codex") is not None,
            "git": shutil.which("git") is not None,
            "rclone_optional": shutil.which("rclone") is not None}
    r = {"plugin_id": PLUGIN_ID, "status": "PREREQUISITES_OBSERVED_NATIVE_UNVERIFIED",
         "dependencies": deps, "native_host_verified": False,
         "native_operations_allowed": False}
    if package is not None:
        z = inspect(package)
        r["controller_package_integrity"] = z["status"]
        r["controller_version"] = z["controller_version"]
    return r


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ArquitecturaRepo optional Agent Continuity Bridge — offline safe by default")
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("inspect", "install", "status", "uninstall", "doctor"):
        p = sub.add_parser(command)
        if command in {"inspect", "install"}:
            p.add_argument("--package", type=Path, required=True)
        if command in {"status", "doctor"}:
            p.add_argument("--package", type=Path)
        if command in {"install", "status", "uninstall"}:
            p.add_argument("--project", type=Path, required=True)
        if command in {"inspect", "install"}:
            p.add_argument("--sha256")
    opts = parser.parse_args(argv)
    try:
        if opts.command == "inspect":
            obj = inspect(opts.package, opts.sha256)
        elif opts.command == "install":
            obj = install(opts.project, opts.package, opts.sha256)
        elif opts.command == "status":
            obj = status(opts.project, opts.package)
        elif opts.command == "doctor":
            obj = doctor(opts.package)
        else:
            obj = uninstall(opts.project)
        print(json.dumps(obj, indent=2, sort_keys=True))
        return 0
    except (BridgeHold, OSError, ValueError, TypeError) as exc:
        print(json.dumps({"plugin_id": PLUGIN_ID, "status": "HOLD", "reason": str(exc)}), file=sys.stdout)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
