# v1 Release Gates

A v1 release is not triggered by a version-number sequence.

It is triggered when every required release gate passes on the exact release candidate.

Canonical criteria:

```text
state/V1_RELEASE_CRITERIA.json
```

Executable verifier:

```bash
python tools/verify_v1_release.py
```

Machine-readable output:

```bash
python tools/verify_v1_release.py --json
```

## Release rule

Every required gate must pass.

A lower-level PASS cannot substitute for another gate.

Examples:

- green unit tests do not replace runtime evidence;
- valid JSON does not replace currentness reconstruction;
- successful adoption does not replace crash recovery;
- a physical stateful reference does not replace cross-profile transfer;
- a successful runtime does not replace bounded-governance checks.

## Required gates

### STRUCTURE_AND_PUBLIC_BOUNDARY

Checks:

- required public surfaces exist;
- JSON parses;
- JSON Schemas use the declared draft and IDs;
- VERSION and manifest agree;
- structure-only content policy remains enforced;
- embedded credentials/private keys/personal email patterns are rejected;
- internal Markdown links resolve;
- migration registry and manifest latest-version metadata agree.

### CORE_CONTRACT_INSTANCES

Validates declared contracts for:

- starter state;
- public profiles;
- migration registry;
- minimal lifecycle example;
- active-campaign example;
- terminal-candidate example;
- physical stateful reference control layer.

### VALIDATION_FALSIFICATION

Requires positive fixtures and adversarial invalid states.

Known falsifiers include:

- checkpoint/current-ref mismatch;
- actor/run authority mismatch;
- missing terminal gate evidence;
- missing Currentness Set owner.

### PROFILE_AND_SCAFFOLD_TRANSFER

Generates every public profile and proves:

- generated control state validates;
- latest bootstrap is used;
- portable validator/migrator/reconstruction/adoption/recovery tooling exists;
- SMALL stays minimal;
- heavier profiles receive required optional mechanisms;
- optional runtime remains opt-in;
- accidental control-layer overwrite is refused.

### SCHEMA_EVOLUTION

Requires:

- read-only migration planning;
- forward migration;
- idempotent re-apply;
- exact lossless reverse where claimed;
- fail-closed lossy downgrade;
- unsupported target rejection;
- migration block while a campaign transaction is pending.

### CANONICAL_OWNERSHIP

Requires:

- exactly one CURRENT owner per represented concern;
- required current owners in Product State currentness;
- reciprocal same-concern supersession;
- cycle/dangling detection;
- physical alignment for known canonical owners.

### FRESH_CONTEXT_RECONSTRUCTION

Requires deterministic reconstruction for:

- fail-closed fresh scaffold;
- active execution;
- Planner strategic-return boundary.

Invalid ownership or pending transaction state must prevent reconstruction.

### PHYSICAL_STATEFUL_REFERENCE

Runs a real SQLite fixture proving:

- request idempotency;
- conflicting idempotency-key rejection;
- restart persistence;
- transaction rollback under injected failure;
- concurrent replay safety.

The same run validates/reconstructs its Agentic SDLC control layer.

### CROSS_PROFILE_ADOPTION

Adopts six unrelated synthetic project shapes:

- SMALL;
- STATEFUL;
- ARTIFACT_HEAVY;
- MULTI_WORKSTREAM;
- MULTI_PRODUCT;
- HIGH_CONSEQUENCE.

Requires:

- deterministic read-only inventory;
- no application-file mutation;
- explicit adoption spec;
- preflight before canonical mutation;
- journaled promotion;
- retry idempotence;
- fresh reconstruction after promotion;
- proportional mechanism burden;
- crash recovery.

### PROJECT_BASELINE_READINESS

Requires new project scaffolds to prove before material campaign initialization:

- CLIENT-confirmed current product requirements;
- explicit functional/non-functional/security/network/UI/data/cost/date baseline;
- CURRENT Planner-owned technical stack frame;
- assessed machine/environment constraints when material;
- explicit deployment/network exposure posture;
- security/backup/recovery choices proportional to exposure;
- CURRENT delivery plan with target release date;
- dated milestones with done conditions and confidence;
- explicit schedule-review date;
- derived project-status view;
- fail-closed campaign initialization while the baseline is incomplete.

Legacy installations that do not yet materialize these baseline surfaces retain backward-compatible runtime behavior until they deliberately adopt the mechanism.

### PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK

Requires:

- managed weekly/monthly schedule support;
- metadata-only report contract;
- local artifact generation enabled by default;
- external submission disabled by default;
- one-command/config opt-out;
- install-time schedule opt-out;
- no stable project tracking identifier;
- no project/repository name, product id, requirements text, code, paths, SHAs, free text, users, emails or credentials;
- adversarial synthetic secret/path/identifier strings do not leak;
- cadence mismatch skips cleanly;
- `enabled=false` emits nothing;
- external submission requires explicit config plus repository-level opt-in.

### RESUMABLE_CAMPAIGN_RUNTIME

Requires:

- dependency-aware tactical DAG;
- concurrent write/resource conflict rejection;
- capacity hold/resume;
- execution-authority release/reacquire;
- durable checkpoint/currentness reconciliation;
- exact review freeze;
- independent review;
- review invalidation after later producer mutation;
- strategic terminal;
- injected crash recovery;
- fail-closed external recovery conflict.

### REPOSITORY_EFFICIENCY_AND_LOCAL_HYGIENE

Requires:

- exact-branch remote refresh without pull/merge/local-HEAD mutation;
- changed-path delta from a known baseline;
- I4 canonical commit authority rejected by default;
- I3 coherent-candidate boundary accepted;
- marker-owned GC dry-run by default;
- expired pre-authorized local workspace deletion;
- protected, future, dirty and unmarked workspace preservation;
- explicit-root containment.

### HARDENING_AND_BOUNDED_GOVERNANCE

Requires:

- all Python tools compile;
- shared transaction/locking primitives are centralized;
- campaign runtime does not reintroduce its own transaction engine;
- schema migration does not reintroduce its own lock/durable writer;
- adoption uses the same shared primitives;
- SMALL carries no optional governance;
- MASTER OWNER and stateful machinery remain optional.

## CLIENT boundary

A v1 PASS does not mean the CLIENT disappears.

The system should not require the CLIENT to repair:

- JSON;
- currentness;
- owner lineage;
- campaign checkpoints;
- transaction recovery;
- technical architecture sequencing.

The CLIENT can still be required for genuine product authority such as:

- material product-visible behavior;
- subjective quality;
- business/economic tradeoffs;
- external/publication/destructive authority.

## Claim boundary

A v1 PASS demonstrates that the starter's declared generic mechanisms, product-baseline controls and synthetic transfer gates work together.

It does not prove autonomous correctness on arbitrary real software, nor does it grant external authority.

A real fork still owns its project-specific product, runtime, security, rights, release and human/perceptual gates.

## Feature freeze rule

After the v1 release criteria are complete:

- do not add features merely because another version number is available;
- fix defects exposed by real adoption/use;
- add a generic mechanism only when a demonstrated failure class cannot be handled by an existing owner/protocol/tool.

This is the stopping rule for the starter architecture phase.
