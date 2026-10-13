# Engineering-first master route — v1.2 stabilization and post-release governed adoption

Date: 2026-10-13. Authority: CLIENT requirements interpreted as engineering scope; this is a **design and test route**, not a release charter, a second Product State or host execution authority. Existing `docs/30_V1_2_STABILIZATION_MASTER_PLAN.md` is the canonical release route; `state/V1_2_ACCEPTANCE_CRITERIA.json` is its machine-readable gate index; `docs/33_V12_CAPABILITY_TRUTH_AND_PORTFOLIO_ADOPTION_DESIGN.md` is the full 22-requirement inventory. This document supplies execution slicing, subsystem contracts and concrete acceptance tests. Do not create another management layer from it.

## 1. Clarified problem and explicit outcome

**Order (not negotiable):** strengthen the actual ENGINEERING SYSTEM -> close ArquitectureRepo v1.2 on a small truthful supported scope -> adopt relevant missing/repaired capabilities into shared portfolio governance and four preexisting governed workstreams. Existing reported longitudinal tests are engineering evidence but do not waive outstanding attachment, SQLite/WAL, host and exact-candidate gates.

The CLIENT wants a persistent I3/L3 that can meaningfully design, implement and improve software incrementally without forgetting what it touched or wasting the computer's disk. The CLI GC does not make cleanup decisions: L3 owns file classification, human/product impact, expiry, references and checkpoint reconciliation. The JSON remembers file identity and safe-delete policy across L3 restarts; the runtime checks filesystem facts before any unlink. L3 must also observe source changes through canonical Git, avoiding both redundant clones and false extra databases.

Success is not a count of documents or agents. It is one bounded demonstrably working vertical capability with reproducible tests, no missing physical data, recoverable restarts, controlled costs and no unauthorized deletion/mutation.

## 2. Role/authority topology — one owner per concern

| Boundary | Canonical responsible actor/system | Can decide | Cannot claim |
|---|---|---|---|
| Product intent and public release | CLIENT + existing authorized strategic gates | Accept product meaning, rights, public use, human experience | A model's green test cannot impersonate CLIENT acceptance |
| Shared governance | Existing I1/MASTER OWNER | Organization-wide role boundaries, portfolio risk, cross-workstream arbitration | Another Product State or second per-project Planner |
| Strategic project plan | Existing I2/Planner | Charter, capability scope and strategic invalidation | Every tactical bug, test retry or sample choice |
| Implementation and local hygiene | Persistent I3/L3 | Design/implement within charter, revise short Plan, manage artifact JSON and Git evidence, execute preauthorized GC, integrate workers | Extend own envelope, demote canonical data, new release scope |
| Specialized work | Authorized I4/L4 | Narrow read/review or delegated build evidence, bound by identity, inputs, budget and surfaces | New canonical I3, unapproved provider calls, self-approval |
| Native host + Git/DB | Installed controller and physical tools | Actually verify execution preconditions, write conflicts, filesystem and provider receipts | Infer legal ownership merely from content or policy prose |
| Runtime artifact ledger | Project-local `artifact_ledger.py` | Atomic JSON persistence, discovery, fingerprint, predelete verification | Creative/human classification decisions, global filesystem watch |
| Workspace GC | Existing `workspace_gc.py` | Proven disposable root/worktree lifecycle under protected ownership | Automatic deletion of user-controlled repositories or DB |

Human H0–H4 terms remain **UNMAPPED** until reconciled with the actual upstream vocabulary and its current policy. Record what action needs a human, who approves it and which exact artifact is accepted; never invent levels or assume no response equals approval.

## 3. Data architecture: no global DB, no loss of L3 history

### 3.1 Three independent stores with complementary ownership

1. Git repository: canonical source tree, versioned rules/charters, HEAD/currentness and approved commits. One persistent checkout per project where safe. Use relevant scoped remote fetch, never habitual `git pull` or independent clones; currentness must not be sacrificed to avoid fetch.
2. Project-local JSON artifact index: installed under the actual selected control dir's `runtime/ARTIFACT_LIFECYCLE_CURRENT.json`, not pushed by default. One entry for each known managed scratch output: owner, campaign, category, path, SHA256, file identity, retention/review/dependencies, physical status. Small bounded Git observations store HEAD and changed-source paths as an **index of Git**, not replacement version control. Retain bounded recent observations; canonical history stays Git.
3. Existing product DB/artifact authorities: catalog SQLite (+ consistent WAL snapshot), cloud objects, publishing/media/right lineage or other product state, all retained at their current canonical owner. No new central DB or fabricated offline substitute to make a test green.

### 3.2 L3 lifecycle contract (mandatory at write boundaries)

- On reentry: check Goal, current charter, repository identity, host writer/lease, current Git HEAD and the prior file-index revision; check disk headroom before heavy generation.
- Before source changes: persist the Git source observation. Before generated outputs: register a NEW scratch root, classify planned output kind and safe retention; do not claim a user-owned root.
- During a controllable producer: invoke `capture` in foreground and register actual results. If the producer fails/interruption occurs, outputs become quarantine after restart/reconcile.
- After source changes: observe current Git/status and preserve material delta without creating a per-file commit. After output creation: reconcile the exact managed roots and compare physical identities. Unwrapped native writes outside roots require a separately surfaced partial-coverage warning and Git/host audit.
- On user command `/cleangarbage`, L3 performs the `cleangarbage` agent skill: inspect state, independently reason about candidate value, do not demote protected evidence, run GC dry-run, perform only already authorized deletion, and report actual freed bytes and holds. If native Codex slash UI cannot receive that exact invocation, use explicit skill/text invocation; native registration is a separate host gate.
- At meaningful terminal: retention/dependency disposition for all large artifacts, source HEAD/diff, file ledger revision, total safe reclaimed bytes, unknown/protected inventory, disk reserve and readback. A missing file is not evidence of success.

### 3.3 Protection invariants

Deletion requires ALL of: self-owned managed root, correct I3/lease, direct physical regular file/no symlink/hardlink, exact source path confined within root, matching fingerprint, category DERIVED_REBUILDABLE or legally allowed TEMP_TRANSACTION, explicit safe flag, expired TTL, closed relevant review, no downstream reference, not Git-tracked, independently ignored, not source/SQL/DB/WAL/secret/rights/evidence, and valid intact JSON/marker/lock state. Any ambiguity is HOLD. Dry-run precedes execute; execute revalidates. Whole-root and file-level GC never independently own the same deletion surface.

A same-user malicious writer can forge unprivileged JSON; treat it as operational tracking, not cryptographically secure containment. Native race-proof enforcement requires an actual host exclusive-writer interface, which is currently not verified.

## 4. The engineering loop, not plan theater

A meaningful increment must cross the whole chain: actual CLIENT requirement -> a concrete use-case and constraints -> short design/ADR when real trade-offs exist -> one vertical implementation -> tests covering normal, boundary, invalid and interruption cases -> physical runtime behavior -> independent review -> corrective rework inside the SAME I3 charter -> acceptance/readback. Files/commits are evidence, not goals.

**Goal** stays small, stable, source-bound and authority-limited. **Plan** is a short tactical rolling horizon amended by I3 only on changed material evidence, active-work review triggers or genuine dependency change. Tool's UI Plan Mode and YAML-delivered I4 tasks are not enforcement until the native host actually consumes and validates them. YAML can carry typed delegated work, not issue its own permissions. Effective configuration must distinguish stable policy, current product state, charter/authority, execution limits and formatting preferences. Strategy reentry happens only for actual charter invalidation or new systemic evidence, never per routine bug or checkpoint.

Commit policy: changes of one coherent verified capability, not per file/fix/test; no branch for every L4. Git safety is enforced only where controlled writer transport invokes the guard, otherwise the capability is **ADVISORY**. L3 can refactor and fix implementation without escalating to I2 until it crosses actual scope.

## 5. Modes and provider capability truth

Declare one of four support grades per mode/feature: `CONFIG_ONLY`, `SYNTHETIC_TESTED`, `HOST_PROVEN`, `INDEPENDENT_ACCEPTED`. Public stable claims require the latter when host-dependent, and at minimum runnable physical proof on a supported real environment. Prefer a small supported SYNCHRONOUS/SOLO core. ASYNC, HYBRID, TEAM, autonomous I4, provider/Gemini, five master tasks and the Windows-only 2.0.2 controller remain explicitly optional/experimental or HOLD until real scheduler/recovery/identity/readback has been shown. The project may still document intended architecture honestly.

Modes are dimensions, not a promise that every combination works. Test pairwise representative mixes plus high-risk intersections; unsupported combinations produce precise HOLD, not silent downgrades. Do not auto-call paid models, upload private source, modify rights-protected artifacts or install plugins as hidden prerequisites. Prefer OpenAI models when suitable and accessible, without preventing other legitimate providers.

## 6. Five bounded engineering packages — critical path

### Package E1: persistent L3 file and Git lifecycle (highest immediate priority)

Acceptance: six profiles install same tool/index and AGENTS/skill; registered sample lifecycle survives separate processes/contexts; Unicode/Windows paths; source Git changes observed; failed capture quarantined; corruption/root takeover/symlink/hardlink/tracked file/canonical DB/active lock/uncertain review all block; executed GC idempotent and physically reclaims known bytes; no extra checkout or per-sample commit. Demonstrate on native Windows with an interrupted I3 and disk-volume before/after. **Exact native slash-menu registration is optional if not technically supported; functional skill/text fallback is mandatory.**

Failure owner: I3 in same campaign, with independent adversarial review for deletion safety. No new global database.

### Package E2: actual execution control (Git, Goal, Plan, bootstrap, I4)

Acceptance: one authoritative Goal reanchors from true repo/state/charter when context changes; stale currentness or missing canonical source blocks *host action* when a supported pre-dispatch hook exists; I3 short Plan can change tactically without rewriting immutable Goal; read-only I4 brief, bounded YAML, independent request/response/consumed evidence if host supports it; no shadow identities/owners, repeated tiny commits/branches or needless bootstrap loops. Test interrupted session, stale actor, duplicate mutator, force-conflict and guard bypass. If no native hook, label local checker advisory and do not pretend hard enforcement.

### Package E3: Windows Daily Control 2.0.2 bridge and recovery

Acceptance on the actual installed bytes: read-only probe of version/build hash, Windows/PowerShell/CLI, exact Goal/thread identity; safe case of one quota-limited Goal resumption, and negative user-paused/complete/blocked/wrong-account cases; deterministic daypack output and remote readback before allowed cleanup; no direct SQLite writes, no new supervisor agent, no automatic paid calls. Reconcile historical installation-success vs later L3 inability to locate source. The 2.0.2 product keeps its own scheduler/host boundaries. If package/bindings are unavailable, keep adapter off and mark unsupported rather than expanding promises.

### Package E4: two complementary real longitudinal product pilots

First a fresh simple CRUD: actual CLI/bootstrap, CLIENT theory, endpoint/DB, tests, plan changes, I4 optional, Git snapshots, generated samples and /cleangarbage, restart recovery and terminal; not merely mock structures. Second a disposable governed repository transfer with existing Planner/I3/DB/state/artifact lineage: no second Product State, no shadow I3, correct attachment mode, SQLite/WAL currentness, exact source/host receipts and write prohibition until authorized. The full earlier local L3 report and uncommitted source diff must be inspected and reconciled against current remote candidate first.

### Package E5: release truth/security, documentation and compatibility

Independent adversarial review on exact HEAD and source-visible native behavior; cross-platform hosted Windows/Linux smoke (macOS only if physically tested); representative profile/mode matrix; installation collision, failure injection, restart, rollback, protected data and privacy/telemetry opt-out tests. FAQ, installation/manual in advertised languages must be navigable and correct. Any optional remote diagnostics need actual collector consent/receipt before claimed delivered. No unreviewed rewrite of historic PR, no protected workstream changes, no merge/tag/publication until all advertised gates and required CLIENT authority are accepted.

## 7. Planned substantive executions — estimates, NOT quotas or release claims

The prior two reported longitudinal tests are credited as prior **tests**, not release PASS. They avoid restarting from zero but do not cover newly repaired code until repeated on the exact candidate.

Base planned budget for the NEXT meaningful proof, conditional on external setup:
- **This assistant / architecture-owner:** 4 integrated work rounds: (A) source+GC hardening and real ownership contracts, (B) Git/Goal/Plan/I4/host enforcement audit, (C) exact controller 2.0.2 interface and mode-scope reconciliation, (D) full candidate adversarial readback and release decision package. Reviews are integrated, not another doc per tiny bug. This estimate is not a claim of asynchronous work.
- **Persistent L3:** 4 substantial *scenarios*, each can contain multiple execution steps and retries IN THE SAME campaign: (L3-1) file/GC/Git interruption/cleanup in a disposable checkout; (L3-2) real CRUD longitudinal including bootstrap, design, plan, source and tests; (L3-3) preexisting governed transfer with DB/WAL and ownership; (L3-4) native Windows 2.0.2/Goal/resume/host security/compatibility. If a native host feature cannot be shown, the result is targeted HOLD/UNSUPPORTED, not a fabricated PASS.
- **Independent I4/L4:** 2 adversarial reviews of different classes: (I4-A) file deletion, identity, repo isolation, privacy and host authority; (I4-B) exact final release/transfer/restore and public claim review. Additional specialists only when they measurably reduce a specific bottleneck.
- **CLIENT/I2/I1:** 1 consolidated final scope and release gate adjudication after evidence. CLIENT product/human approvals occur only when a real protected decision is necessary.

Thus the initial bounded target is **4 engineering-owner integration rounds + 4 L3 substantive scenarios + 2 independent reviews + 1 final release adjudication**, rather than 25 ceremonial executions. These are planning slots, not an artificial ceiling. If a P0/P1 persists, consolidate falsifiers and perform causal subsystem hardening before adding another physical trial. The number changes only with actual observed failures and material evidence; no auto-schedule or deadline promise.

## 8. Risk-prioritized test matrix and stop rules

| Risk and severity | Mandatory negative/physical falsifier | Stop or proceed |
|---|---|---|
| P0 destructive cleanup | User-owned folder, dirty/clean canonical Git, DB/WAL, symlink, modified/unknown file, active writer, reviewer sample | Any wrongful unlink => STOP / reject candidate |
| P0 wrong authority | Changed charter, stale Goal, new mutator, forged I4 YAML, parallel writer, missing source | Any unauthorized effect => STOP / root-cause systemic repair |
| P0 private data/feedback | Disabled diagnostics, secret fields, path leakage, unsigned remote receiver | Unauthorized export or misleading telemetry => STOP |
| P1 Git/data integrity | Remote HEAD moved, dirty worktree, one-checkout policy, wrong branch, local L3 diff not in CI, WAL unchanged-main-file hash | Fail closed or controlled exact source-delta proof; no fake currentness |
| P1 host recovery | Quota vs explicit user pause, wrong thread, double resume, corrupted control state, daypack writer still active | Deterministic HOLD or verified valid resumption; no background false success |
| P1 actual product | CRUD data persisted through process restart, rejected bad input, schema migration, independent transfer of governed repo | Functional tests+physical DB/source readback before stable claim |
| P2 portability/usability | Windows short paths/Unicode, Linux, mixed mode unsupported, FAQ steps literally executed | Fix supported platform; explicitly mark unsupported elsewhere |

**Exit criterion:** all REQUIRED gates on final exact candidate pass independent review; P0/P1 blockers zero (not just silenced tests); source, backup and rollback verifiable; user-facing stable claims align to proved modes; native-host missing capability removed from stable claims with explicit CLIENT/I2 scope decision, not silently waived. Regressions stay within same campaign rather than creating microcampaigns.

## 9. Post-v1.2 portfolio integration (strictly afterward)

Do ONE shared read-only OWNER governance compatibility pass to ensure canonical role/policy and concurrency; then FOUR individually gated workstream transfers, adapted to live code and DB rather than mass scaffolding. Each checks current actor/campaign/charter, canonical checkout, local/remote Git, product DB and external media/evidence, host, leases, disk resources, GC classification and rollback. One existing concern retains one owner; the generic starter supplies only missing capability adapters. Source-specific asset and licensing constraints outrank generic cleanup eligibility.

A baseline integration effort is **one shared OWNER gate + four workstream-specific L3 execution envelopes + one final cross-workstream integration review**. Two coupled production pipelines must also prove upstream/downstream invalidation and artifact reuse together, not just four independent greens. Human approval and resource interference are decided from the *then-live* repositories. No currently protected repo is authorized for mutation by this plan. Do not install a blanket new controller or copy private source back into the public starter.

## 10. Roadmap updates and falsifiers stay durable

Persist only decisions, true gate results, unambiguous blockers and next executable owner in the canonical repo surfaces. Avoid giant handoff transcripts, several competing ACTIVE maps, per-file commits and speculative feature expansions. At each meaningful checkpoint, update the existing gate index and the one master plan. On a repeated issue, identify upstream causal contract and test it before reattempt. A clean unit test is not human acceptance or public-release authority.

Remaining foundational blockers at this planning revision: read full native L3 report and diff; true operational existing-repo attachment; physical WAL snapshot/DB readback; native Codex Daily Control 2.0.2 package/method handshake; actual enforcement rather than advisory Git/Goal/I4 checks; exact-host /cleangarbage availability and GC crash test; truthful supported scope and independent final review.
