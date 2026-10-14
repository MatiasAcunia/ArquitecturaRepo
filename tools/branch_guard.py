#!/usr/bin/env python3
"""Conservative decision-only branch advisor. Never creates/deletes refs."""
from __future__ import annotations

import argparse
import json
from typing import Any


APPROVED_REASONS = {
    "CONCURRENT_ISOLATION", "RELEASE_CANDIDATE", "HOTFIX", "RISK_EXPERIMENT",
}


def assess(*, reason: str, affected_surfaces: list[str],
           owner: str, baseline_sha: str,
           isolation_or_rollback_ref: str | None) -> dict[str, Any]:
    problems = []
    if reason not in APPROVED_REASONS:
        problems.append("BRANCH_MANIA_REASON_NOT_LEGAL")
    if not isinstance(owner, str) or not owner.strip():
        problems.append("INTEGRATION_OWNER_MISSING")
    if not isinstance(baseline_sha, str) or len(baseline_sha) != 40 or any(
        ch not in "0123456789abcdef" for ch in baseline_sha):
        problems.append("EXACT_BASELINE_NOT_PROVEN")
    if (not isinstance(affected_surfaces, list) or not affected_surfaces or
        len(affected_surfaces) > 64 or
        any(not isinstance(p, str) or not p or len(p) > 200 or ".." in p
            or p.startswith("/") or "\\" in p for p in affected_surfaces)):
        problems.append("BOUNDED_WRITE_SURFACES_REQUIRED")
    if not isinstance(isolation_or_rollback_ref, str) or not isolation_or_rollback_ref.strip():
        problems.append("WORKTREE_ISOLATION_OR_ROLLBACK_NOT_SPECIFIED")
    # Only the canonical I3/merge controller can decide actual safe concurrency.
    return {
        "schema_version": "branch-necessity-review-v1",
        "status": "HOLD" if problems else "JUSTIFICATION_COMPLETE_PENDING_I3_REVIEW",
        "may_create_branch": False,
        "isolation_candidate": not problems,
        "required_canonical_review": ["EXACT_REMOTE_HEAD", "ACTIVE_WRITER_AND_DB_CONFLICTS",
                                      "EXISTING_BRANCHES", "CLEANUP_OWNER", "I3_AUTHORIZATION"],
        "failure_codes": sorted(problems),
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Read-only branch necessity audit")
    p.add_argument("--reason", required=True)
    p.add_argument("--surface", action="append", required=True)
    p.add_argument("--owner", required=True)
    p.add_argument("--baseline-sha", required=True)
    p.add_argument("--isolation-ref", required=True)
    a = p.parse_args()
    report = assess(reason=a.reason, affected_surfaces=a.surface, owner=a.owner,
                    baseline_sha=a.baseline_sha, isolation_or_rollback_ref=a.isolation_ref)
    print(json.dumps(report, indent=2))
    return 0 if report["isolation_candidate"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
