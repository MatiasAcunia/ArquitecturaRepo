# ArquitecturaRepo — v1.4 candidate: start here and actual support

Status: **unreleased integration candidate**. The stable public release remains
[v1.3.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.3.0).
This guide describes the v1.4 candidate's observed portable capabilities, not
permission to publish it or to execute an autonomous project.

## What this gives you

ArquitecturaRepo installs a repository-local development control layer. It
organizes product requirements, who may make decisions, source/state
currentness, engineering campaigns, evidence and recovery. It is useful with
humans and optional AI agents, but installing it **does not** select a model,
grant filesystem authority, connect your cloud accounts or make your app.

The source repository and the application you want to build are separate.
Your application may stay private; this framework does not need to publish
its source or copy your database into the starter.

## Path A — a new project or an existing app without governance

Open a terminal in a checked-out ArquitecturaRepo source directory. Start with
the proportional `SMALL` profile and explicitly disable the optional feedback
scheduler. From Bash:

```bash
python "tools/scaffold_project.py" --target "../mi-proyecto" --profile SMALL --product-id MI_PROYECTO --objective "Objetivo inicial, pendiente de confirmación" --language es --no-feedback-workflow
```

From PowerShell:

```powershell
python "tools\scaffold_project.py" --target "..\mi-proyecto" --profile "SMALL" --product-id "MI_PROYECTO" --objective "Objetivo inicial, pendiente de confirmación" --language "es" --no-feedback-workflow
```

The installer prints the exact read-only commands for your chosen target. It
creates a separate `.agentic-sdlc/` control layer without rewriting application
source or existing workflows. If it detects a preexisting canonical control
layer, it refuses to overwrite it.

From **inside the target application directory**, run:

```bash
python -m pip install -r ".agentic-sdlc/requirements-validation.txt"
python ".agentic-sdlc/tools/project_status.py" --control-root ".agentic-sdlc"
python ".agentic-sdlc/tools/discover_project.py" --project-root "."
python ".agentic-sdlc/tools/reconstruct_context.py" --root ".agentic-sdlc"
```

On Windows PowerShell:

```powershell
python -m pip install -r ".agentic-sdlc\requirements-validation.txt"
python ".agentic-sdlc\tools\project_status.py" --control-root ".agentic-sdlc"
python ".agentic-sdlc\tools\discover_project.py" --project-root "."
python ".agentic-sdlc\tools\reconstruct_context.py" --root ".agentic-sdlc"
```

Python 3.12 is the CI-tested interpreter; dependency
installation is local and explicit. Discovery inventories file metadata and
hashes without copying source content. It refuses linked files/folders outside
the target project and linked output destinations.

The initial `HOLD / UNTRUSTED_CONTEXT` is **correct**. A real Planner must
confirm the product requirements and source/technical baseline, prepare the
explicit [adoption specification](16_TRANSFER_ADOPTION.md) and pass its gates.
No material campaign becomes authorized just because installation succeeded.

## Path B — your project already has canonical governance

Do **not** run the generic scaffold over it. In particular, don't replace
an active v1.2/v1.3 Product State, actor/lease, Goal/Plan, database or workflow
with another copy. Use the [read-only existing-governance attachment
preflight](32_EXISTING_GOVERNED_ATTACHMENT.md), preserving exact source refs
and a transactionally consistent SQLite WAL witness where applicable. This
can verify attachment references, but is **not** a general automatic
in-place upgrader and does not authorize new execution.

## Supported portable scope and boundaries

| Capability | What has been verified / limit |
| --- | --- |
| Scaffold | Six profiles and first-time CLI on CI Linux/Windows; `SMALL` is a minimal, no-runtime install. |
| New or ungoverned source | Existing user code/workflow bytes preserved; second-control and overwrite attempts rejected. |
| Governed source | Read-only reference/SQLite currentness preflight with negative tests. No automatic v1.2/v1.3 migration. |
| Status and continuity | Installed status, inventory, source-bound fresh-context reconstruction and explicit HOLDs. |
| Campaigns and Goal/Plan | Optional portable runtime; source/actor/run/lease and recovery tests use synthetic authorized fixtures. No native Codex Desktop promise. |
| DB/recovery/GC | SQLite WAL, journal, idempotent effect and artifact ownership tests; production DB or host behavior is not certified by these fixtures. |
| Models and plugins | Model-neutral portable source; external models, billed API, cloud credentials, automatic scheduling and native host integrations are not included/verified by default. |
| Feedback privacy | Local strict-metadata report configuration is enabled by default. `--no-feedback-workflow` disables the scheduler, **not** the local report generator; set `enabled=false` in the generated feedback configuration to disable all reporting. No collector endpoint is bundled. |
| Public distribution | Current-tree source archive and install readback are exercised on Linux/Windows. No v1.4 published ZIP or container has been released yet. |
| Human usability | Runnable setup/docs and error/negative paths have deterministic coverage; independent external-user comprehension or taste approval is **not** established by automation. |

## Troubleshooting and safe recovery

- `UNTRUSTED_CONTEXT` after first installation: expected. Reconstruct the
  real source and obtain explicit product-baseline confirmation; never
  change a status field merely to get a green command.
- Missing `jsonschema`: install the declared dependency from the generated
  `requirements-validation.txt` and rerun validation/reconstruction.
- `EXISTING_CONTROL_PRESERVED` or a canonical Product State conflict: stop.
  Choose Path B; do not pass a force flag or delete the old state.
- A stale Git/DB/authority witness: HOLD material writes until the source,
  owners, WAL snapshot and current records are independently reconciled.
- A failed or interrupted campaign: retain its journal and current owner;
  recover within the same authorized campaign, not by reinstalling.

## Public distribution and release truth

The portable archive is built from Git-tracked bytes, never untracked local
workspace files. Automated structure/privacy checks reject embedded private
keys, obvious credentials, personally identifying email addresses and named
private workstreams in public policy; the archive also rejects retired private
documents, credential/database paths and symlinks. The author/license and
public repository URL are intentionally public identifiers. Every artifact
must be rechecked from its **exact** source commit at release.

These checks cover the **current candidate tree**. Deleting a file from a
public Git tree does not erase it from older commits, forks or caches; any
actual historical disclosure requires a separately assessed remediation, not
an automatic history rewrite. No history-wide confidentiality audit or
published-v1.4 artifact inspection is claimed here.

Only an explicit CLIENT-approved E6 can merge, tag `v1.4.0`, publish the
portable archive/checksum and independently inspect the downloadable bytes.
