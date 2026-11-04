# 04 — Requesting Changes

ArquitecturaRepo · Complete User Manual · v1.4 edition · English

> Product decisions belong to the CLIENT. The Planner converts them into confirmed requirements, technical boundaries, delivery expectations and verifiable gates. I3 may revise its tactical plan within an authorized charter, but cannot unilaterally change its strategic Goal, forbidden effects, or the CLIENT's product definition.

## In this chapter

1. Start with the outcome, not the code
2. A compact change-request brief
3. Which questions belong to you?
4. Change your mind without destroying history
5. Ask for quality without prescribing a stack
6. Prioritize instead of opening ten Goals
7. When the Planner needs a real decision
8. Five well-formulated requirements
9. Product change versus implementation defect
10. What to say when it works but is not useful
11. A short priority-setting script

## 1. Start with the outcome, not the code

The CLIENT describes who uses a function, what they want to do, what result they can observe, under what conditions it should fail, and what information must survive. The Planner translates that intent into confirmed requirements, dependencies, implementation boundaries, and acceptance gates. Technical preferences are legitimate, but routine decisions about APIs, database schemas, code organization and regression tests normally belong to engineering.

“Add a cancel button” is often incomplete. If cancellation affects remaining places, money, membership status, or history, simply drawing a button is not a complete solution. A useful question is: *When an enrollment is cancelled, does a place become available again? What stays in the historical record?* The answer defines observable behavior and the tests needed for acceptance.

The framework helps separate the product problem from a proposed implementation. An assistant may propose a button, an action menu or another interface, but the CLIENT's actual requirement is the correctly understood cancellation behavior. A visual mockup without the state and error behavior can help discussion; it is not by itself evidence of a finished capability.

## 2. A compact change-request brief

A product request need not be a lengthy specification. For meaningful changes, describe the actor, starting situation, desired action, visible outcome, important exclusions, and retained information. Example:

> As the club administrator, I want to deactivate a member without deleting earlier payments. The deactivated record should disappear from active-member search but remain available to authorized staff in historical views.

The Planner should still clarify whether deactivation can be reversed, whether duplicate identities are allowed, and which historical information must be retained. You should not need to design the database or write the tests yourself.

Here is a complete example for activity enrollment:

| Field | Example |
| --- | --- |
| User | Club administration staff. |
| Starting situation | A member wants to join an activity. |
| Visible outcome | The enrollment is saved only when a place is available and current rules permit it. |
| Exclusions | No online payments or automatic notifications in this version. |
| Retained information | Member identity, activity, date, status and subsequent changes. |
| Acceptance | Staff can enroll the member, see places remaining and cancel without erasing history. |

Do not make the CLIENT fill out ten fields for every small correction. The purpose of the brief is to remove ambiguity that materially affects behavior. The Planner should make confirmed material changes durable; a conversation alone is not a reliable record for a new executor.

## 3. Which questions belong to you?

A question belongs to the CLIENT when it changes the product: Does an overdue payment block activity enrollment? Can an authorized user recover a deactivated record? Does the application need to work offline? May the system send emails, accept online payments, incur costs or publish member information? Those are decisions about people, risk and intended use.

Engineering questions include SQL schema details, API design, test frameworks, branch names, logging structure, internal retry algorithms and migration implementation. The Planner may explain consequences when a technical decision materially changes cost, security, portability or user-visible behavior, but should not ask the CLIENT to arbitrate a failed migration simply because an executor was unable to debug it.

When there are legitimate product alternatives, present them in understandable terms. For example: *With a waiting list, staff must confirm a place when one becomes available; without a waiting list, the enrollment is rejected immediately.* Explain cost and usability consequences, make a recommendation if appropriate, and ask for the actual product choice. There is no need to teach the CLIENT a database schema to obtain an answer.

## 4. Change your mind without destroying history

Product requirements can change. The system needs to know **which** decision changed, **what** replaces it, and **when** the new rule applies. For example:

> Previously members with overdue dues could not enroll in activities. From now on they may enroll, but the administrative view must clearly display outstanding debt. Record the previous rule as superseded and assess the effect on current screens, data and tests.

This may affect eligibility checks, the UI, persistent data, tests and ongoing campaigns. The Planner traces those dependencies and updates the canonical current requirement. A legitimate new requirement does not mean the earlier requirement was fictitious; it means its authority has changed. Two independent `CURRENT` documents silently demanding opposite behavior are a governance defect.

Similarly, the CLIENT may decide:

> I no longer want the application to permanently delete members from its interface. Deactivation must retain their payments and enrollments. Treat the old deletion rule as superseded, examine what happens to existing data, and explain the resulting user journey.

The engineering team owns the migration strategy, recovery, tests and interface changes. The CLIENT approves the new intended behavior and any reserved risk decisions. The current requirement must be reconstructible by a future session without replaying this chat.

If the change fundamentally alters the product boundary—for example, a local one-club tool becomes a multitenant Internet service—the Planner may need to invalidate or supersede a charter and reconsider architecture and dates. If the desired behavior was already in the charter and a test merely exposed defective code, I3 corrects the defect in the same campaign.

## 5. Ask for quality without prescribing a stack

“Make it professional” expresses a direction but is not a measurable acceptance condition. Describe what frustrates or misleads a real user: being unable to find a member, losing entered data on an error, not knowing whether a payment was saved, receiving a cryptic validation message, or triggering an irreversible action without confirmation.

A concrete request might be:

> The dues screen must show status, amount and the date of the latest payment without opening several unrelated windows. If saving fails, it must not display success. I prefer a clear, consistent interface over decorative complexity.

This can lead to usability criteria, integration checks and perceptual review without requiring a particular frontend library. A screenshot of the actual application with a precise criticism can be more useful than a list of adjectives. The CLIENT's subjective judgment can be a real human/perceptual gate where product quality depends on the experience. No screenshot classifier or successful unit test should silently impersonate that acceptance.

Quality also includes negative behavior. A payment screen that works in the happy path but duplicates transactions after a double click may be unacceptable. A form that technically saves but loses entered data after a validation error may fail a usability requirement. The Planner should map such outcomes to appropriate gates, while I3 decides how to implement and test the fixes.

## 6. Prioritize instead of opening ten Goals

Priority determines which capability should become usable first, within dependencies and resource constraints. For the club, the sequence might be: reliable member records, then dues, then activities and enrollments. If the third step requires the first two, document the dependency. Do not authorize ten competing capabilities merely because an assistant can generate ten plans.

| Vague request | More useful direction |
| --- | --- |
| “Build the whole club system.” | “Make member management verifiable first; add dues after its data flow is dependable.” |
| “Fix whatever is wrong.” | “Cancelled enrollments are not releasing places; correct that behavior without losing history and demonstrate the complete flow.” |
| “Make it more modern.” | “Reduce the steps needed to find a member and check overdue dues; prioritize readability.” |
| “Add everything customers might want.” | “Validate the first administrator journey with real examples before expanding scope.” |

If priorities shift while I3 is executing, the system should leave a recoverable checkpoint or properly close the active boundary before changing course. An abrupt priority change is not permission to abandon uncommitted valuable work, erase a campaign record, or silently redirect a Goal. The Planner accounts for dependencies, interference and the critical path.

## 7. When the Planner needs a real decision

The Planner should frame the question as a user consequence, describe the viable alternatives, identify any cost or risk differences, and state what the CLIENT alone must choose. A question such as “Should staff be able to reinstate a cancelled enrollment?” is useful. “Should I use an index with this SQL migration?” generally is not.

When you ask for status, a good answer has three parts: which behavior is physically proven now; what remains before the current objective can be accepted; and whether any indispensable product choice is waiting for you. It should not bury the answer under commit counts, token consumption, worker names, or a technical timeline with no visible result.

If you do not know the answer to a material product question, say so. Mark it open and continue safe work that does not depend on it. Engineering must not silently convert an unconfirmed preference into an authorized requirement.

## 8. Five well-formulated requirements

### Search

> I want to find a member by name or membership number and distinguish active from inactive records. When there is no match, show a clear explanation. Do not expose personal data to unauthorized users.

This defines behavior, an empty-state experience, and a privacy requirement without choosing a search engine. The team can test authorized and unauthorized cases.

### Edit

> Staff need to correct a member's phone number. Before saving, the screen must clearly identify which member is being edited. Invalid input must not erase the rest of the form; show an understandable error.

This describes navigation, state retention and feedback. A successful API endpoint test alone would not demonstrate the whole interaction.

### Deactivation

> Deactivating a member removes the record from the active list, preserves payment history and allows authorized staff to inspect that history.

The word “deactivate” now has a testable meaning. If legal retention or deletion requirements later apply, treat those as a distinct decision and risk review.

### Performance

> Search should remain usable at the number of members we expect in the first year. If the Planner needs that number to size a solution, ask me; do not assume an enterprise scale without evidence.

This connects performance to real workload instead of prescribing a premature database or caching technology.

### New capability

> Add activity enrollments only after members and dues are usable. First confirm capacity, cancellation, overdue-payment and permission rules, then plan integration.

This prevents an apparently finished component from depending on incomplete or contradictory upstream capabilities.

## 9. Product change versus implementation defect

If the confirmed rule prohibits overdue members from enrolling but the application allows it, the implementation violates the current rule. I3 fixes and tests that defect inside the existing authorized scope. If nobody has decided how partial payments affect eligibility, the Planner needs a product clarification before choosing a behavior. If the CLIENT now wants family members to pay for each other, that is a new product rule with potentially new identity and permission implications.

The distinction protects two responsibilities. Engineering should not demand CLIENT approval for every known bug. Equally, it should not convert a new user preference into an unreviewed technical assumption. Material changes update current requirements and preserve what they superseded, so a newly assigned agent can determine the valid rule.

A tactical-plan edit is not automatically a change to product intent. The protected strategic Goal may contain `goal_id`, `campaign_id`, `charter_ref`, `authority_refs`, `definition_of_done`, `hard_gates`, `forbidden_effects`, and `write_envelope`. I3 can revise steps, hypotheses and internal testing plans within that envelope. It cannot simply rewrite a forbidden external effect into an allowed one.

## 10. What to say when it works but is not useful

You can reject a capability because the real user journey is unusable even if saving technically succeeds. For example:

> The form correctly saves the member, but on the phone the confirmation button is outside the visible screen. I cannot accept the user journey until I can complete it on that device.

Attach a screenshot or describe the exact screen size, state, and expected behavior when possible. That is useful perceptual evidence. However, if mobile support was explicitly excluded from the current requirement, adding it may be a product scope change rather than an ordinary in-charter regression. The Planner should make that boundary explicit and, if needed, revise dates and dependencies. If mobile use was already required, I3 repairs the candidate and updates affected evidence within the same campaign.

The CLIENT's judgment is not a substitute for technical testing either. A beautiful screen can still have broken persistence, authorization checks or recovery. A genuinely accepted capability needs all the gates relevant to its intended use, each with its own owner and evidence.

## 11. A short priority-setting script

You can tell the Planner:

> My current priority is [visible outcome]. The user is [who]. They must be able to [complete journey] and must not [important prohibition]. My target date is [date], and the spending limit is [budget, if any]. Before implementation, tell me which product decisions remain open and which current capabilities depend on this change. Engineering owns the technology, tests, integration and in-scope recovery.

You do not have to repeat the wording literally. The objective is to make your intent recoverable and testable without converting every casual suggestion into an irreversible commitment. A capable Planner knows when to ask, when to verify physical state, and when to let I3 execute.

**Next:** Chapter 05 for errors, blockers and sensitive authorizations; Chapter 06 for capability acceptance.

## Sources and applicability

- [CLIENT decision boundary](../../../../protocols/CLIENT_BOUNDARY.md)
- [Interaction ledger](../../../../protocols/INTERACTION_LEDGER.md)
- [Product discovery session](../../../../prompts/PRODUCT_DISCOVERY_SESSION.md)
- [Product requirements and technical baseline](../../../../protocols/PRODUCT_DISCOVERY_REQUIREMENTS_AND_TECHNICAL_BASELINE.md)
- [Capability lifecycle and evidence](../../../../protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md)

The club examples demonstrate good product requests. They do not constitute an actual CLIENT decision for an adopter's application.
