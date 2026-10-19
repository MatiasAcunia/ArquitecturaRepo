#!/usr/bin/env python3
"""Bounded Gemini I4 due-check and privacy-gated read-only API transport.

This is NOT a Codex Goal integration. Delivery/consumption require a separately
verified host adapter; response cannot self-certify independent review.
"""
from __future__ import annotations

import json
import os
import re
import time
import hashlib
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class CognitiveHold(RuntimeError):
    pass


def due_check(*, material_entry: bool, evidence_changed: bool,
              repeated_failures: int, active_minutes_since_review: int | None,
              quota_verified: bool, export_authorized: bool) -> dict[str, Any]:
    trigger = (
        "MATERIAL_ENTRY" if material_entry else
        "NEW_EVIDENCE" if evidence_changed else
        "REPEATED_FAILURE_CLASS" if repeated_failures >= 2 else
        "LONG_GOAL_REVIEW" if active_minutes_since_review is not None and
        active_minutes_since_review >= 120 else None
    )
    if trigger is None:
        return {"status": "NOT_DUE", "trigger": None}
    if not export_authorized:
        return {"status": "SKIPPED_PRIVACY", "trigger": trigger}
    if not quota_verified:
        return {"status": "DEFERRED_QUOTA_UNVERIFIED", "trigger": trigger}
    return {"status": "DUE", "trigger": trigger}


def consult_public_or_synthetic(*, model: str, question: str,
                                export_classification: str, timeout: float = 15.0,
                                transport=None, engineering_role: str = "review",
                                zero_cost_admission: dict[str, Any] | None = None) -> dict[str, Any]:
    if export_classification != "PUBLIC_OR_SYNTHETIC":
        raise CognitiveHold("PRIVATE_DATA_EXPORT_NOT_AUTHORIZED")
    if not isinstance(question, str) or not (10 <= len(question) <= 4000):
        raise CognitiveHold("BOUNDED_QUESTION_REQUIRED")
    if not isinstance(model, str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._-]{1,79}", model):
        raise CognitiveHold("INVALID_MODEL")
    if engineering_role not in {"review", "code_proposal", "test_generation",
                                "architecture_options", "failure_analysis",
                                "engine_version_review", "contract_review"}:
        raise CognitiveHold("UNSUPPORTED_GEMINI_ENGINEERING_ROLE")
    # The expected provider project/tier/remaining free requests must be
    # attested by the actual operator/billing owner immediately before use.
    # Never mistake presence of GEMINI_API_KEY for USD 0 admission.
    proof = zero_cost_admission
    if (not isinstance(proof, dict)
            or proof.get("model") != model
            or proof.get("tier") != "FREE"
            or proof.get("billing_enabled") is not False
            or proof.get("eligible_for_free_generate_content") is not True
            or proof.get("authorized_spend_usd") != 0
            or not isinstance(proof.get("project_id"), str)
            or not proof["project_id"]
            or not isinstance(proof.get("source_ref"), str)
            or not proof["source_ref"]
            or type(proof.get("remaining_free_requests")) is not int
            or proof["remaining_free_requests"] <= 0
            or not isinstance(proof.get("expires_unix"), (int, float))
            or not time.time() < proof["expires_unix"] <= time.time() + 3600):
        raise CognitiveHold("HOLD_GEMINI_COST_NOT_VERIFIED")
    # Pin the declared admission to the actually selected authentication
    # identity when a trustworthy operator supplied its hash. Never log the
    # raw key, and do not rotate through Desktop files to evade free quotas.
    # Explicit local opt-in is separate from mere presence of a provider key.
    if os.environ.get("AGENTIC_SDLC_GEMINI_ENABLED") != "true":
        raise CognitiveHold("GEMINI_TRANSPORT_NOT_OPTED_IN")
    if not (0 < timeout <= 30):
        raise CognitiveHold("GEMINI_TIMEOUT_OUT_OF_BOUNDS")
    try:
        try:
            from .gemini_keyfile import resolve_key, GeminiCredentialHold
        except ImportError:
            from gemini_keyfile import resolve_key, GeminiCredentialHold
        key = resolve_key()
    except GeminiCredentialHold as exc:
        # Keep secret material out of exceptions/receipts. Authentication
        # is NOT evidence of free eligibility or authorized export.
        raise CognitiveHold(str(exc)) from None
    expected_hash = proof.get("api_key_sha256")
    if expected_hash is not None and (
            not isinstance(expected_hash, str)
            or expected_hash != hashlib.sha256(key.encode("utf-8")).hexdigest()):
        raise CognitiveHold("GEMINI_ACCOUNT_BINDING_MISMATCH")
    if transport is None:
        transport = urlopen
    # The model/version and quota are caller-owned and must have been verified.
    url = "https://generativelanguage.googleapis.com/v1beta/models/" + model + ":generateContent"
    body = json.dumps({"contents": [{"parts": [{"text": question}]}],
                       "generationConfig": {"temperature": 0.2,
                                            "responseMimeType": "application/json"}}).encode("utf-8")
    req = Request(url, data=body, headers={"Content-Type": "application/json",
                                           "x-goog-api-key": key}, method="POST")
    try:
        with transport(req, timeout=timeout) as response:
            if response.status != 200:
                raise CognitiveHold("PROVIDER_HTTP_UNEXPECTED")
            data = json.loads(response.read(200000).decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as error:
        raise CognitiveHold("PROVIDER_UNAVAILABLE_OR_QUOTA:" + type(error).__name__) from None
    if not isinstance(data, dict):
        raise CognitiveHold("PROVIDER_RESPONSE_MALFORMED")
    candidates = data.get("candidates", [])
    if not candidates:
        raise CognitiveHold("PROVIDER_EMPTY_RESPONSE")
    try:
        raw = candidates[0]["content"]["parts"][0]["text"]
        result = json.loads(raw)
        if not isinstance(result, dict):
            raise ValueError()
    except (ValueError, KeyError, IndexError, TypeError):
        raise CognitiveHold("PROVIDER_RESPONSE_SCHEMA_INVALID") from None
    if len(raw.encode("utf-8")) > 40000:
        raise CognitiveHold("PROVIDER_PROPOSAL_TOO_LARGE")
    # Provider proposal remains NON_EXECUTABLE and UNCONSUMED.
    # A caller-supplied cost proof is a prerequisite, NOT independent billing
    # verification or a guarantee that a provider charge is impossible.
    return {"schema_version": "cognitive-i4-proposal-v2", "status": "DELIVERY_PENDING",
            "engineering_role": engineering_role, "authorized_spend_usd": 0,
            "request_sha256": hashlib.sha256(body).hexdigest(),
            "response_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            "cost_attestation_source_ref": proof["source_ref"],
            "source_classification": export_classification, "model": model,
            "proposal": result, "consumed_by_i3": False,
            "independent_validation": "NOT_PERFORMED"}


if __name__ == "__main__":
    raise SystemExit("Import as a bounded adapter only.")
