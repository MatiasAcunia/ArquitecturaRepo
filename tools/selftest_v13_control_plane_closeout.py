#!/usr/bin/env python3
"""Independent-shaped regression gates for the v1.3 control-plane closeout.

All filesystem effects are confined to disposable stdlib TemporaryDirectory
roots. This checks FRAMEWORK-local governance, not host OS authentication.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTL = ROOT / "tools" / "campaignctl.py"
SCAFFOLD = ROOT / "tools" / "scaffold_project.py"
LEADER = "CAMPAIGN_LEAD_NOTE_API_001"
RUN = "RUN_I3_002"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def store(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def call(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *map(str, args)], text=True, capture_output=True, timeout=35)


def check_cli(control: Path, should_pass: bool, *params: str) -> str:
    r = call(CTL, "--control-root", str(control), *params)
    assert (r.returncode == 0) is should_pass, f"{params}: exit={r.returncode}\n{r.stderr}\n{r.stdout}"
    return r.stdout + r.stderr


def build_fixture(where: Path) -> Path:
    control = where / "control"
    shutil.copytree(ROOT / "examples" / "active_campaign", control)
    state = control / "state"
    state.mkdir(exist_ok=True)
    for item in ("PRODUCT_STATE_CURRENT.json", "CURRENT_BOOTSTRAP_STATE.json", "IDENTITY_REGISTRY_CURRENT.json", "EXECUTION_AUTHORITY_CURRENT.json"):
        shutil.move(str(control / item), str(state / item))
    ps = load(state / "PRODUCT_STATE_CURRENT.json")
    ps["currentness_set"] = ["state/PRODUCT_STATE_CURRENT.json", "state/CURRENT_BOOTSTRAP_STATE.json", "state/IDENTITY_REGISTRY_CURRENT.json", "state/EXECUTION_AUTHORITY_CURRENT.json", "CLIENT_REQUIREMENTS_CURRENT.md", "CAMPAIGN_API_001_CHARTER.json"]
    ps["active_campaign"]["checkpoint_or_terminal_ref"] = None
    store(state / "PRODUCT_STATE_CURRENT.json", ps)
    auth = load(state / "EXECUTION_AUTHORITY_CURRENT.json")
    auth["checkpoint_ref"] = None
    auth["expires_at"] = (datetime.now(timezone.utc) + timedelta(minutes=100)).isoformat().replace("+00:00", "Z")
    store(state / "EXECUTION_AUTHORITY_CURRENT.json", auth)
    bs = load(state / "CURRENT_BOOTSTRAP_STATE.json")
    bs.update({"requirements_ref": "CLIENT_REQUIREMENTS_CURRENT.md", "product_state_ref": "state/PRODUCT_STATE_CURRENT.json", "active_checkpoint_or_terminal_ref": None})
    store(state / "CURRENT_BOOTSTRAP_STATE.json", bs)
    check_cli(control, True, "init", "--charter", "CAMPAIGN_API_001_CHARTER.json")
    return control


def test_authority(root: Path) -> None:
    control = build_fixture(root / "actor")
    check_cli(control, True, "add", "--id", "A", "--title", "work")
    before = (control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_bytes()
    for actor, run in (("UNREGISTERED", "FAKE-RUN"), (LEADER, "FAKE-RUN"), ("UNREGISTERED", RUN)):
        check_cli(control, False, "start", "--id", "A", "--actor", actor, "--run", run)
        assert (control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json").read_bytes() == before
    check_cli(control, True, "start", "--id", "A", "--actor", LEADER, "--run", RUN)
    expired = control / "state" / "EXECUTION_AUTHORITY_CURRENT.json"
    authority = load(expired)
    authority["expires_at"] = "2020-01-01T00:00:00Z"
    store(expired, authority)
    for cmd in (("verify", "--id", "A"), ("add", "--id", "B", "--title", "other")):
        check_cli(control, False, *cmd)
    authority["expires_at"] = (datetime.now(timezone.utc) + timedelta(minutes=100)).isoformat().replace("+00:00", "Z")
    store(expired, authority)
    check_cli(control, True, "verify", "--id", "A")
    check_cli(control, True, "done", "--id", "A", "--result-ref", "result/A")


def review_fixture(where: Path) -> tuple[Path, Path]:
    control = build_fixture(where)
    registry = control / "state" / "IDENTITY_REGISTRY_CURRENT.json"
    data = load(registry)
    data["actors"].append({"actor_id": "QA", "role_class": "I4_EXECUTION_TEAM_MEMBER", "scope": "CAMPAIGN_API_001", "status": "ACTIVE", "current_run_id": "QA_RUN", "supersedes_actor_id": None})
    store(registry, data)
    evidence = control / "evidence" / "review.txt"
    evidence.parent.mkdir(exist_ok=True)
    evidence.write_text("correct original\n", encoding="utf-8")
    state = load(control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json")
    check_cli(control, True, "freeze", "--candidate-ref", state["integrated_ref"])
    check_cli(control, True, "review", "--reviewer", "QA", "--run", "QA_RUN", "--verdict", "PASS_FOR_STRATEGIC_RETURN", "--evidence", "evidence/review.txt")
    return control, evidence


def test_review(root: Path) -> None:
    term = ("terminal", "--type", "CAPABILITY_READY_FOR_PLANNER_ACCEPTANCE", "--reason", "examined")
    for scenario in ("MODIFIED", "DELETED", "REVIEWER_STALE", "BINDINGS_MISSING"):
        control, evidence = review_fixture(root / scenario)
        path = control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json"
        before = path.read_bytes()
        if scenario == "MODIFIED":
            evidence.write_text("different bytes\n", encoding="utf-8")
        elif scenario == "DELETED":
            evidence.unlink()
        elif scenario == "REVIEWER_STALE":
            registry = control / "state" / "IDENTITY_REGISTRY_CURRENT.json"
            data = load(registry)
            next(x for x in data["actors"] if x["actor_id"] == "QA")["current_run_id"] = "NEW_RUN"
            store(registry, data)
        else:
            data = load(path)
            data["review_freeze"]["evidence_bindings"] = []
            store(path, data)
            before = path.read_bytes()
        check_cli(control, False, *term)
        assert path.read_bytes() == before, f"terminal mutated runtime under {scenario}"
    control, _ = review_fixture(root / "VALID")
    check_cli(control, True, *term)
    assert load(control / "runtime" / "CAMPAIGN_RUNTIME_CURRENT.json")["campaign_status"] == "STRATEGIC_TERMINAL"


def test_scaffold(root: Path) -> None:
    project = root / "governed"
    (project / "state").mkdir(parents=True)
    canonical = project / "state" / "PRODUCT_STATE_CURRENT.json"
    canonical.write_text('{"product_or_workstream":"same"}\n', encoding="utf-8")
    previous = canonical.read_bytes()
    result = call(SCAFFOLD, "--target", str(project), "--profile", "SMALL", "--product-id", "same")
    assert result.returncode != 0 and "EXISTING_CANONICAL_PRODUCT_STATE_HOLD" in result.stderr
    assert canonical.read_bytes() == previous and not (project / ".agentic-sdlc").exists()
    fresh = root / "fresh"
    result = call(SCAFFOLD, "--target", str(fresh), "--profile", "SMALL", "--product-id", "fresh", "--no-feedback-workflow")
    assert result.returncode == 0, result.stderr
    assert "scheduled_workflow=DISABLED_BY_INSTALL_OPTION" in result.stdout
    assert "external_delivery=NOT_OBSERVED" in result.stdout
    assert "monthly strict metadata artifact ON" not in result.stdout
    assert not (fresh / ".github" / "workflows" / "agentic-sdlc-feedback.yml").exists()


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ar-v13-control-plane-") as tmp:
        root = Path(tmp)
        test_authority(root)
        test_review(root)
        test_scaffold(root)
    print("V1.3 CONTROL-PLANE CLOSEOUT PASSED: actor/lease, frozen evidence, reviewer, owner, opt-out, lawful terminal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
