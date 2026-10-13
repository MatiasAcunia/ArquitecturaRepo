#!/usr/bin/env python3
"""Local persistent artifact registry: file-level, fail-closed garbage collection.

Only newly registered system-owned scratch roots can be cleaned. This is not
an OS filesystem monitor; unwrapped host/IDE writes need separate readback.
Whole worktree cleanup stays with workspace_gc.py.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

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
SAFE_SEGMENT = re.compile(r"^[A-Za-z0-9._-]{1,100}$")


class LedgerHold(ValueError):
    pass


def now():
    return datetime.now(timezone.utc)


def stamp(t):
    return t.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def relative(s):
    if (not isinstance(s, str) or not s or len(s) > 700 or
        s.startswith(("/", "\\")) or "\\" in s or ":" in s or "\x00" in s or
        any(x in {"", ".", ".."} or not SAFE_SEGMENT.fullmatch(x) for x in s.split("/"))):
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
            "created_at": s, "updated_at": s, "roots": {}, "files": {}}


def safe_root(name):
    name = relative(name)
    if name != ".agentic-sdlc-scratch" and not name.startswith(".agentic-sdlc-scratch/"):
        raise LedgerHold("UNMANAGED_OUTPUT_ROOT")
    return name


def validate(d):
    if (not isinstance(d, dict) or set(d) != {
        "schema_version", "revision", "created_at", "updated_at", "roots", "files"
    } or d["schema_version"] != VERSION or
        type(d["revision"]) is not int or d["revision"] < 0 or
        not isinstance(d["roots"], dict) or not isinstance(d["files"], dict) or
        len(d["files"]) > 160000):
        raise LedgerHold("LEDGER_INVALID")
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
            not isinstance(item.get("fingerprint"), dict) or
            not re.fullmatch(r"[0-9a-f]{64}", str(item["fingerprint"].get("sha256")))):
            raise LedgerHold("LEDGER_FILE_RECORD_INVALID")
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
def locked(path):
    lock = path.with_name(path.name + ".lock")
    if lock.is_symlink():
        raise LedgerHold("LEDGER_LOCK_SYMLINK")
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise LedgerHold("LEDGER_WRITER_OR_CRASH_LOCK_REQUIRES_REVIEW") from None
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(str(os.getpid()))
            f.flush()
            os.fsync(f.fileno())
        yield
    finally:
        try:
            lock.unlink()
        except FileNotFoundError:
            pass


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
            "review_closed": category in DELETABLE, "dependencies": [],
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
        actual = command("rev-parse", "--show-toplevel")
        if actual.returncode or Path(actual.stdout.strip()).resolve() != project.resolve():
            return "PROJECT_GIT_ROOT_NOT_VERIFIED"
        if command("ls-files", "--error-unmatch", "--", name).returncode == 0:
            return "GIT_TRACKED_FILE"
        if command("check-ignore", "-q", "--", name).returncode != 0:
            return "FILE_NOT_IGNORED"
    except OSError:
        return "GIT_UNAVAILABLE"
    return None


def ready(project, data, name, unknown_roots):
    entry = data["files"][name]
    if entry["status"] != "OBSERVED":
        return "BLOCK", "NOT_OBSERVED"
    if entry["root"] in unknown_roots:
        return "BLOCK", "UNREGISTERED_FILES_PRESENT"
    if entry["category"] not in DELETABLE:
        return "BLOCK", "PROTECTED_OR_UNKNOWN_CLASS"
    if not entry["safe_delete"] or not entry["review_closed"] or entry["dependencies"]:
        return "BLOCK", "REVIEW_REFERENCE_OR_DELETE_PERMISSION_MISSING"
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
    if p.suffix.lower() in {".db", ".sqlite", ".sqlite3", ".sql", ".env", ".key", ".pem"} or p.name.endswith(("-wal", "-shm")):
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


def gc_plan(project, data):
    observed = {root: inventory(project, data, root) for root in data["roots"]}
    unknown = {root for root, files in observed.items()
               if any(name not in data["files"] for name in files)}
    rows = []
    for name, entry in sorted(data["files"].items()):
        if entry["status"] == "DELETED":
            continue
        decision, reason = ("BLOCK", "PHYSICAL_FILE_MISSING") if (
            name not in observed.get(entry["root"], {})
        ) else ready(project, data, name, unknown)
        rows.append({"path": name, "category": entry["category"],
                     "bytes": entry["fingerprint"]["size"],
                     "decision": decision, "reason": reason})
    return {"schema_version": "artifact-gc-report-v1", "mode": "dry-run",
            "revision": data["revision"], "unregistered_roots": sorted(unknown),
            "rows": rows, "ready_count": sum(r["decision"] == "DELETE_READY" for r in rows),
            "deleted_count": 0, "reclaimed_bytes": 0}


def operate(a):
    project = Path(a.project).absolute()
    if not project.is_dir() or project.is_symlink():
        raise LedgerHold("PROJECT_UNTRUSTED")
    path = ledger_file(project, a.control_dir)
    if a.action == "report":
        data = load(path)
        return {"status": "PERSISTED", "revision": data["revision"],
                "files": len(data["files"]), "roots": len(data["roots"])}
    if a.action == "gc" and not a.execute:
        return gc_plan(project, load(path))
    with locked(path):
        data = load(path)
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
            (p / ".gitignore").write_text(
                "*\n!.gitignore\n!" + MARKER + "\n", encoding="utf-8")
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
            if fingerprint(confined(project, name)) != entry["fingerprint"]:
                entry.update(category="QUARANTINE_UNRESOLVED", safe_delete=False)
                save(path, data)
                raise LedgerHold("CHANGED_FILE_NEEDS_RECONCILIATION")
            entry.update(category=a.category, safe_delete=a.safe_delete,
                         review_closed=a.review_closed,
                         expires_at=stamp(now()+timedelta(hours=a.ttl_hours))
                         if a.ttl_hours is not None else None)
            save(path, data)
            return {"status": "CLASSIFIED", "path": name}
        if a.action == "gc":
            result = gc_plan(project, data)
            unregistered = set(result["unregistered_roots"])
            for row in result["rows"]:
                if row["decision"] != "DELETE_READY":
                    continue
                name = row["path"]
                decision, reason = ready(project, data, name, unregistered)
                if decision != "DELETE_READY":
                    row.update(decision="BLOCK", reason=reason)
                    continue
                try:
                    confined(project, name).unlink()
                except OSError:
                    row.update(decision="BLOCK", reason="OS_DELETE_REFUSED")
                    continue
                data["files"][name].update(status="DELETED", safe_delete=False)
                row.update(decision="DELETED", reason="CONTROLLED_REMOVAL")
                save(path, data)
            result["mode"] = "execute"
            result["deleted_count"] = sum(r["decision"] == "DELETED" for r in result["rows"])
            result["reclaimed_bytes"] = sum(
                r["bytes"] for r in result["rows"] if r["decision"] == "DELETED")
            return result
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
    cls.add_argument("--review-closed", action="store_true")
    cls.add_argument("--ttl-hours", type=float)
    g = sub.add_parser("gc")
    g.add_argument("--execute", action="store_true")
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
