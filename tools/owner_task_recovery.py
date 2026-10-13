#!/usr/bin/env python3
"""Optional five-task mutual-recovery policy. No scheduler or network calls.

An approved scheduler adapter may apply returned ENABLE actions, then MUST
read back. CLIENT-disabled and platform-disabled tasks are never recovered.
"""
from __future__ import annotations

from typing import Any


ROLES = ("Delivery", "Architecture", "Quality", "Integrator", "Master")


class OwnerTaskError(ValueError):
    pass


def recovery_actions(tasks: list[dict[str, Any]], *,
                     subject_role: str, client_disabled: set[str] | None = None) -> dict[str, Any]:
    if subject_role not in ROLES:
        raise OwnerTaskError("UNKNOWN_ROLE")
    if len(tasks) != 5 or {x.get("role") for x in tasks} != set(ROLES):
        raise OwnerTaskError("EXACTLY_FIVE_UNIQUE_ROLES_REQUIRED")
    ids = [x.get("id") for x in tasks]
    if any(not isinstance(x, str) or not x for x in ids) or len(set(ids)) != 5:
        raise OwnerTaskError("EXACTLY_FIVE_UNIQUE_TASK_IDS_REQUIRED")
    explicit = client_disabled or set()
    actions = []
    held = []
    for row in tasks:
        if row["role"] == subject_role or row.get("is_enabled") is True:
            continue
        if row["id"] in explicit or row.get("suspension_source") in ("CLIENT", "PLATFORM", "SECURITY"):
            held.append({"role": row["role"], "reason": "EXPLICIT_OR_PLATFORM_SUSPENSION"})
            continue
        if row.get("is_enabled") is False:
            actions.append({"id": row["id"], "operation": "SET_IS_ENABLED_TRUE_ONLY"})
        else:
            held.append({"role": row["role"], "reason": "UNKNOWN_TASK_STATE"})
    return {"schema_version": "five-task-recovery-plan-v1",
            "scope_roles": list(ROLES), "subject_role": subject_role,
            "actions": actions, "held": held,
            "requires_scheduler_readback": bool(actions),
            "actual_recovery_verified": False}


if __name__ == "__main__":
    raise SystemExit("Policy library only; a verified scheduler adapter is required.")
