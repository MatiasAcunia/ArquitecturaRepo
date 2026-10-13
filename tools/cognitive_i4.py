#!/usr/bin/env python3
"""Bounded Gemini I4 due-check and privacy-gated read-only API transport.

This is NOT a Codex Goal integration. Delivery/consumption require a separately
verified host adapter; response cannot self-certify independent review.
"""
from __future__ import annotations

import json
import os
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
                                transport=None) -> dict[str, Any]:
    if export_classification != "PUBLIC_OR_SYNTHETIC":
        raise CognitiveHold("PRIVATE_DATA_EXPORT_NOT_AUTHORIZED")
    if not isinstance(question, str) or not (10 <= len(question) <= 4000):
        raise CognitiveHold("BOUNDED_QUESTION_REQUIRED")
    if not isinstance(model, str) or not model or "/" in model:
        raise CognitiveHold("INVALID_MODEL")
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise CognitiveHold("GEMINI_API_KEY_NOT_CONFIGURED")
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
    # Provider proposal remains NON_EXECUTABLE and UNCONSUMED.
    return {"schema_version": "cognitive-i4-proposal-v1", "status": "DELIVERY_PENDING",
            "source_classification": export_classification, "model": model,
            "proposal": result, "consumed_by_i3": False,
            "independent_validation": "NOT_PERFORMED"}


if __name__ == "__main__":
    raise SystemExit("Import as a bounded adapter only.")
