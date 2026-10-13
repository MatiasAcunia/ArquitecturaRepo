#!/usr/bin/env python3
"""Read-only attachment preflight for an already governed repository.

Never installs a second Product State, OWNER, Planner, campaign or task.
Local source-file integrity is not an independent execution authorization.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

SCHEMA="existing-governed-attachment-v1"
HASH=re.compile(r"^[0-9a-f]{64}$")
CONCERN=re.compile(r"^[A-Z][A-Z0-9_]{2,63}$")
MAX_SIZE=32*1024*1024

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
    if not isinstance(spec,dict) or set(spec)!=fields:
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
    return {
        "schema_version":"existing-governed-attachment-check-v1",
        "status":"HOLD" if failures else "READ_ONLY_REFERENCES_MATCH_NOT_ATTACHED",
        "failure_codes":sorted(failures),
        "source_write_authorized":False,
        "additional_product_state_created":False,
        "may_execute_material_goal":False,
        "live_upstream_owner_verified":False,
        "real_attachment_ready":False,
        "remaining_gates":[
            "UPSTREAM_IDENTITY_AND_AUTHORITY",
            "HOST_INVOCATION_AND_FENCING",
            "LIVE_DB_ARTIFACT_CURRENTNESS",
            "INDEPENDENT_EXISTING_PROJECT_TRANSFER",
        ]
    }

def main()->int:
    p=argparse.ArgumentParser(description="Noninvasive governed-repository reference check")
    p.add_argument("--project-root",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True)
    a=p.parse_args()
    try:
        if a.manifest.stat().st_size>128*1024:
            raise AttachmentHold("ATTACHMENT_MANIFEST_TOO_LARGE")
        result=inspect(a.project_root,json.loads(a.manifest.read_text(encoding="utf-8")))
    except (AttachmentHold,OSError,ValueError,TypeError) as exc:
        code=str(exc) if isinstance(exc,AttachmentHold) else "ATTACHMENT_INPUT_INVALID"
        result={"status":"HOLD","failure_codes":[code],"may_execute_material_goal":False}
    print(json.dumps(result,indent=2))
    return 0 if result["status"]=="READ_ONLY_REFERENCES_MATCH_NOT_ATTACHED" else 2

if __name__=="__main__":
    raise SystemExit(main())
