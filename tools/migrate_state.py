#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
from collections import deque
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
REGISTRY_PATH = ROOT / "migrations" / "registry.json"


class MigrationError(Exception):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise MigrationError(f"missing file: {path}")
    except Exception as exc:
        raise MigrationError(f"invalid JSON at {path}: {exc}")
    if not isinstance(data, dict):
        raise MigrationError(f"expected JSON object at {path}")
    return data


def fsync_dir(path: Path) -> None:
    if os.name == "nt":
        return
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_json(path: Path, data: dict[str, Any]) -> None:
    payload = json.dumps(data, indent=2) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
        fsync_dir(path.parent)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def file_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        raise MigrationError(f"missing migration target: {path}")


@contextmanager
def migration_lock(control: Path, timeout: float):
    lock_path = control / "runtime" / ".campaignctl.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    handle = open(lock_path, "a+b")
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
                        raise MigrationError(
                            f"campaign/state lock busy: {lock_path}; timeout={timeout:.3f}s"
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
                        raise MigrationError(
                            f"campaign/state lock busy: {lock_path}; timeout={timeout:.3f}s"
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


def pending_transaction(control: Path) -> Path:
    return control / "runtime" / "transactions" / "CURRENT_TRANSACTION.json"


def resolve_internal(control: Path, value: str) -> Path:
    candidate = (control / value).resolve()
    try:
        candidate.relative_to(control.resolve())
    except ValueError:
        raise MigrationError(f"migration target escapes control root: {value}")
    return candidate


def validate_schema(data: dict[str, Any], schema_filename: str) -> None:
    schema_path = SCHEMA_DIR / schema_filename
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    problems = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if problems:
        rendered = []
        for problem in problems:
            location = ".".join(str(p) for p in problem.path)
            suffix = f" at {location}" if location else ""
            rendered.append(f"{problem.message}{suffix}")
        raise MigrationError(
            f"schema validation failed against {schema_filename}: " + "; ".join(rendered)
        )


def unique_refs(*values: str) -> list[str]:
    out: list[str] = []
    for value in values:
        if value and value not in out:
            out.append(value)
    return out


def bootstrap_0_1_to_0_2(data: dict[str, Any]) -> dict[str, Any]:
    out = json.loads(json.dumps(data))
    unresolved = list(out.pop("unresolved_currentness"))
    verified = out["status"] == "READY" and not unresolved
    out["schema_version"] = "starter-bootstrap-0.2"
    out["currentness"] = {
        "verified": verified,
        "verified_at": out["observed_at"] if verified else None,
        "source_refs": unique_refs(out["requirements_ref"], out["product_state_ref"]),
        "unresolved": unresolved,
    }
    return out


def bootstrap_0_2_to_0_1(data: dict[str, Any]) -> dict[str, Any]:
    out = json.loads(json.dumps(data))
    currentness = out.pop("currentness")
    unresolved = list(currentness["unresolved"])
    expected_verified = out["status"] == "READY" and not unresolved
    expected_verified_at = out["observed_at"] if expected_verified else None
    expected_refs = unique_refs(out["requirements_ref"], out["product_state_ref"])

    if currentness["verified"] != expected_verified:
        raise MigrationError(
            "bootstrap v0.2 currentness.verified contains semantics not representable by v0.1"
        )
    if currentness["verified_at"] != expected_verified_at:
        raise MigrationError(
            "bootstrap v0.2 currentness.verified_at contains semantics not representable by v0.1"
        )
    if currentness["source_refs"] != expected_refs:
        raise MigrationError(
            "bootstrap v0.2 currentness.source_refs contains semantics not representable by v0.1"
        )

    out["schema_version"] = "starter-bootstrap-0.1"
    out["unresolved_currentness"] = unresolved
    return out


HANDLERS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "bootstrap_0_1_to_0_2": bootstrap_0_1_to_0_2,
    "bootstrap_0_2_to_0_1": bootstrap_0_2_to_0_1,
}


def load_registry() -> dict[str, Any]:
    registry = load_json(REGISTRY_PATH)
    validate_schema(registry, "migration-registry.schema.json")
    return registry


def edges(registry: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for migration in registry["migrations"]:
        out.append(
            {
                "migration_id": migration["migration_id"],
                "contract": migration["contract"],
                "from_version": migration["from_version"],
                "to_version": migration["to_version"],
                "from_schema": migration["from_schema"],
                "to_schema": migration["to_schema"],
                "handler": migration["handler"],
                "direction": "FORWARD",
            }
        )
        if migration.get("reverse_handler"):
            out.append(
                {
                    "migration_id": migration["migration_id"],
                    "contract": migration["contract"],
                    "from_version": migration["to_version"],
                    "to_version": migration["from_version"],
                    "from_schema": migration["to_schema"],
                    "to_schema": migration["from_schema"],
                    "handler": migration["reverse_handler"],
                    "direction": "REVERSE",
                }
            )
    return out


def contract_for_version(registry: dict[str, Any], version: str) -> str:
    contracts = {
        edge["contract"]
        for edge in edges(registry)
        if version in {edge["from_version"], edge["to_version"]}
    }
    if len(contracts) != 1:
        raise MigrationError(
            f"cannot resolve one migration contract for schema_version {version!r}"
        )
    return next(iter(contracts))


def schema_for_version(registry: dict[str, Any], version: str) -> str:
    schemas: set[str] = set()
    for edge in edges(registry):
        if edge["from_version"] == version:
            schemas.add(edge["from_schema"])
        if edge["to_version"] == version:
            schemas.add(edge["to_schema"])
    if len(schemas) != 1:
        raise MigrationError(f"cannot resolve one schema file for version {version!r}")
    return next(iter(schemas))


def migration_path(
    registry: dict[str, Any],
    current: str,
    target: str,
) -> list[dict[str, Any]]:
    if current == target:
        return []

    graph: dict[str, list[dict[str, Any]]] = {}
    for edge in edges(registry):
        graph.setdefault(edge["from_version"], []).append(edge)

    queue: deque[tuple[str, list[dict[str, Any]]]] = deque([(current, [])])
    visited = {current}
    while queue:
        version, path = queue.popleft()
        for edge in graph.get(version, []):
            next_version = edge["to_version"]
            next_path = path + [edge]
            if next_version == target:
                return next_path
            if next_version not in visited:
                visited.add(next_version)
                queue.append((next_version, next_path))

    raise MigrationError(f"no registered migration path from {current!r} to {target!r}")


def build_plan(
    registry: dict[str, Any],
    data: dict[str, Any],
    target_version: str | None,
) -> dict[str, Any]:
    current = data.get("schema_version")
    if not isinstance(current, str):
        raise MigrationError("migration target has no string schema_version")

    contract = contract_for_version(registry, current)
    target = target_version or registry["latest_versions"].get(contract)
    if not target:
        raise MigrationError(f"registry has no latest version for contract {contract!r}")

    path = migration_path(registry, current, target)
    return {
        "contract": contract,
        "current_version": current,
        "target_version": target,
        "steps": path,
    }


def cmd_plan(args: argparse.Namespace) -> None:
    control = Path(args.control_root).resolve()
    target = resolve_internal(control, args.file)
    data = load_json(target)
    registry = load_registry()
    plan = build_plan(registry, data, args.target_version)
    validate_schema(data, schema_for_version(registry, plan["current_version"]))
    print(json.dumps({"file": args.file, **plan}, indent=2))


def cmd_apply(args: argparse.Namespace) -> None:
    control = Path(args.control_root).resolve()
    target = resolve_internal(control, args.file)

    with migration_lock(control, args.lock_timeout):
        pending = pending_transaction(control)
        if pending.exists():
            raise MigrationError(
                f"pending campaign transaction blocks schema migration: {pending}"
            )

        registry = load_registry()
        data = load_json(target)
        plan = build_plan(registry, data, args.target_version)

        if not plan["steps"]:
            validate_schema(data, schema_for_version(registry, plan["current_version"]))
            print(
                json.dumps(
                    {
                        "file": args.file,
                        "status": "ALREADY_AT_TARGET",
                        **plan,
                    },
                    indent=2,
                )
            )
            return

        applied: list[dict[str, Any]] = []
        for step in plan["steps"]:
            before_bytes = file_bytes(target)
            validate_schema(data, step["from_schema"])

            handler = HANDLERS.get(step["handler"])
            if handler is None:
                raise MigrationError(f"unknown migration handler: {step['handler']}")
            migrated = handler(data)

            if migrated.get("schema_version") != step["to_version"]:
                raise MigrationError(
                    f"handler {step['handler']} produced "
                    f"{migrated.get('schema_version')!r}, expected {step['to_version']!r}"
                )
            validate_schema(migrated, step["to_schema"])

            if file_bytes(target) != before_bytes:
                raise MigrationError(
                    f"migration target changed concurrently before applying {step['migration_id']}"
                )

            atomic_json(target, migrated)
            data = migrated
            applied.append(
                {
                    "migration_id": step["migration_id"],
                    "direction": step["direction"],
                    "from_version": step["from_version"],
                    "to_version": step["to_version"],
                }
            )

        print(
            json.dumps(
                {
                    "file": args.file,
                    "status": "MIGRATED",
                    "contract": plan["contract"],
                    "current_version": plan["current_version"],
                    "target_version": plan["target_version"],
                    "applied": applied,
                },
                indent=2,
            )
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Plan and apply explicit schema migrations for Agentic SDLC state."
    )
    parser.add_argument(
        "--control-root",
        default=".",
        help="Control-layer root containing schemas/ and migrations/.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan")
    plan.add_argument("--file", required=True, help="Path relative to --control-root.")
    plan.add_argument("--target-version")
    plan.set_defaults(func=cmd_plan)

    apply = sub.add_parser("apply")
    apply.add_argument("--file", required=True, help="Path relative to --control-root.")
    apply.add_argument("--target-version")
    apply.add_argument("--lock-timeout", type=float, default=10.0)
    apply.set_defaults(func=cmd_apply)

    args = parser.parse_args()
    try:
        args.func(args)
    except MigrationError as exc:
        print(f"MIGRATION FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
