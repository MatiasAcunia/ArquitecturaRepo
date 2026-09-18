# Repository Efficiency and Local Workspace Hygiene

This patch addresses three concrete operational failure classes:

1. commit history fragmented into activity-log microcommits;
2. repository/currentness refresh that reacquires or rereads far more than the observed delta requires;
3. agent-created local workspaces/caches/scratch that accumulate because cleanup ownership was never encoded.

These are execution-system defects, not product-specific rules.

## Commit boundaries

Workers do not own canonical Git history by default.

The integration layer groups tactical work into the smallest causally complete candidate. Separate commits are reserved for coherent candidates, recovery checkpoints, authority transitions and release boundaries.

Reference preflight:

```bash
python tools/commit_guard.py --repo "." --role I3_ENGINEERING_CAMPAIGN_LEAD --boundary COHERENT_CANDIDATE
```

The guard is intentionally not a progress scorer. It checks role/boundary authority and materialized staged state.

## Incremental repository refresh

When an existing trusted clone and baseline exist, use exact-branch fetch plus SHA/diff classification rather than `git pull` or a fresh clone:

```bash
python tools/repo_delta.py --repo "." --remote origin --branch main --baseline "<known-ref>" --fetch --json
```

The tool fetches one branch ref only, fetches no tags, does not recurse into submodules, does not merge/rebase/checkout/reset, leaves local HEAD unchanged and reports changed paths from the known baseline.

The changed-path set is the starting point for context reacquisition. Agents expand to affected owners/dependencies/tests only when evidence requires it.

A full clone/reconstruction remains legal for first bootstrap, divergence, missing objects, topology/global-authority changes or unbounded dependency impact.

## Workspace lifecycle

System-owned local workspaces should be marked when created:

```bash
python tools/workspace_gc.py register --path "../runtime/workspace-001" --class EPHEMERAL_RECONSTRUCTIBLE --owner I3_ENGINEERING_CAMPAIGN_LEAD --ttl-hours 6 --safe-delete
```

This writes `.agentic-sdlc-workspace.json`.

Dry-run GC:

```bash
python tools/workspace_gc.py collect --root "../runtime"
```

Execute only proven-safe cleanup:

```bash
python tools/workspace_gc.py collect --root "../runtime" --execute
```

The collector ignores unmarked directories and blocks protected/quarantined, unexpired, active, symlinked or dirty Git workspaces.

Linked clean Git worktrees are removed through `git worktree remove`, not raw filesystem deletion.

## Garbage-collector boundary

This GC is deliberately for machine-local engineering garbage: disposable clones/workspaces, caches, scratch and temporary execution directories.

It is not a universal product-artifact deleter.

Large generated product assets, accepted evidence, human review references, rights/provenance material and user-managed files remain under the product/artifact lifecycle policy.

## Why marker ownership instead of heuristics

Filename, age and size are not deletion authority.

A safe GC needs positive evidence that the system owns the workspace, the data is reconstructible/short-lived, expiry is reached and no active/recovery dependency remains.

Unknown remains keep/block.

## Test gate

`tools/selftest_repository_hygiene.py` proves:

- exact-branch fetch does not mutate local HEAD;
- changed paths are delta-derived;
- I4 canonical commit authority is rejected;
- I3 coherent-candidate boundary is accepted;
- GC dry-run does not delete;
- expired pre-authorized workspace is deleted;
- protected, future, dirty and unmarked workspaces remain;
- cleanup cannot escape the supplied GC root.

This gate is part of the v1 release verifier from v1.0.1 onward.
