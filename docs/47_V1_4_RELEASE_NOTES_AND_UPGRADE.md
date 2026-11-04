# ArquitecturaRepo v1.4.0 — public release notes and installation boundaries

ArquitecturaRepo is a Git-anchored, model-neutral Agentic SDLC starter. Version
1.4.0 consolidates the portable framework after v1.3.0. A GitHub branch or
source VERSION field alone is **not** evidence of publication: the release is
the immutable [v1.4.0 tag and GitHub Release](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0)
with a downloadable archive, checksum, and exact-source receipts.

## User-visible improvements

- Reusable public policy no longer embeds private maintainer workstream rules
  or retired internal execution reports.
- Read-only local Git/source currentness, source divergence and safe
  continuation diagnostics fail closed when code or canonical state is stale.
- Maintainable, versioned Python tools and proportional installation preserve
  backward-compatible portable contracts and optional runtime boundaries.
- First-time installation works in new and existing **ungoverned** application
  directories without rewriting user code or existing GitHub workflows.
- Installed state starts at `HOLD / UNTRUSTED_CONTEXT`; status, discovery and
  fresh-context reconstruction are runnable immediately after installing the
  declared Python validation dependency.
- A separate read-only attachment preflight exists for **already governed**
  projects; it is not a safe automatic in-place upgrade.
- A source-pinned public ZIP is built, CRC/readback verified, checked against
  committed Git blob bytes, extracted and used in Linux and Windows tests.
  Documented Bash and PowerShell command sequences are exercised separately.

## Install the actual published build

1. Open the [v1.4.0 GitHub Release](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0).
   If it does not exist or lacks verified assets, publication is not complete.
2. Download `ArquitecturaRepo-v1.4.0-portable.zip` and its matching
   `ArquitecturaRepo-v1.4.0-portable.zip.sha256`.
3. Verify the ZIP's SHA-256 against the published checksum, extract it, and
   use the [first-user guide](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/46_V1_4_PUBLIC_START_AND_SUPPORT.md).
4. For a fresh or ungoverned project, start with `SMALL` and the explicit
   `--no-feedback-workflow` switch if you do not want scheduled reports.
5. Existing v1.2/v1.3 governed projects **must not** be overwritten: begin
   with the [read-only attachment path](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/32_EXISTING_GOVERNED_ATTACHMENT.md).

An optional installer image may be provided at
`ghcr.io/matiasacunia/arquitecturarepo:1.4.0`. It is built only from the
verified public ZIP, never directly from a checkout containing `.git` history.
Inspect the registry visibility separately; a successful authenticated push
does not establish anonymous/public pull access.

## Verification and support limits

The complete `validate-starter` Linux and Windows matrix must pass against
the exact source. The publication workflow checks that the validated SHA is
still canonical `main`, builds the portable archive with a source-tree/byte
receipt, creates an immutable GitHub Release, downloads published assets and
rechecks the checksum and a real extraction/install. The optional GHCR build
is exercised in a disposable mounted project before publishing a versioned
container and then inspected from the registry.

Tests and artifacts do **not** certify native Codex Desktop operations,
universal model execution success, provider quotas/costs, customer projects,
real third-party database state or independent external-user usability.
Product acceptance, model choices, external permissions, security, licensing,
deployment and perceptual gates remain the adopter's own decision/evidence.
There is no bundled provider credential, managed cloud collector or automatic
agent billing. Local metadata feedback and separately configured outbound
telemetry are disclosed in [privacy controls](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/22_PRIVACY_PRESERVING_ARCHITECTURE_FEEDBACK.md).

## Compatibility, rollback, and confidentiality

- Historical `v1.3.0` assets and tag remain immutable. Roll back a fresh
  installation by choosing that immutable release; do not replace an active
  installed Product State, database or owner registry without its own reviewed
  migration/rollback procedure.
- New installations should use the versioned archive rather than copying
  arbitrary files from `main`. A standalone source ZIP does not carry a
  `.git` repository; users can create their own project history independently.
- The current distribution excludes private data and known retired internal
  paths by checked source policy. Historical public commits, forks and
  caches are not automatically erased by removing files from a new tree.
  No history-wide secrecy certification is implied; any actual historical
  disclosure requires a separately scoped remediation.

CLIENT explicitly approved E6 integration and v1.4.0 publication on
2026-11-04. The permission is recorded for governance; release status must be
derived from actual tag/assets, not from this text alone.
