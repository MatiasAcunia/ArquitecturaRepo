"""L2 source-complete SIP ZIP and two-ZIP fresh-context preflight.
No product-state writes or provider calls. Entirely optional public-template tool.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

MAX_TOTAL = 32 * 1024 * 1024
MAX_FILE = 3 * 1024 * 1024
MANDATORY = {"goal_id","project","head_sha","charter_ref","engine_ids",
             "first_l4_work_order","bootstrap_text","files","cycles_proposed",
             "authority_refs","currentness_refs","gates","unknowns"}

class PacketHold(ValueError):
    pass

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def safe_path(value: str) -> str:
    if not isinstance(value,str) or not value or len(value)>350 or "\\" in value:
        raise PacketHold("UNSAFE_SOURCE_PATH")
    p=Path(value)
    if p.is_absolute() or any(x in {"..",".",""} for x in p.parts):
        raise PacketHold("UNSAFE_SOURCE_PATH")
    lower=p.name.lower()
    if (lower.startswith(".env") or re.fullmatch(r"gemini\d*\.txt",lower)
        or any(s in lower for s in ("credential","secret","password","private_key",".pem",".p12",".key"))
        or p.parts[0] in {".git",".agentic-sdlc"}):
        raise PacketHold("SECRET_OR_RUNTIME_PATH_NOT_PACKAGED")
    return p.as_posix()

def git(root: Path,*args: str) -> str:
    p=subprocess.run(["git","-C",str(root),*args],capture_output=True,text=True,timeout=20,check=False)
    if p.returncode: raise PacketHold("SOURCE_GIT_READBACK_FAILED")
    return p.stdout.strip()

def validate_spec(spec: dict) -> None:
    if not isinstance(spec,dict) or MANDATORY-set(spec):
        raise PacketHold("MISSING_ENGINEERING_SIP_FIELDS")
    if not isinstance(spec["files"],list) or not spec["files"]:
        raise PacketHold("BOOTSTRAP_SOURCE_FILES_REQUIRED")
    if not isinstance(spec["first_l4_work_order"],dict) or not spec["first_l4_work_order"]:
        raise PacketHold("INITIAL_L4_EXECUTABLE_ORDER_REQUIRED")
    if not isinstance(spec["bootstrap_text"],str) or len(spec["bootstrap_text"])<80:
        raise PacketHold("BOOTSTRAP_TOO_SHORT")
    for k in ("authority_refs","currentness_refs","engine_ids","gates","cycles_proposed"):
        if not isinstance(spec[k],list) or not spec[k]:
            raise PacketHold("EMPTY_REQUIRED_SIP_LIST:"+k)
    if not isinstance(spec["unknowns"],list):
        raise PacketHold("UNKNOWN_LIST_MUST_BE_EXPLICIT")

def build(root: Path,spec: dict,destination: Path) -> dict:
    root=Path(root).resolve(strict=True)
    validate_spec(spec)
    head=git(root,"rev-parse","HEAD")
    if spec["head_sha"]!=head: raise PacketHold("STALE_SIP_SOURCE_HEAD")
    contents={}
    total=0
    for path in sorted(set(map(safe_path,spec["files"]))):
        target=root/path
        if not target.is_file() or target.is_symlink() or not target.resolve().is_relative_to(root):
            raise PacketHold("MISSING_OR_UNSAFE_BOOTSTRAP_FILE:"+path)
        data=target.read_bytes()
        total+=len(data)
        if len(data)>MAX_FILE or total>MAX_TOTAL:
            raise PacketHold("SOURCE_BOOTSTRAP_TOO_LARGE_USE_IMMUTABLE_REF")
        contents["FILES/"+path]=data
    if git(root,"status","--porcelain=v1","-uall"):
        raise PacketHold("DIRTY_WORKTREE_SOURCE_NOT_HEAD_ATTESTED")
    manifest={"schema":"l2-source-complete-sip-v1","goal_id":spec["goal_id"],
              "project":spec["project"],"head_sha":head,
              "files":{k:digest(v) for k,v in sorted(contents.items())},
              "source_files_total":total,"first_l4_order_present":True,
              "prior_goal_progress":spec.get("prior_goal_progress","ABSENT_FIRST_GOAL_OR_UNVERIFIED"),
              "source_of_truth":"EXACT_SNAPSHOT_NOT_PRODUCT_STATE"}
    contents.update({"SIP.json":json.dumps(spec,indent=2,sort_keys=True).encode(),
                     "MANIFEST.json":json.dumps(manifest,indent=2,sort_keys=True).encode(),
                     "BOOTSTRAP.md":spec["bootstrap_text"].encode()})
    contents["SHA256SUMS.json"]=json.dumps({k:digest(v) for k,v in sorted(contents.items())},
                                         sort_keys=True).encode()
    destination=Path(destination).resolve()
    destination.parent.mkdir(parents=True,exist_ok=True)
    if destination.exists(): raise PacketHold("IMMUTABLE_SIP_ALREADY_EXISTS")
    fd,tmp=tempfile.mkstemp(dir=destination.parent,prefix=".sip-",suffix=".zip")
    os.close(fd)
    try:
        with zipfile.ZipFile(tmp,"w",zipfile.ZIP_DEFLATED) as z:
            for name,data in sorted(contents.items()): z.writestr(name,data)
        verify(Path(tmp))
        os.replace(tmp,destination)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
    return {"sha256":digest(destination.read_bytes()),"files":len(manifest["files"]),
            "path":str(destination),"head":head}

def verify(path: Path) -> dict:
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        if (len(set(names))!=len(names) or len(names)>2000
            or sum(i.file_size for i in z.infolist())>MAX_TOTAL+512000):
            raise PacketHold("UNTRUSTED_ZIP_SIZE_OR_NAMES")
        if any(n.startswith("/") or ".." in Path(n).parts or "\\" in n for n in names):
            raise PacketHold("UNSAFE_ZIP_MEMBER")
        if z.testzip() is not None: raise PacketHold("CORRUPT_SIP_ZIP")
        hashes=json.loads(z.read("SHA256SUMS.json"))
        actual={n:digest(z.read(n)) for n in names if n!="SHA256SUMS.json"}
        if actual!=hashes: raise PacketHold("SIP_SHA256_MISMATCH")
        spec=json.loads(z.read("SIP.json"))
        man=json.loads(z.read("MANIFEST.json"))
        validate_spec(spec)
        if man["head_sha"]!=spec["head_sha"] or man["goal_id"]!=spec["goal_id"]:
            raise PacketHold("SIP_SOURCE_GOAL_MISMATCH")
        sources={n for n in names if n.startswith("FILES/")}
        if set(man["files"])!=sources:
            raise PacketHold("SIP_FILE_INVENTORY_INCOMPLETE")
        return {"verified":True,"goal_id":man["goal_id"],
                "head":man["head_sha"],"files":len(sources)}

def two_zip_preflight(sip: Path,progress: Path|None) -> dict:
    source=verify(sip)
    if progress is None:
        return {"sip":source,"goal_progress":"EXPLICITLY_ABSENT",
                "continuation":"NEW_GOAL_ONLY_OR_HOLD_FOR_PREVIOUS_GOAL"}
    with zipfile.ZipFile(progress) as z:
        if z.testzip() is not None: raise PacketHold("GOAL_PROGRESS_CORRUPT")
        manifest=json.loads(z.read("SHA256_MANIFEST.json"))
        actual={n:digest(z.read(n)) for n in z.namelist() if n!="SHA256_MANIFEST.json"}
        if actual!=manifest["members"]: raise PacketHold("GOAL_PROGRESS_SHA_MISMATCH")
        receipt=json.loads(z.read("EXPORT_RECEIPT.json"))
        if receipt["goal_id"]!=source["goal_id"]:
            raise PacketHold("SIP_AND_GOAL_ID_MISMATCH")
        return {"sip":source,"goal_progress_sha256":digest(progress.read_bytes()),
                "goal_progress_class":receipt["recovery_class"],
                "continuation":"REQUIRES_LIVE_SOURCE_DB_AND_HOST_RECONCILIATION"}

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest="command",required=True)
    b=sub.add_parser("build")
    b.add_argument("--repo",type=Path,required=True)
    b.add_argument("--spec",type=Path,required=True)
    b.add_argument("--output",type=Path,required=True)
    v=sub.add_parser("verify");v.add_argument("--zip",type=Path,required=True)
    t=sub.add_parser("two-zip-preflight");t.add_argument("--sip",type=Path,required=True)
    t.add_argument("--progress",type=Path)
    a=p.parse_args()
    try:
        if a.command=="build": result=build(a.repo,json.loads(a.spec.read_text()),a.output)
        elif a.command=="verify": result=verify(a.zip)
        else: result=two_zip_preflight(a.sip,a.progress)
        print(json.dumps(result,indent=2,sort_keys=True))
        return 0
    except (PacketHold,OSError,json.JSONDecodeError,zipfile.BadZipFile) as e:
        p.exit(2,"HOLD_SIP:"+str(e)+"\n")

if __name__=="__main__":
    raise SystemExit(main())
