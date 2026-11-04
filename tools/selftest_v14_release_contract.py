#!/usr/bin/env python3
"""Reject unsafe v1.4 publication wiring before it can run on main.

This static independent oracle is a pre-publication check, not a substitute
for published ZIP readback, GitHub Actions or anonymous container pulls.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    assert (ROOT / "VERSION").read_text(encoding="utf-8").strip() == "1.4.0"
    manifest = json.loads((ROOT / "state/STARTER_MANIFEST.json").read_text(encoding="utf-8"))
    decision = json.loads((ROOT / "state/V1_4_RELEASE_SCOPE_DECISION.json").read_text(encoding="utf-8"))
    assert manifest["version"] == "1.4.0" and manifest["status"] == "PUBLIC_STARTER_STABLE"
    assert decision["version"] == "1.4.0"
    assert decision["decision"] == "AUTHORIZE_E6_INTEGRATION_AND_PUBLIC_RELEASE"
    assert decision["historical_git_privacy_certification"] is False
    assert decision["native_codex_desktop_acceptance"] is False
    assert decision["third_party_customer_usability_acceptance"] is False

    publisher = (ROOT / ".github/workflows/publish-v1-4-release.yml").read_text(encoding="utf-8")
    legacy = (ROOT / ".github/workflows/publish-version-release.yml").read_text(encoding="utf-8")
    ci = (ROOT / ".github/workflows/validate-starter.yml").read_text(encoding="utf-8")
    docker = (ROOT / "packaging/v1_4/Dockerfile").read_text(encoding="utf-8")
    for clause in (
        "workflow_run:", 'workflows: ["validate-starter"]', "branches: [main]",
        "github.event.workflow_run.conclusion == 'success'",
        "github.event.workflow_run.event == 'push'",
        "github.event.workflow_run.head_branch == 'main'",
        "head_repository.full_name == github.repository",
        "ref: ${{ github.event.workflow_run.head_sha }}",
        "persist-credentials: false",
        "git ls-remote origin refs/heads/main",
        "state/V1_4_RELEASE_SCOPE_DECISION.json",
        "Windows portable-core smoke (not Codex Desktop acceptance)",
        "python tools/validate_structure.py",
        "python tools/package_v14_release.py --build",
        "python tools/package_v14_release.py --verify",
        "gh release create",
        "gh release upload",
        "gh release download",
        "curl --fail --location",
        "docker build --pull",
        "docker image rm",
        "docker logout ghcr.io",
        "docker pull",
        "tagged_source_gate:",
        "needs: tagged_source_gate",
        "needs.tagged_source_gate.outputs.should_publish == 'true'",
        "gh release view v1.4.0",
        "should_publish=false",
        "IMMUTABLE_TAG_WITHOUT_RELEASE_HOLD",
        "needs: release",
        "v1.4.0",
    ):
        assert clause in publisher, f"missing exact-source publication guard: {clause}"
    assert "pull_request:" not in publisher
    assert "workflow_dispatch:" not in publisher
    assert publisher.count("permissions:") >= 3
    assert "1.3.0)" in legacy and "1.4.0)" in legacy and "skip=true" in legacy
    assert "python tools/selftest_v14_release_contract.py" in ci
    assert "python tools/package_v14_release.py --build" in ci
    assert "packaging/v1_4/Dockerfile" in ci
    assert "COPY . /opt/architecturarepo/" in docker
    assert 'org.opencontainers.image.version="1.4.0"' in docker
    assert "FROM python:3.12-slim" in docker
    assert (ROOT / "docs/47_V1_4_RELEASE_NOTES_AND_UPGRADE.md").is_file()
    print("V1.4 PUBLICATION CONTRACT PASSED — explicit authority, exact main CI, ZIP byte readback, isolated image")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
