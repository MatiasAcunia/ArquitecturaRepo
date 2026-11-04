# 02 — The Planner and Project Adoption

ArquitecturaRepo · Complete User Manual · v1.4 edition · English

> A scaffold is a starting control layer, not a project baseline. This chapter explains how the Planner reconstructs an application, obtains the CLIENT's product decisions, adopts verified state, and authorizes the first bounded campaign. For concrete commands use the [v1.4 public start](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md) and [adoption contract](../../../16_TRANSFER_ADOPTION.md).

## In this chapter

1. A conversation is not the project
2. Prepare the working space
3. Discovery: ask the right questions
4. Technical baseline and delivery plan
5. Adoption: connect the starter to reality
6. The real examination: a fresh context
7. The first authorized engineering campaign
8. An example first Planner session
9. A baseline the CLIENT can actually confirm
10. An example of a first campaign

## 1. A conversation is not the project

The I2 Planner owns strategic decisions for a product or bounded workstream. A chat application can provide a convenient interface, but its conversation history is neither a canonical database nor evidence that the latest implementation still matches an earlier statement. Durable authority comes from the CLIENT's current requirements, applicable protocols, verified repository and DB state, active ownership, and valid campaign records. If the last executor said “done,” the Planner still needs evidence of the exact candidate and the relevant acceptance gates.

In a small project, one Planner and one execution owner may be sufficient. An I1 Master Owner is useful when several products, separately planned workstreams, shared budgets, or cross-cutting operational controls demand an additional systemic owner. It is not a higher-ranking replacement for the product Planner, and simply naming another chat “Master Owner” does not improve delivery.

The Planner thinks from the intended product outcome backward: who will use the capability, which current interfaces and data it affects, how the result is observed, which dependencies are real, and what would falsify acceptance. It then prepares a capability-level charter. Within that authorized scope, the I3 Execution Controller handles debugging, retries, code organization, integration, review and recovery. An ordinary bug should not create a new charter or a new strategic planning cycle.

## 2. Prepare the working space

Start with the actual application repository, not a remembered description. Read the project's `AGENTS.md`, applicable governance protocols, current requirements, canonical Product State, relevant source references, and existing campaign or runtime records. If the Planner cannot see a necessary repository or host surface, it must identify that specific gap. A plausible memory of a previous conversation is not an acceptable substitute.

You may organize conversations in a ChatGPT project or another collaboration space and attach the manual for convenience. If using a GitHub connector, restrict it to the repository and permissions required. Verify actual access with a read-only request for a known current file. A connected account does not guarantee access to every branch, DB, issue, or runtime. The architecture does not mandate any model, reasoning setting, subscription, or particular vendor.

A useful opening role instruction is:

> Act as this project's I2 Planner. I am the CLIENT: I decide product requirements, priorities, and reserved external permissions. First reconstruct the actual repository and applicable protocols; do not invent state. Define capability boundaries and charters. Assign tactical execution, debugging, and recovery to I3, within authorization. Do not transfer routine Git, testing, source-currentness, or engineering-recovery decisions to me. Clearly distinguish what is verified, what remains unknown, and what product choice requires my answer.

This is a role entry point, not an override for `AGENTS.md`, the current requirements, or an already authorized campaign. A fresh session still needs to read the canonical surfaces. A role title grants no additional filesystem or provider permission by itself.

## 3. Discovery: ask the right questions

Begin by identifying the user and the problem, not by proposing a technology stack. Ask for complete user journeys, the information that must persist, important error cases, connectivity, exposure to the public Internet, personal-data sensitivity, cost constraints, dates, accessibility expectations, and explicit exclusions. An effective Planner can group three to seven related product questions at a time, then return a coherent summary for correction.

Questions should affect meaningful product behavior:

| Useful question for the CLIENT | Technical decision engineering should own |
| --- | --- |
| Who uses the system, on what devices and from where? | Ports, server topology, UI framework, and deployment mechanics. |
| What happens to payment history when a club member is deactivated? | Data schema, foreign keys, migrations, and transactional operations. |
| Are online payments part of the first version? | Payment-provider design, subject to separate authorization for spending and handling real transactions. |
| What usable result matters before the target date? | Internal task order, test implementation, checkpoints, and code organization. |
| Should more than one staff member edit a record simultaneously? | Concurrency strategy and conflict handling consistent with the requirement. |

At the end of discovery, present one product baseline that the CLIENT can verify: functions, user flow, data rules, nonfunctional quality, security and network exposure, interface behavior, backups and recovery needs, costs, dates, exclusions, and open questions. A CLIENT confirmation is not a legal signature or a guarantee that requirements will never change. It establishes a traceable current decision that later revisions must explicitly supersede.

Avoid pushing purely technical uncertainty onto the user. “Which database should I choose?” is usually not a product question. “Can staff lose the last hour of payments after a power cut?” absolutely is, because the answer constrains technical recovery design. The Planner should translate technical tradeoffs into their impact on the user before requesting a reserved decision.

## 4. Technical baseline and delivery plan

After confirming product intent, the Planner chooses or confirms a technical strategy against the actual code and constraints. It covers language and framework, persistence, schema changes, deployment, secrets, access control, testing, UI integration, backups, and recovery. In an installed control layer, current technical choices belong in `state/TECHNICAL_BASELINE_CURRENT.json`, not solely in a conversational recommendation.

The delivery plan records milestones with observable completion conditions, target dates, dependencies, confidence, risks, and next review dates. A revised date must be traceable; silently overwriting an old promised date erases information necessary to reason about delivery. A checklist of programming tasks without dates or user-visible outcomes is not an adequate delivery plan.

The starter contains `tools/baseline_guard.py`, which checks whether the material prerequisites for a campaign are coherent. It must not be bypassed by writing invented requirements or status fields. A campaign should remain blocked if the CLIENT has not confirmed its product baseline, if a material security or network decision is unresolved, or if source/authority state is contradictory.

The Planner should also examine how the capability will actually be executed. A charter explaining only “implement member management” may be strategically meaningful but too vague for a long-running, costly controller. The [outcome-first execution contract](../../../44_OUTCOME_FIRST_AGENT_EXECUTION.md) introduces a bounded work order for multi-operation, paid, batch, or substantial-runtime campaigns. The charter establishes what and why; the work order ties the known inputs to an executable method, a budget, concrete output, stop conditions, and physical evidence. It is **not** a second campaign.

The portable `tools/work_order_guard.py` can `validate` a work-order contract and `assess` progress receipts. Its assessment is a decision aid, not a physical or perceptual acceptance gate and not authorization for a vendor API. A report saying “review-ready” does not establish that the product is usable. If a deterministic file operation can be done with filesystem tools, there is no reason to require paid model evaluation for every file.

## 5. Adoption: connect the starter to reality

The adopted state must describe the actual application. The reproducible workflow begins with the scaffold, a source inventory, a reviewed adoption specification, preflight on a temporary control copy, and a journaled promotion of coherent records. `discover_project.py` collects file metadata and hashes; it does not decide the product's purpose. `apply_adoption.py` materializes decisions and verified facts described by the adoption specification; it cannot discover missing user intent by itself.

The adopted result should connect current requirements, source references, technical baseline, Product State, bootstrap context, owner registry, and any project overlay. Where a DB or SQLite WAL witness matters, its state and reference must be consistent. An existing campaign must not be reset or silently replaced to simplify adoption. In a project with an established canonical control layer, use the [read-only governed-project preflight](../../../32_EXISTING_GOVERNED_ATTACHMENT.md). Generic reinstallation is not a v1.2/v1.3 upgrade mechanism.

If the Planner has read-only remote visibility while the I3 controller has an authorized local checkout, the Planner can prepare one complete execution dispatch. The CLIENT should not have to hand-edit ownership registers, reconcile current SHA values, or assemble fragments of JSON. The executor works from the exact source and reports physical results. The original application's source, history, data, and workflows must be preserved unless an independently justified and authorized change is within scope.

The adoption report should answer five concrete questions:

1. Which repository and source version were actually inspected?
2. Which requirements and decisions did the CLIENT confirm?
3. Which current technical state, owners, and control records were materialized?
4. Which validations were physically executed, with what result?
5. Which unknown, HOLD, or first permitted work boundary remains?

If the answer is only “files installed” or “all green,” the transition is not yet demonstrated. The tools are scaffolding for truthful control state, not a way to impersonate genuine product evidence.

## 6. The real examination: a fresh context

Open a genuinely new working context, with no hidden reliance on the previous conversation's narrative. Give it the repository identity, authorized read access, and the normal entry instructions. Ask it to reconstruct its role and limits, current requirements, source ref, Product State, active campaign and checkpoint if any, open acceptance gate, best evidence, unresolved unknowns, next allowed action, and prohibited actions.

A successful answer must cite current durable sources. Merely repeating the conceptual architecture from memory fails the point of the test. It also fails if the new worker treats a superseded document as current, invents DB state, confuses an executor PASS with final acceptance, or asks the CLIENT to fix a technical currentness conflict the system's owner should resolve.

If access to the repo was missing, classify it as an access problem and repair it within authorization. If the repository's own records contradict one another, identify the canonical owner and repair the durable source or currentness mechanism. Do not “pass” the test by handing the new chat a longer summary of the old conversation. The independent reconstruction method is explained in the [fresh-context test](../../../07_FRESH_CONTEXT_TEST.md) and [fresh-context probe prompt](../../../../prompts/FRESH_CONTEXT_PROBE.md).

## 7. The first authorized engineering campaign

Choose a capability that can be implemented and evaluated end to end. Its charter should state the product result, dependencies, ownership, affected interfaces, interfering resources, relevant gate types, evidence expectations, and conditions that would falsify acceptance or invalidate the charter. It should not prescribe twenty tiny commits or how many retries I3 may need for ordinary defects.

Do not equate “the control layer validates” with “the member can register and recover a payment.” The first is a framework-contract check; the second needs application integration, persistence, behavior, possibly security and usability evidence. A sensible charter distinguishes unit, integration, DB/currentness, semantic/generalization, physical, perceptual/human, and release gates according to the real risks. Passing one does not silently cover the others.

Once authorized, I3 owns implementation and in-scope rework continuously. Code defects, failed tests, reviewer findings, retries, internal refactors, migrations within the envelope, and recovery are not reasons to send every iteration back to the Planner. A material change in product intent, authority, critical interface, or strategic scope may invalidate the charter; that is a different event from a form validation bug.

## 8. An example first Planner session

Use a short, outcome-focused opening request, without asserting that adoption is complete:

> I want an application to register club members and dues. Before planning implementation, inspect my actual application repository and the ArquitecturaRepo starter in read-only mode. Guide me through product decisions that remain open. Separate confirmed choices from assumptions; do not fabricate application or infrastructure facts. Prepare one product baseline for my review. Once I confirm it, select the justified profile and technical strategy, produce a dated delivery plan, and arrange adoption. Do not launch material implementation while baseline and continuity gates remain unsatisfied.

The Planner should inspect existing files, branches, and state before asking questions it can answer by reading. It may ask how many people will use the system, where they work, what historical payments must be retained, or how a late payment differs from a cancelled one. Each clarification should change the product contract or a significant constraint, not merely extend the conversation.

## 9. A baseline the CLIENT can actually confirm

“Build a professional CRUD” is not a reviewable product baseline. A compact example can be much more precise:

| Dimension | Proposed first-version requirement | Decision status |
| --- | --- | --- |
| Primary user | One administrative worker on a club computer. | Awaiting CLIENT confirmation. |
| Data | Members, dues status, payment history, activity enrollments. | Awaiting CLIENT confirmation. |
| Retention rule | Deactivating a member must not delete earlier payments. | Awaiting CLIENT confirmation. |
| Member operations | Create, find, edit, deactivate and inspect history. | Awaiting CLIENT confirmation. |
| Security and network | Initially local; no public Internet deployment. | Awaiting CLIENT confirmation. |
| Interface | Readable forms, useful search and understandable errors. | Awaiting CLIENT confirmation. |
| Recovery | Define backup interval and acceptable loss of recent records. | Open product decision. |
| Exclusions | No online payments or mobile application in version one. | Awaiting CLIENT confirmation. |

Only mark a line confirmed when the CLIENT has actually agreed. When the baseline matches their decisions, record the confirmation and its version in the appropriate canonical project state. If the user later changes a requirement, record the supersession and its impact; do not edit away the earlier decision as though it never existed.

The Planner then records technical choices and delivery milestones, including dates, dependencies, acceptance evidence, confidence, and risk. Those technical decisions should be justified by this product, not by fashionable stacks or whichever language an assistant happens to prefer.

## 10. An example of a first campaign

The first club campaign could be: *Create, find, edit, and deactivate members while preserving historical payments and showing clear errors for invalid input.* The result can be demonstrated in a running application and verified against persistent state. The charter identifies its product boundary, data rules, dependencies, and relevant gates; it need not dictate every file or every terminal command to the executor.

I3 receives that authorized result and current source. It implements, tests, reviews, integrates, and repairs defects inside the campaign. If the form rejects a valid phone number, I3 fixes and retests it. If the CLIENT instead changes the product to serve hundreds of clubs over the public Internet, the product requirement and architectural consequences belong back with the CLIENT and Planner before strategic rerouting.

At the end, the candidate is identified by source and evidence. The Planner can assess technical and strategic gates, and the CLIENT can exercise the actual member journey and accept or reject the reserved perceptual/product aspects. A successful test fixture does not replace either real runtime evidence or the CLIENT's experience.

**Next:** Chapter 03, Daily Operation.

## Sources and applicability

- [Product discovery, requirements and delivery](../../../21_PRODUCT_DISCOVERY_REQUIREMENTS_STACK_AND_DELIVERY.md)
- [Installation and adaptation prompt](../../../../prompts/INSTALL_THIS_SDLC.md)
- [Product discovery session prompt](../../../../prompts/PRODUCT_DISCOVERY_SESSION.md)
- [Fresh-context probe](../../../../prompts/FRESH_CONTEXT_PROBE.md)
- [Fresh-context test](../../../07_FRESH_CONTEXT_TEST.md)
- [Transfer/adoption contract](../../../16_TRANSFER_ADOPTION.md)
- [Existing-governance attachment](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)
- [Outcome-first execution work orders](../../../44_OUTCOME_FIRST_AGENT_EXECUTION.md)
- [Planner operating protocol](../../../../protocols/PLANNER_KERNEL.md)
- [Baseline guard source](../../../../tools/baseline_guard.py)
- [Work-order guard source](../../../../tools/work_order_guard.py)

The examples describe synthetic club records. None is evidence that a particular target repository has been inspected, adopted, or accepted.
