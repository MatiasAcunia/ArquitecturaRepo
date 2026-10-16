#!/usr/bin/env python3
"""Physical managed-output lifecycle, approval, recovery and refusal checks."""
from __future__ import annotations

import datetime as dt
import json
import os
import sqlite3
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from artifact_ledger import digest_json, initial, now, process_alive, stamp

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "artifact_ledger.py"


def run(project: Path, *params: str, code: int = 0) -> dict:
    result = subprocess.run(
        [sys.executable, str(TOOL), "--project", str(project), *params],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == code, (params, result.stdout, result.stderr)
    if not result.stdout.strip():
        return {}
    return json.loads(result.stdout)


def git(project: Path, *params: str) -> None:
    result = subprocess.run(
        ["git", "-C", str(project), *params],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr


def classify(project: Path, name: str, category: str, *, safe: bool,
             ttl: str | None = None) -> dict:
    args = ["classify", "--path", name, "--owner", "I3", "--campaign", "CAMP_A",
            "--category", category]
    if safe:
        args.append("--safe-delete")
    if ttl is not None:
        args += ["--ttl-hours", ttl]
    return run(project, *args)


def review(project: Path, name: str, decision: str = "ACCEPTED") -> dict:
    return run(project, "review", "--path", name, "--owner", "I3",
               "--campaign", "CAMP_A", "--reviewer", "I4_TEST_REVIEWER",
               "--decision", decision, "--evidence-ref", "review/evidence.json")


def capture_file(project: Path, root: str, file: Path, contents: bytes) -> dict:
    if len(contents) > 64 * 1024 and contents == b"x" * len(contents):
        payload = "b'x' * " + str(len(contents))
    else:
        payload = repr(contents)
    code = ("from pathlib import Path; Path(" + repr(str(file)) +
            ").write_bytes(" + payload + ")")
    return run(project, "capture", "--root", root,
               "--category", "DERIVED_REBUILDABLE", "--safe-delete",
               "--ttl-hours", "-1", "--", sys.executable, "-c", code)


def main() -> int:
    physical_gc_receipt: dict[str, int | str | bool] | None = None
    with tempfile.TemporaryDirectory(prefix="artifact-ledger-physical-") as tmp:
        temp = Path(tmp)
        project = temp / "repo"
        project.mkdir()
        git(project, "init", "-b", "main")
        git(project, "config", "user.name", "Example")
        git(project, "config", "user.email", "example.invalid")
        (project / "source.txt").write_text("PRODUCT_SOURCE_PRESERVED")
        (project / "review").mkdir()
        (project / "review" / "evidence.json").write_text(
            '{"review":"bounded synthetic evidence"}\n', encoding="utf-8")
        git(project, "add", "source.txt", "review/evidence.json")
        git(project, "commit", "-m", "fixture authority and review evidence")
        ledger = project / ".agentic-sdlc" / "runtime" / "ARTIFACT_LIFECYCLE_CURRENT.json"
        ledger.parent.mkdir(parents=True)
        (ledger.parent / ".gitignore").write_text(
            "ARTIFACT_LIFECYCLE_CURRENT.json\nARTIFACT_LIFECYCLE_CURRENT.json.lock\n",
            encoding="utf-8",
        )
        git(project, "add", ".agentic-sdlc/runtime/.gitignore")
        git(project, "commit", "-m", "fixture ignores local operational ledger")
        ledger.write_text(json.dumps(initial()), encoding="utf-8")
        lock_path = ledger.with_name(ledger.name + ".lock")
        linked_lock_target = temp / "linked-lock-target.bin"
        linked_lock_target.write_bytes(b"preserve hard-linked content")
        try:
            os.link(linked_lock_target, lock_path)
        except (OSError, NotImplementedError) as exc:
            raise AssertionError("physical fixture volume must support hard-link safety probe") from exc
        hardlink_result = run(project, "observe-git", code=2)
        assert hardlink_result["failure_codes"] == ["LEDGER_LOCK_NOT_PRIVATE_REGULAR_FILE"]
        assert linked_lock_target.read_bytes() == b"preserve hard-linked content"
        assert linked_lock_target.stat().st_nlink == 2
        lock_path.unlink()
        assert run(project, "observe-git")["status"] == "SOURCE_GIT_OBSERVED"
        assert run(project, "observe-git")["status"] == "SOURCE_GIT_UNCHANGED"
        (project / "source.txt").write_text("PRODUCT_SOURCE_MODIFIED")
        (project / "new_code.py").write_text("x=1")
        assert run(project, "observe-git")["changed_count"] >= 2
        observation = json.loads(ledger.read_text())[
            "git_observations"][-1]
        assert {x["path"] for x in observation["changed"]} >= {"source.txt", "new_code.py"}
        (project / "source.txt").write_text("PRODUCT_SOURCE_PRESERVED")
        (project / "new_code.py").unlink()
        run(project, "observe-git")

        root = ".agentic-sdlc-scratch/campaign-A"
        assert run(project, "init-root", "--root", root,
                   "--owner", "I3", "--campaign", "CAMP_A")["status"] == "ROOT_REGISTERED"
        # Marker and nested .gitignore must not turn the registered root into a
        # public source-tree surprise.
        status = subprocess.run(["git", "-C", str(project), "status", "--porcelain",
                                 "--untracked-files=all"], capture_output=True, check=True).stdout
        assert b".agentic-sdlc-scratch/" not in status

        sample_name = root + "/sample.bin"
        sample = project / sample_name
        payload = b"x" * (4 * 1024 * 1024)
        captured = capture_file(project, root, sample, payload)
        assert captured["registered"] == 1
        data = json.loads(ledger.read_text(encoding="utf-8"))
        sample_entry = data["files"][sample_name]
        assert sample_entry["safe_delete"] is True
        assert sample_entry["review_closed"] is False
        assert sample_entry["review_evidence"] is None
        assert run(project, "gc")["ready_count"] == 0
        assert run(project, "cleangarbage")["mode"] == "dry-run"
        assert sample.exists()

        # A real accepted output may consume the sample. This dependency keeps
        # the sample even though it is expired and individually reviewed.
        retained_name = root + "/accepted-decision.json"
        retained = project / retained_name
        retained.write_text('{"accepted":true}\n', encoding="utf-8")
        assert run(project, "reconcile", "--root", root)["registered"] == 1
        classify(project, retained_name, "IMMUTABLE_EVIDENCE", safe=False)
        review(project, retained_name)
        review(project, sample_name)
        edge = run(project, "dependency", "--path", sample_name,
                   "--dependent", retained_name, "--operation", "add",
                   "--owner", "I3", "--campaign", "CAMP_A",
                   "--reviewer", "I4_TEST_REVIEWER",
                   "--evidence-ref", "review/evidence.json")
        assert edge["status"] == "DEPENDENCY_RECORDED"
        plan = run(project, "gc")
        assert next(row for row in plan["rows"] if row["path"] == sample_name)["reason"] == \
            "DEPENDENCIES_OR_ACCEPTED_DEPENDENTS_REMAIN"
        assert run(project, "gc", "--execute", code=2)["status"] == "HOLD"
        assert sample.exists() and retained.exists()
        run(project, "dependency", "--path", sample_name,
            "--dependent", retained_name, "--operation", "remove",
            "--owner", "I3", "--campaign", "CAMP_A",
            "--reviewer", "I4_TEST_REVIEWER",
            "--evidence-ref", "review/evidence.json")

        # Approval is a distinct, immutable receipt bound to exact plan/revision,
        # dependency set, Git state, reviewer evidence and a short lease.
        plan = run(project, "gc")
        assert plan["ready_count"] >= 1, plan["rows"]
        plan_file = temp / "gc-plan.json"
        plan_file.write_text(json.dumps(plan), encoding="utf-8")
        stale_plan_file = temp / "gc-plan-120-days-old.json"
        stale_plan = json.loads(json.dumps(plan))
        old_issued = now() - dt.timedelta(days=120)
        stale_plan["plan_issued_at"] = stamp(old_issued)
        stale_plan["plan_expires_at"] = stamp(old_issued + dt.timedelta(minutes=5))
        stale_plan.pop("plan_sha256")
        stale_plan["plan_sha256"] = digest_json(stale_plan)
        stale_plan_file.write_text(json.dumps(stale_plan), encoding="utf-8")
        os.utime(stale_plan_file, (old_issued.timestamp(), old_issued.timestamp()))
        stale_plan_approval = run(
            project, "approve-gc", "--plan-file", str(stale_plan_file),
            "--path", sample_name, "--reviewer", "I4_TEST_REVIEWER",
            "--evidence-ref", "review/evidence.json", "--approval-out",
            str(temp / "stale-plan-approval.json"), code=2)
        assert stale_plan_approval["failure_codes"] == ["GC_DRY_RUN_RECEIPT_EXPIRED"]
        assert not (temp / "stale-plan-approval.json").exists() and sample.exists()
        alias = temp / "outside-approval-parent"
        try:
            alias.symlink_to(project, target_is_directory=True)
        except (OSError, NotImplementedError):
            alias_supported = False
        else:
            alias_supported = True
            alias_target = alias / "approval-must-not-land-in-project.json"
            redirected = run(
                project, "approve-gc", "--plan-file", str(plan_file),
                "--path", sample_name, "--reviewer", "I4_TEST_REVIEWER",
                "--evidence-ref", "review/evidence.json", "--approval-out",
                str(alias_target), code=2)
            assert redirected["failure_codes"] == ["GC_APPROVAL_MUST_BE_STORED_OUTSIDE_SOURCE_REPO"]
            assert not (project / alias_target.name).exists()
            alias.unlink()
        assert alias_supported, "supported Windows fixture volume must exercise junction/symlink output refusal"
        approval_file = temp / "gc-approval.json"
        approved = run(project, "approve-gc", "--plan-file", str(plan_file),
                       "--path", sample_name, "--reviewer", "I4_TEST_REVIEWER",
                       "--evidence-ref", "review/evidence.json",
                       "--approval-out", str(approval_file))
        assert approved["status"] == "GC_APPROVAL_RECORDED"
        assert approved["human_identity_authentication"] == "NOT_PROVEN_LOCAL_ATTESTATION_ONLY"
        assert json.loads(lock_path.read_text(encoding="utf-8"))["status"] == "idle"

        # Expired receipt lease is rejected even when the receipt hash is
        # recomputed; the checksum is tamper evidence, not reviewer signing.
        expired_receipt = json.loads(approval_file.read_text(encoding="utf-8"))
        expired_receipt["lease_expires_at"] = stamp(now() - dt.timedelta(seconds=1))
        expired_receipt.pop("approval_sha256")
        expired_receipt["approval_sha256"] = digest_json(expired_receipt)
        approval_file.write_text(json.dumps(expired_receipt), encoding="utf-8")
        expired = run(project, "gc", "--execute", "--approval", str(approval_file), code=2)
        assert expired["failure_codes"] == ["GC_APPROVAL_LEASE_EXPIRED"] and sample.exists()

        # A dependency change after a fresh approval invalidates its ledger
        # revision before any unlink.
        plan = run(project, "gc")
        plan_file = temp / "gc-plan-dependency.json"
        plan_file.write_text(json.dumps(plan), encoding="utf-8")
        approval_file = temp / "gc-approval-dependency.json"
        run(project, "approve-gc", "--plan-file", str(plan_file),
            "--path", sample_name, "--reviewer", "I4_TEST_REVIEWER",
            "--evidence-ref", "review/evidence.json",
            "--approval-out", str(approval_file))
        run(project, "dependency", "--path", sample_name,
            "--dependent", retained_name, "--operation", "add",
            "--owner", "I3", "--campaign", "CAMP_A",
            "--reviewer", "I4_TEST_REVIEWER",
            "--evidence-ref", "review/evidence.json")
        stale_revision = run(project, "gc", "--execute", "--approval", str(approval_file), code=2)
        assert stale_revision["failure_codes"] == ["GC_APPROVAL_LEDGER_REVISION_STALE"]
        assert sample.exists()
        run(project, "dependency", "--path", sample_name,
            "--dependent", retained_name, "--operation", "remove",
            "--owner", "I3", "--campaign", "CAMP_A",
            "--reviewer", "I4_TEST_REVIEWER",
            "--evidence-ref", "review/evidence.json")

        # A source-tree change after review invalidates the exact Git binding.
        plan = run(project, "gc")
        plan_file = temp / "gc-plan-git.json"
        plan_file.write_text(json.dumps(plan), encoding="utf-8")
        approval_file = temp / "gc-approval-git.json"
        run(project, "approve-gc", "--plan-file", str(plan_file),
            "--path", sample_name, "--reviewer", "I4_TEST_REVIEWER",
            "--evidence-ref", "review/evidence.json",
            "--approval-out", str(approval_file))
        (project / "new_code.py").write_text("x=2")
        stale = run(project, "gc", "--execute", "--approval", str(approval_file), code=2)
        assert stale["failure_codes"] == ["GC_APPROVAL_GIT_CURRENTNESS_STALE"] and sample.exists()
        (project / "new_code.py").unlink()

        plan = run(project, "gc")
        plan_file = temp / "gc-plan-final.json"
        plan_file.write_text(json.dumps(plan), encoding="utf-8")
        approval_file = temp / "gc-approval-final.json"
        approved = run(project, "approve-gc", "--plan-file", str(plan_file),
                       "--path", sample_name, "--reviewer", "I4_TEST_REVIEWER",
                       "--evidence-ref", "review/evidence.json",
                       "--approval-out", str(approval_file))
        before = run(project, "report")["revision"]
        # Approval must survive a second-boundary rollover; issue/expiry
        # timestamps are freshness metadata, not the reviewed decision itself.
        time.sleep(1.1)
        removal = run(project, "gc", "--execute", "--approval", str(approval_file))
        assert removal["deleted_count"] == 1
        assert removal["reclaimed_bytes"] == len(payload)
        assert removal["file_absent_readback"] is True and not sample.exists()
        assert removal["disk_free_delta_bytes"] == (
            removal["disk_free_after_bytes"] - removal["disk_free_before_bytes"])
        assert removal["disk_free_before_bytes"] > 0
        physical_gc_receipt = {
            "filesystem_root": str(Path(tempfile.gettempdir()).anchor),
            "deleted_count": removal["deleted_count"],
            "logical_reclaimed_bytes": removal["reclaimed_bytes"],
            "disk_free_before_bytes": removal["disk_free_before_bytes"],
            "disk_free_after_bytes": removal["disk_free_after_bytes"],
            "disk_free_delta_bytes": removal["disk_free_delta_bytes"],
            "file_absent_readback": removal["file_absent_readback"],
        }
        assert run(project, "report")["revision"] > before
        assert run(project, "gc")["ready_count"] == 0

        # A producer failure is quarantined; an unknown/unwrapped file blocks
        # the whole root until reconciliation, which never grants deletion.
        failed_sample = project / root / "failed.txt"
        failing = "from pathlib import Path;Path(" + repr(str(failed_sample)) + \
            ").write_text('error');raise SystemExit(7)"
        response = run(project, "capture", "--root", root,
                       "--category", "DERIVED_REBUILDABLE", "--safe-delete",
                       "--ttl-hours", "-1", "--", sys.executable, "-c", failing, code=7)
        assert response["status"] == "FAILED_OUTPUTS_QUARANTINED"
        assert failed_sample.exists()
        assert json.loads(ledger.read_text())["files"][root + "/failed.txt"]["category"] == \
            "QUARANTINE_UNRESOLVED"
        orphan = project / root / "unregistered.bin"
        orphan.write_bytes(b"UNREGISTERED")
        assert root in run(project, "gc")["unregistered_roots"]
        assert run(project, "reconcile", "--root", root)["registered"] == 1
        assert json.loads(ledger.read_text())["files"][root + "/unregistered.bin"]["safe_delete"] is False

        # Changed identity, protected DB/WAL-like suffix, tracked source,
        # malformed evidence, symlink and corrupt ledger all fail closed.
        mutable_name = root + "/changed.txt"
        mutable = project / mutable_name
        mutable.write_bytes(b"old")
        run(project, "reconcile", "--root", root)
        classify(project, mutable_name, "DERIVED_REBUILDABLE", safe=True, ttl="-1")
        review(project, mutable_name)
        mutable.write_bytes(b"NEW FILE CONTENT")
        assert run(project, "gc")["ready_count"] == 0 and mutable.exists()
        run(project, "reconcile", "--root", root)

        db_name = root + "/canonical.sqlite"
        db = project / db_name
        db.write_bytes(b"synthetic_fixture")
        run(project, "reconcile", "--root", root)
        classify(project, db_name, "TEMP_TRANSACTION", safe=True, ttl="-1")
        review(project, db_name)
        assert next(row for row in run(project, "gc")["rows"] if row["path"] == db_name)["reason"] == \
            "DATABASE_SQL_OR_SECRET_FILE"
        assert run(project, "gc", "--execute", code=2)["status"] == "HOLD"
        assert db.exists()

        # SQLite detection uses actual file content, and protects sidecars on
        # Windows regardless of suffix case, even when names evade extension rules.
        actual_db_name = root + "/snapshot.bin"
        actual_db = project / actual_db_name
        connection = sqlite3.connect(actual_db)
        try:
            connection.execute("CREATE TABLE physical_evidence(value TEXT)")
            connection.execute("INSERT INTO physical_evidence VALUES ('valid SQLite file')")
            connection.commit()
        finally:
            connection.close()
        run(project, "reconcile", "--root", root)
        classify(project, actual_db_name, "TEMP_TRANSACTION", safe=True, ttl="-1")
        review(project, actual_db_name)
        actual_row = next(row for row in run(project, "gc")["rows"]
                          if row["path"] == actual_db_name)
        assert actual_row["reason"] == "DATABASE_SQL_OR_SECRET_FILE", actual_row
        assert actual_db.read_bytes().startswith(b"SQLite format 3\x00")
        for suffix in ("-WAL", "-SHM", "-JOURNAL"):
            sidecar_name = root + "/case-check" + suffix
            sidecar = project / sidecar_name
            sidecar.write_bytes(b"sidecar fixture")
            run(project, "reconcile", "--root", root)
            classify(project, sidecar_name, "TEMP_TRANSACTION", safe=True, ttl="-1")
            review(project, sidecar_name)
            sidecar_row = next(row for row in run(project, "gc")["rows"]
                               if row["path"] == sidecar_name)
            assert sidecar_row["reason"] == "DATABASE_SQL_OR_SECRET_FILE", sidecar_row

        tracked_name = root + "/tracked.bin"
        tracked = project / tracked_name
        tracked.write_bytes(b"versioned")
        run(project, "reconcile", "--root", root)
        classify(project, tracked_name, "DERIVED_REBUILDABLE", safe=True, ttl="-1")
        review(project, tracked_name)
        git(project, "add", "-f", tracked_name)
        assert next(row for row in run(project, "gc")["rows"] if row["path"] == tracked_name)["reason"] == \
            "GIT_TRACKED_FILE"
        assert tracked.exists()

        localized_name = root + "/música y voz 01.mp4"
        localized = project / localized_name
        localized.write_bytes(b"SAFE_REBUILDABLE_SAMPLE")
        run(project, "reconcile", "--root", root)
        classify(project, localized_name, "DERIVED_REBUILDABLE", safe=True, ttl="-1")
        review(project, localized_name)
        assert any(row["path"] == localized_name and row["decision"] == "DELETE_READY"
                   for row in run(project, "gc")["rows"])

        outside = project / "secret_outside"
        outside.write_bytes(b"PRIVATE")
        hardlink = project / root / "hardlink-to-secret"
        try:
            os.link(outside, hardlink)
        except (OSError, NotImplementedError):
            hardlink_supported = False
        else:
            hardlink_supported = True
            blocked_hardlink = run(project, "gc", code=2)
            assert blocked_hardlink["failure_codes"] == ["NONREGULAR_OR_HARDLINKED_OUTPUT"]
            assert outside.read_bytes() == b"PRIVATE"
            hardlink.unlink()
        assert hardlink_supported, "supported Windows fixture volume must exercise hardlink refusal"
        link = project / root / "symlinked"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError):
            pass
        else:
            assert run(project, "gc", code=2)["status"] == "HOLD"
            assert outside.read_bytes() == b"PRIVATE"
            link.unlink()

        # A live competing process holds the OS lock; it is never stolen by PID
        # text or by replacing the lock file.
        live_file = project / root / "live-producer.txt"
        done_file = temp / "producer-done.txt"
        child_code = ("from pathlib import Path;import time;Path(" + repr(str(live_file)) +
                      ").write_text('in-progress');time.sleep(5);Path(" +
                      repr(str(done_file)) + ").write_text('done')")
        process = subprocess.Popen(
            [sys.executable, str(TOOL), "--project", str(project), "capture", "--root", root,
             "--category", "DERIVED_REBUILDABLE", "--safe-delete", "--ttl-hours", "-1",
             "--", sys.executable, "-c", child_code],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        deadline = time.monotonic() + 5
        while not live_file.exists() and time.monotonic() < deadline:
            time.sleep(0.02)
        assert live_file.exists()
        competitor = run(project, "reconcile", "--root", root, code=2)
        assert competitor["status"] == "HOLD"
        process.wait(timeout=15)
        stdout, stderr = process.communicate(timeout=2)
        assert process.returncode == 0, (stdout, stderr)
        assert done_file.exists()

        # Kill the ledger-owning capture while its producer is active. The
        # kernel lock releases with the owner; GC remains blocked until explicit
        # owner-bound recovery reconciles the orphan into quarantine.
        crash_file = project / root / "interrupted-output.tmp"
        child_done = temp / "interrupted-producer-done.txt"
        crashed_owner_pid_file = temp / "crashed-ledger-owner-pid.txt"
        crash_code = ("from pathlib import Path;import time;Path(" + repr(str(crash_file)) +
                      ").write_text('partial');time.sleep(5);Path(" +
                      repr(str(child_done)) + ").write_text('producer-finished')")
        crashed_args = [
            "artifact_ledger.py", "--project", str(project), "capture", "--root", root,
            "--category", "DERIVED_REBUILDABLE", "--safe-delete", "--ttl-hours", "-1",
            "--", sys.executable, "-c", crash_code,
        ]
        crashed_command = (
            "import os,sys\nfrom pathlib import Path\n"
            "sys.path.insert(0," + repr(str(TOOL.parent)) + ")\n"
            "Path(" + repr(str(crashed_owner_pid_file)) + ").write_text(str(os.getpid()))\n"
            "import artifact_ledger as m\n"
            "sys.argv=" + repr(crashed_args) + "\nraise SystemExit(m.main())\n"
        )
        crashed = subprocess.Popen(
            [sys.executable, "-c", crashed_command],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        deadline = time.monotonic() + 5
        while not crash_file.exists() and time.monotonic() < deadline:
            time.sleep(0.02)
        assert crash_file.exists()
        assert crashed.poll() is None, "ledger capture completed before interruption"
        crashed.terminate()
        crashed.wait(timeout=5)
        deadline = time.monotonic() + 5
        while not child_done.exists() and time.monotonic() < deadline:
            time.sleep(0.02)
        assert child_done.exists()
        crashed_owner_pid = int(crashed_owner_pid_file.read_text(encoding="utf-8"))
        lock = ledger.with_name(ledger.name + ".lock")
        lock_data = json.loads(lock.read_text(encoding="utf-8"))
        assert (lock_data["status"] == "active"
                and lock_data["operation"] == "capture"
                and lock_data["root"] == root
                and lock_data["pid"] == crashed_owner_pid
                and process_alive(lock_data["pid"]) is False), (
            f"interrupted capture lock is not a dead, exact-scope owner record: "
            f"terminated_process_id={crashed.pid}, owner_pid={crashed_owner_pid}, "
            f"lock={lock_data!r}, "
            f"owner_alive={process_alive(lock_data.get('pid'))}"
        )
        refused_owner = run(project, "recover-lock", "--root", root, "--owner", "I3",
                            "--campaign", "WRONG_CAMPAIGN", "--operator-evidence-ref",
                            "review/evidence.json", code=2)
        assert refused_owner["failure_codes"] == ["RECOVERY_OWNER_OR_CAMPAIGN_MISMATCH"]
        assert json.loads(lock.read_text(encoding="utf-8")) == lock_data
        assert all(row["reason"] == "INTERRUPTED_OPERATION_RECOVERY_REQUIRED"
                   for row in run(project, "gc")["rows"])
        refused_recent = run(project, "recover-lock", "--root", root, "--owner", "I3",
                             "--campaign", "CAMP_A", "--operator-evidence-ref",
                             "review/evidence.json", code=2)
        assert refused_recent["failure_codes"] == ["INTERRUPTED_LOCK_TOO_RECENT"]
        assert json.loads(lock.read_text(encoding="utf-8")) == lock_data
        assert all(row["reason"] == "INTERRUPTED_OPERATION_RECOVERY_REQUIRED"
                   for row in run(project, "gc")["rows"])
        old = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=10)
        lock_data["started_at"] = old.isoformat().replace("+00:00", "Z")
        lock.write_text(json.dumps(lock_data), encoding="utf-8")
        interrupted_plan = run(project, "gc")
        assert interrupted_plan["ready_count"] == 0
        assert root in interrupted_plan["unregistered_roots"]
        assert all(row["reason"] == "INTERRUPTED_OPERATION_RECOVERY_REQUIRED"
                   for row in interrupted_plan["rows"])
        recovery = run(project, "recover-lock", "--root", root, "--owner", "I3",
                       "--campaign", "CAMP_A", "--operator-evidence-ref",
                       "review/evidence.json")
        assert recovery["status"] == "RECOVERED_INTERRUPTION_OUTPUTS_QUARANTINED"
        assert recovery["registered"] >= 1
        crash_entry = json.loads(ledger.read_text())["files"][root + "/interrupted-output.tmp"]
        assert crash_entry["category"] == "QUARANTINE_UNRESOLVED"
        assert crash_entry["safe_delete"] is False
        assert crash_file.exists()

        # Interrupt a second recovery at reconciliation entry. The persisted
        # recover-lock record must itself be recoverable, and replay is idempotent.
        recovery_started = temp / "recover-lock-reconcile-entered.txt"
        recovery_owner_pid_file = temp / "recover-lock-owner-pid.txt"
        stale_capture = {
            "schema_version": "artifact-ledger-lock-v1", "status": "active",
            "pid": lock_data["pid"], "host": socket.gethostname(),
            "started_at": (dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=10))
                .isoformat().replace("+00:00", "Z"),
            "operation": "capture", "root": root,
        }
        lock.write_text(json.dumps(stale_capture), encoding="utf-8")
        recovery_script = (
            "import os,sys,time\nfrom pathlib import Path\n"
            "sys.path.insert(0," + repr(str(TOOL.parent)) + ")\n"
            "import artifact_ledger as m\noriginal=m.reconcile\n"
            "def pause(*args,**kwargs):\n"
            "    Path(" + repr(str(recovery_started)) + ").write_text('entered')\n"
            "    time.sleep(30)\n"
            "    return original(*args,**kwargs)\n"
            "m.reconcile=pause\n"
            "Path(" + repr(str(recovery_owner_pid_file)) + ").write_text(str(os.getpid()))\n"
            "sys.argv=['artifact_ledger.py','--project'," + repr(str(project)) +
            ",'recover-lock','--root'," + repr(root) + ",'--owner','I3','--campaign','CAMP_A',"
            "'--operator-evidence-ref','review/evidence.json']\nraise SystemExit(m.main())\n"
        )
        recovery_process = subprocess.Popen(
            [sys.executable, "-c", recovery_script],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        deadline = time.monotonic() + 10
        while not recovery_started.exists() and recovery_process.poll() is None and time.monotonic() < deadline:
            time.sleep(0.01)
        assert recovery_started.exists(), "recovery did not reach reconciliation"
        recovery_process.terminate()
        recovery_process.wait(timeout=5)
        recovery_owner_pid = int(recovery_owner_pid_file.read_text(encoding="utf-8"))
        interrupted_recovery_lock = json.loads(lock.read_text(encoding="utf-8"))
        assert interrupted_recovery_lock["status"] == "active"
        assert interrupted_recovery_lock["operation"] == "recover-lock"
        assert (interrupted_recovery_lock["root"] == root
                and interrupted_recovery_lock["pid"] == recovery_owner_pid
                and process_alive(interrupted_recovery_lock["pid"]) is False), (
            f"interrupted recovery lock is not a dead, exact-scope owner record: "
            f"terminated_process_id={recovery_process.pid}, owner_pid={recovery_owner_pid}, "
            f"lock={interrupted_recovery_lock!r}"
        )
        refused_recovery_retry = run(
            project, "recover-lock", "--root", root, "--owner", "I3",
            "--campaign", "CAMP_A", "--operator-evidence-ref", "review/evidence.json", code=2)
        assert refused_recovery_retry["failure_codes"] == ["INTERRUPTED_LOCK_TOO_RECENT"]
        assert json.loads(lock.read_text(encoding="utf-8")) == interrupted_recovery_lock
        interrupted_recovery_lock["started_at"] = (
            dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=10)
        ).isoformat().replace("+00:00", "Z")
        lock.write_text(json.dumps(interrupted_recovery_lock), encoding="utf-8")
        replay = run(project, "recover-lock", "--root", root, "--owner", "I3",
                     "--campaign", "CAMP_A", "--operator-evidence-ref",
                     "review/evidence.json")
        assert replay["status"] == "RECOVERED_INTERRUPTION_OUTPUTS_QUARANTINED", replay
        assert replay["registered"] == 0, replay
        replay_entry = json.loads(ledger.read_text())["files"][root + "/interrupted-output.tmp"]
        assert replay_entry == crash_entry
        assert crash_file.exists()

        before = ledger.read_bytes()
        lock.unlink()
        lock.write_text("unverifiable legacy lock")
        legacy = run(project, "reconcile", "--root", root, code=2)
        assert legacy["failure_codes"] == ["LEDGER_LOCK_METADATA_UNVERIFIABLE"]
        assert ledger.read_bytes() == before
        lock.unlink()

        marker = project / root / ".agentic-artifact-root.json"
        original_marker = marker.read_bytes()
        marker.write_bytes(b"{}")
        assert run(project, "gc", code=2)["status"] == "HOLD"
        marker.write_bytes(original_marker)
        saved = ledger.read_bytes()
        forged = json.loads(saved)
        forged["files"][root + "/tracked.bin"]["owner"] = "FOREIGN"
        ledger.write_text(json.dumps(forged), encoding="utf-8")
        assert run(project, "gc", code=2)["status"] == "HOLD"
        ledger.write_bytes(saved)
        ledger.write_bytes(b"{not valid JSON")
        assert run(project, "gc", code=2)["status"] == "HOLD"
        ledger.write_bytes(saved)
        assert run(project, "init-root", "--root", root,
                   "--owner", "I4", "--campaign", "FOREIGN", code=2)["status"] == "HOLD"
        assert (project / "source.txt").read_text() == "PRODUCT_SOURCE_PRESERVED"

    print("ARTIFACT LEDGER PASS: persistent lifecycle, reviewed single-file GC, real disk/readback, lock conflict and interruption quarantine")
    assert physical_gc_receipt is not None
    print("ARTIFACT LEDGER DISK RECEIPT " + json.dumps(physical_gc_receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
