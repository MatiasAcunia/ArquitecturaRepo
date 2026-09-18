# Stateful Reference System and Transfer Evidence

Version 0.7 adds one physical synthetic reference system plus deterministic fresh-context reconstruction.

The goal is not to demonstrate a production backend.

The goal is to prove that the reusable Agentic SDLC mechanisms can bind to a real stateful implementation and reconstruct one coherent posture without chat memory.

## Reference system

```text
examples/stateful_backend/
```

The application is a small SQLite note store.

It demonstrates:

- persistent application state;
- request-level idempotency;
- conflict detection when one idempotency key is reused for another payload;
- transactional rollback;
- persistence across store reconstruction;
- concurrent replay of the same request.

The reference deliberately uses only Python's standard library and SQLite.

## Physical application evidence

```text
examples/stateful_backend/tests/test_note_store.py
```

CI executes five tests covering:

1. idempotent replay returns one note;
2. one request identity cannot be reused for another payload;
3. committed state survives a new store instance;
4. injected failure after note insert rolls the entire transaction back;
5. concurrent replay creates one note and one idempotency record.

The declared evidence surface is:

```text
examples/stateful_backend/evidence/STATEFUL_REFERENCE_EVIDENCE.json
```

## Control layer

The reference has a separate synthetic control layer:

```text
examples/stateful_backend/control/
```

It contains:

- CLIENT requirements;
- Product State;
- structured bootstrap v0.2;
- canonical owner registry;
- project overlay;
- agent entrypoint.

The control layer does not invent an active campaign or execution authority.

The physical capability is already reference-validated, so fresh reconstruction should produce:

```text
RECONSTRUCTED_NO_ACTIVE_EXECUTION
```

not `EXECUTION_AUTHORIZED` and not `STRATEGIC_RETURN_BOUNDARY`.

## Custom ownership

The reference uses the generic owner registry for two project-specific concerns:

- `APPLICATION_STATE_MECHANISM` -> `../app/note_store.py`;
- `REFERENCE_EVIDENCE` -> `../evidence/STATEFUL_REFERENCE_EVIDENCE.json`.

Both are required in Product State currentness.

Removing the canonical application-state mechanism therefore breaks:

- Product State Currentness Set resolution;
- canonical owner resolution;
- fresh-context reconstruction.

This is intentional.

## Deterministic fresh-context reconstruction

`tools/reconstruct_context.py` validates before reconstructing.

It emits a deterministic JSON posture including:

- product/workstream;
- current code ref;
- current gate;
- active campaign boundary;
- currentness status and evidence;
- canonical owners;
- execution authority;
- campaign runtime summary;
- forbidden actions;
- next legal boundary.

It refuses to reconstruct through invalid state.

Examples of fail-closed conditions include:

- duplicate current owner;
- broken currentness ref;
- invalid schema;
- pending multi-file transition journal;
- ambiguous execution authority.

## Transfer self-test

CI runs:

```text
tools/selftest_stateful_reference.py
```

The test requires, in one run:

- all physical SQLite tests pass;
- the control layer validates;
- two independent reconstruction invocations return byte-identical output;
- the reconstructed posture is correct;
- currentness is verified;
- no execution authority or campaign runtime is invented;
- custom owners are present;
- deleting the canonical application-state mechanism causes validation and reconstruction to fail.

## What this proves

The reference provides evidence for these starter properties:

- domain state can coexist with Agentic SDLC control state;
- state semantics can be expressed outside chat;
- currentness can bind project-specific physical mechanisms;
- canonical ownership can extend beyond starter-native contracts;
- a fresh process can recover the same legal posture;
- absence of active engineering work can be represented explicitly.

## What this does not prove

It does not prove:

- universal transfer to arbitrary repositories;
- production database safety;
- distributed transaction correctness;
- security;
- external deployment;
- autonomous product judgment.

Those remain separate gates.

The next transfer gate should therefore test fresh installation/adoption across unrelated project shapes rather than adding more documentation to this reference.
