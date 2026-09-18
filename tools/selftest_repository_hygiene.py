#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_DELTA = ROOT / "tools" / "repo_delta.py"
WORKSPACE_GC = ROOT / "tools" / "workspace_gc.py"
COMMIT_GUARD = ROOT / "tools" / "commit_guard.py"


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def git(cwd: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(cwd), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode:
        raise AssertionError(completed.stderr or completed.stdout)
    return completed.stdout.strip()


def init_remote_case(base: Path) -> tuple[Path, Path, Path, str]:
    base.mkdir(parents=True, exist_ok=True)
    seed = base / "seed"
    remote = base / "remote.git"
    worker = base / "worker"
    seed.mkdir()
    git(seed, "init", "-b", "main")
    git(seed, "config", "user.email", "example.invalid")
    git(seed, "config", "user.name", "Example")
    (seed / "a.txt").write_text("one\n", encoding="utf-8")
    git(seed, "add", "a.txt")
    git(seed, "commit", "-m", "base")
    git(base, "init", "--bare", str(remote))
    git(seed, "remote", "add", "origin", str(remote))
    git(seed, "push", "-u", "origin", "main")
    subprocess.run(
        ["git", "clone", "--branch", "main", str(remote), str(worker)],
        capture_output=True,
        text=True,
        check=True,
    )
    baseline = git(worker, "rev-parse", "HEAD")
    return seed, remote, worker, baseline


def test_repo_delta(base: Path) -> None:
    seed, _, worker, baseline = init_remote_case(base / "delta")
    (seed / "b.txt").write_text("two\n", encoding="utf-8")
    git(seed, "add", "b.txt")
    git(seed, "commit", "-m", "upstream")
    git(seed, "push", "origin", "main")

    before = git(worker, "rev-parse", "HEAD")
    result = run(
        str(REPO_DELTA),
        "--repo",
        str(worker),
        "--branch",
        "main",
        "--baseline",
        baseline,
        "--fetch",
        "--json",
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    payload = json.loads(result.stdout)
    if payload["local_remote_relation"] != "LOCAL_BEHIND":
        raise AssertionError(payload)
    if payload["changed_paths_from_baseline"] != ["b.txt"]:
        raise AssertionError(payload)
    if git(worker, "rev-parse", "HEAD") != before:
        raise AssertionError("repo_delta mutated local HEAD")
    if payload["fetch_scope"] != "refs/heads/main":
        raise AssertionError("repo_delta did not report exact branch scope")


def test_commit_guard(base: Path) -> None:
    repo = base / "commit"
    repo.mkdir()
    git(repo, "init", "-b", "main")
    git(repo, "config", "user.email", "example.invalid")
    git(repo, "config", "user.name", "Example")
    (repo / "x.txt").write_text("base\n", encoding="utf-8")
    git(repo, "add", "x.txt")
    git(repo, "commit", "-m", "base")
    (repo / "x.txt").write_text("candidate\n", encoding="utf-8")
    git(repo, "add", "x.txt")

    worker = run(
        str(COMMIT_GUARD),
        "--repo",
        str(repo),
        "--role",
        "I4_EXECUTION_TEAM_MEMBER",
        "--boundary",
        "COHERENT_CANDIDATE",
    )
    if worker.returncode == 0:
        raise AssertionError("I4 canonical commit authority was incorrectly accepted")

    lead = run(
        str(COMMIT_GUARD),
        "--repo",
        str(repo),
        "--role",
        "I3_ENGINEERING_CAMPAIGN_LEAD",
        "--boundary",
        "COHERENT_CANDIDATE",
        "--json",
    )
    if lead.returncode != 0:
        raise AssertionError(lead.stderr)
    if json.loads(lead.stdout)["canonical_commit_allowed"] is not True:
        raise AssertionError("I3 coherent staged candidate was not authorized")


def register(path: Path, lifecycle: str, *, safe: bool, ttl: float) -> None:
    args = [
        str(WORKSPACE_GC),
        "register",
        "--path",
        str(path),
        "--class",
        lifecycle,
        "--owner",
        "I3_ENGINEERING_CAMPAIGN_LEAD",
        "--ttl-hours",
        str(ttl),
    ]
    if safe:
        args.append("--safe-delete")
    result = run(*args)
    if result.returncode != 0:
        raise AssertionError(result.stderr)


def test_workspace_gc(base: Path) -> None:
    root = base / "gc"
    root.mkdir()
    expired = root / "expired"
    protected = root / "protected"
    future = root / "future"
    dirty = root / "dirty"
    unmarked = root / "unmarked"
    outside = base / "outside"
    unmarked.mkdir()
    outside.mkdir()
    (outside / "keep.txt").write_text("keep\n", encoding="utf-8")

    register(expired, "EPHEMERAL_RECONSTRUCTIBLE", safe=True, ttl=-1)
    register(protected, "PROTECTED_CURRENT_OR_EVIDENCE", safe=False, ttl=-1)
    register(future, "CACHE_RECONSTRUCTIBLE", safe=True, ttl=24)
    register(dirty, "EPHEMERAL_RECONSTRUCTIBLE", safe=True, ttl=-1)
    git(dirty, "init", "-b", "main")
    git(dirty, "config", "user.email", "example.invalid")
    git(dirty, "config", "user.name", "Example")
    (dirty / "tracked.txt").write_text("base\n", encoding="utf-8")
    git(dirty, "add", "tracked.txt", ".agentic-sdlc-workspace.json")
    git(dirty, "commit", "-m", "base")
    (dirty / "tracked.txt").write_text("dirty\n", encoding="utf-8")

    dry = run(str(WORKSPACE_GC), "collect", "--root", str(root))
    if dry.returncode != 0:
        raise AssertionError(dry.stderr)
    dry_payload = json.loads(dry.stdout)
    if not expired.exists():
        raise AssertionError("dry-run deleted candidate")
    rows = {Path(row["path"]).name: row for row in dry_payload["rows"]}
    if rows["expired"]["decision"] != "DELETE_READY":
        raise AssertionError(rows["expired"])
    if rows["protected"]["decision"] != "BLOCK":
        raise AssertionError(rows["protected"])
    if rows["future"]["decision"] != "KEEP":
        raise AssertionError(rows["future"])
    if rows["dirty"]["reason"] != "DIRTY_GIT_WORKSPACE":
        raise AssertionError(rows["dirty"])
    if dry_payload["unmarked_directories_ignored"] != 1:
        raise AssertionError("unmarked directory was not ignored")

    execute = run(str(WORKSPACE_GC), "collect", "--root", str(root), "--execute")
    if execute.returncode != 0:
        raise AssertionError(execute.stderr)
    if expired.exists():
        raise AssertionError("expired safe workspace was not deleted")
    if not protected.exists() or not future.exists() or not dirty.exists() or not unmarked.exists():
        raise AssertionError("GC deleted a blocked/kept/unmarked workspace")
    if not outside.exists():
        raise AssertionError("GC escaped explicit root")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="agentic-sdlc-repo-hygiene-") as tmp:
        base = Path(tmp)
        test_repo_delta(base)
        test_commit_guard(base)
        test_workspace_gc(base)

    protocol = (ROOT / "protocols" / "REPOSITORY_EFFICIENCY_AND_WORKSPACE_HYGIENE.md").read_text(
        encoding="utf-8"
    )
    for required in (
        "COMMIT_MANIA",
        "Delta-first remote currentness",
        "I4 Execution Team Members MUST NOT create canonical commits",
        "Unmarked directories are UNKNOWN",
    ):
        if required not in protocol:
            raise AssertionError(f"repository hygiene invariant missing: {required}")

    print("REPOSITORY EFFICIENCY / HYGIENE SELF-TEST PASSED")
    print("- exact-branch fetch reports delta without pulling/mutating local HEAD")
    print("- I4 canonical commit authority is rejected")
    print("- I3 coherent candidate commit boundary is accepted")
    print("- GC is dry-run by default")
    print("- expired pre-authorized workspace is deleted")
    print("- protected, future, dirty and unmarked workspaces are preserved")
    print("- GC cannot escape its explicit root")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
