# Security policy / Política de seguridad

**Stable branch:** 1.1.x. **Operational 1.2 work:** draft PR, not a supported release.

## Report a security issue

Do not publish credentials, private project files, confidential reproducers, user identifiers or exploit details in a public issue. Contact the repository maintainer through an appropriate private GitHub channel when available; if no private channel is available, do not disclose sensitive payloads publicly.

For non-sensitive defects, open a GitHub Issue with a synthetic reproducible fixture, affected version, expected behavior and observed result. Redact all tokens, paths, personal data and actual product identifiers.

## Trust boundaries

- A green repository CI only proves the tested control-layer candidate, never the adopted application's correctness.
- Installing a scaffold does not grant autonomous authority, external publication, destructive cleanup, billing or private-data export.
- The optional Goal guard is diagnostic only until real, independently verified host pre-dispatch binding exists.
- External effects remain ambiguous until provider readback; self-declared receipts are not independent verification.
- Gemini I4 is disabled by default and must have explicit export permission, key, provider/data-use and quota verification.
- OWNER five-task scheduling requires a real scheduler adapter and the user's installation authorization.
- Codex Desktop, Windows and Codex Daily Control 2.0.2 are separate physical integration gates.
- Monthly strict metadata-only feedback is ON by default in **the adopter's own** GitHub Actions; external sending is OFF unless separately authorized. See [privacy and opt-out](docs/22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md).
- Never run untrusted repository code with elevated privileges or grant unnecessary tokens to jobs.

## Verification before any 1.2 release

The full v1.1 gate, v1.2 adversarial tests, migration compatibility, pinned workflow dependencies, host-specific physical tests, independent review, privacy tests and rollback are mandatory. See [security audit](docs/25_V1_2_SECURITY_HARDENING_AUDIT.md) and [Windows L3 acceptance plan](docs/26_L3_WINDOWS_PHYSICAL_ACCEPTANCE.md).

There is no claim of absolute security. Any new executable surface requires explicit threat modeling and revalidation.
