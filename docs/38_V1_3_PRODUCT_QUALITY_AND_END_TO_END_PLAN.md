# ArquitecturaRepo v1.3 — Product Quality, Industrial Verification and Real SDLC Execution

Status: **PROPOSED v1.3 product plan; not implementation, acceptance or a v1.3 release**.
Baseline: the currently published v1.2.0 generic portable starter; before execution re-read live `main`, tags, install surfaces, tools, docs and runtime.
Authority: CLIENT direction to distinguish rigorous **Python/software-component testing** from **black-box whole-system software-engineering testing**. This document is the canonical v1.3 product proposal; academic intake and exploratory hypotheses live in issue #2, not in another truth database.

## 1. Product outcome and scope boundary

v1.3 is **not a bigger pile of green Python scripts**. It should make the generic, freely installable Agentic SDLC starter more reliable at doing *actual* software engineering on an arbitrary adopter-owned repository: understanding requirements, planning proportionately, editing source through governed authority, testing, fixing, continuing after interruption, reviewing independently, delivering a runnable change and reporting exactly what remains unsupported.

Two complementary independent evidence families:

- **A / CODE CORRECTNESS:** do its Python modules, CLI tools, schemas, state transitions, file/DB transactions and adapters behave correctly under normal, boundary and adversarial inputs?
- **B / SYSTEM EFFECTIVENESS:** once a real user installs the starter, can its actual supported agent/host workflow produce and maintain an independently working software product across sessions, revisions, faults and review?

A PASS from A never counts as a PASS from B. A finished demonstration product never substitutes for A. **Maintainer test applications, private repositories, real user histories, host-specific controllers and maintainer acceptance records are NOT dependencies or gate checks imposed on adopters.** The generic installer must work without any maintainer's projects, vendor account or paid provider. Host-dependent functionality is opt-in, capability detected and accurately labelled; no false native automation promises.

Support claims must be split into `PORTABLE_SUPPORTED`, `OPTIONAL_ADAPTER_VERIFIED`, `CONFIGURED_BUT_UNTESTED`, `NOT_SUPPORTED` and `MAINTAINER_TEST_ONLY`. Never call a private product benchmark a universal installation prerequisite.

## 2. Engineering standard from *The Practice of Programming*

Apply Kernighan & Pike's engineering emphasis as **our v1.3 testing design**, not a claim that a book empirically proves this architecture:

- Keep source, APIs, invariants, error states and tests **simple, explicit, readable and modular**. Avoid duplicating business logic inside tests.
- **Test as code is written.** Every meaningful source change gets a focused executable example or falsifier before aggregating it into the release suite.
- Test boundaries and degenerate cases: empty, one, two, duplicate, malformed, maximum size, stale, missing, corrupt, permission denied, wrong type, interrupted, concurrent and unexpected ordering. Include the ordinary success path.
- Validate actual *observable results*, not only return codes, log messages, self-reported evidence or fake review approvals.
- Every real bug yields a **reproducible failing regression** before the fix; then the repair must preserve unrelated PASS cases.
- Check explanations and failures as well as success. Independent expected results, contract/oracle and golden real outputs must not come from the agent or implementation under evaluation.
- Prefer proven, small algorithms and real data structures. Measure before optimizing; do not trade clarity for speculative event infrastructure.
- Distinguish tests, tracing, benchmarking, debugging, review and user acceptance; none is a substitute for all the others.

## 3. FAMILY A — Python and component engineering

**A0: test-infrastructure trust.** Consolidate the existing v1.2 selftests, scripts, schema validators, CLI fixtures, Git/DB reference tests and CI inventory into one versioned test catalog mapping capability -> code owner -> invariant -> positive/negative oracle -> platform. Preserve working tests; do not rewrite the project just to adopt a fashionable framework. Support pytest where it makes parametrization/fixtures clearer, and preserve self-contained portable CLI entry points where useful. Enforce stable environment setup, seed, deterministic fixtures, suite duration/resource budget and no accidental network access.

**A1: deterministic correctness.** Table-driven parametrized tests of parser, contracts, policy, migrations, Goal/Plan revisions, graph/ownership, CLI exit codes, valid/invalid file names, project profiles, installer uninstall/reinstall, compatibility and exact error contracts. All advertised profiles should remain proportionate; SMALL must not inherit heavyweight orchestration or costly defaults.

**A2: property-based and model-based behavior.** On critical stateful code only, evaluate Hypothesis `@given` and `RuleBasedStateMachine` (alternative allowed if simpler). Examples: revision monotonicity and CAS, single current owner, idempotent replay, DAG acyclicity, permission scopes, GC never unlinks an unapproved byte identity, migration forward/reverse when representable, SQLite canonical snapshot/WAL invalidation, no unauthorized capability promotion. Shrink and retain the minimal falsifier as a deterministic regression. Do not declare a generated test oracle correct merely because it uses the same implementation helper.

**A3: fault injection and recovery.** For state-changing code, enumerate transitions and make failures deterministic **before/after** journal, write/fsync, unlink, rename, commit, external effect, acknowledgement, crash and restart. Include ENOSPC, EACCES, missing directory, symlink/hardlink, corrupt manifest, stale Git HEAD, changed DB snapshot, overlapping process/lease, clock anomalies, retry with same/different key, and Windows/Linux filesystem differences. Observe final on-disk bytes and state after a fresh process; no 'exited HOLD' alone as evidence of correctness.

**A4: concurrency and security.** Concurrent writers, stale lease and identity impersonation, prompt/tool-output injection, directory traversal, zip bombs, secrets in evidence/logs, untrusted source paths, malicious migration payload and unexpected event ordering. Fail closed on destructive and protected paths; never imply a Python guard intercepts a native host command when it cannot.

**A5: mutation / independent quality of tests.** Use selective mutation testing on risky safety logic: inverted checks, dropped persistence, wrong default path, ignored revision, skipped permission, double effect, WAL-main-only hashing. A mutant that survives should lead to a justified test improvement or an explicit equivalent/nonapplicable explanation. Report *mutation score by critical subsystem* and missing observed behaviors; line coverage is diagnostic only, never a target that can replace correctness. Choose and cost-profile tooling; `mutmut` currently needs fork support/WSL on Windows, so make its execution optional and platform-aware.

**A6: package and consumer portability.** Hermetic checkout + fresh install in Linux and Windows; supported Python versions tested from an explicit matrix; fresh and existing repository workflows; defaults do not create vendor-specific jobs or report to external services; idempotent repeat install, safe decline of destructive upgrades, opt-in adapters, correct reversible migrations when promised, no private product identifiers. Check exact built artifact vs tagged source, LICENSE and no secret leaks.

**A-deliverable:** one fast regression command for contributors, a comprehensive reproducible CI suite, a bounded scheduled stress/mutation path, test catalog and machine-readable per-subsystem falsifier/evidence report. No blanket requirement for a new installed test service or permanent cache.

## 4. FAMILY B — does the installed system do actual software engineering?

**B0: independent evaluation contract.** An evaluator unaffiliated with the implementation fixes product requirements and hidden external behavior tests **before** the agent sees the task. The agent may inspect, plan, implement and test, but cannot modify acceptance or substitute its own fixture. Preserve task text, starting repo SHA, permissions, oracle, OS/runtime/model/host versions, available tools, budget, costs and full outcome including failure. Keep benchmark secrets away from the agent; do not make public hidden tests into training hints.

**B1: actual first-use journey.** As an unrelated adopter: fork/clone or use a release in an *empty and a nonempty* repository; select SMALL or appropriate profile; complete product requirements/technical baseline; run available installation, validation and discovery commands; start a real supported agent execution if the host offers it; request a small feature; inspect actual Git diff, independently run code and acceptance tests. 'Scaffold validated' does not satisfy 'feature delivered'. A host-independent setup test still counts as a useful partial but not end-to-end agent success.

**B2: at least three different programming contexts, treated only as benchmark fixtures (not user dependencies):**
1. A clean small Python HTTP CRUD service, seeded with a task and hidden HTTP oracle (create/read/update/delete, invalid input, persistence and restart).
2. A **preexisting** Java/Spring Boot + PostgreSQL service with a realistic feature, schema migration, foreign-key/transaction behavior, backwards-compatibility constraints and Docker build/run; seeded defects and changes must be fixed without breaking old consumers.
3. A preexisting JavaScript/TypeScript web+API or another language ecosystem with a cross-file requirement, build pipeline, component/interface behavior, security boundary and acceptance through a real app/test runner.

Add independent small/medium/long-running tasks, not only generation from empty boilerplate. All three are self-contained disposable benchmark applications owned by QA; no user of ArquitecturaRepo must use those languages, databases or containers. Alternative ecosystems can substitute if they provide stronger independent coverage.

**B3: complete lifecycle and handoff.** Observe traceable CLIENT request -> requirements decisions -> architecture trade-offs -> capability charter -> I3 implementation -> tests -> independent I4 or human review when configured -> necessary in-campaign rework -> runnable change -> exact commit/PR -> readback -> user acceptance. One failed test should trigger repair within the same I3 envelope, not an infinite Planner/charter churn. Measuring *actual correctness and user intervention required* is more important than counting generated documents or commits.

**B4: multi-session interruption and recovery.** Pause at hard points: edited but uncommitted source; DB transaction+WAL; after remote side-effect before acknowledgement; after source moves beyond last review; lost agent context; tool quota pause; restart; I4 delayed answer; conflicting concurrent edits. Resume against live Git/currentness/DB, reject stale actors, never blindly resend an ambiguous effect, preserve existing user changes. A simulated timer does not prove native host Goal control. Test all host-specific claims only on supported and independently provisioned adapters.

**B5: high-consequence and hostile evaluation.** Attempt unauthorized overwrite of existing code, private path export, fabricated reviewer PASS, ignored CLIENT constraints, data-loss migration, flaky test laundering, test-only patch that fails a hidden oracle, noncooperating writer/GC race and unowned resources. Require independent falsifiers and safe containment; no harmful effects on real end-user projects.

**B6: end-user ergonomics.** An ordinary developer must understand what the product provides, select the correct profile, ask for a task, inspect real status/next action, control costs/permissions, recover from an interruption and remove/upgrade the starter without needing knowledge of the maintainer's repositories or internal test-control plane. Measure user setup time, interventions and confusing failure states.

**B-deliverable:** independently reproducible public smoke benchmark + withheld benchmark fixtures + real installation/operation/recovery reports per claimed support configuration. A successful generic release does **not** require a particular private adopter's database, daypack, Goal scheduler or developer machine.

## 5. Feature improvements 1.3 may earn, not assume

Implement a capability only after baselining the working v1.2 and proving that a simpler path is inadequate:

- **Verified, safe engineering actions:** consistent tool/host operation boundary, authentic lease/currentness, explicit write envelope, host-verified capabilities and permissions. A Python-only preflight must say 'advisory' unless native enforcement exists.
- **Protected intent with bounded mutable execution conditions:** immutable CLIENT/I2 Goal core + explicitly authorized, CAS-versioned I3-adjustable conditions without scope escalation; deterministic Plan review against actual work evidence, not caller-supplied minutes.
- **Delegated work that actually returns:** I4 consultant/worker/reviewer REQUESTED -> DELIVERED -> CONSUMED_BY_I3 -> INDEPENDENTLY_VALIDATED, budgets, explicit code/evidence lineage and human escalation when required. SOLO baseline remains available.
- **Robust transactions and recovery:** continue hardening file GC/journals, SQLite WAL, external-effect ambiguity and interrupted upgrades based on reproduced failure modes, not opaque layers.
- **Optional asynchronous orchestration:** only if an A/B test demonstrates meaningful reliability/productivity benefit over a simple synchronous pipeline under the same task, host/model/budget. Events are derived from canonical state, never another owner. Do not copy AutoGen/CrewAI/MetaGPT/ChatDev frameworks merely for their terminology.
- **Better real-product status:** show delivered features, tests actually run, current defects, live authority and user decisions; do not inflate 'green' through synthetic successes.

Every new capability needs portable contract + black-box observable effect (where advertised) + simplicity/latency/cost comparison + rollback and deletion lifecycle + falsifiers. Do not turn optional integration into compulsory installer complexity.

## 6. Academic research pipeline: cumulative original papers, read with criticism

Reuse the annotated research registry from issue #2; **do not reset or duplicate** its prior reading. The previously recorded seven full-text critically read works are P01 AutoGen, P02 MetaGPT, P03 ChatDev, P04 SWE-agent, P05 Agentless, P06 He/Treude/Lo systematic review of 71 studies, and P07 Wang et al. SDLC benchmark survey (current cited version: **178 benchmarks / 461 papers**). P08 SWE-Bench Pro (ICML 2026), P09 OpenHands, P10 agentic SE concepts, P11 agentic SDLC synthesis and P12 AIware agent/human PR study had only summary/metadata review at prior intake; do **not** silently upgrade them to full-read.

For every new primary paper: stable ID, exact version/date/venue, actual sections read, question/methodology/baselines, task sampling, measurements/variance, limitations/contamination threats, replicability/source, what the paper **does** establish, our **inference** about product architecture, alternative simpler design, falsifier and measured before/after adoption result. Classify vendor docs/framework manuals separately from peer-reviewed research.

Prioritize further full-text review in relevance order: SWE-Bench Pro industrial multi-file evaluation; OpenHands real tool execution; independent oracles and benchmark contamination; model-based/stateful testing; reliability/fault injection and AI-agent governance; then framework orchestration A/B. Research is cumulative and actionable only when a transferred hypothesis improves independently measured product results.

Primary public reference examples:
- https://proceedings.mlr.press/v306/deng26f.html (SWE-Bench Pro, ICML 2026)
- https://arxiv.org/abs/2405.15793 (SWE-agent: agent-computer interfaces)
- https://arxiv.org/abs/2407.01489 (Agentless/simple baseline)
- https://hypothesis.readthedocs.io/en/latest/stateful.html (tool documentation, not peer-reviewed evidence)
- https://mutmut.readthedocs.io/en/latest/ (tool documentation, not peer-reviewed evidence)

## 7. Evaluation design and anti-gaming

A release report needs **separate A and B tables**; no averaging a systemic failure away with 1,000 cheap unit PASSes.

Measured outcomes, by task/cohort:
- Code: failing/green regressions, mutation survivors, invalid input outcomes, platform portability, state-machine invariant breaks, crash recovery consistency, unauthorized writes, dependency vulnerabilities and escaped defects.
- System: independent feature acceptance, runnable endpoint/build, no regression in old features, correctness of DB migration, successful resume and rollback, unapproved destructive effects, reviewer findings consumed, human interruptions, developer setup friction and dollars/tokens/wall-time/tool calls.
- Efficiency: source changes per accepted requirement, recurring defect patterns, churn/loops, disk used and cleanup, idle agent loops, duplicated Git checkouts, complexity of runtime setup.

Benchmark with equal model/host/tools/task distribution/spend limits across v1.2 SOLO baseline and each 1.3 variant. Fix or record random seeds and run repeated independent attempts; report median and spread, failures and ceiling budget. Detect contaminated tasks, fake functional mocks, tests written or relaxed after the outcome, and hidden-oracle leakage.

Do not invent universal fixed pass rates or an arbitrary requirement for 100 agents/100 projects. Derive thresholds from baseline measurement and severity. Hard safety constraints: no unapproved private data export, protected modifications, false independent signoff, silent test skipping or ambiguous effect replay. A claimed capability must succeed under its *published supported envelope*, not only an offline toy fixture. A host not offered to the general installer cannot be required for the entire generic release.

## 8. Workstreams, sequence and release gates

**Phase 0 — product truth + risk inventory:** inspect tagged 1.2, current main, supported flags, installers, generated assets and tests. Identify any release docs promising only simulated host support. Produce capability-to-risk-to-test matrix and **measured v1.2 baseline**. No rewrite or artificial acceptance requirements.

**Phase 1 — A testing modernization:** consolidate test catalog/harness; add boundary, property, stateful, mutation and fault/recovery falsifiers on highest-risk code. Preserve selftests and release reproducibility. Independent reviewer demonstrates that selected deliberately broken code is caught and normal code still passes.

**Phase 2 — B consumer benchmark:** disposable fresh+legacy projects, external oracle first, one real complete feature each in supported software ecosystems, actual execution sessions/commits/runnable product, plus interruption, upgrade and recovery. Publish reproducible sanitized public fixtures and keep independent held-out evaluations with explicit licensing.

**Phase 3 — causal product improvements:** use real defects/results to choose safe Goal/Plan native semantics, scoped delegation, transactional reliability and optional adapters. I3 owns ordinary bug/reviewer rework; I2/CLIENT review only new capability boundaries and material interface or authority changes. No proliferation of campaigns for recurring fixture failures.

**Phase 4 — industrial adversarial and comparative runs:** full system longitudinal/multi-version tasks; hostile inputs, rollback, security, resource exhaustion, injected crash, Windows and Linux support where advertised; A/B against v1.2 under comparable budgets; fail variants that cost more without material quality gain.

**Phase 5 — publish v1.3:** versioned contract and README with clear supported vs optional capabilities, exact tagged-source CI, A+ B evidence and independent reviewer signoff. Release only explicitly claimed and verified generic capabilities; retain internal test reports as maintainer evidence. Preserve stable v1.1/v1.2 tags and user data.

Authority: CLIENT chooses product tradeoffs/approves high-risk effects; I2 Planner owns strategic capability charter (WHAT/WHY/gates/owner/falsifier), persistent I3 owns implementation/debugging/recovery/integration, scoped I4 assists and independent review checks the real output. One canonical current plan; research issue #2 is not a second runtime.

## 9. Definition of done and explicit non-goals

A 1.3 candidate is **not finished** merely because all scripts print PASS, because a demo video looks good, or because multiple agents exchanged messages. It is done when:
1. **A**: independently reproducible tests protect critical Python/state invariants, catch seeded bugs, preserve backward compatibility and verify durable crash/recovery.
2. **B**: independent observers can repeat *real* adopter install -> requested code change -> running application -> external acceptance tests -> regression -> interruption/recovery -> deliverable on a declared supported platform and host.
3. The open-source public documentation and generated scaffold are generic and require none of the maintainer's private project names, slots or machine setup.
4. Comparative results show which 1.3 mechanisms improve reliability, correctness or operator cost over v1.2; rejected ideas remain auditable.
5. Cumulative academic reading is source/version-level and never passed off as proven architecture. A human can audit risks, limitations, source identity and privacy.
6. Exact release commit, source manifests, installer bytes and A/B receipts are independently checkable. No test is allowed to bless its own implementation by weakening the acceptance oracle.

Non-goals: new global event bus by default, mandatory extra agent framework, giant transcripts/doc pyramids, arbitrary fixed test counts, making non-Python adopters install Python QA frameworks into their product, automatic subscription charges, claiming unverified native Codex automation, or requiring maintainer's unrelated workstreams as integration dependencies.

**This document is a proposed product plan**, not a new v1.3 implementation, published acceptance, or alteration of v1.2 release history.