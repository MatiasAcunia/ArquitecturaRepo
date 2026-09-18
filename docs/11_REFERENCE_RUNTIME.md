# Optional Reference Campaign Runtime

Version 0.3 adds a minimal durable Campaign Lead runtime.

It is optional.

The architecture remains usable without adopting this controller.

## Purpose

`tools/campaignctl.py` materializes part of the I3 Engineering Campaign Lead operating loop:

- persistent tactical work units;
- dependency-aware READY state;
- append/reprioritize/retire work;
- write-surface and shared-resource conflict prevention;
- actor/run attribution;
- failure/retry;
- HOLD and capacity checkpoint/resume;
- durable checkpoints;
- execution-authority acquisition/release;
- exact review freeze;
- independent review binding;
- review invalidation after later producer/tactical mutation;
- typed strategic terminal requests.

The runtime does not decide product requirements or strategic architecture.

It does not accept a product.

## Preconditions

A real project should already have:

- current CLIENT requirements;
- Product State;
- one authorized campaign charter;
- exact current code/state authority;
- a coherent Currentness Set.

If explicit identity/execution-authority surfaces exist, the runtime respects them.

## Initialize

From the starter/fork:

```bash
python tools/campaignctl.py \
  --control-root "../my-project/.agentic-sdlc" \
  init \
  --charter "campaigns/CAMPAIGN_001/CHARTER.json"
```

If Product State does not yet name the charter as active, initialization fails unless the caller explicitly uses:

```text
--activate-product-state
```

That flag is for an already authorized Planner boundary. It is not a shortcut for self-authorizing a campaign.

## Add tactical work

```bash
python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" add \
  --id W1 \
  --title "Implement capability slice" \
  --priority 100 \
  --write "src/service.py" \
  --resource "db:primary"
```

Dependencies are explicit:

```bash
python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" add \
  --id W2 \
  --title "Integrate downstream path" \
  --depends W1
```

A blocked unit becomes READY only when its dependencies are DONE.

## Start work

```bash
python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" start \
  --id W1 \
  --actor BUILDER_001 \
  --run RUN_001
```

The controller rejects concurrent ACTIVE work when declared write surfaces overlap or shared-resource identities collide.

Those checks are conservative coordination guards, not a substitute for database/application concurrency controls.

## Verify and complete

```bash
python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" verify \
  --id W1 \
  --evidence "evidence/unit.json"

python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" done \
  --id W1 \
  --result-ref "candidate/ref-001" \
  --evidence "evidence/integration.json"
```

Failed work can remain in the same campaign:

```bash
python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" fail \
  --id W1 \
  --note "Generalized defect found"

python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" retry --id W1
```

This is the normal path for in-charter defects.

## Reprioritize or retire work

```bash
python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" reprioritize \
  --id W2 --priority 200

python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" park \
  --id W3 --note "Not on current critical path"

python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" supersede \
  --id W4 --note "Replaced by generalized implementation"

python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" cancel \
  --id W5 --note "No longer required"
```

## Capacity and HOLD

```bash
python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" capacity \
  --reason "Execution capacity unavailable"

python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" resume
```

or:

```bash
python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" hold \
  --reason "Currentness contradiction"
```

A capacity interruption does not manufacture a new campaign.

## Checkpoint

```bash
python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" checkpoint \
  --integrated-ref "candidate/ref-003" \
  --summary "Integrated current campaign state."
```

The controller writes:

```text
campaigns/<campaign_id>/CHECKPOINT_CURRENT.json
```

and reconciles, where present:

- runtime current checkpoint;
- Product State current code ref;
- Product State active campaign pointer;
- Product State Currentness Set;
- bootstrap observed/current pointer;
- ACTIVE execution authority checkpoint ref.

A fresh context should therefore be able to discover the current runtime and checkpoint without chat memory.

## Crash recovery

Multi-file currentness transitions are journaled. If the process dies after only part of a transition is applied, normal `show`, `next` and mutation commands fail closed while the live journal exists.

Recover explicitly:

```bash
python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" recover
```

Recovery rolls forward only while each target is provably still in the recorded before-state or already in the expected after-state. An externally modified target produces a persistent `CONFLICT` instead of being overwritten.

See `docs/12_TRANSACTION_RECOVERY.md` for the full transaction and failure contract.

## Execution authority

If the project uses identity/execution-authority surfaces:

```bash
python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" authority-acquire \
  --actor CAMPAIGN_LEAD_001 \
  --run RUN_I3_001
```

The actor must exist, be ACTIVE, be an I3 Campaign Lead and bind the same run.

Release:

```bash
python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" authority-release \
  --actor CAMPAIGN_LEAD_001 \
  --run RUN_I3_001
```

When an execution-authority surface exists but is not ACTIVE, mutation commands fail closed.

## Review freeze

When all tactical work is terminal and the candidate is exact:

```bash
python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" freeze \
  --candidate-ref "candidate/ref-003"
```

Independent review:

```bash
python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" review \
  --reviewer REVIEWER_001 \
  --run RUN_REVIEW_001 \
  --verdict PASS_FOR_STRATEGIC_RETURN \
  --evidence "evidence/review.json"
```

A reviewer who produced DONE work in the same candidate is rejected.

If producer/tactical work changes after the freeze/review, the favorable freeze is invalidated. The correct route is a new freeze and fresh review.

## Strategic terminal request

Example:

```bash
python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" terminal \
  --type CAPABILITY_READY_FOR_PLANNER_ACCEPTANCE \
  --reason "Exact candidate satisfies the campaign evidence envelope."
```

Readiness terminals require:

- a REVIEWED exact-candidate freeze;
- reviewed candidate == current integrated ref;
- no unfinished tactical work.

The runtime then stops at a strategic boundary.

Planner, CLIENT or another authority owner still performs the applicable strategic/product gate.

## Inspect

```bash
python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" next
python tools/campaignctl.py --control-root "../my-project/.agentic-sdlc" show
```

## Independent validation

`campaignctl.py` is not its own acceptance oracle.

`tools/validate_project.py` independently checks runtime properties including:

- runtime/charter/product identity;
- unique work ids;
- dependency existence and DAG acyclicity;
- dependency/state coherence;
- ACTIVE write/resource conflicts;
- event-log sequence and revision integrity;
- runtime/checkpoint ref consistency;
- runtime/Product State consistency;
- runtime/execution-authority checkpoint/currentness;
- reviewed-candidate identity;
- producer/reviewer separation;
- strategic-terminal/request consistency;
- no unfinished work behind readiness terminals.

## Self-test

CI runs `tools/selftest_runtime.py`.

The synthetic lifecycle physically exercises:

- separate write conflict;
- separate shared-resource conflict;
- dependency blocking;
- capacity interruption/resume;
- authority release/reacquire;
- fault-injected checkpoint/currentness recovery;
- external recovery-conflict preservation;
- exact review freeze;
- independent review;
- post-review invalidation;
- fresh re-freeze/re-review;
- strategic terminal;
- final independent validation.

## Limits

This reference runtime does not:

- execute arbitrary agents/processes by itself;
- manage cloud workers;
- provide distributed locking;
- replace Git/database transactions;
- infer product requirements;
- determine semantic/perceptual quality;
- decide Planner/CLIENT acceptance;
- guarantee security or rights compliance.

It is a minimal durable control-plane reference, not a universal orchestration engine.
