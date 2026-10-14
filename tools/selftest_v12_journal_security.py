#!/usr/bin/env python3
"""Adversarial crash-journal safety, plus one physically valid local recovery."""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path

from state_tx import (
    StateTransactionError, journal_path, recover, sha256_bytes
)


def refused(control: Path, journal: dict, *, outer_marker: Path) -> None:
    current=journal_path(control)
    current.parent.mkdir(parents=True, exist_ok=True)
    payload=json.dumps(journal,sort_keys=True)
    current.write_text(payload,encoding="utf-8")
    before=outer_marker.read_bytes()
    try:
        recover(control)
    except StateTransactionError:
        pass
    else:
        raise AssertionError("MALICIOUS_JOURNAL_WAS_ACCEPTED")
    assert outer_marker.read_bytes()==before, "RECOVERY_TOUCHED_OUTSIDE_PROJECT"
    assert current.read_text(encoding="utf-8")==payload, "INVALID_JOURNAL_WAS_MUTATED"


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="journal-attack-") as tmp:
        root=Path(tmp)
        control=root/"control"
        (control/"runtime"/"transactions").mkdir(parents=True)
        outside=root/"OUTSIDE_PRIVATE_DATA"
        outside.write_bytes(b"DO_NOT_TOUCH")
        tx="a"*32
        stage=f"runtime/transactions/{tx}/op_0001.json"
        path=control/stage
        path.parent.mkdir(parents=True)
        path.write_bytes(b"SAFE_REPLAY")
        base={
            "schema_version":"transition-journal-0.1",
            "transaction_id":tx,
            "label":"synthetic",
            "status":"PREPARED",
            "operations":[{
                "path":"state/RECOVERED.json",
                "before_exists":False,"before_sha256":None,
                "after_sha256":sha256_bytes(b"SAFE_REPLAY"),
                "stage_ref":stage,"applied":False,
            }],
        }
        variants=[
            ("traversal",{"path":"../../OUTSIDE_PRIVATE_DATA"}),
            ("absolute",{"path":str(outside)}),
            ("win_drive",{"path":"C:\\tmp\\PRIVATE"}),
            ("stage_traversal",{"stage_ref":"../../OUTSIDE_PRIVATE_DATA"}),
            ("stage_wrong_tx",{"stage_ref":f"runtime/transactions/{'b'*32}/op_0001.json"}),
            ("protected",{"path":"runtime/transactions/CURRENT_TRANSACTION.json"}),
            ("lock",{"path":"runtime/.campaignctl.lock"}),
            ("bad_hash",{"after_sha256":"NOT_A_SHA"}),
            ("missing_hash",{"before_exists":True,"before_sha256":None}),
            ("bad_applied",{"applied":"true"}),
        ]
        for name, edits in variants:
            journal=json.loads(json.dumps(base))
            journal["operations"][0].update(edits)
            refused(control,journal,outer_marker=outside)
        invalid_id=json.loads(json.dumps(base))
        invalid_id["transaction_id"]="../../escape"
        refused(control,invalid_id,outer_marker=outside)
        missing_ops=json.loads(json.dumps(base))
        missing_ops["operations"]=[]
        refused(control,missing_ops,outer_marker=outside)
        duplicate=json.loads(json.dumps(base))
        duplicate["operations"].append(dict(duplicate["operations"][0]))
        refused(control,duplicate,outer_marker=outside)
        if hasattr(os,"symlink"):
            link=control/"state"
            try:
                link.symlink_to(root,target_is_directory=True)
            except (OSError, NotImplementedError):
                pass
            else:
                malicious=json.loads(json.dumps(base))
                malicious["operations"][0]["path"]="state/OUTSIDE_PRIVATE_DATA"
                refused(control,malicious,outer_marker=outside)
                link.unlink()

        # An untampered journal must remain recoverable after a crash.
        journal_path(control).write_text(json.dumps(base),encoding="utf-8")
        result=recover(control)
        assert result==tx
        assert (control/"state"/"RECOVERED.json").read_bytes()==b"SAFE_REPLAY"
        assert not journal_path(control).exists()
        assert not (control/"runtime"/"transactions"/tx).exists()
        assert outside.read_bytes()==b"DO_NOT_TOUCH"
    print("V1.2 JOURNAL SECURITY PASSED — 13 adversarial cases and valid recovery")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
