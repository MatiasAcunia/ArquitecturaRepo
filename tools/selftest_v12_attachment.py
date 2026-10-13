#!/usr/bin/env python3
"""Attachment must neither duplicate canonical ownership nor touch source."""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from existing_repo_attachment import inspect,AttachmentHold

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
        initial={p:sha(repo/p) for p in data}
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
                )
            ],
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
    print("ATTACHMENT READ-ONLY PREFLIGHT PASSED")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
