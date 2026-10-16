# v1.3 portable core — support boundary and release gates

This is the source-bound engineering support matrix for the v1.3 candidate. It does **not** authorize a v1.3 release. In a draft v1.3.0 release-candidate branch, `VERSION`/starter manifest may say 1.3.0; this is **not** a published release. The historical v1.2 tag stays immutable.

| Capability | Current status | Meaning / required evidence |
| --- | --- | --- |
| Profile installation and state owner initialization | Tested in disposable new projects | First install creates a HOLD / UNTRUSTED_CONTEXT skeleton; it never grants execution authority. |
| Existing governed repository | Safe generic scaffold refusal | A second Product State must never be installed. Use explicit read-only attachment and separate governed migration review; generic `scaffold_project.py` is not an attach operation. |
| Durable campaign control / atomic transaction / SQLite WAL | Portable component tests | The campaign CLI serializes participating mutators with its state lock; a noncooperating external writer is outside its lock boundary. |
| Local execution identity | Registry/lease-bound control-plane claim only | ACTIVE authority requires a current registered I3 actor/run and valid finite lease. Work-unit start matches that actor/run. This is **not** cryptographic OS/user authentication or independently verified native host execution. Unauthenticated local CLI access is not a permission sandbox. |
| Independent review and readiness terminal | Immutable-by-hash review-evidence check | A passing reviewed candidate requires the identical existing evidence files and current registered reviewer identity at terminal time. Any out-of-band evidence change requires new review; terminal readiness is a request for owner acceptance, not automatic publication. |
| Portable ToolPort | Tested fixed disposable adapter | Bounded physical test writes; no arbitrary source-writing host is implied. |
| Codex Desktop / other optional hosts | UNVERIFIED and disabled by default | Requires supported OS/process/permission and cost-bound enforcement evidence for that host/version. No native Goal, quota recovery or process automation claim without live acceptance. |
| Agent Continuity Bridge 0.2.1 | Separate optional offline candidate, PR #5 | ZIP verification and project registration only. External Codex Daily Control 3.1 RC and personal controller configuration are not part of the public package. |
| Architecture feedback | Local generator and optional scheduled workflow, no bundled collector | `--no-feedback-workflow` skips installing the workflow; local generator and outbound *preference* are independent flags, and actual external delivery is NOT_OBSERVED without a verified transport. |
| Automatic bridge upgrades / general native portability | NOT_IMPLEMENTED / NOT_VERIFIED | Do not advertise as supported. |

## Release qualification still required

1. Freeze the exact final clean source bytes, manifest and commit; exclude internal `response/`, checkpoints, user paths, private configurations and generated caches. Preserve the stable v1.1/v1.2 tags.
2. Independently rerun the reviewer-owned black-box oracles, `tools/selftest_v13_control_plane_closeout.py`, the configured Linux/Windows support matrix and an installed portable end-to-end lifecycle. Test genuine negative cases and ordinary successful transitions.
3. Reconcile user-facing packaging, eight available documentation languages, dependency list and lossless migration/rollback behavior. Confirm the public v1.3 release authority before changing `VERSION`, publication allowlist or creating tags.
4. Treat M5 research proposals as **DEFER** absent measured comparative benefit, not as grounds for adding unproven infrastructure. M7 is a separate decision, not a prerequisite to honest portable-core support.

Only the designated release authority may accept the verified release candidate. Local tests, recorded actor strings and draft PR CI alone are not independent sign-off.

For release-package adoption, safe side-by-side handling of governed v1.2 projects, and the explicitly manual publication gate, see `docs/43_V1_3_RELEASE_NOTES_AND_UPGRADE.md`.
