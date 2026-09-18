#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


class DeltaError(RuntimeError):
    pass


def git(repo: Path, *args: str, timeout: int = 90, check: bool = True) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
    )
    if check and completed.returncode:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise DeltaError(f"git {' '.join(args)} failed: {detail}")
    return completed.stdout.strip()


def is_ancestor(repo: Path, base: str, head: str) -> bool:
    completed = subprocess.run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", base, head],
        capture_output=True,
        timeout=30,
        check=False,
    )
    return completed.returncode == 0


def relation(repo: Path, local: str, remote: str) -> str:
    if local == remote:
        return "EXACT"
    if is_ancestor(repo, local, remote):
        return "LOCAL_BEHIND"
    if is_ancestor(repo, remote, local):
        return "LOCAL_AHEAD"
    return "DIVERGED"


def changed_paths(repo: Path, base: str, head: str) -> list[str]:
    if base == head:
        return []
    value = git(
        repo,
        "diff",
        "--name-only",
        "--diff-filter=ACDMRTUXB",
        base,
        head,
        "--",
    )
    return [line.replace("\\", "/") for line in value.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Refresh exactly one remote branch and report repository delta without pull/merge/checkout."
    )
    parser.add_argument("--repo", default=".", help="Existing local Git repository/worktree.")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--branch", help="Branch to inspect; defaults to current branch.")
    parser.add_argument(
        "--baseline",
        help="Known prior SHA/ref used to compute the context-acquisition delta. Defaults to local HEAD.",
    )
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Fetch only the exact remote branch ref, without tags or submodules.",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        repo = Path(args.repo).resolve()
        if not repo.is_dir():
            raise DeltaError(f"repository directory unavailable: {repo}")
        git(repo, "rev-parse", "--git-dir")
        branch = args.branch or git(repo, "branch", "--show-current")
        if not branch:
            raise DeltaError("detached HEAD requires explicit --branch")

        local_head = git(repo, "rev-parse", "HEAD")
        remote_ref = f"refs/remotes/{args.remote}/{branch}"
        if args.fetch:
            refspec = f"+refs/heads/{branch}:{remote_ref}"
            git(
                repo,
                "fetch",
                "--no-tags",
                "--no-recurse-submodules",
                "--quiet",
                args.remote,
                refspec,
            )

        remote_head = git(repo, "rev-parse", remote_ref)
        baseline = args.baseline or local_head
        git(repo, "cat-file", "-e", f"{baseline}^{{commit}}")
        baseline_sha = git(repo, "rev-parse", baseline)

        payload: dict[str, Any] = {
            "schema_version": "repository-delta-0.1",
            "repo": str(repo),
            "remote": args.remote,
            "branch": branch,
            "fetch_performed": bool(args.fetch),
            "fetch_scope": f"refs/heads/{branch}",
            "local_head": local_head,
            "remote_head": remote_head,
            "baseline": baseline_sha,
            "local_remote_relation": relation(repo, local_head, remote_head),
            "baseline_remote_relation": relation(repo, baseline_sha, remote_head),
            "changed_paths_from_baseline": changed_paths(repo, baseline_sha, remote_head),
            "worktree_mutated": False,
            "rule": "No merge, rebase, checkout, reset, pull or full-clone operation is performed.",
        }
    except (DeltaError, OSError, subprocess.TimeoutExpired) as exc:
        print(f"REPO DELTA FAILED: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"REPOSITORY DELTA: {payload['local_remote_relation']}")
        print(f"- local: {payload['local_head']}")
        print(f"- remote: {payload['remote_head']}")
        print(f"- baseline: {payload['baseline']}")
        print(f"- changed paths: {len(payload['changed_paths_from_baseline'])}")
        for path in payload["changed_paths_from_baseline"]:
            print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
