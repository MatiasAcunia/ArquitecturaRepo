# Repository Efficiency and Workspace Hygiene

## Core invariant

Repository movement, commits and local workspaces are engineering resources, not activity signals.

The default operating posture is:

`KNOWN_BASELINE -> NARROW_REMOTE_REFRESH -> DELTA_INSPECTION -> COHERENT_WORK -> ONE_MEANINGFUL_INTEGRATION_BOUNDARY -> LIFECYCLE_CLEANUP`

Do not repeatedly clone, pull, reread or recommit the whole repository merely because one bounded change occurred.

## 1. Hard commit authority

Canonical Git history is not a worker transcript.

- I4 Execution Team Members MUST NOT create canonical commits, push, tag, merge, rebase or move refs unless a project-specific authority contract explicitly makes that bounded Git operation their task.
- I3 / the integration controller owns ordinary engineering candidate commits.
- I2 may create strategic/authority-state commits that are genuinely Planner-owned.
- I1 may create global/system authority or release commits where I1 authority exists.
- A tactical assignment, helper completion, test attempt, reviewer comment or retry is NOT by itself a commit boundary.

A canonical commit must fit one of these boundary classes:

- `COHERENT_CANDIDATE` — one causally complete, independently reviewable implementation/integration unit;
- `RECOVERY_CHECKPOINT` — persistence is materially required to prevent reconstruction/recovery loss;
- `AUTHORITY_TRANSITION` — a durable strategic/currentness/ownership transition;
- `RELEASE_BOUNDARY` — a release/version boundary with its required evidence.

Failure code: `COMMIT_BOUNDARY_UNJUSTIFIED`.

Do not split a single causal repair into microcommits merely to expose activity. Do not combine unrelated/risk-independent changes into one mega-commit.

## 2. Commit-mania rule

`COMMIT_MANIA` is present when Git history becomes an activity log.

Signals include:

- commit after every file/edit/test/retry/helper;
- adjacent commits that have no independent meaning;
- unstable partial candidates committed without recovery value;
- repeated CI-trigger commits without a materially changed hypothesis;
- creating new reports/checkpoints/policies because a small action happened;
- treating commit count or recent Git movement as progress.

Corrective action is to widen the execution/integration unit to the smallest causally complete boundary.

Projects may use `tools/commit_guard.py` or an equivalent enforcement mechanism before canonical commits.

## 3. Delta-first remote currentness

When a trustworthy local clone/worktree and a known baseline already exist, remote currentness MUST be refreshed incrementally.

Preferred Git operation:

`git fetch --no-tags --no-recurse-submodules <remote> +refs/heads/<branch>:refs/remotes/<remote>/<branch>`

Then compare exact SHAs and inspect the delta.

Do not use `git pull` as the default authority/currentness primitive. Pull couples fetch with merge/rebase and may mutate the worktree before currentness is classified.

A known-baseline refresh must not require recloning the repository, fetching unrelated branches/tags, rereading every source file or rebuilding a full repository summary when the affected dependency surface is known.

`tools/repo_delta.py` is the reference read/refresh primitive.

## 4. When full reconstruction is justified

A broader repository read or new clone is legal when at least one is true:

- first bootstrap / no trustworthy local repository exists;
- the baseline object/ref is unavailable;
- local and canonical histories diverged;
- repository topology or global authority materially changed;
- dependency impact cannot be bounded from the observed delta;
- currentness evidence indicates the prior local index is incomplete/stale;
- corruption or missing objects make incremental reconstruction unreliable.

Even then, prefer partial/single-branch clone or sparse/filtered acquisition when compatible with the target project.

A fresh agent context does NOT automatically imply a fresh repository clone.

## 5. Delta-first context acquisition

After a known baseline `B` and refreshed canonical head `H`:

1. classify `B` vs `H`;
2. list changed paths;
3. identify changed canonical owners/authority surfaces;
4. expand to directly affected dependencies/interfaces/tests;
5. read deeper only when evidence requires it.

Do not use full-repository rereads as a ritual after every commit.

Fresh-context correctness still wins over under-reading. Delta-first is an efficiency rule, not permission to ignore material dependencies.

## 6. Workspace ownership

Every system-created local workspace intended to outlive one process step should be explicitly owned and lifecycle-classified.

Reference marker:

`/.agentic-sdlc-workspace.json`

Lifecycle classes:

- `EPHEMERAL_RECONSTRUCTIBLE`
- `CACHE_RECONSTRUCTIBLE`
- `SHORT_TERM_EVIDENCE`
- `QUARANTINE_UNRESOLVED`
- `PROTECTED_CURRENT_OR_EVIDENCE`

Unmarked directories are UNKNOWN and MUST NOT be garbage-collected automatically.

## 7. Local garbage-collection safety

The reference GC is `tools/workspace_gc.py`.

It is dry-run by default.

Automatic deletion requires ALL of:

- candidate is an immediate child of the explicitly supplied GC root;
- candidate contains a valid lifecycle marker;
- `safe_delete=true`;
- lifecycle class is deletable;
- expiry is reached;
- no active lease/sentinel blocks deletion;
- path is not a symlink;
- if Git-backed, worktree/repository state is clean;
- candidate is not protected/quarantined.

If any condition is unknown, preserve and classify instead of guessing.

Failure to clean known disposable bytes is cleanup debt. Deleting unknown/current/user-managed bytes is a more serious correctness failure.

## 8. Git worktrees

Linked Git worktrees require Git-aware cleanup. Raw directory deletion may orphan Git administrative metadata.

The GC must either remove an expired clean linked worktree through `git worktree remove` or refuse deletion with a typed BLOCK result.

Dirty worktrees are never auto-deleted.

## 9. Cleanup checkpoints

System-created ephemeral workspaces should receive an expiry at creation time.

Cleanup is event-driven:

- process scratch/cache after successful readback/promotion;
- execution workspaces after integration + evidence binding + no recovery dependency;
- short-term review evidence after the review/appeal boundary;
- quarantine after explicit classification;
- protected/current evidence has no automatic expiry.

Terminal readiness includes lifecycle reconciliation for campaign-owned workspaces/artifacts.

## 10. Machine-local garbage versus product artifacts

Do not conflate local agent/runtime workspaces, caches, temporary clones and scratch with product artifacts, accepted evidence and user-managed media.

`workspace_gc.py` addresses machine-local engineering garbage.

`STORAGE_AND_ARTIFACT_LIFECYCLE.md` governs product/artifact storage when that optional profile module is active.

## 11. CI and canonical branch discipline

Local edit/test cycles may continue without a commit.

When canonical-branch CI is a required mutation invariant:

- do not stack ordinary canonical commits on red/pending/unverifiable HEAD;
- diagnose the exact candidate first;
- use one corrective causal commit rather than a stream of speculative CI pokes.

This does not require remote CI after every local edit.

## 12. Success criterion

Repository hygiene is healthy when Git history expresses meaningful causal/recovery/authority boundaries, currentness refresh transfers only required refs/objects, context reloads are delta-first, disposable local workspaces have ownership/expiry, GC can prove what it deletes and cleanup does not require CLIENT technical rescue.
