#!/usr/bin/env python3
"""Deterministic, offline language selection for local starter documentation.

GitHub's repository README is static and cannot inspect a viewer's locale.
This module selects documentation for locally installed tools, not product state.
"""
from __future__ import annotations

import argparse
import json
import locale
import os
from pathlib import Path
from typing import Mapping


SUPPORTED = {
    "en": "English", "es": "Español", "pt": "Português",
    "fr": "Français", "de": "Deutsch", "it": "Italiano",
    "ja": "日本語", "zh": "中文",
}
DEFAULT = "en"


class LanguageError(ValueError):
    pass


def normalize_locale(value: str | None) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    head = value.strip().split(".", 1)[0].split("@", 1)[0]
    head = head.replace("_", "-").lower()
    if head in ("c", "posix"):
        return None
    primary = head.split("-", 1)[0]
    return primary if primary in SUPPORTED else None


def choose_language(requested: str = "auto", *,
                    environment: Mapping[str, str] | None = None,
                    os_locale: str | None = None) -> tuple[str, str]:
    if requested != "auto":
        language = normalize_locale(requested)
        if language is None:
            raise LanguageError("Unsupported --language: choose en, es, pt, fr, de, it, ja, zh or auto")
        return language, "USER_SELECTED"
    env = os.environ if environment is None else environment
    explicit = env.get("AGENTIC_SDLC_LANGUAGE", "")
    if explicit and explicit != "auto":
        language = normalize_locale(explicit)
        if language is None:
            raise LanguageError("AGENTIC_SDLC_LANGUAGE is invalid")
        return language, "ENVIRONMENT_OVERRIDE"
    for name in ("LC_ALL", "LC_MESSAGES", "LANG"):
        language = normalize_locale(env.get(name))
        if language:
            return language, "ENVIRONMENT"
    if os_locale is None:
        try:
            os_locale = locale.getlocale()[0]
        except (ValueError, TypeError):
            os_locale = None
    language = normalize_locale(os_locale)
    if language:
        return language, "SYSTEM_LOCALE"
    return DEFAULT, "DEFAULT_ENGLISH"


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve offline localized documentation.")
    parser.add_argument("--language", default="auto",
                        help="auto, en, es, pt, fr, de, it, ja or zh")
    parser.add_argument("--docs-root", type=Path, default=Path(__file__).resolve().parents[1] / "docs" / "i18n")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        language, source = choose_language(args.language)
    except LanguageError as exc:
        parser.exit(2, "LANGUAGE HOLD: " + str(exc) + "\n")
    docs = args.docs_root.resolve()
    paths = {"readme": docs / ("README_" + language + ".md"),
             "faq": docs / ("FAQ_" + language + ".md")}
    if any(not path.is_file() or not path.resolve().is_relative_to(docs) for path in paths.values()):
        parser.exit(2, "LANGUAGE HOLD: missing localized docs\n")
    output = {"language": language, "source": source,
              "readme": str(paths["readme"]), "faq": str(paths["faq"])}
    print(json.dumps(output, ensure_ascii=False, indent=2) if args.json else
          language + " (" + source + ") " + str(paths["readme"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
