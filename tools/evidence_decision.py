#!/usr/bin/env python3
"""Evidence-bound decision objects. Valid records are not product acceptance."""
from __future__ import annotations

import hashlib
import json
from typing import Any


class EvidenceHold(ValueError):
    pass


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode("utf-8")).hexdigest()


def bind_candidate(*, source_hashes: dict[str, str], payload: dict[str, Any],
                   author_actor: str) -> dict[str, Any]:
    if not author_actor or not isinstance(source_hashes, dict) or not source_hashes:
        raise EvidenceHold("EVIDENCE_BINDING_INCOMPLETE")
    if any(not isinstance(v, str) or len(v) != 64 or
           any(c not in "0123456789abcdef" for c in v) for v in source_hashes.values()):
        raise EvidenceHold("UNVERIFIED_SOURCE_DIGEST")
    if not isinstance(payload, dict) or not payload:
        raise EvidenceHold("CANDIDATE_EMPTY")
    return {
        "schema_version": "evidence-bound-candidate-v1",
        "author_actor": author_actor,
        "source_hashes": dict(sorted(source_hashes.items())),
        "candidate_sha256": digest(payload),
        "payload": payload,
        "status": "FROZEN_NOT_ACCEPTED",
    }


def review(candidate: dict[str, Any], *, reviewer_actor: str,
           original_sources: dict[str, str], review_result: str,
           falsifier_refs: list[str]) -> dict[str, Any]:
    if reviewer_actor == candidate.get("author_actor") or not reviewer_actor:
        raise EvidenceHold("SELF_REVIEW_CANNOT_CLAIM_INDEPENDENCE")
    if review_result not in {"SUPPORTED_FOR_FURTHER_GATE", "HOLD", "REJECTED"}:
        raise EvidenceHold("UNSUPPORTED_REVIEW_RESULT")
    if candidate.get("schema_version") != "evidence-bound-candidate-v1" or (
        digest(candidate.get("payload")) != candidate.get("candidate_sha256")
    ):
        raise EvidenceHold("FROZEN_CANDIDATE_DRIFT")
    if original_sources != candidate.get("source_hashes"):
        raise EvidenceHold("EVIDENCE_SOURCE_DRIFT")
    if not isinstance(falsifier_refs, list) or any(not isinstance(x, str) for x in falsifier_refs):
        raise EvidenceHold("INVALID_FALSIFIER_REFS")
    return {
        "schema_version": "evidence-bound-review-v1",
        "candidate_sha256": candidate["candidate_sha256"],
        "source_hashes": original_sources,
        "reviewer_actor": reviewer_actor,
        "review_result": review_result,
        "falsifier_refs": falsifier_refs,
        "product_acceptance": "NOT_CLAIMED",
    }
