# Architecture Overview

## Design goal

Transfer software-engineering responsibility from the human operator to a durable agent organization without pretending that product authority, external authorization or subjective acceptance can always be automated.

The target is not "many agents." The target is sustained correct continuation.

## Responsibility stack

### CLIENT / Product Owner

Owns intent, constraints, priorities, product preferences, subjective acceptance, business decisions and explicitly reserved external actions.

The client may voluntarily discuss architecture or code, but correct technical continuation should not depend on that intervention.

### I1 MASTER OWNER

Owns the development system across projects/workstreams: global process quality, cross-boundary coherence, reusable infrastructure, Planner/Controller operating quality, systemic failure correction, policy hygiene and portfolio risk.

I1 is not another local Planner.

### I2 PROJECT / WORKSTREAM PLANNER

Owns strategic product-backward reasoning for one independently planned boundary: requirement interpretation, capability architecture, owner/interface/state semantics, strategic currentness, gates, critical path, campaign creation and strategic acceptance.

I2 does not manage every implementation red/green loop.

### I3 ENGINEERING CAMPAIGN LEAD / EXECUTION CONTROLLER

Persistent engineering manager for one authorized campaign.

Owns tactical DAG, implementation details, helper/reviewer topology, retries, tests/evaluators, integration, independent review orchestration, checkpoint/recovery and truthful campaign terminal.

Campaign identity persists across context/model/session changes.

### I4 EXECUTION TEAM MEMBERS

Bounded specialists: builders, reviewers, DB/recovery, runtime, test/fuzz, architecture critics, research, security, performance and integration specialists.

I4 returns evidence to I3. It does not become strategic authority.

## State model

### L0 — Client intent evidence

Recoverable user statements, approvals, rejections, requirement changes and product decisions.

### L1 — Interpreted product authority

Normalized CLIENT requirements plus Product State: what the product currently means, which decisions are active, which questions are open, current gates and evidence pointers.

### L2 — Engineering state

Code, DB/runtime state, architecture, active campaigns, checkpoints, tests, artifacts, retries, exact heads and implementation derivations.

Never ask the CLIENT to reconcile L2 when the system can do it.

## Two graph levels

### Strategic capability graph

Owned by I2/I1. Stable capability nodes and dependencies.

`BLOCKED -> READY -> ACTIVE_CAMPAIGN -> PRODUCT_GATE -> DONE`

### Tactical campaign DAG

Owned dynamically by I3.

`BLOCKED_DEPENDENCY -> READY -> ACTIVE -> VERIFY -> DONE`

I2 chooses the campaign boundary. I3 decides the internal work graph.

## Capability lifecycle

```text
strategic reconstruction
  -> capability/owner/state architecture
  -> campaign charter
  -> continuous implementation
  -> whole-capability verification
  -> independent exact-candidate review
  -> grouped in-scope hardening
  -> strategic acceptance
  -> downstream integration / next capability
```

Avoid `tiny sample -> bug -> patch -> Planner -> another patch -> new campaign`.

## Evidence gates

Keep layers distinct and use only those applicable:

- static / structural;
- unit / property;
- integration;
- DB / currentness / lineage / recovery;
- runtime / physical;
- semantic / generalization;
- security / rights / privacy;
- perceptual / human;
- release / publication;
- live-market / telemetry.

A green lower layer cannot silently satisfy a higher layer.

## Currentness and reconstruction

Every project defines a Currentness Set: the minimum durable surfaces needed to reconstruct one unambiguous current posture.

Continuity-critical transitions either update that set coherently or fail closed with a reconciliation-required state.

## Governance minimization

Every permanent mechanism should answer:

`failure class -> mechanism -> canonical owner -> enforcement/evidence -> falsifier -> rollback/supersession`.

If a rule cannot explain what failure it prevents or detects, do not add it.
