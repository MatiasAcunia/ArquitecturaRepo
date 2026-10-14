#!/usr/bin/env python3
"""Crash-safe logical external-effect ledger; never performs an external effect.

This ledger only records an asserted readback; it cannot validate provider truth.
An actual authorized provider adapter must supply independent readback. An ambiguous
request is NOT a license to retry. Uses the existing state_tx owner.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from state_tx import state_lock, write_json_set


class ExternalEffectHold(ValueError):
    pass


def sha(data: Any) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode("utf-8")).hexdigest()


def path_for(root: Path, effect_id: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", effect_id):
        raise ExternalEffectHold("UNSAFE_EFFECT_ID")
    return root.resolve() / "runtime" / "external_effects" / (effect_id + ".json")


def read(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ExternalEffectHold("INVALID_EFFECT_RECORD")
    return data


def transition(root: Path, effect_id: str, event: str, *,
               request: dict[str, Any] | None = None,
               authorized_ref: str | None = None,
               proof: dict[str, Any] | None = None) -> dict:
    root = root.resolve()
    path = path_for(root, effect_id)
    with state_lock(root):
        old = read(path) if path.is_file() else None
        if event == "PREPARE":
            if not isinstance(request, dict) or not request or not authorized_ref:
                raise ExternalEffectHold("AUTHORITY_AND_REQUEST_REQUIRED")
            request_sha = sha(request)
            if old:
                if old["request_sha256"] != request_sha or old["authorized_ref"] != authorized_ref:
                    raise ExternalEffectHold("EFFECT_IDEMPOTENCY_CONFLICT")
                return old
            new = {
                "schema_version": "agentic-external-effect-v1",
                "effect_id": effect_id,
                "request_sha256": request_sha,
                "authorized_ref": authorized_ref,
                "phase": "PREPARED",
                "attempts": 0,
                "receipt_attestation": None,
            }
        elif old is None:
            raise ExternalEffectHold("EFFECT_NOT_PREPARED")
        elif event == "ATTEMPT":
            if old["phase"] != "PREPARED":
                raise ExternalEffectHold("DUPLICATE_OR_AMBIGUOUS_EFFECT_DISPATCH")
            # Mark REQUESTED durably BEFORE an actual adapter sends anything.
            # Crash after this write is ambiguous until independently reconciled.
            new = {**old, "phase": "REQUESTED_AMBIGUOUS", "attempts": 1}
        elif event == "HOLD":
            if old["phase"] == "RECEIPT_ATTESTED_UNVERIFIED":
                raise ExternalEffectHold("RECEIPT_ALREADY_ATTESTED")
            new = {**old, "phase": "HOLD_RECONCILIATION_REQUIRED"}
        elif event == "RECEIPT":
            if old["phase"] not in {"REQUESTED_AMBIGUOUS", "HOLD_RECONCILIATION_REQUIRED"}:
                raise ExternalEffectHold("RECEIPT_WRONG_PHASE")
            if (not isinstance(proof, dict) or
                proof.get("request_sha256") != old["request_sha256"] or
                proof.get("readback_verified") is not True or
                not isinstance(proof.get("external_receipt_sha256"), str) or
                not re.fullmatch(r"[a-f0-9]{64}", proof["external_receipt_sha256"])):
                raise ExternalEffectHold("INDEPENDENT_EXACT_READBACK_REQUIRED")
            # Caller claims readback; this is NOT independent validation. A real
            # adapter and immutable provider receipt remain a separate hard gate.
            new = {**old, "phase": "RECEIPT_ATTESTED_UNVERIFIED",
                   "receipt_attestation": {k: proof[k] for k in
                     ("request_sha256", "external_receipt_sha256", "readback_verified")}}
        else:
            raise ExternalEffectHold("UNSUPPORTED_EFFECT_TRANSITION")
        write_json_set(root, "EXTERNAL_EFFECT_" + event, [(path, new)])
        return new


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--control-root", type=Path, required=True)
    p.add_argument("--effect-id", required=True)
    p.add_argument("--event", choices=("PREPARE", "ATTEMPT", "HOLD", "RECEIPT"), required=True)
    p.add_argument("--request-file", type=Path)
    p.add_argument("--authorized-ref")
    p.add_argument("--proof-file", type=Path)
    a = p.parse_args()
    try:
        request = json.loads(a.request_file.read_text()) if a.request_file else None
        proof = json.loads(a.proof_file.read_text()) if a.proof_file else None
        out = transition(a.control_root, a.effect_id, a.event, request=request,
                         authorized_ref=a.authorized_ref, proof=proof)
    except (OSError, ValueError, KeyError) as e:
        p.exit(2, "EXTERNAL EFFECT HOLD: " + str(e) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
