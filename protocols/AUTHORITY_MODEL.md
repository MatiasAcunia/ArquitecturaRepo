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

## 2026-10-19 Portable role semantics and policy ownership

I1/I2/I3/I4 are role identifiers; L2/L3/L4 are optional practical names independent of a vendor/model codename. If model selection is reserved to the CLIENT by the installed project's authority, I2/I3 cannot override it. Otherwise project-local cost, capacity, privacy, verified availability and delegated decision rights govern selection; there is no public starter default for a model or reasoning setting. An installed multi-project controller may enforce one shared code-writer resource if actually configured, but this public template does not create a portfolio-global lock or native desktop host authority.

Rule ownership: R0 CLIENT intent/model/publish, R1 portable authority taxonomy, R2 Planner Kernel and Execution Team OS, R3 Capability Lifecycle & Evidence plus product-local named engine manifests/versions, R4 actual charter/Goal authority, R5 product gate owners, R6 host_dispatch/engineering_packet/artifact_ledger/cognitive_i4, R7 live project Product State and active journal, R8 historic documents. Root AGENTS/CONFIG are navigation, not a second current rule source. Installed projects may have stronger owner rules; never import the private managed portfolio's volatile state into the public template.
