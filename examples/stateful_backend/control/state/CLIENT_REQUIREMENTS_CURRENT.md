# CLIENT Requirements — CURRENT

Status: CURRENT

## Product objective

Provide a durable local note store reference that demonstrates persistent state and request idempotency.

## Hard requirements

- Creating a note with the same request identity and payload is idempotent.
- Reusing a request identity for a different payload is rejected.
- Committed notes survive store reconstruction.
- A failure inside one create transaction does not leave partial durable state.

## Boundary

This is a synthetic local reference. It is not a production service or deployment authorization.
