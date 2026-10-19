"""Read Gemini API authentication from an explicitly selected local file.

Never print, persist, rotate or upload the key. Authentication does NOT prove
free-tier eligibility or authorize private source export/provider calls.
"""
from __future__ import annotations

import os
import re
from pathlib import Path


class GeminiCredentialHold(ValueError):
    pass


def resolve_key() -> str:
    direct = os.environ.get("GEMINI_API_KEY", "").strip()
    if direct:
        return direct
    chosen = os.environ.get("AGENTIC_GEMINI_API_KEY_FILE", "").strip()
    directory = os.environ.get("AGENTIC_GEMINI_KEY_DIRECTORY", "").strip()
    if chosen:
        candidate = Path(chosen).expanduser()
    elif directory:
        root = Path(directory).expanduser()
        if not root.is_dir() or root.is_symlink():
            raise GeminiCredentialHold("GEMINI_LOCAL_KEY_DIRECTORY_INVALID")
        # User described local desktop text files named gemini<number>.txt.
        # Never iterate keys across projects or quotas: one actual selected
        # identity must be configured explicitly when multiple files exist.
        files = sorted(x for x in root.iterdir() if x.is_file() and not x.is_symlink()
                       and re.fullmatch(r"gemini[0-9]+\.txt", x.name))
        if len(files) != 1:
            raise GeminiCredentialHold("GEMINI_KEY_FILE_SELECTION_REQUIRED")
        candidate = files[0]
    else:
        raise GeminiCredentialHold("GEMINI_API_KEY_NOT_CONFIGURED")
    if (not candidate.is_file() or candidate.is_symlink()
        or not re.fullmatch(r"gemini[0-9]*\.txt", candidate.name)
        or candidate.stat().st_size > 1024):
        raise GeminiCredentialHold("GEMINI_KEY_FILE_INVALID")
    raw = candidate.read_text(encoding="utf-8-sig").strip()
    if raw.startswith("GEMINI_API_KEY="):
        raw = raw.split("=", 1)[1].strip().strip('"').strip("'")
    if not re.fullmatch(r"[A-Za-z0-9_-]{20,256}", raw):
        raise GeminiCredentialHold("GEMINI_KEY_FILE_CONTENT_INVALID")
    return raw
