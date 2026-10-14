# Codex Daily Control 2.0.2 — physical integration contract for ArquitecturaRepo v1.2

Scope: candidate integration boundary, not a new controller or I3 campaign. Source inspected was the user's `Codex_Daily_Control_2_0_2_HARDENING_RC.zip` (SHA-256 `d2c5bfa1dbd2ee7ffc64a37f1d9736f1f313ef67b15f9200944b041f9bd3716e`). Version metadata explicitly reports `2.0.2-hardening-candidate` and native Windows acceptance pending. Its module manifest is at `2.0.1` and must be reconciled in the installed host version contract rather than assumed to be an entirely uniform 2.0.2 binary.

## Physical findings

- ZIP contains 92 entries, with `SOURCE_SHA256SUMS.txt` listing 86 expected files. Byte-for-byte verification: 73 match and **13 do not**. Mismatches include `bin/install.ps1`, the daily-close engine, continuity instrumentation, README/release metadata and some tests. This is a **package-manifest integrity HOLD** until fixed and independently reproduced. These disagreements might reflect a stale signing manifest; they alone do not prove compromise.
- Existing isolated tests: 96 static source-contract pytest cases PASS plus 20 static/native-hardening fixture checks PASS. These cannot prove PowerShell 5.1 AST parse, installed Windows host, app-server, native scheduler, Goal/thread authority, remote Drive readback or recovery.
- The controller is configured for a fixed set of four native slots only. ArquiteturaRepo itself and generic CRUD projects are not covered by these slots. Don't silently add a fifth slot or treat the controller as a universal scheduler; a versioned generalization requires its own engineering acceptance.
- Native operations in the package's `bin/codex-daily-control.ps1`: `Probe`, `Status`, `V2Status`, `PreClose`, `DailyClose`, `V2Cleanup`, `V2NewDay`, `V2ManualRecovery`, etc. **Not all are read-only**: `Invoke-CGKV2Status` calls `Write-CGKV2Receipts` (writes local evidence). `DailyClose` changes native Goal state, sends prompts, builds archives and publishes. `V2Cleanup` can delete threads. No passive adapter may invoke them merely to get a status.
- Controller remains a transport/observer, not CLIENT, OWNER, Planner, I3 or release authority. Native Goal/thread and quota ownership remain with actual app-server/current controller, not a new local JSON claim.

## Native adapter architecture (stage-gated, no invented API)

1. **Stage A — immutable package/installed-byte preflight (implemented in this candidate).** Inspect only explicitly provided ZIP or installed root; parse version, release and four-slot IDs; require SHA-256 manifest consistency and expected external package digest. Reject traversal, ambiguous path, duplicate paths and symlinked installed references. Return typed HOLD reasons, never execution authority. No output of raw secrets, paths to private chats, Goal IDs or Drive credentials.
2. **Stage B — Windows installed host binding (L3 native obligation).** In an approved disposable Windows 10+PowerShell 5.1 environment, locate actual installed files, compare package SHA/manifest against post-install binaries, attest Code Signing/PowerShell AST tests as applicable, exact app-server capability and CLI functions. Reconcile installed binary versions and previous installed state, never silently reinstall over running close. Zero guesswork from historic install reports.
3. **Stage C — identity, quota, recovery and native Goal operations (native host).** Verify each slot's real Goal/thread/account, I3 ownership and currentness; distinguish quota-paused, user-paused, blocked, completed and active turn states; authorize only correct specific Resume/wake with a valid lifecycle envelope and post-call readback. Existing CLI `V2NewDay` expressly **does not resume Goals**, so no fake resume call to that function. Never edit Codex SQLite directly.
4. **Stage D — daily close, daypack and data pipeline.** Four independent daypack receipts, SHA256 frozen-archive vs source, registered Drive MD5+size remote readback and sidecar; closing and deleting chats are distinct stages. Reconcile legacy V9-v13 journals without migration by assumption. Check private-conversation permission and destination rights. No uncontrolled extra clones or large files.
5. **Stage E — independent product/system evidence.** Native crash injection, interrupted rollout and prompt send, duplicated turn prevention, wrong thread/account, malformed lease, stale Git/worktree, interrupted upload, remote byte drift, installation mutex, rollback, 24h resource load and human pause; independent reviewer signs exact source and host. Only then can ArquitecturaRepo advertise real stable 2.0.2 operational integration.

## State and policy

This tool is **not** a replacement for `tools/goal_guard.py`, `tools/state_tx.py`, controller's installed processes, the native app-server or OWNER identity. The gate remains required for stable inclusion unless CLIENT/I2 explicitly re-scopes it; this user's directive confirms it is intended as a **real integration**, not a config-only demo.

If the executable 2.0.2 package is repaired and native host accepted, I3 must integrate it into the existing project setup/currentness lifecycle and then perform exact candidate I4 independent audit. Until then: `CODEX_DAILY_CONTROL_2_0_2=HOLD`. This does not block independent non-2.0.2-safe I3 engineering work, but does prevent declaring the full promised v1.2 capability complete.

## Reproduction

Run the Python tool on an approved ZIP or installed root. It intentionally exits 2/HOLD even when byte integrity is good, because it has no authority to certify native host operation. Tests use synthetic local ZIPs; they do not send prompts, call a cloud service, modify a Goal or delete chats.
