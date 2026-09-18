#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ALLOWED = {
    "I1_MASTER_OWNER": {"AUTHORITY_TRANSITION", "RELEASE_BOUNDARY"},
    "I2_PROJECT_WORKSTREAM_PLANNER": {"AUTHORITY_TRANSITION"},
    "I3_ENGINEERING_CAMPAIGN_LEAD": {"COHERENT_CANDIDATE", "RECOVERY_CHECKPOINT"},
    "I4_EXECUTION_TEAM_MEMBER": set(),
}


class GuardError(RuntimeError):
    pass


def git(repo: Path, *args: str, check: bool = True) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if check and completed.returncode:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise GuardError(f"git {' '.join(args)} failed: {detail}")
    return completed.stdout.strip()


def lines(value: str) -> list[str]:
    return [line.replace("\\", "/") for line in value.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail closed unless a canonical commit has explicit role authority and a meaningful boundary class."
    )
    parser.add_argument("--repo", default=".")
    parser.add_argument("--role", required=True, choices=sorted(ALLOWED))
    parser.add_argument(
        "--boundary",
        required=True,
        choices=[
            "COHERENT_CANDIDATE",
            "RECOVERY_CHECKPOINT",
            "AUTHORITY_TRANSITION",
            "RELEASE_BOUNDARY",
        ],
    )
    parser.add_argument(
        "--allow-unstaged-preflight",
        action="store_true",
        help="Permit checking a working-tree delta before staging; canonical commit should be rechecked after staging.",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        repo = Path(args.repo).resolve()
        git(repo, "rev-parse", "--git-dir")
        if args.boundary not in ALLOWED[args.role]:
            raise GuardError(
                f"role {args.role} is not authorized for commit boundary {args.boundary}"
            )

        unmerged = lines(git(repo, "diff", "--name-only", "--diff-filter=U", "--"))
        if unmerged:
            raise GuardError(f"unmerged paths block commit: {unmerged}")

        staged = lines(
            git(
                repo,
                "diff",
                "--cached",
                "--name-only",
                "--diff-filter=ACDMRTUXB",
                "--",
            )
        )
        unstaged = lines(
            git(repo, "diff", "--name-only", "--diff-filter=ACDMRTUXB", "--")
        )
        untracked = lines(git(repo, "ls-files", "--others", "--exclude-standard"))

        if not staged:
            if not args.allow_unstaged_preflight:
                raise GuardError(
                    "no staged causal change; canonical commit boundary is not materialized"
                )
            if not unstaged and not untracked:
                raise GuardError("no repository delta exists")

        payload = {
            "schema_version": "commit-boundary-check-0.1",
            "status": "PASS",
            "role": args.role,
            "boundary": args.boundary,
            "staged_paths": staged,
            "unstaged_paths": unstaged,
            "untracked_paths": untracked,
            "canonical_commit_allowed": bool(staged),
            "rule": (
                "A tactical assignment/helper/test/retry is not itself a commit boundary. "
                "I4 has no canonical commit authority by default."
            ),
        }
    except (GuardError, OSError) as exc:
        print(f"COMMIT GUARD FAILED: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print("COMMIT GUARD PASSED")
        print(f"- role: {payload['role']}")
        print(f"- boundary: {payload['boundary']}")
        print(f"- staged paths: {len(payload['staged_paths'])}")
        if not payload["canonical_commit_allowed"]:
            print("- preflight only: re-run after staging before canonical commit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
