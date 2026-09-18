# Fork and Bootstrap

## Goal

Turn this generic starter into the durable SDLC control layer for a real project without importing irrelevant historical baggage.

## A — Read-only discovery

Inspect the final product/objective, repository topology, branches, code architecture, DB/state/runtime, CI/tests, deployment/release model, artifacts/evidence, existing agent instructions, known product decisions and external/paid/destructive boundaries.

Do not ask the CLIENT technical questions repository/runtime evidence can answer.

## B — Product authority capture

Create project-owned equivalents of:

- `state/CLIENT_REQUIREMENTS_CURRENT.md`;
- `state/PRODUCT_STATE_CURRENT.md`;
- interaction evidence for material CLIENT changes.

Separate confirmed requirement, explicit decision, quality bar, strong preference, direction, implementation suggestion, open question and superseded decision.

Do not freeze brainstorming into architecture.

## C — Project topology

Decide whether the target needs one Project Planner, multiple workstreams under one product, or multiple separate products under one OWNER.

Do not create boundaries just to justify more agents.

## D — Currentness Set

Define the smallest current surface set a fresh role must read, for example:

```text
AGENTS.md
state/CLIENT_REQUIREMENTS_CURRENT.md
state/PRODUCT_STATE_CURRENT.md
state/CURRENT_BOOTSTRAP_STATE.json
state/ACTIVE_CAMPAIGN.md
latest exact code/DB/runtime evidence pointers
```

Your target may use different names. One concern should have one canonical owner.

## E — Project overlay

Create a thin local overlay defining only project-specific product theory, architecture invariants, current owners, DB/state semantics, gates, runtime/platform constraints and release rules.

Do not duplicate generic role/process protocols.

## F — Capability map

Work backwards from the final product.

For each capability record purpose, owner, dependencies, current physical state, hard gate, downstream consumers and next legal boundary.

Prioritize the smallest materially complete capability on the real critical path.

## G — Fresh-context probe

Use a genuinely fresh agent/context.

It should reconstruct without technical CLIENT rescue: role/non-role, product objective, requirements/current decisions, current state, authority, active campaign, gate/evidence and next legal action.

If it cannot, improve durable state/navigation before scaling execution.

## H — First campaign

The Planner creates one strategic campaign charter.

The Campaign Lead challenges the charter against live state and, if accepted, owns continuous tactical work until a truthful strategic terminal.

Do not route every defect back to Planner.

## Minimum viable installation

A small project does not need every advanced mechanism on day one.

Minimum:

1. role boundary;
2. current requirements;
3. Product State;
4. currentness/reconstruction;
5. campaign charter;
6. exact candidate + independent review;
7. distinct acceptance gate.

Add Sentinel, richer interaction instrumentation, portfolio OWNER automation, storage policy, dynamic multi-lane execution and advanced state machinery only when the project creates those failure classes.
