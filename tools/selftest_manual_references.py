#!/usr/bin/env python3
"""Audit every local Markdown reference in the user-facing manual collection.

This validates the historical Spanish handbook, all available complete v1.4
handbooks, eight introductory guides and FAQs, and both navigation indexes.
Remote websites are outside this offline audit; first-party main-branch blob
references are resolved against the corresponding local source paths.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\((?P<target>[^)]+)\)")
FIRST_PARTY_BLOB = "https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/"


def sources() -> list[Path]:
    collection = [ROOT / "README.md", DOCS / "README.md"]
    collection.extend((DOCS / "manual").rglob("*.md"))
    collection.extend((DOCS / "i18n").rglob("*.md"))
    return sorted(set(collection))


def resolve(source: Path, raw: str) -> tuple[Path | None, str]:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    target = target.split(" #", 1)[0].split(' "', 1)[0]
    if target.startswith(("mailto:", "#", "data:")):
        return None, "skipped"
    if target.startswith(FIRST_PARTY_BLOB):
        uri = urlparse(target)
        return ROOT / unquote(uri.path.split("/blob/main/", 1)[1]), "repo-main"
    parsed = urlparse(target)
    if parsed.scheme or parsed.netloc:
        return None, "external"
    local = unquote(parsed.path)
    if not local:
        return None, "same-file"
    return (source.parent / local).resolve(), "relative"


def main() -> int:
    broken = []
    checked = 0
    files = sources()
    for source in files:
        content = source.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(content):
            target = match.group("target")
            resolved, kind = resolve(source, target)
            if resolved is None:
                continue
            checked += 1
            if not resolved.is_relative_to(ROOT) or not resolved.is_file():
                broken.append((source.relative_to(ROOT), target, kind))
    for source, target, kind in broken:
        print(f"BROKEN {kind}: {source} -> {target}")
    print(f"Manual reference audit: {len(files)} Markdown files, {checked} source-bound references, {len(broken)} broken")
    if broken:
        return 1
    print("PASS: historical and long-form manuals, mini guides, FAQs, and indexes have no broken local references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
