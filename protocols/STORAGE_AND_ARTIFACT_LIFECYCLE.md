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

## File-level persistent lifecycle index (v1.2 candidate)

New scaffolds include a project-local JSON file at .agentic-sdlc/runtime/ARTIFACT_LIFECYCLE_CURRENT.json. Its owner is the local artifact runtime, not Product State. Every system-controlled L3 output must be emitted into an explicitly registered .agentic-sdlc-scratch root through artifact_ledger.py capture, with owner/campaign, category, physical identity, expiry and evidence dependencies. Reconciliation after failures or resume quarantines unknown and modified files. The GC always begins as dry-run and deletes only exact-owned, expired, rebuildable, ignored/untracked files with independent safety checks. SQL/SQLite, canonical/evidence/secret paths, external assets and unknown files are never automatically deleted. The existing workspace_gc.py retains exclusive whole-directory/worktree cleanup ownership. See docs/34_FILE_ARTIFACT_INVENTORY_AND_GC.md.

A host that cannot route an external tool's writes through the capture/reconciliation interface must report tracking as PARTIAL, not promise all native IDE process outputs were observed. The JSON persists across invocations; routine file registration is not a canonical Git-commit boundary. Cleanup must be in the terminal evidence and use meaningful reclaimed-byte readback.
