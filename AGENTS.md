# Agentic SDLC Starter — Root Agent Instructions

Status: public starter root policy.

This repository is an architecture template. Do not treat its example state as the truth of the target project.

## Mission

Adapt this starter into a project-specific Agentic SDLC where:

- the CLIENT owns product intent, preferences and reserved external authority;
- the system owns technical continuation;
- durable repository state replaces chat memory as authority;
- strategic planning and tactical execution are separate;
- evidence, currentness and recovery are first-class.

## Role topology

Exactly four first-class internal role classes:

`I1 MASTER OWNER -> I2 PROJECT/WORKSTREAM PLANNER -> I3 ENGINEERING CAMPAIGN LEAD -> I4 EXECUTION TEAM MEMBER`.

The CLIENT is external.

I1 is optional as a separately active role for small single-project installations. Reviewers, architects, researchers and specialists are bounded I4 subroles unless the adapted project physically requires another independently planned project/workstream boundary.

## Read order

Before material adaptation or planning:

1. `protocols/AUTHORITY_MODEL.md`
2. `protocols/CLIENT_BOUNDARY.md`
3. `protocols/IDENTITY_AND_EXECUTION_AUTHORITY.md`
4. `protocols/CURRENTNESS_RECONSTRUCTION.md`
5. `protocols/REPOSITORY_EFFICIENCY_AND_WORKSPACE_HYGIENE.md`
6. `protocols/PRODUCT_DISCOVERY_REQUIREMENTS_AND_TECHNICAL_BASELINE.md`
7. `protocols/PLANNER_KERNEL.md`
8. `protocols/CAMPAIGN_CHARTER_STANDARD.md`
9. `protocols/EXECUTION_TEAM_OS.md`
10. `protocols/PRODUCT_MODEL_AND_THEORY_LOADING.md`
11. `protocols/CAPABILITY_DAG_AND_ISOLATION.md`
12. `protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md`
13. `protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md`
14. load optional modules only when the selected profile requires them:
   - `protocols/MASTER_OWNER_OS.md`
   - `protocols/STATE_DB_LINEAGE_AND_IDEMPOTENCY.md`
   - `protocols/STORAGE_AND_ARTIFACT_LIFECYCLE.md`
   - `protocols/CAPACITY_DEADLINES_AND_RESUME.md`
   - `protocols/COST_CAPACITY_AND_EXTERNAL_SERVICES.md`
   - `protocols/SECURITY_PRIVACY_RIGHTS_AND_EXTERNAL_ACTIONS.md`
   - `protocols/SYSTEMIC_ESCALATION_AND_ANTI_CHURN.md`
   - `protocols/INTERACTION_LEDGER.md`
15. target-project current requirements/state/technical baseline/delivery plan/code/evidence.

For installation, follow `prompts/INSTALL_THIS_SDLC.md`.

## Evidence precedence

For technical/project truth:

`physical/live evidence > current canonical state > accepted current requirements > current campaign authority > code/tests/config > historical reports > chat/memory`.

Product intent is different: newer explicit CLIENT authority can supersede older normalized requirements and must then be persisted.

Missing evidence is UNKNOWN, not PASS.

## Adaptation rule

Do not mechanically copy project-specific rules from another system.

Extract the mechanism, then instantiate it for the target:

- product topology;
- authority owners;
- client requirements;
- Product State;
- currentness set;
- identity/execution authority;
- capability graph;
- campaign state;
- gates/evidence;
- runtime/resource constraints.

Keep the smallest mechanism that is sufficient.

## Client boundary

Ask the CLIENT when the missing decision is genuinely product/business/preference/external authority.

Do not ask the CLIENT to debug implementation, select ordinary architecture, reconcile stale technical state, schedule helpers, choose retries, interpret routine tests or integrate branches.

Persist material client decisions that change product intent.

Before the first material campaign in a newly baselined project, the Planner must complete product discovery, obtain an explicit non-legal CLIENT baseline confirmation, persist the technical stack/security/network/deployment baseline, and create a dated delivery plan. The CLIENT confirms product requirements; the Planner owns technical choices.

## Campaign rule

The Planner emits strategic capability charters.

Inside a valid charter, I3 owns implementation, tactical decomposition, retries, in-scope refactors/migrations, tests, independent review, integration, hardening, checkpoints and recovery.

Do not create a new Planner pass/campaign because an ordinary test, reviewer or implementation attempt failed.

Canonical Git history is not a worker activity log. I4 workers do not create canonical commits by default; I3/controller integrates causally complete candidates. A tactical assignment/test/retry is not itself a commit boundary.

When a trustworthy clone and known baseline already exist, refresh remote currentness delta-first with an exact branch fetch. Do not default to git pull, reclone, or full-repository reread after every bounded change.

## Acceptance rule

A report saying PASS is never enough by itself.

Bind acceptance to exact candidate/code/state/evidence and the applicable gate.

For material mutable candidates, use an exact review freeze and fresh independent review after material producer mutation.

## Fresh-context criterion

Before claiming the adapted SDLC is installed, a fresh agent should be able to reconstruct:

- its role and non-role;
- actor/run/execution authority when used;
- current client intent/requirements;
- product objective;
- current Product State;
- requirements-baseline confirmation state;
- current technical stack/security/network/deployment baseline when present;
- target release/milestones/next schedule review when present;
- current code/state authority;
- active campaign/checkpoint if any;
- current hard gate;
- strongest evidence;
- next legal and forbidden actions;

without requiring chat archaeology or technical rescue from the CLIENT.
