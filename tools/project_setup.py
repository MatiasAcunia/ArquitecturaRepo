#!/usr/bin/env python3
"""Read-only project/mode/technology discovery. NOT an execution authority.

Profiles remain the canonical six starter profiles; modes are orthogonal
choices, not new controller identities or extra branches/processes.
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path
from typing import Any


WORK_SCOPE = ("SOFTWARE", "NON_CODE_AI", "MIXED")
EXECUTION = ("SYNCHRONOUS", "ASYNCHRONOUS", "HYBRID")
COLLABORATION = ("SOLO", "TEAM")
PROJECT_TYPES = (
    "CRUD", "API", "WEB_APP", "MOBILE", "DESKTOP", "CLI",
    "DATA_PIPELINE", "AI_ML", "AUTOMATION", "GAME",
    "MEDIA_PIPELINE", "INFRASTRUCTURE", "RESEARCH", "OTHER",
)
RISK = ("LOW", "MEDIUM", "HIGH")
OS_NAMES = ("WINDOWS", "LINUX", "MACOS", "OTHER")
SCHEMA = "agentic-operating-preferences-v1"


class SetupError(ValueError):
    pass


def detect_os(system: str | None = None) -> str:
    raw = (system if system is not None else platform.system()).lower()
    return {"windows": "WINDOWS", "linux": "LINUX", "darwin": "MACOS"}.get(raw, "OTHER")


def defaults(*, profile_name: str, runtime_installed: bool = False,
             os_name: str | None = None) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA,
        "profile": profile_name,
        "work_scope": "SOFTWARE",
        "execution_mode": "SYNCHRONOUS",
        "collaboration": "SOLO",
        "project_type": "OTHER",
        "risk": "LOW",
        "platform": os_name or detect_os(),
        "runtime_installed": runtime_installed,
        "model_provider_policy": "OPENAI_PREFERRED_NOT_REQUIRED",
        "plugins": [],
        "host_continuity": "NOT_PROVEN",
        "team_authority": "NOT_PROVEN",
        "external_actions": "NOT_AUTHORIZED",
        "status": "CONFIGURATION_ONLY",
    }


def evaluate(prefs: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(prefs, dict) or prefs.get("schema_version") != SCHEMA:
        raise SetupError("INVALID_OPERATING_SCHEMA")
    fields = {
        "work_scope": WORK_SCOPE,
        "execution_mode": EXECUTION,
        "collaboration": COLLABORATION,
        "project_type": PROJECT_TYPES,
        "risk": RISK,
        "platform": OS_NAMES,
    }
    for key, allowed in fields.items():
        if prefs.get(key) not in allowed:
            raise SetupError("INVALID_" + key.upper())
    if type(prefs.get("runtime_installed")) is not bool:
        raise SetupError("RUNTIME_INSTALLATION_FLAG_INVALID")
    if prefs.get("status") != "CONFIGURATION_ONLY":
        raise SetupError("UNAUTHORIZED_OPERATING_ACCEPTANCE")
    if prefs.get("model_provider_policy") not in {
        "OPENAI_PREFERRED_NOT_REQUIRED", "VENDOR_NEUTRAL",
    }:
        raise SetupError("UNKNOWN_MODEL_PROVIDER_POLICY")
    plugins = prefs.get("plugins")
    if not isinstance(plugins, list) or len(plugins) > 16:
        raise SetupError("INVALID_PLUGIN_DISCOVERY_LIST")
    if any(not isinstance(x, dict) or set(x) != {"purpose", "name", "access"} or
           x.get("access") not in {"READ_ONLY", "WRITE_REQUIRES_GATE"} or
           not isinstance(x.get("name"), str) or not x["name"] or len(x["name"]) > 80 or
           not isinstance(x.get("purpose"), str) or not x["purpose"] or len(x["purpose"]) > 200
           for x in plugins):
        raise SetupError("PLUGIN_SCOPE_NOT_BOUNDED")
    blockers: list[str] = []
    gates = ["CANONICAL_CLIENT_BASELINE", "TECHNICAL_BASELINE",
             "EXACT_CAPABILITY_ACCEPTANCE"]
    if prefs["execution_mode"] != "SYNCHRONOUS":
        blockers.extend(("ASYNC_SCHEDULER_NOT_PHYSICALLY_VERIFIED",
                         "HOST_GOAL_REENTRY_NOT_PHYSICALLY_VERIFIED"))
        gates.extend(("DURABLE_CHECKPOINT_AND_RESUME", "QUOTA_AND_CAPACITY_AUTHORITY"))
        if not prefs["runtime_installed"]:
            blockers.append("ASYNC_RUNTIME_NOT_INSTALLED")
    if prefs["collaboration"] == "TEAM":
        blockers.extend(("TEAM_ACTOR_AUTHORITY_NOT_PHYSICALLY_VERIFIED",
                         "SHARED_RESOURCE_CONCURRENCY_NOT_PHYSICALLY_VERIFIED"))
        gates.extend(("OWNER_REGISTRY", "ISOLATED_WRITERS_AND_INTEGRATION",
                      "INDEPENDENT_REVIEW"))
    if prefs["work_scope"] != "SOFTWARE":
        gates.extend(("NON_CODE_PROVENANCE_AND_RIGHTS",
                      "HUMAN_OR_DOMAIN_ACCEPTANCE"))
    if prefs["risk"] == "HIGH":
        gates.extend(("SECURITY_PRIVACY_RIGHTS",
                      "EXTERNAL_ACTION_AUTHORIZATION", "RECOVERY_ROLLBACK"))
    if prefs["platform"] == "OTHER":
        blockers.append("UNSUPPORTED_PLATFORM_NEEDS_ADAPTER")
    if prefs.get("host_continuity") != "NOT_PROVEN" or prefs.get("team_authority") != "NOT_PROVEN":
        blockers.append("UNVERIFIED_SELF_ATTESTATION_NOT_ACCEPTED")
    if prefs.get("external_actions") != "NOT_AUTHORIZED":
        blockers.append("EXTERNAL_ACTION_AUTHORITY_MUST_BE_SEPARATE")
    return {
        "schema_version": "agentic-operating-evaluation-v1",
        "status": "HOLD_UNPROVEN_INTEGRATION" if blockers else "CONFIGURATION_VALID_NOT_PRODUCT_ACCEPTANCE",
        "execution_ready": False,
        "selection": {key: prefs[key] for key in fields},
        "required_gates": sorted(set(gates)),
        "blockers": sorted(set(blockers)),
        "additional_agents_required": False,
    }


def recommend(*, project_type: str, risk: str = "LOW",
              deployment: str = "LOCAL", data_sensitivity: str = "NONE") -> dict[str, Any]:
    if (project_type not in PROJECT_TYPES or risk not in RISK
        or deployment not in {"LOCAL", "LAN", "INTERNET", "CLOUD", "UNDECIDED"}
        or data_sensitivity not in {"NONE", "PERSONAL", "SENSITIVE"}):
        raise SetupError("DISCOVERY_DIMENSION_INVALID")
    options = {
        "CRUD": ["language and backend suitable for client constraints",
                 "relational DB if durable structured data", "CRUD+validation+authorization tests"],
        "API": ["typed API contract", "runtime and framework matching team skills",
                "integration/contract/security tests"],
        "WEB_APP": ["accessible browser frontend", "backend only if required",
                    "integration/perceptual and accessibility tests"],
        "MOBILE": ["native vs cross-platform trade-off", "device matrix", "offline/network testing"],
        "DESKTOP": ["OS packaging and installer", "filesystem permission tests", "update/rollback strategy"],
        "CLI": ["portable CLI/runtime", "input validation and exit codes", "install/uninstall tests"],
        "DATA_PIPELINE": ["schema/lineage owner", "idempotent incremental loads", "recoverable checkpoints"],
        "AI_ML": ["dataset provenance and rights", "evaluation baseline", "model privacy/cost gates"],
        "AUTOMATION": ["provider authorization", "external effect receipts", "safe retry/reconciliation"],
        "GAME": ["engine/platform constraints", "artifact/versioned asset ownership", "perceptual playtests"],
        "MEDIA_PIPELINE": ["source rights", "render/runtime pipeline", "physical sample acceptance"],
        "INFRASTRUCTURE": ["environment as code", "network/security and rollback", "recovery drills"],
        "RESEARCH": ["source/provenance", "hypothesis and falsifiers", "independent replication"],
        "OTHER": ["whole-product discovery", "current interfaces", "minimal testable capability"],
    }
    hard_gates = ["CLIENT_PRODUCT_BASELINE", "I2_STACK_DECISION"]
    if deployment in {"INTERNET", "CLOUD"}:
        hard_gates += ["NETWORK_THREAT_MODEL", "SECRET_HANDLING"]
    if data_sensitivity != "NONE":
        hard_gates += ["DATA_MINIMIZATION", "ACCESS_CONTROL", "BACKUP_RETENTION"]
    if risk == "HIGH":
        hard_gates += ["INDEPENDENT_SECURITY_REVIEW", "RECOVERY_ROLLBACK"]
    return {
        "status": "NON_AUTHORITATIVE_DISCOVERY_SUGGESTIONS",
        "category": project_type,
        "options_to_evaluate": options[project_type],
        "hard_gates": sorted(set(hard_gates)),
        "stack_owner": "I2_TECHNICAL_BASELINE_CURRENT",
        "tools_languages_frameworks": "DISCOVER_AND_JUSTIFY_NOT_PRESELECTED",
        "model_provider": "OpenAI recommended when task capabilities, privacy and cost fit; alternatives legal",
        "plugin_install": "EXPLICIT_PERMISSION_AND_LEAST_PRIVILEGE_ONLY",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--preferences", type=Path, help="Read-only assessment of existing preferences")
    p.add_argument("--project-type", choices=PROJECT_TYPES, default="OTHER")
    p.add_argument("--risk", choices=RISK, default="LOW")
    p.add_argument("--deployment", choices=["LOCAL","LAN","INTERNET","CLOUD","UNDECIDED"], default="LOCAL")
    p.add_argument("--data-sensitivity", choices=["NONE","PERSONAL","SENSITIVE"], default="NONE")
    args = p.parse_args()
    try:
        if args.preferences:
            result = evaluate(json.loads(args.preferences.read_text(encoding="utf-8")))
        else:
            result = recommend(project_type=args.project_type, risk=args.risk,
                               deployment=args.deployment, data_sensitivity=args.data_sensitivity)
    except (ValueError, OSError, TypeError) as exc:
        p.exit(2, "PROJECT SETUP HOLD: " + type(exc).__name__ + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] != "HOLD_UNPROVEN_INTEGRATION" else 2


if __name__ == "__main__":
    raise SystemExit(main())
