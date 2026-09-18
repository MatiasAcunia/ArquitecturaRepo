# Identity and Execution Authority

## Purpose

Long-running agentic systems must distinguish persistent organizational identity from a model invocation, chat, process, commit author or temporary execution lease.

These are different objects.

## Identity layers

### Role class

Examples:

- I1 MASTER OWNER
- I2 PLANNER
- I3 CAMPAIGN LEAD
- I4 TEAM MEMBER

A role class defines responsibility and decision rights.

### Actor instance

A durable logical actor occupying a role for a product/workstream/campaign.

Example:

`PLANNER_PROJECT_ALPHA_001`

The actor may survive many sessions.

### Run / context

One concrete model/session/context execution.

A new run does not automatically inherit authority merely because it uses the same prompt.

### Campaign identity

Durable identity of one authorized engineering campaign.

The campaign survives context replacement and capacity interruption.

### Execution authority

The exact current permission to perform mutations for a campaign.

Execution authority may be represented by a lease, active-charter pointer, current execution record or equivalent local mechanism.

## Hard rules

- Git commit author is not actor identity.
- Chat identity is not actor identity.
- A model name is not authority.
- A prompt saying "you are the Planner" is not enough.
- A campaign being documented is not proof that it is active.
- Available code is not execution authority.

## Fresh-run reconstruction

A new authority-bearing run starts as `UNTRUSTED_CONTEXT`.

Before mutation it must establish:

- role class;
- actor instance;
- product/workstream;
- current campaign if applicable;
- current execution authority;
- exact code/state baseline;
- protected boundaries;
- current checkpoint;
- legal write surfaces.

If any material relation is ambiguous, HOLD mutation.

## Serial authority

For one canonical write surface, exactly one integration owner should exist at a time.

Parallel team members may work in isolated surfaces, but canonical integration remains singular unless the project explicitly defines a safe multi-writer protocol.

## Authority transition

When authority changes:

1. persist the new actor/run/lease relation;
2. invalidate or supersede the old current authority;
3. reconcile Product/Engineering State;
4. update the Currentness Set;
5. verify a fresh context cannot legally act under both old and new authority.

## Acceptance

Identity/currentness equality is necessary but not sufficient for product acceptance.

It establishes who/what is current; it does not prove the product capability itself.
