#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


MARKER = ".agentic-sdlc-workspace.json"
DELETABLE_CLASSES = {
    "EPHEMERAL_RECONSTRUCTIBLE",
    "CACHE_RECONSTRUCTIBLE",
    "SHORT_TERM_EVIDENCE",
}
BLOCKED_CLASSES = {
    "QUARANTINE_UNRESOLVED",
    "PROTECTED_CURRENT_OR_EVIDENCE",
}


class GCError(RuntimeError):
    pass


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_iso(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def git(path: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", "-C", str(path), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if check and completed.returncode:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise GCError(f"git {' '.join(args)} failed: {detail}")
    return completed


def is_git_workspace(path: Path) -> bool:
    completed = git(path, "rev-parse", "--is-inside-work-tree", check=False)
    return completed.returncode == 0 and completed.stdout.strip() == "true"


def git_dirty(path: Path) -> bool:
    completed = git(path, "status", "--porcelain=v1", "--untracked-files=all")
    return bool(completed.stdout.strip())


def linked_worktree(path: Path) -> bool:
    return (path / ".git").is_file()


def directory_size(path: Path) -> int:
    total = 0
    for child in path.rglob("*"):
        try:
            if child.is_file() and not child.is_symlink():
                total += child.stat().st_size
        except OSError:
            continue
    return total


def load_marker(path: Path) -> dict[str, Any]:
    marker = path / MARKER
    try:
        value = json.loads(marker.read_text(encoding="utf-8"))
    except Exception as exc:
        raise GCError(f"invalid marker {marker}: {exc}") from exc
    if not isinstance(value, dict):
        raise GCError(f"marker is not an object: {marker}")
    required = {
        "schema_version",
        "workspace_id",
        "lifecycle_class",
        "owner",
        "created_at",
        "expires_at",
        "safe_delete",
    }
    missing = sorted(required - set(value))
    if missing:
        raise GCError(f"marker missing fields {missing}: {marker}")
    if value["schema_version"] != "workspace-lifecycle-0.1":
        raise GCError(f"unsupported marker schema: {value['schema_version']}")
    return value


def classify(path: Path, marker: dict[str, Any], now: datetime) -> dict[str, Any]:
    lifecycle = str(marker["lifecycle_class"])
    result: dict[str, Any] = {
        "path": str(path),
        "workspace_id": marker["workspace_id"],
        "lifecycle_class": lifecycle,
        "owner": marker["owner"],
        "safe_delete": bool(marker["safe_delete"]),
        "expires_at": marker["expires_at"],
        "decision": None,
        "reason": None,
        "bytes": directory_size(path),
        "git_backed": False,
        "linked_worktree": False,
    }

    if path.is_symlink():
        result["decision"] = "BLOCK"
        result["reason"] = "SYMLINK_ROOT"
        return result
    if (path / ".keep").exists() or (path / ".agentic-sdlc-active").exists():
        result["decision"] = "BLOCK"
        result["reason"] = "ACTIVE_OR_KEEP_SENTINEL"
        return result

    lease_until = marker.get("lease_until")
    if lease_until:
        try:
            if parse_iso(str(lease_until)) > now:
                result["decision"] = "BLOCK"
                result["reason"] = "ACTIVE_LEASE"
                return result
        except ValueError:
            result["decision"] = "BLOCK"
            result["reason"] = "INVALID_LEASE"
            return result

    if lifecycle in BLOCKED_CLASSES:
        result["decision"] = "BLOCK"
        result["reason"] = "PROTECTED_OR_QUARANTINED_CLASS"
        return result
    if lifecycle not in DELETABLE_CLASSES:
        result["decision"] = "BLOCK"
        result["reason"] = "UNKNOWN_LIFECYCLE_CLASS"
        return result
    if not marker["safe_delete"]:
        result["decision"] = "BLOCK"
        result["reason"] = "SAFE_DELETE_FALSE"
        return result

    try:
        expires_at = parse_iso(str(marker["expires_at"]))
    except ValueError:
        result["decision"] = "BLOCK"
        result["reason"] = "INVALID_EXPIRY"
        return result
    if expires_at > now:
        result["decision"] = "KEEP"
        result["reason"] = "NOT_EXPIRED"
        return result

    if is_git_workspace(path):
        result["git_backed"] = True
        result["linked_worktree"] = linked_worktree(path)
        if git_dirty(path):
            result["decision"] = "BLOCK"
            result["reason"] = "DIRTY_GIT_WORKSPACE"
            return result

    result["decision"] = "DELETE_READY"
    result["reason"] = "EXPIRED_PREAUTHORIZED_CLEAN"
    return result


def remove_candidate(path: Path, row: dict[str, Any]) -> None:
    if row["git_backed"] and row["linked_worktree"]:
        completed = git(path, "worktree", "remove", "--force", str(path), check=False)
        if completed.returncode:
            detail = completed.stderr.strip() or completed.stdout.strip()
            raise GCError(f"git worktree remove failed for {path}: {detail}")
        return
    shutil.rmtree(path)


def register(args: argparse.Namespace) -> int:
    path = Path(args.path).resolve()
    path.mkdir(parents=True, exist_ok=True)
    marker_path = path / MARKER
    if marker_path.exists() and not args.force:
        raise GCError(f"marker already exists: {marker_path}")

    now = utc_now()
    expires = now + timedelta(hours=float(args.ttl_hours))
    payload = {
        "schema_version": "workspace-lifecycle-0.1",
        "workspace_id": args.workspace_id or f"workspace-{uuid.uuid4().hex[:12]}",
        "lifecycle_class": args.lifecycle_class,
        "owner": args.owner,
        "created_at": iso(now),
        "expires_at": iso(expires),
        "lease_until": None,
        "safe_delete": bool(args.safe_delete),
        "source_repo": args.source_repo,
        "source_ref": args.source_ref,
        "reason": args.reason,
    }
    marker_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2) if args.json else f"WORKSPACE REGISTERED: {path}")
    return 0


def collect(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    if not root.is_dir():
        raise GCError(f"GC root unavailable: {root}")
    now = parse_iso(args.now) if args.now else utc_now()

    rows: list[dict[str, Any]] = []
    unmarked = 0
    invalid = 0
    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.is_symlink():
            continue
        marker_path = child / MARKER
        if not marker_path.exists():
            unmarked += 1
            continue
        try:
            marker = load_marker(child)
            row = classify(child, marker, now)
        except GCError as exc:
            invalid += 1
            rows.append(
                {
                    "path": str(child),
                    "decision": "BLOCK",
                    "reason": "INVALID_MARKER",
                    "error": str(exc),
                    "bytes": directory_size(child),
                }
            )
            continue
        rows.append(row)

    deleted: list[str] = []
    reclaimed = 0
    if args.execute:
        for row in rows:
            if row.get("decision") != "DELETE_READY":
                continue
            path = Path(row["path"]).resolve()
            try:
                path.relative_to(root)
            except ValueError as exc:
                raise GCError(f"candidate escaped GC root: {path}") from exc
            if path.parent != root:
                raise GCError(f"candidate is not an immediate child of GC root: {path}")
            before = int(row.get("bytes") or 0)
            remove_candidate(path, row)
            deleted.append(str(path))
            reclaimed += before
            row["decision"] = "DELETED"
            row["reason"] = "EXECUTED_PREAUTHORIZED_CLEANUP"

    report = {
        "schema_version": "workspace-gc-report-0.1",
        "root": str(root),
        "mode": "execute" if args.execute else "dry-run",
        "observed_at": iso(now),
        "marked_candidates": len(rows),
        "unmarked_directories_ignored": unmarked,
        "invalid_markers_blocked": invalid,
        "delete_ready": sum(1 for row in rows if row.get("decision") == "DELETE_READY"),
        "deleted_count": len(deleted),
        "reclaimed_bytes": reclaimed,
        "rows": rows,
    }
    print(json.dumps(report, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Marker-owned local workspace garbage collector.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_register = sub.add_parser("register")
    p_register.add_argument("--path", required=True)
    p_register.add_argument(
        "--class",
        dest="lifecycle_class",
        required=True,
        choices=sorted(DELETABLE_CLASSES | BLOCKED_CLASSES),
    )
    p_register.add_argument("--owner", required=True)
    p_register.add_argument("--ttl-hours", required=True, type=float)
    p_register.add_argument("--safe-delete", action="store_true")
    p_register.add_argument("--source-repo")
    p_register.add_argument("--source-ref")
    p_register.add_argument("--reason", default="")
    p_register.add_argument("--workspace-id")
    p_register.add_argument("--force", action="store_true")
    p_register.add_argument("--json", action="store_true")

    p_collect = sub.add_parser("collect")
    p_collect.add_argument("--root", required=True)
    p_collect.add_argument("--execute", action="store_true")
    p_collect.add_argument("--now", help="Override current UTC time for deterministic tests.")
    p_collect.add_argument("--json", action="store_true")

    args = parser.parse_args()
    try:
        if args.command == "register":
            return register(args)
        return collect(args)
    except (GCError, OSError, subprocess.TimeoutExpired) as exc:
        print(f"WORKSPACE GC FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
