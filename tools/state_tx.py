#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


class StateTransactionError(Exception):
    pass


def now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fsync_dir(path: Path) -> None:
    if os.name == "nt":
        return
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_json(path: Path, data: dict[str, Any]) -> None:
    payload = (json.dumps(data, indent=2) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
        fsync_dir(path.parent)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def durable_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    fsync_dir(path.parent)


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise StateTransactionError(f"cannot read JSON {path}: {exc}")
    if not isinstance(data, dict):
        raise StateTransactionError(f"expected JSON object at {path}")
    return data


def journal_path(control: Path) -> Path:
    return control / "runtime" / "transactions" / "CURRENT_TRANSACTION.json"


def stage_dir(control: Path, transaction_id: str) -> Path:
    return control / "runtime" / "transactions" / transaction_id


def relative_target(control: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(control.resolve()))
    except ValueError:
        raise StateTransactionError(f"transaction target escapes control root: {path}")


@contextmanager
def state_lock(control: Path, timeout: float = 10.0) -> Iterator[None]:
    path = control / "runtime" / ".campaignctl.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = open(path, "a+b")
    acquired = False
    deadline = time.monotonic() + max(timeout, 0.0)

    try:
        if os.name == "nt":
            import msvcrt

            handle.seek(0, os.SEEK_END)
            if handle.tell() == 0:
                handle.write(b"0")
                handle.flush()
            while True:
                try:
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                    acquired = True
                    break
                except OSError:
                    if time.monotonic() >= deadline:
                        raise StateTransactionError(
                            f"state lock busy: {path}; timeout={timeout:.3f}s"
                        )
                    time.sleep(0.05)
        else:
            import fcntl

            while True:
                try:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    acquired = True
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        raise StateTransactionError(
                            f"state lock busy: {path}; timeout={timeout:.3f}s"
                        )
                    time.sleep(0.05)
        yield
    finally:
        if acquired:
            if os.name == "nt":
                import msvcrt

                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()


def cleanup(control: Path, journal: dict[str, Any]) -> None:
    directory = stage_dir(control, journal["transaction_id"])
    if directory.exists():
        shutil.rmtree(directory)
        fsync_dir(directory.parent)
    current = journal_path(control)
    if current.exists():
        current.unlink()
        fsync_dir(current.parent)


def conflict(control: Path, journal: dict[str, Any], reason: str) -> None:
    journal["status"] = "CONFLICT"
    journal["conflict_reason"] = reason
    journal["updated_at"] = now_iso()
    atomic_json(journal_path(control), journal)


def recover(control: Path) -> str | None:
    path = journal_path(control)
    if not path.exists():
        return None

    journal = load_json(path)
    if journal.get("schema_version") != "transition-journal-0.1":
        raise StateTransactionError(f"unsupported transition journal: {path}")
    if journal.get("status") == "CONFLICT":
        raise StateTransactionError(
            "transaction conflict requires reconciliation: "
            + str(journal.get("conflict_reason"))
        )

    for operation in journal["operations"]:
        target = control / operation["path"]
        stage = control / operation["stage_ref"]
        current_hash = sha256_file(target)

        if current_hash == operation["after_sha256"]:
            operation["applied"] = True
            continue

        if operation["before_exists"]:
            if current_hash != operation["before_sha256"]:
                reason = (
                    f"{operation['path']}: target hash is neither transaction "
                    "before nor after state"
                )
                conflict(control, journal, reason)
                raise StateTransactionError(reason)
        elif target.exists():
            reason = f"{operation['path']}: target unexpectedly exists during recovery"
            conflict(control, journal, reason)
            raise StateTransactionError(reason)

        if sha256_file(stage) != operation["after_sha256"]:
            reason = f"{operation['path']}: staged payload is missing or corrupted"
            conflict(control, journal, reason)
            raise StateTransactionError(reason)

        target.parent.mkdir(parents=True, exist_ok=True)
        os.replace(stage, target)
        fsync_dir(target.parent)
        operation["applied"] = True
        journal["status"] = "COMMITTING"
        journal["updated_at"] = now_iso()
        atomic_json(path, journal)

    for operation in journal["operations"]:
        if sha256_file(control / operation["path"]) != operation["after_sha256"]:
            reason = f"{operation['path']}: after-state verification failed"
            conflict(control, journal, reason)
            raise StateTransactionError(reason)

    journal["status"] = "COMMITTED"
    journal["updated_at"] = now_iso()
    atomic_json(path, journal)
    transaction_id = journal["transaction_id"]
    cleanup(control, journal)
    return transaction_id


def write_state_set(
    control: Path,
    label: str,
    writes: list[tuple[Path, dict[str, Any] | str]],
) -> str:
    if journal_path(control).exists():
        raise StateTransactionError(
            "pending transition exists; recover it before another multi-file mutation"
        )
    if not writes:
        raise StateTransactionError("transaction requires at least one write")

    transaction_id = uuid.uuid4().hex
    directory = stage_dir(control, transaction_id)
    directory.mkdir(parents=True, exist_ok=False)
    fsync_dir(directory.parent)

    operations: list[dict[str, Any]] = []
    seen: set[str] = set()
    try:
        for index, (target, data) in enumerate(writes, start=1):
            relative = relative_target(control, target)
            if relative in seen:
                raise StateTransactionError(f"duplicate transaction target: {relative}")
            seen.add(relative)

            if isinstance(data, dict):
                payload = (json.dumps(data, indent=2) + "\n").encode("utf-8")
            elif isinstance(data, str):
                payload = data.encode("utf-8")
            else:
                raise StateTransactionError(
                    f"unsupported transaction payload type for {relative}: {type(data)!r}"
                )
            staged = directory / f"op_{index:04d}.json"
            durable_bytes(staged, payload)
            before_exists = target.exists()
            operations.append(
                {
                    "path": relative,
                    "before_exists": before_exists,
                    "before_sha256": sha256_file(target) if before_exists else None,
                    "after_sha256": sha256_bytes(payload),
                    "stage_ref": relative_target(control, staged),
                    "applied": False,
                }
            )
    except Exception:
        if directory.exists():
            shutil.rmtree(directory)
            fsync_dir(directory.parent)
        raise

    created = now_iso()
    journal = {
        "schema_version": "transition-journal-0.1",
        "transaction_id": transaction_id,
        "label": label,
        "status": "PREPARED",
        "created_at": created,
        "updated_at": created,
        "operations": operations,
        "conflict_reason": None,
    }
    atomic_json(journal_path(control), journal)
    journal["status"] = "COMMITTING"
    journal["updated_at"] = now_iso()
    atomic_json(journal_path(control), journal)

    crash_raw = os.getenv("AGENTIC_SDLC_TX_CRASH_AFTER_APPLY")
    crash_after = int(crash_raw) if crash_raw else None
    applied = 0

    for operation in journal["operations"]:
        target = control / operation["path"]
        staged = control / operation["stage_ref"]
        current_hash = sha256_file(target)

        if operation["before_exists"]:
            if current_hash != operation["before_sha256"]:
                reason = f"{operation['path']}: target changed after transaction preparation"
                conflict(control, journal, reason)
                raise StateTransactionError(reason)
        elif target.exists():
            reason = f"{operation['path']}: target appeared after transaction preparation"
            conflict(control, journal, reason)
            raise StateTransactionError(reason)

        if sha256_file(staged) != operation["after_sha256"]:
            reason = f"{operation['path']}: staged payload failed integrity check"
            conflict(control, journal, reason)
            raise StateTransactionError(reason)

        target.parent.mkdir(parents=True, exist_ok=True)
        os.replace(staged, target)
        fsync_dir(target.parent)
        operation["applied"] = True
        applied += 1
        journal["updated_at"] = now_iso()
        atomic_json(journal_path(control), journal)

        if crash_after is not None and applied == crash_after:
            os._exit(92)

    journal["status"] = "COMMITTED"
    journal["updated_at"] = now_iso()
    atomic_json(journal_path(control), journal)
    cleanup(control, journal)
    return transaction_id





def write_json_set(
    control: Path,
    label: str,
    writes: list[tuple[Path, dict[str, Any]]],
) -> str:
    return write_state_set(control, label, list(writes))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Recover a pending Agentic SDLC local multi-file state transaction."
    )
    parser.add_argument("--control-root", required=True)
    parser.add_argument("--lock-timeout", type=float, default=10.0)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("recover")
    args = parser.parse_args()

    control = Path(args.control_root).resolve()
    try:
        with state_lock(control, args.lock_timeout):
            transaction_id = recover(control)
    except StateTransactionError as exc:
        print(f"STATE TRANSACTION FAILED: {exc}", file=sys.stderr)
        return 1

    if transaction_id is None:
        print("NO PENDING TRANSACTION")
    else:
        print(f"RECOVERED {transaction_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
