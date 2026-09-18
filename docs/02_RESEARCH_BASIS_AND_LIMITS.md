# Evidence Basis and Limits

## Purpose

This starter encodes engineering patterns intended for sustained agentic software development.

It is a practical architecture, not a claim that any specific agent system can autonomously complete arbitrary software projects.

## Evidence philosophy

The architecture assumes that long-running agentic development should distinguish:

- declared design;
- materialized mechanism;
- physically exercised behavior;
- accepted capability.

These levels must not be collapsed.

A policy existing in a file is not proof that runtime behavior follows it. A passing test is not automatically product acceptance. A successful agent report is not independent evidence.

## Design problems addressed

The starter focuses on recurring classes of failure in long-running agent systems:

- fresh-context reconstruction;
- human/client role boundaries;
- technical responsibility leaking back to the client;
- producer-versus-independent verification;
- stale/current/superseded state;
- recovery and continuation across context changes;
- governance overhead;
- strategy/tactics separation;
- cross-component currentness;
- false-ready and false-PASS states.

## Bounded claims

This architecture is designed to make those problems explicit and testable. It does not claim that the mechanisms always solve them.

A fork should verify, in its own environment, whether:

1. durable state is sufficient for fresh-context reconstruction;
2. independent verification can falsify producer claims;
3. currentness and supersession are unambiguous;
4. tactical work can continue without unnecessary strategic round-trips;
5. the CLIENT can remain outside routine technical coordination;
6. the governance overhead is justified by the failure classes it prevents.

## Important limitations

This repository does not claim:

- arbitrary-project full technical autonomy;
- that a four-role topology is optimal for every project;
- that more agents improve results;
- that fresh-context reconstruction is solved in every runtime;
- that independent agent review is sufficient for every product property;
- that generic process rules can replace project-specific product theory.

## Validation rule

Use this progression:

`DECLARED DESIGN -> MATERIALIZED MECHANISM -> PHYSICALLY EXERCISED -> ACCEPTED CAPABILITY`

A fork must earn each transition with evidence appropriate to its own product and environment.

## Design implication

Treat this repository as a hypothesis-rich starter:

1. fork;
2. minimize;
3. adapt to the real project;
4. physically exercise mechanisms;
5. remove rules that do not pay rent;
6. retain mechanisms that prevent verified failure classes.
