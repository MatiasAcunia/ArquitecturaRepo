#!/usr/bin/env python3
"""Local persistent artifact registry: file-level, fail-closed garbage collection.

Only newly registered system-owned scratch roots can be cleaned. This is not
an OS filesystem monitor; unwrapped host/IDE writes need separate readback.
Whole worktree cleanup stays with workspace_gc.py.
"""
from __future__ import annotations
import argparse
import ctypes
import hashlib
import json
import os
import re
import subprocess
import shutil
import socket
import stat
import sys
import tempfile
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

if os.name == "nt":
    import msvcrt
else:
    import fcntl

VERSION = "artifact-ledger-v1"
NAME = "ARTIFACT_LIFECYCLE_CURRENT.json"
MARKER = ".agentic-artifact-root.json"
CLASSES = (
    "SOURCE_VERSIONED", "CANONICAL_STATE", "IMMUTABLE_EVIDENCE",
    "SHORT_TERM_EVIDENCE", "DERIVED_REBUILDABLE", "TEMP_TRANSACTION",
    "SENSITIVE_LOCAL", "EXTERNAL_CANONICAL", "QUARANTINE_UNRESOLVED",
)
DELETABLE = {"DERIVED_REBUILDABLE", "TEMP_TRANSACTION"}
PROTECTED_EXT = {".sqlite", ".sqlite3", ".db", ".sql", ".env", ".key", ".pem"}
SAFE_SEGMENT = re.compile(r'^[^\\/:*?"<>|\x00-\x1f\x7f]{1,100}$')
RESERVED_STEMS = {"CON", "PRN", "AUX", "NUL"} | {
    prefix + str(i) for prefix in ("COM", "LPT") for i in range(1, 10)
}
GC_PLAN_FRESHNESS = timedelta(minutes=5)


class LedgerHold(ValueError):
    pass


def now():
    return datetime.now(timezone.utc)


def stamp(t):
    return t.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def relative(s):
    if (not isinstance(s, str) or not s or len(s) > 700 or
        s.startswith(("/", "\\")) or "\\" in s or ":" in s or "\x00" in s or
        any(x in {"", ".", ".."} or x.endswith((" ", ".")) or x.split(".", 1)[0].upper() in RESERVED_STEMS or not SAFE_SEGMENT.fullmatch(x) for x in s.split("/"))):
        raise LedgerHold("UNSAFE_RELATIVE_PATH")
    return s


def confined(project, value):
    p = project.resolve()
    for part in relative(value).split("/"):
        p /= part
        if p.is_symlink():
            raise LedgerHold("SYMLINK_PATH_BLOCKED")
    if not p.resolve().is_relative_to(project.resolve()):
        raise LedgerHold("PATH_ESCAPE_BLOCKED")
    return p


def ledger_file(project, control):
    if "/" in relative(control) or control in {".git", ".github"}:
        raise LedgerHold("UNTRUSTED_CONTROL_ROOT")
    return confined(project, control + "/runtime/" + NAME)


def initial():
    s = stamp(now())
    return {"schema_version": VERSION, "revision": 0,
            "created_at": s, "updated_at": s, "roots": {}, "files": {}, "git_observations": []}


def safe_root(name):
    name = relative(name)
    if name != ".agentic-sdlc-scratch" and not name.startswith(".agentic-sdlc-scratch/"):
        raise LedgerHold("UNMANAGED_OUTPUT_ROOT")
    return name


def validate(d):
    required = {"schema_version", "revision", "created_at", "updated_at", "roots", "files"}
    if (not isinstance(d, dict) or not required.issubset(d) or
        set(d) - (required | {"git_observations"}) or
        d["schema_version"] != VERSION or
        type(d["revision"]) is not int or d["revision"] < 0 or
        not isinstance(d["roots"], dict) or not isinstance(d["files"], dict) or
        len(d["files"]) > 160000):
        raise LedgerHold("LEDGER_INVALID")
    observations = d.get("git_observations", [])
    if not isinstance(observations, list) or len(observations) > 32:
        raise LedgerHold("GIT_OBSERVATION_HISTORY_INVALID")
    for observation in observations:
        if (not isinstance(observation, dict) or set(observation) !=
            {"observed_at", "head", "changed"} or
            not isinstance(observation["head"], str) or
            not isinstance(observation["changed"], list) or
            len(observation["changed"]) > 5000):
            raise LedgerHold("GIT_OBSERVATION_ENTRY_INVALID")
    for root, owner in d["roots"].items():
        safe_root(root)
        if (not isinstance(owner, dict) or set(owner) !=
            {"id", "owner", "campaign", "created_at"} or
            any(not isinstance(v, str) or not v for v in owner.values())):
            raise LedgerHold("LEDGER_OWNER_RECORD_INVALID")
    for name, item in d["files"].items():
        if (relative(name) != name or not isinstance(item, dict) or
            item.get("path") != name or item.get("root") not in d["roots"] or
            item.get("category") not in CLASSES or
            item.get("status") not in {"OBSERVED", "MISSING", "DELETED"} or
            type(item.get("safe_delete")) is not bool or
            type(item.get("review_closed")) is not bool or
            not isinstance(item.get("dependencies"), list) or
            not isinstance(item.get("dependents", []), list) or
            not isinstance(item.get("dependency_history", []), list) or
            not isinstance(item.get("fingerprint"), dict) or
            not re.fullmatch(r"[0-9a-f]{64}", str(item["fingerprint"].get("sha256")))):
            raise LedgerHold("LEDGER_FILE_RECORD_INVALID")
        for dependent in item.get("dependents", []):
            relative(dependent)
        for dependency in item.get("dependencies", []):
            relative(dependency)
        review = item.get("review_evidence")
        if review is not None and (
            not isinstance(review, dict) or
            set(review) != {"decision", "reviewer", "evidence_ref", "evidence_sha256", "reviewed_at", "artifact_sha256"} or
            review.get("decision") not in {"ACCEPTED", "REJECTED"} or
            not isinstance(review.get("reviewer"), str) or not review["reviewer"] or
            not isinstance(review.get("evidence_ref"), str) or
            not re.fullmatch(r"[0-9a-f]{64}", str(review.get("evidence_sha256"))) or
            not re.fullmatch(r"[0-9a-f]{64}", str(review.get("artifact_sha256")))
        ):
            raise LedgerHold("LEDGER_REVIEW_EVIDENCE_INVALID")
        for event in item.get("dependency_history", []):
            if (not isinstance(event, dict) or set(event) !=
                {"dependent", "reviewer", "evidence_ref", "evidence_sha256", "removed_at"} or
                not isinstance(event.get("reviewer"), str) or not event["reviewer"] or
                not re.fullmatch(r"[0-9a-f]{64}", str(event.get("evidence_sha256")))):
                raise LedgerHold("LEDGER_DEPENDENCY_HISTORY_INVALID")
            relative(event["dependent"])
        root_owner = d["roots"][item["root"]]
        if item.get("owner") != root_owner["owner"] or item.get("campaign") != root_owner["campaign"]:
            raise LedgerHold("LEDGER_OWNER_CAMPAIGN_CONFLICT")
    for name, item in d["files"].items():
        for dependent in item.get("dependents", []):
            if dependent == name or dependent not in d["files"]:
                raise LedgerHold("LEDGER_DEPENDENT_REFERENCE_INVALID")
    return d


def load(path):
    if path.is_symlink() or not path.is_file():
        raise LedgerHold("PERSISTENT_LEDGER_MISSING")
    try:
        if path.stat().st_size > 32 * 1024 * 1024:
            raise LedgerHold("LEDGER_TOO_LARGE")
        return validate(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, json.JSONDecodeError):
        raise LedgerHold("PERSISTENT_LEDGER_CORRUPT") from None


def save(path, data):
    validate(data)
    data["revision"] += 1
    data["updated_at"] = stamp(now())
    fd, tmp = tempfile.mkstemp(prefix=".artifact-atomic-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, sort_keys=True, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


@contextmanager
def locked(path, *, operation="mutation", root=None):
    lock = path.with_name(path.name + ".lock")
    if lock.is_symlink():
        raise LedgerHold("LEDGER_LOCK_SYMLINK")
    stream = None
    acquired = False
    try:
        flags = os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(lock, flags, 0o600)
        lock_stat = os.fstat(fd)
        if not stat.S_ISREG(lock_stat.st_mode) or lock_stat.st_nlink != 1:
            os.close(fd)
            raise LedgerHold("LEDGER_LOCK_NOT_PRIVATE_REGULAR_FILE")
        stream = os.fdopen(fd, "r+b")
        if os.name == "nt":
            stream.seek(0, os.SEEK_END)
            if stream.tell() == 0:
                stream.write(b"\0")
                stream.flush()
            stream.seek(0)
            try:
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                acquired = True
            except OSError:
                raise LedgerHold("LEDGER_WRITER_ACTIVE") from None
        else:
            try:
                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired = True
            except OSError:
                raise LedgerHold("LEDGER_WRITER_ACTIVE") from None
        stream.seek(0)
        previous_bytes = stream.read()
        if previous_bytes == b"\0":
            previous_bytes = b""
        previous = None
        if previous_bytes:
            try:
                previous = json.loads(previous_bytes.decode("utf-8"))
            except (UnicodeError, json.JSONDecodeError):
                raise LedgerHold("LEDGER_LOCK_METADATA_UNVERIFIABLE") from None
            if (not isinstance(previous, dict) or
                previous.get("schema_version") != "artifact-ledger-lock-v1" or
                previous.get("status") not in {"idle", "active", "failed"}):
                raise LedgerHold("LEDGER_LOCK_METADATA_UNVERIFIABLE")
        if previous and previous.get("status") in {"active", "failed"} and operation != "recover-lock":
            raise LedgerHold("LEDGER_INTERRUPTED_OPERATION_REQUIRES_RECOVERY")
        current = {"schema_version": "artifact-ledger-lock-v1", "status": "active",
                   "pid": os.getpid(), "host": socket.gethostname(),
                   "started_at": stamp(now()), "operation": operation, "root": root}
        def write_state(value):
            raw = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
            stream.seek(0)
            stream.truncate()
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        write_state(current)
    except BaseException:
        if stream is not None:
            try:
                if acquired:
                    if os.name == "nt":
                        stream.seek(0)
                        msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                    else:
                        fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
            finally:
                stream.close()
        raise
    try:
        yield previous
    except BaseException as exc:
        if (operation == "recover-lock" and previous and
            previous.get("status") in {"active", "failed"}):
            # A refused recovery must leave the interrupted writer record intact.
            # Recording this recovery attempt as idle would remove the durable
            # gate even though no reconciliation occurred.
            failed_state = previous
        elif isinstance(exc, LedgerHold):
            current.update(status="idle", last_completed_at=stamp(now()),
                           last_refusal=str(exc))
            current.pop("started_at", None)
            failed_state = current
        elif operation == "recover-lock" and previous:
            failed_state = previous
        else:
            current.update(status="failed", failure_kind=type(exc).__name__)
            failed_state = current
        try:
            write_state(failed_state)
        except OSError:
            pass
        raise
    else:
        current["status"] = "idle"
        current.pop("started_at", None)
        current["last_completed_at"] = stamp(now())
        write_state(current)
    finally:
        if stream is not None:
            try:
                if os.name == "nt":
                    stream.seek(0)
                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
            finally:
                stream.close()


def owned_root(project, data, name):
    name = safe_root(name)
    base = confined(project, name)
    owner = data["roots"].get(name)
    marker = base / MARKER
    if owner is None or not base.is_dir() or marker.is_symlink() or not marker.is_file():
        raise LedgerHold("SCRATCH_OWNERSHIP_UNVERIFIED")
    try:
        m = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        raise LedgerHold("SCRATCH_MARKER_CORRUPT") from None
    if (not isinstance(m, dict) or m.get("schema_version") != VERSION or
        m.get("root") != name or any(m.get(k) != v for k, v in owner.items())):
        raise LedgerHold("SCRATCH_OWNER_CHANGED")
    return base


def inventory(project, data, root):
    base = owned_root(project, data, root)
    files = {}
    for parent, directories, filenames in os.walk(base, followlinks=False):
        if any((Path(parent) / x).is_symlink() for x in directories):
            raise LedgerHold("SYMLINKED_SCRATCH_DIRECTORY")
        for name in filenames:
            p = Path(parent) / name
            if p.parent == base and name in {MARKER, ".gitignore"}:
                continue
            if p.is_symlink() or not p.is_file() or p.stat().st_nlink != 1:
                raise LedgerHold("NONREGULAR_OR_HARDLINKED_OUTPUT")
            rel = p.relative_to(project).as_posix()
            relative(rel)
            st = p.stat()
            files[rel] = [st.st_size, st.st_mtime_ns]
            if len(files) > 20000:
                raise LedgerHold("SCRATCH_FILE_BUDGET_EXCEEDED")
    return files


def fingerprint(path):
    if path.is_symlink() or not path.is_file():
        raise LedgerHold("FILE_NOT_REGULAR")
    first = path.stat()
    if first.st_nlink != 1:
        raise LedgerHold("MULTIPLE_HARDLINKS")
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""):
            h.update(chunk)
    last = path.stat()
    if (first.st_dev, first.st_ino, first.st_size, first.st_mtime_ns) != (
        last.st_dev, last.st_ino, last.st_size, last.st_mtime_ns
    ):
        raise LedgerHold("FILE_CHANGED_DURING_FINGERPRINT")
    return {"sha256": h.hexdigest(), "size": last.st_size,
            "mtime_ns": last.st_mtime_ns, "device": last.st_dev, "inode": last.st_ino}


def digest_json(value):
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False).encode("utf-8")).hexdigest()


def file_digest(project, relative_path, *, require_tracked=True):
    path = confined(project, relative_path)
    if not path.is_file():
        raise LedgerHold("EVIDENCE_REFERENCE_NOT_A_FILE")
    if require_tracked:
        tracked = subprocess.run(
            ["git", "-C", str(project), "ls-files", "--error-unmatch", "--", relative_path],
            capture_output=True, check=False, timeout=15)
        if tracked.returncode:
            raise LedgerHold("EVIDENCE_REFERENCE_NOT_GIT_TRACKED")
    return fingerprint(path)["sha256"]


def process_alive(pid):
    if type(pid) is not int or pid <= 0:
        return None
    if os.name == "nt":
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        handle = kernel32.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not handle:
            error = ctypes.get_last_error()
            if error == 87:  # ERROR_INVALID_PARAMETER: no such process
                return False
            if error == 5:  # ERROR_ACCESS_DENIED: conservatively assume live
                return True
            return None
        try:
            code = ctypes.c_ulong()
            if not kernel32.GetExitCodeProcess(handle, ctypes.byref(code)):
                return None
            return code.value == 259  # STILL_ACTIVE
        finally:
            kernel32.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return None


def read_lock_metadata(path):
    lock = path.with_name(path.name + ".lock")
    if not lock.exists():
        return None
    if lock.is_symlink():
        raise LedgerHold("LEDGER_LOCK_SYMLINK")
    try:
        raw = lock.read_bytes()
        if not raw:
            return None
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        raise LedgerHold("LEDGER_LOCK_METADATA_UNVERIFIABLE") from None
    if (not isinstance(value, dict) or
        value.get("schema_version") != "artifact-ledger-lock-v1" or
        value.get("status") not in {"idle", "active", "failed"}):
        raise LedgerHold("LEDGER_LOCK_METADATA_UNVERIFIABLE")
    return value


def new_entry(project, data, root, name, category, safe, ttl):
    if category not in CLASSES or safe and (category not in DELETABLE or ttl is None):
        raise LedgerHold("INVALID_DISPOSITION")
    if ttl is not None and not (-24 <= ttl <= 24 * 365):
        raise LedgerHold("INVALID_RETENTION_HOURS")
    owner = data["roots"][root]
    current = now()
    return {"path": name, "root": root, "category": category,
            "owner": owner["owner"], "campaign": owner["campaign"],
            "fingerprint": fingerprint(confined(project, name)),
            "status": "OBSERVED", "safe_delete": bool(safe),
            "review_closed": False, "review_evidence": None,
            "dependencies": [], "dependents": [], "dependency_history": [],
            "created_at": stamp(current), "last_seen_at": stamp(current),
            "expires_at": stamp(current + timedelta(hours=ttl)) if ttl is not None else None}


def reconcile(project, data, root, before, after, category, safe, ttl, success):
    added = changed = missing = 0
    for name, stat in after.items():
        entry = data["files"].get(name)
        if entry is None:
            kind = category if success and name not in before else "QUARANTINE_UNRESOLVED"
            permit = bool(safe and kind in DELETABLE)
            data["files"][name] = new_entry(
                project, data, root, name, kind, permit, ttl if permit else None)
            added += 1
        elif (entry["status"] != "OBSERVED" or stat != [
            entry["fingerprint"]["size"], entry["fingerprint"]["mtime_ns"]
        ]):
            entry.update(fingerprint=fingerprint(confined(project, name)),
                         category="QUARANTINE_UNRESOLVED", safe_delete=False,
                         review_closed=False, expires_at=None,
                         last_seen_at=stamp(now()), status="OBSERVED")
            changed += 1
    for name, entry in data["files"].items():
        if entry["root"] == root and entry["status"] == "OBSERVED" and name not in after:
            entry.update(status="MISSING", safe_delete=False)
            missing += 1
    return {"registered": added, "changed_quarantined": changed, "missing": missing}


def git_protection(project, name):
    def command(*args):
        return subprocess.run(["git", "-C", str(project), *args],
                              capture_output=True, text=True, check=False)
    try:
        actual = command("rev-parse", "--show-cdup")
        if actual.returncode or actual.stdout.strip():
            return "PROJECT_GIT_ROOT_NOT_VERIFIED"
        if command("ls-files", "--error-unmatch", "--", name).returncode == 0:
            return "GIT_TRACKED_FILE"
        if command("check-ignore", "-q", "--", name).returncode != 0:
            return "FILE_NOT_IGNORED"
    except OSError:
        return "GIT_UNAVAILABLE"
    return None


def sqlite_or_sidecar(path):
    """Recognize SQLite by content and protect all case variants of WAL files."""
    lowered = path.name.casefold()
    if lowered.endswith(("-wal", "-shm", "-journal")) or path.suffix.casefold() in {
        ".db", ".sqlite", ".sqlite3"
    }:
        return True
    try:
        if path.is_file() and not path.is_symlink():
            with path.open("rb") as handle:
                return handle.read(16) == b"SQLite format 3\x00"
    except OSError:
        # Failure to establish a safe type must fail closed for GC.
        return True
    return False


def ready(project, data, name, unknown_roots):
    entry = data["files"][name]
    if entry["status"] != "OBSERVED":
        return "BLOCK", "NOT_OBSERVED"
    if entry["root"] in unknown_roots:
        return "BLOCK", "UNREGISTERED_FILES_PRESENT"
    if entry["category"] not in DELETABLE:
        return "BLOCK", "PROTECTED_OR_UNKNOWN_CLASS"
    review = entry.get("review_evidence")
    if (not entry["safe_delete"] or not entry["review_closed"] or
        not isinstance(review, dict) or review.get("decision") != "ACCEPTED"):
        return "BLOCK", "REVIEW_REFERENCE_OR_DELETE_PERMISSION_MISSING"
    if review.get("artifact_sha256") != entry["fingerprint"].get("sha256"):
        return "BLOCK", "REVIEW_ARTIFACT_IDENTITY_STALE"
    try:
        if file_digest(project, review["evidence_ref"]) != review["evidence_sha256"]:
            return "BLOCK", "REVIEW_EVIDENCE_STALE"
    except (LedgerHold, OSError, subprocess.SubprocessError):
        return "BLOCK", "REVIEW_EVIDENCE_UNREADABLE"
    if entry.get("dependencies") or entry.get("dependents"):
        return "BLOCK", "DEPENDENCIES_OR_ACCEPTED_DEPENDENTS_REMAIN"
    if not entry["expires_at"]:
        return "BLOCK", "EXPIRY_MISSING"
    try:
        deadline = datetime.fromisoformat(entry["expires_at"].replace("Z", "+00:00"))
        if deadline.tzinfo is None:
            raise ValueError("missing offset")
    except (ValueError, AttributeError):
        return "BLOCK", "INVALID_EXPIRY"
    if deadline > now():
        return "KEEP", "NOT_EXPIRED"
    p = confined(project, name)
    if (sqlite_or_sidecar(p) or p.suffix.casefold() in {".sql", ".env", ".key", ".pem"}):
        return "BLOCK", "DATABASE_SQL_OR_SECRET_FILE"
    try:
        owned_root(project, data, entry["root"])
        if fingerprint(p) != entry["fingerprint"]:
            return "BLOCK", "FILE_IDENTITY_CHANGED"
    except (LedgerHold, OSError):
        return "BLOCK", "FILE_OR_ROOT_UNVERIFIED"
    git = git_protection(project, name)
    if git:
        return "BLOCK", git
    return "DELETE_READY", "OWNED_EXPIRED_UNMODIFIED_IGNORED"


def inspect_git(project):
    """Read the actual canonical checkout; never copy source files into the ledger."""
    def git(*params):
        try:
            return subprocess.run(
                ["git", "-C", str(project), *params],
                capture_output=True, text=False, check=False,
                timeout=15,
            )
        except (OSError, subprocess.TimeoutExpired):
            raise LedgerHold("GIT_SOURCE_READBACK_FAILED") from None
    actual = git("rev-parse", "--show-cdup")
    if actual.returncode or actual.stdout.strip():
        raise LedgerHold("CANONICAL_GIT_CHECKOUT_MISMATCH")
    head = git("rev-parse", "--verify", "HEAD")
    if head.returncode:
        # Unborn repos are observable, not release-current or mutation-authorized.
        revision = "UNBORN"
    else:
        revision = os.fsdecode(head.stdout).strip()
        if not re.fullmatch(r"[0-9a-f]{40,64}", revision):
            raise LedgerHold("GIT_HEAD_UNVERIFIED")
    current = git("-c", "status.renames=false", "status",
                  "--porcelain=v1", "-z", "--untracked-files=all")
    if current.returncode or len(current.stdout) > 2_000_000:
        raise LedgerHold("GIT_STATUS_UNVERIFIABLE_OR_OVERSIZE")
    records = current.stdout.split(b"\x00")
    if records and records[-1] == b"":
        records.pop()
    if len(records) > 5000:
        raise LedgerHold("GIT_SOURCE_PATH_BUDGET_EXCEEDED")
    changed = []
    for raw in records:
        if len(raw) < 4 or raw[2:3] != b" ":
            raise LedgerHold("GIT_STATUS_RECORD_INVALID")
        status = raw[:2].decode("ascii", errors="strict")
        filename = os.fsdecode(raw[3:])
        # Git porcelain -z keeps spaces and accents in file names verbatim.
        # Values are local-only evidence; never concatenate them into shell.
        if not filename or filename.startswith(("/", "\\")) or "\x00" in filename:
            raise LedgerHold("GIT_STATUS_PATH_INVALID")
        changed.append({"status": status, "path": filename})
    return {"observed_at": stamp(now()), "head": revision, "changed": changed}


def gc_plan(project, data, *, allow_locked=False):
    observed = {root: inventory(project, data, root) for root in data["roots"]}
    unknown = {root for root, files in observed.items()
               if any(name not in data["files"] for name in files)}
    lock = None if allow_locked else read_lock_metadata(
        ledger_file(project, ".agentic-sdlc"))
    interrupted = bool(lock and lock.get("status") in {"active", "failed"} and not allow_locked)
    git_observation = inspect_git(project)
    git_binding = {"head": git_observation["head"], "changed": git_observation["changed"]}
    rows = []
    for name, entry in sorted(data["files"].items()):
        if entry["status"] == "DELETED":
            continue
        decision, reason = ("BLOCK", "INTERRUPTED_OPERATION_RECOVERY_REQUIRED") if interrupted else (("BLOCK", "PHYSICAL_FILE_MISSING") if (
            name not in observed.get(entry["root"], {})
        ) else ready(project, data, name, unknown))
        review = entry.get("review_evidence") or {}
        rows.append({"path": name, "category": entry["category"],
                     "bytes": entry["fingerprint"]["size"],
                     "decision": decision, "reason": reason,
                     "root": entry["root"], "owner": entry["owner"],
                     "campaign": entry["campaign"],
                     "fingerprint": entry["fingerprint"],
                     "dependencies": entry.get("dependencies", []),
                     "dependents": entry.get("dependents", []),
                     "review_evidence_sha256": review.get("evidence_sha256")})
    issued = now()
    result = {"schema_version": "artifact-gc-report-v2", "mode": "dry-run",
            "revision": data["revision"], "unregistered_roots": sorted(unknown),
             "git_binding": git_binding,
            "rows": rows, "ready_count": sum(r["decision"] == "DELETE_READY" for r in rows),
            "deleted_count": 0, "reclaimed_bytes": 0,
            "plan_issued_at": stamp(issued),
            "plan_expires_at": stamp(issued + GC_PLAN_FRESHNESS)}
    result["decision_sha256"] = gc_plan_decision_sha256(result)
    result["plan_sha256"] = digest_json(result)
    return result


def gc_plan_decision_sha256(plan):
    decision = {key: value for key, value in plan.items()
                if key not in {"plan_issued_at", "plan_expires_at",
                               "decision_sha256", "plan_sha256"}}
    return digest_json(decision)


def read_bounded_json(path, limit=2 * 1024 * 1024):
    p = Path(path)
    if p.is_symlink() or not p.is_file() or p.stat().st_size > limit:
        raise LedgerHold("RECEIPT_MISSING_SYMLINKED_OR_OVERSIZE")
    try:
        value = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        raise LedgerHold("RECEIPT_INVALID") from None
    if not isinstance(value, dict):
        raise LedgerHold("RECEIPT_INVALID")
    return value


def write_receipt_once(path, value):
    destination = Path(path).absolute()
    if destination.exists() or destination.is_symlink() or not destination.parent.is_dir():
        raise LedgerHold("RECEIPT_OUTPUT_PREEXISTS_OR_PARENT_MISSING")
    raw = (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("utf-8")
    try:
        fd = os.open(destination, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError:
        raise LedgerHold("RECEIPT_OUTPUT_PREEXISTS") from None


def approve_gc(project, data, args):
    plan = read_bounded_json(args.plan_file)
    stated_digest = plan.pop("plan_sha256", None)
    if (plan.get("schema_version") != "artifact-gc-report-v2" or
        plan.get("mode") != "dry-run" or stated_digest != digest_json(plan)):
        raise LedgerHold("GC_DRY_RUN_RECEIPT_INTEGRITY_INVALID")
    try:
        issued = parse_expiry(plan.get("plan_issued_at"), "GC_DRY_RUN_RECEIPT_TIME_INVALID")
        expires = parse_expiry(plan.get("plan_expires_at"), "GC_DRY_RUN_RECEIPT_TIME_INVALID")
        file_mtime = datetime.fromtimestamp(Path(args.plan_file).stat().st_mtime, timezone.utc)
    except (OSError, OverflowError, ValueError):
        raise LedgerHold("GC_DRY_RUN_RECEIPT_TIME_INVALID") from None
    current_time = now()
    if (issued > current_time + timedelta(seconds=5) or expires <= current_time or
        expires < issued or expires - issued > GC_PLAN_FRESHNESS or
        current_time - issued > GC_PLAN_FRESHNESS or
        file_mtime > current_time + timedelta(seconds=5) or
        current_time - file_mtime > GC_PLAN_FRESHNESS):
        raise LedgerHold("GC_DRY_RUN_RECEIPT_EXPIRED")
    if plan.get("decision_sha256") != gc_plan_decision_sha256(plan):
        raise LedgerHold("GC_DRY_RUN_RECEIPT_INTEGRITY_INVALID")
    current = gc_plan(project, data)
    if (plan.get("revision") != data["revision"] or
        plan.get("decision_sha256") != current.get("decision_sha256")):
        raise LedgerHold("GC_DRY_RUN_RECEIPT_STALE")
    row = next((item for item in current["rows"] if item["path"] == args.path), None)
    if row is None or row["decision"] != "DELETE_READY":
        raise LedgerHold("GC_TARGET_NOT_DELETE_READY")
    if args.reviewer.strip() in {"", row["owner"]}:
        raise LedgerHold("GC_REVIEWER_MUST_BE_NAMED_AND_DISTINCT")
    if not 1 <= args.lease_minutes <= 15:
        raise LedgerHold("GC_APPROVAL_LEASE_OUT_OF_RANGE")
    evidence_sha = file_digest(project, args.evidence_ref)
    output = Path(args.approval_out).absolute()
    try:
        # Canonicalize the existing parent to catch junctions and symlinks
        # whose lexical path is outside the checkout but resolves inside it.
        output = output.parent.resolve(strict=True) / output.name
    except OSError:
        raise LedgerHold("GC_APPROVAL_PARENT_UNRESOLVED") from None
    try:
        output.relative_to(project.resolve())
    except ValueError:
        pass
    else:
        raise LedgerHold("GC_APPROVAL_MUST_BE_STORED_OUTSIDE_SOURCE_REPO")
    issued = now()
    approval = {
        "schema_version": "artifact-gc-reviewed-approval-v1",
        "approval_id": uuid.uuid4().hex,
        "plan_sha256": stated_digest,
        "decision_sha256": current["decision_sha256"],
        "ledger_revision": data["revision"],
        "target": args.path,
        "owner": row["owner"], "campaign": row["campaign"],
        "fingerprint": row["fingerprint"],
        "dependencies": row["dependencies"], "dependents": row["dependents"],
        "git_binding": current["git_binding"],
        "reviewer": args.reviewer.strip(),
        "review_evidence_ref": args.evidence_ref,
        "review_evidence_sha256": evidence_sha,
        "issued_at": stamp(issued),
        "lease_expires_at": stamp(issued + timedelta(minutes=args.lease_minutes)),
    }
    approval["approval_sha256"] = digest_json(approval)
    write_receipt_once(output, approval)
    return {"status": "GC_APPROVAL_RECORDED", "approval_path": str(output),
            "approval_sha256": approval["approval_sha256"],
            "plan_sha256": stated_digest, "ledger_revision": data["revision"],
            "target": args.path, "reviewer": approval["reviewer"],
            "lease_expires_at": approval["lease_expires_at"],
            "human_identity_authentication": "NOT_PROVEN_LOCAL_ATTESTATION_ONLY"}


def parse_expiry(value, failure):
    try:
        moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if moment.tzinfo is None:
            raise ValueError
        return moment
    except (ValueError, AttributeError):
        raise LedgerHold(failure) from None


def validate_gc_approval(project, data, args, *, allow_locked=False):
    if not args.approval:
        raise LedgerHold("GC_EXECUTION_REQUIRES_REVIEWED_APPROVAL")
    approval = read_bounded_json(args.approval)
    stated_sha = approval.pop("approval_sha256", None)
    if (approval.get("schema_version") != "artifact-gc-reviewed-approval-v1" or
        stated_sha != digest_json(approval)):
        raise LedgerHold("GC_APPROVAL_INTEGRITY_INVALID")
    if parse_expiry(approval.get("lease_expires_at"), "GC_APPROVAL_LEASE_INVALID") <= now():
        raise LedgerHold("GC_APPROVAL_LEASE_EXPIRED")
    if approval.get("ledger_revision") != data["revision"]:
        raise LedgerHold("GC_APPROVAL_LEDGER_REVISION_STALE")
    evidence_sha = file_digest(project, approval.get("review_evidence_ref"))
    if evidence_sha != approval.get("review_evidence_sha256"):
        raise LedgerHold("GC_APPROVAL_EVIDENCE_STALE")
    plan = gc_plan(project, data, allow_locked=allow_locked)
    if plan["git_binding"] != approval.get("git_binding"):
        raise LedgerHold("GC_APPROVAL_GIT_CURRENTNESS_STALE")
    if plan["decision_sha256"] != approval.get("decision_sha256"):
        raise LedgerHold("GC_APPROVAL_SOURCE_OR_PLAN_STALE")
    row = next((item for item in plan["rows"] if item["path"] == approval.get("target")), None)
    if (row is None or row["decision"] != "DELETE_READY" or
        row["fingerprint"] != approval.get("fingerprint") or
        row["owner"] != approval.get("owner") or
        row["campaign"] != approval.get("campaign") or
        row["dependencies"] != approval.get("dependencies") or
        row["dependents"] != approval.get("dependents")):
        raise LedgerHold("GC_APPROVAL_TARGET_OR_DEPENDENCY_STALE")
    target = approval["target"]
    decision, reason = ready(project, data, target, set(plan["unregistered_roots"]))
    if decision != "DELETE_READY":
        raise LedgerHold("GC_PREDELETE_REVALIDATION_" + reason)
    return approval, plan, stated_sha


def execute_gc(project, data, args):
    approval, plan, stated_sha = validate_gc_approval(
        project, data, args, allow_locked=True)
    target = approval["target"]
    physical = confined(project, target)
    before_identity = fingerprint(physical)
    if before_identity != approval["fingerprint"]:
        raise LedgerHold("GC_PREDELETE_FILE_IDENTITY_STALE")
    free_before = shutil.disk_usage(project).free
    try:
        physical.unlink()
    except OSError:
        raise LedgerHold("OS_DELETE_REFUSED") from None
    if physical.exists() or physical.is_symlink():
        raise LedgerHold("GC_DELETE_READBACK_FAILED")
    data["files"][target].update(status="DELETED", safe_delete=False)
    save(ledger_file(project, ".agentic-sdlc"), data)
    free_after = shutil.disk_usage(project).free
    return {"schema_version": "artifact-gc-report-v2", "mode": "execute",
            "revision": data["revision"], "target": target,
            "decision": "DELETED", "reason": "REVIEWED_SINGLE_TARGET_REMOVED",
            "approval_sha256": stated_sha, "plan_sha256": approval["plan_sha256"],
            "deleted_count": 1, "reclaimed_bytes": before_identity["size"],
            "disk_free_before_bytes": free_before,
            "disk_free_after_bytes": free_after,
            "disk_free_delta_bytes": free_after - free_before,
            "reclaimed_bytes_basis": "logical_deleted_file_sizes",
            "file_absent_readback": True,
            "disk_delta_limitations": "Includes unrelated concurrent filesystem activity"}


def operate(a):
    supplied = Path(a.project).absolute()
    if not supplied.is_dir() or supplied.is_symlink():
        raise LedgerHold("PROJECT_UNTRUSTED")
    # Windows may present TEMP as RUNNER~1 while resolve() expands it.
    # Use ONE canonical root for os.walk, relative_to and Git identity.
    project = supplied.resolve()
    path = ledger_file(project, a.control_dir)
    if a.action == "report":
        data = load(path)
        lock = read_lock_metadata(path)
        return {"status": "PERSISTED", "revision": data["revision"],
                "files": len(data["files"]), "roots": len(data["roots"]),
                "writer_status": lock.get("status") if lock else "UNINITIALIZED"}
    if a.action in {"gc", "cleangarbage"} and not a.execute:
        return gc_plan(project, load(path))
    if a.action in {"gc", "cleangarbage"} and a.execute:
        if not a.approval:
            raise LedgerHold("GC_EXECUTION_REQUIRES_REVIEWED_APPROVAL")
        # Fail obvious stale or forged approvals before opening the writer
        # lease; validate again while holding the exclusive lease at unlink.
        validate_gc_approval(project, load(path), a, allow_locked=False)
    if a.action == "approve-gc":
        return approve_gc(project, load(path), a)
    op_root = getattr(a, "root", None)
    if op_root is None and a.action in {"classify", "review", "dependency"}:
        try:
            op_data = load(path)
            op_entry = op_data["files"].get(relative(a.path))
            op_root = op_entry.get("root") if op_entry else None
        except LedgerHold:
            op_root = None
    if op_root is None and a.action in {"gc", "cleangarbage"} and a.execute:
        try:
            op_data = load(path)
            approval = read_bounded_json(a.approval)
            target = op_data["files"].get(approval.get("target"))
            op_root = target.get("root") if target else None
        except (LedgerHold, OSError):
            op_root = None
    with locked(path, operation=a.action, root=op_root) as previous_lock:
        data = load(path)
        if a.action == "recover-lock":
            if not previous_lock or previous_lock.get("status") not in {"active", "failed"}:
                return {"status": "NO_INTERRUPTED_OPERATION", "revision": data["revision"]}
            root = safe_root(a.root)
            owner = data["roots"].get(root)
            if not owner or owner["owner"] != a.owner or owner["campaign"] != a.campaign:
                raise LedgerHold("RECOVERY_OWNER_OR_CAMPAIGN_MISMATCH")
            allowed_recovery_ops = {"capture", "reconcile", "classify", "review",
                                    "dependency", "gc", "cleangarbage", "recover-lock"}
            if (previous_lock.get("host") != socket.gethostname() or
                previous_lock.get("root") != root or
                previous_lock.get("operation") not in allowed_recovery_ops):
                raise LedgerHold("INTERRUPTED_OPERATION_IDENTITY_UNVERIFIED")
            pid = previous_lock.get("pid")
            alive = process_alive(pid)
            if alive is not False:
                raise LedgerHold("INTERRUPTED_WRITER_LIVENESS_UNVERIFIED")
            if a.minimum_age_seconds < 300:
                raise LedgerHold("RECOVERY_MINIMUM_AGE_CANNOT_BE_SHORTENED")
            started = parse_expiry(previous_lock.get("started_at"), "INTERRUPTED_LOCK_TIME_INVALID")
            age = (now() - started).total_seconds()
            if age < a.minimum_age_seconds:
                raise LedgerHold("INTERRUPTED_LOCK_TOO_RECENT")
            if not a.operator_evidence_ref:
                raise LedgerHold("RECOVERY_OPERATOR_EVIDENCE_REQUIRED")
            operator_evidence_sha = file_digest(project, a.operator_evidence_ref)
            git_before = inspect_git(project)
            files = inventory(project, data, root)
            stats = reconcile(project, data, root, {}, files,
                              "QUARANTINE_UNRESOLVED", False, None, False)
            save(path, data)
            git_after = inspect_git(project)
            return {"status": "RECOVERED_INTERRUPTION_OUTPUTS_QUARANTINED",
                    "previous_pid": pid, "previous_operation": previous_lock.get("operation"),
                    "ledger_revision": data["revision"],
                    "operator_evidence_ref": a.operator_evidence_ref,
                    "operator_evidence_sha256": operator_evidence_sha,
                    "git_before": {"head": git_before["head"], "changed": git_before["changed"]},
                    "git_after": {"head": git_after["head"], "changed": git_after["changed"]},
                    "git_binding_unchanged": (git_before["head"] == git_after["head"] and
                                               git_before["changed"] == git_after["changed"]),
                    **stats}
        if a.action == "observe-git":
            observation = inspect_git(project)
            history = data.setdefault("git_observations", [])
            newest = history[-1] if history else None
            if newest and newest["head"] == observation["head"] and newest["changed"] == observation["changed"]:
                return {"status": "SOURCE_GIT_UNCHANGED", "head": observation["head"],
                        "changed_count": len(observation["changed"]), "ledger_revision": data["revision"]}
            history.append(observation)
            if len(history) > 32:
                del history[:-32]
            save(path, data)
            return {"status": "SOURCE_GIT_OBSERVED", "head": observation["head"],
                    "changed_count": len(observation["changed"]), "ledger_revision": data["revision"]}
        if a.action == "init-root":
            name = safe_root(a.root)
            p = confined(project, name)
            if name in data["roots"] or p.exists() or p.is_symlink():
                raise LedgerHold("PREEXISTING_ROOT_CANNOT_BE_CLAIMED")
            if not a.owner.strip() or not a.campaign.strip():
                raise LedgerHold("OWNER_AND_CAMPAIGN_REQUIRED")
            p.mkdir(parents=True, exist_ok=False)
            item = {"id": uuid.uuid4().hex, "owner": a.owner,
                    "campaign": a.campaign, "created_at": stamp(now())}
            (p / MARKER).write_text(json.dumps(
                {"schema_version": VERSION, "root": name, **item}) + "\n",
                encoding="utf-8")
            (p / ".gitignore").write_text("*\n", encoding="utf-8")
            data["roots"][name] = item
            save(path, data)
            return {"status": "ROOT_REGISTERED", "root": name}
        if a.action in {"reconcile", "capture"}:
            root = safe_root(a.root)
            if root not in data["roots"]:
                raise LedgerHold("ROOT_NOT_REGISTERED")
            before = inventory(project, data, root)
            exit_code = 0
            if a.action == "capture":
                cmd = list(a.command)
                if cmd and cmd[0] == "--":
                    cmd.pop(0)
                if not cmd:
                    raise LedgerHold("CAPTURE_COMMAND_REQUIRED")
                if a.safe_delete and (
                    a.category not in DELETABLE or a.ttl_hours is None):
                    raise LedgerHold("DELETE_CLASS_AND_TTL_REQUIRED")
                try:
                    exit_code = subprocess.run(cmd, cwd=project, check=False).returncode
                except OSError:
                    exit_code = 127
            after = inventory(project, data, root)
            stats = reconcile(
                project, data, root, before if a.action == "capture" else {},
                after, a.category if a.action == "capture" else "QUARANTINE_UNRESOLVED",
                a.safe_delete if a.action == "capture" else False,
                a.ttl_hours if a.action == "capture" else None,
                a.action == "capture" and exit_code == 0)
            save(path, data)
            return {"status": "CAPTURED" if exit_code == 0 else "FAILED_OUTPUTS_QUARANTINED",
                    "exit_code": exit_code, **stats}
        if a.action == "classify":
            name = relative(a.path)
            entry = data["files"].get(name)
            if entry is None or entry["status"] != "OBSERVED":
                raise LedgerHold("UNREGISTERED_FILE")
            root_auth = data["roots"][entry["root"]]
            if a.owner != root_auth["owner"] or a.campaign != root_auth["campaign"]:
                raise LedgerHold("WRONG_OWNER_OR_CAMPAIGN")
            if (entry["category"] in {
                "SOURCE_VERSIONED", "CANONICAL_STATE", "IMMUTABLE_EVIDENCE",
                "SENSITIVE_LOCAL", "EXTERNAL_CANONICAL"}
                and entry["category"] != a.category):
                raise LedgerHold("PROTECTED_CLASS_CANNOT_BE_DEMOTED")
            if a.safe_delete and (
                a.category not in DELETABLE or a.ttl_hours is None):
                raise LedgerHold("DELETE_CLASS_OR_TTL_INVALID")
            if a.ttl_hours is not None and not (-24 <= a.ttl_hours <= 24 * 365):
                raise LedgerHold("RETENTION_OUT_OF_RANGE")
            if fingerprint(confined(project, name)) != entry["fingerprint"]:
                entry.update(category="QUARANTINE_UNRESOLVED", safe_delete=False)
                save(path, data)
                raise LedgerHold("CHANGED_FILE_NEEDS_RECONCILIATION")
            entry.update(category=a.category, safe_delete=a.safe_delete,
                         review_closed=False, review_evidence=None,
                         expires_at=stamp(now()+timedelta(hours=a.ttl_hours))
                         if a.ttl_hours is not None else None)
            save(path, data)
            return {"status": "CLASSIFIED", "path": name}
        if a.action == "review":
            name = relative(a.path)
            entry = data["files"].get(name)
            if entry is None or entry["status"] != "OBSERVED":
                raise LedgerHold("UNREGISTERED_FILE")
            root_auth = data["roots"][entry["root"]]
            if a.owner != root_auth["owner"] or a.campaign != root_auth["campaign"]:
                raise LedgerHold("WRONG_OWNER_OR_CAMPAIGN")
            if not a.reviewer.strip() or a.reviewer.strip() == root_auth["owner"]:
                raise LedgerHold("REVIEWER_MUST_BE_NAMED_AND_DISTINCT")
            current_fingerprint = fingerprint(confined(project, name))
            if current_fingerprint != entry["fingerprint"]:
                entry.update(category="QUARANTINE_UNRESOLVED", safe_delete=False,
                             review_closed=False, review_evidence=None, expires_at=None)
                save(path, data)
                raise LedgerHold("CHANGED_FILE_NEEDS_RECONCILIATION")
            evidence_sha = file_digest(project, a.evidence_ref)
            entry["review_evidence"] = {
                "decision": a.decision, "reviewer": a.reviewer.strip(),
                "evidence_ref": a.evidence_ref,
                "evidence_sha256": evidence_sha,
                "reviewed_at": stamp(now()),
                "artifact_sha256": current_fingerprint["sha256"],
            }
            entry["review_closed"] = a.decision == "ACCEPTED"
            save(path, data)
            return {"status": "REVIEW_RECORDED", "path": name,
                    "decision": a.decision, "evidence_sha256": evidence_sha,
                    "reviewer_identity_authentication": "NOT_PROVEN_LOCAL_ATTESTATION_ONLY"}
        if a.action == "dependency":
            name = relative(a.path)
            dependent = relative(a.dependent)
            entry = data["files"].get(name)
            target = data["files"].get(dependent)
            if (entry is None or entry["status"] != "OBSERVED" or target is None or
                target["status"] != "OBSERVED"):
                raise LedgerHold("DEPENDENCY_FILE_UNREGISTERED_OR_MISSING")
            owner = data["roots"].get(entry["root"])
            if not owner or a.owner != owner["owner"] or a.campaign != owner["campaign"]:
                raise LedgerHold("WRONG_OWNER_OR_CAMPAIGN")
            if not target.get("review_evidence") or target["review_evidence"].get("decision") != "ACCEPTED":
                raise LedgerHold("DEPENDENT_MUST_HAVE_ACCEPTED_REVIEW_EVIDENCE")
            if not a.reviewer.strip() or a.reviewer.strip() == owner["owner"]:
                raise LedgerHold("REVIEWER_MUST_BE_NAMED_AND_DISTINCT")
            evidence_sha = file_digest(project, a.evidence_ref)
            current = entry.setdefault("dependents", [])
            if a.operation == "add":
                if dependent not in current:
                    current.append(dependent)
                    current.sort()
            else:
                if dependent not in current:
                    raise LedgerHold("DEPENDENCY_EDGE_NOT_PRESENT")
                current.remove(dependent)
                entry.setdefault("dependency_history", []).append({
                    "dependent": dependent, "reviewer": a.reviewer.strip(),
                    "evidence_ref": a.evidence_ref,
                    "evidence_sha256": evidence_sha,
                    "removed_at": stamp(now()),
                })
            save(path, data)
            return {"status": "DEPENDENCY_RECORDED", "path": name,
                    "dependent": dependent, "operation": a.operation,
                    "evidence_sha256": evidence_sha}
        if a.action in {"gc", "cleangarbage"}:
            return execute_gc(project, data, a)
    raise LedgerHold("UNKNOWN_ACTION")


def main():
    p = argparse.ArgumentParser(description="Project-local generated file inventory and safe GC")
    p.add_argument("--project", required=True)
    p.add_argument("--control-dir", default=".agentic-sdlc")
    sub = p.add_subparsers(dest="action", required=True)
    init = sub.add_parser("init-root")
    init.add_argument("--root", required=True)
    init.add_argument("--owner", required=True)
    init.add_argument("--campaign", required=True)
    sub.add_parser("report")
    sub.add_parser("observe-git")
    rec = sub.add_parser("reconcile")
    rec.add_argument("--root", required=True)
    cap = sub.add_parser("capture")
    cap.add_argument("--root", required=True)
    cap.add_argument("--category", default="QUARANTINE_UNRESOLVED", choices=CLASSES)
    cap.add_argument("--safe-delete", action="store_true")
    cap.add_argument("--ttl-hours", type=float)
    cap.add_argument("command", nargs=argparse.REMAINDER)
    cls = sub.add_parser("classify")
    cls.add_argument("--path", required=True)
    cls.add_argument("--owner", required=True)
    cls.add_argument("--campaign", required=True)
    cls.add_argument("--category", required=True, choices=CLASSES)
    cls.add_argument("--safe-delete", action="store_true")
    cls.add_argument("--ttl-hours", type=float)
    review = sub.add_parser("review")
    review.add_argument("--path", required=True)
    review.add_argument("--owner", required=True)
    review.add_argument("--campaign", required=True)
    review.add_argument("--reviewer", required=True)
    review.add_argument("--decision", choices=("ACCEPTED", "REJECTED"), required=True)
    review.add_argument("--evidence-ref", required=True)
    dependency = sub.add_parser("dependency")
    dependency.add_argument("--path", required=True, help="artifact that is retained while its dependent is accepted")
    dependency.add_argument("--dependent", required=True)
    dependency.add_argument("--operation", choices=("add", "remove"), required=True)
    dependency.add_argument("--owner", required=True)
    dependency.add_argument("--campaign", required=True)
    dependency.add_argument("--reviewer", required=True)
    dependency.add_argument("--evidence-ref", required=True)
    approve = sub.add_parser("approve-gc")
    approve.add_argument("--plan-file", required=True)
    approve.add_argument("--path", required=True)
    approve.add_argument("--reviewer", required=True)
    approve.add_argument("--evidence-ref", required=True)
    approve.add_argument("--approval-out", required=True)
    approve.add_argument("--lease-minutes", type=int, default=5)
    recovery = sub.add_parser("recover-lock")
    recovery.add_argument("--root", required=True)
    recovery.add_argument("--owner", required=True)
    recovery.add_argument("--campaign", required=True)
    recovery.add_argument("--minimum-age-seconds", type=int, default=300)
    recovery.add_argument("--operator-evidence-ref")
    g = sub.add_parser("gc")
    g.add_argument("--execute", action="store_true")
    g.add_argument("--approval")
    clean = sub.add_parser("cleangarbage", help="L3-owned cleanup workflow: dry-run default")
    clean.add_argument("--execute", action="store_true")
    clean.add_argument("--approval")
    a = p.parse_args()
    try:
        result = operate(a)
        print(json.dumps(result, indent=2, sort_keys=True))
        return result.get("exit_code") or 0
    except (LedgerHold, OSError, ValueError, subprocess.SubprocessError) as e:
        reason = (str(e) if isinstance(e, LedgerHold) else "OS_OR_RUNTIME_" + type(e).__name__ + (("_" + str(e.errno)) if isinstance(e, OSError) and e.errno is not None else ""))
        print(json.dumps({"status": "HOLD", "failure_codes": [reason]}, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
