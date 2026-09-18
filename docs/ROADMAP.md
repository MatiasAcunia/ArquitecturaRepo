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

## v0.5 — Backward-compatible schema evolution

Implemented:

- versioned migration-registry contract;
- manifest-declared latest schema versions;
- preserved legacy bootstrap v0.1 schema;
- structured bootstrap v0.2 currentness contract;
- simultaneous validator support for v0.1 and v0.2;
- explicit read-only migration planning;
- graph-based forward/reverse migration path resolution;
- source-schema validation before each migration step;
- destination-schema validation after each migration step;
- atomic durable migration writes;
- shared state lock with the campaign runtime;
- migration blocking while a campaign transaction journal is live;
- idempotent apply when already at target;
- exact representable v0.2→v0.1 reverse migration;
- fail-closed rejection of lossy downgrade;
- new scaffolds emitting bootstrap v0.2;
- portable migration tool and registry in generated control layers;
- CI forward/reverse/idempotence/failure self-test.

## v0.6 — Canonical ownership and supersession

Implemented:

- generic owner-registry schema;
- owner registry generated in new project scaffolds;
- exactly one CURRENT owner per represented concern;
- physical surface resolution for CURRENT local owners;
- owner-to-Product-State Currentness Set binding;
- known-contract alignment for Product State, bootstrap and CLIENT requirements;
- reciprocal supersession lineage;
- same-concern supersession enforcement;
- dangling-owner detection;
- supersession-cycle detection;
- cross-version duplicate bootstrap-owner detection;
- valid owner replacement fixture;
- adversarial ownership/supersession CI self-test.

## v0.7 — Fresh-context reconstruction and physical reference transfer

Implemented:

- validate-first deterministic fresh-context reconstruction;
- deterministic posture output across repeated fresh invocations;
- fail-closed reconstruction through invalid owners/currentness/recovery state;
- reconstruction of fresh scaffold, active campaign and Planner-return states;
- portable reconstruction tool in generated scaffolds;
- physical SQLite stateful reference system;
- idempotent replay semantics;
- idempotency conflict detection;
- transactional rollback under injected application failure;
- restart persistence;
- concurrent replay verification;
- project-specific application/evidence owners bound to Product State currentness;
- end-to-end CI requiring application tests + control validation + fresh reconstruction;
- adversarial removal of the canonical application state mechanism.

## v0.8 — Transfer/adoption testing

Implemented:

- deterministic read-only project inventory;
- explicit adoption-spec contract;
- preflight validation on a copied candidate control layer;
- journaled multi-file adoption promotion;
- generic portable state-transaction recovery;
- retry-idempotent adoption;
- application-file preservation checks;
- six unrelated synthetic project shapes across all public operating profiles;
- profile-proportional mechanism checks;
- post-adoption project validation;
- post-adoption deterministic fresh-context reconstruction;
- fault-injected adoption crash and recovery;
- no technical CLIENT editing of Product State/bootstrap/owners/currentness.

## v0.9 — Hardening and release-candidate reduction

Next candidate work:

- remove duplicated transaction/locking implementations where safe;
- define machine-readable v1 release criteria;
- make one command execute the complete release evidence suite;
- measure required-vs-optional mechanism burden;
- remove stale roadmap/documentation claims;
- run clean-install/reconstruct/adopt probes from final artifacts;
- freeze new features unless a release criterion is still unproven.

## v1.0 — Transfer-hardened public starter

Target properties:

- unrelated forks can install the starter without source-project institutional memory;
- governance burden remains bounded;
- setup does not require technical client rescue;
- currentness/identity/terminal relationships are machine-checkable where useful;
- documentation matches executable reference mechanisms;
- optional complexity can be removed cleanly for small projects.

Product version numbers do not imply universal autonomy or generalization claims.
