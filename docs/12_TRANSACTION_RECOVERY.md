# Multi-file Transition Journal and Recovery

Version 0.4 adds a fail-closed transaction journal for campaign-control transitions that must update several canonical JSON owners coherently.

The journal exists because per-file atomic replacement is not enough for operations such as:

- campaign initialization;
- campaign checkpoint/currentness promotion;
- execution-authority acquire/release;
- strategic terminal return.

Those transitions may touch combinations of:

- runtime/CAMPAIGN_RUNTIME_CURRENT.json;
- state/PRODUCT_STATE_CURRENT.json;
- state/CURRENT_BOOTSTRAP_STATE.json;
- state/EXECUTION_AUTHORITY_CURRENT.json;
- campaigns/<campaign_id>/CHECKPOINT_CURRENT.json.

A process crash between those writes can otherwise leave individually valid files that disagree about current truth.

## Canonical live journal

When a multi-file transition is active:

```text
runtime/transactions/CURRENT_TRANSACTION.json
```

is the one live owner for recovery state.

Its contract is `schemas/transition-journal.schema.json`.

A valid current project must not retain this file after a successful transition.

`tools/validate_project.py` therefore rejects any project that still has a live `CURRENT_TRANSACTION.json`.

## Transaction lifecycle

### PREPARED

Before any canonical target is replaced:

1. every target path is constrained to the control root;
2. the current target state is hashed;
3. the complete after-state JSON is serialized;
4. every after-state payload is written and fsynced to a transaction staging directory;
5. the journal records:
   - target path;
   - whether the target previously existed;
   - before SHA-256;
   - after SHA-256;
   - staged-payload ref;
   - applied flag.

Only after all stage payloads are durable is the journal published as `PREPARED`.

### COMMITTING

The journal moves to `COMMITTING`.

For each operation, the controller verifies that the live target still equals the recorded before-state.

If it does:

- the staged payload replaces the target atomically;
- the containing directory is fsynced on supported POSIX systems;
- the operation is marked applied in the journal.

If the target no longer matches the expected before-state, the transaction stops instead of overwriting unknown state.

### COMMITTED

After every target hash equals its expected after-state:

- the journal is marked `COMMITTED`;
- staged transaction files are removed;
- `CURRENT_TRANSACTION.json` is removed.

The absence of a live journal is part of normal currentness.

## Crash recovery

If the process dies during commit, the journal and unapplied stage files remain.

No ordinary mutation or read-only `show/next` operation is allowed to silently proceed through that state.

Recovery is explicit:

```bash
python tools/campaignctl.py \
  --control-root ".agentic-sdlc" \
  recover
```

Recovery evaluates every target independently.

For each operation:

- if target hash == after hash, that operation already committed;
- if target still matches the recorded before-state and the stage payload matches the after hash, recovery rolls it forward;
- if the target is neither the recorded before-state nor after-state, recovery does not overwrite it.

The completed transaction is re-verified before the live journal is removed.

## Conflict semantics

If a target has changed externally after transaction preparation, recovery records:

```text
status = CONFLICT
```

with a concrete conflict reason.

The controller then fails closed.

A `CONFLICT` journal is not automatically rolled back or overwritten. The physical state must be reconciled by the applicable technical authority because the controller cannot know whether the external mutation is valid.

This is deliberately different from retrying an ordinary in-charter defect. A transaction conflict is a currentness/authority ambiguity.

## Why roll-forward instead of rollback

The reference implementation uses roll-forward because all intended after-state payloads are durably staged before the first canonical replacement.

That gives recovery a complete known target state.

Rollback would require preserving and authorizing restoration of every old payload, and could itself overwrite a legitimate external mutation after the crash.

The current implementation therefore:

- rolls forward only when before/after hashes prove the target is still transaction-owned;
- stops on any ambiguous external state.

## Mutation locking

The transaction journal is combined with the Campaign Lead runtime's exclusive mutation lock.

The lock prevents two normal `campaignctl` processes from preparing competing mutations concurrently.

The hashes remain necessary because:

- external tools can still edit files;
- processes can crash;
- manual recovery can occur later;
- the filesystem can contain state written outside `campaignctl`.

Locking and transactional currentness solve different failure classes.

## Fault injection

The runtime self-test intentionally kills the controller during a checkpoint transition after only part of the write set has been applied.

The expected sequence is:

1. process terminates mid-transition;
2. live journal remains;
3. independent project validation fails;
4. read-only runtime inspection fails closed;
5. explicit `recover` rolls the remaining targets forward;
6. journal is removed;
7. project validation passes again.

The self-test also creates a second crash state, mutates an unapplied target externally, and verifies that:

- recovery fails;
- the journal persists as `CONFLICT`;
- the external target remains untouched.

## Test-only crash hook

The reference self-test uses:

```text
AGENTIC_SDLC_TEST_CRASH_AFTER_APPLY
```

to terminate the process after a specified number of canonical replacements.

This environment variable exists only for deterministic fault injection. It is not an operating-mode control and should not be set in normal execution.

## Durability boundary

The implementation currently provides:

- staged complete after-state payloads;
- SHA-256 before/after verification;
- atomic same-filesystem replacement;
- file fsync;
- POSIX directory fsync where supported;
- exclusive process mutation locking;
- explicit fail-closed recovery.

It is still a local-filesystem reference runtime, not a distributed transaction protocol.

It does not coordinate external databases, cloud services, remote repositories or multiple filesystems as one ACID transaction.

Those resources still require their own idempotency, transaction or compensation semantics.

## Acceptance boundary

Successful journal recovery proves only that the declared local control-plane transition reached one coherent after-state.

It does not prove:

- product correctness;
- runtime behavior;
- semantic quality;
- security;
- rights compliance;
- release readiness;
- Planner or CLIENT acceptance.
