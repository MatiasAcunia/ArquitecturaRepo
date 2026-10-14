#!/usr/bin/env python3
"""Read-only attachment preflight for an already governed repository.

Never installs a second Product State, OWNER, Planner, campaign or task.
Local source-file integrity is not an independent execution authorization.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
import uuid
import re
from pathlib import Path
from typing import Any
from sqlite_currentness import SQLiteCurrentnessHold, snapshot_sha256

SCHEMA="existing-governed-attachment-v1"
HASH=re.compile(r"^[0-9a-f]{64}$")
CONCERN=re.compile(r"^[A-Z][A-Z0-9_]{2,63}$")
MAX_SIZE=32*1024*1024
ATTACHMENT_RECEIPT="EXISTING_PROJECT_ATTACHMENT_CURRENT.json"

class AttachmentHold(ValueError):
    pass

def source_ref(root:Path, relative:str)->Path:
    if (not isinstance(relative,str) or not 0<len(relative)<=512
        or "\\" in relative or ":" in relative or "\x00" in relative
        or relative.startswith("/")
        or any(x in {"",".",".."} for x in relative.split("/"))):
        raise AttachmentHold("UNSAFE_ATTACHMENT_PATH")
    current=root.resolve()
    for part in relative.split("/"):
        current=current/part
        if current.is_symlink():
            raise AttachmentHold("ATTACHMENT_SYMLINK_REFUSED")
    if not current.resolve().is_relative_to(root.resolve()):
        raise AttachmentHold("ATTACHMENT_PATH_OUTSIDE_SOURCE")
    return current

def digest_file(path:Path)->str:
    if not path.is_file() or path.stat().st_size>MAX_SIZE:
        raise AttachmentHold("REQUIRED_ATTACHMENT_SOURCE_MISSING_OR_OVERSIZE")
    digest=hashlib.sha256()
    with path.open("rb") as reader:
        for blob in iter(lambda:reader.read(1048576),b""):
            digest.update(blob)
    return digest.hexdigest()

def inspect(root:Path,spec:dict[str,Any])->dict[str,Any]:
    if root.is_symlink() or not root.is_dir():
        raise AttachmentHold("UNTRUSTED_EXISTING_PROJECT_ROOT")
    fields={"schema_version","mode","preserve_existing_authority","source_writes_allowed",
            "external_actions_allowed","authority_surfaces"}
    if not isinstance(spec,dict) or frozenset(spec) not in {frozenset(fields),frozenset(fields|{"sqlite_currentness"})}:
        raise AttachmentHold("INVALID_ATTACHMENT_MANIFEST")
    if (spec["schema_version"]!=SCHEMA or spec["mode"]!="READ_ONLY_REFERENCE"
        or spec["preserve_existing_authority"] is not True
        or spec["source_writes_allowed"] is not False
        or spec["external_actions_allowed"] is not False):
        raise AttachmentHold("ATTACHMENT_PRIVILEGE_OR_SCOPE_INVALID")
    entries=spec["authority_surfaces"]
    if not isinstance(entries,list) or not 2<=len(entries)<=64:
        raise AttachmentHold("INVALID_ATTACHMENT_OWNER_MAP")
    concerns=set()
    paths=set()
    failures=set()
    for entry in entries:
        if not isinstance(entry,dict) or set(entry)!={"concern","source_ref","sha256"}:
            raise AttachmentHold("INVALID_ATTACHMENT_ENTRY")
        concern,ref,sha=entry["concern"],entry["source_ref"],entry["sha256"]
        if not isinstance(concern,str) or not CONCERN.fullmatch(concern) or concern in concerns:
            raise AttachmentHold("DUPLICATE_OR_INVALID_CANONICAL_OWNER")
        if not isinstance(sha,str) or not HASH.fullmatch(sha):
            raise AttachmentHold("INVALID_ATTACHMENT_DIGEST")
        if ref in paths:
            raise AttachmentHold("DUPLICATED_ATTACHMENT_SOURCE")
        concerns.add(concern)
        paths.add(ref)
        p=source_ref(root,ref)
        try:
            if digest_file(p)!=sha:
                failures.add("ATTACHMENT_SOURCE_STALE")
        except (OSError,AttachmentHold):
            failures.add("ATTACHMENT_SOURCE_MISSING_OR_UNREADABLE")
    if not {"CLIENT_REQUIREMENTS","PRODUCT_STATE"}.issubset(concerns):
        failures.add("CANONICAL_OWNER_MAP_INCOMPLETE")
    sqlite_binding=None
    if "sqlite_currentness" in spec:
        sqlite_binding=spec["sqlite_currentness"]
        if (not isinstance(sqlite_binding,dict) or set(sqlite_binding)!={"source_ref","snapshot_sha256","database_sha256","pointer_ref"}
            or not isinstance(sqlite_binding.get("source_ref"),str)
            or not isinstance(sqlite_binding.get("pointer_ref"),str)
            or (sqlite_binding.get("snapshot_sha256") is not None and
                (not isinstance(sqlite_binding.get("snapshot_sha256"),str) or
                 not HASH.fullmatch(sqlite_binding["snapshot_sha256"])))
            or not isinstance(sqlite_binding.get("database_sha256"),str)
            or not HASH.fullmatch(sqlite_binding["database_sha256"])):
            failures.add("SQLITE_CURRENTNESS_MANIFEST_INVALID")
        else:
            try:
                db=source_ref(root,sqlite_binding["source_ref"])
                pointer_path=source_ref(root,sqlite_binding["pointer_ref"])
                pointer=json.loads(pointer_path.read_text(encoding="utf-8"))
                if (not isinstance(pointer,dict) or
                    pointer.get("database_sha256")!=sqlite_binding["database_sha256"] or
                    Path(str(pointer.get("database_path",""))).name!=Path(sqlite_binding["source_ref"]).name):
                    failures.add("SQLITE_POINTER_DIGEST_MISMATCH")
                if digest_file(db)!=sqlite_binding["database_sha256"]:
                    failures.add("SQLITE_MAIN_FILE_STALE")
                if sqlite_binding["snapshot_sha256"] is None:
                    failures.add("SQLITE_CONSISTENT_SNAPSHOT_REQUIRED")
                elif snapshot_sha256(db)!=sqlite_binding["snapshot_sha256"]:
                    failures.add("SQLITE_CURRENTNESS_STALE")
            except (SQLiteCurrentnessHold,OSError,AttachmentHold,ValueError,TypeError):
                failures.add("SQLITE_CURRENTNESS_UNVERIFIABLE")
    return {
        "schema_version":"existing-governed-attachment-check-v1",
        "status":"HOLD" if failures else "READ_ONLY_REFERENCES_MATCH_NOT_ATTACHED",
        "failure_codes":sorted(failures),
        "source_write_authorized":False,
        "additional_product_state_created":False,
        "may_execute_material_goal":False,
        "live_upstream_owner_verified":False,
        "real_attachment_ready":False,
        "sqlite_snapshot_sha256":sqlite_binding.get("snapshot_sha256") if isinstance(sqlite_binding,dict) else None,
        "remaining_gates":[
            "UPSTREAM_IDENTITY_AND_AUTHORITY",
            "HOST_INVOCATION_AND_FENCING",
            "LIVE_DB_ARTIFACT_CURRENTNESS",
            "INDEPENDENT_EXISTING_PROJECT_TRANSFER",
        ]
    }

def git_snapshot(root:Path)->dict[str,Any]:
    def run(*args:str)->subprocess.CompletedProcess[bytes]:
        try:
            return subprocess.run(["git","-C",str(root),*args],capture_output=True,
                                  text=False,check=False,timeout=15)
        except (OSError,subprocess.TimeoutExpired):
            raise AttachmentHold("ATTACHMENT_GIT_READBACK_FAILED") from None
    top=run("rev-parse","--show-cdup")
    if top.returncode or top.stdout.strip():
        raise AttachmentHold("ATTACHMENT_REQUIRES_EXACT_GIT_ROOT")
    head=run("rev-parse","--verify","HEAD")
    if head.returncode:
        raise AttachmentHold("ATTACHMENT_GIT_HEAD_UNVERIFIED")
    revision=head.stdout.decode("ascii",errors="strict").strip()
    if not re.fullmatch(r"[0-9a-f]{40,64}",revision):
        raise AttachmentHold("ATTACHMENT_GIT_HEAD_UNVERIFIED")
    status=run("-c","status.renames=false","status","--porcelain=v1","-z","--untracked-files=all")
    if status.returncode or len(status.stdout)>2_000_000:
        raise AttachmentHold("ATTACHMENT_GIT_STATUS_UNVERIFIABLE")
    records=status.stdout.split(b"\0")
    if records and records[-1]==b"": records.pop()
    if len(records)>5000: raise AttachmentHold("ATTACHMENT_GIT_STATUS_BUDGET_EXCEEDED")
    changed=[]
    for record in records:
        if len(record)<4 or record[2:3]!=b" ": raise AttachmentHold("ATTACHMENT_GIT_STATUS_INVALID")
        changed.append({"status":record[:2].decode("ascii",errors="strict"),
                        "path_sha256":hashlib.sha256(record[3:]).hexdigest()})
    return {"head":revision,"changed":changed}

def attach_read_only(root:Path,spec:dict[str,Any],control_dir:str=".agentic-sdlc")->dict[str,Any]:
    preflight=inspect(root,spec)
    if preflight["status"]!="READ_ONLY_REFERENCES_MATCH_NOT_ATTACHED":
        raise AttachmentHold("ATTACHMENT_AUTHORITY_MAP_STALE_OR_INCOMPLETE")
    if not isinstance(control_dir,str) or not re.fullmatch(r"[A-Za-z0-9_.-]{1,80}",control_dir) or control_dir in {".","..",".git"}:
        raise AttachmentHold("UNTRUSTED_ATTACHMENT_CONTROL_DIR")
    root=root.resolve()
    control=root/control_dir
    runtime=control/"runtime"
    for path in (control,runtime):
        if path.is_symlink(): raise AttachmentHold("ATTACHMENT_CONTROL_SYMLINK_REFUSED")
    if not control.is_dir() or not runtime.is_dir():
        raise AttachmentHold("EXISTING_CONTROL_RUNTIME_REQUIRED")
    receipt=runtime/ATTACHMENT_RECEIPT
    relative_receipt=receipt.relative_to(root).as_posix()
    ignored=subprocess.run(["git","-C",str(root),"check-ignore","-q","--",relative_receipt],
                           capture_output=True,check=False,timeout=15)
    if ignored.returncode:
        raise AttachmentHold("ATTACHMENT_RECEIPT_WOULD_POLLUTE_GIT")
    owners={item["concern"]:item["source_ref"] for item in spec["authority_surfaces"]}
    bindings=[{"concern":item["concern"],"source_ref":item["source_ref"],"sha256":item["sha256"]}
              for item in spec["authority_surfaces"]]
    git=git_snapshot(root)
    sqlite_receipt=spec.get("sqlite_currentness")
    if sqlite_receipt is not None:
        sqlite_receipt={key:sqlite_receipt[key] for key in
                        ("source_ref","snapshot_sha256","database_sha256","pointer_ref")}
    manifest_sha=hashlib.sha256(json.dumps(spec,sort_keys=True,separators=(",",":"),
                                            ensure_ascii=False).encode("utf-8")).hexdigest()
    if receipt.exists():
        if receipt.is_symlink() or not receipt.is_file() or receipt.stat().st_size>MAX_SIZE:
            raise AttachmentHold("EXISTING_ATTACHMENT_RECEIPT_UNTRUSTED")
        try: existing=json.loads(receipt.read_text(encoding="utf-8"))
        except (OSError,UnicodeError,json.JSONDecodeError): raise AttachmentHold("EXISTING_ATTACHMENT_RECEIPT_CORRUPT") from None
        if (not isinstance(existing,dict) or existing.get("schema_version")!="operational-existing-project-attachment-v1"
            or existing.get("manifest_sha256")!=manifest_sha or existing.get("authority_surfaces")!=bindings
            or existing.get("sqlite_currentness")!=sqlite_receipt):
            raise AttachmentHold("EXISTING_ATTACHMENT_CONFLICT_REQUIRES_REVIEW")
        if existing.get("git_binding")!=git:
            raise AttachmentHold("EXISTING_ATTACHMENT_GIT_BINDING_STALE")
        return {"status":"ATTACHED_READ_ONLY_CURRENT","receipt_ref":relative_receipt,
                "receipt_sha256":hashlib.sha256(receipt.read_bytes()).hexdigest(),
                "source_write_authorized":False,"additional_product_state_created":False,
                "may_execute_material_goal":False,"native_host_enforcement":"UNVERIFIED"}
    record={
        "schema_version":"operational-existing-project-attachment-v1",
        "attachment_id":uuid.uuid4().hex,
        "created_at":dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),
        "manifest_sha256":manifest_sha,
        "authority_surfaces":bindings,
        "canonical_product_state_ref":owners["PRODUCT_STATE"],
        "sqlite_currentness":sqlite_receipt,
        "git_binding":git,
        "status":"ATTACHED_READ_ONLY_CURRENT",
        "source_write_authorized":False,
        "external_actions_authorized":False,
        "additional_product_state_created":False,
        "additional_planner_or_i3_created":False,
        "may_execute_material_goal":False,
        "capabilities":["persistent canonical-owner reference map","read-only source digest check"],
        "unsupported":["host invocation fencing","material Goal execution","canonical DB mutation","SQLite WAL acceptance","provider or publication actions"],
    }
    body=(json.dumps(record,sort_keys=True,indent=2)+"\n").encode("utf-8")
    try:
        fd=os.open(receipt,os.O_CREAT|os.O_EXCL|os.O_WRONLY|getattr(os,"O_NOFOLLOW",0),0o600)
        with os.fdopen(fd,"wb") as handle:
            handle.write(body);handle.flush();os.fsync(handle.fileno())
    except FileExistsError:
        raise AttachmentHold("ATTACHMENT_RECEIPT_RACE_REQUIRES_READBACK") from None
    readback=json.loads(receipt.read_text(encoding="utf-8"))
    after=inspect(root,spec)
    if readback!=record or after["status"]!="READ_ONLY_REFERENCES_MATCH_NOT_ATTACHED" or git_snapshot(root)!=git:
        raise AttachmentHold("ATTACHMENT_POSTWRITE_SOURCE_OR_GIT_READBACK_FAILED")
    return {"status":"ATTACHED_READ_ONLY_CURRENT","receipt_ref":relative_receipt,
            "receipt_sha256":hashlib.sha256(body).hexdigest(),
            "source_write_authorized":False,"additional_product_state_created":False,
            "may_execute_material_goal":False,"native_host_enforcement":"UNVERIFIED",
            "authority_surface_count":len(bindings),"git_head":git["head"]}

def detach_read_only(root:Path,expected_sha256:str,rollback_image:Path,
                     control_dir:str=".agentic-sdlc")->dict[str,Any]:
    if not HASH.fullmatch(expected_sha256): raise AttachmentHold("EXPECTED_ATTACHMENT_DIGEST_INVALID")
    if root.is_symlink() or not root.is_dir(): raise AttachmentHold("UNTRUSTED_EXISTING_PROJECT_ROOT")
    root=root.resolve()
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,80}",control_dir) or control_dir in {".","..",".git"}:
        raise AttachmentHold("UNTRUSTED_ATTACHMENT_CONTROL_DIR")
    receipt=root/control_dir/"runtime"/ATTACHMENT_RECEIPT
    if receipt.is_symlink() or not receipt.is_file() or receipt.stat().st_size>MAX_SIZE:
        raise AttachmentHold("ATTACHMENT_RECEIPT_MISSING_OR_UNTRUSTED")
    raw=receipt.read_bytes()
    actual=hashlib.sha256(raw).hexdigest()
    if actual!=expected_sha256: raise AttachmentHold("ATTACHMENT_RECEIPT_IDENTITY_STALE")
    try: record=json.loads(raw.decode("utf-8"))
    except (UnicodeError,json.JSONDecodeError): raise AttachmentHold("ATTACHMENT_RECEIPT_CORRUPT") from None
    if (not isinstance(record,dict) or record.get("schema_version")!="operational-existing-project-attachment-v1"
        or record.get("source_write_authorized") is not False
        or record.get("additional_product_state_created") is not False
        or record.get("may_execute_material_goal") is not False):
        raise AttachmentHold("ATTACHMENT_RECEIPT_SCOPE_UNTRUSTED")
    source_readback=[]
    for binding in record.get("authority_surfaces",[]):
        path=source_ref(root,binding["source_ref"])
        digest=digest_file(path)
        source_readback.append({"concern":binding["concern"],"sha256":digest,
                                "matches_attachment":digest==binding["sha256"]})
    sqlite_binding=record.get("sqlite_currentness")
    if sqlite_binding is not None:
        db=source_ref(root,sqlite_binding["source_ref"])
        current_snapshot=snapshot_sha256(db)
        source_readback.append({"concern":"SQLITE_CURRENTNESS","sha256":current_snapshot,
                                "matches_attachment":current_snapshot==sqlite_binding["snapshot_sha256"]})
    output=Path(rollback_image).absolute()
    try: output.relative_to(root)
    except ValueError: pass
    else: raise AttachmentHold("ROLLBACK_IMAGE_MUST_BE_OUTSIDE_SOURCE_REPO")
    before_git=git_snapshot(root)
    image={"schema_version":"existing-project-attachment-rollback-image-v1",
           "status":"DETACH_ROLLBACK_IMAGE","receipt_sha256":actual,
           "receipt":record,"source_readback":source_readback,
           "git_binding_before":before_git,
           "source_files_mutated":False,"product_state_mutated":False}
    body=(json.dumps(image,sort_keys=True,indent=2)+"\n").encode("utf-8")
    try:
        fd=os.open(output,os.O_CREAT|os.O_EXCL|os.O_WRONLY|getattr(os,"O_NOFOLLOW",0),0o600)
        with os.fdopen(fd,"wb") as handle:
            handle.write(body);handle.flush();os.fsync(handle.fileno())
    except FileExistsError:
        raise AttachmentHold("ROLLBACK_IMAGE_OUTPUT_PREEXISTS") from None
    before_stat=receipt.stat()
    if hashlib.sha256(receipt.read_bytes()).hexdigest()!=expected_sha256:
        raise AttachmentHold("ATTACHMENT_RECEIPT_CHANGED_BEFORE_DETACH")
    if (receipt.stat().st_dev,receipt.stat().st_ino)!=(before_stat.st_dev,before_stat.st_ino):
        raise AttachmentHold("ATTACHMENT_RECEIPT_FILE_IDENTITY_CHANGED")
    receipt.unlink()
    if receipt.exists() or receipt.is_symlink(): raise AttachmentHold("ATTACHMENT_DETACH_READBACK_FAILED")
    after_git=git_snapshot(root)
    if after_git!=before_git: raise AttachmentHold("ATTACHMENT_DETACH_CHANGED_GIT_SOURCE")
    return {"status":"DETACHED_READ_ONLY_ROLLBACK","receipt_sha256":actual,
            "rollback_image_ref":str(output),"rollback_image_sha256":hashlib.sha256(body).hexdigest(),
            "receipt_absent_readback":True,"git_binding_unchanged":True,
            "source_files_mutated":False,"product_state_mutated":False,
            "canonical_source_surfaces":source_readback}

def main()->int:
    p=argparse.ArgumentParser(description="Noninvasive governed-repository reference check")
    p.add_argument("--project-root",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True)
    mode=p.add_mutually_exclusive_group()
    mode.add_argument("--attach-read-only",action="store_true",
                      help="Persist a minimal read-only attachment receipt in an existing ignored runtime")
    mode.add_argument("--detach-read-only",action="store_true",
                      help="Remove only the exact adapter receipt after saving a rollback image")
    p.add_argument("--control-dir",default=".agentic-sdlc")
    p.add_argument("--expected-receipt-sha256")
    p.add_argument("--rollback-image-out",type=Path)
    a=p.parse_args()
    try:
        if a.manifest.stat().st_size>128*1024:
            raise AttachmentHold("ATTACHMENT_MANIFEST_TOO_LARGE")
        if a.detach_read_only:
            if not a.expected_receipt_sha256 or not a.rollback_image_out:
                raise AttachmentHold("EXPLICIT_RECEIPT_DIGEST_AND_ROLLBACK_IMAGE_REQUIRED")
            result=detach_read_only(a.project_root,a.expected_receipt_sha256,
                                    a.rollback_image_out,a.control_dir)
        else:
            spec=json.loads(a.manifest.read_text(encoding="utf-8"))
            result=(attach_read_only(a.project_root,spec,a.control_dir) if a.attach_read_only
                    else inspect(a.project_root,spec))
    except (AttachmentHold,OSError,ValueError,TypeError) as exc:
        code=str(exc) if isinstance(exc,AttachmentHold) else "ATTACHMENT_INPUT_INVALID"
        result={"status":"HOLD","failure_codes":[code],"may_execute_material_goal":False}
    print(json.dumps(result,indent=2))
    return 0 if result["status"] in {"READ_ONLY_REFERENCES_MATCH_NOT_ATTACHED","ATTACHED_READ_ONLY_CURRENT","DETACHED_READ_ONLY_ROLLBACK"} else 2

if __name__=="__main__":
    raise SystemExit(main())
