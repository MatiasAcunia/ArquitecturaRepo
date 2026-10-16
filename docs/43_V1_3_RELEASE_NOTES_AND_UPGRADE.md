# ArquitecturaRepo v1.3.0 — release notes, supported scope and upgrade guidance

Status: **an untagged build is a release candidate; only an authorized v1.3.0 tag with a GitHub Release is published**. This document does not itself authorize publication.

## What is included

- Portable framework installation into a fresh project, with proportional profiles and eight offline documentation languages.
- Goal/Plan/charter and campaign control-plane contracts, source/currentness checks and bounded actor/run/finite-lease requirements.
- Durable review evidence revalidation at strategic terminal, and separate review/acceptance boundaries.
- Portable deterministic ToolPort test adapter, idempotent effect receipts, journal/recovery and SQLite WAL currentness checks.
- Safe refusal to install a second canonical Product State into an already governed repository; explicit read-only attachment remains available.
- Honest local architecture-feedback configuration and workflow opt-out status.

## What is NOT included or guaranteed

- No automatic in-place upgrade/uninstaller for existing v1.2-governed projects. Schema-specific migration tools are not a universal 1.2-to-1.3 migration.
- No third-party model ability guarantee, autonomous general-purpose IDE agent, live Codex Desktop/Goal/quota controls, external 3.1 controller bundle or API credentials.
- No blanket claim that a Linux-installed acceptance test guarantees every Windows configuration. The source CI includes Windows portable compatibility and a Windows installed-framework test; individual adopter environments vary.
- No external feedback delivery without a verified endpoint and the relevant consent/transport configuration.

## Installation and adoption

For a new project use the source at the exact published v1.3.0 Git tag, inspect `prompts/INSTALL_THIS_SDLC.md` and run `python tools/scaffold_project.py --help` before choosing an installation profile. A new installation begins in HOLD/UNTRUSTED_CONTEXT; confirm CLIENT requirements and technical baseline before any campaign authority. The `--no-feedback-workflow` flag prevents installing the scheduled feedback workflow, but does not necessarily disable the separately configured local generator or outbound preference.

For an unmanaged existing codebase, first back up or commit user-owned files and run an isolated dry-run of the installer. The installer must refuse collisions and preserve user-owned GitHub Actions and application source; examine the generated diff before accepting changes.

For a **previously governed** project (including v1.2): **do not overlay a new scaffold or copy `.agentic-sdlc` wholesale**. First inventory and back up the canonical Product State, role identities, campaign/currentness, Goal/Plan, DB/WAL, receipts, secrets and project Git SHA. Keep the existing v1.2 control layer active. Use the explicit read-only reference attachment to inspect and verify source ownership (see `docs/32_EXISTING_GOVERNED_ATTACHMENT.md`); plan and independently validate any future migration in a separate checkout. Do not transfer ACTIVE authority, perform automatic rollback of a live DB, or delete original governance from a release archive. No general core automatic upgrade/removal claim is made in this release.

Rollback: For a **new disposable install**, preserve its original project files and remove only known newly installed artifacts once their SHA identities are independently checked. For **governed v1.2 projects**, no in-place migration is performed by default, so the safest rollback is to keep using the existing v1.2 control layer. Never blindly delete Project State, user-owned workflows or receipts. Preserve old release tags and do not perform a release workflow from an untrusted branch.

## Optional integrations

Agent Continuity Bridge 0.2.1 is a separate opt-in, offline adapter candidate (PR #5); it is not a mandatory dependency of the v1.3.0 core and does not prove real Codex Desktop native operations. The external Codex Daily Control 3.1 release candidate and personal configuration are not distributed in this repository or archive. Consult `docs/42_V1_3_PORTABLE_SUPPORT_AND_RELEASE_GATES.md` for exact support boundaries.

## Verification and authority

GitHub Actions tests of the **same committed release tree** must pass on Ubuntu and Windows, including installed-framework exercises. A separate reviewer runs independent safety oracles and verifies actual filesystem effects/currentness before acceptance. Release is performed only by explicit manual authorization on `main` with the exact commit SHA. The historical v1.2 tag and release stay immutable. Neither a draft PR nor green CI alone authorizes v1.3.0 publication.

License: MIT for the project-owned code, with the LICENSE file preserved. Third-party integrations and their original licenses are separate. No professional legal opinion is claimed.
