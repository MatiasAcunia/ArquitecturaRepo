# Outcome-first execution system — I2/I3 operational correction

Status: framework operating contract. Applies to the portable software development workflow; not evidence that a third-party agent has complied. Keep existing `docs/41_V1_3_EXECUTION_ROUTE_ACCEPTANCE_AND_MILESTONES.md` as the canonical release/acceptance route. This document specifies **how an authorized campaign is made executable without spending hours reviewing its own process**.

## Why

A generic capability charter can be strategically correct and operationally unusable. If the Planner states only “import the required source files”, an execution controller without a bounded work order may invent extra engines, platform checks, provider requests and new gates, consuming hours on advisory output without delivering the requested import. Logs, tests, tokens, worktrees and checkpoints are not customer outcomes.

The failure must be repaired at the causal planning/execution interface—not by asking I3 to “think harder”, adding another Planner round, or forcing paid model evaluations on simple source processing.

## Authority boundaries

- CLIENT owns **what counts as the requested deliverable** and may accept its perceptual/content selection. CLIENT acceptance of a collection does not grant public copyright/license permission or satisfy another application's distinct source/currentness requirement.
- I1 MASTER OWNER owns portfolio-level priorities, resource allocation, competing surface locks, common failures and cross-project correction. If an L2 or I3 repeatedly does not deliver, I1 reroutes the causal mechanism, not new advisory-only engines.
- I2 Planner owns detailed **operator readiness**: true user outcome, evidence-backed source inventory, dependency classification, precise acceptance/readback and one bounded *tactical execution work order* for predictable/high-risk work. This is in addition to, not a replacement for, the capability-level charter. I2 may delegate ordinary programming implementation choices inside the charter; it may not delegate all scoping, quality thresholds, or critical execution-method selection to a weak model.
- I3 Campaign Controller is the hands-on owner: executes the order **on the machine**, selects safe implementation details, uses OS/file/process tools, recovers in-envelope errors, verifies actual files/state and reports result/receipts. It is not a second L2 and cannot invent a hard gate, demand an extra provider/model, or silently change the user's acceptance definition. An order change requires a bounded written delta and specific failing evidence, not a new campaign.
- I4 specialists are bounded assistance, not permanent stations that every file must pass through. Use deterministic OS tools for deterministic tasks; use sampled human/model visual review only when task requires perceptual judgment and no already-approved human decision exists.

## The work order: mandatory between charter and long-running I3

For any campaign with more than one materially independent operation, paid provider calls, repeated batches, or substantial runtime/cost, I2/I3 must write one source-pinned `agentic-execution-work-order-v1` contract **before executing**. A minimal machine-checkable template is in `templates/EXECUTION_WORK_ORDER.json`; `tools/work_order_guard.py` validates its structure and progress receipts. The contract is a tactical artifact inside the already-authorized campaign, never a new charter/campaign/Planner PASS.

It must include all of the following, in practical language:

1. **Exact requested output** — number/type/location and whether the requested gate is collection, preparation, quality, production rights, publication, or human perception. Different gate owners and scopes must remain separate.
2. **Pin the actual source** — repo + branch + commit (when available); canonical DB/current selector and source hashes; identify only uncertainty that can affect this output.
3. **Physical starting inventory** — what already exists, what is missing, what is trusted, what can be reused without copying/download and where it is. Never replace known files with a speculative engine.
4. **Ordered operations** — step-by-step OS/tool route, exact batch boundaries, input→output, deterministic check, fallback and bounded attempts; use available scripts/tools rather than building a new stack.
5. **Budgets and exit behavior** — limit elapsed work, paid calls, retries and consecutive zero-output cycles. At a threshold, stop repeating the method, preserve deliveries and escalate one precise question/delta to the causal owner. A long-lived Goal may span many work orders; a single unproductive I3 invocation must not run for dozens of hours.
6. **Acceptance/falsifiers** — one executable outcome/manifest and physical readback. A human acceptance must be carried as an authentic externally witnessed receipt; a JSON field or generated message cannot impersonate CLIENT. Distinguish delivery accepted from deferred downstream usage readiness.
7. **Unnecessary work prohibition** — forbid repeated download, per-file LLM scoring, full-drive rescans, duplicate worktrees, quota probing after known exhaustion and any check not required by the concrete output.

**Progress** is a delta in delivered/certified user outcomes against baseline with evidence; time spent/commits/reviews/provider tokens cannot substitute. `tools/work_order_guard.py assess` emits a *decision aid* (continue, budget stop, zero-output stop, review-ready), never an external authorization or automatic acceptance. No user-facing release PASS is granted by the guard.

## Operator example — generic batch import (synthetic)

Input: a project needs a collection of 40 source files imported and indexed. A trusted inventory already identifies 35 present, hash-verified files; five entries remain missing or invalid. The acceptance gate is **collection delivery**, not downstream transformation or public distribution.

- Phase 1: read the existing bounded inventory and confirm the 35 valid files; do not download, rescan or duplicate them.
- Phase 2: acquire or repair only the five remaining files using the project's already-authorized sources, then verify identity, content hashes and readable format. Never invent a model-based grading engine for a deterministic presence/hash check.
- Phase 3: persist the one accepted 40-file manifest, measured source evidence and the genuine CLIENT acceptance if the human gate was required and actually occurred.
- Phase 4: keep later conversion, quality preferences, publishing rights and production readiness as distinct downstream gates. An unresolved downstream gate cannot erase a genuinely finished collection gate or excuse an actual rights violation.

Elapsed time depends on the environment and actual bytes. The principle is to credit physically verified delivered files, while allowing separate later gates to remain UNKNOWN or HOLD.

## Simple bounded loop (operator)

1. Preflight once: real target, source/currentness, owner/authority, disk/capacity, minimal external permissions.
2. Execute the next highest-value physical operation from the work order (batch where reasonable).
3. Record output path, source identity, size/hash or truthful failure; update one canonical state surface.
4. Check the **delivered-outcome delta**. If zero twice with nonzero spend, switch execution method or stop for a precise decision. Do not issue equivalent paid queries with new wording.
5. Retry only the affected inputs, at most the contract's local bound. Preserve successful batch results.
6. Complete independently checkable acceptance; checkpoint only at real interruption and do not generate multiple competing CURRENTs.
7. Remove ephemeral caches/clones/uploads, retain one evidence receipt, hand off the next *real* downstream responsibility.

A high-level charter remains concise and capability-owned; a work order for a commodity execution task is intentionally prescriptive. The level of detail adapts to the risk and competence of the available executor. This resolves the apparent conflict between “no microtasks in campaign charter” and “do not leave an expensive operational decision entirely to I3”.

## Project rollout

For each existing product, independently reconstruct its **actual** latest canonical repository, DB, Goal/lease, Planner and I3 run, artifacts and source ownership before applying anything. Do not assume applying an improved framework to one repo automatically repairs active, dirty projects or historical chats. Map each long-running Goal to deliverables and bounded work orders, identify already completed sub-deliverables, and preserve human approvals. Start with read-only assessment; any production mutation needs exact live state and scoped authority. If a source or handoff package is missing, mark only that project unknown and do not invent its work status.

Acceptance is observed increase in completed, physically verified deliverables per unit of work, fewer repeat loops and less unnecessary provider spend—measured against each project's own pre-change baseline, not counted as extra architecture documents.
