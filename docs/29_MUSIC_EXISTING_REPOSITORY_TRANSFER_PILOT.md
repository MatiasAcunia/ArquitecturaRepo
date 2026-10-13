# v1.2 Transfer Pilot B — Existing MUSIC repository (read-only authority + isolated adapter)

Status: planned follow-up **after** the first synthetic CRUD L3 terminal. This is a capability-level test charter, not authorization to execute, publish, call providers, copy private data, or change any live MUSIC/OWNER state.

## Why MUSIC rather than another toy app

\`MatiasAcunia/music@main\` is an established, separate music-product workstream with extensive CLIENT theory, OWNER-governed I1→I2→I3→I4 identities, a complex Python foundry, channel/family/artifact lineage, independent reviewers, durable SQLite artifacts, third-party rights gates, and a single material execution rule. It is deliberately unlike a small CRUD. Reproducing its actual currentness and limits is more valuable than forcing its test suite green.

Baseline evidence inspected 2026-10-13: MUSIC GitHub \`main@a8ca5376 (abbreviated historical observation)\`; the active \`contracts/ACTIVO.md\` and \`response/ACTUAL.md\` require reconciliation with physical/local catalog evidence, not trust in either summary alone. \`state/CURRENT_BOOTSTRAP_STATE.json\` and \`state/PRODUCT_STATE.json\` retain older currentness dates and are not automatically the live runtime truth. \`state/EXECUTION_SERIALIZATION_CURRENT.json\` caps independent material executions at exactly one. \`state/R1_RIGHTS_PROVENANCE_CURRENT.json\` preserves non-publication and rights holds. MUSIC's \`canonical_catalog.CanonicalCatalog.audit_existing_read_only()\` must not initialize a substitute DB.

**Never use this inspected SHA as a future currentness claim.** Re-fetch and record live MUSIC/OWNER HEADs immediately before the pilot.

## Scope and isolation

1. Complete the CRUD longitudinal pilot first; gather its consolidated failures and fixes before adding a second test route.
2. L3 discovers an existing local MUSIC checkout. Reuse it read-only if possible; do not create duplicate permanent clones or heavy artifact caches. If no checkout exists, one disposable, bounded Git checkout of \`music@main\` is acceptable after inspecting size, privacy, LFS/submodules, access and free disk. Do not download rendered media or private cloud roots merely to make tests pass.
3. Create exactly one **disposable isolated MUSIC-like adoption candidate**, as needed, by a temporary worktree or carefully selected source-only snapshot. Record exact source commit, paths, file and state digests, a clear cleanup owner and rollback. Do not mutate real \`MatiasAcunia/music@main\`, an active local MUSIC Goal/worktree, \`MatiasAcunia/owner\`, CI scheduling, secrets, cloud credentials, channel identities, usage counters or publication.
4. All tester writes occur only in this disposable candidate. Copy only material, authorized source and policy surfaces. If required canonical media/DB are absent or their lineage cannot be verified from Git, record an **expected HOLD**, not replacement data or false acceptance.

## Core hypothesis

An adopter can attach Agentic SDLC v1.2 to an already governed, real repository **without taking over product authority, overwriting existing truth or misrepresenting availability of external assets**. Its optional controls should add demonstrable currentness/recovery/validation value while preserving the project's established semantics.

The starter remains generic: MUSIC's code, channel identities, rights rules and DB schema never become global starter defaults.

## Adversarial gates

### M1. Zero destructive adoption
Show exact before/after hashes of existing policy, CLIENT theory, code and tests. Install only under a recognized project-local control path; no force-overwrite of existing MUSIC state. Existing \`AGENTS.md\`, \`CONFIG.md\`, \`state/\`, \`contracts/\`, \`response/\` and \`src/music_foundry/\` remain canonical and untouched. If the scaffold's generic \`state/PRODUCT_STATE_CURRENT.json\` or technical baseline conflicts with MUSIC's own Product State, classify it as a compatibility/adaptation problem: do not silently establish a second CURRENT owner.

### M2. Identity/authority mapping
Map CLIENT (external), OWNER I1, MUSIC I2 Planner, persistent campaign I3 and optional specialist/reviewer I4 **one-to-one**. Verify that historical Git commits are not actor identity; session reset does not create a new Planner or campaign; fresh I2 is UNTRUSTED until live OWNER Kernel and active-domain theory are read. Reject a fake I4→I2, I3→CLIENT or unapproved L4 material side effect. Do not install a second OWNER or five-task pack into MUSIC by default.

### M3. Canonical theory and conflicts
Reconstruct actual \`state/CLIENT_PRODUCT_REQUIREMENTS_CURRENT.md\`, \`contracts/ACTIVO.md\`, \`response/ACTUAL.md\`, state CURRENTs and relevant OWNER rules. Test contradictory/stale summaries: physically available state supersedes earlier entries, and an uncertain local DB/currentness forces targeted HOLD. No invented CLIENT approval, no new channel binding or change to accepted sonic/product policy. A reorganization must preserve prior decision provenance and supersession.

### M4. Real filesystem/DB semantics
Audit the preexisting SQLite catalog strictly read-only and with existing-only APIs; capture whether the original authorized DB and bound media actually exist in this candidate. A Git checkout is not proof of the external DB, audio, thumbnail or output roots. Do not create a clean replacement to satisfy a test. Probe expected missing-file/HOLD, stale-path, wrong-hash, partial archive, schema/version mismatch and symlink traversal handling. Synthetic fixtures may be used **separately**, always labeled simulation.

### M5. Serial execution and side effects
MUSIC's explicit \`max_concurrent_material_executions=1\` overrides a generic \`ASYNCHRONOUS+TEAM\` preference until CLIENT authorization changes. No real GPU/music/image generation, billing, uploads, OAuth, public usage/track-list mutation or remote publication. Require receipts and independent readback when claiming external effects. Simulate duplicated retries without performing an actual paid provider call.

### M6. Sound/visual rights and product gates
An in-repo test PASS must never become a perceptual review, original-audio ownership, license clearance, six-channel binding or CLIENT publication acceptance. Respect provenance, reviewer-source binding, channel-owned family limits, and historical freeze evidence. A sample that cannot be listened to/seen by the authorized reviewer is HOLD.

### M7. Engineering regression & recovery
Run scoped, non-provider unit/schema/import and representative integration tests in a disposable environment. Separate failures caused by (a) MUSIC-specific source bugs, (b) absent external media/DB, (c) invalid local dependencies/configuration and (d) v1.2 adapter defects. Deliberately fail an import, remove a **test-only** fixture, interrupt a synthetic transaction, invalidate a ref, and prove same-campaign repair without Planner churn, frequent branches or fake PASS. Do not run entire expensive neural/render matrix merely to increase test count.

### M8. Process criticism and transfer quality
L3 observes installation friction, documentation, bootstrap workload, duplicate owner creation, wrong model/provider/stack suggestion, needless scheduler/plugin setup, too much review paperwork, branch/commit mania, disk/time/cost use and genuine reliability gains. Critique the **starter architecture**, not just its Python scripts. Explicitly identify mechanics that MUST be opt-in versus safe, helpful defaults.

### M9. Feedback/privacy/rollback
Prove local strict-metadata reports, outbound opt-out, disabled-state behavior, safe simulation of a collector receipt and zero transmission of MUSIC repo names, channel IDs, paths, DB/audio hashes, rights disputes, private theory or raw failure text. No real external collector is currently configured. Destroy only this pilot's disposable artifacts after recording minimum evidence; leave original MUSIC checkout intact.

## Terminal acceptance and next integration

Deliver one transfer audit with real vs simulated proof, exact live source refs, relevant code paths, evidence hashes, before/after change table, expected vs observed, PASS/FAIL/HOLD per M1–M9, privacy/disk-cost outcomes, reproducible negative tests, and maximum three prioritized systemic v1.2 fixes. Any failure that is specific to MUSIC's own implementation is not automatically an ArquitecturaRepo v1.2 bug.

**Promotion rule:** complete CRUD pilot + MUSIC transfer pilot + clean-install/rollback and security release challenge + exact-head CI + independent test review. Do not promise “all possible scripts” are infallible or claim other operating systems are supported until physically tested. Release 1.2.0 only for features with actual accepted host/adapter evidence; otherwise mark them experimental/unsupported and continue hardening.
