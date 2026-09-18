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

Then validate it:

```bash
python tools/validate_project.py --root "../my-project/.agentic-sdlc"
```

The generated control layer starts in `HOLD / UNTRUSTED_CONTEXT`. It does not invent live code, campaign or acceptance state.

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

Version 0.2 validates more than JSON syntax.

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
- duplicate current owner detection for mechanically identifiable owners.

CI also runs negative fixtures that must fail.

See `docs/10_EXECUTABLE_VALIDATION.md`.

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
- `tools/selftest_validation.py` — adversarial validator self-test.
- `tools/selftest_scaffold.py` — all-profile scaffold self-test.
- `examples/minimal/` — pre-campaign example.
- `examples/active_campaign/` — active campaign/currentness example.
- `examples/terminal_candidate/` — exact-candidate terminal/review example.
- `docs/00_ARCHITECTURE_OVERVIEW.md` through `docs/10_EXECUTABLE_VALIDATION.md` — architecture, adaptation and validation guidance.
- `state/STARTER_MANIFEST.json` — machine-readable starter identity.

## What this is not

- not a guarantee of autonomous software development;
- not a universal architecture proven across arbitrary projects;
- not a reason to create extra agents when one agent is sufficient;
- not a substitute for product-specific tests/runtime/security/perceptual evidence;
- not a project snapshot or historical data export.

This repository contains only reusable structure, generic mechanisms and synthetic examples. It intentionally excludes project-specific names, repositories, branches, identifiers, providers, costs, quantities, artifacts and historical state.

## Status

`v0.2.0 — PUBLIC STARTER PREVIEW`

v0.2 adds executable validation and fail-closed scaffolding. Every fork still has to establish its own product truth and gates.

## License

No explicit open-source license has been selected yet. The repository is public and intended to be forked for experimentation, but a formal reuse license should be selected before treating it as a fully licensed open-source distribution.
