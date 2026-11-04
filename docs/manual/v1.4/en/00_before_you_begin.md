# 00 — Before You Begin

ArquitecturaRepo · Complete User Manual · v1.4 edition · English

> This chapter explains the product, its limits, and who decides what. It accompanies the [published v1.4.0 release](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0). It is documentation, not evidence that a particular application has been built, secured, or accepted. Commands and compatibility boundaries are checked against the [current first-user guide](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md) and [release notes](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md).

## In this chapter

1. What you install—and what you do not
2. Who makes each decision
3. What must remain accessible
4. How to use this manual
5. The product decisions only you can make
6. Scope, limitations, and versions
7. One complete example, from idea to acceptance
8. Common decisions and their owners
9. A one-page project starter brief
10. How to know whether the framework is helping

## 1. What you install—and what you do not

ArquitecturaRepo is a portable engineering-control starter. It provides public operating protocols, reusable templates, installation profiles, machine-checkable contracts, Python validation and recovery utilities, and an optional local campaign controller. Together these mechanisms organize software development when work passes between people, programming agents, reviewers, and new conversations. They do not constitute a finished product-building service. Installing the starter does not mean an agent can take a broad request and deliver a validated application without further decisions, work, and evidence.

The published version is identified by a specific Git tag and release assets—not by a version string alone. For v1.4.0, the distribution includes a portable ZIP, its checksum, and a manifest. Verify the downloaded bytes before installation. The continuously updated `main` branch can contain documentation fixes that are not part of the already published ZIP. The framework's release is evidence about its own source and tested mechanisms; it says nothing about whether an unrelated application built with it works.

An application needs its own requirements, technical choices, real execution, tests, risk controls, and final acceptance. The repository contains synthetic adoption examples and a physical reference application to exercise selected framework behavior. Such fixtures support the framework's claims but are not a substitute for testing the project you actually want to ship. A capability that has not passed its applicable real-world gate should remain UNKNOWN, HOLD, or explicitly unsupported—not be described as completed because a script or agent predicted success.

The practical benefit is continuity. A new session should be able to inspect durable repository evidence and reconstruct: what is being built, which decisions still apply, which source version and technical state are current, what work is authorized, what was actually tested, and what remains uncertain. Chats can end, accounts or models can change, and an agent may lose its context. Your project should not require someone to remember the entire conversation in order to continue safely.

The manual uses GitHub, Windows, Python, and conversational coding agents in examples because they are familiar starting points. They are not universal dependencies. A project may use another operating system, another programming stack, different tools, or only human workers. External models, cloud services, credentials, and paid provider calls are optional and require separate authorization. Installing ArquitecturaRepo does not grant those permissions.

It is especially important to distinguish three statements:

- The starter is installable and its portable mechanisms pass their own tests.
- Your application has adopted the starter with valid, current authority and state.
- Your application satisfies its functional, security, reliability, and human-experience requirements.

They are separate claims. Passing the first does not imply the second or third.

## 2. Who makes each decision

The framework separates decisions by responsibility, not necessarily by the number of people, AI models, chats, or programs involved. A small project can use one human product owner, one planning role, and one executor. A dedicated Master Owner becomes valuable when multiple products, shared resources, or cross-project policies require separate oversight. Merely creating a chat named “Master Owner” does not establish such a need.

| Role | Owns | Should not routinely do |
| --- | --- | --- |
| CLIENT / product owner | Problem, intended users, priorities, product behavior, subjective quality, spending limits, publication, and other reserved authorizations. | Resolve merge conflicts, hand-edit governance records, design tests, or repair broken currentness. |
| I1 · Master Owner (when needed) | Shared operating system, inter-project coordination, systemic quality, capacity, and ownership boundaries. | Replace the project Planner or control every small task. |
| I2 · Planner | Product interpretation, technical strategy, capability boundaries, architecture, charter acceptance criteria, and strategic acceptance. | Become the debugging loop or rewrite the campaign for every failed test. |
| I3 · Execution Controller / Campaign Lead | Implementation management, debugging, integration, review, retries, checkpoints, and recovery within an authorized campaign. | Invent new product requirements or approve its own work as the final authority. |
| I4 · Execution specialists | Bounded code, research, tests, technical review, and source-linked evidence. | Override product decisions or claim strategic acceptance. |

The product owner can reject an interface that feels confusing even when automated tests pass. A technical reviewer can reject incorrect implementation evidence. The Planner determines whether the authorized capability satisfies its strategic conditions. Those decisions must not silently replace one another.

In one common arrangement, ChatGPT helps the user reason about planning, while Codex edits and tests a repository. That is an example, not a product requirement or a mandatory subscription. A commercial service does not automatically become I2 or I3; those labels describe authority, obligations, and evidence requirements. One person or agent may perform several bounded roles, provided conflicts of interest and independent-review needs are respected.

## 3. What must remain accessible

When learning the real technical state, start with the source and environment that physically exist, then current canonical Product State, confirmed requirements, current campaign authority, DB and artifacts where relevant. A previous chat response—even one stating PASS—is weaker than current physical evidence. On the other hand, a new explicit decision from the CLIENT can change product intent; the system must then record that supersession rather than pretending an older interpretation remains authoritative.

Do not solve contradictory records by choosing whichever filename looks newer. An absent fact is UNKNOWN. A material contradiction between active sources of authority means HOLD for actions that depend on the disputed fact, followed by reconciliation. Read-only investigation can continue while material changes are paused.

The framework distinguishes three broad layers:

1. L0: evidence of what the CLIENT actually requested, clarified, or approved, including later changes.
2. L1: interpreted current requirements, product theory, and canonical Product State.
3. L2: implementation, code, databases, campaigns, checkpoints, reviews, and runtime evidence.

These layers prevent a persuasive conversational summary from being confused with deployed software. They also prevent a document containing a future plan from overriding a later, physically verified implementation result.

At minimum, a fresh worker should reconstruct the product objective, current requirements, verifiable code reference, relevant environment and DB witnesses, active campaign if one exists, open gate, strongest evidence, unresolved unknowns, and next permitted or prohibited action. If this cannot be reconstructed, continuity is not yet demonstrated.

Terms you will encounter throughout the collection:

- **Scaffold:** the generated `.agentic-sdlc/` control layer. Its initial `HOLD / UNTRUSTED_CONTEXT` status is deliberate.
- **Discovery:** a read-only effort to understand the existing product, source, environment, and needs.
- **Adoption:** the reviewed promotion of verified facts and decisions into coherent control state. It is not blind copying from examples.
- **Product State:** the canonical description of the product's currently recognized capabilities and status.
- **Charter:** an authorized strategic contract for an engineering capability, including boundaries and acceptance criteria.
- **Gate:** a defined check that must be satisfied before a particular kind of acceptance. Different risks require different gates.
- **Currentness:** evidence that code, state, authority, and artifacts still refer to the versions actually being used.

## 4. How to use this manual

Read Chapter 01 before a first installation, then Chapter 02 before starting the first material feature. The remaining chapters are references to consult as their operational questions arise. You do not need to memorize eight chapters before trying the SMALL profile in a disposable or ungoverned project.

Each chapter has a different observable outcome:

| Chapter | When to read it | What you should be able to verify |
| --- | --- | --- |
| 00 · Before You Begin | Before installing | You understand the responsibilities, boundaries, and overall lifecycle. |
| 01 · Installation | When preparing a project | An installed, validated control layer exists; no adoption or execution authority is fabricated. |
| 02 · Planner and Adoption | Before the first feature | Requirements, baseline, ownership, and next action can be reconstructed without the previous chat. |
| 03 · Daily Operation | During active engineering | Work is authorized, executed, tested, reviewed, and recorded in the same campaign. |
| 04 · Requesting Changes | When changing product behavior | The request describes observable behavior, priorities, boundaries, and open decisions. |
| 05 · Errors and Recovery | During incidents and uncertain state | Evidence is preserved and further damage is avoided while recovery is verified. |
| 06 · Closing Capabilities | When someone says “done” | The exact candidate and applicable acceptance gates have sufficient evidence. |
| 07 · Worked Club Example | To practice the whole flow | You can follow one member-management capability from requirements to acceptance. |

After Chapter 01, a newly installed control layer may still correctly be on HOLD. After Chapter 02, a genuinely fresh agent should reconstruct the project without relying on the original conversation. After Chapter 06, the accepted candidate should be identifiable, with separate evidence for each applicable gate. If one of these outcomes is missing, return to the step that produces it. The number of documents you read is not itself evidence of installation or progress.

## 5. The product decisions only you can make

Before installing anything, write a short project brief. Explain the real problem, intended user, primary journey, data to be handled, expected usage environment, target date, budget, desired interface quality, and what is explicitly out of scope. If you have not made a decision, label it an open question.

For example:

> I want a local application to register club members and their dues. One administrative worker will use it. The first version will not accept online payments. It must retain payment history. I want a simple readable interface. The budget for paid services is zero.

You do not need to decide whether the implementation should use SQLite or PostgreSQL, how many branches Git needs, which framework to use, or which retry algorithm to implement. Engineering owns those choices, while explaining the consequences of decisions that affect the product or your reserved authority. With personal data, payments, publishing, or external integrations, the team must identify the relevant risks and obtain the permissions that belong to you. Agent involvement does not make consent, lawful processing, or publication rights automatic.

## 6. Scope, limitations, and versions

ArquitecturaRepo publishes reusable mechanisms and synthetic examples. Its transfer and recovery tests do not demonstrate that every application can be safely installed, operated, or shipped. The optional local `campaignctl.py` maintains certain campaign states; by itself it does not launch arbitrary coding agents or certify native Codex Desktop behavior. The public v1.4.0 support matrix distinguishes proven portable behavior from unsupported host-specific claims.

The application, operating system, API price, model name, and UI of a third-party service can change. The manual therefore avoids making them permanent parts of the method. Always compare version-sensitive instructions to the exact release and the current code you actually installed. The original repository code and documentation use the MIT license; third-party dependencies and assets have their own rights and terms.

Git tags are version references, not proof that a hosting service technically enforces immutability. Verify release artifacts against their published digests, and distinguish any newer `main` documentation from the tagged distribution. A verified release does not authorize a new campaign, billable provider call, or product publication.

## 7. One complete example, from idea to acceptance

Imagine an association that wants to register members. The CLIENT decides who may register records, what information is mandatory, and what “deactivate a member” means. The Planner turns those decisions into testable requirements. It must not assume that deactivation means permanent deletion. Before authorizing development, it inspects existing code and state, identifies dependencies, and asks only the product questions that materially change the intended result.

Once the scope is confirmed, the Planner records current requirements, Product State, technical baseline, and a dated delivery plan. It chooses a capability that can be delivered and evaluated end to end. Its charter specifies the outcome, allowed boundaries, dependencies, relevant gates, and conditions that would invalidate the agreement.

The Execution Controller then organizes implementation. It may assign code, tests, review, and integration to specialists, or carry them out directly in a small project. It fixes ordinary defects and reruns relevant tests inside the same authorized campaign. It does not return every bug to the Planner as a new strategic decision. When a meaningful candidate exists, the Planner reviews the independent evidence and the CLIENT assesses reserved product and perceptual matters.

The cycle is not over because a convincing report was written or a large number of commits appeared. It is over only when the requested capability works to the accepted standard and the repository preserves enough current evidence for the next worker to continue. Chapter 07 follows this example in detail with fictional club data.

## 8. Common decisions and their owners

| Situation | Decision and expected evidence |
| --- | --- |
| “Members in arrears cannot enroll in activities.” | CLIENT defines the rule; Planner records the confirmed requirement and its tests. |
| “Should we use SQLite or PostgreSQL?” | Engineering chooses according to the verified usage, concurrency, backups, deployment, and risk. |
| “Can we publish our real member data in a demo?” | CLIENT must authorize any lawful, specific use; the team protects data by default. |
| “A test failed after a correction.” | I3 diagnoses and repairs inside the same charter; evidence is rerun. |
| “I now want the local app to become a public web service.” | CLIENT confirms the product change; Planner reevaluates hosting, access, security, and scope. |
| “The coding agent said everything is ready.” | That statement is not acceptance. Require a source-bound candidate and the relevant technical and human checks. |

## 9. A one-page project starter brief

Keep your first brief compact. A useful version includes:

- **Purpose:** what the first version solves and who will use it.
- **Main journey:** what the user tries to accomplish and how success is visible.
- **Data:** what is stored, whether it is personal, and required retention.
- **Environment:** device, operating conditions, connectivity, and offline needs.
- **Boundaries:** target date, spending limit, approved integrations, and exclusions.
- **Visible quality:** readability, accessibility, error messages, speed, and the experience you care about.

You do not need to prepare a full technical specification. The engineering process should discover the relevant details without inventing your unresolved product decisions. Keep the brief as the input to the conversation and formal adoption in Chapter 02.

## 10. How to know whether it is helping

After two or three delivery cycles, ask for a short demonstration: which new capability can you use, where is the evidence, what changed since the previous cycle, which material risk remains, and what is the next authorized action? If the answer is only “we made many commits,” “we ran more agents,” or “there is more documentation,” the effort has not yet been connected to a product outcome.

An architecture like this can reduce reliance on individual chat histories, but it does not eliminate judgment, security review, or real-world testing. Measure its value through continuity, clear ownership, usable capabilities, credible evidence, and reliable recovery—not the number of protocols or sessions.

**Next:** Chapter 01, Installation.

## Sources and applicability

- [Published v1.4.0 release](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0)
- [Actual public support and first-user installation](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [Release and upgrade boundaries](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md)
- [Architecture overview](../../../00_ARCHITECTURE_OVERVIEW.md)
- [Authority model](../../../../protocols/AUTHORITY_MODEL.md)
- [MIT license](../../../../LICENSE)

This is user guidance about the starter. No example or framework test is a substitute for verifying the adopter's own product.
