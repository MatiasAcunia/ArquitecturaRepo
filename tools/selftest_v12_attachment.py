#!/usr/bin/env python3
"""Attachment must neither duplicate canonical ownership nor touch source."""
from __future__ import annotations
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path
from existing_repo_attachment import inspect,AttachmentHold
from sqlite_currentness import snapshot_sha256

ROOT=Path(__file__).resolve().parents[1]

def sha(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main()->int:
    with tempfile.TemporaryDirectory(prefix="attachment-v12-") as d:
        repo=Path(d)/"established"
        (repo/"state").mkdir(parents=True)
        (repo/"docs").mkdir()
        data={
            "docs/requirements.md":"CLIENT theory remains product-owned.\n",
            "state/product.json":'{"status":"CURRENT","owner":"external"}\n',
            "state/authority.json":'{"lease":"not-granted-to-starter"}\n',
        }
        for rel,value in data.items():
            (repo/rel).write_text(value,encoding="utf-8")
        (repo/".gitignore").write_text(
            "state/catalog.sqlite-wal\nstate/catalog.sqlite-shm\n",encoding="utf-8")
        sqlite_db=repo/"state"/"catalog.sqlite"
        connection=sqlite3.connect(sqlite_db,isolation_level=None)
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("CREATE TABLE catalog (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
        connection.execute("INSERT INTO catalog(name) VALUES ('copied governed row')")
        assert Path(str(sqlite_db)+"-wal").stat().st_size>0
        sqlite_main_sha=sha(sqlite_db)
        pointer={"database_path":"state/catalog.sqlite","database_sha256":sqlite_main_sha}
        (repo/"state"/"catalog-pointer.json").write_text(json.dumps(pointer)+"\n",encoding="utf-8")
        data["state/catalog-pointer.json"]=json.dumps(pointer)+"\n"
        initial={p:sha(repo/p) for p in data}
        sqlite_snapshot=snapshot_sha256(sqlite_db)
        spec={
            "schema_version":"existing-governed-attachment-v1",
            "mode":"READ_ONLY_REFERENCE",
            "preserve_existing_authority":True,
            "source_writes_allowed":False,
            "external_actions_allowed":False,
            "authority_surfaces":[
                {"concern":c,"source_ref":p,"sha256":initial[p]}
                for c,p in (
                    ("CLIENT_REQUIREMENTS","docs/requirements.md"),
                    ("PRODUCT_STATE","state/product.json"),
                    ("EXECUTION_AUTHORITY","state/authority.json"),
                    ("CANONICAL_CATALOG_POINTER","state/catalog-pointer.json"),
                )
            ],
            "sqlite_currentness":{"source_ref":"state/catalog.sqlite",
                                  "snapshot_sha256":sqlite_snapshot,
                                  "database_sha256":sqlite_main_sha,
                                  "pointer_ref":"state/catalog-pointer.json"},
        }
        result=inspect(repo,spec)
        assert result["status"]=="READ_ONLY_REFERENCES_MATCH_NOT_ATTACHED"
        assert result["may_execute_material_goal"] is False
        assert result["real_attachment_ready"] is False
        assert not (repo/".agentic-sdlc").exists()
        assert initial=={p:sha(repo/p) for p in data}
        (repo/"docs"/"requirements.md").write_text("changed without authority")
        assert "ATTACHMENT_SOURCE_STALE" in inspect(repo,spec)["failure_codes"]
        (repo/"docs"/"requirements.md").write_text(data["docs/requirements.md"])
        for bad in ("../outside","/etc/passwd","C:\\secret","docs/../state/product.json"):
            wrong=json.loads(json.dumps(spec))
            wrong["authority_surfaces"][0]["source_ref"]=bad
            try: inspect(repo,wrong)
            except AttachmentHold: pass
            else: raise AssertionError("ATTACHMENT_PATH_ESCAPE")
        wrong=json.loads(json.dumps(spec))
        wrong["authority_surfaces"][1]["concern"]="CLIENT_REQUIREMENTS"
        try: inspect(repo,wrong)
        except AttachmentHold: pass
        else: raise AssertionError("DUPLICATE_OWNER_ACCEPTED")
        if hasattr(os,"symlink"):
            alias=repo/"docs"/"alias.md"
            try:alias.symlink_to(repo/"state"/"product.json")
            except (OSError,NotImplementedError):pass
            else:
                wrong=json.loads(json.dumps(spec))
                wrong["authority_surfaces"][0]["source_ref"]="docs/alias.md"
                try:inspect(repo,wrong)
                except AttachmentHold:pass
                else:raise AssertionError("SYMLINK_ACCEPTED")
                alias.unlink()
        spec_path=Path(d)/"private-spec.json"
        spec_path.write_text(json.dumps(spec),encoding="utf-8")
        process=subprocess.run(
            [sys.executable,str(ROOT/"tools"/"existing_repo_attachment.py"),
             "--project-root",str(repo),"--manifest",str(spec_path)],
            capture_output=True,text=True,check=False)
        assert process.returncode==0,process.stdout+process.stderr
        assert "READ_ONLY_REFERENCES_MATCH_NOT_ATTACHED" in process.stdout
        assert "established" not in process.stdout
        assert initial=={p:sha(repo/p) for p in data}
        assert not (repo/".agentic-sdlc").exists()

        # Existing governed-project attachment writes only a distinct local
        # reference receipt into an already present, Git-ignored runtime.
        runtime=repo/".agentic-sdlc"/"runtime"
        runtime.mkdir(parents=True)
        (runtime/".gitignore").write_text(
            "EXISTING_PROJECT_ATTACHMENT_CURRENT.json\n",encoding="utf-8")
        subprocess.run(["git","-C",str(repo),"init","-b","main"],capture_output=True,check=True)
        subprocess.run(["git","-C",str(repo),"config","user.name","Attachment Test"],check=True)
        subprocess.run(["git","-C",str(repo),"config","user.email","example.invalid"],check=True)
        subprocess.run(["git","-C",str(repo),"add","docs","state",".gitignore",
                        ".agentic-sdlc/runtime/.gitignore"],check=True)
        subprocess.run(["git","-C",str(repo),"commit","-m","existing governed fixture"],capture_output=True,check=True)
        attached=subprocess.run(
            [sys.executable,str(ROOT/"tools"/"existing_repo_attachment.py"),
             "--project-root",str(repo),"--manifest",str(spec_path),"--attach-read-only"],
            capture_output=True,text=True,check=False)
        assert attached.returncode==0,attached.stdout+attached.stderr
        attached_result=json.loads(attached.stdout)
        assert attached_result["status"]=="ATTACHED_READ_ONLY_CURRENT"
        receipt=runtime/"EXISTING_PROJECT_ATTACHMENT_CURRENT.json"
        receipt_bytes=receipt.read_bytes()
        record=json.loads(receipt_bytes)
        assert record["additional_product_state_created"] is False
        assert record["additional_planner_or_i3_created"] is False
        assert record["may_execute_material_goal"] is False
        assert initial=={p:sha(repo/p) for p in data}
        status=subprocess.run(["git","-C",str(repo),"status","--porcelain","--untracked-files=all"],
                              capture_output=True,check=True).stdout
        assert status==b""
        repeated=subprocess.run(
            [sys.executable,str(ROOT/"tools"/"existing_repo_attachment.py"),
             "--project-root",str(repo),"--manifest",str(spec_path),"--attach-read-only"],
            capture_output=True,text=True,check=False)
        assert repeated.returncode==0 and json.loads(repeated.stdout)["status"]=="ATTACHED_READ_ONLY_CURRENT"
        assert receipt.read_bytes()==receipt_bytes
        rollback_image=Path(d)/"attachment-rollback-image.json"
        detached=subprocess.run(
            [sys.executable,str(ROOT/"tools"/"existing_repo_attachment.py"),
             "--project-root",str(repo),"--manifest",str(spec_path),"--detach-read-only",
             "--expected-receipt-sha256",attached_result["receipt_sha256"],
             "--rollback-image-out",str(rollback_image)],
            capture_output=True,text=True,check=False)
        assert detached.returncode==0,detached.stdout+detached.stderr
        detached_result=json.loads(detached.stdout)
        assert detached_result["status"]=="DETACHED_READ_ONLY_ROLLBACK"
        assert detached_result["receipt_absent_readback"] is True
        assert not receipt.exists()
        image=json.loads(rollback_image.read_text(encoding="utf-8"))
        assert image["receipt_sha256"]==attached_result["receipt_sha256"]
        assert image["product_state_mutated"] is False
        assert initial=={p:sha(repo/p) for p in data}
        status=subprocess.run(["git","-C",str(repo),"status","--porcelain","--untracked-files=all"],
                              capture_output=True,check=True).stdout
        assert status==b""
        connection.execute("INSERT INTO catalog(name) VALUES ('committed WAL change')")
        assert sha(sqlite_db)==sqlite_main_sha  # main-file bytes remain a file-only blind spot
        wal_hold=inspect(repo,spec)
        assert wal_hold["status"]=="HOLD"
        assert "SQLITE_CURRENTNESS_STALE" in wal_hold["failure_codes"]
        (repo/"docs"/"requirements.md").write_text("stale after attachment\n",encoding="utf-8")
        stale_attach=subprocess.run(
            [sys.executable,str(ROOT/"tools"/"existing_repo_attachment.py"),
             "--project-root",str(repo),"--manifest",str(spec_path),"--attach-read-only"],
            capture_output=True,text=True,check=False)
        assert stale_attach.returncode==2
        assert json.loads(stale_attach.stdout)["status"]=="HOLD"
        assert not receipt.exists()
        assert initial["state/product.json"]==sha(repo/"state/product.json")
        connection.close()
    print("ATTACHMENT READ-ONLY PREFLIGHT PASSED")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
