# Schema Evolution and Explicit Migrations

Version 0.5 introduces versioned state-schema evolution.

The purpose is to let a fork upgrade durable Agentic SDLC state without forcing all existing repositories to rewrite current state at the moment the starter changes.

## Compatibility model

A contract may have:

- one latest schema;
- one or more legacy schemas retained for compatibility;
- explicit registered migration edges between versions.

The validator may accept more than one supported version at the same time.

New scaffolds emit the latest version.

Existing projects are not silently upgraded by validation, scaffolding or runtime commands.

## First evolved contract

The first real migration is:

```text
CURRENT_BOOTSTRAP
starter-bootstrap-0.1
        ->
starter-bootstrap-0.2
```

The legacy schema remains at:

```text
schemas/current-bootstrap-v0.1.schema.json
```

The current/latest schema is:

```text
schemas/current-bootstrap.schema.json
```

## Why bootstrap v0.2 exists

Version 0.1 represented currentness only as:

```json
{
  "unresolved_currentness": []
}
```

Version 0.2 makes that state explicit:

```json
{
  "currentness": {
    "verified": true,
    "verified_at": "2030-01-01T00:00:00Z",
    "source_refs": [
      "state/CLIENT_REQUIREMENTS_CURRENT.md",
      "state/PRODUCT_STATE_CURRENT.json"
    ],
    "unresolved": []
  }
}
```

This distinguishes:

- currentness has been positively verified;
- when that verification occurred;
- which durable owners were used;
- what remains unresolved.

For bootstrap v0.2, `READY` requires verified currentness with no unresolved items.

## Migration registry

The canonical migration graph is:

```text
migrations/registry.json
```

Its schema is:

```text
schemas/migration-registry.schema.json
```

The registry records:

- contract;
- from version;
- to version;
- from schema;
- to schema;
- forward handler;
- optional reverse handler.

The starter manifest separately declares latest schema versions.

Structural validation requires the manifest and migration registry to agree.

## Plan without mutation

```bash
python tools/migrate_state.py \
  --control-root ".agentic-sdlc" \
  plan \
  --file "state/CURRENT_BOOTSTRAP_STATE.json"
```

The planner:

1. reads the file's `schema_version`;
2. resolves its contract;
3. selects the declared latest version unless an explicit target is supplied;
4. finds a registered path;
5. validates the current file against its source schema;
6. prints the plan.

Plan does not mutate the target.

## Apply

```bash
python tools/migrate_state.py \
  --control-root ".agentic-sdlc" \
  apply \
  --file "state/CURRENT_BOOTSTRAP_STATE.json"
```

Every migration step:

1. validates the input against the declared source schema;
2. runs the registered transform;
3. checks that the produced `schema_version` is exactly the declared destination;
4. validates the result against the destination schema;
5. checks that the target file was not modified concurrently;
6. replaces the file atomically and durably.

If the file is already at the requested target, apply returns `ALREADY_AT_TARGET` and does not rewrite it.

## Explicit target and reverse migration

A target version can be requested:

```bash
python tools/migrate_state.py \
  --control-root ".agentic-sdlc" \
  apply \
  --file "state/CURRENT_BOOTSTRAP_STATE.json" \
  --target-version "starter-bootstrap-0.1"
```

Reverse migration is available only when the registry declares a reverse handler.

A reverse handler must not silently discard semantics that cannot be represented by the older version.

For bootstrap v0.2 -> v0.1, downgrade fails if the richer `currentness` block contains meaning that was not deterministically representable in v0.1.

That is a hard failure, not a lossy best-effort downgrade.

## Migration and campaign transactions

Schema migration uses the same exclusive state lock as `campaignctl`.

If a campaign multi-file transition journal is live:

```text
runtime/transactions/CURRENT_TRANSACTION.json
```

schema apply fails.

The pending campaign transition must first be recovered or reconciled.

This prevents a schema rewrite from racing with currentness recovery.

## Backward compatibility

Version 0.5 intentionally supports both:

- `starter-bootstrap-0.1`;
- `starter-bootstrap-0.2`.

That means an existing fork can update validation tooling without immediately rewriting its bootstrap file.

Newly generated scaffolds use v0.2.

Compatibility can only be removed in a future version when the public contract explicitly says so and a supported migration path exists.

## Validation

`tools/validate_project.py` dispatches validation by the instance's own `schema_version`.

Therefore legacy state is validated against the legacy schema, not coerced through the latest schema.

For v0.2, validation additionally checks currentness relationships such as:

- `READY` implies verified currentness;
- verified currentness has a verification timestamp;
- currentness source refs resolve;
- bootstrap/current Product State refs still agree.

## Self-test

CI runs:

```text
tools/selftest_migrations.py
```

The test physically proves:

- plan is read-only;
- v0.1 -> v0.2 succeeds;
- migrated project still validates;
- re-applying at v0.2 is idempotent;
- representable v0.2 -> v0.1 restores the original semantics exactly;
- richer v0.2 state refuses lossy downgrade;
- an unsupported target version fails closed;
- a live campaign transaction blocks migration.

## Adding another migration

A new contract/version should not be added by replacing an old schema in place.

The expected process is:

1. retain the old schema under a versioned filename if it remains supported;
2. add the new/latest schema;
3. add a migration-registry edge;
4. implement and register the handler;
5. update latest-version metadata;
6. add forward validation;
7. add idempotence tests;
8. add reverse tests if reverse is claimed;
9. add a falsifier for semantics that cannot be downgraded;
10. only then make new scaffolds emit the new version.

## Limits

The current migration tool operates on local JSON state files.

It does not automatically migrate:

- application databases;
- arbitrary source code;
- remote services;
- external provider state;
- project-specific custom schemas not registered in the migration graph.

Those require their own migration contracts and evidence.

A successful schema migration proves state-format compatibility, not product correctness or acceptance.
