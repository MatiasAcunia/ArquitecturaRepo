#!/usr/bin/env python3
"""Check genuine long-form manual editions, references and locale coverage.

This self-test does not translate or fill missing chapters. Use --require-all
only when all eight full editions are believed to be ready for publication.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from build_long_manual import CHAPTERS, MANUAL_ROOT, ROOT


LOCALES = ("en", "es", "pt", "fr", "de", "it", "ja", "zh")
LINKS = re.compile(r"(?<!!)\]\((?P<url>[^\s)]+)\)")
HEADINGS = re.compile(r"^# 0[0-7] [—–-] .+", re.MULTILINE)


def verify(locale: str) -> tuple[int, int]:
    directory = MANUAL_ROOT / locale
    failures = 0
    words_or_chars = 0
    for i, filename in enumerate(CHAPTERS):
        path = directory / filename
        if not path.is_file():
            print(f"MISSING: {path.relative_to(ROOT)}")
            failures += 1
            continue
        content = path.read_text(encoding="utf-8")
        if not HEADINGS.search(content):
            print(f"BAD CHAPTER HEADING: {path.relative_to(ROOT)}")
            failures += 1
        if locale in ("ja", "zh"):
            length = len(re.sub(r"\s+", "", content))
            minimum = 2900
        else:
            length = len(content.split())
            minimum = 1100
        if length < minimum:
            print(f"TOO SHORT FOR COMPLETE MANUAL: {path.relative_to(ROOT)} ({length} < {minimum})")
            failures += 1
        words_or_chars += length
        for match in LINKS.finditer(content):
            link = match.group("url")
            if link.startswith(("https://", "http://", "mailto:", "#")):
                continue
            local = link.partition("#")[0]
            target = (path.parent / local).resolve()
            if not target.is_relative_to(ROOT) or not target.is_file():
                print(f"BROKEN LINK: {path.relative_to(ROOT)} → {link}")
                failures += 1
    print(f"{locale}: {len(CHAPTERS) - sum(not (directory / name).is_file() for name in CHAPTERS)}/8 chapters; {words_or_chars} units; {failures} failures")
    return failures, words_or_chars


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=LOCALES, default="en")
    parser.add_argument("--require-all", action="store_true", help="Enforce eight complete localized books")
    parser.add_argument("--available", action="store_true", help="Check every published long-form directory, without treating the remaining locales as published")
    args = parser.parse_args()
    if args.require_all:
        requested = LOCALES
    elif args.available:
        requested = tuple(locale for locale in LOCALES if (MANUAL_ROOT / locale).is_dir())
        if not requested:
            parser.error("No long-form manual editions found")
    else:
        requested = (args.language,)
    failures = 0
    for locale in requested:
        count, _ = verify(locale)
        failures += count
    if failures:
        print(f"FAIL: {failures} structural/content/reference defects")
        return 1
    print("PASS: chapters are full-length, structured and have no broken local file references")
    return 0


if __name__ == "__main__":
    sys.exit(main())
