#!/usr/bin/env python3
"""Physical read-only Git/currentness cases independent of provider/schema packages."""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from reconstruct_context import control_json_snapshot, observe_git_currentness


def git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode:
        raise AssertionError(f"git {args} failed: {completed.stderr}")
    return completed.stdout.strip()


def commit(repo: Path, message: str) -> str:
    git(repo, "add", "-A")
    git(repo, "-c", "user.name=E2 Test", "-c", "user.email=e2@example.test", "commit", "--quiet", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def check(value: bool, label: str) -> None:
    if not value:
        raise AssertionError(label)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ar-v14-git-currentness-") as tmp:
        base = Path(tmp)
        absent = base / "without_git"
        absent.mkdir()
        no_git = observe_git_currentness(absent, "UNRECONSTRUCTED")
        check(no_git["code_ref_relation"] == "NO_GIT_REPOSITORY", "missing Git must remain unverified")
        check(not no_git["local_source_reconciled"], "missing Git incorrectly reconciled")
        state_file = absent / "current.json"
        state_file.write_text('{"revision":1}\n', encoding="utf-8")
        snapshot = control_json_snapshot(absent)
        state_file.write_text('{"revision":2}\n', encoding="utf-8")
        check(snapshot != control_json_snapshot(absent), "mid-reconstruction JSON mutation undetected")

        repo = base / "project"
        repo.mkdir()
        control = repo / ".agentic-sdlc"
        control.mkdir()
        state = control / "state"
        state.mkdir()
        git(repo, "init", "--quiet")
        empty = observe_git_currentness(control, "UNRECONSTRUCTED")
        check(empty["code_ref_relation"] == "NO_COMMIT", "empty repository must be unverified")

        (repo / "app.py").write_text("print('first')\n", encoding="utf-8")
        (state / "current.txt").write_text("initial\n", encoding="utf-8")
        baseline = commit(repo, "source baseline")
        exact = observe_git_currentness(control, baseline)
        check(exact["code_ref_relation"] == "EXACT_HEAD", "exact immutable code ref not recognized")
        check(exact["local_source_reconciled"], "clean exact source not reconciled locally")
        check(exact["upstream"]["relation"] == "NO_TRACKING_REF", "invented remote tracking")
        check(not exact["upstream"]["live_remote_verified"], "invented live remote verification")
        check(not exact["git_proves_actor_authority"], "Git wrongly became actor authority")

        remote = base / "bare_remote.git"
        git(base, "init", "--bare", "--quiet", str(remote))
        git(repo, "remote", "add", "origin", str(remote))
        git(repo, "push", "--quiet", "--set-upstream", "origin", "HEAD")
        tracking = observe_git_currentness(control, baseline)
        check(tracking["upstream"]["relation"] == "EXACT_TRACKING_SNAPSHOT", "tracking snapshot not observed")
        check(not tracking["upstream"]["live_remote_verified"], "tracking snapshot mistaken for remote")

        (state / "current.txt").write_text("changed control state\n", encoding="utf-8")
        commit(repo, "control-only commit")
        control_only = observe_git_currentness(control, baseline)
        check(control_only["code_ref_relation"] == "ANCESTOR_DECLARATIVE_STATE_ONLY", "self-referential control commit misclassified")
        check(control_only["local_source_reconciled"], "control-only descendants must be locally distinguishable")
        check(control_only["upstream"]["relation"] == "LOCAL_AHEAD_TRACKING", "tracking relation not observed")

        executable = control / "tools"
        executable.mkdir()
        (executable / "operation.py").write_text("raise RuntimeError('new tool')\n", encoding="utf-8")
        commit(repo, "control executable changed")
        control_code = observe_git_currentness(control, baseline)
        check(control_code["code_ref_relation"] == "ANCESTOR_WITH_SOURCE_CHANGES", "control executables wrongly classified as state-only")
        check(not control_code["local_source_reconciled"], "control executable falsely reconciled")

        (repo / "app.py").write_text("print('changed source')\n", encoding="utf-8")
        commit(repo, "source changed")
        changed_source = observe_git_currentness(control, baseline)
        check(changed_source["code_ref_relation"] == "ANCESTOR_WITH_SOURCE_CHANGES", "stale source code ref wrongly reconciled")
        check(not changed_source["local_source_reconciled"], "stale code baseline permitted")

        (repo / "app.py").write_text("print('working tree')\n", encoding="utf-8")
        dirty = observe_git_currentness(control, git(repo, "rev-parse", "HEAD"))
        check(dirty["worktree"]["status"] == "CHANGED", "dirty worktree not observed")
        check(not dirty["local_source_reconciled"], "dirty source was reconciled")
        git(repo, "restore", "app.py")

        symbolic = observe_git_currentness(control, "UNRECONSTRUCTED")
        check(symbolic["code_ref_relation"] == "UNBOUND_SYMBOLIC_CODE_REF", "symbolic code ref incorrectly verified")
        missing = observe_git_currentness(control, "f" * 40)
        check(missing["code_ref_relation"] == "CODE_REF_NOT_LOCAL", "unknown source commit incorrectly verified")

        # This remote is a disposable local bare repository. No network request
        # or user repository is touched by this physical regression.
        git(repo, "push", "--quiet", "origin", "HEAD")
        git(repo, "reset", "--hard", baseline)
        behind = observe_git_currentness(control, baseline)
        check(behind["upstream"]["relation"] == "LOCAL_BEHIND_TRACKING", "tracking-behind state hidden")
        (state / "current.txt").write_text("different control branch\n", encoding="utf-8")
        divergent_head = commit(repo, "independent local control change")
        divergence = observe_git_currentness(control, divergent_head)
        check(divergence["upstream"]["relation"] == "DIVERGED_OR_UNRELATED_TRACKING", "tracking divergence hidden")
        check(not divergence["upstream"]["live_remote_verified"], "divergence implies live remote proof")

        git(repo, "checkout", "--quiet", "--detach", "HEAD")
        detached = observe_git_currentness(control, git(repo, "rev-parse", "HEAD"))
        check(detached["branch"] is None, "detached HEAD reported as a branch")
        check(not detached["local_source_reconciled"], "detached HEAD incorrectly authorized")

    print("GIT CURRENTNESS PHYSICAL SELF-TEST PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
