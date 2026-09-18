# Product Model and Theory Loading

## Purpose

Prevent agents from designing technically coherent solutions for the wrong product because they reconstructed only local code or a shallow component list.

## Whole-product model

Before material strategy, I2 should be able to explain:

- final client-visible product;
- major capabilities/elements;
- how those elements interact;
- current physical state of each material capability;
- current acceptance/gate model;
- critical dependencies;
- current bottleneck/critical path.

This is a compact model, not a requirement to read every historical file.

## Summary first, deepen by decision

Use:

`system summary -> identify active decision domain -> load all material theory/evidence for that domain -> reason`

Do not:

- ingest the entire repository mechanically;
- decide first and read domain theory later;
- assume a generic engineering pattern overrides established product behavior.

## Material theory

Theory may include:

- client requirements and prior accepted/rejected product decisions;
- domain rules;
- product behavior standards;
- physical accepted/rejected references;
- current architecture/DB/interface constraints;
- legal/rights/security constraints;
- cost/capacity rules;
- upstream/downstream contracts;
- known failure modes.

## Domain transition

If reasoning materially moves from one domain to another, load the new domain before making the material decision.

Examples:

- backend state -> UI/UX;
- generation -> perceptual quality;
- local implementation -> deployment/security;
- data processing -> rights/privacy;
- one workstream -> cross-workstream integration.

## Missing prior authority

If material prior product authority is known to exist but cannot be recovered:

- do not invent it;
- do not ask the CLIENT to reconstruct repository-recoverable history;
- HOLD the dependent route while recovering the canonical evidence.

## Product-backward route

Use the whole-product model to choose:

`final product -> capability map -> current physical state -> critical dependency/gate -> smallest materially complete next capability`

## Anti-tunneling falsifier

Before authorizing a campaign ask:

"What local technical success could satisfy this campaign while still leaving the actual product materially wrong?"

If a plausible answer exists and the charter does not guard against it, the strategic envelope is incomplete.
