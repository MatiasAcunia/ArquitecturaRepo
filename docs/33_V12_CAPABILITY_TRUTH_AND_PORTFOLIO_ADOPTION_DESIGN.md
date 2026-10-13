# v1.2 capability-truth closure and post-release integration architecture

Date: 2026-10-13. Status: **CLIENT REQUIREMENTS RECONCILIATION PROPOSAL / NOT IMPLEMENTATION AUTHORITY**.

Source: new CLIENT direction to prioritize a smaller, genuinely working Agentic SDLC; enforce useful Git, file lifecycle, Goal/Plan/I4, human boundaries, iterative engineering and an existing external Codex Daily Control 2.0.2 package, then adopt accepted changes into OWNER plus four portfolio workstreams. This document is *one strategic planning input*, not a second Product State, Planner charter, policy kernel or execution queue. The canonical v1.2 release gate owner stays \`state/V1_2_ACCEPTANCE_CRITERIA.json\`; the existing \`docs/30_V1_2_STABILIZATION_MASTER_PLAN.md\` owns release sequencing.

**Physical-truth boundary:** a green exact-HEAD CI run proves only the covered source on that HEAD. A prior Windows install log, a local pilot report, a GPT statement, a YAML declaration, a synthetic provider mock, or an Agentic SDLC config cannot prove the current host, original project databases, actual scheduler, human judgment or full release. A private L3 consolidated transfer report was reported but its full bytes/diff have not been read here; hold exact-diff reconciliation. No protected adopter repo or Goal is authorized for modification by this proposal.

## A. Enumerated CLIENT requirements, existing assets and disposition

Three meanings must never be conflated: \`EXISTS_AS_POLICY\`, \`HAS_LOCAL_CODE_AND_TESTS\`, and \`PHYSICALLY_CONNECTED_AND_ACCEPTED\`. A feature advertised to an adopter needs a versioned support label and an actual falsifier that was passed on the supported host. \`UNVERIFIED\` and \`UNSUPPORTED\` are valid, explicit outputs.

| # | Requirement / concern | Existing starter or upstream mechanism (not sufficient proof) | Minimum new work / disposition |
|---|---|---|---|
| R01 | Small, stable, truthful feature set; no invented autonomy | v1.1 release gates, v1.2 criteria, exact-head CI, candidate verifier | Mandatory v1.2: inventory each publicly advertised behavior as SUPPORTED/EXPERIMENTAL/CONFIG_ONLY/UNSUPPORTED with exact evidence; remove/prominently qualify unproven claims |
| R02 | Test capabilities, modes and real first-use behavior | six profile fixtures, Windows hosted smoke, longitudinal CRUD tests | Mandatory release: negative and real-host gates; coverage by risk/pairs rather than pretending the entire combinatorial space was executed |
| R03 | One local canonical Git checkout per project | \`repo_delta.py\`, OWNER workspace hygiene and \`workspace_gc.py\` | Mandatory process: checkout-owner inventory, reuse, no redundant clones, read-only detection; hard enforcement only within actual controlled execution transport |
| R04 | Remote Git currentness without repeated pointless pulls | \`repo_delta.py\` fetch-one-ref/delta, commit guard | Define remote-HEAD freshness policy and semantic fast-forward conditions; \`fetch\` is not \`pull\`; never automatically merge/rebase a dirty protected checkout |
| R05 | Save and classify files created/changed by L3 | existing state journal, manifests, artifact lineage, workspaces | Optional per-project artifact lifecycle manifest with explicit source/evidence/derived/secret/external/temporary classes, canonical owner, lineage, retention, risk; no log spam per ephemeral file |
| R06 | Selective cleanup and disciplined .gitignore | GC, storage policies, disposable sandbox paths | Mandatory safety; sample-only cleanup cannot delete canonical DB/evidence, unowned files, dirty checkout or attached worktrees; show dry-run and source evidence before destructive GC |
| R07 | Persist state correctly (Git, structured files or DB) | Product State, bootstrap, \`state_tx.py\`, existing reference SQLite tests | Reuse current state owner; optional SQLite index only when scale/concurrency warrants. For canonical SQLite, consistent snapshot currentness including WAL is mandatory; no global second database |
| R08 | Fewer meaningless commits and branches | \`commit_guard.py\`, \`branch_guard.py\`, \`REPOSITORY_EFFICIENCY_AND_WORKSPACE_HYGIENE.md\` | Hard only through integrated Git-write transport; source-change/review gates, causal boundary and branch isolation proof; no "commit once per task" |
| R09 | Short useful Goal and editable tactical Plan | \`goal_guard.py\`, \`goal_plan.py\`, \`campaignctl.py\` | Distinguish immutable desired outcome/authority from evolving Plan; enforce before material host actions with genuine native binding, not a voluntary CLI command |
| R10 | I4/L4 delegation and YAML | I4 team topology, schemas, bounded cognitive provider | YAML may be a declarative task *input* once parsing, provenance and host delivery are tested; immutable authorization continues in existing current authority/Goal records. No separate YAML source of truth or new role |
| R11 | Human boundary H0–H4 | human/CLIENT gates and roles exist; an upstream interaction protocol explicitly warns not to invent H2/H3/H4 labels | HOLD on taxonomy mapping: use existing authoritative code meanings only; meanwhile document factual human action, actor, artifact and approval. No fabricated numeric level |
| R12 | Product-appropriate deep analysis, design and engineering | Planner Kernel, capability charters, Execution Team OS, baseline | Show actual design choices and changed code/artifacts/tests; baseline and review evidence; no plan-as-output theater |
| R13 | Small vs large bootstrap / theory loading | reconstruction/currentness + OWNER summary/domain layers | Proportional, cached and source-bound: full material theory once per fresh context; inspect changed hashes/sections later; never reread everything each turn or trust stale context |
| R14 | Setup of CLIENT/I2/I3/Goals with correct identity | scopes, owner registry, existing-role kernels and runtime | Adapter must map existing owners before installing; one CURRENT owner per concern and single I3 campaign. Existing project attachment currently read-only preflight only |
| R15 | Format/policy/rule classes and precedence | \`AGENTS.md\`, charter, CLIENT rules, OWNER kernels | Provide a rule applicability matrix (global stable, product standing, transient current, charter, runtime, user/human) and reject conflicting or superseded rules; do not duplicate policy text |
| R16 | Recurring agent errors and coherent repair | anti-loop policy, I3 in-charter rework, independent reviewer | Classify hallucination, false PASS, loops, stale role, duplicate effects, path drift, provider failures, reviewer mismatch, permission and cost; 2+ same-class returns trigger subsystem hardening not new microcampaign |
| R17 | Iterative/incremental production-quality development | runtime DAG, unit/integration, candidate review | One narrow vertical capability -> physical test -> independent review -> rework -> accepted handoff; measure working results and loss of manual CLIENT overhead, not test/commit count |
| R18 | Codex Daily Control 2.0.2 fully integrated where real | external Windows 2.0.2 candidate/readme/install evidence; starter references only | Explicit separately installable, version-bound Windows host adapter; do not vendor package, infer native API, read secret data or mutate native SQLite for convenience |
| R19 | Real synchronous/async/hybrid, solo/team and non-code modes | \`project_setup.py\` and preferences are declarative | Sync/solo bounded path can be core; async/team/provider needs physically verified scheduler/leases/capacity/consent. Unsupported combos HOLD and are not advertised as operational |
| R20 | Tool/model/plugin/framework/OS selection | discovery UI/catalog, technical baseline schema, optional Gemini I4 | Choices remain recommendations unless actual tool installed and validated; OpenAI suitable defaults not provider lock-in; no implicit paid models or plugin installations |
| R21 | Monthly small, useful, transparent opt-out diagnostics | local allowlist + workflow; outbound transport without approved central collector | Audit effective local notice, data freshness, disable persistence after upgrade, and no private fields/identifiers; no central-delivery claim until real receiver receipt |
| R22 | Four established workstreams plus global OWNER rollout | OWNER owns role/process rules; each workstream owns product/DB and human gates | **After** stable v1.2: one portfolio integration program with per-workstream compatibility map and independent gate. No blind scaffold and no blanket rewriting of four repos |

This is a **requirements inventory**, not permission to implement all 22 as v1.2 product features.

## B. Capability budget: what 1.2 should and should not promise

### B1. Stable v1.2 core — mandatory if advertised

1. Safe initialization and idempotent refusal on existing controls; atomic control staging and rollback; byte-preserving safe install on supported OS.
2. Correct canonical currentness, exact authority, Product State and theory integrity; immutable Goal vs tactical Plan; no forged release PASS. Local structural checking is not native host permission.
3. Existing-project **safe adoption path** with no second Product State/Planner/Controller; before acceptance, a real attachment adapter and transfer audit must pass, not merely \`READ_ONLY_REFERENCES_MATCH_NOT_ATTACHED\`.
4. One well-defined, controlled Git checkout and workspace hygiene route; candidate commits/recovery/cleanup do not destroy user data. Existing policy-only checks must be truthfully scoped if the host write interception does not exist.
5. Consistent SQLite readback when SQLite is a real canonical store (including WAL), and lossless/reversible upgrade when such upgrade is claimed.
6. Code-level validation, Windows hosted smoke, native approved test where claimed, robust docs, easy opt-out and one complete end-to-end longitudinal project.

### B2. Optional integrations requiring separate physical proof

- Native Codex Desktop / Codex Daily Control 2.0.2 Goal lifecycle and quota-aware Resume;
- independently scheduled async/hybrid Goals and TEAM identity/fenced concurrency;
- automatic I4 consultation, Gemini or other model integration and observed consumption by continuing I3;
- five OWNER portfolio Tasks and recovery;
- real remote telemetry collector with authenticated identity, disable persistence and receipt;
- macOS/native non-Windows shell adapters and cloud providers;
- perceptual/creative production judgment, human approval, paid actions and public publication.

An option may be distributed as \`CONFIG_ONLY\` or \`EXPERIMENTAL\` only if documentation, installer behavior and gate register say so. If the CLIENT requires one of these as a *stable* included feature, full 1.2.0 stays HOLD until its physical gate passes. Never silently reinterpret an earlier required gate.

### B3. Explicitly not promised

- A new universal SQLite DB for every tiny project.
- Universal automatic interruption of arbitrary IDE/tools, native Codex/private SQLite patching or a guaranteed SDK for undocumented Desktop operations.
- Automatic LLM/agent creation from a YAML file or a setting labeled ASYNCHRONOUS.
- A guaranteed single clone/pull across every external process on a user's PC. The controlled transport can enforce one canonical checkout within its ownership; unrelated shell commands require independent OS-level restrictions.
- Exactly-once *external* effects without provider-side idempotency/readback.
- Complete reliability across every stack, provider, OS or all cross-product combinations.
- Fully autonomous understanding/acceptance of CLIENT creative, legal, rights or human-perception decisions.

## C. Technical design — minimal interfaces, existing owners first

### C1. Repository / Git boundary

Canonical per project: \`repo_identity\`, \`repo_root\`, \`remote_url\`, \`tracking_ref\`, \`exact_local_HEAD\`, \`observed_remote_HEAD\`, \`last_checked_at\`, \`working_tree_state\`, \`current_campaign\`, \`canonical_owner\`, \`temporary_worktrees[]\`. The live Git repository remains source of truth for its objects, not a duplicated registry's copy. The structured record is a *reconstructible snapshot* plus invalidation hints.

Controlled operation policy:
- \`OBSERVE\`: verify physical path and repository identity, current branch, dirty/untracked files, existing worktrees and conflicts.
- \`REMOTE_CHECK\`: use the existing scoped \`repo_delta.py\` route; fetch exact relevant ref only when currentness is required or local observations are stale, not on every turn. Fetch is not a worktree mutation.
- \`APPLY\`: updates are allowed only for the designated writer/campaign with explicit expected HEAD and clean/compatible worktree. No blind pull/merge/reset, no unrelated branch movement.
- \`ISOLATE\`: reuse one canonical checkout; create a Git-aware temporary worktree only for actual interference or independent release review. Registered owner, lease/TTL and cleanup trigger mandatory.
- \`CLOSE\`: stage only meaningful exact-source changes, review, commit with authorized boundary class, test/CI exact candidate; cleanup only non-evidence disposable worktrees/caches.

**Never turn "avoid repeatedly pulling" into "do not fetch on changed remote":** stale Git is a correctness failure too. Hard enforcement belongs in integrated operations; advisory guards remain described as advisory.

### C2. Artifact/file lifecycle and optional metadata store

Define one \`artifact_lifecycle\` metadata interface, not an extra Product State:
- \`SOURCE_VERSIONED\`: application source/config/policies and accepted small current surfaces, tracked by Git where appropriate.
- \`CANONICAL_STATE\`: authoritative Product/DB state; exact currentness/lineage and backup ownership. May intentionally live outside Git.
- \`IMMUTABLE_EVIDENCE\`: bounded receipts, source digests, tests/review and accepted artifacts. Never overwritten by "latest" logs.
- \`DERIVED_REBUILDABLE\`: render intermediates, build outputs, downloaded disposable fixtures, caches and samples. Prefer ignored scratch/ephemeral roots with explicit cleanup authority.
- \`TEMP_TRANSACTION\`: staging/journaled transaction scratch, deletable only after no active operation and durable readback.
- \`SENSITIVE_LOCAL\`: credentials, private user data, proprietary media and local host state; never auto-commit, auto-feedback or upload.
- \`EXTERNAL_CANONICAL\`: immutable object store, cloud/GCS/media or remote DB generations; persist locator+version/hash/right owner, not a false local stand-in.

An item becomes cleanable only if its record says \`DERIVED_REBUILDABLE\` or legal \`TEMP_TRANSACTION\`, its exact owner and active lease allow it, it is ignored/untracked or otherwise proven noncanonical, not symlinked, outside protected repo/media/DB roots and not an external authority. A dry-run should state why an item is eligible. Unknown/missing class = HOLD, not delete.

\`.gitignore\` generation must follow these classes and each environment. Ignoring an asset does **not** make it safe to delete; tracking a DB does **not** prove a consistent WAL snapshot. Validate after writes that unexpected untracked temporary files/large binaries/private paths are either classified or blocked from commit. Capture **material** creation/modification/review/promotion as journal events, not every intermediate filesystem operation.

Persistence choice: for SMALL, retain existing tracked JSON/Markdown, Git and \`state_tx.py\`. For STATEFUL/ARTIFACT_HEAVY, optional indexed SQLite store only when necessary for scale/query/concurrency and with schema migrations, WAL-consistent snapshots and independent existing-only recovery. One concern = one canonical owner; indexes are projections and must never replace original DB truth.

### C3. Goal, Plan and I4 task boundary

Goal is short and immutable for its campaign: objective, exact owner, charter ref/hash, allowed write envelope, budget/cost/rights, stopping conditions, independent acceptance gates, forbidden effects. It **does not** include the entire technical solution or 100-line microtask plans.

Tactical Plan is I3-owned, short-horizon, versioned and amendable: current hypotheses, nearest dependent work, blockers, risk, evidence, expected test, next legal action and replan reason. Prefer a few active steps plus expandable DAG, not a universal rigid item count. Replanning is due at new material evidence, changed upstream authority, repeated systemic defect or a proved active-work interval; a mere turn boundary is not a new strategic PASS. No "plan forever" instead of engineering.

I4/L4 briefs may be YAML **only as a typed serialization** validated into the existing delegation/authority model. Proposed bounded fields:
\`schema_version, parent_campaign_id, parent_i3_actor, task_id, task_kind, allowed_read_refs_with_hash, allowed_write_surfaces, quota_time_cost, forbidden_effects, output_schema, independent_review_requirement, expires_at, evidence_receipt_ref\`.
No arbitrary shell, executable tool names, user identity spoofing, raw credentials or extra delegation without separate authorization. An I4 reviewing exact candidate must be technically independent and read-only; an implementer may write only within the handed-off isolated envelope. The YAML itself never acquires runtime execution rights. Use current JSON/contracts as the canonical authority; no second mutable \`GOAL.yaml\` or \`OWNER.yaml\` truth.

The actual host integration must call a pre-dispatch verifier (identity, lease, currentness, canonical store, Plan, privacy/quota) and a post-execution verifier (artifacts, causal classification, receipt, state transaction, review due). If native hooks are unavailable, **advertise manual/on-demand diagnostics only**, not enforced autonomous behavior.

### C4. Bootstrap and rule precedence

Small-project startup: detect repository identity -> verify exact source/currentness + relevant CLIENT baseline -> choose one profile/mode -> verify human restrictions -> begin one capability. Do not load a portfolio-wide encyclopedia to edit a tiny CRUD.

Complex-project startup: common OWNER kernel once in genuinely new context -> current product summary -> active domain theory -> material cross-domain dependencies -> exact charter/runtime/DB/artifacts -> relevant historical supersession. Subsequent turns are digest/delta-driven; changed identity/authority triggers re-anchor, not blind trust. On changed scope, rebuild only affected domain and dependencies.

Rule categories and precedence must remain distinguishable:
1. CLIENT/external human consent and applicable safety/privacy/rights;
2. global stable OWNER organizational role and rule ownership;
3. product-specific standing policy/CLIENT requirements and current status;
4. authorized capability charter and I3 delegated envelope;
5. host/runtime resource/session/scheduler permission;
6. tool/serialization/format convention.

No lower-level YAML, AGENTS supplement or prior chat may supersede higher current authority. Human-intervention event taxonomy must use actually defined upstream labels; if an H0–H4 mapping is not authoritative, record \`HUMAN_CLASS_UNMAPPED_HOLD\` and a factual description rather than invent meanings.

### C5. Recurring failure and real product-quality loop

Each material failure gets one primary causal owner:
\`SOURCE_DEFECT, STARTER_ADAPTER, HOST_RUNTIME, CONFIGURATION, AUTHORITY_CURRENTNESS, PROVIDER_QUOTA, DATA_DB_WAL, CONCURRENCY, ARTIFACT_LINEAGE, AGENT_BEHAVIOR, SECURITY_PRIVACY, HUMAN_PRODUCT_GATE, EXTERNAL_EVIDENCE_MISSING\`.
Stable signature + exact reproducer + counterexample + changed surfaces + fix + residual risk. A model explanation is not a reproduced cause.

Actual loop: baseline -> smallest useful vertical increment -> test the normal path and bad inputs -> inject interruption/incorrect authority -> I3 fix/retest within charter -> independent review on exact candidate -> only then promotion. After two or more same-class returns, stop patch-by-patch and harden the owner subsystem. Planner/I1 intervene for new systemic evidence or invalidated charter, not another typo. Measure useful product behavior, safe recovery and decreased user intervention, not commits/documents/tokens.

### C6. External Codex Daily Control 2.0.2 bridge

Treat the existing Windows package as a **separate host-owned product**, not as code to copy wholesale into a cross-platform Python starter. Legacy/current README and a previous Windows install log report: four project-slot Goal bindings, local read-only Codex SQLite/history, a native CLI/app-server bridge, strict quota-aware 300-minute recovery, foreground calibration, nightly readback/daypacks, and guarded cleanup. These are *reported historical capabilities*, not a live contract for the current installed bytes. A later L3 preflight did not locate/verify the installation. **Resolve this discrepancy physically, not by picking the more favorable report.**

Adapter handshake requirements:
1. \`probe\`: physical install root/build hash, OS/PowerShell, native CLI version/capabilities, installed package provenance, configured slot identity and actual Goal/thread availability, read-only; no token disclosure.
2. \`observe\`: exact Goal/actor/campaign/plan, native lifecycle, current project repository identity/remote, source/tree currentness and Windows locking/permission constraints.
3. \`request\`: typed operation intent to the existing controller: inspect, refresh allowed quota, resume **only** safely recoverable usage-limited Goal, pause/close with independently required authorization, or archive. Never request normal paid new turns in a diagnostic.
4. \`receipt\`: read back the same native Goal+thread, status/actual continuation, reason for HOLD and authoritative physical source; wrong account/thread, user pause, completed, blocked or budget-limited never auto-resumes.
5. \`recovery\`: durable, bounded retry with idempotency and explicit active-writer/ambiguous-effect HOLD. No direct mutation of Codex SQLite, no scraping auth tokens into logs, no reliance on unvalidated runtime internals or GUI click as the primary resume path.
6. \`close/daypack\`: output belongs to controller/local authorized archive; packaging and remote-drive availability are independently verified before any allowed deletion. Private raw chat and user paths must never be part of public starter telemetry.

Verify against actual installed Codex build and official protocol/schema; never assume a method merely because a previous version used it. Distinguish local metadata in SQLite from the native app-server read/write authority. A validated native Goal continuation does not prove campaign strategic acceptance; the repo's Planner/I3 retains that role. This bridge is Windows-specific until separately proven elsewhere.

### C7. Modes, model/providers and team capabilities

Use an evidence-backed capability registry with state:
\`DECLARED_ONLY / LOCAL_SIMULATION_PASSED / HOST_PHYSICAL_PASSED / INDEPENDENT_ACCEPTED / NOT_SUPPORTED\`.
Each public example and CLI path states which stage applies. A GUI/user preference does not move it forward.

Represent the independent dimensions already in \`project_setup.py\`, but use a **pairwise combinatorial test matrix** + high-risk intersections, not an implausible universal exhaustive test count. Include mandatory negative combinations: ASYNC without scheduler, TEAM with colliding write resource, HYBRID with unanswered human gate, AI with unsupported paid/rights export, suspended Goal with available quota, stale product DB/WAL, and unsupported OS. Each must correctly HOLD, not fake-run.

For OpenAI/Gemini/other providers: verify model access, quota/limits, data export permission, provider identity, deterministic response receipt, rate limiting, budget and independent consumption. OpenAI recommendations must be genuine provider-neutral engineering defaults. No plugin/tool auto-install or unverified paid calls.

## D. Stable support and acceptance matrix

| Boundary | Minimal falsifier | What counts as PASS | Status at proposal time |
|---|---|---|---|
| Non-destructive new install/upgrade | Inject disk failure, existing CLIENT theory and workflow, symlink/Windows alias | Byte-preserving rollback and exact installed hash | Source/CI tests present; new project host still pending |
| Git canonical checkout | Dirty HEAD, stale remote, duplicate checkout/worktree | Fail closed or safe exact delta; no overwritten user changes | Existing guards; external host enforcement unproven |
| File lifecycle / GC | Unmarked, protected artifact, active lease, symlink, dirty linked worktree | Only owned rebuildables removed; reconstructibility retained | GC exists; integrated file-class manifest not proven |
| State / SQLite/WAL | Commit WAL without changing main-file hash | Snapshot currentness rejects stale logical state, original DB unchanged | New code/Windows CI synthetic; physical original DB pending |
| Goal/Plan native boundary | Change charter during active Goal; stale I3 | Real pre-action block and durable Plan revision/rollback | Local guard only; host hook unproven |
| I4 YAML/teams | Forged task, wrong owner, stale model receipt | Denial with no effects; real exact-I3 review receipt | Planning only; no YAML runtime claim |
| Existing-governed attachment | Preexisting owner + Product State + active campaign | No shadow CURRENT, legal narrow adapter and independent transfer | Read-only ref check only; operational transfer HOLD |
| Human gates | Unmapped H label or human-perceptual acceptance | No guessed grade, explicit signer/decision boundary | Policy only |
| 2.0.2 host | Missing installed build or conflicting native Goal state | Version-bound real Resume/readback and safe rollback | Prior install log vs later unverified; HOLD |
| Feedback | Disabled report, private keys, fake/redirected collector | Report only allowed fields and proven disable; remote receipt separate | Local tests present; external collector HOLD |
| Longitudinal product | Fresh install, real code/DB, repeated sessions/review | Exact candidate artifacts, final runtime and independent review | Initial pilot reported, exact new report/diff unavailable |
| Independent release | CI on wrong SHA, simulated PASS, stale private patch | All **advertised** claims supported by exact candidate+independent gates | Release HOLD |

No single CI job can certify the host/human/provider rows above. A green release candidate remains a candidate.

## E. Risk-first implementation sequence (no fixed calendar or pointless campaigns)

**E0 — reconcile evidence and freeze scope.** Read the reported full L3 consolidated report and its local diff/manifests. Verify report hash, compare source tree with latest branch, distinguish first pilot findings from later GitHub changes; no blind cherry-pick. Fix the operational governed attachment and WAL falsifiers on one candidate; exact Linux+Windows CI. Do not publish or adopt into active projects yet.

**E1 — harden the portable core.** As a bounded I3 envelope, address only demonstrated P0/P1 defects in Git/file lifecycle, currentness, bootstrap, Goal/Plan, installed/root parity and cleanup. Introduce a lifecycle manifest only if actual artifact-loss/leak/duplicated ownership tests demonstrate the old mechanisms insufficient. Reuse \`state_tx.py\`, \`campaignctl.py\`, \`workspace_gc.py\`, \`commit_guard.py\` and \`repo_delta.py\`. No redundant always-on agent or second SQLite truth.

**E2 — native host and narrow optional adapter.** Independently inspect actual 2.0.2 files and native Codex build on approved disposable Windows Goal; verify legal methods and state transitions with readback, start/stop/rollback. If host cannot expose a stable pre-dispatch hook, mark hard enforcement \`UNSUPPORTED\` instead of promising it. Prove at least one real authorized I4 exchange only if separately permitted, or keep this adapter off by default.

**E3 — realistic coverage and release decision.** Six profile regressions; representative project-type smoke; pairwise mode/config coverage and targeted adversarial cases; two unrelated real project shapes (fresh CRUD and existing governed repo); Windows physical + hosted Linux evidence; independent exact-candidate review. Test public README/FAQ instructions literally. Make an explicit CLIENT/I2 choice: release a smaller proven core while preserving experimental integrations as opt-in, or HOLD v1.2 until the previously mandatory advanced gates actually pass. Keep \`main\` stable until the decision is legally accepted.

**E4 — post-release portfolio integration, not simultaneous rewrite.** Treat acceptance as one portfolio program with one OWNER I1 authority decision and **four distinct local adoption envelopes**. First produce, for each, a read-only compatibility inventory: existing hierarchy/theory, current campaign/lease, canonical repo/worktree, DB/WAL/media lineage, output/rights/perceptual gates, scripts, human approvals, host and rollback. Identify missing capability versus redundant one. Prefer reuse/adapter and selective enforcement to copying public starter scaffolds or duplicate policies.

Each independent workstream starts with a source-bound dry-run on a disposable checkout, negative isolation tests and restored artifact/DB controls. Integrate only the verified delta to its actual canonical owner; preserve all original campaign charters and active I3 runs unless explicit invalidation. For two tightly coupled workstreams of one final product, test upstream/downstream interface invalidation and shared-output concurrency as well as independent product-domain controls. Roll out sequentially by lowest blast radius **based on live evidence**, not by a guessed universal order.

### Post-release responsibilities

- OWNER/I1: shared policy, actor identity/scope, process/harness and cross-workstream integration. It must not own each project's Product State or introduce a second Planner.
- Domain I2: strategic compatibility analysis, material charter, human gates and acceptance in own workstream.
- Persistent I3: adapter implementation, migration/testing, in-charter rework, integration, cleanup and runtime proof.
- Optional I4: isolated independent reviewer, specialist or explicitly permitted build worker; no default canonical Git commit/merge.
- CLIENT: product meaning and protected legal/perceptual/publication decisions; not debugging or manual project coordination.

## F. Adversarial second pass / non-obvious second-order failure modes

1. **Enforcing "one pull" can create stale currentness.** Solve with scoped fetch/expected-HEAD CAS, not absolute prohibition.
2. **Automatic .gitignore can hide a canonical DB or evidence.** Classification precedes ignore policy and cleanup; ignored does not mean disposable.
3. **A global artifact DB can become a second source of truth.** Index must be a projection, or actual canonical owner must be explicitly migrated with acceptance.
4. **YAML can accidentally grant tools/authority.** Parse as inert data; bind actor/charter and validate host tool-permission boundary.
5. **Strong bootstrap can become slow ceremony.** Use summary-first and domain-selective hashes, with mandatory deep re-anchor only at material authority transitions.
6. **The nightly controller can fight user pause.** Never auto-resume manual pause, complete, blocked or budget-limited; preserved user suspension outranks automation even if quota returns.
7. **Time-based plan triggers can force churn.** Use verified active-work time and material evidence; no strategic PASS on every transcript turn.
8. **"Independent reviewer" can reuse producer evidence and reward itself.** Separate actor, source digest, negative falsifier and perceptual gate when relevant.
9. **A Git checkout is not the complete product DB.** WAL, cloud generations, rights receipts and media outside Git require existing-only readback; absence means HOLD.
10. **Two Windows builds may expose different native APIs.** Bind exact installed Codex/2.0.2 version and capabilities; avoid depending on historical inferred schemas.
11. **Rerunning tests can itself spend money or mutate product state.** Classify tests by cost/effects and default to synthetic/fixture transport before any real provider/production operation.
12. **Four independently green adapters can still interfere.** OWNER must validate cross-project shared disk/CPU, host quota, accounts, locks and common output paths.
13. **Anonymous diagnostic counts may become misleading.** Include a bounded reporting window and fixed failure enums; preserve opt-out across migrations, never transmit case payloads.
14. **Public PR history differs from present tree.** Removed private material may remain fetchable from past commits; audit before publication and use approved integration strategy without unrequested history rewrite.
15. **"Fully integrated" is not equivalent to physically supported.** Keep a capability split between source/CI, host, external effect, product/human judgment and public release authority.

## G. Terminal handoff contract

One bounded L3 engineering report for v1.2, not a new PLAN/charter per bug:
- exact local source manifest plus remote HEAD and semantic delta;
- root cause, scope and risk of each remaining P0/P1;
- original vs disposable DB/WAL/source readback, profile and OS;
- installer/artifact/Git checkout inventory, ignore/GC dry-run, no-overwrite proof;
- plan/Goal/I4 host integration proof, installed 2.0.2 bytes/version and actual native calls where permitted;
- cross-process restart/fault injection, reviewer independence and cost/privacy;
- PASS/FAIL/HOLD/NOT_APPLICABLE per canonical release gate and **supported-claim** coverage;
- before/after repository state, rollback and next legal owner.

A real release decision occurs only after all included feature gates are met and I2/CLIENT authority confirms scope. The next adoption plan must start with a fresh read-only portfolio audit, not this historical document treated as live state.
