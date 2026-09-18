# Transfer and Adoption Workflow

Version 0.8 turns starter installation into a reproducible, fail-closed workflow for unrelated projects.

The workflow is:

```text
existing project
    ->
fail-closed scaffold
    ->
read-only inventory
    ->
explicit adoption spec
    ->
preflight on copied control state
    ->
journaled promotion
    ->
validate
    ->
fresh-context reconstruction
```

The tooling does not infer product truth on behalf of the CLIENT or Planner.

It mechanizes the transition after an agent has reconstructed that truth.

## 1. Scaffold

Create a project-local control layer:

```bash
python tools/scaffold_project.py \
  --target "../project" \
  --profile SMALL \
  --product-id PROJECT_ALPHA \
  --objective "Initial product objective"
```

The control layer starts:

- Product State: `HOLD`;
- bootstrap: `UNTRUSTED_CONTEXT`;
- no active campaign;
- no external authority.

The existing application is not rewritten.

## 2. Read-only project discovery

Generated scaffolds include:

```text
tools/discover_project.py
```

Example:

```bash
python .agentic-sdlc/tools/discover_project.py \
  --project-root "." \
  --output ".agentic-sdlc/discovery/PROJECT_INVENTORY.json"
```

The inventory contains deterministic metadata:

- relative path;
- byte size;
- SHA-256;
- suffix;
- total file count/bytes;
- top-level entries.

It excludes common generated/vendor/control directories including:

- `.git`;
- `.agentic-sdlc`;
- `node_modules`;
- Python virtual environments;
- `__pycache__`.

The inventory does not copy source contents into the control layer.

## 3. Adoption spec

An agent performs product/domain reconstruction and writes an explicit adoption spec conforming to:

```text
schemas/adoption-spec.schema.json
```

The spec states, rather than guesses:

- product/workstream identity;
- exact current-code ref;
- product objective;
- normalized requirements;
- open product questions;
- observed capabilities;
- evidence refs;
- currentness refs;
- custom canonical owners;
- architecture invariants;
- state semantics;
- verification gates;
- external-authority boundaries;
- next legal boundary;
- forbidden actions.

This is the strategic/human-readable judgment boundary.

The tool does not create these decisions itself.

## 4. Preflight

Apply:

```bash
python .agentic-sdlc/tools/apply_adoption.py \
  --control-root ".agentic-sdlc" \
  --spec ".agentic-sdlc/adoption/ADOPTION_SPEC.json"
```

Before touching canonical current state, the tool:

1. validates the adoption spec;
2. resolves every local evidence/currentness/custom-owner ref;
3. checks product identity across Product State/bootstrap/owner registry;
4. rejects an active campaign;
5. builds the complete proposed requirements/Product State/bootstrap/owners/overlay state;
6. copies the existing control layer to a temporary candidate;
7. applies the proposed state only to that copy;
8. runs the normal project validator against the copied candidate.

A candidate that does not validate never reaches canonical state.

## 5. Journaled promotion

After successful preflight, adoption updates these surfaces as one local transaction:

- `state/CLIENT_REQUIREMENTS_CURRENT.md`;
- `governance/PROJECT_OVERLAY.md`;
- `state/PRODUCT_STATE_CURRENT.json`;
- `state/CURRENT_BOOTSTRAP_STATE.json`;
- `state/OWNER_REGISTRY_CURRENT.json`.

The generic transaction engine is:

```text
tools/state_tx.py
```

It uses the same transition-journal contract as the reference campaign runtime.

A crash mid-adoption therefore leaves one recoverable transaction rather than a falsely coherent partial control layer.

## 6. Recovery

If a process dies during adoption:

```bash
python .agentic-sdlc/tools/state_tx.py \
  --control-root ".agentic-sdlc" \
  recover
```

Fresh reconstruction refuses to proceed while the transaction journal remains live.

Recovery rolls forward only where before/after hashes prove the target is still owned by that transaction.

## 7. Retry semantics

Reapplying an adoption spec that already exactly describes current state returns:

```text
ALREADY_ADOPTED
```

It validates the existing control state but does not increment Product State or rewrite current owners.

A materially different spec is a new adoption/currentness change, not an idempotent retry.

## 8. Post-adoption posture

A successful baseline adoption without an active engineering campaign should reconstruct:

```text
RECONSTRUCTED_NO_ACTIVE_EXECUTION
```

That means:

- currentness has been positively verified;
- current durable owners are known;
- the baseline capability model is reconstructible;
- no I3 execution authority is invented;
- future engineering requires a strategic campaign boundary.

## Transfer test matrix

CI runs:

```text
tools/selftest_adoption.py
```

It creates six unrelated temporary project shapes:

- SMALL;
- STATEFUL;
- ARTIFACT_HEAVY;
- MULTI_WORKSTREAM;
- MULTI_PRODUCT;
- HIGH_CONSEQUENCE.

For each project the test requires:

- application files exist before installation;
- scaffold succeeds;
- repeated inventory is deterministic;
- inventory excludes the generated control layer;
- explicit adoption succeeds;
- repeated adoption is idempotent;
- project validation succeeds;
- fresh-context reconstruction succeeds;
- reconstructed currentness is verified;
- no active execution is invented;
- original application files remain byte-identical;
- profile-specific protocol burden is correct.

The test additionally fault-injects a crash during one adoption and proves recovery through the generic transaction journal.

## Governance-burden checks

The transfer matrix also verifies selected negative properties.

For example:

- SMALL does not receive MASTER OWNER;
- SMALL does not receive the stateful protocol;
- SMALL does not receive the optional Campaign Lead runtime unless explicitly requested;
- STATEFUL receives state/lineage/idempotency semantics;
- ARTIFACT_HEAVY receives artifact lifecycle + cost/capacity semantics;
- MULTI_PRODUCT receives MASTER OWNER;
- HIGH_CONSEQUENCE receives security/privacy/rights/external-action semantics.

This is part of keeping governance proportional.

## CLIENT boundary

Adoption tooling removes technical file-editing work from the CLIENT.

It does not eliminate legitimate product authority.

The CLIENT may still be needed for:

- ambiguous product-visible behavior;
- product objectives;
- subjective quality;
- business/economic tradeoffs;
- external authority.

The CLIENT should not be needed to:

- decide JSON shapes;
- edit owner registries;
- repair currentness sets;
- coordinate atomic writes;
- recover transaction journals;
- decide which technical protocol file must be copied.

## Claim boundary

Passing the adoption matrix demonstrates transfer of the control architecture across several unrelated synthetic shapes.

It does not prove universal transfer to every repository or domain.

A real fork still has to supply project-specific product truth and evidence.
