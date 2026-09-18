# Currentness and Reconstruction

## Core rule

A fresh agent starts as `UNTRUSTED_CONTEXT`.

It becomes authoritative only after reconstructing current state from durable evidence.

## State layers

- L0 CLIENT intent evidence
- L1 normalized requirements / Product State
- L2 engineering state

Keep them distinct.

## Currentness Set

Each project defines the minimum durable set needed to reconstruct one coherent posture.

Typical members:

- root agent policy;
- CLIENT requirements;
- Product State;
- bootstrap/currentness state;
- active campaign pointer;
- current checkpoint/terminal;
- exact code/DB/runtime evidence pointers.

## Continuity-critical transition

Any change that alters what a fresh context is allowed to believe or execute is continuity-critical.

Examples include campaign activation/termination, execution authority change, provider/runtime authority change, Product State route change, supersession/invalidation and accepted-candidate transition.

For such a transition:

1. identify affected current owners;
2. update them coherently when practical;
3. otherwise fail closed as `CURRENTNESS_RECONCILIATION_REQUIRED`;
4. bind exact authority identity/evidence;
5. run a fresh-context reconstruction falsifier.

## Fresh-context probe

A new context must recover:

- role/non-role;
- current requirements/open questions;
- product objective;
- current state;
- current code/head/runtime authority;
- active campaign/checkpoint;
- current hard gate;
- strongest evidence;
- next legal action;
- forbidden action.

Failure means the continuity mechanism needs repair. Do not bridge it with chat memory.

## Precedence

Technical currentness generally follows:

`physical/live evidence > canonical current state > campaign authority > code/tests/config > reports > historical docs > chat memory`.

CLIENT intent uses its own precedence: newer explicit client authority can supersede normalized requirements and must then be persisted.
