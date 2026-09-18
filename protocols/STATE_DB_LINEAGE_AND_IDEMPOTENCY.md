# State, Database, Lineage and Idempotency

## Scope

Use this protocol whenever a capability owns persistent state, a database, durable manifests, queues, external-event processing or generated-asset lineage.

## One canonical fact owner

Each material fact should have one canonical current owner.

Derived views, indexes and reports may exist, but they must not become competing writable truth.

If two writable surfaces can both claim the same current fact without a reconciliation rule, the architecture is defective.

## Current vs history

Distinguish:

- current state — what is authoritative now;
- immutable or append-only history — what happened;
- derived/cache state — reconstructible representations;
- evidence snapshots — frozen proof for a gate.

Do not overwrite history merely to make current state look clean.

## Transactions and single-writer semantics

Define, as applicable:

- transaction boundary;
- integration writer;
- concurrency/locking behavior;
- conflict behavior;
- atomic promotion from candidate to current;
- crash point and recovery behavior.

A worktree/branch does not isolate a shared live database.

## Idempotency

Any operation that can be retried after timeout/crash/restart should define an idempotency identity or equivalent replay-safety mechanism.

Test:

- same identity + same payload;
- same identity + conflicting payload;
- duplicate external event;
- partial prior completion;
- restart after commit but before acknowledgement.

## Migrations

Before a state/schema migration establish:

- source schema/version;
- target schema/version;
- compatibility window;
- rollback/forward-fix strategy;
- backup/recovery boundary;
- migration idempotency;
- readback verification;
- dependent service/interface impact.

A migration script existing is not proof that production/current state was migrated correctly.

## Lineage

When outputs depend on prior inputs/transforms, preserve enough identity to reconstruct:

`source/input -> transform/config/model/version -> intermediate identity -> accepted output`

Lineage should support:

- provenance;
- currentness;
- invalidation;
- reproducibility where practical;
- rights/license tracing where applicable;
- exact-candidate review.

## Invalidation

Define what changes make derived state/artifacts stale.

Examples:

- source content changes;
- model/config changes;
- canonical product requirement changes;
- schema semantics change;
- upstream accepted candidate changes.

Stale derived state must not remain silently current.

## Recovery

Recovery evidence should prove more than a happy-path restart.

Where relevant test:

- interrupted write;
- duplicated work;
- partially persisted batch;
- missing artifact;
- stale lock/lease;
- conflicting current pointer;
- restored service against old schema/state.

## Acceptance

A green unit test cannot substitute for current database/readback evidence when state correctness is material.

Stateful acceptance should bind the exact schema/state/candidate relation that downstream execution will actually consume.
