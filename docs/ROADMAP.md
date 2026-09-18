# Public Starter Roadmap

This roadmap is for the public architecture repository itself. It is not a promise of autonomous background work.

## v0.1 — Core structure preview

Implemented:

- role/authority model;
- client boundary;
- identity and execution authority;
- Planner kernel;
- product-model/theory-loading discipline;
- persistent Campaign Lead model;
- campaign charter;
- capability DAG and isolation;
- capability lifecycle;
- exact-candidate review freeze;
- layered evidence gates;
- state/DB/lineage/idempotency protocol;
- capacity/resume semantics;
- storage/artifact lifecycle;
- cost/external-service semantics;
- security/privacy/rights/external-action boundaries;
- systemic escalation/anti-churn;
- interaction provenance;
- fork/install/re-anchor/fresh-context prompts;
- synthetic minimal example;
- machine-readable schemas for current state/campaign/identity/bootstrap/interaction/manifest;
- structure-only CI validator.

## v0.2 — Stronger executable validation

Candidate additions:

- validate example instances against JSON Schemas in CI;
- relationship-graph checks across Product State -> execution authority -> checkpoint -> terminal;
- stale/superseded currentness checks;
- duplicate-current-owner detection;
- generated bootstrap package from a project profile;
- schema migration/versioning rules.

## v0.3 — Minimal reference runtime

Candidate additions:

- resumable campaign controller;
- tactical work-unit state;
- resource/write-set isolation;
- independent-review orchestration;
- checkpoint/recovery;
- append/reprioritize/retire tactical work;
- typed strategic terminals.

The runtime should remain optional. Projects must be able to use the architecture without adopting a specific orchestration engine.

## v0.4 — Synthetic reference projects

Candidate examples:

- small single-repository application;
- stateful backend;
- multi-workstream product;
- artifact-heavy pipeline;
- high-consequence/external-action project.

Examples must remain synthetic and structure-only.

## v1.0 — Transfer-hardened public starter

Target properties:

- unrelated forks can install the starter without source-project institutional memory;
- governance burden remains bounded;
- setup does not require technical client rescue;
- currentness/identity/terminal relationships are machine-checkable where useful;
- documentation matches executable reference mechanisms;
- optional complexity can be removed cleanly for small projects.

Product version numbers do not imply universal autonomy or generalization claims.
