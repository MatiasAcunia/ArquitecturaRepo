---
name: cleangarbage
description: L3-owned safe cleanup of generated samples, caches and temporary artifacts; use on /cleangarbage, clean garbage, disk hygiene or when a campaign needs to reclaim scratch space.
---

# L3 /cleangarbage workflow

L3/I3 is the responsible decision maker, not a blind garbage daemon. The literal user message `/cleangarbage` requests this workflow. Current Codex builds may not register arbitrary custom slash entries; invoke the `cleangarbage` skill explicitly, or send the agent the ordinary text `cleangarbage` if needed. Do not promise native command-menu support before verifying the installed host.

1. Read current Goal, charter, CLIENT boundaries, physical project Git HEAD and existing I3 authority. Reuse its sole canonical checkout; never reclone or use a blanket `git pull`.
2. Load the existing project-local `runtime/ARTIFACT_LIFECYCLE_CURRENT.json`. Missing, corrupt or mismatched ownership means HOLD; never recreate the inventory to bypass protection.
3. Run `artifact_ledger.py observe-git` to persist a bounded source-change snapshot of HEAD and Git porcelain status; then check live `git status`/source changes. For every owned `.agentic-sdlc-scratch/` output root listed in JSON, run `artifact_ledger.py reconcile --root <root>`. New and modified/unwrapped outputs become quarantine, never automatically deletable.
4. L3 examines category, owner/campaign, actual file identity, active leases/writers, Git tracked/ignored state, review/human obligations, downstream dependencies, licensing/privacy, retention and rebuildability. Distinguish samples pending human approval, evidence, application DBs, external objects and disposable intermediates.
5. Run `artifact_ledger.py gc` (dry-run). Explain ready, blocked, unknown, bytes available and why. For genuinely preauthorized, expired, reproducible scratch output, use `artifact_ledger.py gc --execute` without asking the CLIENT to micromanage each file. If an external approval is needed, request only that decision and keep the rest protected. Never automatically delete source, SQL/SQLite/WAL, rights evidence, original video/audio, accepted review samples, unregistered files, Git repos or active worktrees.
6. Reconcile and physically read back deleted files and remaining evidence; report actual bytes reclaimed, HOLD causes and residual disk pressure. Do not confuse a successful script return with an independent acceptance gate.

At every material generation: before and after source changes invoke `observe-git`; before execution capture a Git/source baseline, run sample/build/render/test producers through the owned-root `capture` interface, and reconcile on completion/failure/reentry. Maintain JSON across agent contexts. Source writes outside captured scratch roots must be reconstructed from Git and separately reported; this portable tool does NOT intercept arbitrary native IDE/Codex writes. Do not create a Git commit for each file. At terminal, present a concise durable per-category inventory and verified cleanup result.

The skill is an agent workflow, not an autonomous privileged deletion tool, native slash-command registration, or authority to alter product state.
