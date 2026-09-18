# Synthetic Stateful Backend Overlay

Status: CURRENT

## Product

SYNTHETIC_STATEFUL_BACKEND

## State owner

SQLite is the durable application-state mechanism for this reference.

The idempotency request row and note row are committed in the same SQLite transaction.

## Fixed invariants

- one request identity maps to one payload hash and one note;
- the same request/payload replays the existing note;
- a different payload under the same request identity is a conflict;
- application transaction failure rolls back both note and idempotency identity;
- no external service is required.

## Verification gates

- UNIT_PROPERTY
- DB_CURRENTNESS_LINEAGE_RECOVERY
- RUNTIME_PHYSICAL

## External authority

None.
