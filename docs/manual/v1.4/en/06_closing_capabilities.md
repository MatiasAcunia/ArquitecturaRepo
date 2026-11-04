# 06 — Closing Capabilities and Acceptance

ArquitecturaRepo · Complete User Manual · v1.4 edition · English

> A capability closes against an **exact candidate and the applicable evidence**. An I3 terminal invites strategic review; it does not automatically approve a product, satisfy a human gate, grant publication rights, or deploy anything. This chapter separates those decisions and explains how to correct in-scope failures without restarting the architecture.

## In this chapter

1. A capability is a product result
2. Five components of closure
3. The exact candidate is the review unit
4. Missing evidence does not require an artificial campaign
5. Accept, resume, or change objective
6. Periodic review and the stopping rule
7. An auditable closure record
8. Rejection example: correct without restarting
9. Usable product versus green framework
10. When to end a session or stop work

## 1. A capability is a product result

“Member management” is not finished when someone draws a form or commits its component. It is finished when the agreed behavior works in the relevant environment, required information survives, applicable checks pass, current state and lineage are coherent, and the appropriate strategic and human authorities have accepted the result.

The Planner defines the capability's boundary and charter. I3 integrates an exact candidate, obtains independent review when required, and returns source-bound evidence. The Planner audits that terminal against current requirements and charter acceptance criteria. The CLIENT decides reserved product preferences, perceptual quality and external effects when applicable.

A cycle is not a fixed number of prompts or one coding session. A campaign can survive ordinary retries, a disconnected host and several execution checkpoints. Those changes do not create new authorization or erase earlier evidence. Conversely, a large number of commits and a confident report do not establish that the person using the application can complete the journey.

## 2. Five components of closure

| Component | Closure question |
| --- | --- |
| Visible result | Can the intended person perform the requested task in the relevant environment? |
| Applicable checks | Have the unit, integration, DB/recovery, security, runtime, UI and other gates relevant to this capability been exercised? |
| Coherent current state | Is the candidate's exact code and configuration known, together with current requirements, Product State and affected data/artifacts? |
| No concealed material blocker | Does any unresolved defect invalidate the claimed result despite passing unrelated checks? |
| Competent acceptance | Have the Planner and, where applicable, the CLIENT inspected evidence within their authority instead of accepting a generic `DONE`? |

Not every capability needs every possible test. A static internal tool may have no meaningful perceptual gate, while a member-payment application must address data persistence and the human-facing payment journey. The crucial rule is that one gate may not silently replace a different gate that actually applies. A valid JSON schema is not evidence of durable CRUD operations; a unit test is not proof that a person can find the function on screen.

Use the following gate vocabulary consistently:

- **Unit:** individual logic behaves correctly under controlled inputs.
- **Integration:** interacting components satisfy their interface contracts.
- **DB/currentness:** relevant records, migrations, source bindings, and runtime witnesses agree and persist as required.
- **Semantic/generalization:** the behavior matches the actual intended rule beyond one narrow fixture.
- **Physical:** the program or artifact genuinely runs, opens, renders or performs the journey on the relevant target.
- **Perceptual/human:** a qualified person assesses the experience or subjective product criteria where necessary.
- **Release:** the exact distributable candidate, permissions, rights and downstream publication conditions are satisfied.

The evidence, owner and need for each gate should be proportional to the feature. Adding a dozen unnecessary checks can reduce delivery without increasing safety; omitting a material gate can produce a convincing report about a broken product.

## 3. The exact candidate is the review unit

An independent reviewer must inspect the same source and state that will be proposed for acceptance. Depending on the capability, that may require code ref, configuration, DB snapshot or schema version, exact asset hashes and runtime environment. A review against candidate A cannot simply be transferred to B because both have the same branch name or filename.

The normal sequence is: integrate candidate, freeze its relevant identity, perform independent review and required physical tests, then submit a terminal for strategic audit. If a producer materially changes the candidate after that review, the affected approval needs to be renewed for the new candidate. This does not require erasing unrelated stable evidence, but it does forbid treating a stale favorable review as an endorsement of changed bytes.

The [review-freeze and terminal-integrity protocol](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md) defines this relationship. The optional reference controller can model freeze, review and terminal states; it cannot impersonate the actual product owner or automatically demonstrate a proprietary host's behavior.

Even after technical review passes, human acceptance, real deployment evidence, privacy checks, third-party rights or public-release authorization may remain open. Record those as separate downstream gates. A technical I3 terminal means “candidate ready for the appropriate review,” not “every authority has approved every effect.”

## 4. Missing evidence does not require an artificial campaign

If the remaining defect is within the authorized charter, the Planner sends I3 a **consolidated** list of falsifiers and their evidence. I3 researches, repairs, integrates, retests and arranges a new appropriate review in the *same* campaign. It should not ask for a new strategic plan after every failed test.

After repeated returns of the same defect class, the right response is broader subsystem hardening and independent review, not a chain of narrowly worded microfixes. A newly discovered material product choice, changed authorization or incompatible strategic interface may instead require the Planner to revisit the charter boundary. The distinction prevents both governance churn and uncontrolled scope expansion.

A useful terminal summary is short:

> **Candidate:** exact ref and environment. **Observed result:** the user journey actually exercised. **Passed gates:** linked evidence. **Open gates:** the specific limitation and impact. **Remaining risks and new product decisions:** separated. **Next action and owner:** one clear current route.

This is a readable view of canonical evidence, not a second Product State to maintain in parallel. References must resolve to the actual reviewed candidate, not merely a similarly named log or a prior version.

## 5. Accept, resume, or change objective

**Accept.** When the right authorities have the right evidence, the Planner records the accepted capability and updates canonical Product State and current pointers. The CLIENT completes any reserved perceptual or product acceptance. Only then should dependent downstream work rely on the newly accepted result.

**Resume after interruption.** A new executor or Planner reconstructs the current campaign and checkpoint. It does not mark started work complete because a service limit was reached, nor does it invent approval because a session ended. Current source, DB, owners and evidence remain stronger than remembered conversation history.

**Change priorities or product intent.** A temporary scheduling adjustment is not necessarily a requirement change. A changed rule about data or user behavior is. Record supersessions and make unfinished work recoverable. Do not keep two contradictory active charters for the same concern, and do not erase earlier valid work merely because the priority order changed.

## 6. Periodic review and the stopping rule

Once a week, the CLIENT should be able to ask: Which capabilities are accepted? What is the current priority? What can actually be demonstrated today? Which target date is still justified? What material risk remains? Is there a product decision only I can make?

The answer should be grounded in source and evidence, not a tally of commits, agents, hours, review comments or tokens. Such activity may be necessary, but it is not the delivered result. A framework can become counterproductive if it adds more reporting than it removes uncertainty.

The reusable starter has a stopping principle too: once release gates are met, do not continuously add generic policy and machinery merely to keep engineering active. New mechanisms need an identified class of failure or genuine capability gap that existing controls do not address. Apply the same discipline inside products. Both premature acceptance and infinite searching for immaterial microdefects undermine trustworthy closure.

## 7. An auditable closure record

A new worker who was absent during implementation should be able to understand the evidence without reading the entire chat. A compact closure record provides a map to canonical sources:

| Field | What must be traceable |
| --- | --- |
| Candidate | Exact source/state/artifact identity reviewed. |
| Outcome | End-to-end journey, with concrete input, action and observable output. |
| Tests | Relevant execution outputs and environment. |
| Persistent state | Post-write readback, restart and recovery checks where applicable. |
| Security and rights | Proportional checks for sensitive data, network exposure or third-party material. |
| Independent review | Reviewer identity, scope and exact candidate examined. |
| Post-review changes | Whether anything material changed, and which checks were renewed. |
| Human gate | Authentic acceptance or rejection where real usability or subjective quality matters. |
| Next route | Accept, return to I3, request product decision, or HOLD with a specific cause. |

Do not create another competing `CURRENT` file for the convenience of this table. The record is a way to navigate existing canonical evidence. If a link leads to an old ref, a missing artifact or a test fixture unrelated to the claimed product, the record is insufficient for acceptance.

The two broad families of framework release evidence should also remain separate: internal code/contract/transaction correctness, and a complete installed lifecycle on a real portable target. Neither family automatically certifies UX or business correctness of an unrelated application built with the framework.

## 8. Rejection example: correct without restarting

Suppose a club application now supports creating and deactivating members. Independent review discovers that deactivation erases payment history, contrary to the charter. That is an implementation defect within the already authorized capability. The Planner returns one clear falsifier: *Deactivation of a member with payments must preserve historical transactions after a restart; currently payments disappear.*

I3 examines persistence and relationships, fixes the cause, adds meaningful regression tests, demonstrates the record after restart, integrates the new candidate and obtains a new independent review. It does not open a separate “fix deactivation” campaign or ask the CLIENT whether a foreign key should cascade.

If the reviewer inspected version A, and the persistence change produced version B, the PASS for A cannot accept B. This is why exact candidate identity matters. Evidence from unaffected tests may remain reusable when their source dependencies are unchanged, but the affected persistence and review gates must be updated.

Now consider a different event: the CLIENT requests a new permission-based reactivation feature. That is not a repair of the known deletion defect; it is a new product rule. The Planner confirms the desired behavior, assesses existing interfaces and risk, and decides whether it fits the authorized envelope or requires strategic revision.

## 9. Usable product versus green framework

A campaign may pass governance validation and put its reference controller in a terminal state while producing no usable application screen. Product acceptance must demonstrate the actual requested result. For a local club app, open it, register a fictional member, find the record, edit it, deactivate it, and confirm that payment history survives. If persistence matters, restart the application and repeat the relevant readback. If permissions matter, test the unauthorized path too.

ArquitecturaRepo's own release gate is different. `tools/verify_v1_release.py` checks a concrete snapshot of the reusable framework and synthetic fixtures. Source verification, Linux/Windows portable install checks, and release artifact readback are distinct checks. A green framework release does not certify every possible adopted installation or application made with it. An external/native host adapter requires its own demonstrated compatibility.

The [v1.4 support matrix](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md) explicitly distinguishes what was exercised from what remains outside portable proof. Keep those limits visible when reporting a project's progress. The phrase “all tests passed” must say whose tests, on which candidate, and against which capability.

## 10. When to end a session or stop work

After strategic acceptance, persist the change to current Product State, maintain source-bound lineage and unblock only dependencies justified by that acceptance. After an in-scope rejection, return to the same campaign. After a material invalidation, revisit the strategic boundary with the appropriate owner. When evidence cannot establish currentness, leave a concrete HOLD rather than guessing.

The CLIENT can finish a day without understanding the internal controller, but should know which capabilities are usable now, which are not, what decision is required of them, and when the next milestone will be reviewed. A project that can answer those questions only while yesterday's chat remains open has not achieved durable continuity.

**Next:** Chapter 07, A Worked Club Example from Discovery to Acceptance.

## Sources and applicability

- [Review freeze and terminal integrity](../../../../protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md)
- [Capability lifecycle and evidence](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md)
- [Executable validation](../../../10_EXECUTABLE_VALIDATION.md)
- [Reusable-framework release gates](../../../17_V1_RELEASE_GATES.md)
- [v1.4 supported installation and distribution scope](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Release verifier source](../../../../tools/verify_v1_release.py)

Acceptance is always source- and context-specific. These examples do not create authority or substitute for actual evidence in an adopting project.
