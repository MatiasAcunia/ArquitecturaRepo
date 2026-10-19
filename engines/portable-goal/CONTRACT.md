# Portable Goal Engineering Engine — contract and release rules

- `engine_id`: `arquitectura.portable-goal-engineering`
- Inputs: authorized source/charter/runtime state and live host currentness, never chat as authority
- Outputs: bounded inspectable execution/planning/engine evidence; no automatic Product State promotion
- Source implementation: `tools/goal_plan.py`, `tools/host_dispatch.py`, `tools/cognitive_i4.py`, `tools/cognitive_ledger.py`, `tools/engine_registry.py`
- Existing verification owner: `tools/selftest_operational_v12.py`
- Failure model: missing provider/host/DB/cost/readback evidence is a scoped HOLD, not a PASS
- Current adopted version: **UNPROVEN / null**

Each future immutable release receipt must bind exact Git commit, file digests, design/contract hash, tests, gates, compatibility, promoter and predecessor/rollback. Releases cannot be certified by this document or by a tactical Goal ZIP.
