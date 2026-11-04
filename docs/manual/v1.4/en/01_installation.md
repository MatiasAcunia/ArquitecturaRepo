# 01 — Installation and Configuration

ArquitecturaRepo · Complete User Manual · v1.4 edition · English

> This chapter covers first-time installation and its boundary with project adoption. Commands follow the [published v1.4.0 instructions](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md). A successful scaffold is **not** evidence that the application has been understood, adopted, implemented, or accepted.

## In this chapter

1. Environment and accounts
2. The starter, the fork, and the application
3. Verify the location before changing anything
4. Select a proportionate profile
5. Generate the control layer
6. Validate without manufacturing acceptance
7. The next action is discovery, not coding
8. Before attempting installation again
9. From scaffold to genuine adoption
10. Connections, access, and privacy
11. Safe troubleshooting

## 1. Environment and accounts

This walkthrough uses Windows, PowerShell, Python, and a local checkout of ArquitecturaRepo. GitHub can host your source; a conversational assistant can help with planning; a coding agent can work inside an authorized checkout. None of these particular commercial services is a universal prerequisite for the architecture. A developer comfortable with Git does not need GitHub Desktop, and a remote coding agent does not require a dedicated GPU in your own computer. You do need enough storage, a reliable way to access source code, and the permissions required by the tools you choose.

First identify the repository that contains the application you intend to develop. A frequent and damaging mistake is to open the framework's own folder in the coding tool and ask it to implement your application's feature there. The framework and the application have separate purposes and should normally have separate repositories. Decide which directory the tool will read and which directory it can modify *before* authorizing any write.

Check Python from PowerShell:

```powershell
& "python" --version
& "py" --version
```

Python 3.12 is the version tested in the v1.4 portable continuous-integration runs. If neither command works, install an appropriate Python build from its official distributor, restart your terminal, and repeat the version check. Do not run an untrusted installer or assume a command worked when it returned a nonzero exit status. The UI location of GitHub, ChatGPT, or a coding tool may change; identify the operation you need rather than relying on the color or position of a particular button.

Protect your accounts. Enable suitable account authentication, work with the least necessary access, and keep tokens, private keys, and connection strings out of prompts and the repository. Connecting a provider to a chat does not prove the assistant has read the correct repository or has permission to operate on the actual application. The presence of a tool is different from authorization to use it.

## 2. The starter, the fork, and the application

Three things are easily confused:

| Location | Purpose | What it must not be mistaken for |
| --- | --- | --- |
| `ArquitecturaRepo/` | The public source, protocols, templates, tools, tests, and documentation used to create a control layer. | Your application's source or Product State. |
| Your optional fork | Your own version of the public starter if you need to maintain custom changes. | A newly created application. |
| `club-app/`, or your real application repository | The actual product, its code and data, and its installed `.agentic-sdlc/` control layer. | A disposable copy of synthetic examples. |

The starter's examples deliberately contain illustrative facts. Copying one of their Product State files into a real application would silently assert made-up code references, requirements, owners, and decisions. Installation therefore creates a cautious initial state rather than declaring a valid adopted project.

A reasonable local directory arrangement is:

```text
C:\Proyectos\
    ArquitecturaRepo\
    club-app\
```

From the source repository, read its [README](../../../../README.md) and [MIT license](../../../../LICENSE). If you want to maintain your own starter variant, fork it; otherwise an ordinary checkout is enough. Create or select the *actual* application separately. A real existing application does not need to be erased and recreated merely to follow this guide. Record the exact version or tag of the starter used for installation, because `main` may subsequently move.

For a source archive, prefer the [v1.4.0 release](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0), which provides the versioned archive and its SHA-256 checksum and manifest. Verify the artifact before using it. A Git tag and a published ZIP are distribution identifiers; they are not permission to run code in a different repository. Be aware that any release notes published after the ZIP was built do not retroactively change the ZIP's contents.

## 3. Verify the location before changing anything

Open a terminal in the starter checkout. These PowerShell commands only inspect your current working location, the available interpreter, and Git state:

```powershell
Get-Location
& "python" --version
& "git" status --short
```

If the Git command reports that no repository exists, investigate the path before proceeding. If it lists local changes, do not discard them simply to imitate a tutorial. Identify their owner and role, and preserve them when relevant. Confirm the target path separately; the scaffold command operates on the path you pass it, not on the application you merely intended.

If using GitHub Desktop, ensure the selected repository is the application when you intend to work on its implementation. If using a coding agent, open the application's exact working directory and give it the starter location as a read-only reference until the installation boundary is clear. The agent may perform installation if authorized, but should first inspect the starter, the destination, and any existing governance in read-only mode.

If the application has history, migrations, live data, existing governance, or an `.agentic-sdlc/` directory, stop and examine its current state. Removing an old checkout or overwriting its control layer can erase the evidence needed for safe recovery. **For an already-governed application, use the [existing-governance attachment preflight](../../../32_EXISTING_GOVERNED_ATTACHMENT.md), not the generic scaffold.** That route is read-only and does not promise an automatic migration from v1.2 or v1.3.

## 4. Select a proportionate profile

Choose the profile by product risk and operating characteristics, not by how many AI agents you hope to use. The framework defines six public profile families in [profiles/profiles.json](../../../../profiles/profiles.json):

| Profile | Choose it when the product has… |
| --- | --- |
| `SMALL` | A simple product boundary without material state or operational risk that requires heavier controls. |
| `STATEFUL` | Persistent data, users, backups, schema changes, recovery, or a runtime whose state matters. |
| `ARTIFACT_HEAVY` | Numerous or costly outputs, lifecycle and lineage requirements, storage pressure, or rights-sensitive artifacts. |
| `MULTI_WORKSTREAM` | Separately planned workstreams contributing to one final product, with integration and interference to coordinate. |
| `MULTI_PRODUCT` | Distinct products sharing resources, policies, or infrastructure; may justify an I1 Master Owner. |
| `HIGH_CONSEQUENCE` | Material consequences for privacy, security, finances, health, integrity, or irreversible external operations. |

`HIGH_CONSEQUENCE` is not a prestige label, and `MULTI_PRODUCT` does not automatically imply you must create many separate agents. The profile selects reusable control families; it does not prove your product's actual risk, create technical evidence, or grant authority to publish, spend, or process personal data. Document why you selected a profile and revise it when verified circumstances change.

The fictional club application used in Chapter 07 is `STATEFUL`: it stores member records, payments, and activity enrollments. It does not thereby need an elaborate Master Owner hierarchy or a large agent fleet. A small version may still have a single human owner and a small engineering arrangement while implementing the state and recovery controls appropriate to its data.

For first exploration in a truly new or ungoverned project, `SMALL` is the recommended baseline. Start with the least complex arrangement that can safely represent the facts and risks. Escalating later should be a reasoned adjustment, not a reaction to the fact that a protocol mentions a more elaborate role.

## 5. Generate the control layer

From the checked-out v1.4 starter, a new project can be scaffolded with the following PowerShell command. Use a destination path you have already verified:

```powershell
& "python" "tools\scaffold_project.py" --target "..\mi-proyecto" --profile "SMALL" --product-id "MI_PROYECTO" --objective "Initial objective, awaiting confirmation" --language "en" --no-feedback-workflow
```

For the fictional club application, a justified stateful choice would look like this:

```powershell
& "python" "tools\scaffold_project.py" --target "..\club-app" --profile "STATEFUL" --product-id "CLUB_MANAGER" --objective "Member and dues management for a club" --language "en" --no-feedback-workflow
```

Do not combine command lines into one and do not paste the line breaks of printed sample layouts into a terminal. The path, objective, product ID, and language are examples to replace when *you* run an installation, not assertions about an actual project.

The installer creates a new repository-local `.agentic-sdlc/` layer in the destination. It does not rewrite existing application source or workflows. It must refuse to overwrite an existing canonical control layer; do not use a force option as an ordinary recovery technique. A second run is not a substitute for understanding a failed first run. If the installer prints the next read-only commands, prefer those commands for the exact target and version you actually used.

The initial status intentionally is `HOLD / UNTRUSTED_CONTEXT`. This means the template does not yet know your code baseline, current Product State, requirements, owners, or active campaign. Editing a status field to `READY` would falsify continuity. There should be no invented project acceptance or authorized coding campaign at this stage.

The optional `--with-runtime` flag adds reference campaign machinery; it does not install an external model, authenticate a provider, start native Codex Desktop jobs, or authorize any work. The optional GitHub Actions feedback scheduler is disabled by `--no-feedback-workflow`; this does **not** disable the local metadata report generator. The report configuration is a separate choice discussed in Section 10.

## 6. Validate without manufacturing acceptance

Move into the target application's directory *after* a successful scaffold. Install the declared local validation dependencies and run the three v1.4 commands:

```powershell
& "python" -m pip install -r ".agentic-sdlc\requirements-validation.txt"
& "python" ".agentic-sdlc\tools\project_status.py" --control-root ".agentic-sdlc"
& "python" ".agentic-sdlc\tools\discover_project.py" --project-root "."
& "python" ".agentic-sdlc\tools\reconstruct_context.py" --root ".agentic-sdlc"
```

The status command reports recognized governance and what remains unresolved. Discovery inventories file metadata and hashes without copying source contents into a remote service; it refuses links outside the intended project and linked destinations used for output. Reconstruction checks whether a fresh worker could recover meaningful, source-bound current state. A failure or HOLD in the last command can be the **correct** result before adoption. It should identify facts that still need confirmation instead of hiding them.

The installed control layer also includes structural validation tools. The portable release guide's three commands are the appropriate starting sequence because they expose currentness and adoption needs, not just well-formed JSON. Tests of control contracts do not demonstrate that the club can register a member, that its database is safe, or that a user will understand its interface.

Confirm three observable facts: `.agentic-sdlc/` exists at the intended target; the application's existing files and workflows remain intact; and the initial status and discovery findings can be read without relying on a chat. Save any error output for diagnosis. A missing dependency such as `jsonschema` is a local environment problem; install the declared requirements rather than altering project records or creating another checkout.

**Completion of this step means “scaffold created and inspected,” not “application adopted.”** The distinction is central to the framework: installation checks the mechanism, while adoption connects that mechanism to the real product.

## 7. The next action is discovery, not coding

After installation, follow [the installation/adaptation prompt](../../../../prompts/INSTALL_THIS_SDLC.md), [product discovery prompt](../../../../prompts/PRODUCT_DISCOVERY_SESSION.md), and the [transfer and adoption contract](../../../16_TRANSFER_ADOPTION.md). If the application already existed, the [reanchoring prompt](../../../../prompts/REANCHOR_EXISTING_PROJECT.md) is relevant. These are source-backed instructions for inspecting the actual project; they are not permission to let an agent make unresolved product decisions.

The Planner should determine what the product currently does, what the CLIENT wants changed, what code and data are current, what environment matters, and which facts require confirmation. A material implementation campaign should wait for an adopted baseline and an explicit charter. Coding immediately after creating the directory skips the step that makes the governance truthful.

## 8. Before attempting installation again

If `.agentic-sdlc/` already exists, inspect it before rerunning anything. It may contain canonical Product State, an active campaign, a lease, current ownership, DB references, or evidence that must survive. A successful-looking second scaffold can still cause serious continuity damage if it replaces such material.

Do not use deletion, force-overwrite, or a fresh repository as a first response to a validation failure. Classify the failure: environment or dependency, path, schema, unsupported compatibility, reference/currentness, or an actual conflicting control layer. Keep the complete error report and ask the responsible engineering owner to correct the cause in place when possible. For a genuinely governed project, the read-only preflight is the default safe path.

## 9. From scaffold to genuine adoption

The transition to an operational control layer has several distinct parts:

1. Inspect the real application and its environment, initially without writing.
2. Ask the CLIENT to confirm or correct the intended user behavior and scope.
3. Record traceable, current requirements and the technical/source baseline.
4. Construct the delivery plan and a concrete adoption specification.
5. Check ownership, files, links, DB state and dependencies in preflight.
6. Promote internally consistent control state using the supported adoption process.
7. Validate the resulting records and reconstruct them in a fresh context.
8. Only then route a materially authorized capability to its engineering owner.

The [adoption guide](../../../16_TRANSFER_ADOPTION.md) explains this boundary. The assistant must not fabricate a JSON baseline, current SHA, active Goal, or approval to make a validator go green. If the necessary fact is a product decision, it belongs to the CLIENT. If it is technical, the appropriate engineering owner must investigate and demonstrate the result. “We are ready” should mean the evidence and authority are reconstructible, not merely that an installation script exited successfully.

## 10. Connections, access, and privacy

You may connect GitHub or another provider to assist read-only exploration. Begin with only the repositories and rights needed. A signed-in service is not proof that the correct repository, branch, application, or runtime is active. Before allowing a coding tool to write, check its current directory, configured permissions, and relevant branch or worktree. Do not grant global access “just in case.”

Local reversible checks differ sharply from publication, destructive filesystem operations, API purchases, sending project content to third parties, or modifying production services. The latter need explicit authority with a clear target and limit. Do not copy secrets into agent prompts, public issues, Git history, workflow logs, or the public starter. The application can remain private while the governance starter is public.

The framework can generate privacy-preserving metadata feedback locally. In v1.4 the local strict-metadata report configuration is enabled by default, while external collection is not bundled. `--no-feedback-workflow` removes the periodic workflow scheduler; it does **not** disable the local generator. To disable reporting entirely, set `enabled=false` in the installed feedback configuration. Review the [feedback privacy policy](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md) and any executable workflow changes before making an affirmative choice.

## 11. Safe troubleshooting

| Observation | Safe interpretation | Next action |
| --- | --- | --- |
| Python is not recognized. | The terminal cannot locate an interpreter. | Verify your installation and path; leave the application unchanged. |
| `.agentic-sdlc/` is absent. | The scaffold may have targeted another folder or failed. | Compare the exact target path and command output. |
| `HOLD / UNTRUSTED_CONTEXT`. | First installation succeeded without inventing project facts. | Continue discovery and adoption; do not suppress HOLD. |
| `jsonschema` is missing. | Validation dependencies were not installed in the active interpreter. | Install the declared requirements and rerun the read-only checks. |
| An existing control layer is preserved. | The installer protected canonical governance. | Use the read-only governed-project attachment procedure. |
| Validation or reconstruction reports a conflict. | Structure, authority, source, or DB witnesses may disagree. | Preserve the report; reconcile the exact cause before material writes. |
| The coding agent sees another repository. | Its operational scope points to the wrong directory. | Stop writes and verify target, permissions, and working tree. |
| Tests pass but the application does not open. | Control tests did not cover the application's physical behavior. | Run the actual product and check its real user journey. |

The correct result of the installation chapter is an initial control layer whose structure and limits can be inspected. Its adaptation to real code, requirements, data, and current authority is the subject of Chapter 02. Do not treat those two milestones as interchangeable.

**Next:** Chapter 02, Planner and Adoption.

## Sources and applicability

- [v1.4.0 GitHub Release](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0)
- [Public start and supported boundaries](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [v1.4.0 release and upgrade notes](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md)
- [Fork and bootstrap](../../../01_FORK_AND_BOOTSTRAP.md)
- [Transfer and adoption](../../../16_TRANSFER_ADOPTION.md)
- [Existing governed-project attachment](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)
- [Executable validation](../../../10_EXECUTABLE_VALIDATION.md)
- [Feedback and privacy](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md)
- [Scaffold source](../../../../tools/scaffold_project.py)

All instructions concern the starter or a fictional application. They do not prove installation, acceptance, or runtime compatibility for a specific adopter's project.
