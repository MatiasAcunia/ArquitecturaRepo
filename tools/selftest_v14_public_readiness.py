#!/usr/bin/env python3
"""Exercise the exact public source archive as a real, offline new adopter.

This is a physical distribution and independent-oracle smoke test. It does not
claim a human usability review, hosted-model permission or release approval.
"""
from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path, PurePosixPath


SOURCE = Path(__file__).resolve().parents[1]
PREFIX = "ArquitecturaRepo-candidate/"
FORBIDDEN_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".sqlite", ".db"}
RETIRED_PRIVATE_DOC_PREFIXES = ("docs/30_", "docs/31_", "docs/33_", "docs/35_", "docs/36_", "docs/37_")


def invoke(*cmd: str | Path, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [str(part) for part in cmd],
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=90,
        check=False,
    )
    return result


def require(result: subprocess.CompletedProcess[str], description: str) -> str:
    if result.returncode != 0:
        raise AssertionError(
            f"{description}: exit={result.returncode}\n"
            f"stdout={result.stdout[-1200:]}\nstderr={result.stderr[-1200:]}"
        )
    return result.stdout


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def enforce_public_path(name: str) -> None:
    if not name.startswith(PREFIX):
        raise AssertionError("archive contains data outside its declared root")
    relative = name[len(PREFIX):]
    if not relative:
        return
    parts = PurePosixPath(relative).parts
    if any(part in {"..", ".git", "__pycache__", ".venv", "venv"} for part in parts):
        raise AssertionError(f"private/generated archive path: {relative}")
    if any(part.lower().startswith(".env") for part in parts):
        raise AssertionError(f"environment-file archive path: {relative}")
    if PurePosixPath(relative).suffix.lower() in FORBIDDEN_SUFFIXES:
        raise AssertionError(f"credential/database archive path: {relative}")
    if relative.startswith(RETIRED_PRIVATE_DOC_PREFIXES):
        raise AssertionError(f"retired internal maintainer document in public ZIP: {relative}")


def test_archive(source_zip: Path) -> tuple[Path, int]:
    require(invoke("git", "-C", SOURCE, "-c", "core.autocrlf=false", "archive", "--format=zip", f"--prefix={PREFIX}", "-o", source_zip, "HEAD"), "git archive")
    # The released object is HEAD, not the platform-dependent checkout index.
    # On Windows autocrlf/configuration may affect working-tree presentation;
    # bind the archive independently to committed Git TREE blob identities.
    committed_tree = require(invoke("git", "-C", SOURCE, "ls-tree", "-r", "HEAD"), "committed source tree")
    tracked_blobs: dict[str, str] = {}
    for entry in committed_tree.splitlines():
        metadata, path = entry.split("\t", 1)
        mode, kind, blob_sha = metadata.split()
        if mode == "120000":
            raise AssertionError("public source distribution contains a tracked symlink")
        if kind != "blob" or mode not in {"100644", "100755"}:
            raise AssertionError(f"unsupported committed Git tree entry in portable distribution: {path}")
        tracked_blobs[path] = blob_sha
    tracked = set(tracked_blobs)
    with zipfile.ZipFile(source_zip) as archive:
        if archive.testzip() is not None:
            raise AssertionError("candidate ZIP failed CRC/readback")
        entries = {name for name in archive.namelist() if not name.endswith("/")}
        for name in archive.namelist():
            enforce_public_path(name)
            entry = archive.getinfo(name)
            if stat.S_IFMT(entry.external_attr >> 16) == stat.S_IFLNK:
                raise AssertionError(f"portable archive contains a symlink: {name}")
        actual = {name.removeprefix(PREFIX) for name in entries}
        if actual != tracked:
            raise AssertionError(
                f"ZIP differs from tracked source: missing={sorted(tracked - actual)[:5]}, "
                f"extra={sorted(actual - tracked)[:5]}"
            )
        for name in sorted(entries):
            payload = archive.read(name)
            raw_header = f"blob {len(payload)}\0".encode("ascii")
            blob_sha = hashlib.sha1(raw_header + payload).hexdigest()
            relative = name.removeprefix(PREFIX)
            if blob_sha != tracked_blobs.get(relative):
                raise AssertionError(
                    f"archive bytes differ from the committed Git HEAD blob: {relative} "
                    f"actual={blob_sha} expected={tracked_blobs.get(relative)} "
                    f"crlf={payload.count(bytes((13, 10)))} lf={payload.count(bytes((10,)))}"
                )
        if source_zip.stat().st_size > 12 * 1024 * 1024:
            raise AssertionError("portable starter unexpectedly exceeds 12 MiB distribution budget")
        extracted = source_zip.parent / "extracted"
        archive.extractall(extracted)
    root = extracted / PREFIX.rstrip("/")
    for required in (
        "README.md", "LICENSE", "VERSION", "state/STARTER_MANIFEST.json",
        "tools/scaffold_project.py", "tools/reconstruct_context.py",
        "tools/validate_project.py", "prompts/INSTALL_THIS_SDLC.md",
    ):
        if not (root / required).is_file():
            raise AssertionError(f"archive missing required runnable public file: {required}")
    if (root / ".git").exists():
        raise AssertionError("portable archive unexpectedly includes a Git checkout")
    return root, len(actual)


def test_first_time_use(extracted: Path, temp: Path) -> None:
    # The new user's project is intentionally unrelated to the starter and
    # includes Unicode/spaces; this also tests Windows path quoting.
    project = temp / "proyecto clínica con espacios"
    application = project / "src" / "saludo.py"
    application.parent.mkdir(parents=True)
    application.write_text("MENSAJE = 'hola'\n", encoding="utf-8")
    workflow = project / ".github" / "workflows" / "test.yml"
    workflow.parent.mkdir(parents=True)
    workflow.write_text("# Work owned by the adopter\n", encoding="utf-8")
    original_code, original_workflow = digest(application), digest(workflow)

    result = invoke(
        sys.executable, extracted / "tools" / "scaffold_project.py",
        "--target", project,
        "--profile", "SMALL",
        "--product-id", "E5_DEMO",
        "--objective", "A small local example; requirements still unconfirmed.",
        "--language", "es",
        "--no-feedback-workflow",
    )
    output = require(result, "ZIP-extracted starter scaffold")
    if "HOLD / UNTRUSTED_CONTEXT" not in output or "external_delivery=NOT_OBSERVED" not in output:
        raise AssertionError("first-time installer implies readiness or silent external telemetry")
    control = project / ".agentic-sdlc"
    if not (control / "state" / "PRODUCT_STATE_CURRENT.json").exists():
        raise AssertionError("scaffold did not create control-layer state")
    if (control / "tools" / "campaignctl.py").exists():
        raise AssertionError("minimal no-provider starter unexpectedly includes optional campaign runtime")
    if (project / ".github" / "workflows" / "agentic-sdlc-feedback.yml").exists():
        raise AssertionError("explicit scheduler opt-out ignored")
    if digest(application) != original_code or digest(workflow) != original_workflow:
        raise AssertionError("starter modified adopter-owned application or workflow")

    status = require(invoke(sys.executable, control / "tools" / "project_status.py", "--control-root", control), "installed status")
    if "BASELINE READY: False" not in status:
        raise AssertionError("unconfirmed product baseline presented as executable")
    discovery = require(invoke(sys.executable, control / "tools" / "discover_project.py", "--project-root", project), "installed discovery")
    inventory = json.loads(discovery)
    paths = {item["path"] for item in inventory["files"]}
    if "src/saludo.py" not in paths or any(p.startswith(".agentic-sdlc/") for p in paths):
        raise AssertionError("inventory crossed application/control-layer boundary")

    validator = invoke(sys.executable, control / "tools" / "validate_project.py", "--root", ".")
    reconstruction = invoke(sys.executable, control / "tools" / "reconstruct_context.py", "--root", control)
    if validator.returncode == 0:
        if "PROJECT VALIDATION PASSED" not in validator.stdout:
            raise AssertionError("installed validator success was not a validation")
        recovered = json.loads(require(reconstruction, "installed fresh-context reconstruction"))
        if recovered["posture"] != "UNTRUSTED_CONTEXT":
            raise AssertionError("no-approval fresh context granted authority")
        if recovered["git_currentness"]["code_ref_relation"] != "NO_GIT_REPOSITORY":
            raise AssertionError("ZIP's independent target invented a source Git repository")
    else:
        if "No module named 'jsonschema'" not in validator.stderr:
            raise AssertionError(f"unexpected validation defect: {validator.stderr[-500:]}")
        if "validation dependency 'jsonschema' is missing" not in reconstruction.stderr:
            raise AssertionError("first-time reconstruction did not explain missing validation dependency")

    again = invoke(
        sys.executable, extracted / "tools" / "scaffold_project.py",
        "--target", project, "--profile", "SMALL", "--product-id", "E5_DEMO",
        "--language", "es", "--no-feedback-workflow",
    )
    if again.returncode == 0 or "EXISTING_CONTROL_PRESERVED" not in again.stderr:
        raise AssertionError("reinstall overwrote a current user control layer")
    if digest(application) != original_code or digest(workflow) != original_workflow:
        raise AssertionError("rejected reinstall still modified adopter-owned bytes")


def test_presentation_and_source() -> None:
    primary = (SOURCE / "README.md").read_text(encoding="utf-8")
    manual = (SOURCE / "docs" / "manual" / "ES" / "README.md").read_text(encoding="utf-8")
    if "# ArquitecturaRepo" not in primary or "#quick-start" not in primary:
        raise AssertionError("public README does not identify the starter and an accessible entrypoint")
    if "https://github.com/ArquitecturaRepo/" in (primary + manual):
        raise AssertionError("public-facing GitHub link omits repository owner")
    for public_link in ("releases/tag/v1.3.0", "releases/download/v1.3.0/", "actions/workflows/publish-ghcr-package.yml"):
        if f"https://github.com/MatiasAcunia/ArquitecturaRepo/{public_link}" not in (primary + manual):
            raise AssertionError(f"missing canonical public release/workflow link: {public_link}")
    if "v1.4 candidate" not in primary or "UNTRUSTED_CONTEXT" not in primary:
        raise AssertionError("README confuses released source with untrusted v1.4 candidate")


def main() -> int:
    started = time.monotonic()
    test_presentation_and_source()
    with tempfile.TemporaryDirectory(prefix="ar-v14-public-package-") as directory:
        work = Path(directory)
        archive = work / "candidate.zip"
        extracted, file_count = test_archive(archive)
        archive_bytes = archive.stat().st_size
        archive_sha256 = digest(archive)
        test_first_time_use(extracted, work)
    print("E5 PUBLIC READINESS / PORTABLE ARCHIVE SELF-TEST PASSED")
    print(f"- git-archive path and Git blob byte parity: {file_count} public tracked files")
    print(f"- ZIP physical CRC and extraction: {archive_bytes} bytes; SHA-256 {archive_sha256}")
    print("- extracted source installed into an existing Unicode/space path with user files preserved")
    print("- status/discovery/reconstruction, no provider runtime, no scheduler, reinstall refusal")
    print("- canonical public links and candidate/released version boundaries")
    print(f"- duration: {time.monotonic() - started:.2f}s (no paid provider calls or release effects)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
