# Failure Modes This Architecture Is Designed to Contain

The starter exists because long-running agentic projects fail in ways that one-shot coding prompts do not expose.

## 1. Chat-memory authority

Failure: the agent treats previous conversation memory as current truth.

Containment: durable state, explicit currentness, fresh-context reconstruction.

## 2. Stale-current state

Failure: several files claim to be CURRENT but disagree.

Containment: one concern/one owner, Currentness Set, fail-closed reconciliation.

## 3. Worker PASS becomes product PASS

Failure: a producer reports success and downstream work proceeds without independent evidence.

Containment: exact-candidate evidence, independent review, separate acceptance gates.

## 4. Gate substitution

Failure: green unit tests are treated as runtime, semantic, perceptual or release acceptance.

Containment: explicit layered gates.

## 5. Planner micromanagement

Failure: every test failure returns to strategic planning.

Containment: persistent I3 Campaign Lead with broad tactical authority.

## 6. Campaign ends because a model invocation ends

Failure: context/token/capacity boundaries create fake strategic terminals.

Containment: durable checkpoints and same-campaign resume semantics.

## 7. Controller under-ownership

Failure: I3 behaves as a dispatcher and asks Planner/client to choose retries, fixes and tactical decomposition.

Containment: dynamic tactical DAG and explicit I3 decision rights.

## 8. Goal tunneling

Failure: a local technical objective passes while the final product is still wrong.

Containment: product-backward Planner reasoning and strategic terminal review.

## 9. Duplicate governance

Failure: every incident creates a new policy/file, producing contradictory authority.

Containment: one concern/one canonical owner and governance-pay-rent rule.

## 10. Client technical escape

Failure: the human becomes debugger, architect, state reconciler or agent coordinator simply to keep progress alive.

Containment: explicit client boundary and technical-escape classification.

## 11. Evaluator leakage

Failure: the same generator, fixture or producer-owned metadata makes the evaluator pass.

Containment: producer/evaluator separation, frozen exact candidate, adversarial/independent derivation.

## 12. Product-specific state leaks across reusable infrastructure

Failure: reuse silently copies another project's volatile state or assumptions.

Containment: shared mechanism, isolated Product State.

## 13. Unbounded parallelism

Failure: more agents create write collisions, shared-resource corruption or integration burden.

Containment: resource/write-set isolation and benefit-based parallelism.

## 14. Artifact accumulation

Failure: renders, samples, caches and failed attempts consume storage indefinitely.

Containment: explicit artifact lifecycle and terminal cleanup.

## 15. Historical detail beats current evidence

Failure: a detailed old plan appears more authoritative than a sparse current state.

Containment: evidence precedence and supersession semantics.

## 16. Governance exists only on paper

Failure: documented rules are mistaken for physically enforced or effective mechanisms.

Containment: distinguish declared design, materialized mechanism, physical exercise and accepted capability.
