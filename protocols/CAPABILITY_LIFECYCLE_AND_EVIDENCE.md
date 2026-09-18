# Capability Lifecycle and Evidence

## Unit of progress

Progress is:

- functional capability unlock;
- required quality-gate advance;
- real risk reduction.

Not progress by itself:

- commits;
- prompts;
- agents;
- tests;
- hours;
- tokens;
- documents.

## Lifecycle

`RECONSTRUCT -> ARCHITECT -> CHARTER -> BUILD -> VERIFY -> INDEPENDENT REVIEW -> HARDEN -> ACCEPT -> INTEGRATE`

## Capability scope

Prefer a materially complete path such as:

`input -> validation -> orchestration -> persistence -> output -> downstream handoff`.

Do not make one bug/sample exception the strategic unit.

## Verification layers

Use the applicable set:

1. static/structural;
2. unit/property;
3. integration;
4. DB/currentness/lineage/recovery;
5. runtime/physical;
6. semantic/generalization;
7. security/rights/privacy;
8. perceptual/human;
9. release/publication;
10. live-market/telemetry.

Never silently substitute one for another.

## Independent review

For material exact-candidate gates:

- reviewer identity differs from producer;
- reviewer binds exact candidate head/digest/state;
- reviewer receives charter and evidence, not a desired verdict;
- review attempts to falsify;
- in-scope defects return to the same I3 campaign;
- producer mutation after review freeze invalidates favorable review if material.

## Evidence relationship

Treat terminal evidence as a relationship graph, not a pile of green files.

Where applicable verify consistency among:

`current state -> execution authority -> checkpoint -> candidate -> review freeze -> reviewer reconstruction -> verdict -> terminal`.

## Samples

Tiny samples are smoke diagnostics.

Formal evidence scale should match risk and cost.

Do not swap failed frozen members merely to recover PASS.

## Product acceptance

Machine evidence can establish machine properties.

Subjective product acceptance remains a separate client/human gate when genuinely required.
