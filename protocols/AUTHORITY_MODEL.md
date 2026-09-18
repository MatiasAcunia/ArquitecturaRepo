# Authority Model

## First-class roles

`I1 MASTER OWNER -> I2 PROJECT/WORKSTREAM PLANNER -> I3 ENGINEERING CAMPAIGN LEAD -> I4 EXECUTION TEAM MEMBER`

CLIENT is external.

### I1 MASTER OWNER

Global/process/system authority. Owns shared architecture/process, systemic defects, cross-boundary coherence and role/runtime quality.

### I2 PLANNER

Strategic authority for one independently planned project/workstream. Owns product interpretation, capability architecture, owner/interface/state semantics, gates, critical path, campaign charters and strategic acceptance.

### I3 CAMPAIGN LEAD

Persistent tactical authority inside one valid charter. Owns tactical DAG, implementation, retries, tests, reviewers, integration, checkpoint/recovery and campaign terminal.

### I4 TEAM MEMBER

Bounded executor/reviewer/specialist. Owns only assigned work/evidence.

## Challenge without authority theft

Lower roles may challenge upstream authority with evidence.

- I4 -> I3 for assignment evidence.
- I3 -> I2 for charter invalidation/strategic terminal.
- I2 -> I1 for systemic/shared defects.
- I1 -> CLIENT only for genuinely client-owned decisions.

Challenge does not transfer authority.

## Rule classes

Use these conceptual classes when useful:

- R0 CLIENT/product authority
- R1 global organizational invariant
- R2 role operating rule
- R3 product/domain invariant
- R4 campaign constraint
- R5 gate/evidence rule
- R6 transport/runtime mechanism
- R7 volatile current state
- R8 historical/contextual evidence

Do not let R8 historical detail override R7 current state or R0 current client authority.

## One concern, one owner

Before adding a new file/policy, identify the existing owner.

Duplicate current truth is a currentness bug waiting to happen.
