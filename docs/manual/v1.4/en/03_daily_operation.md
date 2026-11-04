# 03 — Daily Operation

ArquitecturaRepo · Complete User Manual · v1.4 edition · English

> This chapter follows an already adopted project with a valid current charter. The framework's optional controller provides portable reference mechanisms; it is **not** a promise that Codex Desktop, a cloud agent, or another proprietary host will execute commands autonomously. Runtime claims must be verified on the actual host.

## In this chapter

1. Start a session without starting over
2. Turn a wish into a verifiable capability
3. What I3 does when work becomes difficult
4. Reserved authorizations and external actions
5. Read an executor report critically
6. Git and continuity
7. The five-question daily closure
8. A working day without depending on chat memory
9. An example of a bounded dispatch
10. Interpret controller states
11. Process the final report
12. Leave a recoverable session

## 1. Start a session without starting over

Before sending a new programming request, identify the actual project and worktree, current branch and source reference, unresolved local changes, canonical Product State, the active charter if one exists, and the last verified candidate. A worker returning after a host session ends should read the durable checkpoint. Restarting a similar-looking project from an old prompt is not continuity.

When the checkout is trustworthy and the baseline is known, look at the exact relevant Git delta and its dependencies. Do not automatically reclone or blindly `git pull` every time an agent resumes; those actions can disrupt unintegrated user work. Conversely, do not trust incremental sync when the source diverged or current authority is unresolved. Read-only reconciliation comes first in that case.

The CLIENT should receive a compact current-state summary without having to choose which SHA or DB snapshot is authoritative. It is an engineering responsibility to inspect the actual repository, the project instructions, dirty working tree, and relevant leases or current-state records. The Planner should recover the product objective and the authorized campaign state before routing a new feature.

A split-screen arrangement with one planning chat and one coding environment may be convenient, but it is not required. A reliable handoff consists of source-bound instructions, canonical state and evidence, not the position of application windows. If the required evidence cannot be read, mark the specific missing fact UNKNOWN and stop only the actions that depend on it.

## 2. Turn a wish into a verifiable capability

“Register dues payments, retain history, and show whether a member is in arrears” describes observable behavior. “Write the payment function” describes only a possible implementation step. The Planner should start from the former, identify existing interfaces, data rules, dependencies and risk, then authorize a bounded capability. I3 decides the internal sequence of code edits and tests within that charter.

For example, the CLIENT can say:

> I need staff to register dues payments without losing historical records and to see who has paid up. Do not add online payments yet, and keep the screen simple. I want to test the complete workflow before accepting it.

This is enough to establish intent, but not necessarily enough to begin a campaign. The Planner still needs to verify current requirements, data retention, deployment boundaries, source and ownership. The resulting dispatch names the expected capability, source inputs, limitations, affected interfaces and owners, execution gates, and a precise review-ready output. It does not ask the CLIENT to coordinate specialists or select technical retry strategies.

For long-running or batch-heavy work, the [outcome-first work order](../../../44_OUTCOME_FIRST_AGENT_EXECUTION.md) makes execution operational: source-pinned inventory, ordered available-tool route, budgets, meaningful stop conditions, concrete output and physical readback. A charter and a work order are complementary: the first defines strategic authority; the second helps I3 use that authority efficiently. Neither can authorize an external bill or private-data disclosure by implication.

## 3. What I3 does when work becomes difficult

Suppose the implementation exists but the integration test fails after a payment update. I3 preserves the observed failure and environment, traces the affected component, fixes the cause, runs the relevant tests again, integrates the candidate and obtains an appropriate independent review. The problem remains in the original campaign unless it reveals material new scope or authority.

In-scope debugging, refactoring, retries, migrations within the charter, evaluator repair, integration and crash recovery belong to I3 continuously. Repeated failure of the same class is a reason to inspect the subsystem and its test design as a whole, not to stack another local patch or return to the Planner for a new microcampaign. The Planner should examine a consolidated terminal candidate, not every tactical iteration.

An unresolvable source/currentness conflict, an absent permission for an external action, or an actual change in intended product behavior requires a different response. I3 must describe the precise blocker and causal owner instead of disguising a new permission as a retry. Read-only diagnosis can often proceed while writes remain on HOLD.

Independent review must cover the *exact* candidate offered for strategic audit. If the code, schema, or relevant artifact changes materially after a favorable review, that earlier result is not blanket approval of the new candidate. Record the new evidence and rerun checks affected by the change; do not invalidate unrelated verified work without a reason.

The optional `tools/campaignctl.py` supports reference campaign control in the portable distribution. It is not a universal autonomous coding runner. Similarly, Goal and tactical-plan helpers can manage records without proving that a particular host has activated native `/plan` tools or write-safe dispatch. [The reference runtime](../../../11_REFERENCE_RUNTIME.md) describes its supported boundaries; claims about a real agent host need separate verification.

## 4. Reserved authorizations and external actions

Different operations carry different permission and risk profiles:

| Action | Appropriate treatment |
| --- | --- |
| Inspect a repository or run local tests within granted scope. | Ordinary authorized technical investigation. |
| Edit and integrate source within an approved charter. | I3 engineering responsibility, subject to the exact worktree and ownership. |
| Install a new dependency or open a new tool. | Check provenance, necessity, permissions, and the effect on the project. |
| Deploy, publish, send messages, spend provider credit, or delete material data. | Obtain the specific reserved authorization and a proportional preflight. |
| Paste a secret, password, or private customer export into a prompt. | Do not do it; use the project's approved secret/data mechanism. |
| Encounter contradictory canonical DB, ownership, or source witnesses. | HOLD dependent writes; reconstruct and reconcile current state. |

The CLIENT decides product behavior, acceptable risk, external publication and spending boundaries. The CLIENT should not have to resolve merge conflicts, pick database index names, repair migrations, or coordinate recovery. Some product choices cannot be delegated to engineering; many technical details can and should be.

## 5. Read an executor report critically

A useful report identifies the exact source candidate and environment, the intended behavior, what changed physically, which tests and demonstrations ran, what failed and how it was corrected, what independent review examined, and which gate remains open. The number of commits, tokens, agents, checkpoints or runtime hours is not evidence of a usable feature.

If a report says “PASS,” ask *which* gate passed. A unit test may exercise a calculation with mocks; an integration test may connect components; a DB/currentness check may show that the persisted record survives an actual transaction; a physical check may open the real application; a perceptual check may confirm that a human can use it. Passing one does not silently cover the others, and a release gate has its own scope.

The report should also name the next action and its owner. A new business requirement belongs to the CLIENT and Planner; a known in-charter bug remains with I3; a complete source-bound candidate returns for consolidated strategic audit. This avoids turning a nontechnical product owner into the incident coordinator.

When accepting a capability, the Planner records which candidate was accepted, against which current charter and evidence, and what can be done next. When rejecting in-scope defects, it returns one consolidated list of falsifiers to the same campaign. A genuinely changed product intent must be recorded as a traceable decision, not hidden under “bug fix.”

## 6. Git and continuity

Git stores code and history; it is not itself a complete Product State or authorization ledger. A commit identifies content and parents, not every human or agent responsible for a decision, not a real DB witness, and not final product acceptance. A branch advancing does not demonstrate that a particular worker had authority or that a capability is current.

Do not create a canonical commit for every worker message. Execution specialists should provide their bounded changes and evidence to the integration owner, who checks interactions and currentness. A worktree may contain valuable uncommitted changes; never discard them simply to make a status check show a clean tree. When several workers share files, DB state or runtime surfaces, resolve interference based on affected resources rather than project name alone.

An existing correct checkout is normally preferable to another clone. Reuse it when safe, and use temporary worktrees only when justified by genuine concurrency. Keep generated screenshots, exports, renders and caches in ephemeral or ignored locations unless they are required evidence. Protect disk space as a production resource.

After a session limit, the same charter can continue if the current source, checkpoint, owners and evidence are reconstructible. A vendor's token limit is not a Charter Invalidation Event. When a host cannot resume a specific thread, use the canonical repository state rather than inventing continuity.

## 7. The five-question daily closure

At the end of a work period, obtain answers to five questions:

1. Which capability is active, and who currently owns execution?
2. Which code reference, Product State and relevant DB/currentness witness have actually been checked?
3. Which was the last real gate passed, and what evidence belongs to it?
4. What defect, risk, permission or product decision remains open?
5. What is the next legal action tomorrow, with a named owner, without requiring the CLIENT to arbitrate technical state?

Material decisions and next routes should be persisted in the repository's canonical locations. A chat may be useful discussion context, but it must not be the only surviving statement of current truth. The next worker should be able to answer the same questions by reading the project.

## 8. A working day without depending on chat memory

At the beginning of a day, recover the existing goal before proposing another feature. The Planner checks whether a campaign is still active, its integrated source reference, missing evidence and reserved decisions. The possible outcomes are straightforward: continue I3 execution, audit a consolidated terminal, request a product decision, or authorize a genuinely new capability after its prerequisites are satisfied.

A session interrupted by usage limits or a crash should resume from an actual recorded checkpoint. If no checkpoint exists but durable state is sufficient, reconstruct it. If neither is sufficient, identify the precise lost evidence and HOLD dependent changes. A fresh chat repeating the words “we were halfway through” is not evidence of the halfway state.

## 9. An example of a bounded dispatch

The following message illustrates the *content* of an authorized work order. It is not a universal permission to run in any repository:

> **Goal:** Implement the current charter's member-management capability.
>
> **Context and inputs:** Read the real `AGENTS.md`, confirmed requirements, canonical Product State, active charter and current source. Reconstruct applicable ownership and currentness before writing.
>
> **Constraints:** Retain payment history; preserve the confirmed local-only exposure; do not add online payments or unrelated features; do not publish or spend on external services.
>
> **Execution gates:** Physically exercise create, search, edit, deactivate and persisted history after restart; test invalid and duplicate inputs; independently review the integrated candidate.
>
> **Done when:** Provide the exact ref, source-bound evidence, review result, residual risks and an honest terminal for Planner audit. Resolve ordinary bugs, retries and internal refactors within the existing charter.

The actual dispatch should be adapted to the current approved charter and available tools. Do not invent `AGENTS.md` or Product State just because their names appear in this example. Locate the real surfaces and report any genuinely absent ones.

## 10. Interpret controller states

Status labels are operational clues, not substitute acceptance:

| State | What it indicates | What it does not prove |
| --- | --- | --- |
| `READY` | A runnable unit has satisfied prerequisite checks. | It is already executing or will succeed. |
| `ACTIVE` | An authorized unit is owned by an active execution context. | The resulting application behavior is correct. |
| `VERIFY` | Applicable checks are being assembled or executed. | Every product gate is satisfied. |
| `HOLD` / `CAPACITY` | A recorded dependency or resource condition blocks progress. | A new campaign must be opened. |
| Tactical `DONE` | A bounded execution unit met its local conditions. | Planner or CLIENT accepted the capability. |
| Strategic terminal | I3 has returned a candidate or a precisely evidenced blocker. | Publication or a reserved external action is authorized. |

The portable reference implementation does not create a complete distributed agent environment. If a project uses another controller, require equivalent verified guarantees of authority, currentness, concurrency, journal recovery and gate separation in the *actual* implementation.

## 11. Process the final report

The Planner reviews the exact candidate, proven environment, current requirements, actual tests, independent review and open risks. It should not redo I3's tactical implementation or rubber-stamp a self-reported PASS. Where evidence is incomplete, name the missing gate instead of treating all gates as failed or passed together.

For an in-scope rejection, the return message should give observed behavior, reproduction conditions, the exact evidence and the blocked gate in one consolidated batch. I3 owns correction and integration. If the same subsystem repeatedly fails for the same reason, require broader subsystem hardening and independent review within the campaign rather than serial one-line patches.

A truly new product rule, permission, or incompatible interface may require strategic reentry. That is not an excuse to reopen planning for a known regression. The distinction protects both product coherence and delivery speed.

## 12. Leave a recoverable session

Before stopping, persist the current code ref, active objective, existing checkpoint, relevant DB/asset witnesses, strongest test and review evidence, remaining blockers, and next route in the appropriate canonical surfaces. Keep private artifacts and credentials out of public repository docs. A genuine release or acceptance requires its own gate even when a tactical work unit finishes.

The CLIENT should be able to ask “what can I use today?” and get an answer about delivered capabilities and material risks. A newly opened context demonstrates durable continuity by recovering that answer from the repository and its authorized runtime evidence, without replaying the entire conversation.

**Next:** Chapter 04, Requesting Changes.

## Sources and applicability

- [Execution-team operating protocol](../../../../protocols/EXECUTION_TEAM_OS.md)
- [Capability lifecycle and evidence](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md)
- [Reference runtime](../../../11_REFERENCE_RUNTIME.md)
- [Repository efficiency and disk hygiene](../../../20_REPOSITORY_EFFICIENCY_AND_LOCAL_HYGIENE.md)
- [Outcome-first work orders](../../../44_OUTCOME_FIRST_AGENT_EXECUTION.md)
- [Goal/Plan source](../../../../tools/goal_plan.py)
- [Host dispatch source](../../../../tools/host_dispatch.py)
- [Reference campaign controller](../../../../tools/campaignctl.py)

These operational practices describe contracts and examples; their presence in a repository does not certify any particular external host or application runtime.
