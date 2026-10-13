# Existing governed project attachment — read-only first

Status: **LOCAL_REFERENCE_PREFLIGHT_ONLY**. This is not an operational native Goal/Planner/I3 attachment and must not be advertised as completing any failed existing-project transfer.

Existing projects may already have canonical CLIENT requirements, Product State, identities, Planner, I3, DB and media/rights authority. Normal scaffolding creates a *different* Product State and owner registry; never install it blindly into such a repository.

`tools/existing_repo_attachment.py` takes a private local JSON map of existing canonical concerns to source-relative paths and their SHA-256 digests. The map must use `existing-governed-attachment-v1`, `READ_ONLY_REFERENCE`, `preserve_existing_authority=true`, `source_writes_allowed=false`, `external_actions_allowed=false`, and `authority_surfaces` with exactly one `CLIENT_REQUIREMENTS` and `PRODUCT_STATE` owner plus any other actual existing concerns. The tool checks path confinement, absence of symlink escapes, required files and pinned bytes. Its JSON output uses enum statuses only; it never exports code, product names, paths or digests.

Read-only usage: `python tools/existing_repo_attachment.py --project-root <authorized-disposable-source-copy> --manifest <private-local-map>`. This tool creates no new Product State, registry, reviewer or execution authority; it never mutates the original repo or calls external services.

A successful ref check returns `READ_ONLY_REFERENCES_MATCH_NOT_ATTACHED`, **not** a material-execution permit. Genuine attachment still needs I1/I2/I3 mapping, canonical DB/WAL/asset readback, host currentness/fencing and independent L3 transfer verification. Missing or ambiguous authority returns HOLD. A protected source must be accessed only on an explicitly authorized disposable copy.

The exact consolidated L3 transfer report must be reviewed before implementation of a mutating/operational adapter. This diagnostic does not close the physical transfer gate.
