# ArquitecturaRepo v1.3 — Engineering Execution Route, Gates and Milestones

Status: COMPLETE PROPOSED ROUTE, **NOT EXECUTED**. 2026-10-14. Ownership: CLIENT owns the product; I2/Planner owns strategic capability charters, persistent I3 owns actual engineering and ordinary repairs, scoped I4 supports and independent QA validates.
This route operationalizes [the target software architecture and TPP engineering design](40_V1_3_TARGET_SOFTWARE_ARCHITECTURE_AND_TPP_ENGINEERING.md), [the independent A/B testing program](38_V1_3_PRODUCT_QUALITY_AND_END_TO_END_PLAN.md) and [the academic/framework analysis](39_V1_3_AGENT_FRAMEWORKS_AND_AGENTIC_SDLC_RESEARCH_TRANSFER.md). It is the single canonical v1.3 sequence. Academic readings are tracked in research issue #2; issue #4 indexes the plan, rather than duplicating a second mutable plan.

## 1. Product destination and invariant boundaries

An unrelated developer should be able to install the open-source starter in a new or existing repository, give a software feature request, verify constraints and status, choose an installed supported optional coding-agent host, then obtain real edited code, application build, actual tests, same-campaign defect correction, independent review, continuation after interruption and a runnable source-bound change.

The generic portable core must work without maintainer-owned products, a particular vendor, a private controller, a second global database, heavyweight agents or a paid subscription. The real agent execution path requires a compatible, expressly authorized host; absent such a host, the product must say so and offer a usable manual/portable path, never fake code execution. Full agent effectiveness is a separate product-support claim, not a condition that every general user install our QA benchmarks.

The predecessor v1.2.0 tag stays immutable. Current main includes later integration/docs and must be compared against that exact tag before implementation. A shipped version is not implicitly equal to a newer main commit. Every proposed feature must be compatible with this upgrade boundary or have an explicit safe migration and truthful breaking-change decision.

Two *independent* releases gates: A = internal Python/contract/transaction correctness, B = an agent installed in an unrelated real software project delivered independently working software. Neither substitutes for the other. A can succeed with fake HostPort adapters for deterministic testing; B cannot be accepted on fake execution.

## 2. Ownership, controls and one integration branch

Before coding, I2 performs strategic PASS1 end-to-end and PASS2 adversarial review, then issues one capability-level charter covering the earliest connected critical-path results. It must contain the actual user outcome, authority, scope, source refs, interfaces, risks, A+B testing, permissions, capacity, falsifiers and return boundary—not prescribe each implementation microtask. A new PASS3 is reserved for materially new systemic or architectural evidence.

Use one v1.3 integration branch, suggested name feat/agentic-sdlc-v1.3, opened from a verified current main HEAD after authorization. One draft PR for cohesive candidate integration. Do not create separate permanent branches per framework/test/error, clone or worktree unnecessarily, alter v1.1/v1.2 release tags, or merge unverified external code.

I3 is the continuous execution owner: architecture within approved interfaces, code, unit/integration tests, actual host execution, feature repair, in-envelope refactors/migrations, worker delegation, fault injection, safe rollback, integration and reviewer returns. I4 can provide scoped code or expert advice; results are not authoritative until actually received/consumed and independently validated. QA owns benchmark fixtures, immutable hidden oracle, scorekeeping and independent readback. Host package owner validates compatibility where native permissions/thread calls are involved. CLIENT approves meaningful product choices and high-consequence external effects, not each syntax error.

## 3. Dependency route

M0 Source/benchmark truth --> M1 Trustworthy code tests + M2 True agent-host operation --> M3 One full real software feature --> M4 Different apps and longitudinal recovery --> M5 Evidence-gated research patterns --> M6 Exact release qualification.

M1 and M2 can proceed concurrently only under a documented noninterference split and exact source integration ownership. M3 requires M2 real host write/readback, not just an SDK import or package preflight. M5 depends on the failure evidence collected in M3/M4. M6 evaluates one exact candidate code tree and one declared supported host envelope. A partial gate cannot silently satisfy an unrelated release promise.

No artificial fixed duration, agent count or percentage target: independently measure the v1.2 baseline, set thresholds proportionate to risk and test sample size, then pre-register them before accepting improvements. Report unsuccessful attempts and environmental drift.

## 4. M0 — Evidence, risk and reproducible external baseline

Owned by I2/QA with I3 reconstruction.

Reconstruct exact tagged v1.2 and current main: tools/campaignctl.py, state_tx.py, goal_guard.py, goal_plan.py, artifact_ledger.py, scaffold_project.py, apply_adoption.py, existing native-adapter preflight, schemas, migrations, generated profile packages and all current selftests. Produce a single capability/owner/authority/evidence matrix with columns: capability, actual source owner, writable state, current implementation, advertised support, missing mechanism, risk severity, positive/negative A tests, external B behavior, dependent host, recovery, rollback, cost and adoption friction.

Create external QA applications, pinned and runnable without an agent: disposable Python HTTP CRUD with persistence and restart, preexisting Spring Boot+PostgreSQL API with migration/transaction constraints, and a preexisting JS/TS web+API app with independent build and end-user behavior. Include one clean installation, one existing/governed installation, one late change and one seeded bug. These ecosystems are benchmark fixtures, not dependencies of the open-source installer.

For each real task QA pre-commits initial Git SHA, human requirements, external acceptance oracle (FAIL_TO_PASS plus PASS_TO_PASS), security/privacy scope, allowed commands and budget. The agent cannot read/modify withheld tests. Record supported host/model/build/platform versions and exact baseline; if tagged v1.2 cannot run a native agent, compare it honestly with its portable/manual or a matched single-agent reference rather than invent native baseline performance.

M0 PASS: independently runnable external apps and oracles; current tag/main/source distinction; documented actual user first-run flow and support matrix; each critical capability traced to owner and QA. M0 FAIL: hidden oracle writable by builder; source based on remembered chat rather than physical Git; fixture cannot start independently.

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

## 7. M3 — First complete software-engineering vertical slice

Owner I3; independent QA controls hidden app-level acceptance.

Execute ONE Python CRUD/API task end-to-end from a pinned external repo: installation -> CLIENT requirements -> proportionate baseline/plan -> currentness and authenticated host -> actual code edits -> real interpreter/app startup and HTTP/DB tests -> bounded error feedback -> same-I3 fix -> independent source-bound reviewer -> hidden acceptance and PASS_TO_PASS regression -> restart/recovery -> exact PR/commit/diff -> user-readable result.

Require one deliberate failing test or build error to exercise causal debugging; I3 must not turn this into microcharters or a fixed three-retry ritual. Require at least one interruption after a mutable state change; verify that no stale or duplicate authority/effect is replayed. Verify actual HTTP response and persistent DB content after server restart, not merely tests written by agent.

M3 PASS: externally runnable working feature passes QA's prior hidden oracle, preserves old functions and user files, corrected failure stays within the same campaign, review corresponds to final source, state and artifacts recover, cost/privacy/permissions are recorded. M3 FAIL: app never starts, hidden tests edited by worker, fake HTTP mock as product output, reviewer validates stale SHA, success based on an agent-written summary.

This is the first true vertical v1.3 capability unlock. Do not introduce a central event bus or more organizational roles before it works.

## 8. M4 — Industrial variability and longitudinal recovery

Broaden only from a successful M3 to the other independent app contexts: Java/Spring+PostgreSQL with actual migration/compatibility, TS frontend+API with cross-file behavior and build, and a preexisting governed repository where an installation must not create a duplicate Product State/owner. Exercise meaningful variations: late user requirement, different supported host mode, crash after code edit, DB WAL/migration, two overlapping writers, lost receipt, source changing after reviewer freeze, bad permission, untrusted model/tool text and exhausted resources. Use a risk-based subset per task and publish an accurate support matrix; never silently advertise every configuration.

Longitudinal run must extend through distinct processes/sessions, preserving exact candidate SHA and transaction readback. Compare setup effort, accepted features, escaped defects, repeated causal failure class, latency/cost/tokens when measurable, user interventions, review churn, accidental worktrees, disk cost and cleanup, rollback and recoverability. Preserve failure trajectories, not curated screenshots.

M4 PASS: meaningful generality across declared supported app/host/OS combinations, independent working software, no unapproved mutations, repeatable crash/upgrade/recovery and observable supported-scope limits. M4 FAIL: only one toy app, recompiled mocks, hidden benchmark contamination or use of maintainer private projects as user prerequisites.

## 9. M5 — Conditional admission of research-inspired patterns

I2/CLIENT strategic decisions informed by I3 experiments and independent QA. Every new mechanism must compete against a simpler v1.2/M3/M4 reference with matched task, model version, host, budget, permissions, sample distribution and oracle.

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
GATE B: on a declared actually supported host, unrelated developer repo and independent oracle, real feature request -> agent-coded diff -> executable app -> test/fix -> review -> resume -> acceptance, with all failures reported and reproducible source identity.
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

After CLIENT/I2 design approval, the first connected charter can cover M0-M3 as a true capability-level slice, with architecture interfaces and independent A+B release candidate. I3 is given latitude to use real projects, select supported host interfaces, repair tests, refactor safely, and iterate until M3 has a real terminal. Another charter is justified only for a genuinely material authority boundary, a different host permission model, or measured optional async/multiagent scope—not every internal code repair.

The first real engineering handoff is therefore: reconstruct v1.2/main exact source, run independent QA fixture baseline, implement one supported HostPort+ToolPort with permissions and real readback, and deliver one independently accepted CRUD feature in the same persistent I3 campaign. M4/M5/M6 follow evidence, not speculative additional infrastructure.

**This document is a complete engineering route, not proof of implementation or authorization of external services.** It never retags or reopens the historical 1.2 line.
