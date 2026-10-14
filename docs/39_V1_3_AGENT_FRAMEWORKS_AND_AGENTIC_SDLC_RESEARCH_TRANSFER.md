# ArquitecturaRepo v1.3 — Framework Patterns and Academic Agentic SDLC: Critical Transfer Dossier

**Status: RESEARCH / DESIGN ONLY — potential v1.3, no implementation, no authorization for a new release.**
**Date:** 2026-10-14. **Public baseline:** immutable v1.2.0 tag; its accumulated implementation work and CI were completed and released. We are not reopening v1.2's historical private integration trial gates or making them adopter prerequisites. All future design decisions belong to v1.3.

**Canonical division of responsibility:**
- This dossier: source-grounded four-framework transfer hypotheses, Agentic SDLC scholarship, practical design choices and proposed falsifiers.
- [Product quality / testing plan](38_V1_3_PRODUCT_QUALITY_AND_END_TO_END_PLAN.md): two independent evaluation families (A Python and component tests; B full installed system delivering independently working software), adoption ergonomics, release quality.
- GitHub research issue #2: accumulated readings and source corrections; no second product-state/current-plan truth.
- GitHub v1.3 issue #4: compact planning/index tracker. No new parallel Planner or execution campaign is authorized by writing a document.

## A. The CLIENT-supplied report: complete four-pattern mapping and disposition

The CLIENT proposed: (1) AutoGen Observer/Actor event-loop orchestration; (2) CrewAI Pipeline/Command, role-scoped prompts and reduced context; (3) MetaGPT State/SOP/artifact-driven design first; (4) ChatDev phase gates, real test execution, automated debugging and bounded retries; combined as requirements -> validated design -> delegated construction -> tool-tested correction -> durable integration.

**Preserve these as important *hypotheses*. Do not promote the report's absolute statements to verified software-engineering laws.** The named sources differ substantially, and observations about one specific framework or evaluation setting do not prove that exactly those mechanisms universally improve product outcomes. The desired result is *natively implemented, simple and observable engineering capability*, not the adoption of changing third-party orchestration libraries.

### Pattern 1 — AutoGen / Observer-Actor / Domain events

**Original source:** Wu et al., *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*, COLM 2024, original https://arxiv.org/html/2308.08155; Microsoft's later AutoGen Core documentation describes actor-like asynchronous messaging and event-driven handlers. As of 2026 the original AutoGen repository is maintenance-mode and points to Microsoft Agent Framework; re-evaluate the active successor rather than treating a historical API as current.

**What the source actually supports:** configurable agents, human/tool-backed actors, customizable conversations, programmed interaction patterns. Later Core supports message passing and independent runtimes. **It does not establish that every small software project needs a mandatory globally centralized bus, nor that an event text message automatically authorizes an agent.**

**Relevant existing v1.2 code:** `tools/campaignctl.py` already has a revisioned `event(...)` function appending ordered activity to an existing runtime state, plus `cmd_fail`, `cmd_retry`, `cmd_recover`, authoritative state and lock handling. This is an activity log and state-machine substrate, **not** proof of a separate actor runtime, typed pub/sub delivery or native host execution.

**Tentative v1.3 transfer:**
- Typed transition envelope: `schema_version, event_id, aggregate_id/campaign_id, issuer_actor_id, causal_predecessor, source_revision/HEAD, observed_at, effect_scope, correlation_id, immutable evidence_ref/hash`; event payload is a *notice* to consult canonical truth.
- Candidate events: `REQUIREMENTS_BASELINED`, `CHARTER_AUTHORIZED`, `GOAL_STARTED`, `TASK_READY`, `I4_RESULT_AVAILABLE`, `EVIDENCE_REVIEW_DUE`, `CLIENT_DECISION_REQUIRED`, `HOST_INTERRUPTED`, `CANDIDATE_PROPOSED`. Exact registry remains subject to practical evidence; no unnecessary global taxonomy.
- A real human `CLIENT_APPROVED` must bind authenticated actor, decision, scope, expiry/epoch and target artifact. CLI text, agent-generated JSON or queued event never becomes human consent by itself.
- Use existing canonical Git/Product State/local runtime and `state_tx.py`; **no competing universal event DB**. Outbox/inbox/replay cursor only when real asynchronous loss/reordering justifies it, with bounded retention and idempotent consumers. Non-async SMALL uses direct simple calls.
- Real native host limitations are surfaced, not faked by a Python bool.

**Falsifiers:** duplicate/out-of-order/forged/stale events cannot advance authority or reapply external effects; context loss does not restart a terminated campaign; event backlog, replay, missed signal and process restart behave correctly; synchronous comparison remains faster/cheaper for ordinary small tasks. **Reject a central event bus if it adds complexity without a measurable product gain.**

### Pattern 2 — CrewAI / Pipeline-Command / Scoped roles and context

**Source classification:** official CrewAI *technical documentation* (not by itself peer-reviewed causal evidence) describes agents, processes, tasks and Flows with routing, conditional execution, structured state and persistence; see https://docs.crewai.com/en/concepts/flows. It is misleading to reduce CrewAI to a universally linear assembly line or insist that each task only receives the immediately previous output; real dependencies often require verified broader context.

**Existing v1.2:** roles CLIENT -> I1 MASTER OWNER -> I2 Planner -> persistent I3 Campaign Lead -> I4 executor/reviewer/specialist; tactical DAG and dependency/resource conflict checks in `campaignctl.py`. Static role prompts alone cannot constrain tool permissions.

**Tentative v1.3 transfer:**
- Treat each real tool invocation as a typed `Command`: issuer+authorized actor, capability, target source/asset identity, expected revision, write envelope, safety/cost bounds, inputs, output/artifact refs and independent readback.
- Role-specialized context assembled from the *current* Product State, requirements, charter, relevant source, currentness witness and bounded task-specific evidence. Do not relay giant transcripts or untrusted chat memory as truth; also do not hide required cross-file architecture context from I3.
- Keep I3 responsible for iterative debugging, in-charter refactoring, successive candidates and ordinary failures. I4 can execute narrow tasks or offer independent advice; its result is not accepted until consumed by I3 and verified. I4 cannot quietly become new Planner or override CLIENT requirements.
- Decomposition is by independently meaningful work units and interference boundaries; **not by arbitrary files or mandatory model/controller/route microtasks**. An I3 may implement a simple CRUD vertical slice coherently in one turn if faster and safer.
- Inter-role input/output contracts carry source identity, status and follow-on feedback, not merely role backstories.

**Falsifiers:** role-prompt injection cannot bypass actual mutator/write permissions; two agents cannot overwrite conflicting surfaces without lease/merge protection; truncated context does not silently ignore functional/nonfunctional requirements; any new task/pipeline layer must improve accepted feature throughput versus the baseline and reduce, not increase, Planner churn.

### Pattern 3 — MetaGPT / State, SOPs and Artifact-driven engineering

**Original source:** Hong et al., ICLR 2024, https://arxiv.org/html/2308.00352. Evidence: role-defined SOPs, materialized intermediate artifacts, shared communication, executable feedback and comparisons in the paper's selected benchmarks. The paper's engineer loop caps at three retries **for that specific experiment/implementation**, not as a universal limit.

**Existing v1.2:** real JSON schemas, validated Product State/OWNER/charter contracts, generated project profiles, conditional baselines, migrations, reviewed GC inventory and source-bound receipts. This product already owns the fundamental idea that physical/current evidence outranks conversational summaries.

**Tentative v1.3 transfer:**
- Define minimum required typed artifacts **proportionate to risk**: a minimal existing README+objective+acceptance examples for a small trivial change; explicit DB schema/API and migration/effects/contracts for a breaking data change; security/rights/privacy and rollback for high-consequence changes.
- Preserve CLIENT/I2-owned requirements and charter core; allow I3 the explicitly bounded mutable plan/conditions with monotonic CAS/permissions, but never allow a planner output or model-generated file to supersede canonical authority by mere syntactic validation.
- A contract is not trustworthy because `json.loads` succeeds. Validate semantic invariants, schema evolution, compatibility, independent acceptance, migration behavior and readback of real deployed/executable artifacts.
- Source of truth remains the existing live Git/DB/Product State. Designs are versioned with ownership and currentness, not frozen forever when evidence demands a coherent authorized redesign.
- No *universal* ban on generating code before documents, nor compulsory `database_schema.json` for a stateless script. Design-first rigor increases with the consequences of the change.

**Falsifiers:** new schema incompatible with current DB/clients is rejected; duplicate CURRENT owners fail; old design cannot be used after supersession; an AI's self-authored acceptance contract cannot replace external intended behavior; unnecessary artifacts are measured as setup/maintenance overhead.

### Pattern 4 — ChatDev / Phase gates and controlled auto-correction

**Original source:** Qian et al., ACL 2024, https://aclanthology.org/2024.acl-long.810/. Chat-chain structure, communicative dehallucination, debug across turns and evaluation limitations are source-supported. The phrase `max_retries = 3` is **not** a universal ChatDev requirement; the three-retry example derives from MetaGPT's particular executable-feedback loop.

**Existing v1.2:** many real Python scripts, CLI schema validators, `campaignctl.py` fail/retry/recover states, source-bound independent review, `state_tx.py` and `artifact_ledger.py` durable state incl pre-unlink `DELETE_INTENT`. However, a selftest exit code does not prove agent-host orchestration or user-visible software correctness.

**Tentative v1.3 transfer:**
- I3 runs the actual language-appropriate command (pytest, npm test, JUnit/Maven, static check, executable acceptance) inside a constrained worktree with real output, signed to exact source/environment identity.
- On failure, classify causal failure vs flaky test/environment/dependency/permission/product mismatch. Return bounded diagnostics with redaction, not unbounded stderr, to the *same I3 campaign* for correction. Keep an independent evaluator/hidden oracle outside the builder's write envelope.
- Adaptive retries depend on novelty of evidence, class recurrence, resource budget, verified corrections and independent review. On repeated same-class failures, shift from incremental patches to exhaustive subsystem hardening within I3; escalate only genuine charter invalidation or unsupported host/CLIENT decision.
- Rollback is not synonymous with wiping the worktree: preserve user changes, complete evidence, pre-existing DB state, and safe recovery metadata. Tests green does not promote a release; independent system behavior and approvals are separate gates.
- A functional fix must retain previous PASS behavior *and* pass new FAIL_TO_PASS tests under independent conditions, including crash/retry/side effects and real software execution.

**Falsifiers:** error injection cannot trigger runaway retries/token spend; no false recovery after ambiguous external effect; review gate invalidates after the producer changes the source; code that passes a builder-authored weak test but fails hidden API behavior remains REJECTED; short retry count does not force arbitrary Planner churn.

### The combined flow — a **proposal**, not a finished architecture

`CLIENT expresses product objective -> currentness-bound requirements baseline -> I2 capability charter if scope warrants -> persistent I3 receives authenticated command -> optional scoped I4 delegation -> implementation in managed workspace -> actual compiler/tests/execution -> feedback and in-campaign hardening -> independent code and black-box system oracle -> reviewed current artifact -> CLIENT decision only at meaningful gates -> durable deliverable`.

Events may announce some transitions; they **do not replace** canonical state, the host authority layer, or the possibility of an intentionally simple synchronous flow. Non-code domain gates differ from generic Python tests, but are not new mandatory dependencies for unrelated adopters.

## B. Academic Agentic SDLC literature: cumulative reading ledger and quality-of-evidence boundaries

Read/annotate **original sources, not names in a list**, and preserve exact paper versions, methodological differences, what is directly observed versus conjectured product transfer. This dossier consolidates current decision-relevant observations; research issue #2 maintains the accumulated longer bibliography and corrections.

**Research levels as of this revision:**
- **P01–P07 — original full-text critical reads previously recorded** in research issue #2: P01 Wu et al. AutoGen (COLM 2024); P02 Hong et al. MetaGPT (ICLR 2024); P03 Qian et al. ChatDev (ACL 2024); P04 Yang et al. SWE-agent ACI (https://arxiv.org/html/2405.15793); P05 Xia et al. Agentless (https://arxiv.org/html/2407.01489); P06 He/Treude/Lo systematic software-engineering multiagent review, 71 studies (https://arxiv.org/html/2404.04834); P07 Wang et al., *SDLC Perspective: Survey of Benchmarks*, March 2026 v3 (https://arxiv.org/html/2505.05283), **178 benchmarks from 461 papers** with roughly **61% implementation, 5% requirements and 3% design**. This corrects an earlier obsolete count in the historical issue text.
- **P08 — SWE-Bench Pro:** Xiang Deng et al., ICML 2026 (proceedings: https://proceedings.mlr.press/v306/deng26f.html; accessible original arXiv technical sections: https://arxiv.org/html/2509.16941). **Selected methodology/results/ablations/limitations now examined**, not a claim that every appendix has been comprehensively replicated or experimentally re-run. Original public benchmark has 1,865 problems in 41 repositories; the paper stresses long-horizon/multi-file patch requirements, real environments, independent verifier construction and hidden/held-out contamination risks. The paper's analysis reports performance variance across models and a strong effect of clarified requirements/interface descriptions; its explicit limitations include uneven language coverage and `FAIL_TO_PASS/PASS_TO_PASS` verifiers that may exclude valid alternative solutions. **Transfer:** multi-file independent hidden acceptance, varied languages, clarified contractual requirements before agent execution, challenge-level transparency, real repository execution and benchmark contamination audits. **Do not conclude:** every test suite is universally valid or a fixed benchmark score proves complete autonomous SDLC.
- **P09 — OpenHands:** Wang et al., ICLR 2025 (https://arxiv.org/html/2407.16741; original conference https://proceedings.iclr.cc/paper_files/paper/2025/hash/a4b6ad6b48850c0c331d1259fc66a69c-Abstract-Conference.html). **Selected platform architecture, evaluation and limitations sections now examined**, not yet a complete full-text empirical replication. Describes code+terminal/browser actions, sandbox execution, agent/tool interfaces and a breadth of benchmarks. **Transfer:** true executable tools, environment isolation, robust actions/observations, tool side-effect permissions, real end-to-end readback and reproducibility; **not** proof that adopting its entire runtime or LLM agents makes all user projects reliable.
- **P10/P11/P12 — QUEUED for technical full-text reading** (do not invent completion): the Agentic Software Engineering concept paper, six-layer Agentic SDLC synthesis, and 2026 agent-vs-human PR empirical report recorded in research issue #2. Authenticate exact canonical versions/venues and practical scope before deriving policies.
- **CrewAI Flows and Microsoft Agent Framework** are vendor-maintained technology references, not interchangeable with peer-reviewed research findings. Preserve version/date, current maintenance status and which code actually implements a claimed capability.

**Research synthesis: three conclusions worth acting on experimentally:**

1. **Simplicity competes with agency.** Agentless' localization -> repair -> validation result and SWE-agent's focused Agent-Computer Interface emphasize that careful tool and task design may outperform larger agent organizations under constrained benchmarks. v1.3 must keep a SOLO/simple path and evaluate complexity incrementally.
2. **SDLC coverage is currently uneven.** P07's 178-benchmark survey finds a strong bias toward code implementation. A mature system needs independent requirements, design, migration, deployment/operation, currentness and maintenance evaluation, not only code synthesis.
3. **Real execution, benchmark validity and tooling matter.** P08/P09 illustrate runnable code, repository tasks, hidden oracles, tool interfaces and contamination control; a '100% scripts green' milestone is neither industrial product behavior nor freedom from regression. Build B-level whole-system tests distinct from A-level Python correctness.

## C. Two-axis **industrial** v1.3 evaluation (the actual product criterion)

**The two axes are independent; authoritative details in** [docs/38](38_V1_3_PRODUCT_QUALITY_AND_END_TO_END_PLAN.md).

**A — Python internals / *The Practice of Programming*.** Table/edge testing, small and malformed inputs, crash boundary and exact output, independent golden oracle, incremental regression, selected state-machine/property tests, meaningful mutation and security tests. Actual v1.2 tools in scope: `state_tx.py`, `artifact_ledger.py`, `goal_guard.py`, `goal_plan.py`, `campaignctl.py`, adoption/scaffold/migration logic and optional adapters. Check Windows/Linux differences; never weaken critical verification merely to paint CI green. Measure test oracle quality rather than number of passing cases.

**B — industrial installed-system evaluation.** Independent QA fixtures (generic CRUD/API, preexisting relational service with migration, multi-file web/API integration, high-consequence recovery where supported) are *our* benchmark projects. A third party installs ArquitecturaRepo, submits an independently specified feature, lets its **actually supported** agent/host perform source edits and tests, then the evaluator runs hidden external behavioral tests, executes the real application, checks non-regression, interruption/recovery, source identity, review independence, costs, disk and human effort. No maintainer project may be a dependency for the user's installer.

**Control comparisons:** matched versioned model/host/budget/task family; simple v1.2 implementation versus each single proposed feature (typed commands, artifacts, events, specialist feedback), then combined variant only after individual value. Report ALL attempted runs and failing trajectories, variability, costs and pre-registered criteria. Do not invent a universal retry count, % threshold or number of workers without baseline risk evidence. False claims of native host enforcement or false independent oracle are blocking even when source tests pass.

## D. Implementation priorities *if* CLIENT/I2 authorize a v1.3 development charter

In order of actual causal need, not attractive framework features:
1. **Evidence and baseline first:** current exact v1.2 source, existing functions, setup and user promises, 2-axis tests before any new abstraction. Inspect user install experience and why I3 fails to deliver in real code.
2. **Strengthen Python-critical invariants:** real negative regression, provider ambiguity, WAL/currentness, GC durable intent, lease and permission enforcement, extra independent state-machine checks.
3. **One genuinely supported end-to-end vertical slice:** real CRUD/API request through a real installed supported host, actual commands, running application, independent oracle and review readback. This is stronger evidence than another set of YAML documents.
4. **Only if necessary: typed command+event/control seam** over existing `campaignctl`, with idempotency, actual permissions and recovery. Test against direct synchronous alternative.
5. **Real I4 request/delivery/consumption and bounded I3 goal condition edits**, only with true host integration where advertised. L3/I3 handles bug fixes and reviewer rework without inventing I2 loops.
6. **Industrial longitudinal study** on unrelated software repositories, across sessions/restarts, competing writes, migration/data, budget/capacity and private data; evaluate real user friction and cost, not just success rates.
7. **Release contract** must clearly distinguish generic portable-supported from opt-in verified-host features; version/tag/release exact reproducibility and backward-compatible upgrade without changing historical v1.2 tags.

**Hard non-goals:** adopt complete AutoGen/CrewAI/MetaGPT/ChatDev dependencies; create a global universal event bus; force every developer through Markdown/JSON SOP bureaucracy; make I4 or a separate Planner a prerequisite for one CRUD; make real coding contingent on formal documents for trivial safe changes; freeze architecture despite new evidence; declare a 3-retry cap a law; roll back by deleting user work; import third-party/private projects as installer dependencies; accumulate unnecessary worktrees, logs, package duplicates or endless synthetic evidence.

## E. Paper-learning operating procedure

When advancing the v1.3 research issue, persist for each paper:
`paper_id, exact_primary_url, version/venue/date, read_scope (abstract/selected sections/full), method, task selection, baseline, metric, ablation, quantitative result with conditions, contamination/privacy/validity threats, observation, engineering inference, simplest competing approach, candidate_existing_owner, test_falsifier, A/B outcome, adopted/rejected/deferred, next_read`.
An academic hypothesis is not a production design decision until its contribution survives baseline comparison and independent evidence; design authority remains with CLIENT/I2, and implementation with persistent I3. Update the existing research issue rather than forking duplicate living registries.

## F. Historical closure and current state

- Public `v1.1.0` and `v1.2.0` are already issued and immutable. All six historical 1.2 engineering-owner executions and the integrated PR are complete as release history. The separate 1.2 host/private-project trial evidence remains historical maintainer QA, not open user-facing installation requirements.
- This document **does not** reopen or rewrite v1.2 source/tags, start a new native controller, launch an executor, change protected projects, install external frameworks, or claim v1.3 completed.
- From here forward, focus on the **possible v1.3**, guided by actual software-engineering effect and industrial testing. Research can proceed without converting old private host trials into a blocking dependency.
