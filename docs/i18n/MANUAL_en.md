# ArquitecturaRepo — Practical v1.4.0 manual (English)

This is an actionable eight-topic (00–07) guide for adopting **v1.4.0** in your own project. It is **not** a full translation of the archived v1.3 Spanish manual. Historical chapters remain in the source repository under `docs/manual/ES/`. Release claims refer to the verified, immutable [v1.4.0 GitHub Release](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0); v1.3.0 remains available as the previous version.

## 00 · Before starting: purpose and limits

ArquitecturaRepo is a repository-local **development control layer**, not an application generator or a replacement for Codex. It organizes product goals, decisions, ownership, current state, campaigns, evidence, and recovery so a new chat or agent can reconstruct the next permitted action.

- CLIENT decides product intent, sensitive actions, subjective quality, and publication.
- I1 coordinates multiple projects only where that coordination is necessary.
- I2 Planner reconstructs the product and defines capability boundaries and verification gates.
- I3 Controller implements, tests, integrates, debugs, and recovers within the authorized campaign.
- I4 specialists are optional; **four roles do not imply four models or four chats**.

Your application can remain private. The public starter does not need its code, database, credentials, or chat transcripts. Actual privacy also depends on the tools and model providers you separately authorize: installation grants **no** external access or execution authority.

## 01 · Safe installation

Use Python 3.12 (tested in CI). Download the [v1.4.0 portable ZIP](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/download/v1.4.0/ArquitecturaRepo-v1.4.0-portable.zip), verify it against the accompanying published `.sha256`, extract it, and open a terminal in that extracted source directory. You may also check out immutable Git tag `v1.4.0`.

For a new project, or an existing application **without canonical governance**, start with `SMALL`:

```bash
python "tools/scaffold_project.py" --target "../my-project" --profile SMALL --product-id MY_PROJECT --objective "Initial objective, pending confirmation" --language en --no-feedback-workflow
```

Windows PowerShell:

```powershell
python "tools\scaffold_project.py" --target "..\my-project" --profile "SMALL" --product-id "MY_PROJECT" --objective "Initial objective, pending confirmation" --language "en" --no-feedback-workflow
```

The installer adds `.agentic-sdlc/`, preserves existing application code/workflows, and refuses to replace existing canonical control. `--no-feedback-workflow` removes scheduling, **not** the local report generator. To disable all reporting set `enabled=false` in `.agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json`. No external feedback collector is bundled.

Now work **inside the target application directory**:

```bash
python -m pip install -r ".agentic-sdlc/requirements-validation.txt"
python ".agentic-sdlc/tools/project_status.py" --control-root ".agentic-sdlc"
python ".agentic-sdlc/tools/discover_project.py" --project-root "."
python ".agentic-sdlc/tools/reconstruct_context.py" --root ".agentic-sdlc"
```

On Windows PowerShell, use quoted `\` paths instead of `/`. `HOLD / UNTRUSTED_CONTEXT` is an **expected** initial result: the real product baseline and permission to act have not been confirmed yet.

If your project already has a Product State, running campaigns, actor/lease, or controller, **do not scaffold on top of it**. Use the [read-only existing-governance preflight](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/32_EXISTING_GOVERNED_ATTACHMENT.md). There is no automatic universal in-place v1.2/v1.3 migration.

## 02 · The Planner and adoption

Start from real code, requirements, users, data, security constraints, dependencies and delivery needs. The CLIENT confirms the product baseline. I2 then defines a **capability-level** charter: outcome, scope, owners, interfaces, acceptance criteria, hard gates, and falsifiers. It does not prescribe every microtask.

Never copy synthetic sample Product State into a real application or treat a passing scaffold test as permission to run a campaign. Existing governed installations require read-only reconciliation before any separate adoption authorization.

## 03 · Day-to-day operation

Read the current source and canonical state, not only chat history. I3 manages implementation, integration, tests, retries and interrupted-run recovery inside the authorized charter. Bugs and ordinary rework stay within **that same campaign**. Add agents only when separable work and independent evidence make them useful.

Reconstruction must reconcile Git, identity, authority, database currentness and evidence. If a material contradiction cannot be resolved, use `HOLD`. The portable starter does **not** certify native Codex Desktop/Goals actions, external model providers, paid services, or unattended real-world effects.

## 04 · Requesting a change

Specify the observable result, context, constraints, and acceptance test. For example: “Show unpaid monthly membership dues; preserve existing data; accept when calculation and UI match representative paid/late cases.” I2 decides whether the change invalidates strategy or fits existing scope. I3 owns engineering adjustments within that scope.

## 05 · Errors and recovery

- `UNTRUSTED_CONTEXT`: confirm the real source/product; never manually flip status just to obtain a green check.
- Missing `jsonschema`: install dependencies from the generated `requirements-validation.txt`.
- `EXISTING_CONTROL_PRESERVED` or Product State conflict: stop; use read-only attachment, not force or deletion.
- Mismatched Git, SQLite WAL snapshot, actor or lease: hold material actions until exact current evidence is reconciled.
- Interrupted campaign: keep journals, run identity, and artifacts; recover in the same authorized campaign. Clean only files whose ownership and deletion policy are verified.

When filing a public Issue, include steps and **redacted** logs, never project secrets, personal paths, private names, database dumps, confidential requirements or agent transcripts.

## 06 · Capability acceptance

Treat unit, integration, DB/currentness, semantic/generalization, physical, perceptual/human, and release gates **separately**. A green test or a worker's “done” is not the product owner's acceptance. Record exact source, inputs, evidence, responsible actor, and final decision on canonical project surfaces. Synthetic CI does not certify arbitrary production applications.

## 07 · Worked example: membership club

1. CLIENT asks to register members, collect dues and identify unpaid months; confirms expected user-visible behavior.
2. I2 examines the existing repository/data model and permissions, establishes the smallest useful vertical capability and success criteria.
3. I3 implements member creation → monthly fee → outstanding-balance view, tests persistence and reconstructs state.
4. A calculation bug is fixed and retested within **the same** campaign.
5. CLIENT tries the real flow and accepts or returns findings; exact evidence and current decision persist in the repository.

## Links and version boundaries

- [Short guide](README_en.md) · [English FAQ](FAQ_en.md) · [Root README](../../README.md).
- [v1.4 start, supported scope and privacy](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/46_V1_4_PUBLIC_START_AND_SUPPORT.md).
- [Immutable v1.4.0 release](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0).

This guide is not a security certification, independent human usability test, native-host integration claim, or proof that the framework outperforms direct Codex use. The MIT license does not cover third-party materials automatically.
