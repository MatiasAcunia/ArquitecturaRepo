# Engineering Campaign Charter Standard

## Purpose

The charter is the strategic delegation envelope from I2 Planner to I3 Campaign Lead.

One charter should cover one cohesive capability/engine objective.

## Required fields

### Identity

- project/workstream;
- campaign id;
- capability/engine;
- authoritative baseline/ref;
- current authority/state pointers;
- critical-path relevance.

### Capability objective

Express:

`CURRENT EXECUTABLE CAPABILITY -> REQUIRED EXECUTABLE CAPABILITY`.

### Strategic architecture envelope

- product purpose;
- owning capability boundary;
- existing owners to evolve;
- fixed public/interface semantics;
- permitted interface evolution;
- dependency direction;
- product/failure invariants;
- deterministic vs AI responsibilities;
- protected owner boundaries.

### State envelope

When stateful:

- canonical fact owner;
- current/history semantics;
- allowed schema/migration envelope;
- transaction/single-writer expectations;
- idempotency/conflict behavior;
- restart/recovery;
- lineage/invalidation;
- protected state.

### Resource/protection envelope

- allowed write surfaces;
- protected paths/state;
- shared DB/resources;
- external/paid/publication/destructive gates;
- isolation constraints;
- artifact/storage lifecycle if material.

### Verification outcomes

Select required layers:

- unit/property;
- integration;
- DB/currentness/recovery;
- whole-capability E2E;
- downstream compatibility;
- semantic/generalization;
- physical evidence;
- security/rights/privacy;
- perceptual/human;
- independent exact-candidate review;
- release/live evidence.

### Invalidation events

Explicit strategic conditions that force Planner return.

Ordinary implementation/test/reviewer failures are not invalidation events.

### Done when

State exact campaign-level evidence needed for a strategic terminal.

## Charter principle

Planner specifies strategic boundaries, not every command/task.

Campaign Lead is expected to discover prerequisites and dynamically plan within the envelope.
