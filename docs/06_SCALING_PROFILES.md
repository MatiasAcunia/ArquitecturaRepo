# Scaling Profiles

The architecture is intentionally elastic. Do not deploy the same amount of governance to every project.

## Profile S — Small project

Use when:

- one repository;
- one product;
- one Planner;
- low deployment risk;
- limited persistent state;
- one or few execution agents.

Typical stack:

`CLIENT -> PLANNER -> CAMPAIGN LEAD -> BUILDER/REVIEWER`

MASTER OWNER may be omitted as a separate active role if there is no cross-project/systemic layer to govern.

## Profile M — Stateful product

Add when the system has:

- databases;
- migrations;
- background jobs;
- runtime recovery;
- persistent user state;
- deployment environments.

Add stronger:

- currentness set;
- DB/state envelope;
- idempotency/recovery gates;
- exact environment binding;
- checkpoint semantics;
- security review.

## Profile A — Artifact-heavy product

Add when the system generates many large or expensive artifacts.

Add:

- storage preflight;
- artifact lifecycle;
- exact lineage;
- representative physical/perceptual gates;
- cleanup authority;
- cost/yield tracking.

## Profile W — Multi-workstream product

Use when one final product has independently planned workstreams.

Add:

- one Planner per strategic workstream;
- explicit cross-workstream contracts;
- one product-level integration authority;
- isolated volatile state;
- cross-workstream currentness/acceptance gates.

Do not merge workstream state just because they share a final product.

## Profile P — Multi-product portfolio

Use when several separate products share an agent/runtime/process platform.

Add MASTER OWNER for:

- shared process/runtime quality;
- portfolio resource risk;
- systemic defect correction;
- reusable infrastructure;
- cross-project governance hygiene.

Do not let MASTER OWNER become a second local Planner.

## Profile H — High-consequence system

Use when failures can cause material financial, security, privacy, safety or irreversible external effects.

Add stronger:

- explicit authorization gates;
- threat/risk modeling;
- independent security/safety review;
- immutable evidence;
- rollback/recovery;
- environment segregation;
- secret handling;
- auditability;
- stricter release criteria.

## Scaling rule

A project moves to a more complex profile because physical failure modes require it, not because the architecture diagram looks more sophisticated.
