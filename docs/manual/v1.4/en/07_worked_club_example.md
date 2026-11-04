# 07 — Worked Example: A Club Management Application

ArquitecturaRepo · Complete User Manual · v1.4 edition · English

> This is a **fictional teaching example**, not a deployed application, a generated backend, or proof that an AI model can automatically deliver an accepted CRUD system. The examples, records and candidate names below are illustrative. On a real project, requirements, source, DB/WAL state, tools and acceptance evidence must come from that project.

## In this chapter

1. The example product: a club with concrete needs
2. Ask questions that change the product
3. Install without confusing a starter with an application
4. First capability: member management
5. From Planner to execution: a complete request
6. What to test before acceptance
7. Second capability: dues, without expanding scope
8. Evaluate the whole example
9. The first cycle with fictional data
10. Record a finding and route it correctly
11. The second cycle depends on the first
12. Final exercise: recover the project in a new context

## 1. The example product: a club with concrete needs

An association employs one administrative worker who registers members, tracks dues, manages activities and records enrollments. The application must preserve relevant history, avoid oversubscribing activities and show who is up to date with dues. The first release is simple, internally operated, and deliberately excludes online payments, a dedicated mobile app, fiscal invoicing and external integrations unless a later product decision justifies them.

That product description gives a direction, not an implementation. It does not decide whether the source will be Python, Java or another language; it does not define a verified schema or host; and it does not authorize anyone to access genuine membership data. The real codebase, stack, threat model, operating environment, and exact acceptance gates must be reconstructed when an actual project exists.

A useful capability sequence is member identity → dues and payment history → activities and capacity → enrollment eligibility and cancellation. This is a dependency relationship, not an invitation to create four agent hierarchies or four independent products. If the first capability lacks trustworthy member identity, subsequent payments cannot safely refer to those members. If the second capability cannot produce a current dues status, enrollment eligibility cannot truthfully rely on that status.

## 2. Ask questions that change the product

The Planner begins by asking the CLIENT who operates the club, whether the program is restricted to one computer or accessed over a network, what personal data is held, how backups should work, the budget, target date and which actions may alter historical records. A plausible first rule is: *An administrator may deactivate a member, but earlier payments must remain available to authorized staff.*

Other decisions must be explicit. Does any overdue dues period block a new enrollment? Can the member enroll when they have a payment arrangement? Does cancellation free a place immediately? Is there a waiting list when an activity is full? Do different employees need different rights? Without confirmed answers, a Planner should not turn guesses into the current product specification.

An illustrative first-version baseline is:

| Area | Requested first-release behavior |
| --- | --- |
| Members | Create, edit, search and deactivate, while preserving historical relations. |
| Dues | Register payments, identify overdue periods and inspect history. |
| Activities | Name, schedule, capacity and available places. |
| Enrollments | Register/cancel participation with capacity and dues rules. |
| Exclusions | No online payment, mobile application, mass notifications or complex dashboards. |

Every line is provisional until the CLIENT confirms it. Dues and enrollments imply persistent application state, so the Planner would evaluate the `STATEFUL` profile and the data, idempotency, recovery and security controls justified by real usage.

## 3. Install without confusing a starter with an application

For a new ungoverned club repository, the installer may create the control layer with the justified profile. From a v1.4 source checkout in PowerShell:

```powershell
& "python" "tools\scaffold_project.py" --target "..\club-app" --profile "STATEFUL" --product-id "CLUB_MANAGER" --objective "Fictional club member and dues management" --language "en" --no-feedback-workflow
```

The result is `.agentic-sdlc/` inside `club-app/`, initially in `HOLD / UNTRUSTED_CONTEXT`. The installer does not claim that any existing club application runs, that its DB is configured, or that a development campaign has authority. If `club-app/` already has canonical governance, use the [read-only governed-project attachment](../../../32_EXISTING_GOVERNED_ATTACHMENT.md); do not install a second control layer or force over the first.

After creating an initial scaffold, the installer provides read-only status, inventory and reconstruction commands for that target. [Chapter 01](01_installation.md) includes the v1.4 sequence. The Planner and I3 then inspect source, inventory, baseline, requirements and existing state. They prepare a reviewed adoption specification, run preflight, promote coherent records and demonstrate fresh-context reconstruction.

The CLIENT reviews the actual scope and approves product behavior. Engineering selects a justified stack, DB, network exposure, permissions, backup strategy and dated delivery milestones. Only when the relevant baseline and currentness gates are coherent should the Planner authorize a first material charter.

## 4. First capability: member management

Starting with members is a product dependency choice. Payments, activity enrollments and other records need a stable member identity. The first campaign's outcome might be:

> An authorized administrator can create a member, inspect the record, correct details, find it through search and deactivate it. Existing historical payments or enrollments remain intact and available through the permitted interface.

The charter should name affected interfaces, data ownership, expected error behavior and applicable gates. Tests include duplicate identities, invalid data, actual writes and subsequent reads, persistence after application restart, correct active/inactive filtering, safe historical relations, and a complete user-interface journey when the product has a UI. Independent review must inspect the exact integrated candidate.

The CLIENT does not need to specify the ORM, transaction boundaries, table names or folder layout. Engineering should explain any choice that changes cost, accessibility or reserved risk. Existing data must be treated as current evidence, with migrations and backups handled through an authorized process. No sample record from this manual should be confused with a real user.

## 5. From Planner to execution: a complete request

A dispatch can be compact while still giving I3 what it needs:

> **Goal:** Deliver the member-management capability in the current authorized charter.
>
> **Context:** Reconstruct confirmed requirements, canonical Product State, real repository and exact source ref. Identify affected member records and current DB state.
>
> **Constraints:** Preserve history; do not introduce dues processing, notifications or other unrelated features; remain within the confirmed network and spending boundaries.
>
> **Execution gates:** Physically exercise create, search, edit, deactivate and durable readback. Test invalid and duplicate inputs, plus relevant authorization and concurrency paths. Independently review the integrated candidate.
>
> **Done when:** Return exact candidate ref, verifiable physical evidence, applicable test results, review findings, remaining gates and an honest strategic terminal.

I3 may break the work into tactical steps, implement and review in bounded units, debug and retry. If a double click creates the same member twice contrary to the confirmed uniqueness rule, I3 fixes the defect in the same campaign; there is no need to open a second strategic campaign for duplicate prevention.

Where work has multiple material operations or significant cost, add a bounded work order with a concrete inventory, method, budgets and stop conditions. A work order is part of the existing authorized campaign; it cannot expand the CLIENT's product request or call a paid provider without authorization.

## 6. What to test before acceptance

Use fictional records such as `MEMBER-001`. The test plan below is a specification of actions to perform, **not evidence that any such application exists**:

| Step | User action | Expected observable outcome |
| --- | --- | --- |
| 1 | Open the application as an authorized administrator. | The real login or local-access mechanism permits the intended role. |
| 2 | Create `MEMBER-001` with valid synthetic details. | Exactly one member record is saved; success and identity are visible. |
| 3 | Search by an allowed identifier. | The correct record appears, without revealing unauthorized data. |
| 4 | Change a fictional phone number. | The new value appears after saving and a fresh read. |
| 5 | Close and reopen the application. | The change persists through the actual DB/recovery path. |
| 6 | Deactivate the member. | Active search no longer returns the record as active. |
| 7 | Inspect history with appropriate permissions. | Historical payment and enrollment records remain available. |
| 8 | Attempt an invalid/duplicate operation. | The app rejects it clearly without silently corrupting state. |

For each step record the exact candidate, test input, expected result, observed result and environment. A lack of visible errors is not proof of persistence; inspect the post-write state through the actual application or an appropriate data readback. If two employees can act simultaneously, exercise the concurrency scenario in that environment rather than inferring it from a sequential test.

Do not put real members' personal information in screenshots, public issue descriptions or videos. When the UX matters, a qualified human should complete the journey and provide the perceptual result, separate from automated tests. When the data matters, check current DB/WAL witnesses, relevant recovery behavior and rollback protections in the real environment.

## 7. Second capability: dues, without expanding scope

Once members are strategically accepted, the CLIENT may request recording dues payments, viewing who is current and retaining a complete payment history. The Planner confirms billing periods, partial payments, overdue states, corrections, permissions and who may edit financial records. Engineering then chooses appropriate persistence, idempotency, audit and recovery mechanisms.

For example, the CLIENT might decide: *If a payment was recorded in error, administrators reverse it with an audit entry instead of permanently deleting the original transaction.* This is a product decision with technical consequences. The Planner records it; I3 implements the schema, behavior and tests. The implementation should reject accidental duplicate effects when a user repeats an action or a network request arrives twice, according to the confirmed rule.

Activity enrollment and capacity management should follow when their upstream member identities and dues status are trustworthy. Avoid adding microservices, a cloud payment processor, a complex permission system or a mobile app merely because those technologies are available. Each additional mechanism needs a real product or risk justification.

## 8. Evaluate the whole example

At the end of this exercise, you should be able to explain what the CLIENT decided, how the Planner confirmed and persisted requirements, what physical evidence I3 produced, why a green test cannot automatically establish acceptance, how the team handles an ordinary in-scope defect, and how a fresh worker reconstructs the current state.

The objective is not to memorize every internal file name. It is to know where each decision belongs and to require an observable result whose provenance remains accessible after the chat ends. A system with elaborate role descriptions but no demonstrable member journey has not delivered the product outcome.

## 9. The first cycle with fictional data

To practice, invent a member named “Test Member A” and a fictional contact number. Confirm which fields the product genuinely requires and which identifier must be unique. The Planner expresses the requirement, while engineering chooses the storage model, uniqueness controls and transaction behavior.

Perform the full path: create the member, see them in the list, search, edit, restart the program, read the edited record, deactivate, and inspect permitted history. Record expected and observed outputs at every point. The initial UI screenshot is just the beginning of this proof; it does not demonstrate what the DB actually persisted.

Add negative cases: duplicate unique identifiers, invalid fields, simulated controlled DB disconnection during save, and repeated submissions that might reach the backend twice. The exact expected error depends on the confirmed product rule; silently inconsistent data is not an acceptable default. Where several operators are in scope, verify interleaving or simultaneous actions rather than claiming concurrency safety from a single-user fixture.

## 10. Record a finding and route it correctly

Suppose the CLIENT tries deactivating “Test Member A” and sees that payment history disappears. If retention was already a confirmed requirement, the behavior is an implementation defect. Record the candidate ref, steps, observed output and affected gate. The Planner sends that consolidated falsifier to I3. The controller repairs the persistence path, reruns physical and data checks, integrates a new candidate and obtains an appropriate independent review.

Now suppose the CLIENT asks whether an inactive member may be reactivated with the same member number. If no earlier decision defines that behavior, do not label either possible outcome a bug. The Planner asks the product question, records the new requirement and evaluates its impact on current authority and interfaces. A new rule and a violation of an existing rule are not equivalent events.

The team should not manufacture acceptance on the basis of the manual's fictional narrative. If no actual application has been built, the correct status of all physical demo steps is **NOT RUN**, not PASS. The point of the exercise is learning which evidence would be necessary.

## 11. The second cycle depends on the first

Dues need a stable member key and clear rules about partial payments, duplicates, deadlines and corrections. The CLIENT confirms these rules; the Planner records them against the accepted member capability. I3 then implements them with sufficient integration, DB and recovery checks. The next campaign should use the accepted candidate and its current interfaces, not a remembered earlier implementation.

Before implementing activity enrollment, verify that the dues status consumed by eligibility rules actually exists and is current. Starting with enrollments while dues policy remains provisional can lead to duplicated or contradictory checks. This is a critical-path relationship between product capabilities, not a requirement to run more agents or create a complex organization.

## 12. Final exercise: recover the project in a new context

Imagine the work stops and a different Planner enters tomorrow. Without giving that worker the previous chat, the repository and authorized runtime should reveal whether member management is accepted, which exact candidate and evidence support it, which dues questions remain open, who owns execution, and what next action is permitted.

If two campaigns claim to be active for the same resource, or an old report is labeled current, the worker should recognize and reconcile that contradiction instead of guessing. If a source or DB witness is missing, it should declare the specific uncertainty and HOLD dependent work, while continuing permissible read-only investigation.

The exercise is complete when you can distinguish: a genuine product decision, an in-scope defect, a temporary environment failure, a required external authorization and an actual strategic charter invalidation. Demonstrable physical results and independently reconstructible current state—not installation alone—are the final learning outcome.

## Sources and applicability

- [Minimal synthetic example](../../../../examples/minimal/README.md)
- [Fork and bootstrap](../../../01_FORK_AND_BOOTSTRAP.md)
- [Product discovery and dated delivery](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md)
- [CLIENT boundary](../../../../protocols/CLIENT_BOUNDARY.md)
- [Campaign charter standard](../../../../protocols/CAMPAIGN_CHARTER_STANDARD.md)
- [v1.4 public start](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Existing governed-project preflight](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)

The source-backed instructions and fictional club examples are educational. None of them establishes a real application, permission, accepted feature or tested deployment.
