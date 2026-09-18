# Executable Validation and Scaffolding

Version 0.2 adds executable checks and a fail-closed project scaffold.

## Scaffold a project control layer

From a fork/clone of this starter:

```bash
python tools/scaffold_project.py \
  --target "../my-project" \
  --profile SMALL \
  --product-id PROJECT_ALPHA \
  --objective "Describe the client-visible product objective."
```

The command creates `.agentic-sdlc/` inside the target project.

It refuses to overwrite an existing control directory unless `--force` is explicit.

## Scaffold semantics

A generated scaffold intentionally starts as:

- Product State: `HOLD`;
- bootstrap: `UNTRUSTED_CONTEXT`;
- current code/runtime ref: `UNRECONSTRUCTED`;
- no active campaign;
- no product acceptance;
- no external authority.

This prevents the installer itself from manufacturing current truth.

Profiles select optional mechanism families but do not invent product-specific state.

## Validate a project

```bash
python tools/validate_project.py --root "../my-project/.agentic-sdlc"
```

The validator performs JSON Schema validation plus cross-file relationship checks.

## Relationships currently checked

### Product State

- one current Product State owner per product/workstream inside the validation root;
- duplicate capability ids rejected;
- Currentness Set refs must resolve;
- active campaign must have a matching charter;
- charter product/workstream must match Product State;
- charter capability must exist in Product State;
- active checkpoint/candidate ref must agree with current code ref where applicable.

### Identity and execution authority

For ACTIVE execution authority:

- only one active authority per campaign inside the validation root;
- campaign must have a charter;
- authority baseline must match charter baseline;
- Campaign Lead actor must exist;
- actor must be an active I3 Campaign Lead;
- actor current run must match authority current run;
- checkpoint ref must resolve to the same campaign.

### Bootstrap/currentness

- bootstrap product must have Product State;
- READY bootstrap cannot contain unresolved currentness;
- observed code ref must match Product State;
- requirements/Product State refs must resolve;
- active campaign and checkpoint/terminal pointers must agree with Product State.

### Terminal integrity

For readiness terminals:

- campaign charter must exist;
- required independent review must exist;
- reviewed candidate must equal terminal candidate;
- required charter verification gates must have evidence;
- a human/perceptual gate may remain open only for a terminal explicitly returning for Planner/human decision.

## Duplicate-current detection

The validator rejects duplicate current owners for identities it can mechanically identify, including:

- Product State for the same product/workstream;
- campaign charters with the same campaign id;
- checkpoints with the same checkpoint id;
- terminals for the same campaign;
- actor ids;
- active execution authority for the same campaign.

This does not replace project-specific duplicate-owner checks for custom state.

## Falsification self-test

CI intentionally creates invalid temporary states and requires the validator to reject them.

Current negative cases include:

- Product State/current checkpoint ref mismatch;
- actor/run execution-authority mismatch;
- missing terminal evidence for a required runtime gate;
- missing Currentness Set owner.

A validator change that starts accepting those states fails CI.

## Scaffold self-test

CI generates every public profile:

- SMALL;
- STATEFUL;
- ARTIFACT_HEAVY;
- MULTI_WORKSTREAM;
- MULTI_PRODUCT;
- HIGH_CONSEQUENCE.

Every generated control layer must validate.

The self-test also verifies that:

- SMALL does not silently install MASTER OWNER or execution authority;
- MULTI_PRODUCT includes the MASTER OWNER module and fail-closed authority surfaces;
- HIGH_CONSEQUENCE includes security/privacy/rights handling;
- accidental overwrite is rejected.

## What validation does not prove

A green validator does not prove:

- code correctness;
- database/runtime truth;
- semantic quality;
- perceptual quality;
- security;
- rights compliance;
- release readiness;
- CLIENT acceptance.

It proves only the generic structural and relationship properties encoded by this starter.

Product-specific gates still require product-specific evidence.
