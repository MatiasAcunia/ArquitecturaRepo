# Documentation index — ArquitecturaRepo

This index separates the **public installable product** from **maintainer engineering and historical evidence**. File visibility on GitHub is public; a file is not private merely because a heading says "maintainer-only". Only explicitly published, source-verified capabilities are supported. The latest release is v1.2.0; v1.3 M0–M6 remain engineering/QA work, and M7 is later optional package/plugin absorption.

## Start here — ordinary adopter

- [README](../README.md): product, capabilities, quick start, profiles and status.
- [Installation instructions](../prompts/INSTALL_THIS_SDLC.md): adapt a new or existing project with safe discovery.
- [Spanish FAQ](FAQ_ES.md) and [language translations](i18n/README_en.md).
- [Architecture overview](00_ARCHITECTURE_OVERVIEW.md), [minimum profile](05_MINIMUM_VIABLE_PROFILE.md), [scaling profiles](06_SCALING_PROFILES.md), [project modes](27_PROJECT_MODES_AND_STACK_SELECTION.md).
- [Existing repository attachment preflight](32_EXISTING_GOVERNED_ATTACHMENT.md) and [adoption guide](16_TRANSFER_ADOPTION.md).
- [Project requirements and baseline](21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md).
- [Current portable v1.2 capabilities and limits](23_OPERATIONAL_AGENTIC_SDLC_V1_2.md); [Spanish version](24_OPERATIONAL_AGENTIC_SDLC_V1_2_ES.md).
- [Privacy/feedback controls](22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md) and [safe artifact GC](34_FILE_ARTIFACT_INVENTORY_AND_GC.md).
- [Public roadmap](ROADMAP.md), [security](../SECURITY.md), [contributing](../CONTRIBUTING.md), [license](../LICENSE).

## Technical reference — when the capability is relevant

The numbered docs 01–20 cover bootstrap, mechanisms, failure modes, reference layout/runtime, executable validation, transactions, schemas, canonical ownership, stateful examples, migration, release history and repository hygiene. Select them by task rather than reading the entire library for every operation. Executable source, release tags, schemas and current adopter state outrank historical proposals.

## Contributor / maintainer engineering — NOT adopter prerequisites

- [v1.2 security audit](25_V1_2_SECURITY_HARDENING_AUDIT.md), [Windows physical acceptance scenario](26_L3_WINDOWS_PHYSICAL_ACCEPTANCE.md), [longitudinal fixture protocol](28_LONGITUDINAL_L3_TEST_PROTOCOL.md), [existing-governance transfer pilot](29_EXISTING_REPOSITORY_TRANSFER_PILOT.md).
- [Current v1.3 QA scope](38_V1_3_PRODUCT_QUALITY_AND_END_TO_END_PLAN.md), [research review](39_V1_3_AGENT_FRAMEWORKS_AND_AGENTIC_SDLC_RESEARCH_TRANSFER.md), [architecture design](40_V1_3_TARGET_SOFTWARE_ARCHITECTURE_AND_TPP_ENGINEERING.md), [M0–M6 milestones and gates](41_V1_3_EXECUTION_ROUTE_ACCEPTANCE_AND_MILESTONES.md).
- [v1.3 portable support and release limits (engineering candidate)](42_V1_3_PORTABLE_SUPPORT_AND_RELEASE_GATES.md): local governance controls, optional host dependencies and unreleased capability matrix.

These are auditable design and QA inputs, not additional installation contracts, external-platform guarantees, private-controller dependencies or instructions for users to run personal pilot Goals. Any resumed engineering must remain within its existing authorized campaign and receive independent terminal review.

## Private historical maintainer records — removed from the public working tree

Six superseded v1.2 internal documents were moved into a separately held private archive (see the maintainer's private CURRENT index, **not linked here**): stabilization master plan 30, private L3 terminal intake 31, portfolio adoption design 33, engineering-first historical plan 35, and version-specific Codex Daily Control 2.0.2 and 2.1 integration reports 36–37. Their old names and blob identities are recorded privately for audit. They were never adopter dependencies, and their removal does not supersede canonical source/charter/state.

**Important:** removing files from the current public Git tree does not delete their old contents from existing commits, forks, clones or caches. A separate coordinated exposure/history-remediation process is required if historical content contains actual secrets or confidential personal data. Do not rewrite shared history automatically.

## Distribution boundary

The generic installer should carry only the selected public runtime, schemas, profiles, needed protocols, prompts and templates. It must not package maintainer test logs, private identity maps, private project names, raw controller ZIPs, user environments, agent conversations, evaluator secrets or old private handoffs. Optional integrations declare explicitly what they support and what evidence is synthetic versus physical. Independently verify actual release bytes before publication.

This index is navigation, not a second Product State, campaign charter or independent release authority.
