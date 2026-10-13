# Project-local artifact inventory and safe GC (v1.2 candidate)

## Why this exists

A persistent I3 creates files across separate sessions. A model's memory is not
a reliable record of temporary renders, samples, build outputs, SQLite fixtures,
evidence or changes. The original workspace_gc.py knows about explicitly marked
WHOLE workspaces but does not inventory individual files. A lightweight JSON
ledger closes that gap for managed producer output without building a second
global database or another Product State.

Each scaffold now installs a local file:
.agentic-sdlc/runtime/ARTIFACT_LIFECYCLE_CURRENT.json
(or the selected --control-dir equivalent).
It starts empty and persists independent of model context and task sessions.

## Authoritative boundaries

- Git is authoritative for tracked source, branches and exact code identity.
- Product State and canonical DB retain their existing owners and backup policy.
- workspace_gc.py owns entire disposable directories and Git-aware worktree
  lifecycle. It must never take over existing folders or canonical repositories.
- artifact_ledger.py owns individual FILE entries inside a new scratch root
  explicitly created under .agentic-sdlc-scratch. It may not erase the root.
- File classification is an operational index and reclaim plan, not proof that
  a provider call was paid, a human accepted a video, or an external DB is safe.
- A private L3 artifact manifest is not part of monthly telemetry and cannot
  be uploaded or committed to the public starter by default.

## Categories

SOURCE_VERSIONED: source/config/intended Git content, never auto-delete.
CANONICAL_STATE: authoritative application/DB state, never auto-delete.
IMMUTABLE_EVIDENCE: accepted/independent review and recovery receipts, protected.
SHORT_TERM_EVIDENCE: samples awaiting review, protected until explicit promotion.
DERIVED_REBUILDABLE: temporary generated outputs, eligible after verification.
TEMP_TRANSACTION: bounded staging files, eligible after verified transaction.
SENSITIVE_LOCAL: secrets/user/private media, protected.
EXTERNAL_CANONICAL: cloud data/version references, no local deletion authority.
QUARANTINE_UNRESOLVED: unknown, modified or failed-run files, protected.

Every registry entry stores project-relative path, category, owner, campaign,
SHA256, size, device/inode/mtime, creation and observation times, expiry,
review closure, dependencies, delete permission and current/deleted/missing
status. Entries are saved as one atomically replaced JSON with exclusive
local writer lock; unresolved crash locks require owner review, not guessing.

## Exact controlled lifecycle

1. Preflight one canonical Git checkout, disk headroom, quota and the valid
   campaign/write envelope.
2. Register a NEW system-owned scratch root, for example:
   python .agentic-sdlc/tools/artifact_ledger.py --project . init-root
     --root .agentic-sdlc-scratch/campaign-A --owner I3 --campaign CAMP_A
   Existing directories cannot be claimed for GC, even if apparently empty.
3. Wrap the actual foreground generator in artifact_ledger.py capture with
   --root, --category and (only if independently safe) --safe-delete and
   --ttl-hours, followed by -- and the process argv. Avoid an intermediary
   shell where argument injection could occur. Outputs are fingerprinted and
   added to JSON; failed commands leave their outputs QUARANTINED.
4. On resumed context, abnormal termination, review boundary or terminal,
   run artifact_ledger.py reconcile --root ... . Unknown files are registered
   as QUARANTINE; changed files lose previous deletion eligibility.
5. Inspect artifact_ledger.py gc (dry-run default). It computes actual file
   identity and blocks unregistered siblings, symlinks, hardlinks, tracked or
   nonignored files, code and DB types, open review/dependency references,
   changed files, unknown roots or wrong owners.
6. Only artifact_ledger.py gc --execute can unlink an exact eligible file,
   after a second verification under the exclusive ledger writer lock.
   Every successful unlink updates the persistent ledger; repeated GC is
   idempotent and reports bytes reclaimed. Do not run GC merely because a
   numerical TTL elapsed if evidence or ownership is still uncertain.
7. Preserve the JSON ledger and material cleanup receipts across contexts.
   Archive a bounded evidence snapshot at meaningful engineering milestones
   when needed, but never create a commit after every individual generated file.

A category and a TTL are necessary but not sufficient permissions. SQLite
files, SQL, WAL/SHM and secret-looking files are protected even when someone
mistakenly selects DERIVED_REBUILDABLE. Missing files are marked MISSING after
reconciliation; they are never silently recreated. Artifact roots are separate
from productive paths, even inside a Git repository.

## Critical limitations and validation

This observer covers files inside controlled scratch roots and processes
routed through capture; it does NOT intercept arbitrary native Codex, IDE,
third-party process or external application writes. Source modifications
outside the scratch area remain under Git/currentness and the I3 candidate
manifest. Claiming complete filesystem monitoring requires a real host hook
and OS-specific physical tests. Without that hook, a nonwrapped producer must
be recorded through a bounded reconciliation and its outputs treated as
unclassified evidence, not automatically removable.

A same-user malicious actor could edit both JSON and ownership markers;
this ledger is not cryptographic attestation or a privileged sandbox. No
remote collector receives these paths. Deletion races with independent
processes cannot be eliminated without a verified external writer lease.
Protect concurrent writers, production DB and expensive media with their
canonical resource owners. For large outputs, hashing consumes I/O: measure
storage and use bounded batches. Generic script tests cannot replace physical
Windows, media/artifact and crash/recovery trials.

Minimum tests: fresh scaffold on all six profiles; happy-path sample
reclamation; dry-run nonmutation; bad generator quarantined; changed file,
unknown file, symlink and Git-tracked file protected; SQL/SQLite protected;
expired permission only; repeated GC idempotent; prior workspace takeover
blocked; interrupted-L3 reconciliation and disk recovery check on Windows.

This capability remains candidate-only pending exact Linux/Windows CI and
actual L3 adoption. The v1.2 release and governed-project transfer remain HOLD.

Portable output filenames with Unicode letters and spaces are supported. Windows device-name aliases and trailing-dot/space paths remain invalid. Every file entry must match the registered root owner and campaign or the ledger fails closed.

The generated control runtime includes a local .gitignore for the per-file ledger and its writer lock. The registry is retained physically across L3 sessions without forcing per-sample Git commits; any evidentiary snapshot must be deliberately sanitized/accepted at a meaningful checkpoint. Corrupt JSON, invalid owner bindings, changed root markers and existing writer locks all produce HOLD instead of permitting cleanup. No automatic stale-lock takeover is allowed.

## L3 responsibility and /cleangarbage

L3 maintains the JSON continuously; this is not a blind scheduled collector. A literal /cleangarbage message instructs L3 to follow the [cleangarbage skill](../.agents/skills/cleangarbage/SKILL.md): rebuild current Git/source evidence, reconcile every registered root, classify actual output, run GC dry-run, delete only protected-policy-authorized exact-safe files and read back reclaimed bytes. The skill is packaged in generated control as skills/cleangarbage/SKILL.md, and AGENTS.md specifies the invocation. Native Codex slash-menu registration is host-dependent and unproven; use explicit skill/text invocation if unavailable. The source tree outside the managed scratch roots remains governed by canonical Git/normal I3 review, not by this GC.

The CLI also exposes `cleangarbage` as a semantic alias of `gc`. It is dry-run unless `--execute` is explicitly supplied by an authorized L3 after reconciliation and candidate review. This Python subcommand is real and tested; it is not a native Codex slash-menu command.

GC reports both the logical byte sizes of deleted files and the physically observed free-space before/after/delta. They are not the same metric: concurrent processes, sparse/compressed files and metadata can change the actual disk delta. Do not advertise logical bytes as independently verified free disk space.
