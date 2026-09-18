# Prompt — Install This Agentic SDLC Into My Project

Copy/paste the prompt below into an agent that can inspect and write the target project.

---

You are responsible for adapting the Agentic SDLC starter in this repository to my real software project.

Do not merely copy filenames or create governance documents. Reconstruct the target project and instantiate the smallest architecture that physically supports durable agentic development.

Read the starter root `AGENTS.md` and the applicable protocols first.

Goal:
Create a project-specific SDLC where the human can remain primarily a CLIENT/product owner and the agent organization owns technical continuation.

Required approach:

0. Select the minimum sufficient operating profile using:
   - `docs/05_MINIMUM_VIABLE_PROFILE.md`
   - `docs/06_SCALING_PROFILES.md`
   - `docs/09_ADAPTATION_DECISION_TREE.md`
   Do not install mature-system complexity that the target does not need.
1. Perform read-only discovery of the target repository/repositories, branches, code, DB/state, tests, CI/runtime/deployment, current documentation, artifacts and existing agent instructions.
2. Reconstruct the final client-visible product and current physical implementation before designing governance.
3. Ask me only high-leverage CLIENT questions that materially change product/business/preference/external authority. Do not ask me to debug, choose routine architecture, reconcile technical state, schedule agents or interpret ordinary tests.
4. Run `prompts/PRODUCT_DISCOVERY_SESSION.md` when the product baseline is not already physically established. Conduct real product discovery before material implementation.
5. Create normalized current CLIENT requirements and Product State using the starter templates, adapted rather than copied blindly.
6. Present the complete current functional/non-functional/security/network/UI/data/cost/date/exclusion baseline to the CLIENT and obtain one explicit non-legal baseline confirmation.
7. Create a persistent technical baseline / stack frame including machine/environment constraints, stack, DB/state, security, networking, deployment, UI quality, operations/recovery and recurring-cost assumptions.
8. Create a dated delivery plan with milestone outcomes, target dates, dependencies, confidence, risks and next review date.
9. Create one project/workstream overlay from `templates/PROJECT_OVERLAY.md` containing only product-specific theory, owners, state semantics, gates and platform constraints.
10. Define the exact product/workstream topology and role instances. Use the four-role model, but do not activate a separate MASTER OWNER for a small project unless a real systemic/shared boundary exists.
11. If actor/run distinction or concurrent mutation matters, instantiate the identity registry and execution-authority contracts. Do not infer authority from chat identity, model name or Git author.
12. Define one Currentness Set and one canonical owner per concern. Remove, supersede or fail-close duplicate/stale current authorities rather than adding another tracker.
13. Build a product-backward capability map from final product to current physical state.
14. If persistent state exists, define canonical fact ownership, current/history semantics, transactions/single-writer behavior, idempotency, migration/recovery, lineage and invalidation.
15. Define campaign, execution, recovery, review and evidence mechanisms at the smallest sufficient complexity. Use the provided schemas where machine-readable state adds real value.
16. Before creating the first Engineering Campaign Charter, run the project baseline guard when present. Do not bypass a blocked baseline. Create the charter only after the strategic boundary is coherent. Planner owns the envelope; Campaign Lead owns the tactical DAG.
17. Run `prompts/FRESH_CONTEXT_PROBE.md` in a genuinely fresh context. Do not provide a narrative handoff. The new agent must recover role, authority, client intent, Product State, active campaign/gate/evidence, next legal action and forbidden actions from durable state.
18. Classify mechanisms as DECLARED_ONLY, MATERIALIZED, PHYSICALLY_EXERCISED or ACCEPTED_CAPABILITY. Do not claim installation success merely because files exist.
19. Persist `templates/INSTALLATION_REPORT.md` with:
    - selected profile;
    - what was actually installed;
    - canonical owners;
    - Currentness Set;
    - role/authority instances;
    - mechanisms intentionally omitted;
    - fresh-context result;
    - open HOLDs/falsifiers;
    - first legal campaign boundary.
20. Run the starter/project validation available in the fork and fix structural/currentness defects before large implementation work.

Constraints:

- physical/live evidence outranks memory;
- no worker self-report as acceptance;
- distinct verification gates remain distinct;
- no fixed agent count;
- Planner owns strategy, Campaign Lead owns tactics;
- ordinary in-charter defects remain in the same campaign;
- campaign identity survives model/session interruption;
- material CLIENT decisions from conversation must become durable state;
- do not expose secrets, personal data or private machine data;
- shared mechanisms must not import volatile state from another product/workstream;
- governance must pay rent: every permanent mechanism must map to a real failure class.

Do not start a large implementation campaign until currentness/reconstruction and the first charter boundary are coherent.
