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

## v0.9 — Hardening and release candidate

Implemented:

- centralized local control-state locking/journaling/recovery in `state_tx.py`;
- Campaign Lead runtime delegates transaction/recovery semantics to the shared primitive;
- schema migrations delegate locking/durable writes to the shared primitive;
- adoption uses the same shared primitive;
- static hardening test prevents duplicate primitive reintroduction;
- all Python tools compile in hardening CI;
- SMALL has zero optional protocols and heavy mechanisms remain optional;
- machine-readable v1 release criteria;
- canonical contract-instance release test;
- one-command complete v1 release verifier;
- documented feature-freeze/stopping rule;
- complete v1 release gate passes on the release-candidate tree.

## v1.0 — Transfer-hardened public starter

Stable release boundary.

Release properties:

- exact clean v0.9 release candidate passed the complete v1 evidence gate;
- structure-only public boundary is machine-checked;
- canonical contract instances validate;
- negative/falsification fixtures reject known invalid states;
- all public profiles scaffold and remain proportional;
- schema evolution supports explicit forward/reverse/idempotent paths;
- canonical ownership/currentness/supersession are mechanically checked;
- fresh contexts reconstruct deterministic legal posture without chat memory;
- a physical SQLite reference proves persistent state/idempotency/recovery behavior;
- six unrelated synthetic project shapes pass adoption without application-file mutation;
- campaign execution is resumable and crash-recoverable;
- local control-state locking/journaling/recovery uses one shared primitive;
- the complete release definition of done is executable with `tools/verify_v1_release.py`.

Claim boundary:

- this is a generic starter with tested synthetic transfer evidence;
- it is not proof of universal autonomous correctness;
- real projects still own product, runtime, security, rights, perceptual/human and release gates.

Post-1.0 rule:

- architecture feature work stops by default;
- future changes are driven by reproducible defects, compatibility/security issues or demonstrated generic adoption failures;
- do not add roles, policies or examples merely to continue version iteration.

Formal open-source licensing remains a separate repository-owner decision.


## v1.0.1 — Repository efficiency and local hygiene defect patch

Implemented from observed operational failure classes:

- hard canonical commit-boundary authority; I4 does not own canonical commits by default;
- explicit anti-`COMMIT_MANIA` semantics;
- exact-branch, no-tags, no-submodule delta refresh without `git pull`;
- changed-path context reacquisition from a known baseline;
- portable `repo_delta.py` in generated scaffolds;
- portable `commit_guard.py` in generated scaffolds;
- workspace lifecycle marker/schema/template;
- dry-run-first marker-owned `workspace_gc.py`;
- protected/quarantine/unexpired/dirty/unmarked cleanup blocks;
- Git-aware linked-worktree cleanup;
- adversarial repository-hygiene self-test;
- v1 release gate extended to cover these failure classes.

This is a defect-driven patch under the post-1.0 stopping rule; role topology and product authority are unchanged.


## v1.1 — Product discovery and engineering baseline

Implemented:

- structured product-discovery conversation before first material campaign;
- CLIENT-confirmed current requirements baseline without treating confirmation as a legal signature;
- Planner-owned persistent technical stack/security/network/deployment baseline;
- machine/environment capability assessment when material;
- simple-functional UI default with explicit system-verifiable checks;
- dated delivery plan with milestone confidence, risks and schedule-change history;
- derived project status/tracker instead of a second manual source of truth;
- project-local Agentic SDLC operating review for real-use/pilot evidence;
- campaign runtime fail-closed baseline guard for new scaffolds;
- fresh-context reconstruction includes technical/delivery baseline state.
- privacy-preserving recurring architecture feedback;
- weekly/monthly managed GitHub Actions schedule;
- metadata-only artifact enabled by default with visible opt-out;
- external feedback submission disabled by default and explicitly opt-in;
- non-leakage self-test for project identifiers/content/paths/credentials.

This is an evidence-driven capability addition, not a restart of open-ended architecture iteration.
