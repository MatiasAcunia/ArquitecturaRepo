#!/usr/bin/env python3
"""Durable single-owner receipt chain for optional I4 cognitive consultations.

Never executes an LLM. Network attempts are separately accounted, and returned
advice never becomes product authority, I3 consumption or independent review.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from state_tx import state_lock, write_json_set


class ConsultationHold(ValueError):
    pass


def _is_sha(value: Any) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"[a-f0-9]{64}", value))


def _path(root: Path, consultation_id: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", consultation_id):
        raise ConsultationHold("INVALID_CONSULTATION_ID")
    return root.resolve() / "runtime" / "cognitive_i4" / (consultation_id + ".json")


def _read(path: Path) -> dict[str, Any]:
    result = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(result, dict):
        raise ConsultationHold("INVALID_CONSULTATION_RECORD")
    return result


def register(root: Path, *, consultation_id: str, campaign_id: str,
             source_digest: str, question_digest: str, model: str,
             export_classification: str) -> dict[str, Any]:
    if not campaign_id or not model or not _is_sha(source_digest) or not _is_sha(question_digest):
        raise ConsultationHold("INVALID_CONSULTATION_IDENTITY")
    if export_classification != "PUBLIC_OR_SYNTHETIC":
        raise ConsultationHold("UNAUTHORIZED_SOURCE_EXPORT")
    root = root.resolve()
    path = _path(root, consultation_id)
    with state_lock(root):
        row = {
            "schema_version": "agentic-i4-consultation-v1",
            "consultation_id": consultation_id,
            "campaign_id": campaign_id,
            "source_digest": source_digest,
            "question_digest": question_digest,
            "model": model,
            "export_classification": export_classification,
            "phase": "DUE",
            "network_attempt_count": 0,
            "response_sha256": None,
            "host_delivery_ref": None,
            "host_consumption_ref": None,
            "disposition_evidence_ref": None,
        }
        if path.is_file():
            existing = _read(path)
            if any(existing.get(key) != row[key] for key in (
                    "consultation_id", "campaign_id", "source_digest",
                    "question_digest", "model", "export_classification")):
                raise ConsultationHold("CONSULTATION_IDEMPOTENCY_CONFLICT")
            return existing
        write_json_set(root, "I4_CONSULTATION_REGISTER", [(path, row)])
        return row


def advance(root: Path, consultation_id: str, event: str, *,
            current_source_digest: str,
            response_sha256: str | None = None,
            evidence_ref: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    path = _path(root, consultation_id)
    with state_lock(root):
        if not path.is_file():
            raise ConsultationHold("CONSULTATION_NOT_REGISTERED")
        old = _read(path)
        if old["source_digest"] != current_source_digest:
            raise ConsultationHold("CONSULTATION_SOURCE_STALE")
        phase = old["phase"]
        if event == "CLAIM" and phase == "DUE":
            new = {**old, "phase": "CLAIMED"}
        elif event == "REQUEST" and phase == "CLAIMED":
            # Commit REQUESTED before the provider call. Crash/timeout is ambiguous.
            new = {**old, "phase": "REQUESTED_AMBIGUOUS",
                   "network_attempt_count": old["network_attempt_count"] + 1}
        elif event == "RESPONSE" and phase == "REQUESTED_AMBIGUOUS":
            if not _is_sha(response_sha256):
                raise ConsultationHold("RESPONSE_DIGEST_REQUIRED")
            new = {**old, "phase": "RESPONSE_RECORDED_UNCONSUMED",
                   "response_sha256": response_sha256}
        elif event == "DELIVER" and phase == "RESPONSE_RECORDED_UNCONSUMED":
            if not evidence_ref:
                raise ConsultationHold("HOST_DELIVERY_PROOF_REQUIRED")
            new = {**old, "phase": "DELIVERY_ATTESTED_UNCONSUMED",
                   "host_delivery_ref": evidence_ref}
        elif event == "CONSUME" and phase == "DELIVERY_ATTESTED_UNCONSUMED":
            if not evidence_ref:
                raise ConsultationHold("SUBSEQUENT_I3_MODEL_EVENT_REQUIRED")
            new = {**old, "phase": "CONSUMPTION_ATTESTED_UNVALIDATED",
                   "host_consumption_ref": evidence_ref}
        elif event in ("ADOPT", "REJECT") and phase == "CONSUMPTION_ATTESTED_UNVALIDATED":
            if not evidence_ref:
                raise ConsultationHold("INDEPENDENT_TEST_OR_CAUSAL_EVIDENCE_REQUIRED")
            new = {**old, "phase": "ADOPTED_PENDING_GATE" if event == "ADOPT" else "REJECTED_WITH_EVIDENCE",
                   "disposition_evidence_ref": evidence_ref}
        else:
            raise ConsultationHold("INVALID_OR_DUPLICATE_CONSULTATION_TRANSITION")
        write_json_set(root, "I4_CONSULTATION_" + event, [(path, new)])
        return new
