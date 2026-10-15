# ArquitecturaRepo v1.3 — Engineering Execution Route, Gates and Milestones

Status: CURRENT PRODUCT ACCEPTANCE ROUTE, **NOT PROOF OF EXECUTION OR RELEASE**. Revised per explicit CLIENT scope correction 2026-10-15. Ownership: CLIENT owns the product; I2/Planner owns strategic capability charters, persistent I3 owns actual engineering and ordinary repairs, scoped I4 supports and independent QA validates.
This route operationalizes [the target software architecture and TPP engineering design](40_V1_3_TARGET_SOFTWARE_ARCHITECTURE_AND_TPP_ENGINEERING.md), [the independent A/B testing program](38_V1_3_PRODUCT_QUALITY_AND_END_TO_END_PLAN.md) and [the academic/framework analysis](39_V1_3_AGENT_FRAMEWORKS_AND_AGENTIC_SDLC_RESEARCH_TRANSFER.md). It is the single canonical v1.3 sequence. Academic readings are tracked in research issue #2; issue #4 indexes the plan, rather than duplicating a second mutable plan.

## 1. Product destination and invariant boundaries

An unrelated developer should be able to install the starter in a new or existing repository and exercise each advertised ArquitecturaRepo capability correctly: intake and authority, Goal/charter/Plan and campaign state, optional supported execution transport, traceable actual tool/host effects, bounded I3 rework, independent review receipt and invalidation, continuation after interruption, currentness, rollback and honest terminal/reporting. The framework controls and observes engineering workflows; it does not guarantee that a chosen model can solve an arbitrary programming task or that model-authored code is correct.

The generic portable core must work without maintainer-owned products, a particular vendor, a private controller, a second global database, heavyweight agents or a paid subscription. The real agent execution path requires a compatible, expressly authorized host; absent such a host, the product must say so and offer a usable manual/portable path, never fake code execution. Full agent effectiveness is a separate product-support claim, not a condition that every general user install our QA benchmarks.

The predecessor v1.2.0 tag stays immutable. Current main includes later integration/docs and must be compared against that exact tag before implementation. A shipped version is not implicitly equal to a newer main commit. Every proposed feature must be compatible with this upgrade boundary or have an explicit safe migration and truthful breaking-change decision.

Two *independent* evidence families: A = internal Python/contract/transaction correctness; B = end-to-end correctness of the installed ArquitecturaRepo lifecycle and each advertised integration/capability in a representative real or disposable repository. Neither substitutes for the other. B may use deterministic fault-injectable adapters for the portable lifecycle, but native-host support requires an independently observed real host operation. Failure by an underlying AI model to solve an application task is recorded separately from framework defects; incorrect authorization, state, execution receipt, gates or reporting is a framework failure.

## 2. Ownership, controls and one integration branch

Before coding, I2 performs strategic PASS1 end-to-end and PASS2 adversarial review, then issues one capability-level charter covering the earliest connected critical-path results. It must contain the actual user outcome, authority, scope, source refs, interfaces, risks, A+B testing, permissions, capacity, falsifiers and return boundary—not prescribe each implementation microtask. A new PASS3 is reserved for materially new systemic or architectural evidence.

Use one v1.3 integration branch, suggested name feat/agentic-sdlc-v1.3, opened from a verified current main HEAD after authorization. One draft PR for cohesive candidate integration. Do not create separate permanent branches per framework/test/error, clone or worktree unnecessarily, alter v1.1/v1.2 release tags, or merge unverified external code.

I3 is the continuous execution owner: architecture within approved interfaces, code, unit/integration tests, actual host execution, feature repair, in-envelope refactors/migrations, worker delegation, fault injection, safe rollback, integration and reviewer returns. I4 can provide scoped code or expert advice; results are not authoritative until actually received/consumed and independently validated. QA owns benchmark fixtures, immutable hidden oracle, scorekeeping and independent readback. Host package owner validates compatibility where native permissions/thread calls are involved. CLIENT approves meaningful product choices and high-consequence external effects, not each syntax error.

## 3. Dependency route

M0 Framework capability inventory and independent baseline --> M1 Trustworthy internal code tests + M2 Verified optional host integration --> M3 Complete ArquitecturaRepo lifecycle vertical --> M4 Installation/platform and recovery variability --> M5 Evidence-gated mechanism improvements --> M6 Exact framework release qualification. M7, explicitly reserved by CLIENT for subsequent optional package/plugin absorption and privacy-safe distribution, starts only after M0–M6 acceptance and separate scope authorization.

M1 and M2 can proceed concurrently under a documented noninterference split and exact source integration ownership. M3 validates both the portable full lifecycle and the separate optional enabled host branch; the native-host branch requires M2 physical write/readback, never SDK imports or simulated flags. M5 depends on causal evidence from M3/M4. M6 evaluates one exact candidate tree and a declared supported capability/host matrix. No gate is replaced by another and external model task success is not silently promoted into framework acceptance.

No artificial fixed duration, agent count or percentage target: independently measure the v1.2 baseline, set thresholds proportionate to risk and test sample size, then pre-register them before accepting improvements. Report unsuccessful attempts and environmental drift.

## 4. M0 — Evidence, risk and reproducible framework baseline

Owned by I2/QA with I3 reconstruction.

Reconstruct the exact tagged v1.2, current main, registered campaign and runtime state and each advertised module: installation/adoption, profile selection, Product State, Goal/charter/Plan, actor/lease, campaign DAG and next-action, I4 handoff, review, currentness/invalidation, journal/DB/GC, CLI, optional host ports and packaging. Produce a single capability-to-owner-to-interface-to-consumer-to-falsifier matrix with observed current implementation and support category.

QA independently prepares pinned disposable fresh and existing repositories, controlled file/DB state, adversarial inputs, expected source/currentness effects and protected surfaces. A small program or HTTP service may provide realistic tool output, but its AI-generated feature quality is NOT a milestone prerequisite. Baselines distinguish observed real host behavior, deterministic simulated lifecycle tests, unavailable host capability and model-dependent task outcomes. No benchmark depends on maintainer private repositories.

M0 PASS: independently runnable harness/fixtures and oracles for ArquitecturaRepo's own claims, verifiable v1.2/main/source distinction, documented first-use flow and exact capability/host support matrix. M0 FAIL: inaccessible/private-only fixtures, unverifiable source, circular evaluator ownership, or a test plan that confuses model coding competence with framework correctness.

## 5. M1 — Family A: systematic Python and contract tests

Owner I3 component engineering, with independent QA of oracles. Preserve working v1.2 tests.

Refactor test architecture only as needed to expose an efficient fast local command, a complete CI code suite and separate bounded stress/mutation/nightly evaluation. No extra Python framework is forced into the adopter's application. Use parametrized small/empty/one/two/many/malformed/duplicate/stale cases, independent expected outputs, exact physical file/DB readback and focused FAIL-before-PASS regressions. Treat test-to-production code duplication as a smell. Cover all public profiles, install/adoption/upgrade/remove boundaries and OS differences that are advertised.

High-risk sequences need model/state-machine tests where it makes sense: Goal/Plan revision and protected core, actor lease/authority, campaign status/DAG, I4 consultation currentness, journal recovery, external effect receipt and file GC before/after durable DELETE_INTENT and physical unlink, SQLite WAL. Use Hypothesis stateful as a candidate and shrink counterexamples to committed deterministic regression. Use selected mutation testing to prove tests detect removed checks or wrong path/revision; explain surviving equivalents. Mutmut requires fork support/WSL on Windows, so keep that analysis in optional maintainer QA tooling. Never optimize for superficially high line coverage or test count.

Systematic fault injection: process kill before/after state write, fsync, rename, unlink, effect send, response-loss and reviewer freeze; ENOSPC, EACCES, symlink/multilink, malicious archive paths, stale Git, corrupt source, WAL drift, two writers and clock/lease anomalies. Verify real state in a new process. Permanent evidence is hashed and de-duplicated, ephemeral test outputs cleaned after review.

M1 PASS: seeded dangerous mutations are detected, observed on-disk state after injected interruption satisfies written invariants, existing supported v1.2 behaviors still work, each known bug has a regression, QA can reproduce on a clean checkout. M1 FAIL: only exit-code assertions, fake self-approval, broken currentness accepted, tests changed to accommodate a wrong result, unprotected filesystem mutations.

## 6. M2 — Verified optional agent-host and executable command seam

Owner I3 + host owner/security reviewer. This is the most important missing mechanism before claiming real autonomous SDLC.

Select the smallest actually supported host path after environment inspection. A candidate is the documented version-pinned Codex Python SDK, which exposes start/resume of threads and workspace/read-only sandbox settings. Run real conformance and permission tests; no undocumented private Codex SQLite edits, invented native Goal methods or assumption that the read-only Daily Control 2.1 preflight is an agent runner. An alternative versioned supported CLI/other vendor may be substituted if it satisfies real permissions and readback.

Define one HostPort and one ToolPort interface. HostCapabilities includes observed SDK/host versions, platform, authentication, operations, sandbox/write enforcement, thread continuity, timeouts and truthful support classification. EngineeringCommand binds actor, campaign/Goal, exact source SHA/state revision/lease, allowed write surfaces, expected effect/approval, budget, evidence and idempotency. AgentTurnReceipt records actual thread+turn, source before/after, observed commands, log reference, actual effect/diff and error status. Implement the first consumer concurrently with these contracts; do not create unused schema monuments.

Real smoke sequence: user approves disposable workspace; supported host starts an actual agent thread; agent makes an authorized code change; runner observes Git/filesystem bytes; same thread executes focused tests; after interrupt/restart the SDK resumes correctly; protected file remains intact and source/currentness is validated again. CLI/status must expose supported/unsupported and failed operations accurately. Token/cost estimates must distinguish observable provider facts from unknown data.

M2 PASS: genuine host interaction and independently observed source mutation/test execution/restart on a supported environment, no write-envelope bypass, safe permission model and clean rollback. M2 FAIL: mock or JSON flags treated as a native host, uncontrolled model shell/effect permissions, duplicate effect on resume, blanket full-access needed for trivial operations.

## 7. M3 — Complete ArquitecturaRepo lifecycle vertical

Owner I3; independent QA controls framework-level acceptance and immutable expectations.

Exercise ONE end-to-end installed ArquitecturaRepo workflow on a disposable repository: setup and project discovery -> CLIENT intent and technical baseline -> authority and capability-level charter -> persistent I3 tactical Plan and a chosen authorized action -> physical actor/currentness/lease check -> command delivery to a deterministic test adapter AND, separately where advertised, verified native HostPort -> truthful execution/effect receipt and state readback -> injected tool/reviewer failure -> same-campaign diagnosis and in-envelope correction -> independent source-bound review -> post-review invalidation where relevant -> interruption/resume -> current terminal or honest HOLD/report. Observe exact state, events, files, Git identity, permissions and recovery, not agent-written summaries.

A model may attempt an actual tiny code modification to exercise the native seam, but successful application implementation, hidden app acceptance and app quality are NOT required to prove framework lifecycle semantics. A host invocation is not required for a portable-only configuration that explicitly does not advertise agent execution. For any host claim, real authorized physical host readback is mandatory.

M3 PASS: all advertised framework transitions and effects follow the contract, retries and reviewer rework stay in the same charter, protected state survives, stale/duplicate actions are rejected, receipts match observed source and execution, and the end status is truthful. M3 FAIL: fictitious host operation, unlawful effect, stale lease accepted, missing effect/review lineage, uncontrolled replay, false PASS, broken recovery, or a fixture that never exercised the promised capability. A model's inability to solve a programming challenge is separately measured, not automatically a framework FAIL.

## 8. M4 — Portability, variability and longitudinal recovery

Broaden the framework-level M3 lifecycle across fresh and existing/governed installations, advertised supported OS/host combinations, different codebase layouts and realistic events: late CLIENT requirement, same-campaign bug return, missing capability, permitted parallel work under HOLD, DB WAL/migration, overlapping writers, lost receipts, source changes after review freeze, untrusted tool text, permission denial and resource exhaustion. Distinct programming-language repositories can detect adoption and path-assumption defects, but the model is not required to implement a feature correctly in each language.

Longitudinal trials must span independent processes/sessions with exact candidate SHA, canonical state and transaction readback. Measure lost authority/effects, false acceptance, needless client relays, planner churn, recovery, installation friction, disk resources and supported-scope honesty. Record model outcomes separately.

M4 PASS: framework behavior generalizes across the actually advertised combinations, adopts existing state without duplicate owners, avoids unapproved changes, reliably recovers and accurately reports unsupported branches. M4 FAIL: hidden dependence on private repos, unrecoverable accepted state, false host claims, replayed effects or hard-coded environmental assumptions.

## 9. M5 — Conditional admission of research-inspired patterns

I2/CLIENT strategic decisions informed by I3 experiments and independent QA. Every new framework mechanism must compete against a simpler v1.2/M3/M4 reference with matched framework task, host, permissions, version, budget and state oracle; hold model conditions comparable where relevant, but evaluate framework-controlled behavior separately from external model programming quality.

Potential candidates in priority order:
- Typed commands, source-bound scoped context and useful role interfaces, rather than strict prompt-only permissions or giant chat histories.
- One logical Goal with protected CLIENT/I2 core and CAS-bounded I3-editable conditions; only tactical scope may change.
- Actual I4 REQUESTED -> DELIVERED -> CONSUMED_BY_I3 -> INDEPENDENTLY_VALIDATED when additional expertise measurably improves user outcomes.
- Typed domain event projection and durable outbox/inbox only if real async WAIT/RESUME or I4 recovery needs it; no mandatory global bus or competing database.
- Risk-proportionate typed design/SOP artifacts for consequential schema/architecture changes, minimal docs for trivial changes.
- Tool-driven feedback and causal fixes without arbitrary retry caps, and independent hidden oracle after the self-test loop.

For each candidate pre-register source paper/framework claim versus **our inference**, comparison, expected improvement, added interfaces/state/resources, privacy/security risk, rollback and what would falsify it. Run repeated matched scenarios, report all attempts, variance, cost and real product acceptance. Outcome must be ADOPT, DEFER or REJECT; rejected complexity stays out of v1.3. If an extra agent or event bus does not produce meaningful improvement, reject it even if its architecture looks sophisticated.

M5 PASS: only causally useful mechanisms are included; SOLO remains efficient; no extra role silently takes Planner/CLIENT authority. M5 FAIL: features imported solely from AutoGen/CrewAI/MetaGPT/ChatDev branding, no empirical comparator, tests altered to justify the feature, more cost/churn without quality gain.

## 10. M6 — Industrial release gate and v1.3.0 publication

One exact committed release candidate. No averaging thousands of A tests with a failed B scenario.

GATE A: all relevant Python/component/contract/schema/source/transaction properties and regression, selected mutation quality and fault injection pass; supported Windows/Linux portability and 1.2 backward compatibility documented.
GATE B: independently installed ArquitecturaRepo, on a disposable fresh/existing repository, correctly performs the full advertised Goal/charter/Plan/actor/lease/campaign/dispatch/receipt/rework/review/currentness/resume/reporting lifecycle. For declared native-host capabilities, the actual host performs an authorized bounded operation with physical effect/readback. The model's task-solving quality and resulting app correctness are reported separately, not acceptance gates for ArquitecturaRepo.
GATE C: unauthorized protected writes, secret exfiltration, unsafe GC, forged approvals, false independent review or duplicate remote side effects fail closed. Risk-reviewed exceptions are clearly unsupported, never silently accepted.
GATE D: actor/lease/Goal/currentness owner graph, durable WAL/journal/recovery, I3/I4 feedback lineage and post-review invalidation are real and independently verified for the enabled capabilities.
GATE E: ordinary adopter workflow is understandable, proportionate in CPU/RAM/disk/model cost, privacy conscious, incremental upgrade/removal safe, no compulsory proprietary controller or maintainer QA application.
GATE F: exact release tree/manifest, independent source CI, package/upgrader, support matrix and honest release notes, signed-off change authority and immutable v1.3.0 tag. Preserve historic releases; update release notes only for truthful public product capabilities.

R6 FAIL or HOLD when a mandatory advertised capability is unproven. For optional host/platform features, label unsupported or defer rather than block a generic release on unrelated private environments. Never declare true native automation from Python-only preflight.

## 11. Cadence and effective testing workflow

Per meaningful change: smallest failing repro where relevant; readable clear interfaces; focused tests and actual observable artifact; preserve old PASS behavior and check new FAIL_TO_PASS.
Per integrated capability: full portable code suite, contract/source/currentness readback, independent review, no unresolved in-charter P0/P1 behavior.
Expanded/scheduled maintainers' QA lane: property/stateful stress, mutation, concurrency/fault injection, cross-OS and medium-term host/action use. A scheduled GitHub CI lane is an ordinary job definition, not a ChatGPT background promise.
Before I2 strategic terminal: independent code reviewer and separate adversarial risk review, all true blockers consolidated back to same I3 if in charter; no planner churn.
Before release: single-source A+B evidence and independently executable benchmark oracle, privacy/license/security/capacity gate and user-visible proof of supported scope.

Evidence per capability: ID, owner, source SHA, requirement/oracle ref, A and B results, real host/build, failure/race injected, receipts, permissions, reviewer, cost/time/disk, known limitations, rollback, next action. Do not retain 10 identical large artifacts or full private chat logs.

## 12. Stop conditions / anti-gaming / reset policy

- Host not available: continue A and portable progress only; do not claim B succeeded. Select another documented host under real authorization, or narrow target support.
- Repeated same-class bugs: I3 performs full causal subsystem hardening and independent review; do not spawn Planner on each failed command. Strategic reroute only for new material charter invalidation.
- Unsafe external or filesystem effect: reconcile first; never replay after ambiguous receipt or delete replacement file just because a stale path matches.
- Oracle leak/test-only patch: invalidate B and re-establish independent fixture/oracle.
- Changed model/provider/runtime: pin cohort and attribute drift; don't misattribute to design.
- No observed product benefit: reject optional framework-pattern complexity, preserve simple synchronous route.
- Excessive disk/clone/log growth: stop, reconcile artifact ownership, clean disposable files under explicit policy.
- Unknown authority after resume: HOLD exact operation, preserve state; chat memory is not native readback.
- Requirement changes from CLIENT: update actual protected decision chain, not accept an I4 suggestion as authority.

## 13. First authorized charter and full route ownership

After CLIENT/I2 design approval, the first connected charter can cover M0-M3 as a capability-level framework slice, with architecture interfaces and independent A+B framework evidence. I3 may use disposable real-world repositories, select supported host interfaces, repair tests, refactor safely, and iterate until M3 has a genuine framework lifecycle terminal. Another charter is justified only for a genuinely material authority boundary, a different host permission model, or measured optional async/multiagent scope—not every internal code repair.

The engineering handoff is therefore: reconstruct exact source/campaign authority, run an independent framework fixture baseline, implement and test actual advertised lifecycle consumers and a supported optional HostPort+ToolPort with permissions and readback, then demonstrate one independently accepted full ArquitecturaRepo lifecycle in the same persistent I3 campaign. M4/M5/M6 follow framework evidence, not external app feature success or speculative extra infrastructure.

**This document is a complete engineering route, not proof of implementation or authorization of external services.** It never retags or reopens the historical 1.2 line.
