#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD = ROOT / "tools" / "scaffold_project.py"


def run(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="agentic-baseline-") as tmp:
        project = Path(tmp) / "project"
        result = run(
            str(SCAFFOLD),
            "--target", str(project),
            "--profile", "STATEFUL",
            "--product-id", "BASELINE_TEST",
            "--objective", "Synthetic baseline-readiness product.",
            "--with-runtime",
        )
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)

        control = project / ".agentic-sdlc"
        guard = control / "tools" / "baseline_guard.py"
        status_tool = control / "tools" / "project_status.py"
        campaignctl = control / "tools" / "campaignctl.py"

        blocked = run(str(guard), "--control-root", str(control), "--json")
        if blocked.returncode == 0 or json.loads(blocked.stdout)["ready"] is not False:
            raise AssertionError("fresh scaffold baseline unexpectedly READY")

        init_blocked = run(
            str(campaignctl),
            "--control-root", str(control),
            "init",
            "--charter", "campaigns/MISSING.json",
        )
        combined = init_blocked.stdout + init_blocked.stderr
        if init_blocked.returncode == 0 or "PROJECT_BASELINE_NOT_READY" not in combined:
            raise AssertionError(
                "campaign runtime did not block on missing project baseline\n" + combined
            )

        req_path = control / "state" / "CLIENT_REQUIREMENTS_CURRENT.md"
        req = req_path.read_text(encoding="utf-8")
        req = req.replace("Baseline status: DRAFT", "Baseline status: CLIENT_CONFIRMED")
        req = req.replace("CLIENT confirmation: PENDING", "CLIENT confirmation: CONFIRMED")
        req = req.replace("Confirmed at: PENDING", "Confirmed at: 2035-01-02T12:00:00Z")
        req_path.write_text(req, encoding="utf-8")

        tech_path = control / "state" / "TECHNICAL_BASELINE_CURRENT.json"
        tech = json.loads(tech_path.read_text(encoding="utf-8"))
        tech.update(
            {
                "baseline_version": "1",
                "status": "CURRENT",
                "updated_at": "2035-01-02T12:00:00Z",
            }
        )
        tech["environment"] = {
            "development_os": "Synthetic desktop OS",
            "deployment_target": "Single local workstation",
            "network_mode": "LOCALHOST_ONLY",
            "machine_profile": {
                "assessment_status": "OBSERVED",
                "os_summary": "Synthetic desktop OS",
                "cpu_summary": "General-purpose multi-core CPU",
                "ram_gb": 16,
                "storage_free_gb": 100,
                "gpu_summary": "NOT_MATERIAL",
                "notes": "Sufficient for local CRUD development.",
            },
        }
        tech["stack"] = {
            "language": "Python",
            "runtime": "CPython",
            "backend": "Server-rendered web application",
            "frontend": "HTML forms and minimal JavaScript",
            "database": "SQLite",
            "persistence_migrations": "Explicit schema migrations",
            "package_manager": "pip",
            "test_stack": "unittest",
            "deployment": "Local workstation",
            "rationale": "Minimum sufficient stack for a small stateful CRUD.",
        }
        tech["security"] = {
            "authentication_model": "NONE_SINGLE_USER_LOCAL",
            "authorization_model": "Single local operator",
            "secrets_management": "No secrets in source control",
            "data_classification": "Synthetic non-sensitive data",
            "backup_recovery": "Copy/restore documented local DB backup",
            "exposure_controls": ["Bind application to localhost only"],
        }
        tech["networking"] = {
            "listen_scope": "127.0.0.1 only",
            "ports_services": ["Local HTTP application port"],
            "tls": "Not required for localhost-only baseline",
            "dns": "Not applicable",
            "firewall_notes": "No inbound LAN/Internet exposure",
        }
        tech["operations"] = {
            "logging_observability": "Local application logs without secrets",
            "backup_restore": "Documented local DB backup/restore",
            "rollback": "Versioned code plus DB backup before destructive migration",
        }
        tech["costs"] = {
            "developer_ai_tooling": "Paid AI development subscription assumed",
            "product_external_services": [],
            "recurring_cost_assumptions": ["No paid product service in baseline"],
        }
        tech["unresolved"] = []
        tech_path.write_text(json.dumps(tech, indent=2) + "\n", encoding="utf-8")

        plan_path = control / "state" / "DELIVERY_PLAN_CURRENT.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        plan.update(
            {
                "plan_version": "1",
                "status": "CURRENT",
                "updated_at": "2035-01-02T12:00:00Z",
                "planning_start_date": "2035-01-02",
                "target_release_date": "2035-02-15",
                "schedule_basis": "Synthetic target derived from confirmed baseline.",
                "milestones": [
                    {
                        "id": "M1",
                        "title": "Core CRUD capability",
                        "target_date": "2035-01-20",
                        "status": "PLANNED",
                        "capability_ids": ["CAP_CORE"],
                        "depends_on": [],
                        "done_when": "Core create/read/update/delete flows pass functional tests.",
                        "forecast_confidence": "MEDIUM",
                        "evidence_refs": [],
                    },
                    {
                        "id": "M2",
                        "title": "Usable release candidate",
                        "target_date": "2035-02-15",
                        "status": "PLANNED",
                        "capability_ids": ["CAP_RELEASE"],
                        "depends_on": ["M1"],
                        "done_when": "Required workflows and simple UI verification pass.",
                        "forecast_confidence": "LOW",
                        "evidence_refs": [],
                    },
                ],
                "risks": [],
                "schedule_changes": [],
                "next_review_date": "2035-01-10",
                "unresolved": [],
            }
        )
        plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")

        ready = run(str(guard), "--control-root", str(control), "--json")
        if ready.returncode != 0 or json.loads(ready.stdout)["ready"] is not True:
            raise AssertionError(
                "completed baseline did not pass\n" + ready.stdout + ready.stderr
            )

        status = run(str(status_tool), "--control-root", str(control), "--json")
        status_data = json.loads(status.stdout)
        if (
            status.returncode != 0
            or status_data["baseline_ready"] is not True
            or status_data["target_release_date"] != "2035-02-15"
        ):
            raise AssertionError("derived project status lost baseline/date state")

        after_ready = run(
            str(campaignctl),
            "--control-root", str(control),
            "init",
            "--charter", "campaigns/MISSING.json",
        )
        after_combined = after_ready.stdout + after_ready.stderr
        if "PROJECT_BASELINE_NOT_READY" in after_combined:
            raise AssertionError("runtime still reports baseline blocked after readiness")
        if "missing required file" not in after_combined:
            raise AssertionError(
                "runtime did not advance past baseline gate\n" + after_combined
            )

    print("PROJECT BASELINE SELF-TEST PASSED")
    print("- fresh scaffold baseline is blocked")
    print("- runtime refuses campaign init before baseline readiness")
    print("- confirmed requirements + CURRENT technical baseline + dated plan pass")
    print("- derived project status exposes dates and readiness")
    print("- runtime advances beyond baseline gate after readiness")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
