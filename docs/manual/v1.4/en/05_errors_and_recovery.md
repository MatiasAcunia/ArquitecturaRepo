# 05 — Errors, Incidents and Recovery

ArquitecturaRepo · Complete User Manual · v1.4 edition · English

> The objective of recovery is to restore a **truthful, verifiable state**, not merely to make an error message disappear. Preserve source, ownership, transaction journals, DB witnesses and relevant evidence. An ordinary in-charter bug is repaired by I3; a missing authorization or contradictory canonical currentness is a different class of blocker.

## In this chapter

1. Preserve evidence first
2. Environment and account failures
3. When the control layer fails validation
4. Git is not an “undo problems” button
5. Repeated failures require a causal change
6. Security, privacy, and third-party rights
7. Exit an incident with evidence
8. Three complete recovery examples
9. Decision table for sensitive operations
10. What successful validation does not prove
11. The starter's privacy and feedback controls

## 1. Preserve evidence first

Record the exact error message, the command or action that produced it, the relevant time, the affected repository and working tree, and the source or artifact reference if known. Do not instinctively delete a directory, reinstall the starter, discard local changes, or create another clone. Such actions can destroy precisely the information needed to recover safely.

The technical owner must classify the problem before choosing a repair route. Possible causes include an unavailable executable, missing permission, application defect, invalid governance contract, conflicting source ref, broken DB transaction, external provider failure, or reserved authorization. They are different incidents with different safe responses.

| Observation | Safe first response |
| --- | --- |
| An integration test fails for an active feature. | I3 keeps the reproduction and repairs it inside the existing charter. |
| A control-layer validator rejects canonical state. | HOLD dependent actions; locate the conflicting relation and its owner. |
| Local and remote Git changes conflict. | Preserve both, inspect the exact delta and reconcile without guessing. |
| Real user data might be corrupted. | Stop sensitive writes, preserve backups and WAL/journal evidence, assess restoration. |
| Publishing or a paid action lacks explicit authority. | Do not perform the external effect while authorization is absent. |
| The coding host may have dispatched an external side effect before crashing. | Mark the effect unknown and perform readback before considering a retry. |

The aim is not to reduce the number of red indicators by hiding them. The repair must address the cause and demonstrate the relevant gate on the current candidate. Read-only investigation and preservation normally remain possible while material changes are on HOLD.

## 2. Environment and account failures

**Python or another command is missing.** Verify the current directory, interpreter name, installed version and active environment. Use the declared project dependencies and trusted sources. Do not alter Product State to compensate for a missing executable. A coding assistant with access to the local environment can inspect the path; otherwise preserve the full command output for the person who can.

**GitHub does not appear in your planning interface.** Separate authentication, connector installation, permission scope, repository visibility and branch availability. A failed read does not justify writing files, importing more secrets, or granting access to an entire account. Confirm access to the exact authorized repository using a read-only request.

**The coding agent opens the wrong project.** Verify that the local folder exists and contains the actual product. Do not substitute the ArquitecturaRepo starter for `club-app` simply because both directories are named in the manual. Confirm write permissions and active worktree before making changes.

**A session is interrupted or its usage limit is reached.** The provider session is not the campaign. Recover the authorized Goal, active owner, last checkpoint, integrated candidate and pending effects from durable evidence. A time limit does not authorize a new campaign or a competing controller. If the host cannot resume the thread, the repository remains the source of continuity.

## 3. When the control layer fails validation

The installed `tools/validate_project.py` examines contracts and references in `.agentic-sdlc/`. It may reject a missing authority record, duplicate owner, inconsistent candidate/review relation or malformed current-state reference. It does **not** by itself test whether the application can connect to its DB, that a staff member can log in, or that payment history survives a restart.

Before editing anything, preserve the validator's exact output, the control-layer root, current Git ref, dirty files and relevant DB witness. The appropriate owner should determine whether the cause is a missing dependency, a contract mismatch, a genuinely stale reference, a partial transaction or a conflicting external edit.

Never force `READY` into a JSON file or erase a journal simply to make validation pass. If two actors plausibly own the same active effect, or a candidate has changed after an independent review, the correct response is to reconstruct authority and lineage. A cosmetic field edit would make the report more reassuring while making the underlying state less truthful.

Transactional control-layer changes may update multiple related files. The framework documents explicit [transaction recovery](../../../12_TRANSACTION_RECOVERY.md) using before/after hashes and ownership. A pending journal can appropriately block further mutation. An external conflicting edit must be surfaced as a conflict, not silently overwritten to complete a stale transaction. The team should only resume when the relevant records agree and the recovery operation has been physically read back.

With SQLite, the main `.db` file alone may not represent the live data state while Write-Ahead Logging is in use. The associated WAL and transactionally consistent snapshot matter. A checksum of just the main file is therefore not automatically proof of current DB contents. The [existing-governance attachment route](../../../32_EXISTING_GOVERNED_ATTACHMENT.md) preserves this distinction; it does not automatically repair a production database.

## 4. Git is not an “undo problems” button

When GitHub Desktop or the CLI reports a conflict, do not blindly choose “mine” or “theirs.” Both sides may contain legitimate work. First inspect the exact base, local modifications, remote delta and current ownership. A trusted checkout should not be deleted merely because a diff is inconvenient.

The starter includes `tools/repo_delta.py` for bounded incremental inspection and `tools/workspace_gc.py` for controlled cleanup. Neither is permission to delete source, accepted artifacts, unknown human files or current evidence. Begin cleanup with a read-only inventory and dry run; deletion needs positively established ownership and disposability. A directory that appears old is not necessarily garbage.

Use one persistent checkout per repository when safe, and temporary shared-object worktrees only for genuine concurrency. Do not accumulate cloned repositories, large render caches or duplicate evidence “just in case.” At the same time, do not make disk hygiene a pretext for destroying lineage, backups, active transaction records or artifacts needed to falsify or accept a capability.

`git reset --hard`, forced replacement of a branch and recursive deletion are not general recovery recipes. When a rollback is truly necessary, identify the precise target, restore point and affected data first. An application rollback may need a corresponding schema or data strategy; moving Git alone cannot unwind a production DB transaction.

## 5. Repeated failures require a causal change

Running the same command with the same inputs and assumptions repeatedly is not progress. When a class of failure recurs, I3 consolidates its observations, inspects the affected subsystem and interfaces, strengthens relevant regression and integration tests, and obtains independent review. It remains the same authorized campaign until there is genuine strategic invalidation.

For costly work, the bounded work-order contract establishes budgets, retry limits and stop conditions. If successive attempts produce no delivered outcome, I3 changes the method or reports the exact causal blocker. The planner should not generate an endless sequence of new campaigns simply to relabel the same failure. Likewise, passing a narrow unit test after a patch is not enough if the actual user workflow remains broken.

The useful terminal is one of: physically delivered capability with relevant checks, an explicitly bounded blocker with evidence and owner, or a recoverable checkpoint with a known legal next action. A stream of commits, model calls or advisory documents does not substitute for any of these.

## 6. Security, privacy, and third-party rights

A technical charter does not imply permission to expose private information, pay an API, disclose credentials, remove protected records or publish another person's material. These operations have their own reserved authority and risk boundaries. Use least privilege, synthetic data in unauthorized demos, authenticated secrets mechanisms, lawful data handling and source-appropriate license checks.

- Never place passwords, tokens, private keys or connection strings in prompts, issues, repository history or public build logs.
- Work with synthetic or appropriately deidentified information when a review or demonstration does not need real people.
- Before a destructive migration or cleanup, identify affected records and verify an appropriate backup and restoration route.
- Before publishing third-party images, code, music or video, establish the rights required for the actual use. The starter's MIT license covers its own licensed material, not unrelated assets.
- Before billable provider calls, obtain the authorized budget, rate/cost bounds and meaningful stop conditions. A connection failure does not justify unlimited paid retries.
- Before exposing an application publicly, verify authentication, authorization, network configuration, data paths, secrets and the explicit decision to deploy.

Privacy, intellectual property, security and operational safety are related but distinct gates. A human's acceptance of a sample's visual quality does not create a copyright license. A code test passing does not create permission to publish personal data. Keep each decision with its actual owner.

## 7. Exit an incident with evidence

An incident can be closed only when the recovery report explains what failed, its cause, what changed, what source/data were preserved or restored, what physical checks were performed, and which risks or gates remain open. The report names the current candidate and the owner of the next action. I3 can confirm a technical repair, while the Planner evaluates whether the capability's strategic conditions are again met.

If the current state cannot be reconstructed, or there is no trustworthy recovery route for critical data, say so plainly. An explicit HOLD with a precise missing witness is safer than pretending that the original application state survived. Continue safe investigation rather than authorizing dependent mutations against unknown conditions.

## 8. Three complete recovery examples

### Incident A — The coding session ends during a campaign

The coding host disconnects while a member search feature is in progress. Do not send the same high-level request into a new isolated session and hope the resulting work is equivalent. Inspect the actual checkout for uncommitted writes, locate the campaign journal and latest checkpoint, identify the current owner/lease, and read any pending external effect receipts. Confirm what candidate was integrated and what remains outstanding.

If source and authority agree, resume the existing campaign at the next legal step. If a critical reference is absent, record which witness is missing and HOLD only work that depends on it. Provider-session limits neither create new product requirements nor invalidate the current charter.

### Incident B — A multi-file state update is interrupted

A transition intended to update bootstrap, Product State, ownership and checkpoint stops halfway. Several files may now disagree about which version is current. The framework's state-transaction journal exists so the owner can distinguish fully applied changes from partial or conflicting ones. Inspect it before running further mutations.

Use the documented recovery command belonging to the tool that initiated the transition, such as `campaignctl recover` for a compatible reference-runtime transaction. The transaction mechanism advances only when expected before/after hashes still justify each write. If someone else edited the same canonical file, the correct outcome can be `CONFLICT`. Do not manually erase the journal, edit statuses or overwrite the unrelated change to force a clean report.

### Incident C — Tests pass but the real application fails

A dues calculation passes unit tests, but the member screen shows an outdated amount after saving. Capture the exact source candidate, user steps, environment, expected and observed behavior, and relevant DB state. The unit gate passed; the end-to-end or persistence gate did not. Exercise the failing interaction against the current candidate and repair the shared state or integration path.

If the issue is within the existing charter, I3 owns the correction and updated independent review. Repeatedly rerunning the same unit test cannot validate a missing UI refresh or DB commit. The incident is resolved when the physical journey and adjacent affected checks demonstrate the repaired behavior.

## 9. Decision table for sensitive operations

| Proposed action | Primary risk | Minimum pre-execution boundary |
| --- | --- | --- |
| Show a demo using real member records. | Personal-data disclosure. | Use synthetic records or establish appropriate consent, purpose, permissions and protection. |
| Create a GitHub token. | Excessive access or leakage. | Least privilege; keep the secret out of source and logs; revoke it if exposed. |
| Delete apparently temporary folders. | Loss of live work or evidence. | Confirm exact owner, disposable status and dry-run target. |
| Open a public deployment. | New attack surface, private-data exposure and cost. | CLIENT authorization, security/network preflight and observable rollback plan. |
| Activate a paid API. | Unbounded charges or retries. | Explicit budget, operation bounds, measurement and terminal failure behavior. |
| Publish third-party media. | Unauthorized reuse. | Verify source identity, license, applicable scope and attribution. |

A general “you may work in this project directory” is not blanket authorization for irreversible, external or billable effects. Engineering chooses technical safeguards; the CLIENT makes product and reserved exposure decisions.

## 10. What successful validation does not prove

A passing `validate_project.py` result may show that structural control records are internally consistent. It cannot prove that a backend is reachable, a real DB survives restart, an endpoint enforces all required permissions, or a user can complete the intended journey. A synthetic adoption test does not authorize an untested production migration. An attractive screenshot does not replace real interaction testing.

When repairing an incident, rerun the gate that actually failed and nearby checks plausibly affected by the fix. Identify the new candidate and reviewer. Do not invalidate unrelated evidence for no reason, but do not promote a material code change using stale review results. If code, DB and current Product State still contradict each other, keep dependent changes on HOLD until physically reconciled.

The same separation applies to distribution: a passing source build is not by itself proof of a published archive's contents, checksum or availability. Release readback is a distinct check on the exact distributed bytes.

## 11. The starter's privacy and feedback controls

In v1.4 the scaffold's local strict-metadata feedback report configuration is enabled by default. A periodic GitHub Actions scheduler can also be generated. External collection is not bundled in the public release; sending feedback externally requires the separately documented explicit opt-ins. Review the [privacy feedback contract](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md) and the installed executable workflow before enabling any network effect.

The `--no-feedback-workflow` scaffold option avoids installing the periodic scheduler, but **does not disable the local report generator**. To turn off the latter, set `enabled=false` in the installed feedback configuration. Be explicit about the distinction rather than describing either option as “disabling all telemetry” without checking its actual scope.

None of these defaults proves that a subsequently developed application handles its own personal data safely. Each adopting project must assess its actual credentials, logs, data flows, permissions, network interfaces and retention requirements.

**Next:** Chapter 06, Closing Capabilities and Acceptance Gates.

## Sources and applicability

- [Security, privacy, third-party rights and external actions](../../../../protocols/SECURITY_PRIVACY_RIGHTS_AND_EXTERNAL_ACTIONS.md)
- [Transaction recovery](../../../12_TRANSACTION_RECOVERY.md)
- [Privacy-preserving architecture feedback](../../../22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md)
- [Existing-governance read-only preflight](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)
- [Reference transaction implementation](../../../../tools/state_tx.py)
- [Workspace cleanup implementation](../../../../tools/workspace_gc.py)
- [Repository delta inspection](../../../../tools/repo_delta.py)

These examples are hypothetical. Any real recovery or deletion requires direct evidence from the affected target and the appropriate authorization.
