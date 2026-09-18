# Public Starter Roadmap

This roadmap is for the public architecture repository itself. It is not a promise of autonomous background work.

## v0.1 — Core structure

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
- machine-readable contracts;
- installation/re-anchor/fresh-context prompts.

## v0.2 — Executable validation and scaffolding

Implemented:

- JSON Schema validation for public contracts;
- relationship checks across Product State, charter, identity, execution authority, checkpoint, bootstrap and terminal;
- duplicate-current-owner checks for mechanically identifiable owners;
- Currentness Set ref validation;
- exact-candidate review/evidence checks;
- positive synthetic examples for pre-campaign, active-campaign and terminal states;
- adversarial negative fixtures that must fail;
- machine-readable installation profiles;
- fail-closed project scaffold generator;
- all-profile scaffold self-test;
- CI enforcement for the full executable validation surface.

Not yet implemented:

- schema migration/versioning framework;
- generic relationship rules for arbitrary project-specific custom state.

## v0.3 — Optional reference Campaign Lead runtime

Implemented:

- campaign-runtime schema;
- persistent tactical work-unit state;
- append/reprioritize/park/supersede/cancel;
- dependency-aware READY state;
- cross-platform exclusive mutation lock with timeout;
- write-surface/shared-resource conflict prevention;
- failure/retry;
- HOLD and capacity checkpoint/resume;
- durable checkpoint emission;
- Product State/bootstrap/execution-authority currentness reconciliation;
- execution-authority acquire/release;
- exact review-freeze lifecycle;
- independent reviewer binding;
- automatic freeze invalidation after later tactical/producer mutation;
- typed strategic terminal requests;
- independent runtime relationship validation;
- end-to-end runtime self-test;
- optional portable runtime installation via `--with-runtime`.

## v0.4 — Transactional currentness and crash recovery

Implemented:

- transition-journal schema;
- complete after-state staging before canonical mutation;
- SHA-256 before/after ownership checks;
- atomic target replacement with filesystem durability hardening;
- exclusive mutation lock plus transaction ownership checks;
- transactional campaign init;
- transactional checkpoint/currentness promotion;
- transactional execution-authority acquire/release;
- transactional strategic terminal return;
- explicit `campaignctl recover`;
- read and mutation fail-closed behavior while a journal is pending;
- independent validator rejection of pending transitions;
- deterministic process-kill fault injection in CI;
- roll-forward recovery after partial checkpoint commit;
- adversarial external mutation test;
- persistent `CONFLICT` instead of overwriting ambiguous external state;
- cleanup of pre-journal orphan stages after preparation errors.

## v0.5 — Schema evolution and richer synthetic reference projects

Next candidate work:

- schema migration/versioning framework;
- stronger generic supersession/current-owner checks;
- migration-path validation and reversible fixtures;
- synthetic stateful backend reference;
- synthetic multi-workstream reference;
- synthetic artifact-heavy reference;
- synthetic high-consequence/external-action reference.

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
