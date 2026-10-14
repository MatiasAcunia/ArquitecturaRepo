# ArquitecturaRepo 1.3 — Target Software Architecture and Engineering Design

Status: **DESIGN BASELINE / PROPOSED**, not built or accepted. Date: 2026-10-14.
Authority: CLIENT's request for an integral v1.3 design grounded in Software Engineering, the entire span of *The Practice of Programming* (Kernighan and Pike), cumulative academic Agentic SDLC research, and two independently measured test families.
Main product: a portable, open-source agentic software-development starter that a third party can install in **their own** project. Maintainer applications, internal test Goals, proprietary machinery and the four historical portfolio workstreams are NOT end-user dependencies.

Related canonical records: [doc 38 — two-axis industrial testing](38_V1_3_PRODUCT_QUALITY_AND_END_TO_END_PLAN.md); [doc 39 — four-framework and primary-paper transfer](39_V1_3_AGENT_FRAMEWORKS_AND_AGENTIC_SDLC_RESEARCH_TRANSFER.md); research issue #2; v1.3 planning issue #4. This document owns the **proposed target architecture**, while doc 41 owns the **execution and acceptance route**. Historical v1.2 tags are immutable.

## 1. Evidence-based starting point: what exists and what does not

Physically inspected on 2026-10-14: the v1.2.0 tag points to the historical release commit, while the later main branch contains further public-source changes and research documentation. Verify their two different exact SHAs from Git before using either as a baseline; never infer byte equality across them. The immutable v1.2.0 tag remains the public regression baseline, while a freshly inspected main is the proposed starting surface for v1.3.

Existing source owners (do NOT fork them):
- `tools/campaignctl.py` plus `schemas/campaign-runtime.schema.json`: persistent campaign lifecycle, typed work states, DAG/resource conflicts, `event()` revisioned activity log, failure/retry, freeze, independent review, strategic terminal and recovery. It is NOT itself a real LLM/agent host.
- `tools/state_tx.py`: bounded local transaction/journal, exclusive lock, atomic writes, crash/recovery paths; never invent another canonical DB.
- `tools/goal_guard.py`, `tools/goal_plan.py`, `schemas/goal-contract.schema.json`, `schemas/tactical-plan.schema.json`: immutable Goal core and CAS-reviewed mutable Plan with byte-bound evidence. I3-editable **bounded Goal conditions** remain a desired additional capability; editing Plan alone does not satisfy them.
- `tools/artifact_ledger.py`, `schemas/artifact-ledger.schema.json`: source/ownership-bound artifacts, reviewed safe GC, durable DELETE_INTENT before unlink and selected ledger. This does not establish safety under noncooperating filesystem writers.
- `tools/cognitive_i4.py`, `schemas/cognitive-consultation.schema.json`: bounded consultation and phases including delivered/consumed; an internal recorded phase does not establish independently verified native I4 communication.
- `tools/external_effects.py`, `schemas/external-effect.schema.json`: ambiguous/at-most-once recovery modeling; no generic exactly-once guarantee for arbitrary remote providers.
- `tools/scaffold_project.py`, `tools/apply_adoption.py`, `tools/reconstruct_context.py`, `tools/validate_project.py`, profile/templates/migrations: portable project installation, currentness and schema/adoption paths.
- `tools/codex_daily_control_adapter.py`: **read-only** package/installed-byte preflight, not a verified native runner. Latest main has no maintainer project names in its expected slots; the historical 1.2.0 tag still does. The controller is a separate optional package, not an architecture-core prerequisite.
- Many real selftest/CI tools, SQLite/WAL tests and six install profiles. These are **component proof**, not proof that a real agent delivered a complete software feature to an unrelated user.

First v1.3 action is to reconstruct the executable source/host/adopter truth, not to rewrite v1.2 code on assumptions.

## 2. Product experience, roles and scope

An ordinary software developer should be able to:
1. Install in a new or existing repository on a declared supported OS/Python version.
2. Describe the product objective and constraints, select a proportional profile, approve required risky choices.
3. See a single comprehensible source-bound current status and the next action.
4. Select an **installed, detected, expressly authorized compatible agent host** (the portable core remains usable without one).
5. Submit a feature request; see actual code edited in an isolated managed working surface, real build/tests run, defects repaired by the same I3, review consumed, and a source-bound candidate delivered.
6. Interrupt, safely resume, inspect cost, read independent test results, accept/reject and upgrade/remove without losing user-owned files.

Support tiers must be explicit and machine-checkable:
- `PORTABLE_CORE` — validation, scaffolding, state, manifests, CLI, offline tests;
- `HOST_VERIFIED` — runtime adapter and exact host/build+permission/continuation capabilities measured in that environment;
- `HOST_ADVISORY` — can provide a plan, inspection, or export but cannot enforce native side-effects;
- `UNSUPPORTED` — refuse claims/actions that this runtime cannot guarantee;
- `MAINTAINER_TEST_ONLY` — evaluation cohort, never adopter prerequisite.

Preserve authority: CLIENT is product owner and authorizes consequential effects; I1 MASTER OWNER governs the whole portfolio only where selected; I2 Planner owns capability-level architecture and material charter; persistent I3 Campaign Lead owns ordinary implementation/debugging/refactoring/retries, integrated final candidate, in-envelope tool execution and feedback; I4 bounded workers/specialists/reviewers have scoped contracts and cannot silently become Planner. A SIMPLE/SOLO project should not have to instantiate I1/I2/I4 machinery merely to implement a safe CRUD operation.

## 3. Architecture: one coherent monolith with replaceable external ports

**Prefer a modular Python codebase over microservices, mandatory event bus, generic agent framework or a second orchestrator.** Existing files and schemas remain canonical owners. Some candidate adapters are separate optional packages. Suggested logical layers:

1. **UX / project bootstrap** — existing `project_setup`, `scaffold_project`, `apply_adoption`, `project_status`, `reconstruct_context`. A *thin* new `tools/agentic.py` facade may be admitted only after usability testing proves that today's CLIs force users to understand internal scripts. Any facade delegates to existing tools; it must not become another state authority.
2. **Product policy / authority / commands** — existing Goal guard, protected/client theory, charter, currentness, leases, CAS and authority validation. New command validation must bind actor identity, scope, source revision, tool/effect permissions, budget, expiry and user approvals to physical evidence, not a prompt.
3. **Orchestration / campaign domain** — existing `campaignctl` and its revisioned runtime state. Default sync path directly executes the next authorized work unit. Bounded optional worker/event dispatch extends the same state machine only when demonstrated useful for real WAIT/RESUME and I4 delivery.
4. **State/persistence** — existing Git source, Product State and currentness references, `state_tx`, workspace/artifact ledger and provider effect receipts. No second current Product State, global event database, ad hoc truth in chat, or case-insensitive collision with user files.
5. **External ports** — `HostPort` (actual agent host), `ToolPort` (bounded shell/test/build commands), `ReviewPort` (source-bound independent reviewer), `EffectPort` (provider idempotency/reconciliation) and optional `SchedulerPort` (observed capacity/recurrence). Ports are testable without real accounts via fake adapters, but release claims require actual host checks.
6. **Evaluation/quality** — independent A-level Python component tests, B-level black-box repo/task runner and independent acceptance oracle, exact run/effect readbacks and comparative performance/cost measurements.

Suggested dependency direction:

`CLI -> application commands -> domain invariants -> canonical state transaction -> external ports`.

Implementations depend on domain interfaces, not domain logic on Codex/Windows APIs. No worker may write protected surfaces just because it produced an accepted-looking Markdown file.

### 3.1 Port/DTO contract candidates — NOT implemented today

**HostCapabilities (read-only):**
`adapter_id, host_product, adapter_version, host_build, platform, authentication_state, permission_enforcement, sandbox_modes, thread_start, thread_resume, turn_stream, cancel, external_effects, supported_working_roots, quotas_observable, observed_at, expiry, evidence_digest`.
A capability needs physical signed/source-bound observation; no caller-provided `verified=true`. For a host lacking an operation return `UNSUPPORTED`, not best-effort private SQLite manipulation.

**EngineeringCommand (single-action authorization):**
`command_id, campaign_id, actor_id, role, source_sha, expected_state_revision, operation, affected_surfaces, allowed_mutation_scope, effect_class, permissions_ref, approved_budget, expiration, idempotency_key, input_evidence_refs`.
Validation is independent of the LLM: check current actor/lease/source/Goal/human envelope before dispatch; after dispatch read back actual filesystem/Git/tool result. Stale commands fail closed.

**AgentTurnReceipt:**
`command_id, thread_id, turn_id, host_build, actor, source_before, source_after_or_diff_digest, observable_tool_actions, exit_or_host_status, begun_at, finished_at, bounded_cost_if_observed, output_digest, privacy_classification, error_class`. Never use turn text as self-authentication.

**TestExecutionEvidence:**
`source_tree_sha, test_command_argv, cwd_or_ephemeral_root, environment_digest, tool_version, exit_code, bounded_log_artifact_ref, expected_test_oracle_ref, recorded_files_or_effects, run_id, reviewer`. Evidence that a command printed PASS cannot substitute for a hidden independent application behavior oracle.

**Review/Acceptance:**
`candidate_source_sha, declared_capability, tests_executed, independent_reviewer_identity, findings, conflicts, accepted_scope, protected_client_approvals, post_review_invalidation_rev, disposition`.
A reviewer cannot validate its own code change and an owner cannot edit a hidden evaluation answer after results.

Schemas should be added **only when their first consuming tool and test are included in the same capability** (provisional file candidates: `schemas/host-capabilities.schema.json`, `schemas/engineering-command.schema.json`, `schemas/agent-turn-receipt.schema.json`, `schemas/independent-evaluation.schema.json`). Do not create a museum of unused schemas or duplicated artifact-current registers.

### 3.2 Real host choice, without turning the core into a vendor product

2026 upstream evidence: public Codex Python SDK documentation includes `Codex.thread_start`, `thread_resume`, streaming, `Sandbox.read_only` / `workspace_write` and published interpreter/runtime version matching. TypeScript SDK similarly supports `startThread`, `resumeThread` and JSONL event streaming. See https://github.com/openai/codex/blob/main/sdk/python/docs/getting-started.md and https://github.com/openai/codex/blob/main/sdk/typescript/README.md.

**Preferred first experiment:** a clearly optional, version-pinned Python Codex SDK `HostPort` adapter on disposable worktrees. Verify SDK on real supported Linux/Windows before labelling `HOST_VERIFIED`, including login, thread start/continuation, sandbox, permission readback, crash/resume, source diff and rejection of unauthorized effects. If SDK cannot expose enforced scope or receipts, narrow the supported claim and keep a manual/fake-adapter path rather than hack undocumented native state. Windows Codex Daily Control 2.1 remains a **separate optional host-continuity integration**, not a default or required dependency; resolve actual API compatibility before writing its native bridge. Do NOT claim the read-only 2.1 package preflight is agent execution.

Longer term another adapter may be implemented through a documented local CLI, TypeScript SDK or independent vendor. Host-independent policy and QA tests must still pass unchanged. No universal raw token or account credential collection.

## 4. Key domain state transitions and authoritative semantics

**Campaign/Goal state:** CLIENT requirements -> (proportional) approved baseline -> charter authorized if needed -> I3 active -> runnable command -> scoped implementation -> verifiable evidence -> independent review -> accepted candidate or in-campaign repair -> user decision at meaningful gates. Preserve `campaignctl` and `state_tx` transition ownership, not a competing generic FSM.

**Bounded Goal conditions:** current `schemas/goal-contract.schema.json` has immutable core fields and no I3-editable conditions. Propose one signed versioned annex inside the *same logical Goal identity*, with `core_digest`, `conditions_revision`, `editable_schema_scope`, `editor_actor`, `lease_epoch`, `justification/evidence`, `last_accepted_source_rev`. I3 may change tactical scheduling, hypotheses, resource envelope inside caps, completion mechanics and verified blockers; it may NOT widen `hard_gates`, `forbidden_effects`, `write_envelope`, meaning of done, external authorization, CLIENT requirements, or I2 charter scope. Atomic CAS + append durable decision ref + verify core digest. A Plan edit is not Goal change; both must be coordinated without duplicating owners. For an I3 request outside scope, return to I2/CLIENT with a concrete proposed delta.

**Delegation:** optional I4 flow `REQUESTED -> AUTHORIZED -> DELIVERED -> CONSUMED_BY_I3 -> INDEPENDENTLY_REVIEWED -> ACCEPTED/REJECTED` with source/role/budget/request version, exact artifact digest, confidentiality and unchanged currentness. Delivered without consumption is incomplete; consultant feedback is advice, not authority.

**Tools and external effects:** for deterministic, reversible workspace tools, verify actual effects after execution. For irreversible or remote effects, require prepared intent+approval/provider idempotency+reconciliation; response lost != safe retry. HOLD with precise cause if exact effect unknown; no global exactly-once promise.

**Failure handling:** `FAILED` work remains in the *same* campaign; classify syntax/build/test/requirements/environment/flaky/host/currentness/authority/effect. Keep minimal reproducible log and causal hypothesis; test incremental correction and regression. Repeated same-class defects => subsystem-wide hardening and independent reviewer **inside I3**, not three arbitrary retries then new charter. Escalation only on material change of scope/authority/architecture.

**Durable context and startup:** first read actual repository current HEAD, Product State, ownership, pending transactions, active actor and leases, Goal/Plan, current artifacts, provider receipts; only then issue next command. Chat transcript is untrusted context; host resume must not supersede canonical current state. Every restart maintains idempotence and does not create duplicate canonical copies. State evolution/migration is explicit, backward-compatible and safe.

**Optional events:** current `campaignctl.event()` is an ordered activity log, not a pub/sub engine. If real supported asynchronous handoff justifies it, add one bounded typed command/event projection in that runtime with CAS replay checks and retention; never a mandatory global message bus for SMALL/SOLO.

## 5. The Practice of Programming — full nine-chapter engineering mapping

The source's actual 1999 table of contents covers Style, Algorithms/Data Structures, Design/Implementation, Interfaces, Debugging, Testing, Performance, Portability, and Notation, plus collected rules. We are **applying principles as design judgment**, not claiming to have reproduced or read every page in this artifact. Publisher: https://www.pearson.com/en-us/subject-catalog/p/practice-of-programming-the/P200000009026/9780133133417 ; chapter index: https://www.oreilly.com/library/view/the-practice-of/9780133133448/toc.html .

1. **Style:** precise naming: `source_revision` is not `approved_revision`, `observed` is not `verified`, `advisory` is not `enforced`. Keep functions small, explicit errors, idiomatic Python, no giant nested dispatch functions. Do not introduce dozens of invented abbreviations or duplicate status fields.
2. **Algorithms/data structures:** map state machines/DAG and owners to minimal appropriate maps/sets/adjacency relations; bounded-size indexes and stream log reads; avoid repeated filesystem traversal, quadratic full-tree hashing or unconditional deep Git clones. Define complexity only where data sizes warrant it.
3. **Design/implementation:** build complete, useful vertical slices with a real observable output, then generalize only from known variation. Refactor around *one canonical owner and one source path*, not historical file names. Choose explicit invariants and known libraries instead of microservices and meta-frameworks.
4. **Interfaces:** command / evidence / host boundary contracts with precise inputs, outputs, error families, ownership, permission and versioning. Isolate uncertain APIs behind the smallest possible adapter; do not expose mutable internal `dict`s as free-floating authority.
5. **Debugging:** capture smallest repro, classify failure, isolate cause, fix systemic invariant, verify with logging + actual observable files and application behavior, remove obsolete logs; never chase a PASS by bypassing a failing gate.
6. **Testing:** systematic positive/negative/boundary, malformed/empty/one/duplicate/max, full sequence stateful, fault injection, independent expected outputs and regression at each code change. Two independent A Python and B entire-system evaluation axes; mere test counts never certify product correctness.
7. **Performance:** measure user time to first accepted feature, total model tokens/cost/latency/host calls, repeated file scans, worktree/disk waste and worst-case recovery; only optimize diagnosed bottlenecks; keep SOLO path efficient.
8. **Portability:** Python stdlib core where practical; optional pinned SDK/test extras, isolated OS host interfaces, Windows vs Linux paths/locks/sqlite/fsync behavior, UTF-8/i18n, install/uninstall/rollback and user-readable errors. A developer using Java or JS must NOT install Hypothesis in their app.
9. **Notation:** minimal versioned JSON Schema for machine contracts, readable Markdown for humans, stable CLI verbs and process exit codes; prefer declarative data for policy over string parsing of model prose, avoid designing a second language/interpreter to describe obvious task commands.

Engineering checks on every capability: `Why this abstraction?`, `Smallest working alternative?`, `Expected inputs and edge cases?`, `What fails on disk/process/host interruption?`, `Who owns current state?`, `What observable artifact proves it worked?`, `What simpler baseline is being beaten?`, `What would falsify it?`, `What does it cost?`, `How to remove/rollback?`.

## 6. Threat model and response architecture

| Threat | Owner/authority | Required mitigation or honest unsupported label |
| --- | --- | --- |
| Stale Git/Goal after agent resume | state/currentness + HostPort | Pin source SHA and state revision; fail stale command, recover idempotently. |
| Agent can write outside its envelope | host permission boundary + command validator | Host sandbox enforced where supported; otherwise read-only/advisory and no false native guarantee. |
| Model/selftest fabricates approval | CLIENT decision/ref + independent QA | Authenticated exact artifact consent; independent hidden oracle; no self-signing. |
| External effect sent twice after timeout | EffectPort + provider owner | Durable intent, reconciliation and idempotency evidence; HOLD if ambiguous. |
| GC deletes replaced file | artifact ledger + filesystem/host authority | Pre/post unlink controls, durable intent, cooperative-root guarantee; exclude uncontrolled noncooperating writers from support. |
| Untrusted prompt/tool-output injection | command boundary + confidentiality | Label untrusted text, separate instruction authority, redacted logs and export rules. |
| I3/I4 concurrent writes conflict | campaignctl + source/lease | Resource-interference checks, source-bound write envelope, independent merge/readback. |
| Rerun after crash duplicates cleanup or stages | state_tx + artifact ledger | Journal, CAS, idempotency, bounded artifacts, recovery on startup. |
| Tester changes its own hidden oracle | independent evaluator owner | Separate test custody/immutable task/oracle before execution and withheld scoring. |
| Scalability collapses with 1000 files/tasks | performance/instrumentation | Reuse real Git delta, bounded registries, measure before optimizing. |
| User migrates/removes starter | scaffold/adoption owner | Marker-owned files, preview+explicit decision, no deletion of user assets or source. |

Privacy/data: no user credentials in receipts or full chat logs; no outbound telemetry without informed configuration and privacy policy. External SDK login stays with provider. Disk is protected: reuse one canonical checkout, temporary worktrees only when required, clean after evaluation, canonical evidence by hash/path not duplicated payloads.

## 7. Research transfer decision matrix

- **AutoGen actor/event:** MAYBE later opt-in runtime, after real loss/replay/async failures; default NO mandatory bus. Existing event log is starting point.
- **CrewAI command/pipeline:** YES to typed command/role/context boundaries, but no single mandatory linear chain, microtasks or prompt-enforced permissions.
- **MetaGPT artifact/SOP:** YES to risk-proportionate typed evidence contracts; NO universal schema-before-code rule and NO perpetual immutable design blocking justified refactor.
- **ChatDev correction loop:** YES to real test runner + same-campaign causal feedback; NO fixed three retries, no automatic unsafe rollback and no 100%-green promotion.
- **SWE-agent:** YES to tool UX and observable Agent-Computer Interface principles; compare against a thin supported adapter rather than whole-framework import.
- **Agentless:** YES as a genuinely simpler competitor for localization->repair->validation, particularly SOLO workflows; complexity must earn its keep.
- **SWE-Bench Pro / OpenHands:** YES to multi-file real tasks, reproducible environments, external oracles and contamination checks; benchmark limitations explicitly reported.
- **SDLC surveys:** YES to testing requirements, architecture, operation, recovery and maintenance beyond code writing; literature is not proof our implementation works.

Research maturity/status and exact primary-source caveats remain in doc 39 and issue #2; do not silently convert abstract-level reading into fully validated findings.

## 8. Architecture acceptance and refactoring discipline

A design is not accepted by creating more code, JSON files, commits or roles. Its first proof is an unrelated adopter getting a real requested feature running with fewer human interventions and acceptable cost relative to v1.2, while currentness, safety, privacy, test independence and existing code behavior remain intact.

Every implementation must have an owner, existing impacted surfaces, seam/interface contract, migration and compatibility plan, exact test oracle, crash and concurrency failure modes, independent reviewer and rollback. Prefer additive changes with reversible migration; zero dangerous upgrades in users' repositories. Experimental optional adapter work may live in isolated fixtures while the portable core remains usable.

**Decisions fixed for the proposed v1.3 architecture:** generic open source; Python-first modular core; one canonical state owner per concern; simple SOLO baseline; two genuinely independent test families; no compulsory third-party framework, native controller, global bus, extra role or private test project; authenticated write/effect boundary; persistent same-campaign I3 debugging; risk-proportionate artifacts and actual user software outcomes.

**Decisions not yet fixed without measurements:** which specific host adapter reaches HOST_VERIFIED; whether events improve async operation; new schemas beyond first consumer; exact task difficulty/cost thresholds; additional agents; which performance optimizations warrant complexity. Doc 41 defines empirical gates to decide these.
