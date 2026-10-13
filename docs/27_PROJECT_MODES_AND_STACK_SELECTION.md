# v1.2 — Operating modes, project discovery, stacks, agents and extensions

Status: selectable planning configurations, NOT proof that the agent host/scheduler or a specific model is operational. This document extends existing profile selection, theory loading, planner kernel, technical baseline and runtime; it does not create a new SDLC or new Current owner.

## 1. Orthogonal setup dimensions

Profile (existing): SMALL, STATEFUL, ARTIFACT_HEAVY, MULTI_WORKSTREAM, MULTI_PRODUCT, HIGH_CONSEQUENCE.

- Execution: SYNCHRONOUS (interactive, per-invocation, no background promise); ASYNCHRONOUS (authorized real scheduler/Goal host, durable resumable checkpoints); HYBRID (human checkpoints + independently scheduled legal work). Declared async/hybrid must HOLD without actual host/scheduler/currentness/quotas proved.
- Collaboration: SOLO vs TEAM. TEAM is independent of execution; requires contributors' human/agent identities, least-privilege access, ownership matrix, handoff protocol, reviewer independence, single integrator, concurrency isolation and protected resource/DB locks/fencing.
- Work scope: SOFTWARE, NON_CODE_AI (research, analysis, written operations, media or data curation), MIXED. NON_CODE_AI requires provenance, permissions and independently applicable review/human gates rather than software build checks alone.
- Project category: CRUD, API, WEB_APP, MOBILE, DESKTOP, CLI, DATA_PIPELINE, AI_ML, AUTOMATION, GAME, MEDIA_PIPELINE, INFRASTRUCTURE, RESEARCH, OTHER.
- Risk: LOW/MEDIUM/HIGH. Risk controls are additive and cannot be switched off through mode selection.
- Platform: WINDOWS, LINUX, MACOS, OTHER. Portable Python scripts are not physical validation of Windows Codex Desktop, GitHub scheduler, launch agents or cross-platform filesystem behavior.

Combinations are legal only if every material gate is verified. See \`tools/project_setup.py\` and \`schemas/operating-preferences.schema.json\`. The installed \`configuration/OPERATING_PREFERENCES.json\` is a setup preference, NOT a second canonical Product State or permission to spawn agents. In particular, the default SMALL + SYNCHRONOUS + SOLO + SOFTWARE remains lightweight.

## 2. Actual end-to-end engineering

Product discovery -> CLIENT baseline -> domain evidence/theory -> analysis -> design and architecture -> capability DAG -> charter -> I3 tactical planning -> implementation -> tests and debugging -> exact-candidate independent review -> integration -> deployment (if authorized) -> monitoring and maintenance -> evidence-backed feedback.

Keep software product evidence, non-code domain/perceptual evidence, privacy/security, release authorization and subjective CLIENT approval as distinct gates. Planning is iterative; new requirements can supersede earlier versions only after canonical reconciliation.

## 3. Technology assessment

Before recommending a technology stack, I2 reconstructs existing code and deployment and records a technical baseline covering:

| Concern | Trade-offs to evaluate (examples, NOT required stack) |
|---|---|
| Languages | Python, Java, TypeScript/JavaScript, Go, C#, Rust, Kotlin, Swift and existing installed runtimes; portability/skills/maintenance |
| Backend | Spring Boot, FastAPI, Django, .NET, Express/NestJS, Go services; type safety, complexity, licensing and testability |
| Frontend | static/server-rendered, React/Vue/Svelte, native UI, Android/iOS; accessibility and device support |
| Databases | SQLite, PostgreSQL, MySQL, MongoDB, cloud stores; migrations, backups, queries and concurrent writers |
| Infrastructure | local CLI/Windows service/Linux systemd/macOS launchd, Docker/Compose, CI, cloud orchestration; auth, networks, cost and rollback |
| Tests | unit/property, API and DB integration, E2E, performance/fuzz, accessibility, physical/semantic acceptance |
| AI interfaces | direct API, local models, optional MCP/plugin adapter, bounded I4 review; model cost, data policy, reproducibility and permission |
| Toolchain | Git, code formatters, type checks, CI, package managers, vulnerability scans, secret scans and reproducible builds |

A tiny CRUD should not receive a full microservice architecture; a distributed app, AI service or rights-sensitive pipeline may need deeper state/lineage/security controls. Stack suggestions are **non-authoritative** until I2 documents and validates the decision in \`state/TECHNICAL_BASELINE_CURRENT.json\`.

## 4. Model, plugin and agent policy

Start evaluation with current OpenAI models when beneficial for coding, architecture, reasoning and tool use; choose based on live availability and validated quality/cost/privacy, not a fixed marketing model name. Compare Gemini, other provider APIs and local/open models on the same tasks. A source-of-truth model is never inferred from brand, chat, Git author or token usage.

Extensions are least-privilege opt-in: declare purpose, read/write scope, data exported, permission owner, credentials/rotation, sandbox, call budget, concurrency, reversibility and test/falsifiers. MCP/plugin installation and external calls require explicit authorization. Read-only advice does not certify its own correctness. Do not use a separate paid LLM supervisor by default.

## 5. Diagnostics and misconfiguration

Common failure families: untrusted or stale context, contradictory product requirements, absent canonical DB, duplicate/wrong owner, stale write lease, impossible dependency DAG, circular retries, agent fabricated PASS, source/prompt injection, repeated evaluator failure, private-data leak, unexpected paid API, misconfigured environment/python/ports/network/firewall, invalid model names/quota, missing GUI/headless/Windows adapters, accidental commit/branch/worktree accumulation.

Observe and classify with fixed categories. On a material defect, stop affected work, capture minimal evidence, identify causal owner, correct within same charter if legal, independently re-evaluate, and update canonical state. Never turn event count or error words into a causal claim or create a new campaign for every error.

## 6. Environments and modes in combination

\`ASYNCHRONOUS+TEAM+NON_CODE_AI\`, \`HYBRID+TEAM+MIXED\`, and other combinations are representable. They are not *ready* until real scheduler, Goal continuity, cross-agent identities, resource fencing, rights and human acceptance are proven. Use synthetic mode tests first, one disposable physical host pilot next; Windows/Linux/macOS adoption later. No speculative auto-restart or destructive cleanup.

## 7. Repository theory and Git hygiene

CLIENT intent and meaning go into existing canonical requirements, Product State and domain overlay, with L0 interaction lineage for material changes. Restructure sections and archive obsolete theory as desired, but never discard evidence or leave duplicated current policies. I2 reconciles material contradictions before dispatch. I3 owns implementation, retries and candidate integration. Commit and branch mania are prohibited; create a branch only for justified isolation, hotfix or release, never for each task or agent invocation.

The optional `tools/branch_guard.py` is a pure decision aid: it can classify a branch reason and its affected surfaces, but it never moves Git refs or gives itself I3 merge authority. Actual isolated branch creation requires live exact HEAD, conflict and cleanup review.
