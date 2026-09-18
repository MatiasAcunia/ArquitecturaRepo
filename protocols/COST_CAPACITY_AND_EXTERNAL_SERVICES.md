# Cost, Capacity and External Services

## Purpose

Agentic systems often depend on metered models, compute, storage, APIs and artifact generation.

Cost and quota are architecture inputs when they affect whether the system can sustainably produce accepted outputs.

## Measure accepted-output economics

Do not optimize only headline request price.

Where relevant measure:

`total recurring cost / accepted useful output`

Include:

- rejected outputs;
- rerolls/retries;
- latency/throughput;
- storage/egress;
- operator burden;
- quota fragility;
- recovery cost;
- rights/quality constraints.

## Provider assumptions are current facts, not eternal policy

Record time-sensitive provider facts separately from durable architecture:

- model/version;
- price/quota;
- free allowance/credits;
- region;
- terms;
- rate limits;
- observed throughput/yield;
- effective cost.

Refresh before material spend or scale.

## Credits and free allowances

Treat reported/promotional credits as bounded external capacity.

Do not design correctness around an assumption that a temporary credit will always exist.

Prefer architecture that can substitute providers/models when the product contract permits it.

## Provider abstraction

Use an abstraction boundary when:

- multiple providers are plausible;
- quotas/prices change;
- fallback is valuable;
- testing can run locally/synthetically;
- product semantics can remain stable.

Do not add an abstraction merely because one could exist.

## Optimization order

Prefer, when product gates remain intact:

1. eliminate unnecessary calls/work;
2. cache/reuse safely;
3. batch;
4. reduce rejected-output rate;
5. use lower-cost equivalent models/providers;
6. exploit legitimate free/credit capacity;
7. optimize compute/storage;
8. renegotiate product quality only through proper CLIENT authority.

## Capacity planning

For a planned batch/campaign, estimate:

- required calls/compute;
- expected accepted yield;
- low/likely/high cost;
- quota headroom;
- throughput;
- restart/idempotency behavior;
- failure/retry cost.

Do not launch a large external batch from a single nominal per-call estimate.

## External-spend gate

Before material spend, bind:

- exact provider/model/current terms;
- cost envelope;
- campaign authority;
- idempotency/restart protection;
- accepted-output metric;
- stop condition.

Paid capacity is never implied by internal readiness.
