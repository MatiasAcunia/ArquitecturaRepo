# Storage and Artifact Lifecycle

## Core invariant

Artifact-producing campaigns must treat storage as a bounded production resource.

Before expensive generation, know:

- what artifact classes will be created;
- where they are written;
- expected batch/peak pressure when measurable;
- which exact artifacts/evidence must survive;
- which are temporary/reconstructible;
- who may delete them;
- cleanup trigger/deadline;
- recovery reserve.

Do not generate until disk exhaustion and then ask the CLIENT what to delete.

## Lifecycle classes

### KEEP_CANONICAL_OR_EVIDENCE

Current/accepted artifacts, exact human/reviewer references, immutable hard-gate evidence, unique provenance/rights evidence, recovery state or expensive unreproducible dependencies.

### SHORT_TERM_EVIDENCE

Candidate samples, failure examples and diagnostics needed for current review/root cause. Must have an expiration trigger.

### EPHEMERAL_RECONSTRUCTIBLE

Staging/temp/cache/proxies/duplicate encodes and other safe-to-regenerate outputs. Delete aggressively after successful promotion/readback and dependency checks.

### QUARANTINE_UNRESOLVED

Unknown ownership/provenance/deletion safety. Must have an owner and classification deadline.

## Preflight

Before a large batch:

1. inspect actual free space;
2. estimate next bounded batch;
3. reserve recovery/staging space;
4. identify safe cleanup candidates;
5. identify protected/current/accepted/user-managed material;
6. establish hard-stop floor.

If unsafe:

`STOP_NEW_GENERATION -> SAFE_CLEANUP -> RECHECK -> CONTINUE_OR_HOLD`.

## Terminal

Before readiness, reconcile storage.

Do not leave large known disposable populations as unnamed future cleanup debt.
