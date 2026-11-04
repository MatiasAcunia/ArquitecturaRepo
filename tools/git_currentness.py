#!/usr/bin/env python3
"""Read-only local Git evidence for canonical fresh-context reconstruction.

No fetch/pull/mutation, native authority, or claim of live remote freshness.
This module has no third-party dependencies and is installed with the core.
"""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Any


def observe_git_currentness(control_root: Path, declared_code_ref: str) -> dict[str, Any]:
    """Compare a declared code baseline with physical local Git state.

    Product State can be committed inside Git: the code SHA declared within
    a commit cannot point to that same commit. An ancestor followed only by
    declarative control-state changes is therefore distinct from changed code.
    Neither case proves live remote freshness or actor execution authority.
    """

    def git(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(control_root), *args],
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
            timeout=12,
            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
        )

    observation: dict[str, Any] = {
        "schema_version": "git-currentness-observation-0.1",
        "mode": "LOCAL_READ_ONLY_NO_FETCH",
        "repository_root": None,
        "head": None,
        "branch": None,
        "declared_code_ref": declared_code_ref,
        "code_ref_relation": "UNOBSERVED",
        "worktree": {"status": "UNKNOWN", "changed_entries": None},
        "upstream": {
            "tracking_ref": None,
            "tracking_head": None,
            "relation": "UNKNOWN",
            "live_remote_verified": False,
        },
        "local_source_reconciled": False,
        "reconciliation_required": [],
        "git_proves_actor_authority": False,
    }
    required: list[str] = observation["reconciliation_required"]
    try:
        top = git("rev-parse", "--show-toplevel")
        if top.returncode:
            observation["code_ref_relation"] = "NO_GIT_REPOSITORY"
            required.append("Attach or initialize the intended Git repository and observe its HEAD.")
            return observation

        repo = Path(top.stdout.strip()).resolve()
        observation["repository_root"] = str(repo)
        head = git("rev-parse", "--verify", "HEAD^{commit}")
        if head.returncode:
            observation["code_ref_relation"] = "NO_COMMIT"
            required.append("Create or identify a real committed source baseline.")
            return observation
        observation["head"] = head.stdout.strip()

        branch = git("symbolic-ref", "--quiet", "--short", "HEAD")
        if branch.returncode == 0:
            observation["branch"] = branch.stdout.strip()
        else:
            required.append("Detached HEAD: identify the intended integration branch before writes.")

        dirty = git("status", "--porcelain=v1", "--untracked-files=normal")
        if dirty.returncode:
            required.append("Git worktree status could not be verified.")
        else:
            changed = len(dirty.stdout.splitlines())
            observation["worktree"] = {
                "status": "CHANGED" if changed else "CLEAN",
                "changed_entries": changed,
            }
            if changed:
                required.append("Review uncommitted and untracked files before source-sensitive writes.")

        upstream = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
        if upstream.returncode:
            observation["upstream"]["relation"] = "NO_TRACKING_REF"
            required.append("No upstream tracking ref; live remote source has not been compared.")
        else:
            observation["upstream"]["tracking_ref"] = upstream.stdout.strip()
            tracked = git("rev-parse", "--verify", "@{upstream}^{commit}")
            if tracked.returncode:
                observation["upstream"]["relation"] = "TRACKING_REF_UNRESOLVED"
                required.append("Resolve the configured upstream tracking commit.")
            else:
                tracking_sha = tracked.stdout.strip()
                observation["upstream"]["tracking_head"] = tracking_sha
                if tracking_sha == observation["head"]:
                    relation = "EXACT_TRACKING_SNAPSHOT"
                else:
                    local_a = git("merge-base", "--is-ancestor", observation["head"], tracking_sha)
                    remote_a = git("merge-base", "--is-ancestor", tracking_sha, observation["head"])
                    if local_a.returncode == 0:
                        relation = "LOCAL_BEHIND_TRACKING"
                    elif remote_a.returncode == 0:
                        relation = "LOCAL_AHEAD_TRACKING"
                    else:
                        relation = "DIVERGED_OR_UNRELATED_TRACKING"
                observation["upstream"]["relation"] = relation
                if relation != "EXACT_TRACKING_SNAPSHOT":
                    required.append("Reconcile local HEAD with the upstream tracking commit.")

        if not re.fullmatch(r"[0-9a-fA-F]{40}", declared_code_ref or ""):
            observation["code_ref_relation"] = "UNBOUND_SYMBOLIC_CODE_REF"
            required.append("Bind the declared code baseline to an immutable full commit SHA.")
        else:
            declared = git("cat-file", "-e", f"{declared_code_ref}^{{commit}}")
            if declared.returncode:
                observation["code_ref_relation"] = "CODE_REF_NOT_LOCAL"
                required.append("Obtain and verify the declared code commit locally.")
            elif declared_code_ref.lower() == observation["head"].lower():
                observation["code_ref_relation"] = "EXACT_HEAD"
            else:
                ancestor = git("merge-base", "--is-ancestor", declared_code_ref, observation["head"])
                if ancestor.returncode:
                    observation["code_ref_relation"] = "CODE_REF_NOT_ANCESTOR"
                    required.append("Reconcile the declared code commit with the current HEAD lineage.")
                else:
                    # A code file moved into state/ must remain visible as a
                    # change outside that directory, even with rename detection.
                    differences = git(
                        "diff", "--no-renames", "--name-only", declared_code_ref, observation["head"], "--"
                    )
                    try:
                        control_relative = control_root.resolve().relative_to(repo)
                    except ValueError:
                        control_relative = Path(".")
                    prefix = control_relative.as_posix().rstrip("/") + "/state/"
                    if (
                        differences.returncode == 0
                        and not prefix.startswith("./")
                        and all(
                            path.startswith(prefix)
                            and Path(path).suffix.lower() in {".json", ".md", ".txt"}
                            for path in differences.stdout.splitlines()
                        )
                    ):
                        observation["code_ref_relation"] = "ANCESTOR_DECLARATIVE_STATE_ONLY"
                    else:
                        observation["code_ref_relation"] = "ANCESTOR_WITH_SOURCE_CHANGES"
                        required.append("Review source changes after the declared code baseline.")

        observation["local_source_reconciled"] = (
            observation["code_ref_relation"] in {"EXACT_HEAD", "ANCESTOR_DECLARATIVE_STATE_ONLY"}
            and observation["worktree"]["status"] == "CLEAN"
            and observation["branch"] is not None
        )
        required.append(
            "Before remote-sensitive operations, verify the live remote ref explicitly; "
            "a tracking ref is only a local snapshot."
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        observation["code_ref_relation"] = "GIT_OBSERVATION_FAILED"
        required.append(
            f"Local Git observation failed ({type(exc).__name__}); investigate without assuming currentness."
        )
    return observation
