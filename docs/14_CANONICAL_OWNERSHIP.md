# Canonical Owner Registry and Supersession

Version 0.6 adds an optional generic ownership graph for durable project concerns.

The architecture already has dedicated ownership rules for known contracts such as Product State, campaign authority and runtime state.

The owner registry fills a different gap: project-specific or extensible concerns that otherwise become informal conventions.

New scaffolds generate it by default. Existing projects without it remain valid.

## Canonical surface

```text
state/OWNER_REGISTRY_CURRENT.json
```

Schema:

```text
schemas/owner-registry.schema.json
```

The registry is scoped to one product/workstream.

## Core rule

For every concern represented in the registry:

> exactly one owner is CURRENT.

Older owners may remain in the same registry as `SUPERSEDED` lineage.

Two CURRENT entries for the same concern are invalid.

A concern with only superseded entries and no current owner is also invalid.

## Owner record

A registry owner declares:

- `owner_id` — stable identity for this ownership epoch;
- `concern_id` — the thing being canonically owned;
- `scope` — product/workstream/domain scope;
- `status` — `CURRENT` or `SUPERSEDED`;
- `surface_ref` — durable canonical surface;
- `surface_type` — file, directory or external surface;
- `required_in_currentness_set` — whether Product State must include this surface in its Currentness Set;
- `supersedes_owner_ids` — prior owner identities replaced by this owner;
- `superseded_by_owner_id` — successor identity for an old owner.

## Generated core concerns

Fresh scaffolds register the reusable control-layer concerns:

- `AGENT_ENTRYPOINT`;
- `CLIENT_REQUIREMENTS`;
- `PRODUCT_STATE`;
- `CURRENT_BOOTSTRAP`;
- `PROJECT_OVERLAY`;
- `CANONICAL_OWNER_REGISTRY`.

Profiles with explicit identity/execution authority also register:

- `IDENTITY_REGISTRY`;
- `EXECUTION_AUTHORITY`.

This does not mean every state file must be placed in the generic registry.

Dedicated campaign/runtime contracts remain governed by their own identity/currentness semantics.

## Currentness binding

A CURRENT owner can declare:

```json
{
  "required_in_currentness_set": true
}
```

For local file/directory owners, validation then requires:

1. the surface physically exists;
2. Product State includes the exact owner surface in its Currentness Set.

A superseded owner cannot remain required in currentness.

This prevents a registry from naming one current owner while reconstruction still loads its predecessor.

## Known-contract alignment

For known core concerns, the validator cross-checks the registry against the actual canonical state.

Examples:

- `CANONICAL_OWNER_REGISTRY` must point to the registry being validated;
- `PRODUCT_STATE` must point to the actual Product State file;
- `CURRENT_BOOTSTRAP` must point to the actual current bootstrap file;
- `CLIENT_REQUIREMENTS` must agree with bootstrap `requirements_ref`;
- `PRODUCT_STATE` must agree with bootstrap `product_state_ref`.

This makes the registry evidence-bound rather than a second disconnected declaration.

## Supersession

A replacement owner should keep the old entry and add a new CURRENT entry.

Example:

```json
{
  "owner_id": "OWNER_REQUIREMENTS_002",
  "concern_id": "CLIENT_REQUIREMENTS",
  "status": "CURRENT",
  "surface_ref": "state/CLIENT_REQUIREMENTS_V2.md",
  "supersedes_owner_ids": [
    "OWNER_REQUIREMENTS_001"
  ],
  "superseded_by_owner_id": null
}
```

The old entry becomes:

```json
{
  "owner_id": "OWNER_REQUIREMENTS_001",
  "concern_id": "CLIENT_REQUIREMENTS",
  "status": "SUPERSEDED",
  "required_in_currentness_set": false,
  "supersedes_owner_ids": [],
  "superseded_by_owner_id": "OWNER_REQUIREMENTS_002"
}
```

The links must be reciprocal.

The replacement surface must also be promoted through the relevant currentness/bootstrap refs.

## Supersession invariants

Validation rejects:

- unknown superseded owner IDs;
- unknown successor IDs;
- one-sided lineage links;
- superseding an owner from a different concern;
- supersession cycles;
- superseded owners still marked as required currentness;
- more than one CURRENT owner for a concern;
- no CURRENT owner for a represented concern.

## Why owner identity is separate from a path

A path can remain stable while ownership semantics change, or a concern can move to a new path.

Therefore:

```text
owner_id != surface_ref
```

The stable owner identity lets lineage remain explicit even when files are renamed or replaced.

## Custom project concerns

A fork can add concerns such as:

- `DATABASE_MIGRATION_STATE`;
- `MODEL_REGISTRY`;
- `PUBLICATION_QUEUE`;
- `ASSET_CATALOG`;
- `DEPLOYMENT_INVENTORY`;
- `SECURITY_EXCEPTION_REGISTER`.

The test is not “is this file important?”

Use the registry when ambiguity over which surface is authoritative would create material reconstruction or execution risk.

Do not create one registry entry for every file.

## External owners

`surface_type = EXTERNAL` exists for concerns whose canonical authority lives outside the local repository.

The generic validator does not claim it can prove an external resource exists from a local path.

A project using an EXTERNAL owner must supply project-specific verification for accessibility/currentness.

## Relationship to Currentness Set

The Currentness Set answers:

> what evidence must a fresh context load now?

The owner registry answers:

> which durable surface is authoritative for this concern, and what did it supersede?

They overlap, but they are not the same abstraction.

An owner can be canonical without needing to be loaded on every bootstrap.

## Relationship to Git history

Owner identity and supersession must not be inferred from commits.

Git history can be evidence, but:

- commit author is not ownership;
- latest modified file is not automatically current;
- path movement is not supersession;
- branch movement is not execution authority.

The registry records the explicit current ownership relation.

## Self-test

CI runs:

```text
tools/selftest_ownership.py
```

The test proves:

- generated core owner graph validates;
- duplicate CURRENT owners fail;
- a required owner missing from Currentness Set fails;
- dangling successor references fail;
- supersession cycles fail;
- a fully reconciled requirements-owner supersession passes;
- cross-concern supersession fails.

## Limits

The owner registry does not decide which architecture is correct.

It does not replace:

- Product State;
- campaign charters;
- execution authority;
- database lineage;
- runtime locking;
- review/acceptance gates.

It makes canonical ownership and supersession mechanically reconstructible where generic project state would otherwise be ambiguous.
