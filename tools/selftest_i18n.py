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


def check_local_links(path: Path) -> None:
    """Check readable relative Markdown targets, including offline installs."""
    for href in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
        location = href.split("#", 1)[0]
        if not location or ":" in location or location.startswith("/"):
            continue
        check((path.parent / location).is_file(),
              "broken localized documentation link: " + str(path) + " -> " + href)


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
        manual = docs / f"MANUAL_{code}.md"
        check(readme.is_file() and faq.is_file() and manual.is_file(), "missing localized documents: " + code)
        readme_text = readme.read_text(encoding="utf-8")
        faq_text = faq.read_text(encoding="utf-8")
        manual_text = manual.read_text(encoding="utf-8")
        for localized_path in (readme, faq, manual):
            check_local_links(localized_path)
        minimum = 700 if code in {"ja", "zh"} else 1000
        check(len(readme_text) > minimum and len(faq_text) > minimum,
              "localized documentation too short: " + code)
        check(len(re.findall(r"^### [0-9]+\.", faq_text, flags=re.M)) == 13,
              "FAQ coverage parity broken: " + code)
        check("enabled=false" in readme_text + faq_text, "feedback opt-out missing: " + code)
        check("--language" in readme_text + faq_text, "language option missing: " + code)
        check(f"(MANUAL_{code}.md)" in readme_text and f"(MANUAL_{code}.md)" in faq_text,
              "localized manual is not linked from guide and FAQ: " + code)
        check(all(re.search(rf"^## 0{section} ", manual_text, flags=re.M) for section in range(8)),
              "practical manual missing one of the eight sections: " + code)
        check("--no-feedback-workflow" in manual_text and "enabled=false" in manual_text,
              "manual feedback-scheduler/report distinction missing: " + code)
        check("EXISTING_CONTROL_PRESERVED" in manual_text and "UNTRUSTED_CONTEXT" in manual_text,
              "manual recovery boundaries missing: " + code)
        check("https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0" in manual_text,
              "manual release source missing: " + code)
        check(len(manual_text) >= (2500 if code in {"ja", "zh"} else 3500),
              "localized practical manual unexpectedly thin: " + code)
        for label, content in (("readme", readme_text), ("faq", faq_text)):
            check("1.4.0" in content and "v1.3.0" in content,
                  f"published/source version lineage missing in {code} {label}")
            check("https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0" in content,
                  f"canonical release URL missing in {code} {label}")
            check("1.1.0" not in content,
                  f"stale v1.1 stable-release claim in {code} {label}")

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
            installed_faq = control / "docs" / "i18n" / f"FAQ_{code}.md"
            installed_readme = control / "docs" / "i18n" / f"README_{code}.md"
            installed_manual = control / "docs" / "i18n" / f"MANUAL_{code}.md"
            check(installed_faq.is_file(),
                  "offline post-install language switch unavailable: " + code)
            check(installed_manual.is_file(),
                  "offline post-install manual unavailable: " + code)
            for installed_path in (installed_readme, installed_faq, installed_manual):
                check_local_links(installed_path)
        check("(docs/i18n/MANUAL_ja.md)" in (control / "README.md").read_text(encoding="utf-8"),
              "installed root README manual link was not rebased")
        installed_source_guide = (control / "docs" / "i18n" / "README_ja.md").read_text(encoding="utf-8")
        check("(../46_V1_4_PUBLIC_START_AND_SUPPORT.md)" not in installed_source_guide,
              "installed source-only documentation reference is broken")
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
        check(selected_docs["language"] == "fr" and Path(selected_docs["faq"]).is_file()
              and Path(selected_docs["manual"]).is_file(),
              "switching docs offline did not work")

    print("I18N SELF-TEST PASSED — 8 locales, 13 FAQ topics each, auto, override, fallback, offline install")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
