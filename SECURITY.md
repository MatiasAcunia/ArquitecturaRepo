# Security policy / Política de seguridad

**Current published version:** [v1.4.0](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0). The moving `main` branch may contain later changes; use the tagged release and verify the archive checksum when installing. Previous v1.3.0 and v1.2.0 releases remain historical baselines.

## Report a security issue

Do not publish credentials, private project files, confidential reproducers, user identifiers or exploit details in a public issue. Contact the repository maintainer through an appropriate private GitHub channel when available; if no private channel is available, do not disclose sensitive payloads publicly.

For non-sensitive defects, open a GitHub Issue with a synthetic reproducible fixture, affected version, expected behavior and observed result. Redact all tokens, paths, personal data and actual product identifiers.

## Trust boundaries

- A green repository CI only proves the tested control-layer candidate, never the adopted application's correctness.
- Installing a scaffold does not grant autonomous authority, external publication, destructive cleanup, billing or private-data export.
- The optional Goal guard is diagnostic only until real, independently verified host pre-dispatch binding exists.
- External effects remain ambiguous until provider readback; self-declared receipts are not independent verification.
- No external AI provider is mandatory. Any optional provider or reviewer requires explicit data-export permission, credentials, quota/cost checks and independent evaluation; installation does not enable those calls.
- Native agent hosts, external schedulers and cloud actions require separately authorized adapters and physical integration evidence. Portable CI does not certify them.
- Monthly strictly allowlisted feedback in **the adopter's own** GitHub Actions is ON by default. Opt-out external delivery is prepared only for a verified HTTPS collector, which is NOT bundled or currently configured. Users can disable local or outbound delivery before first scheduled run. See [privacy and opt-out](docs/22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md).
- Never run untrusted repository code with elevated privileges or grant unnecessary tokens to jobs.

## Verification and security scope for v1.4

The v1.4 portable release gate covers source-bound Linux/Windows installation and regression checks, negative-path safety, privacy and archive readback. It does not certify security or correctness of an adopter's application, external model, host adapter or deployment. Treat the [current support matrix](docs/46_V1_4_PUBLIC_START_AND_SUPPORT.md) and [release notes](docs/47_V1_4_RELEASE_NOTES_AND_UPGRADE.md) as the public scope; the [v1.2 security audit](docs/25_V1_2_SECURITY_HARDENING_AUDIT.md) and [Windows integration acceptance plan](docs/26_L3_WINDOWS_PHYSICAL_ACCEPTANCE.md) remain historical references, not fresh v1.4 certification.

There is no claim of absolute security. Any new executable surface requires explicit threat modeling and revalidation.
