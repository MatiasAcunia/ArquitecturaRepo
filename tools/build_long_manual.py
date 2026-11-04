#!/usr/bin/env python3
"""Build a source-backed, typeset PDF from a complete eight-chapter manual.

No translation, language model, provider API, or network access is used.
Only editions with all eight real chapter files and valid repository-local links
can be built. This script must not be used to relabel a mini guide as a book.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
MANUAL_ROOT = ROOT / "docs" / "manual" / "v1.4"
REPO_BLOB = "https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/"
CHAPTERS = [
    "00_before_you_begin.md",
    "01_installation.md",
    "02_planner_and_adoption.md",
    "03_daily_operation.md",
    "04_requesting_changes.md",
    "05_errors_and_recovery.md",
    "06_closing_capabilities.md",
    "07_worked_club_example.md",
]
LOCALE_LABELS = {
    "en": {
        "title": "The Complete User Manual", "code": "ENGLISH", "lang": "en-US",
        "chapter": "CHAPTER", "header": "COMPLETE USER MANUAL",
        "eyebrow": "ENGINEERING SYSTEMS / USER GUIDES",
        "summary1": "Eight full chapters: discovery, installation, adoption, operation,",
        "summary2": "changes, recovery, acceptance and a worked product example.",
        "byline": "Source-backed documentation for the public ArquitecturaRepo framework.",
        "contents": "Contents", "date": "4 November 2026", "version": "VERSION", "footer_date": "NOVEMBER 2026",
    },
    "es": {
        "title": "Manual completo de uso", "code": "ESPAÑOL", "lang": "es-ES",
        "chapter": "CAPÍTULO", "header": "MANUAL COMPLETO · v1.4",
        "eyebrow": "SISTEMAS DE INGENIERÍA / GUÍAS DE USO",
        "summary1": "Ocho capítulos extensos: descubrimiento, instalación, adopción,",
        "summary2": "operación, cambios, recuperación, aceptación y ejemplo guiado.",
        "byline": "Documentación contrastada con las fuentes de ArquitecturaRepo.",
        "contents": "Índice general", "date": "4 de noviembre de 2026", "version": "VERSIÓN", "footer_date": "NOVIEMBRE DE 2026",
    },
    "pt": {
        "title": "Manual completo de utilização", "code": "PORTUGUÊS", "lang": "pt-PT",
        "chapter": "CAPÍTULO", "header": "MANUAL COMPLETO · v1.4",
        "eyebrow": "SISTEMAS DE ENGENHARIA / GUIAS DE UTILIZAÇÃO",
        "summary1": "Oito capítulos completos: descoberta, instalação, adoção, operação,",
        "summary2": "mudanças, recuperação, aceitação e um exemplo guiado de produto.",
        "byline": "Documentação verificada com o código-fonte do ArquitecturaRepo.",
        "contents": "Índice geral", "date": "4 de novembro de 2026", "version": "VERSÃO", "footer_date": "NOVEMBRO DE 2026",
    },
    "fr": {
        "title": "Manuel d'utilisation complet", "code": "FRANÇAIS", "lang": "fr-FR",
        "chapter": "CHAPITRE", "header": "MANUEL COMPLET · v1.4",
        "eyebrow": "INGÉNIERIE LOGICIELLE / GUIDES D'UTILISATION",
        "summary1": "Huit chapitres : découverte, installation, adoption, opération,",
        "summary2": "changements, récupération, acceptation et exemple de produit.",
        "byline": "Documentation vérifiée par rapport aux sources d'ArquitecturaRepo.",
        "contents": "Table des matières", "date": "4 novembre 2026", "version": "VERSION", "footer_date": "NOVEMBRE 2026",
    },
    "de": {
        "title": "Vollständiges Benutzerhandbuch", "code": "DEUTSCH", "lang": "de-DE",
        "chapter": "KAPITEL", "header": "BENUTZERHANDBUCH · v1.4",
        "eyebrow": "SOFTWAREENTWICKLUNG / BENUTZERHANDBÜCHER",
        "summary1": "Acht Kapitel: Einführung, Installation, Adoption, Betrieb,",
        "summary2": "Änderungen, Wiederherstellung, Abnahme und Vereinsbeispiel.",
        "byline": "An den Quellen des ArquitecturaRepo-Starters geprüfte Anleitung.",
        "contents": "Inhaltsverzeichnis", "date": "4. November 2026", "version": "VERSION", "footer_date": "NOVEMBER 2026",
    },
}
LINK = re.compile(r"(?P<prefix>\]\()(?P<url>[^\s)]+)(?P<suffix>\))")


def resolve_link(chapter: Path, raw: str) -> str:
    if raw.startswith(("https://", "http://", "mailto:", "#")):
        return raw
    target, sep, fragment = raw.partition("#")
    if not target:
        return raw
    resolved = (chapter.parent / target).resolve()
    try:
        relative = resolved.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"Link escapes the repository: {chapter}: {raw}") from exc
    if not resolved.is_file():
        raise ValueError(f"Broken file link: {chapter.relative_to(ROOT)} → {raw}")
    link = REPO_BLOB + quote(relative.as_posix(), safe="/")
    if sep:
        link += "#" + quote(fragment, safe="-")
    return link


def collect(locale: str) -> str:
    source = MANUAL_ROOT / locale
    missing = [name for name in CHAPTERS if not (source / name).is_file()]
    if missing:
        raise ValueError(f"Incomplete {locale} long manual: missing {', '.join(missing)}")
    chapters = []
    for name in CHAPTERS:
        chapter = source / name
        content = chapter.read_text(encoding="utf-8")
        if len(content.split()) < 1100:
            raise ValueError(f"Not a full-length chapter: {chapter.relative_to(ROOT)}")
        # In the PDF, repository-local references must link to the repository,
        # not to nonexistent neighboring files at the PDF download location.
        def rewrite(match: re.Match[str]) -> str:
            return match.group("prefix") + resolve_link(chapter, match.group("url")) + match.group("suffix")

        chapters.append(LINK.sub(rewrite, content))
    return "\n\n".join(chapters) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", default="en", help="Completed long-form locale")
    parser.add_argument("--output", type=Path, required=True, help="PDF output path")
    args = parser.parse_args()
    if args.language not in LOCALE_LABELS:
        parser.error(f"No verified PDF typography settings for locale {args.language!r}")
    labels = LOCALE_LABELS[args.language]
    if not shutil.which("pandoc") or not shutil.which("xelatex"):
        parser.error("PDF generation requires local pandoc and xelatex")

    try:
        source = collect(args.language)
    except ValueError as exc:
        parser.error(str(exc))

    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="arquitecturarepo-manual-") as tmp:
        temp_dir = Path(tmp)
        rendered = temp_dir / "manual.md"
        rendered.write_text(source, encoding="utf-8")
        preamble = temp_dir / "preamble.tex"
        latex = r"""\usepackage{microtype}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{etoolbox}
\usepackage{longtable}
\usepackage{xcolor}
\usepackage{hyperref}
\definecolor{ARdark}{HTML}{13243A}
\definecolor{ARaccent}{HTML}{176F87}
\definecolor{ARmuted}{HTML}{63788C}
\hypersetup{colorlinks=true,linkcolor=ARdark,urlcolor=ARaccent,citecolor=ARaccent}
\titleformat{\chapter}[display]{\normalfont\sffamily\bfseries\color{ARdark}}
{\fontsize{15}{18}\selectfont CHAPTER \thechapter}{10pt}{\fontsize{21}{26}\selectfont}
\titlespacing*{\chapter}{0pt}{-10pt}{22pt}
\titleformat{\section}{\Large\sffamily\bfseries\color{ARaccent}}{\thesection}{9pt}{}
\titleformat{\subsection}{\large\sffamily\bfseries\color{ARdark}}{\thesubsection}{9pt}{}
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[C]{\small\thepage}\renewcommand{\headrulewidth}{0pt}}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\sffamily\color{ARmuted} ARQUITECTURAREPO}
\fancyhead[R]{\small\sffamily\color{ARmuted} COMPLETE USER MANUAL · v1.4}
\fancyfoot[C]{\small\thepage}
\renewcommand{\headrulewidth}{0.3pt}
\setlength{\headheight}{15pt}
\setlength{\parskip}{4pt}
\setlength{\parindent}{0pt}
\makeatletter
\renewcommand{\maketitle}{%
  \begin{titlepage}
  \thispagestyle{empty}
  \vspace*{28mm}
  {\sffamily\bfseries\color{ARaccent}\large ENGINEERING SYSTEMS / USER GUIDES\par}
  \vspace{12mm}
  {\color{ARaccent}\rule{43mm}{2.5pt}\par}
  \vspace{21mm}
  {\sffamily\bfseries\color{ARdark}\fontsize{34}{41}\selectfont ArquitecturaRepo\par}
  \vspace{8mm}
  {\sffamily\color{ARdark}\fontsize{20}{26}\selectfont The Complete User Manual\par}
  \vspace{3mm}
  {\sffamily\color{ARmuted}\Large VERSION 1.4 / ENGLISH\par}
  \vspace{15mm}
  {\sffamily\large Eight full chapters: discovery, installation, adoption, operation,\par}
  {\sffamily\large changes, recovery, acceptance and a worked product example.\par}
  \vfill
  {\color{ARaccent}\rule{\textwidth}{0.5pt}\par}
  \vspace{5mm}
  {\sffamily\small MATÍAS ACUÑA  ·  NOVEMBER 2026\par}
  {\sffamily\small Source-backed documentation for the public ArquitecturaRepo framework.\par}
  \end{titlepage}
}
\makeatother
"""
        replacements = {
            "CHAPTER \\thechapter": f"{labels['chapter']} \\thechapter",
            "COMPLETE USER MANUAL · v1.4": labels["header"],
            "ENGINEERING SYSTEMS / USER GUIDES": labels["eyebrow"],
            "The Complete User Manual": labels["title"],
            "VERSION 1.4 / ENGLISH": f"{labels['version']} 1.4 / {labels['code']}",
            "Eight full chapters: discovery, installation, adoption, operation,": labels["summary1"],
            "changes, recovery, acceptance and a worked product example.": labels["summary2"],
            "Source-backed documentation for the public ArquitecturaRepo framework.": labels["byline"],
            "MATÍAS ACUÑA  ·  NOVEMBER 2026": f"MATÍAS ACUÑA  ·  {labels['footer_date']}",
        }
        for old, new in replacements.items():
            latex = latex.replace(old, new)
        preamble.write_text(latex, encoding="utf-8")
        command = [
            "pandoc", str(rendered), "--standalone", "--toc", "--toc-depth=2",
            "--top-level-division=chapter", "--pdf-engine=xelatex",
            "--metadata", "title:ArquitecturaRepo",
            "--metadata", f"subtitle:{labels['title']} · v1.4 · {labels['code']}",
            "--metadata", "author:Matías Acuña",
            "--metadata", f"date:{labels['date']}",
            "--metadata", f"lang:{labels['lang']}",
            "--metadata", f"toc-title:{labels['contents']}",
            "--variable", "documentclass=scrreprt", "--variable", "classoption=oneside",
            "--variable", "papersize=a4", "--variable", "fontsize=11pt",
            "--variable", "mainfont=DejaVu Serif", "--variable", "sansfont=DejaVu Sans",
            "--variable", "monofont=DejaVu Sans Mono",
            "--variable", "geometry:margin=22mm",
            "--include-in-header", str(preamble),
            "--output", str(output),
        ]
        subprocess.run(command, check=True)
    print(f"Built {output} ({output.stat().st_size:,} bytes) from eight complete source chapters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
