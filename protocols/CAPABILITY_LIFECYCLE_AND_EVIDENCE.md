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

## Durable, independently verifiable engine product versions — 2026-10-19

Named engine is a coherent reusable code-owned unit with WHAT/WHY/HOW, product boundaries, entrypoints (one or many scripts), typed contracts, consumers, tests, real gates, source/currentness/lineage, compatibility, historical release receipts and rollback. Each meaningful Goal generally targets closure of ONE critical-path engine, not batch generation of new helper engines; L2 may produce hard source prototypes, L3 coordinates Cycle construction and L4 codes, then the product authority accepts a version after actual runtime/perceptual gates. `tools/engine_registry.py` validates read-only product-local catalogs and immutable source history; candidates are NOT RELEASED. SemVer is a convention, not proof. Version changes must explicitly record WHY/HOW, exact code artifact hashes, tests, DB/migrations, before/after consumer contracts and physical acceptance receipts. Product engines implement repetitive operations; LLMs are bounded helpers for creative/semantic portions with independent quality evidence, not one-per-item adjudicators.
