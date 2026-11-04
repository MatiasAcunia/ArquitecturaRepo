# Documentation index — ArquitecturaRepo

This index separates the **public installable product** from **maintainer engineering and historical evidence**. File visibility on GitHub is public; a file is not private merely because a heading says "maintainer-only". Only explicitly published, source-verified capabilities are supported. **v1.4.0 has been published** as a [versioned GitHub Release with portable ZIP, checksum and manifest](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0). `main` can contain later documentation edits and is not itself that release; v1.3.0 is the previous version.

## Start here — ordinary adopter

- [README](../README.md): product, capabilities, quick start, profiles and status.
- [v1.4.0 first-user guide and actual support matrix](46_V1_4_PUBLIC_START_AND_SUPPORT.md): executable installation, published-artifact identity, honest limits, privacy and recovery.
- [v1.4.0 mini guides in eight languages](i18n/MINI_GUIDE_en.md): concise 00–07 walkthroughs, installation commands and recovery boundaries; [ES](i18n/MINI_GUIDE_es.md), [PT](i18n/MINI_GUIDE_pt.md), [FR](i18n/MINI_GUIDE_fr.md), [DE](i18n/MINI_GUIDE_de.md), [IT](i18n/MINI_GUIDE_it.md), [JA](i18n/MINI_GUIDE_ja.md), [ZH](i18n/MINI_GUIDE_zh.md). These are summaries, not translations of the full manual.
- [Full eight-chapter Spanish manual, historical v1.3 edition](manual/ES/README.md) — approximately 19,000 words. Seven separate full-length v1.4 language editions now exist in the source tree; the remaining Chinese mini guide is not a full translation. Current v1.4 install instructions remain in the public start guide and release notes.
- The eight mini guides were written **after** the v1.4.0 release. They are available in the `main` source tree and in installations produced from that updated tree, **not** in the original v1.4.0 ZIP/container. Future offline distribution of these documents needs its own versioned release.
- [v1.4.0 release notes and upgrade boundaries](47_V1_4_RELEASE_NOTES_AND_UPGRADE.md): versioned capabilities, published package verification and deliberate non-upgrade of existing governed state.
- [Installation instructions](../prompts/INSTALL_THIS_SDLC.md): adapt a new or existing project with safe discovery.
- [Spanish FAQ](FAQ_ES.md), [full Spanish v1.4 manual (60 pages)](manual/v1.4/es/README.md), [full English v1.4 manual (59 pages)](manual/v1.4/en/README.md), [full Portuguese v1.4 manual (57 pages)](manual/v1.4/pt/README.md), [full French v1.4 manual (57 pages)](manual/v1.4/fr/README.md), [full German v1.4 manual (58 pages)](manual/v1.4/de/README.md), [full Italian v1.4 manual (61 pages)](manual/v1.4/it/README.md), [full Japanese v1.4 manual (59 pages)](manual/v1.4/ja/README.md), and [eight localized mini guides](i18n/README_en.md).
- [Architecture overview](00_ARCHITECTURE_OVERVIEW.md), [minimum profile](05_MINIMUM_VIABLE_PROFILE.md), [scaling profiles](06_SCALING_PROFILES.md), [project modes](27_PROJECT_MODES_AND_STACK_SELECTION.md).
- [Existing repository attachment preflight](32_EXISTING_GOVERNED_ATTACHMENT.md) and [adoption guide](16_TRANSFER_ADOPTION.md).
- [Project requirements and baseline](21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md).
- [Historical portable v1.2 capabilities and limits](23_OPERATIONAL_AGENTIC_SDLC_V1_2.md); [Spanish version](24_OPERATIONAL_AGENTIC_SDLC_V1_2_ES.md). Consult the v1.4 support matrix above for current release scope.
- [Privacy/feedback controls](22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md) and [safe artifact GC](34_FILE_ARTIFACT_INVENTORY_AND_GC.md).
- [Public roadmap](ROADMAP.md), [security](../SECURITY.md), [contributing](../CONTRIBUTING.md), [license](../LICENSE).

## Technical reference — when the capability is relevant

The numbered docs 01–20 cover bootstrap, mechanisms, failure modes, reference layout/runtime, executable validation, transactions, schemas, canonical ownership, stateful examples, migration, release history and repository hygiene. Select them by task rather than reading the entire library for every operation. Executable source, release tags, schemas and current adopter state outrank historical proposals.

## Optional plugins

- [Agent Continuity Bridge 0.2.1](../plugins/agent-continuity-bridge/README.md) — opt-in offline bridge, installer and eight language guides. It inspects/records an independently supplied controller package but does not install or control Codex Desktop, Goals, quotas, or cloud usage. Native actions remain unverified and out of portable-core release scope; the plugin can be upgraded independently after compatibility evidence.

## Contributor / maintainer engineering — NOT adopter prerequisites

- [v1.2 security audit](25_V1_2_SECURITY_HARDENING_AUDIT.md), [Windows physical acceptance scenario](26_L3_WINDOWS_PHYSICAL_ACCEPTANCE.md), [longitudinal fixture protocol](28_LONGITUDINAL_L3_TEST_PROTOCOL.md), [existing-governance transfer pilot](29_EXISTING_REPOSITORY_TRANSFER_PILOT.md).
- [Historical v1.3 QA scope](38_V1_3_PRODUCT_QUALITY_AND_END_TO_END_PLAN.md), [research review](39_V1_3_AGENT_FRAMEWORKS_AND_AGENTIC_SDLC_RESEARCH_TRANSFER.md), [architecture design](40_V1_3_TARGET_SOFTWARE_ARCHITECTURE_AND_TPP_ENGINEERING.md), [M0–M6 milestones and gates](41_V1_3_EXECUTION_ROUTE_ACCEPTANCE_AND_MILESTONES.md).
- The historical v1.3 route also mentioned **M7** as optional subsequent package/plugin absorption. It is not a prerequisite for first-time adoption, a claim of completed support, or an E4 authorization.
- [Historical v1.3 portable support/release qualification](42_V1_3_PORTABLE_SUPPORT_AND_RELEASE_GATES.md) and [published v1.3.0 release notes](43_V1_3_RELEASE_NOTES_AND_UPGRADE.md). Historical candidate status does not supersede its subsequent release.

These are auditable design and QA inputs, not additional installation contracts, external-platform guarantees, private-controller dependencies or instructions for users to run personal pilot Goals. Any resumed engineering must remain within its existing authorized campaign and receive independent terminal review.

## Historical source and confidentiality

Obsolete maintainer records are not part of the current starter or adopter instructions. This public index intentionally does not list private archive names, identities or locations. Such records are never required for installing or using ArquitecturaRepo.

**Important:** removing files from the current public Git tree does not delete their old contents from existing commits, forks, clones or caches. A separate coordinated exposure/history-remediation process is required if historical content contains actual secrets or confidential personal data. Do not rewrite shared history automatically.

## Distribution boundary

The generic installer should carry only the selected public runtime, schemas, profiles, needed protocols, prompts and templates. It must not package maintainer test logs, private identity maps, private project names, raw controller ZIPs, user environments, agent conversations, evaluator secrets or old private handoffs. Optional integrations declare explicitly what they support and what evidence is synthetic versus physical. Independently verify actual release bytes before publication.

This index is navigation, not a second Product State, campaign charter or independent release authority.

- [Outcome-first execution and bounded work orders](44_OUTCOME_FIRST_AGENT_EXECUTION.md) — source-pinned operator instructions, physical progress receipts, stop budgets and closure boundaries.
