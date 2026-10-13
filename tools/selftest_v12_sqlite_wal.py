#!/usr/bin/env python3
"""A main-file hash alone MUST NOT accept committed SQLite WAL updates."""
from __future__ import annotations

import hashlib
from contextlib import closing
import json
import sqlite3
import tempfile
from pathlib import Path

from goal_guard import assess, goal_fingerprint
from goal_plan import update, TacticalPlanError
from sqlite_currentness import snapshot_sha256, is_sqlite_database, wal_nonempty


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="sqlite-wal-currentness-") as tmp:
        control=Path(tmp)/"control"
        (control/"state").mkdir(parents=True)
        (control/"runtime").mkdir()
        charter=control/"state"/"CHARTER.md"
        charter.write_text("synthetic authorized charter")
        db=control/"state"/"canonical.sqlite"
        connection=sqlite3.connect(db)
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA wal_autocheckpoint=0")
        connection.execute("CREATE TABLE item (id INTEGER PRIMARY KEY, name TEXT)")
        connection.execute("INSERT INTO item(name) VALUES ('first')")
        connection.commit()
        assert is_sqlite_database(db)
        assert wal_nonempty(db), "fixture must retain active WAL"
        main_bytes=sha(db)
        charter_hash=sha(charter)
        goal={
            "schema_version":"agentic-goal-contract-v1",
            "goal_id":"WAL_TEST","campaign_id":"WAL_CAMPAIGN",
            "charter_ref":"state/CHARTER.md","charter_sha256":charter_hash,
            "authority_refs":{"state/CHARTER.md":charter_hash},
            "definition_of_done":"synthetic WAL currentness",
            "hard_gates":["WAL_SNAPSHOT"],"forbidden_effects":["PUBLICATION"],
            "write_envelope":["runtime"],
            "canonical_store":{"required":True,"ref":"state/canonical.sqlite",
                               "sha256":main_bytes},
        }
        goal_file=control/"state"/"GOAL_CONTRACT_CURRENT.json"
        goal_file.write_text(json.dumps(goal))
        diagnostic=assess(control)
        assert "SQLITE_WAL_CURRENTNESS_UNBOUND" in diagnostic["failure_codes"]
        try:
            update(control,expected_revision=-1,plan={"steps":[]},
                   active_minutes=1,review_evidence_ref="synthetic")
        except TacticalPlanError as e:
            assert "SQLITE_WAL_CURRENTNESS_UNBOUND" in str(e)
        else:
            raise AssertionError("unbound WAL permitted Plan revision")
        snapshot=snapshot_sha256(db)
        goal["canonical_store"]["sqlite_snapshot_sha256"]=snapshot
        goal_file.write_text(json.dumps(goal))
        checked=assess(control)
        assert checked["local_integrity_passed"] is False  # Plan not yet stored.
        assert "SQLITE_WAL_CURRENTNESS_UNBOUND" not in checked["failure_codes"]
        first=update(control,expected_revision=-1,plan={"steps":[]},
                     active_minutes=2,review_evidence_ref="synthetic")
        assert first["revision"]==0
        assert assess(control)["local_integrity_passed"] is True
        assert assess(control)["may_execute_material_goal"] is False

        # WAL changes can leave the main DB file byte-identical.
        connection.execute("INSERT INTO item(name) VALUES ('second')")
        connection.commit()
        assert sha(db)==main_bytes, "expected writes to remain uncheckpointed in WAL"
        assert snapshot_sha256(db)!=snapshot
        stale=assess(control)
        assert "SQLITE_SNAPSHOT_STALE" in stale["failure_codes"]
        try:
            update(control,expected_revision=0,plan={"steps":[]},
                   active_minutes=3,review_evidence_ref="stale")
        except TacticalPlanError as e:
            assert "SQLITE_SNAPSHOT_STALE" in str(e)
        else:
            raise AssertionError("stale WAL snapshot permitted Plan update")
        plan=json.loads((control/"runtime"/"TACTICAL_PLAN_CURRENT.json").read_text())
        assert plan["revision"]==0

        # A normal non-WAL live SQLite DB also needs an application-level
        # consistent witness; a bare file hash is not a safe universal gate.
        legacy=control/"state"/"legacy.sqlite"
        with closing(sqlite3.connect(legacy)) as plain:
            plain.execute("CREATE TABLE records(id INTEGER PRIMARY KEY)")
            plain.commit()
        from sqlite_currentness import inspect_store
        assert "SQLITE_CONSISTENT_SNAPSHOT_REQUIRED" in inspect_store(
            legacy,{"required":True,"ref":"state/legacy.sqlite","sha256":sha(legacy)}
        )
        # No sidecar-less immutable read fallback: a corrupt DB must HOLD.
        connection.close()
        db.write_bytes(b"not an SQLite source")
        failed=assess(control)
        assert "SQLITE_SNAPSHOT_SOURCE_INVALID" in failed["failure_codes"]
    print("SQLITE WAL CURRENTNESS PASSED: main-file hash unchanged but WAL snapshot invalidates Goal/Plan")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
