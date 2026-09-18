# Agentic SDLC Starter Architecture

A forkable starter for building a durable multi-agent software-development system around a real project.

The core idea:

> The human should be able to act primarily as a CLIENT / product owner, while the agent system owns the technical SDLC: reconstruction, planning, architecture, implementation, testing, verification, integration, recovery, continuation, and process improvement.

This repository is not a prompt collection. It is an operating architecture for long-running agentic software development.

## What you get

The starter defines four internal engineering roles:

`MASTER OWNER -> PROJECT PLANNER -> ENGINEERING CAMPAIGN LEAD -> EXECUTION TEAM MEMBERS`

with the CLIENT outside the engineering organization.

It provides:

- durable CLIENT intent and Product State;
- repository-first fresh-context reconstruction;
- currentness, supersession and fail-closed rules;
- identity/run/execution-authority separation;
- strategic capability planning;
- persistent engineering campaigns;
- dynamic tactical DAGs;
- exact-candidate independent review;
- distinct verification gates;
- state/DB/lineage/idempotency semantics;
- checkpoint/recovery/capacity semantics;
- optional storage, cost, security/privacy/rights and MASTER OWNER modules;
- machine-readable schemas;
- cross-file relationship validation;
- fail-closed scaffolding by project profile;
- optional durable Campaign Lead runtime/controller;
- fail-closed multi-file transition journaling and crash recovery;
- backward-compatible schema evolution with explicit migrations;
- canonical owner registry with verifiable supersession lineage;
- deterministic fresh-context reconstruction;
- a physical stateful reference system with transfer evidence;
- six-shape fail-closed transfer/adoption workflow;
- centralized control-state transaction/recovery primitives;
- executable v1 release criteria and stopping rule;
- positive and adversarial CI fixtures.

## Quick start

### Option A — ask an agent to adapt the architecture

1. Fork this repository.
2. Give the agent access to the fork and the target project.
3. Paste `prompts/INSTALL_THIS_SDLC.md`.
4. Require read-only discovery before material mutation.
5. Run the fresh-context probe before claiming installation success.

### Option B — create a fail-closed scaffold first

```bash
python tools/scaffold_project.py \
  --target "../my-project" \
  --profile SMALL \
  --product-id PROJECT_ALPHA \
  --objective "Describe the client-visible product objective."
```

The generated control layer starts in `HOLD / UNTRUSTED_CONTEXT`. It does not invent live code, campaign or acceptance state.

To include the optional runtime:

```bash
python tools/scaffold_project.py \
  --target "../my-project" \
  --profile STATEFUL \
  --product-id PROJECT_ALPHA \
  --objective "Describe the client-visible product objective." \
  --with-runtime
```

Generated control layers carry their own schemas, validator and validation dependency declaration.

For a project with substantial existing history, use `prompts/REANCHOR_EXISTING_PROJECT.md`.

## Architecture in one picture

```text
CLIENT / PRODUCT OWNER
        |
        v
I1  MASTER OWNER                     optional as a separate active role
    shared system/process coherence
        |
        v
I2  PROJECT / WORKSTREAM PLANNER
    product-backward strategy + capability architecture
        |
        v
I3  ENGINEERING CAMPAIGN LEAD / EXECUTION CONTROLLER
    persistent tactical engineering + integration
        |
        +-------------------+-------------------+
        v                   v                   v
I4  BUILDER            REVIEWER            SPECIALISTS
    implementation      falsification        DB/runtime/test/security/etc.
```

State is intentionally split:

```text
L0  CLIENT INTENT EVIDENCE
L1  NORMALIZED REQUIREMENTS / PRODUCT STATE
L2  ENGINEERING STATE / CAMPAIGNS / CODE / DB / RUNTIME
```

A fresh agent must be able to reconstruct the same legal next action from durable evidence without relying on chat memory.

## Core principles

1. Physical/live evidence outranks summaries and memory.
2. One concern has one canonical owner.
3. Product intent is not implementation state.
4. Worker PASS is evidence, not acceptance.
5. A lower verification gate never substitutes for a higher one.
6. Planner owns strategy; Campaign Lead owns tactics.
7. Ordinary in-charter defects stay inside the same campaign.
8. Campaign identity survives model invocations and context resets.
9. Progress means capability unlock, gate advance or real risk reduction — not commits, prompts, tests or token volume.
10. The CLIENT should not be required to reconcile technical state.
11. Material product decisions made in conversation must become durable state.
12. Governance must pay rent.

## Profiles

Public profiles:

- `SMALL`
- `STATEFUL`
- `ARTIFACT_HEAVY`
- `MULTI_WORKSTREAM`
- `MULTI_PRODUCT`
- `HIGH_CONSEQUENCE`

Profiles select optional mechanism families. They do not manufacture project-specific authority.

See `docs/06_SCALING_PROFILES.md` and `docs/09_ADAPTATION_DECISION_TREE.md`.

## Executable validation

The validator checks more than JSON syntax.

Current checks include:

- JSON Schema validation;
- Product State -> campaign charter consistency;
- capability ownership references;
- Currentness Set path resolution;
- actor/run/execution-authority consistency;
- checkpoint/current-ref consistency;
- bootstrap/Product State consistency;
- terminal/review exact-candidate consistency;
- evidence coverage for required charter gates;
- campaign-runtime DAG/dependency/currentness integrity;
- runtime checkpoint/authority/Product State coherence;
- producer/reviewer separation;
- pending transition-journal rejection;
- duplicate current owner detection for mechanically identifiable owners.

CI also runs negative fixtures that must fail.

See `docs/10_EXECUTABLE_VALIDATION.md`.

## Optional reference runtime

`tools/campaignctl.py` is a durable local Campaign Lead control-plane reference. It supports tactical DAG mutation, dependency-aware work, execution authority, checkpoints, exact review freeze, strategic terminals, exclusive mutation locking and fail-closed multi-file recovery.

Critical currentness transitions are staged and journaled before canonical files are replaced. A crash leaves `runtime/transactions/CURRENT_TRANSACTION.json`; normal inspection/mutation fails closed until explicit `campaignctl recover` succeeds. External hash conflicts are preserved as `CONFLICT` rather than overwritten.

See `docs/11_REFERENCE_RUNTIME.md` and `docs/12_TRANSACTION_RECOVERY.md`.

## Schema evolution

State formats evolve explicitly rather than being rewritten in place. The migration registry keeps legacy and latest versions separate, new scaffolds emit the latest schema, and existing supported versions continue to validate until compatibility is intentionally retired.

`tools/migrate_state.py` supports read-only planning, explicit apply, reversible migration when a lossless reverse exists, idempotent re-apply, and fail-closed downgrade when newer semantics cannot be represented by the old contract.

The first real evolved contract is `CURRENT_BOOTSTRAP`: legacy `starter-bootstrap-0.1` remains supported while new scaffolds emit structured `starter-bootstrap-0.2`.

See `docs/13_SCHEMA_EVOLUTION.md`.

## Canonical ownership

New scaffolds include `state/OWNER_REGISTRY_CURRENT.json` for durable control-layer concerns. Each represented concern must have exactly one CURRENT owner; older owners remain explicit SUPERSEDED lineage.

Validation binds CURRENT local owners to physical surfaces and, where declared, Product State currentness. Known concerns are also cross-checked against bootstrap/Product State refs. Dangling lineage, one-sided supersession, cycles, cross-concern supersession and duplicate CURRENT owners fail validation.

Existing forks without an owner registry remain supported; this is an extensible ownership mechanism, not a forced rewrite of old projects.

See `docs/14_CANONICAL_OWNERSHIP.md`.

## Fresh-context reconstruction and reference system

`tools/reconstruct_context.py` validates a control layer first and then emits one deterministic current posture from durable evidence only. It refuses to summarize through invalid currentness, duplicate owners or pending recovery state.

`examples/stateful_backend/` is the first physical transfer fixture: a real SQLite note store with idempotency, rollback, restart persistence and concurrent replay tests, bound to a separate Agentic SDLC control layer. CI requires application behavior, control validation and reconstruction to pass together.

See `docs/15_STATEFUL_REFERENCE_AND_TRANSFER.md`.

## Transfer/adoption workflow

Generated scaffolds include read-only discovery, explicit adoption-spec application and generic state-transaction recovery. Adoption preflights a complete candidate control layer before canonical mutation, then promotes requirements/Product State/bootstrap/owners/overlay as one journaled transaction.

CI applies the workflow to six unrelated synthetic project shapes: SMALL, STATEFUL, ARTIFACT_HEAVY, MULTI_WORKSTREAM, MULTI_PRODUCT and HIGH_CONSEQUENCE. It requires deterministic discovery, application-file preservation, profile-proportional mechanism burden, retry-idempotence, validation, fresh-context reconstruction and crash recovery.

See `docs/16_TRANSFER_ADOPTION.md`.

## Release-candidate hardening

Runtime, schema migration and adoption now share `tools/state_tx.py` for local locking/durable transaction semantics instead of maintaining parallel implementations.

The 1.0 definition of done is machine-readable at `state/V1_RELEASE_CRITERIA.json` and executable with:

```bash
python tools/verify_v1_release.py
```

The release gate covers structure/public boundary, contract instances, falsification, profile proportionality, schema evolution, ownership, fresh-context reconstruction, physical stateful behavior, six-shape adoption, resumable campaign runtime and hardening/bounded governance.

See `docs/17_V1_RELEASE_GATES.md` and `docs/18_RELEASE_CANDIDATE_HARDENING.md`.

## Repository map

- `AGENTS.md` — root instructions.
- `protocols/` — reusable operating semantics.
- `schemas/` — machine-readable contracts.
- `templates/` — current-state/campaign/identity/installation templates.
- `profiles/` — machine-readable installation profiles.
- `prompts/` — install, re-anchor, fresh-context and MASTER OWNER prompts.
- `tools/validate_structure.py` — starter structure/leak validator.
- `tools/validate_project.py` — schema + relationship validator.
- `tools/scaffold_project.py` — fail-closed project scaffold generator.
- `tools/campaignctl.py` — optional durable Campaign Lead runtime.
- `tools/migrate_state.py` — explicit state-schema migration planner/executor.
- `tools/reconstruct_context.py` — validate-first deterministic fresh-context reconstruction.
- `tools/discover_project.py` — deterministic read-only project inventory.
- `tools/apply_adoption.py` — preflighted, journaled adoption promotion.
- `tools/state_tx.py` — canonical local control-state transaction/recovery engine shared by runtime, migrations and adoption.
- `tools/verify_v1_release.py` — executable complete v1 release gate.
- `tools/selftest_validation.py` — adversarial validator self-test.
- `tools/selftest_scaffold.py` — all-profile scaffold self-test.
- `tools/selftest_runtime.py` — crash/recovery and runtime lifecycle self-test.
- `tools/selftest_migrations.py` — forward/reverse/idempotence/lossy-downgrade migration self-test.
- `tools/selftest_ownership.py` — owner/currentness/supersession falsification self-test.
- `tools/selftest_reconstruction.py` — fresh-context determinism/fail-closed self-test.
- `tools/selftest_stateful_reference.py` — physical SQLite + control-layer transfer self-test.
- `tools/selftest_adoption.py` — six-shape adoption, proportionality and crash-recovery self-test.
- `tools/selftest_contracts.py` — canonical contract-instance validation suite.
- `tools/selftest_hardening.py` — primitive-centralization and bounded-governance self-test.
- `examples/minimal/` — pre-campaign example.
- `examples/active_campaign/` — active campaign/currentness example.
- `examples/terminal_candidate/` — exact-candidate terminal/review example.
- `examples/stateful_backend/` — physical stateful implementation + control-layer reference system.
- `docs/00_ARCHITECTURE_OVERVIEW.md` through `docs/18_RELEASE_CANDIDATE_HARDENING.md` — architecture, adaptation, validation, runtime, recovery, schema evolution, ownership, transfer and release-gate guidance.
- `state/STARTER_MANIFEST.json` — machine-readable starter identity.

## What this is not

- not a guarantee of autonomous software development;
- not a universal architecture proven across arbitrary projects;
- not a reason to create extra agents when one agent is sufficient;
- not a substitute for product-specific tests/runtime/security/perceptual evidence;
- not a project snapshot or historical data export.

This repository contains only reusable structure, generic mechanisms and synthetic examples. It intentionally excludes project-specific names, repositories, branches, identifiers, providers, costs, quantities, artifacts and historical state.

## Status

`v0.9.0 — PUBLIC STARTER PREVIEW`

v0.9 is the release candidate: duplicated local transaction/locking primitives are centralized, governance proportionality is frozen by tests, and the complete v1 definition of done is executable. No new generic feature is planned before 1.0.

## License

No explicit open-source license has been selected yet. The repository is public and intended to be forked for experimentation, but a formal reuse license should be selected before treating it as a fully licensed open-source distribution.
