# Agentic SDLC v1.2 — operational candidate and acceptance boundary

Status: IMPLEMENTATION IN PROGRESS, not a 1.2.0 release. The stable public starter remains 1.1.0 until the physical gates listed in state/V1_2_ACCEPTANCE_CRITERIA.json pass.

## Purpose

v1.2 transfers observed generic failure classes into an opt-in operational layer:
Goal and tactical planning integrity; no stale authority after invocation; ambiguous external effects; evidence-bound independent decisions; optional cognitive specialists; safe host continuity; multi-product coordination; and privacy-preserving feedback.

Do not equate a passing code test with a model-host integration, user consent, a physical review or a public release.

## What is implemented in the candidate

- tools/goal_guard.py: fail-closed, read-only Goal/charter/authority-ref checksum, mutable-plan binding and optional required canonical store presence. Returns HOLD when the current host/remote preflight is not proven. A host must actually invoke it before every material Goal/task call. A command-line flag is not independent evidence that a hook ran.
- tools/goal_plan.py: transactionally append an I3-owned tactical plan revision using the existing state_tx lock/journal and optimistic revision check. An immutable Goal cannot be silently rebased. The 120-minute threshold refers to verified active-progress time, not wall-clock time.
- tools/external_effects.py: pre-dispatch durable ambiguity record, same-logical-ID idempotency and receipt declaration. Provider readback must be independently verified by a real adapter before acceptance; this module is not a cloud API client.
- tools/cognitive_i4.py: deterministic material-event due check, fail-closed privacy and quota decisions, optional Gemini JSON transport for PUBLIC_OR_SYNTHETIC input only. Successful receipt remains DELIVERED_PENDING, not CONSUMED/ACCEPTED.
- tools/owner_task_recovery.py: pure, five-role mutual-recovery decision policy that respects explicit CLIENT or platform suspensions and never edits scheduler metadata. Actual scheduler integration/readback is a separate gate.
- tools/selftest_operational_v12.py: synthetic and adversarial tests without network calls or mutations to real projects.

These tools are only copied into profiles that request the optional runtime or OWNER-compatible multi-product role. SMALL does not silently activate a resident supervisor or an LLM.

## Goal contract

An I2-authorized installation can place state/GOAL_CONTRACT_CURRENT.json with:

- schema_version: agentic-goal-contract-v1
- goal_id, campaign_id, definition_of_done
- charter_ref, charter_sha256, authority_refs (repository-local exact paths + hashes)
- hard_gates, forbidden_effects, write_envelope
- optional canonical_store with required=true, ref, and optional exact checksum

I3 then runs goal_plan.py with an expected revision and tactical-plan input. Material reentry is HOLD unless the actual host adapter independently verifies canonical remote, the invocation hook and authority. Missing Goal is NOT_CONFIGURED, not implicit permission to run.

The currently shipped core campaignctl, transaction engine, scaffolder, validator and six profile contracts remain the authoritative v1.1 base. v1.2 must integrate with those owners rather than fork a parallel controller.

## Host continuity / Codex Daily Control

The relevant Windows reference is Codex Daily Control **2.0.2-hardening-candidate**, not 2.0.1. Its reported Windows installation successfully validated native CLI/app-server, Goals/threads/history, per-account quota, staging, checksum/ZIP, and project binding. This source repository does not ship its Windows package, claim to manage private native Codex SQLite or assume undocumented Resume methods.

Before any v1.2 Codex support label becomes SUPPORTED, a separate, non-destructive Windows test must verify:
- app-server/Goal lifecycle compatibility with the actual installed build;
- one exact suspended-for-quota Goal resumes only under verified current ordinary 300-minute usage authorization;
- paused, complete, blocked or budget-limited Goals never resume accidentally;
- installation/restart rollback, foreground calibration, Goal and thread identity, safe closeout and durable daypack/cloud readback;
- active writer and remote-receipt failures produce HOLD; old chat is not deleted;
- actual Goal pre-dispatch guard, recurring plan check, and I4 advice delivery to the same I3 without a manual relay.

Until then, CODEX_DESKTOP_GOAL_ADAPTER_NOT_YET_PROVEN is mandatory.

## Gemini cognitive lane

I3 remains the hands-on persistent engineering owner. Gemini may be an optional read-only I4 planning, challenge or anti-churn input, **never a replacement for I3, Planner acceptance, security or physical review**. Material entry, evidence changes, repeated failure and a long active Goal are consultation due checks; due does not imply a paid call. Per-provider key, model, quotas, legal basis, export scope, budget and data use must be verified. No private/source code is exported by default. Provider output must reach I3 with exact source and response digests and receive a later, explicit I3-consumption acknowledgment and test/proof; receiving a JSON response alone is not the acceptance gate.

## Optional five-task OWNER pack

The logical roles are Delivery, Architecture, Quality, Integrator and Master. Do not install them on a single small project. Scheduling requires an explicit scheduler adapter, exactly five discovered task IDs, preservation of prompts/cadence/titles, safety suspensions and verified readback. No sixth supervisory agent. A disabled task due to user instruction is never revived. A pure simulation test is not live scheduler acceptance.

## Privacy: automatic minimal monthly feedback

**ON by default:** the installer copies a read-only monthly GitHub Actions workflow and a config file with enabled=true, cadence=MONTHLY, artifact_enabled=true, privacy_mode=STRICT_METADATA_ONLY. Each scheduled run constructs a short allowlisted metadata report in the user's own repository Actions artifact (30-day retention). It helps the maintainer improve starter structure, migration ergonomics, failure categories and setup defaults.

**Exactly what it contains:** starter version/profile, whether the optional runtime is installed, booleans/status enumerations about validation, bootstrap/currentness, baseline, campaign state, counts of owners/capabilities/milestones/work units, recovery/retries/holds, and the operating-review rating. It excludes code, product identifiers, repo names, requirements, messages, usernames, paths, SHAs, credentials, file contents and unbounded free text. It is not acceptance evidence or product state.

**External transmission:** default preference ON when a named verified receiving endpoint exists; currently no endpoint is configured, so actual external sending remains NOT_PROVEN and users can opt out. No claim that the maintainer automatically receives private-project reports merely because an artifact exists. A verified collector, anonymous receipt, consent/disable UX and leakage falsifiers remain required for an external feedback product claim. No silent upload.

**Disable:** set feedback/ARCHITECTURE_FEEDBACK_CONFIG.json enabled=false, or remove the managed .github/workflows/agentic-sdlc-feedback.yml, or scaffold with --no-feedback-workflow. There is no penalty or functionality loss. The user may inspect reports and change cadence.

## Validation and release

Run:

    python tools/verify_v1_release.py
    python tools/selftest_operational_v12.py
    python tools/verify_v12_candidate.py
    python tools/verify_v12_candidate.py --require-release-ready

The last command intentionally returns nonzero until physical and external gates are proved. Never change this behavior simply to paint CI green.

All six existing profiles, older scaffolds, schema migrations and v1.1 release tests must remain compatible. No forced rewrite of installed control layers; new contracts remain absent until explicitly authorized. A production 1.2.0 release additionally needs Windows and Gemini real-host proof, independent adoption, effective scheduler review, privacy audit, validated external effects, exact HEAD CI and honest feature-support reporting.

## Known unproven capabilities

- Actual Codex Goal host pre-dispatch and native lifecycle integration
- Verified consumer receipt of Gemini consultation by a continuing Goal
- Verified external-effect receipt by independent provider adapter
- Real five-task scheduling and mutual recovery
- Maintainer-owned collector and anonymous receipt
- Independent unrelated-project adoption and Windows rollback

Do not call these completed features.
