# Agentic SDLC — Getting started

[Mini guide v1.4](MINI_GUIDE_en.md) · [Complete v1.4 English manual](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/docs/manual/v1.4/en/README.md) · [FAQ](FAQ_en.md)

The [complete eight-chapter English manual](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/docs/manual/v1.4/en/README.md) is available in the **source repository**, updated for v1.4. The [historical full-length Spanish v1.3 manual](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/docs/manual/ES/README.md) is preserved separately. Neither long-form manual is copied into installed control layers by the v1.4.0 release installer. This introductory guide and the mini guide are **short**; use the complete manual for depth and the [v1.4 installation guide](../46_V1_4_PUBLIC_START_AND_SUPPORT.md) for authoritative commands.

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

To disable all reporting, set enabled=false in .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json. Removing .github/workflows/agentic-sdlc-feedback.yml or installing with --no-feedback-workflow disables only the scheduler, not the local generator.

## Safety and release status

**v1.4.0 has been published** as a [versioned GitHub Release with portable ZIP and SHA-256 checksum](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0). Verify downloaded bytes before installation; the moving `main` branch can contain later documentation changes and is not the release artifact. The previous v1.3.0 release remains available. New or ungoverned projects can use the [v1.4 first-user guide](../46_V1_4_PUBLIC_START_AND_SUPPORT.md); already governed projects require [read-only attachment](../32_EXISTING_GOVERNED_ATTACHMENT.md), not an automatic overwrite. Native Codex Desktop, third-party AI providers and external effects have not been physically certified by portable CI alone.

## Languages

The installer detects your OS language (or accepts --language es, for example). Documentation is available offline. GitHub's top-level README is static, so select a language from its links.

[Mini guide v1.4](MINI_GUIDE_en.md) · [Complete eight-chapter manual](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/docs/manual/v1.4/en/README.md) · [FAQ](FAQ_en.md) · [GitHub README](../../README.md)
