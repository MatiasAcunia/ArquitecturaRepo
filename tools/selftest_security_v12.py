#!/usr/bin/env python3
"""Security invariants for v1.2's portable source and optional host adapters.

Tests trusted upstream action pins, strict scope, no misleading release claim,
no host-permit shortcut, disabled external effects by default, and no private
data path by default. Physical host/provider gates remain separate.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from goal_guard import assess
from feedback_submit import FeedbackHold, safe_endpoint


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ACTION_PINS = {
    "actions/checkout": ("11bd71901bbe5b1630ce" + "ea73d27597364c9af683", "4.2.2"),
    "actions/setup-python": ("a26af69be951a213d495" + "a4c3e4e4022e16d87065", "5.6.0"),
    "actions/upload-artifact": ("ea165f8d65b6e75b5404" + "49e92b4886f43607fa02", "4.6.2"),
}


def main() -> int:
    for workflow in (
        ROOT / ".github" / "workflows" / "validate-starter.yml",
        ROOT / "templates" / "AGENTIC_SDLC_FEEDBACK_WORKFLOW.yml",
    ):
        source = workflow.read_text(encoding="utf-8")
        uses = re.findall(r"(?m)^\s*(?:-\s*)?uses:\s*(actions/[A-Za-z-]+)@([0-9a-f]{40})\s*#\s*v(\d+\.\d+\.\d+)\s*$", source)
        if len(uses) < 2:
            raise AssertionError("workflow has unpinned / missing official actions: " + str(workflow))
        for action, commit, version in uses:
            if action not in EXPECTED_ACTION_PINS or (commit, version) != EXPECTED_ACTION_PINS[action]:
                raise AssertionError("unreviewed upstream action pin: " + action)
        if re.search(r"(?m)^\s*(?:-\s*)?uses:\s*actions/[^@\s]+@v\d", source):
            raise AssertionError("mutable GitHub Action tag in " + str(workflow))
        if "permissions:\n  contents: read" not in source:
            raise AssertionError("workflow requests unexpected repository permissions")
        if "persist-credentials: false" not in source:
            raise AssertionError("workflow accidentally persists checkout token")
    feedback_wf = (ROOT / "templates" / "AGENTIC_SDLC_FEEDBACK_WORKFLOW.yml").read_text(encoding="utf-8")
    if "23 4 * * 0" in feedback_wf:
        raise AssertionError("weekly job remains despite monthly default")
    if "tools/feedback_submit.py" not in feedback_wf:
        raise AssertionError("optional external submission bypasses schema/hash validation")
    if "head -c 2000" in feedback_wf or "curl --data" in feedback_wf:
        raise AssertionError("unbounded/raw collector output remains")

    with tempfile.TemporaryDirectory(prefix="security-v12-") as tmp:
        integrity = assess(Path(tmp))
        if integrity.get("may_execute_material_goal") is not False:
            raise AssertionError("unconfigured Goal unexpectedly authorized")
    versions = json.loads((ROOT / "state" / "V1_2_ACCEPTANCE_CRITERIA.json").read_text(encoding="utf-8"))
    if versions["baseline_stable_version"] != "1.1.0":
        raise AssertionError("baseline version advanced without physical gates")
    release_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if release_version == "1.2.0":
        # CLIENT authorized publishing the portable source independently of
        # accepting the separately tracked, still-required native host gates.
        scope_path = ROOT / "state" / "V1_2_RELEASE_SCOPE_DECISION.json"
        scope = json.loads(scope_path.read_text(encoding="utf-8"))
        if (scope.get("schema_version") != "agentic-v12-client-scoped-release-decision-v1"
            or scope.get("version") != release_version
            or scope.get("authority_source") != "EXPLICIT_CLIENT_DIRECTIVE_IN_CONVERSATION_UNATTESTED_BY_NATIVE_HOST"
            or scope.get("ship_scope") != "PORTABLE_CORE_WITH_DECLARED_UNVERIFIED_NATIVE_CAPABILITIES"
            or scope.get("full_physical_release_accepted") is not False
            or scope.get("physical_release_gates_overridden") is not False
            or not isinstance(scope.get("excluded_claims"), list)
            or len(scope["excluded_claims"]) < 5):
            raise AssertionError("scoped portable source release lacks explicit and bounded CLIENT decision")
        gates = versions.get("gates", [])
        if (len(gates) != 15 or not all(g.get("required") is True for g in gates)
            or any(g.get("status") == "PHYSICALLY_VERIFIED_EXACT" for g in gates)):
            raise AssertionError("physical acceptance criteria silently altered for source release")
    elif release_version == "1.3.0":
        # Backward-compatibility gate: never reinterpret v1.2 CLIENT authority
        # as an authorization to publish v1.3.0. A staged version is legal
        # only when it cannot be released by the legacy automatic publisher.
        legacy_scope = json.loads((ROOT / "state" / "V1_2_RELEASE_SCOPE_DECISION.json").read_text(encoding="utf-8"))
        if (legacy_scope.get("version") != "1.2.0"
            or legacy_scope.get("full_physical_release_accepted") is not False
            or legacy_scope.get("physical_release_gates_overridden") is not False):
            raise AssertionError("v1.3 staging rewrote v1.2 CLIENT/release history")
        manual_path = ROOT / ".github" / "workflows" / "publish-v1-3-manual.yml"
        old_path = ROOT / ".github" / "workflows" / "publish-version-release.yml"
        if not manual_path.is_file():
            raise AssertionError("v1.3 draft has no explicit release publisher")
        manual = manual_path.read_text(encoding="utf-8")
        old_auto = old_path.read_text(encoding="utf-8")
        if ("workflow_dispatch:" not in manual
            or "workflow_run:" in manual
            or "push:" in manual
            or "exact_commit_sha" not in manual
            or "RELEASE_V1_3_0" not in manual
            or "github.ref == 'refs/heads/main'" not in manual
            or "github.actor == 'MatiasAcunia'" not in manual
            or "git ls-remote origin refs/heads/main" not in manual
            or "1.3.0)" not in old_auto
            or "skip=true" not in old_auto
            or old_auto.count("steps.identity.outputs.skip != 'true'") != 2):
            raise AssertionError("v1.3 staging weakened exact-source/manual publication boundary")
    elif release_version != "1.1.0":
        raise AssertionError("release version unauthorized or no scoped CLIENT decision")
    verifier = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "verify_v12_candidate.py"),
         "--json", "--require-release-ready"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if verifier.returncode != 2:
        raise AssertionError("release verifier did not fail-closed on unproven physical gates")
    result = json.loads(verifier.stdout)
    if result["release_ready"] is not False or not result["physical_gates_not_yet_accepted"]:
        raise AssertionError("unverified candidate claimed release readiness")
    print("V1.2 SECURITY SELF-TEST PASSED — pinned upstream actions, exact scope and fail-closed release")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
