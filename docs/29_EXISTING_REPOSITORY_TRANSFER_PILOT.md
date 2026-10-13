# v1.2 Transfer Pilot B — Existing governed project adoption

Status: planned independently after the initial synthetic CRUD terminal. Not an authorization to mutate any user's active project.

## Hypothesis

Can the public starter attach to an established repository with existing CLIENT theory, ownership, roles, policies, database, code, tests, historical state and external artifacts without introducing a second authority, replacing facts, elevating permissions, activating costly effects, or losing continuity?

Select one user-authorized non-synthetic project. The private repository name, its exact live SHA, internal source paths, identities, product requirements and artifact references belong solely in the **private, user-controlled L3 test packet**, never in this public starter. This document is generic and reusable.

## Isolation

- Read the selected project's canonical authority and workstream rules. First assess whether a local canonical checkout already exists. Avoid duplicate permanent clones, heavy media downloads and redundant worktrees.
- If a copy is needed, create one bounded disposable, explicitly authorized sandbox copy of code and safe metadata only, after disk/privacy/rights preflight. Keep production repos, Goals, scheduled tasks, credentials, protected DB and external effects unchanged.
- Record exact source/head, content hashes, allowed scope, test owner, resource ceiling, rollback and cleanup in the local private evidence folder. Do not commit private identifiers or snippets to the public starter.
- An absent canonical DB, cloud asset, rights clearance, live provider or accepted sample produces expected HOLD. Do not manufacture its replacement to make CI green.

## Required adversarial gates

**B1 — Non-destructive adoption.** Compare hashes of pre-existing application and policy files before/after. The scaffold must not overwrite authoritative state or create competing CURRENT truths. A legal project overlay should coexist with existing governance.

**B2 — Identity and authority.** Reconstruct CLIENT as external, I1 upstream, one domain I2 Planner, the actual persistent campaign I3 and optional I4 participants. Verify that Git commits/model sessions aren't actor identities; role boundaries and reviewer independence survive install and restart. No additional supervisor unless requested.

**B3 — CLIENT lineage/currentness.** Load materially complete actual CLIENT requirements and active domain theory. Resolve stale historical summaries and contradictions against immutable physical evidence, current files, revisions and lineage. No silent reinterpretation or fabricated acceptance.

**B4 — Physical state and data stores.** Audit existing DB and artifact generations read-only. Prove strict existing-only mode, schema, source identity and hashes. Missing external artifacts must fail closed, not cause empty DB recreation or false accepted production state.

**B5 — Runtime modes and concurrency.** Project-specific serialization, resource locks, authorizations and caps override a generic async/team preference. Simulate stale mutators and conflicting writes without invoking real paid APIs. A mode declaration is not scheduler/host proof.

**B6 — Rights, provenance and perceptual/product acceptance.** Software tests do not automatically establish rights, licensing, human quality gates or publication permission. Keep all external gates independent and reversible.

**B7 — Selective engineering regression and recovery.** Run a bounded, representative source/test subset without destructive environment change or provider calls. Distinguish starter adapter errors from project defects, missing external data, dependency failures and hardware/OS limitations. Test a synthetic bad config, interrupted transaction, stale source, attempted retry and reviewer rejection; same I3 campaign absorbs in-scope repair.

**B8 — Process criticism.** Quantify onboarding friction, duplicate policies, extra branches/commits, unnecessary clones, wasted agent/tool invocations, unexpected model/API cost and time-consuming steps. Evaluate whether the starter simplifies real engineering rather than merely producing more docs/scripts.

**B9 — Privacy and rollback.** Show local metadata-only feedback, opt-out, zero private identifiers/payload in public or outbound artifacts, collector mock receipt, restored sandbox state and temporary-artifact cleanup. Do not transmit to an unverified external endpoint.

## Acceptance and honest limitations

One sanitized, evidence-backed transfer audit gives PASS / FAIL / HOLD / NOT_APPLICABLE for B1–B9, expected-vs-observed result, real-vs-synthetic provenance, no-leak proof, reproducible system-level defects and at most three prioritized corrective recommendations. Missing paid media/DB/publication should remain documented HOLD rather than blocking evaluation of independent, testable features.

Do not count a project's own failing application script as a starter defect without causal reproduction at the adapter boundary. Do not imply the test proves all project categories, operating systems, model providers or paid integrations.

Release gate: initial CRUD + this transfer pilot + clean reinstall and rollback + exact-head CI + independent adversarial acceptance, then publish only proven features. Preserve the stable branch until those gates pass.

## Preflight-only existing governance attachment

Use [read-only reference preflight](32_EXISTING_GOVERNED_ATTACHMENT.md) before normal adoption. A successful owner-reference check is **not** an operational attachment and does not pass B1–B9; the exact L3 transfer failure and DB/host currentness must be reconciled before any authoritative migration.
