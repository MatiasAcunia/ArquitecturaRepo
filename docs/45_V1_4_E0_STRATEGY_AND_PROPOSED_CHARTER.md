# ArquitecturaRepo v1.4 — E0 strategic reconstruction and proposed engineering charter

Status: **E0 STRATEGIC AUDIT COMPLETE; CHARTER PROPOSED / NOT YET AUTHORIZED**. This file is the single v1.4 E0 decision proposal, not an implementation PASS, an active campaign record, or a release authorization. Date: 2026-11-04 (UTC). Scope is the generic public starter, not the maintainer's private portfolio. A new explicit CLIENT authorization is required before E1 material execution; release/publication requires its own authorization and exact evidence.

## 1. Product destination and CLIENT intent

ArquitecturaRepo is a portable, Git-repository-anchored engineering continuity architecture for software projects developed with human judgment and optional AI agents. Its product is **durable, reconstructible decisions, responsibilities, project state, currentness, evidence, and a lawful next action**, with a proportionate way to organize planning, execution, verification, recovery and handoffs. Scripts are support mechanisms, not the product's reason to exist.

An ordinary adopter should be able to install the appropriate profile, state the intended product, see one understandable current posture, resume from a fresh context without chat archaeology, and use optional verified execution adapters where genuinely available. The CLIENT keeps product intent, material preferences, external authorization and human/perceptual acceptance; technical debugging, state reconciliation and in-charter rework remain system-owned. The framework does not guarantee model coding skill, fully autonomous native hosts, profitability or success of an adopter's application.

The v1.4 theme is **consolidation rather than feature expansion**: maintain and strengthen existing working mechanisms, eliminate cross-layer contradictions and avoid a second source of truth. No release date or quantitative success threshold is invented by this E0.

## 2. Pinned physical baseline and evidence limitations

| Surface | Observed baseline and implication |
| --- | --- |
| Public repository | This repository, `main@05cefc058b55` (2026-10-25), clean read-only audit checkout. Full ref must be independently resolved from Git before mutation. |
| Published release | `v1.3.0` published 2026-10-17 at `9c00e19b74d1`; a portable ZIP and `.sha256` asset exist. Historical tags must remain immutable. |
| Branch delta | Current `main` is 66 commits ahead of `v1.3.0`; it is not identical to the tagged release. No open PR or non-main branch was present at E0 intake. |
| Source scale | Current tree has 300 tracked blobs, 90 Python files (about 1.08 MB of Python source), and 45 Python test/self-test paths. Seven major modules total about 7,500 lines. Counts are maintenance signals, **not** capability evidence. |
| GitHub CI | The 2026-10-26 `validate-starter` run `40254498029` failed in Linux `validate_structure.py` and Windows `selftest_scaffold.py`. Subsequent dependent tests were skipped, not passed. |
| Linux falsifier | Structure-only scanner rejects a synthetic `.test` email fixture in `tools/test_engineering_packet.py` and legitimate 40-hex source identifiers in `engines/portable-goal/{engine.json,CHANGELOG.md}`. Repair the false-positive rule/fixture conflict without weakening real privacy/source-leak detection. |
| Windows falsifier | `SMALL` is expected not to install cognitive I4 tools, yet `tools/scaffold_project.py` unconditionally copies `tools/cognitive_i4.py`; the Windows test aborts with `SMALL cannot install cognitive I4 tools`. This is a real proportionality defect, not just a documentation mismatch. |
| Local targeted checks | Python syntax compilation succeeded. `selftest_candidate_manifest.py`, `selftest_work_order_guard.py`, and four `test_engineering_packet.py` cases passed in the audit environment. Other local full-framework attempts could not pass without the documented `jsonschema` dependency. Do not count these as full E2E or platform PASS. |
| Documentation currentness | README identifies v1.3.0 as published, while `docs/ROADMAP.md` still says proposed v1.3.0 is not released. `docs/41...` and `docs/42...` remain historical v1.3 planning/support documents, not a v1.4 execution authority. |
| Optional agents | `host_dispatch.py` deliberately holds native Codex CLI agent execution when host-enforced scope/cost evidence is absent; `portable-test-v1` verifies only a restricted disposable ToolPort path. There is no source-backed universal autonomous-agent claim. |
| Public/private separation | Public `AGENTS.md` and appended protocol sections contain maintainer-portfolio-specific instructions; `docs/44...` includes a concrete private-style media case. This conflicts with a generic starter's separation and increases maintenance/portability risk. No credential leak is asserted by this audit. |

Primary live evidence: source at the pinned SHA; `state/STARTER_MANIFEST.json`, `profiles/profiles.json`, `tools/{scaffold_project,validate_project,reconstruct_context,campaignctl,state_tx,artifact_ledger,host_dispatch,tool_port}.py`; root `AGENTS.md`; `docs/{38,40,41,42,43,44}_*.md`; GitHub release and workflow run. Read the exact tagged release separately when verifying regressions.

## 3. PASS1 — whole-product reconstruction and causal route

### End-to-end workflow and owner surfaces

1. **Adopter intent and boundaries:** CLIENT states the product, permitted operations, deployment/privacy/cost and approval boundaries. `state/CLIENT_REQUIREMENTS_CURRENT.md` is normalized intent; accepted newer user decisions must supersede it explicitly, not live in a chat summary.
2. **Bootstrap and canonical currentness:** `tools/scaffold_project.py`, profile definitions, product/technical/delivery state, owner registry and `CURRENT_BOOTSTRAP_STATE` establish an initially `UNTRUSTED_CONTEXT` installation. `validate_project.py` and `reconstruct_context.py` are the current validation/reconstruction owners. A new context derives authority from physical repo/state, not a prompt or commit author.
3. **Strategic-to-tactical handoff:** I2 owns capability charters and interfaces; one persistent I3 owns its authorized campaign, DAG, implementation, in-charter defect repair, tests, integration, review/recovery and terminal evidence. I1 is optional for small installs and portfolio-only admission rules never become universal defaults.
4. **Mutable operational state:** `campaignctl.py` and `state_tx.py` own participating local campaign transitions, atomic files, locks, journals and crash recovery. Git commits capture meaningful durable authority/recovery/release boundaries; GitHub is neither a per-event database nor an implicit transaction/OS permission boundary. Local uncommitted state, remote HEAD and DB/WAL need explicit currentness/reconciliation semantics.
5. **Optional operations and evidence:** host/tool ports, artifact lifecycle and feedback are opt-in/profile-proportional. Simulated commands, script exit codes, agent-produced PASS text and static schema checks cannot certify physical external effects, security, human acceptance or release. Unsupported native host operations remain honest HOLD/UNSUPPORTED.
6. **Adoption, handoff and publication:** fresh and already-governed repositories have separate safe routes; upgrading a governed v1.2/v1.3 installation cannot overwrite Product State, owner authority, DB or user workflows. Independent installed-framework proof, cross-OS verification, package readback and explicit release authorization close the line.

### Canonical product boundaries for v1.4

| Boundary | Primary existing owners | v1.4 posture |
| --- | --- | --- |
| User-facing bootstrap/profile/status | `scaffold_project`, `project_setup`, `profiles`, `project_status`, manuals | Keep one simple supported entry path; SMALL genuinely light; no mandatory provider. |
| Requirements and durable currentness | CLIENT requirements, Product State, bootstrap, owner registry, `validate_project`, `reconstruct_context` | One fact owner per concern; remove duplicate current prose and reconcile local/remote state. |
| Campaign/Goal/Plan | `campaignctl`, Goal/Plan guards, `state_tx` | Preserve identity, lease, CAS, in-campaign rework and journal recovery; simplify interfaces only with proven equivalence. |
| Optional host and worker transport | `host_dispatch`, `tool_port`, adapters, I4 tools | Physically verified capability matrix; optional install; no native authority invented. |
| Artifacts, DB, GC and external effects | `artifact_ledger`, `workspace_gc`, SQLite currentness, `external_effects` | Keep explicit data ownership, identity, rollback and unsafe-delete HOLD; avoid an unnecessary second DB. |
| Documentation and packaging | README, docs index/manual, GitHub Actions, release workflow/ZIP/Docker | One current support story; historical v1.3 docs labelled as history; reproducible source-to-package lineage. |

Critical path: first reconcile `main` vs `v1.3.0` and broken CI; then separate portable public core from maintainer-specific or optional mechanisms, solidify state/reconstruction and profile boundaries, refactor only where coupling/defects justify it, demonstrate real installed lifecycle/recovery/transfer, and qualify one exact v1.4 release candidate. The user-facing value is lower adoption and recovery friction with truthful continuity, **not** fewer files or more agents.

## 4. PASS2 — independent adversarial challenge

| Falsifier / second-order effect | Required design response |
| --- | --- |
| "Simplify" removes an apparently unused guard and permits stale writes, replay or data loss. | Prove the original invariant with seeded regression/physical readback before retiring code; preserve rollback and historical receipts. |
| GitHub remote HEAD is mistaken for current local transaction, DB/WAL or active lease. | Explicit local/remote/checkpoint identity, CAS and conflict/HOLD semantics; test fresh clone and crash between state write and Git promotion. |
| A second `CURRENT` file or a summary starts competing with Product State. | One canonical owner, derived displays only, explicit supersession and validated lineage. |
| A profile declares SMALL but installs heavy AI/feedback/controller mechanisms. | Profile-by-profile file/behavior/resource oracle, optionality and no unsupported default network/provider effects. |
| Public docs contain maintainer-specific models, hosts, names or operational recipes. | Move private-specific rules to their actual owner, replace public references with generic examples, preserve legitimate historical attribution without leaking private state. |
| Refactors reduce LOC but break old CLI contracts, released package consumers, or existing governed installations. | Immutable v1.3 baseline, behavior compatibility matrix, explicit versioned migration/rollback, no auto-overwrite. |
| Provider simulation is counted as autonomous native agent success. | Separate portable ToolPort proof from per-host live physical verification; unsupported claims are omitted or labelled. |
| Tests self-certify, skip on failure, or pass despite a broken installation. | Independent source-bound E2E oracle, both normal success and adversarial cases, gates tracked separately, no retroactive weakening. |
| Data privacy is weakened through scheduled feedback, logs, packages or remote actions. | Allowlisted metadata, verified/visible consent semantics, no secret/content export, package exclusion and real negative tests. |
| Cleanup, re-clones or CI retries consume protected disk/compute and delete valuable artifacts. | One checkout per repo, bounded ephemeral outputs, ownership-aware cleanup only, actual cost/capacity evidence. |
| A private project result is claimed as a direct ArquitecturaRepo adopter without proof. | Public case studies must bind actual installed mechanism/commit/effect lineage; otherwise describe shared method, not installed product success. |
| E1 defects trigger repeated Planner campaigns or early "DONE" while critical gate remains red. | One I3 campaign absorbs in-envelope rework and class-level hardening; Planner returns only for charter invalidation or consolidated terminal. |

Adversarial verdict: **GO for a narrowly bounded v1.4 consolidation charter proposal**, **NO-GO for release or broad automation claims on current `main`**, and **HOLD on any unverified migration/native-host capability**. No PASS3 is justified by the current evidence.

## 5. Proposed unified Engineering Campaign Charter

**Provisional ID:** `AR-V14-CONSOLIDATE` (not active until approved). **Capability:** a truthful, transferable, maintainable Git-repository-based Agentic SDLC starter, replacing the inconsistent post-v1.3 main candidate. **Authority:** CLIENT product intent and release approval; I2 strategic scope and terminal audit; one continuous I3 implementation, tests, refactors, integration, recovery and in-envelope QA; independent reviewer verifies exact candidate. Keep one integration branch/PR, not one branch or charter per defect.

**In scope:** known CI defect repair; public/private governance separation; core/optional/profile classification; canonical currentness and handoff ergonomics; code modularity/refactoring where warranted; compatible schema/CLI and explicit migrations; safe adoption into fresh/existing repositories; docs and packaging truth; A+B physical framework tests, cross-OS smoke and exact release qualification.

**Out of scope:** new AI agent frameworks, compulsory hosted services or model providers, broad autonomous native-host promises, new global event DB, model-quality benchmarks as framework acceptance, unrelated private portfolio rewrites, real product publication/revenue claims, blanket auto-upgrade of governed projects, and code churn motivated only by an arbitrary line-count target. Optional integration additions require measured benefit and separately verified authority; unsupported adapters may remain unverified without blocking portable-core release.

**Protected boundaries:** historical v1.1/v1.2/v1.3 tags and released assets; third-party/adopter application code and data; existing governed Product State, actor/lease, DB/WAL and user-owned workflows; secrets/credentials/private portfolio state; review and accepted evidence; unapproved paid/network/publication/destructive effects. Candidate changes require reversible deltas and bounded write surfaces. No unreviewed force push, tag rewrite, in-place existing-project takeover or duplicate canonical state.

**Interfaces/dependencies:** preserve or version the existing CLI, schemas, profile manifests, `state_tx` journal/recovery semantics, identity/lease, Goal/Plan/charter and protected currentness relationships. Code components depend on canonical policy/state, not specific native hosts; adapter support is versioned and source/effect-bound. Generated projects must not depend on the maintainer's directories, accounts, secrets or proprietary controls.

**Required gates (no substitutions):**

- **Unit/property:** affected invariants, positive and malicious/boundary cases, caught seed mutations, deterministic regression.
- **Integration:** complete generated project plus existing-repository non-destructive adoption and supported public CLI lifecycle.
- **DB/currentness/recovery:** crash, concurrent writers, WAL, stale Git/current owner, no double external effects and fresh-process/source reconstruction.
- **Semantic/generalization:** independent fresh-context actor reconstructs same next legal/forbidden action across unrelated disposable codebase shapes and profile scopes.
- **Runtime/physical:** actual file/DB/process readback; each host marketed as VERIFIED has a separate true host operation and scope/permission readback.
- **Security/privacy/rights:** no unauthorized writes, secret export, unsafe GC, forged signoff or hidden network/provider dependency; correct telemetry disclosure.
- **Human/perceptual:** a first-time adopter can understand setup, current status, supported limits and recovery without maintainer explanation; no invented usability PASS.
- **Release:** exact candidate SHA, independently reviewed supported-capability matrix, Linux+Windows CI, preserved historical compatibility, reproducible tagged ZIP/checksum and any separately advertised container package, install/readback from **published** artifact, explicit CLIENT release authorization.

**Strategic terminal:** one source-pinned report maps each charter obligation to independently verified evidence or a precise declared limitation, records residual risks and supports a defensible accept/reject/rework decision. Ordinary defects return to this same campaign. Two or more same-class returns trigger I3 subsystem-wide hardening and independent review rather than planner churn.

**Charter invalidation events:** CLIENT materially changes product destination; verified source/authority changes outside the baseline envelope; a necessary incompatible public contract or irreversible data migration exceeds approved compatibility/rollback boundaries; an external provider/security/legal constraint makes the declared support claim impossible; or new independent evidence defeats the proposed core/optional architecture. Ordinary CI/test/refactor defects are not invalidation.

## 6. Integrated engineering route (not microcampaigns)

| Stage | Product-level outcome and evidence boundary |
| --- | --- |
| **E1 — baseline and policy hygiene** | Reconcile immutable release/current main, repair known CI/class defects, separate public reusable policy from maintainer-specific material, remove conflicting current claims without destroying lineage. |
| **E2 — canonical continuity** | Single durable fact ownership, reliable reconstruction and legitimate next action across Git/local state, currentness, transaction and handoff boundaries; no new global DB. |
| **E3 — maintainable Python** | Cohesive and readable modules/interfaces, reduced duplicate behavior, safe optional components, full regressions and compatibility/migration proof. |
| **E4 — adopter experience** | Verified fresh and governed-existing adoption paths, proportional profiles, clear CLI/manual/status, appropriate no-provider mode and truthful optional adapter support. |
| **E5 — comprehensive A+B hardening** | Independent whole-framework installed lifecycle, recovery/negative tests, cross-OS, versioned support matrix, human usability and bounded maintenance/cost/disk evidence. |
| **E6 — exact integration and release** | Final clean source + independent review, PR-to-main acceptance, publication-authorized `v1.4.0` tag/Release, tested portable ZIP/checksum and other advertised package only after physical verification. |

These are execution-review milestones inside **one** continuous I3 authority after authorization. Do not assign a new campaign, Planner PASS or branch for each failed test. Keep v1.4 code work off `main` until integration/release gates; never retag `v1.3.0`.

## 7. E0 handoff and decision boundary

E0 has produced a pinned PASS1, independent PASS2, critical-path map, capability/owner/support boundary, concrete falsifiers and one proposed charter. It **has not** proven full installed-framework behavior, fixed source, granted E1 write authority, merged a branch or released v1.4. The one material CLIENT decision remaining is whether to authorize `AR-V14-CONSOLIDATE` with the stated scope and protected boundaries; normal implementation details and bug recovery are not CLIENT decisions. Before E1, I3 must check fresh remote HEAD, open branch/PR state and known dirty/runtime owners; if source advanced, inspect the delta and reconcile rather than silently using this 2026-11-04 baseline.
