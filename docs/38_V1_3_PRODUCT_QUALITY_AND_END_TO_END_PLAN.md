# ArquitecturaRepo v1.3 — Product Quality, Industrial Verification and Real SDLC Execution

Status: **CLIENT-CORRECTED v1.3 product/QA scope; not implementation, acceptance or a release**. 2026-10-15. The authoritative acceptance/milestone definitions live in `docs/41_V1_3_EXECUTION_ROUTE_ACCEPTANCE_AND_MILESTONES.md`. Later M7 optional package/plugin absorption is deferred until M0–M6 are actually accepted.
Baseline: the currently published v1.2.0 generic portable starter; before execution re-read live `main`, tags, install surfaces, tools, docs and runtime.
Authority: explicit CLIENT scope: distinguish component tests from independent end-to-end ArquitecturaRepo framework capability tests. This plan supplies QA rationale; doc 41 owns specific milestone gates. Do not turn model coding performance into a framework release requirement. Research hypotheses live in issue #2, not another current-state owner.

## 1. Product outcome and scope boundary

v1.3 is **not a bigger pile of green Python scripts**. It must make ArquitecturaRepo itself operate coherently: client intent and authority, Goal/Plan/charter/campaign lifecycle, owner boundaries, safe command and optional host adapters, truthful execution receipts, state/currentness, I3 rework, independent review, failure recovery, portability, security and reporting. Model skill in writing application software depends on the chosen model, tool access, environment and task, and is NOT a guarantee made by ArquitecturaRepo.

Two complementary independent evidence families:

- **A / CODE CORRECTNESS:** do its Python modules, CLI tools, schemas, state transitions, file/DB transactions and adapters behave correctly under normal, boundary and adversarial inputs?
- **B / FRAMEWORK EFFECTIVENESS:** after real installation on disposable new/existing repositories, does each declared ArquitecturaRepo capability and interface work end-to-end, including honest support detection, bounded effects, state transitions, invalidation, recovery and reporting? Application quality and model coding success are observed separately.

A PASS from A never counts as a PASS from B. Neither a successful nor an unsuccessful externally generated application substitutes for an independent framework test. A model failure must not become a framework failure unless ArquitecturaRepo mishandles authority, dispatch, state, review, error classification, recovery or its declared contract. **Maintainer test applications, private repositories, real user histories, host-specific controllers and maintainer acceptance records are NOT dependencies or gate checks imposed on adopters.** The generic installer must work without any maintainer's projects, vendor account or paid provider. Host-dependent functionality is opt-in, capability detected and accurately labelled; no false native automation promises.

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

## 4. FAMILY B — installed framework capability verification

**B0: QA-owned framework oracle.** Independently freeze the initial source/state, advertised profile and capabilities, protected write surfaces, expected authority and transition graph, effect receipts, recovery constraints and falsifiers. The implementer cannot silently edit the oracle. A model-authored application's business correctness is not this oracle.

**B1: installation and adoption.** Exercise the actual public installer on a fresh and on an existing disposable repository. Verify profiles, preserved user files, product/state ownership, discovery, CLI behavior, upgrade/removal and no required maintainer-private services or databases. Test portable-only operation without credentials.

**B2: capability lifecycle.** With deterministic responses and fault-injection, exercise CLIENT intake, Goal core and mutable I3 Plan constraints, charter/actor/lease authority, campaign transitions and next-action under ACTIVE/PAUSED/HOLD, independent reviewer receipts, rework in the same campaign, I4 result consumption where supported, currentness/invalidation, state persistence, crash recovery and honest terminal classification. Assert actual filesystem and DB effects, not written policy or agent self-report.

**B3: optional host/vendor interoperability.** HostPort/ToolPort must use versioned, documented capability negotiation; explicit authentication/permission and write boundaries; safe timeouts, cancellation, idempotency and effect receipts. No provider is compulsory. Test deterministic port conformance without credentials. For EACH adapter advertised as physically VERIFIED, independently run a bounded real operation against that actual compatible host and observe permissions, source/effects and resumption. Unavailable integrations must be labelled not supported/configured but unverified, never counted as PASS. OpenAI/Codex is an optional possible adapter, not ArquitecturaRepo's structural identity.

**B4: adversarial and longitudinal recovery.** Across independent processes, test stale/forged actor, two writers, invalid Goal CAS, source changed after review, interrupted WAL/GC, ambiguous effect receipt, unauthorized protected write, untrusted instructions in tool output, provider failure/rate limit and disk exhaustion. Fail closed without data loss or fabricated acceptance. Verify restored bytes, ledger/DB, lineage and next legal action.

**B5: portability and economics.** Test the declared OS/runtime/profile combinations and a range of disposable repository shapes, not the AI's ability to solve all languages. Provider/model/browser differences are inputs and support-matrix entries. Report costs/tokens only where observed; vendor calls/fees are opt-in. Keep SOLO/manual and portable behavior practical when agent execution is absent.

**B6: separation of failure ownership.** A model may be asked to edit a simple fixture to test dispatch, observation, failure feedback and bounded rework. Test PASS when the framework handles a model failure correctly and reports a blocked or failed external task truthfully. Test FAIL when framework state, authorization, receipts, downstream review or acceptance lie or corrupt state. A runnable CRUD, model benchmark score or hidden application oracle may be additional diagnostic evidence, never a mandatory release dependency for core ArquitecturaRepo.

**B deliverable:** reproducible black-box framework tests plus independent receipts mapped to every *advertised* capability and optional adapter. A synthetic port test establishes the portable contract; a real-provider test establishes only the corresponding advertised live integration. No blanket guarantee of all vendors, models or third-party applications.

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

**Phase 2 — B framework validation:** disposable fresh/existing repos, independently pinned framework oracles, actual state/command/receipt/review/invalidation/recovery lifecycle and separately tested optional native adapters where advertised. A small application task may exercise the interface; model task success is not a framework prerequisite.

**Phase 3 — causal product improvements:** use real defects/results to choose safe Goal/Plan native semantics, scoped delegation, transactional reliability and optional adapters. I3 owns ordinary bug/reviewer rework; I2/CLIENT review only new capability boundaries and material interface or authority changes. No proliferation of campaigns for recurring fixture failures.

**Phase 4 — industrial adversarial and comparative runs:** full framework lifecycle and longitudinal/multi-version state tests, hostile inputs, rollback, security, exhaustion, crash injection and claimed OS/host support. Compare framework-controlled quality and overhead against v1.2 under comparable conditions; keep model performance separate.

**Phase 5 — publish v1.3:** versioned contract and README with clear supported vs optional capabilities, exact tagged-source CI, A+ B evidence and independent reviewer signoff. Release only explicitly claimed and verified generic capabilities; retain internal test reports as maintainer evidence. Preserve stable v1.1/v1.2 tags and user data.

Authority: CLIENT chooses product tradeoffs/approves high-risk effects; I2 Planner owns strategic capability charter (WHAT/WHY/gates/owner/falsifier), persistent I3 owns implementation/debugging/recovery/integration, scoped I4 assists and independent review checks the real output. One canonical current plan; research issue #2 is not a second runtime.

## 9. Definition of done and explicit non-goals

A 1.3 candidate is **not finished** merely because all scripts print PASS, because a demo video looks good, or because multiple agents exchanged messages. It is done when:
1. **A**: independently reproducible tests protect critical Python/state invariants, catch seeded bugs, preserve backward compatibility and verify durable crash/recovery.
2. **B**: independent observers can repeat installer -> authenticated/configured lifecycle -> authority -> command/receipt -> state/currentness -> review/rework -> interruption/recovery -> honest status and artifact readback, across declared supported profiles. Real host execution is mandatory only for an adapter specifically advertised as live-supported. No universal model coding or working-application requirement.
3. The open-source public documentation and generated scaffold are generic and require none of the maintainer's private project names, slots or machine setup.
4. Comparative results show which 1.3 mechanisms improve reliability, correctness or operator cost over v1.2; rejected ideas remain auditable.
5. Cumulative academic reading is source/version-level and never passed off as proven architecture. A human can audit risks, limitations, source identity and privacy.
6. Exact release commit, source manifests, installer bytes and A/B receipts are independently checkable. No test is allowed to bless its own implementation by weakening the acceptance oracle.

Non-goals: guaranteeing agent coding skill or externally generated app success; requiring any particular AI/vendor/platform; new global event bus by default; mandatory extra agent framework; giant transcripts/doc pyramids; arbitrary fixed test counts; forcing adopter-specific QA languages; automatic paid calls; claiming unverified native host automation; requiring maintainer's private projects, transcripts or controllers.

**This document records product QA scope, not executed evidence, release approval or an alteration of v1.2 history.** Use doc 41 and live source/currentness for M0–M6; reserve M7 optional package absorption until the earlier gates are accepted.