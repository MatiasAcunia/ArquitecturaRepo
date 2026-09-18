# Agentic SDLC Starter Architecture

A forkable starter for building a durable multi-agent software-development system around a real project.

The core idea:

> The human should be able to act primarily as a CLIENT / product owner, while the agent system owns the technical SDLC: reconstruction, planning, architecture, implementation, testing, verification, integration, recovery, continuation, and process improvement.

This repository is not a prompt collection. It is an operating architecture for long-running agentic software development.

## What you get

The starter defines four internal engineering roles:

`MASTER OWNER -> PROJECT PLANNER -> ENGINEERING CAMPAIGN LEAD -> EXECUTION TEAM MEMBERS`

with the CLIENT outside the engineering organization.

It also provides:

- durable CLIENT intent and requirements;
- Product State separated from Engineering State;
- repository-first fresh-context reconstruction;
- currentness, supersession and fail-closed rules;
- strategic capability planning instead of patch-by-patch prompting;
- persistent engineering campaigns that survive model/session changes;
- dynamic tactical DAGs owned by the Campaign Lead;
- independent exact-candidate review;
- distinct verification gates: unit, integration, state/currentness, runtime, semantic, perceptual, security/rights, release;
- checkpoint/recovery semantics;
- interaction provenance so product decisions made in chat do not disappear;
- templates for requirements, Product State, campaign charters, checkpoints and terminals;
- ready-to-paste prompts for adapting the architecture to another project.

## Quick start

1. Fork this repository.
2. Give your coding/repository agent read/write access to the fork and to the project you want to manage.
3. Paste the prompt in `prompts/INSTALL_THIS_SDLC.md`.
4. Let the agent perform read-only discovery first.
5. Answer only genuine product/client questions. Do not become its debugger or technical project manager.
6. Require the agent to persist the adapted architecture and run a fresh-context reconstruction test before beginning material implementation.

For an existing project with substantial history, use `prompts/REANCHOR_EXISTING_PROJECT.md`.

## Architecture in one picture

```text
CLIENT / PRODUCT OWNER
        |
        v
I1  MASTER OWNER
    system/process coherence
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
12. Governance must pay rent. Do not add a process layer unless it prevents or detects a real failure class.

## Repository map

- `AGENTS.md` — root instructions for agents entering this starter.
- `docs/00_ARCHITECTURE_OVERVIEW.md` — complete conceptual map.
- `docs/01_FORK_AND_BOOTSTRAP.md` — adaptation procedure.
- `docs/02_RESEARCH_BASIS_AND_LIMITS.md` — evidence philosophy and claim boundaries.
- `docs/03_MECHANISM_SELECTION.md` — generic mechanism-selection criteria.
- `docs/04_FAILURE_MODES.md` — failure classes the architecture is designed to contain.
- `docs/05_MINIMUM_VIABLE_PROFILE.md` — smallest useful installation.
- `docs/06_SCALING_PROFILES.md` — when to add stateful/artifact/workstream/portfolio/high-consequence mechanisms.
- `docs/07_FRESH_CONTEXT_TEST.md` — reconstruction acceptance test.
- `docs/08_REFERENCE_PROJECT_LAYOUT.md` — reference ownership/layout patterns.
- `docs/09_ADAPTATION_DECISION_TREE.md` — profile/mechanism selection logic.
- `docs/ROADMAP.md` — planned evolution after v0.1.
- `protocols/` — reusable operating semantics.
- `templates/` — canonical state/charter/identity/installation templates.
- `prompts/` — installation, reconstruction and optional MASTER OWNER prompts.
- `schemas/` — machine-readable state/campaign/identity contracts.
- `examples/minimal/` — fully synthetic small-project example.
- `state/STARTER_MANIFEST.json` — machine-readable starter identity.
- `tools/validate_structure.py` — structure/JSON/leak-safety validator.

## What this is not

- not a guarantee of autonomous software development;
- not a universal architecture proven across arbitrary projects;
- not permission to hide uncertainty behind more agents;
- not a reason to create extra agents when one agent is sufficient;
- not a substitute for tests, runtime evidence or human product judgment;
- not a project snapshot or a historical data export.

This repository contains only reusable structure, generic protocols, templates and synthetic guidance. It intentionally excludes project-specific names, repositories, branches, identifiers, providers, costs, product counts, artifacts and historical state.

## Status

`v0.1.4 — PUBLIC STARTER PREVIEW`

The architecture is usable as a starter, but every fork must validate the mechanisms in its own environment.

## License

No explicit open-source license has been selected yet. The repository is public and intended to be forked for experimentation, but a formal reuse license should be selected before treating it as a fully licensed open-source distribution.
