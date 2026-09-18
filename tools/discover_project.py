#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

EXCLUDED_DIRS = {".git", ".agentic-sdlc", "__pycache__", ".venv", "venv", "node_modules"}
MANAGED_FEEDBACK_WORKFLOW = ".github/workflows/agentic-sdlc-feedback.yml"
MANAGED_FEEDBACK_MARKER = "Managed by Agentic SDLC starter"


def is_managed_control_file(project: Path, path: Path) -> bool:
    try:
        relative = str(path.relative_to(project)).replace(os.sep, "/")
    except ValueError:
        return False
    if relative != MANAGED_FEEDBACK_WORKFLOW:
        return False
    try:
        head = path.read_text(encoding="utf-8")[:512]
    except Exception:
        return False
    return MANAGED_FEEDBACK_MARKER in head


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inventory(project: Path) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    for root, dirs, names in os.walk(project):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS)
        root_path = Path(root)
        for name in sorted(names):
            path = root_path / name
            if is_managed_control_file(project, path):
                continue
            try:
                relative = path.relative_to(project)
                stat = path.stat()
            except (OSError, ValueError):
                continue
            files.append(
                {
                    "path": str(relative).replace(os.sep, "/"),
                    "bytes": stat.st_size,
                    "sha256": sha256(path),
                    "suffix": path.suffix.lower(),
                }
            )

    total_bytes = sum(item["bytes"] for item in files)
    top_level = sorted({item["path"].split("/", 1)[0] for item in files})
    return {
        "schema_version": "project-inventory-0.1",
        "project_name": project.name,
        "file_count": len(files),
        "total_bytes": total_bytes,
        "top_level_entries": top_level,
        "files": files,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a deterministic read-only inventory of a target project."
    )
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    project = Path(args.project_root).resolve()
    if not project.is_dir():
        print(f"DISCOVERY FAILED: project root is not a directory: {project}", file=sys.stderr)
        return 1

    data = inventory(project)
    payload = json.dumps(data, indent=2) + "\n"

    if args.output:
        output = Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload, encoding="utf-8")
        print(str(output))
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
