#!/usr/bin/env python3
"""Offline locale selection, translation coverage and sandboxed install tests."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from i18n import SUPPORTED, LanguageError, choose_language, normalize_locale


ROOT = Path(__file__).resolve().parents[1]


def check(assertion: bool, message: str) -> None:
    if not assertion:
        raise AssertionError(message)


def scaffold(destination: Path, language: str, *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "tools" / "scaffold_project.py"),
         "--target", str(destination), "--profile", "SMALL",
         "--product-id", "SYNTHETIC_LOCALE", "--language", language],
        cwd=ROOT, env=env, capture_output=True, text=True, check=False,
    )


def main() -> int:
    examples = {
        "es_UY.UTF-8": "es",
        "pt_BR": "pt",
        "fr_FR": "fr",
        "de_DE": "de",
        "it_IT": "it",
        "ja_JP.UTF-8": "ja",
        "zh_CN.UTF-8": "zh",
        "en_US.UTF-8": "en",
        "C.UTF-8": None,
    }
    for value, expected in examples.items():
        check(normalize_locale(value) == expected, "locale mapping failed: " + value)
    check(choose_language("auto", environment={"LC_ALL": "es_UY.UTF-8"})[0] == "es",
          "auto failed to detect language")
    check(choose_language("auto", environment={"LANG": "xx_YY"}, os_locale="en_US")[0] == "en",
          "unsupported locale must use safe English fallback")
    check(choose_language("pt", environment={"LC_ALL": "ja_JP"})[0] == "pt",
          "explicit --language must override host locale")
    check(choose_language("auto", environment={"AGENTIC_SDLC_LANGUAGE": "zh", "LANG": "es"})[0] == "zh",
          "environment preference must override system locale")
    try:
        choose_language("auto", environment={"AGENTIC_SDLC_LANGUAGE": "not-a-language"})
    except LanguageError:
        pass
    else:
        raise AssertionError("invalid explicit locale silently accepted")

    docs = ROOT / "docs" / "i18n"
    for code in SUPPORTED:
        readme = docs / f"README_{code}.md"
        faq = docs / f"FAQ_{code}.md"
        check(readme.is_file() and faq.is_file(), "missing localized documents: " + code)
        readme_text = readme.read_text(encoding="utf-8")
        faq_text = faq.read_text(encoding="utf-8")
        minimum = 700 if code in {"ja", "zh"} else 1000
        check(len(readme_text) > minimum and len(faq_text) > minimum,
              "localized documentation too short: " + code)
        check(len(re.findall(r"^### [0-9]+\.", faq_text, flags=re.M)) == 12,
              "FAQ coverage parity broken: " + code)
        check("enabled=false" in readme_text + faq_text, "feedback opt-out missing: " + code)
        check("--language" in readme_text + faq_text, "language option missing: " + code)
        check("1.1.0" in faq_text and "1.2" in faq_text,
              "release gates not explained: " + code)

    with tempfile.TemporaryDirectory(prefix="agentic-i18n-") as tmp:
        root = Path(tmp)
        explicit = scaffold(root / "japanese", "ja")
        check(explicit.returncode == 0, "Japanese scaffold failed: " + explicit.stderr)
        control = root / "japanese" / ".agentic-sdlc"
        meta = json.loads((control / "docs" / "LANGUAGE_SELECTION.json").read_text(encoding="utf-8"))
        check(meta["language"] == "ja" and meta["source"] == "USER_SELECTED",
              "selected language metadata not pinned")
        check("はじめに" in (control / "README.md").read_text(encoding="utf-8"),
              "Japanese instructions did not become first local README")
        for code in SUPPORTED:
            check((control / "docs" / "i18n" / f"FAQ_{code}.md").is_file(),
                  "offline post-install language switch unavailable: " + code)
        env = dict(os.environ, AGENTIC_SDLC_LANGUAGE="es")
        auto = scaffold(root / "spanish", "auto", env=env)
        check(auto.returncode == 0, "auto Spanish install failed: " + auto.stderr)
        selected = json.loads((root / "spanish" / ".agentic-sdlc" /
                               "docs" / "LANGUAGE_SELECTION.json").read_text(encoding="utf-8"))
        check(selected["language"] == "es" and selected["source"] == "ENVIRONMENT_OVERRIDE",
              "auto did not select Spanish")
        bad = scaffold(root / "invalid", "ru")
        check(bad.returncode != 0 and not (root / "invalid").exists(),
              "unsupported language created a partial project")
        cmd = subprocess.run(
            [sys.executable, str(control / "tools" / "i18n.py"),
             "--language", "fr", "--docs-root", str(control / "docs" / "i18n"),
             "--json"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        check(cmd.returncode == 0, "portable locale documentation tool failed")
        selected_docs = json.loads(cmd.stdout)
        check(selected_docs["language"] == "fr" and Path(selected_docs["faq"]).is_file(),
              "switching docs offline did not work")

    print("I18N SELF-TEST PASSED — 8 locales, 12 FAQ topics each, auto, override, fallback, offline install")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
