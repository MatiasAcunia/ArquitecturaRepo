# Portable Goal Engineering Engine — contract and release rules

- `engine_id`: `arquitectura.portable-goal-engineering`
- Inputs: authorized source/charter/runtime state and live host currentness, never chat as authority
- Outputs: bounded inspectable execution/planning/engine evidence; no automatic Product State promotion
- Source implementation: `tools/goal_plan.py`, `tools/host_dispatch.py`, `tools/cognitive_i4.py`, `tools/cognitive_ledger.py`, `tools/engine_registry.py`
- Existing verification owner: `tools/selftest_operational_v12.py`
- Failure model: missing provider/host/DB/cost/readback evidence is a scoped HOLD, not a PASS
- Current adopted version: **UNPROVEN / null**

Each future immutable release receipt must bind exact Git commit, file digests, design/contract hash, tests, gates, compatibility, promoter and predecessor/rollback. Releases cannot be certified by this document or by a tactical Goal ZIP.

## Model-neutral portability and evidence bounds

Portable SIP ZIP contracts: exact `head_sha`, selected material source files and checksums, product/charter/currentness references, real initial L4 work order, Cycle hypotheses, known unknowns and gates. Output is immutable as a dated artifact; L2 daypack, L3 Goal ZIP and I2 output SIP have distinct authority. `l2-two-zip-preflight` is the correct L2 input check; `two-zip-preflight` is the correct L3 input check. Both require physical Git/DB/source state reconstruction afterward.

Credential resolution: `GEMINI_API_KEY`, or explicit `AGENTIC_GEMINI_API_KEY_FILE`, or unique `gemini<number>.txt` under opt-in `AGENTIC_GEMINI_KEY_DIRECTORY`. Ambiguous/multiple files HOLD; never rotate accounts to exceed provider quotas. Free-tier/cost verification remains a separate failure-closed gate; no external call is a product PASS.
