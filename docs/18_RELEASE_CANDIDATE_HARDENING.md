# Release-Candidate Hardening

Version 0.9 is a hardening/reduction phase.

No new product capability is introduced merely to increase the version number.

The goal is to remove duplicated control primitives, freeze the public mechanism set and make v1 readiness executable.

## Shared control-state transaction primitive

Canonical implementation:

```text
tools/state_tx.py
```

It owns:

- exclusive local control-state locking;
- transition-journal location;
- atomic/durable JSON writes;
- staged mixed JSON/text transaction writes;
- before/after SHA-256 ownership checks;
- crash fault injection used by tests;
- roll-forward recovery;
- fail-closed external conflict behavior.

The same primitive is used by:

- `campaignctl.py`;
- `migrate_state.py`;
- `apply_adoption.py`.

The hardening self-test rejects reintroduction of private lock/journal/durable-writer implementations in runtime or migrations.

## Why this reduction matters

Before centralization, campaign runtime and adoption/migration flows could evolve subtly different recovery behavior.

That creates exactly the class of ambiguity the architecture is designed to eliminate.

The target invariant is now:

> one local control-state transaction semantics, many callers.

Project-specific application/database transactions remain separate because they own different state and failure semantics.

## Bounded governance

The release candidate keeps heavy mechanisms optional.

In particular:

- MASTER OWNER is not core;
- state/DB lineage protocol is not core;
- Campaign Lead runtime is opt-in;
- SMALL has no optional protocols by default.

Heavier profiles add mechanism families only where their failure classes require them.

## Release criteria as code

Canonical criteria:

```text
state/V1_RELEASE_CRITERIA.json
```

Runner:

```text
tools/verify_v1_release.py
```

The verifier executes the complete required evidence suite and stops at the first failed gate.

It is intentionally independent from version-number progression.

A candidate cannot become 1.0 just because 0.9 exists.

## Release candidate feature freeze

Once the v1 gate exists:

- no new generic feature enters unless one required gate is still unproven;
- a test failure is repaired at its causal owner;
- documentation-only improvements cannot substitute for missing executable evidence;
- unnecessary optional mechanisms should be removed rather than normalized into the core.

## Exact-candidate rule

The final 1.0 decision must use the exact clean release commit.

Required sequence:

1. all v1 gates pass on the release-candidate tree;
2. v0.9 history is compacted to its milestone;
3. the compacted v0.9 commit passes CI;
4. 1.0 metadata/status is applied without adding new mechanisms;
5. the exact 1.0 commit runs the full release gate;
6. only then is the starter declared 1.0.

## Post-1.0 stopping rule

After 1.0, architecture development stops by default.

Future work should be driven by:

- a concrete adoption failure;
- a reproducible correctness/recovery defect;
- a newly required generic failure class;
- a compatibility/security issue.

Not by:

- wanting another version;
- adding more roles;
- adding another policy surface;
- adding another example with no new falsifier;
- duplicating an existing owner/mechanism.
