# Agentic SDLC — Getting started

A reusable, repository-first architecture for agent-assisted software development. It provides roles, durable state, planning, recovery and verification. It does not autonomously build arbitrary software or remove product-owner decisions.

## Install in an existing project

Choose the smallest suitable profile. Start with read-only discovery; never transplant sample Product State into a real project. A fresh scaffold begins in HOLD / UNTRUSTED_CONTEXT.

```bash
python tools/scaffold_project.py --target "../my-project" --profile SMALL --product-id EXAMPLE --language auto
```

## Roles and boundaries

The CLIENT owns product and sensitive approvals; I2 owns strategy and acceptance; I3 owns in-charter engineering and recovery; optional I4 supplies bounded assistance and independent evidence. Four roles do not require four processes.

## Privacy and monthly feedback

New scaffolds generate a small monthly metadata-only report in the project's own GitHub Actions artifacts. Enabled by default, it helps improve starter structure and categorize failures. It is not sent to the starter maintainer automatically. No code, conversations, project names, paths, identifiers or credentials are included.

Disable feedback by setting enabled=false in .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json, by removing .github/workflows/agentic-sdlc-feedback.yml or by installing with --no-feedback-workflow.

## Safety and release status

Stable release: 1.1.0. Version 1.2 is a candidate under testing; Codex Desktop Goal, Gemini, external-effect adapters and scheduled multi-project tasks need physical acceptance. CI alone is not product acceptance.

## Languages

The installer detects your OS language (or accepts --language es, for example). Documentation is available offline. GitHub's top-level README is static, so select a language from its links.

[FAQ](FAQ_en.md) · [GitHub README](../../README.md)
