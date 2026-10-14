# Privacy-Preserving Architecture Feedback

The starter can generate recurring architecture-usage feedback without reading or exporting project content.

The minimal monthly report is ON by default so the project owner can inspect structural adoption friction, error categories, recovery frequency and setup issues. This can help improve the starter architecture and organize engineering-process data. The report is stored in the adopter's own GitHub Actions artifacts; it is not silently delivered to the starter maintainer.

## Default behavior

New scaffolds install a managed GitHub Actions workflow at:

`.github/workflows/agentic-sdlc-feedback.yml`

and a project-local config at:

`.agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json`

Defaults:

- feedback generation: enabled;
- cadence: monthly (automatically scheduled, where GitHub Actions schedules are active);
- GitHub Actions artifact: enabled;
- external submission preference: on once a verified HTTPS collector has been configured; without one, transport cannot run and local artifacts remain the only delivery;
- privacy mode: `STRICT_METADATA_ONLY`.

The managed workflow schedules one monthly run by default. The exporter emits only when the configured cadence matches its trigger; manual dispatch remains available. Users who prefer weekly feedback may configure their own schedule and cadence explicitly.

## What the report can contain

Only allowlisted metadata:

- starter version;
- selected profile;
- whether the optional runtime is installed;
- validator pass/fail;
- bootstrap/product status enums;
- currentness verified boolean;
- current owner count;
- capability count;
- whether a campaign is active;
- whether a transaction is pending;
- whether the project baseline is ready;
- technical baseline status;
- machine-assessment status;
- network exposure category;
- delivery-plan status;
- milestone count;
- overdue milestone count;
- schedule-change count;
- campaign status;
- work-unit status counts;
- retry/failure/HOLD/review-invalidation/recovery event counts;
- operating-review rating enum.

## What is deliberately excluded

The report contract declares and the self-test verifies that it contains no:

- repository or product names;
- project identifiers;
- requirements text;
- code;
- file paths;
- commit/code refs or SHAs;
- free text;
- usernames;
- email addresses;
- credentials or secrets.

No stable installation identifier is generated, so reports are not designed to track a specific project across time.

## Local artifact

The default workflow uploads the report as a GitHub Actions artifact for 30 days.

This provides an inspectable file and a workflow-run link without modifying the project repository.

The workflow uses read-only repository permissions.

Scheduled GitHub Actions run on the default branch. On public repositories GitHub may disable schedules after a long inactivity period; manual dispatch remains available.

## v1.2 outbound defaults and absence of a collector

The default is **opt-out for minimized reporting** requested by the project maintainer. The installer prominently prints a report/recipient notice, links the exact JSON schema and documents the disable switches. No collector address is included in this candidate: **there is currently no physical route to send those reports to the maintainer**. Claiming central reception would be false.

If a future verified maintainer endpoint is set through `AGENTIC_SDLC_FEEDBACK_ENDPOINT`, the managed job may send the allowlisted report each month unless `external_submission_enabled=false`, `enabled=false`, or repository variable `AGENTIC_SDLC_FEEDBACK_SUBMIT=false`. A network request is prohibited on missing endpoint, unsafe destination, invalid categories, or missing consent/privacy disclosures. Output remains in the adopter's repo; recipient replies must echo exact SHA256 receipt. No stable tracking identifier or source/repository URL is transmitted; a server may still observe network timestamps/runner metadata, so do not promise mathematically untraceable anonymity.

No source code, prompts, file paths, usernames, tokens, client/business details or free-text error strings leave the project. Event categories are fixed, bounded numeric counts; this does not diagnose causality. User choices override automatic delivery without impacting SDLC operation. Disable before the first scheduled run by reading the generated README and config.

## External submission

External submission is preference-on after a verified collector exists and remains explicitly opt-out. The collector is NOT configured in the current release candidate.

It occurs only when all of these are true:

1. `external_submission_enabled` is `true` in the feedback config (default);
2. repository variable `AGENTIC_SDLC_FEEDBACK_SUBMIT` is not `false` (user opt-out);
3. repository variable `AGENTIC_SDLC_FEEDBACK_ENDPOINT` contains a verified, intended collector endpoint.

No personal access token is requested by the starter.

The endpoint must accept an unauthenticated JSON POST if this mode is used.

This allows a future maintainer-owned collector to receive the already-sanitized report without giving the starter credentials to the user's project.

Until a collector is physically configured, nothing is sent outside the repository's normal GitHub Actions artifact storage. The status must be reported as NOT_CONFIGURED, not SENT.

## Disable it

Any of these is sufficient:

- set `enabled` to `false` in `feedback/ARCHITECTURE_FEEDBACK_CONFIG.json`;
- delete `.github/workflows/agentic-sdlc-feedback.yml`;
- install with `--no-feedback-workflow`.

Disabling feedback does not affect validation, planning, runtime or product behavior.

## Why this is separate from Product State

Architecture feedback is process-improvement evidence.

It is not product authority, currentness authority or acceptance evidence.

The config and operating-review surfaces have owners, but they are not required members of Product State currentness.

## Security posture

The exporter performs no network requests.

Only the managed workflow can perform an optional HTTP POST, and only after explicit repository configuration.

The workflow requests `contents: read` and no write permission.

A user should review changes to the managed workflow just like any other CI code, because any executable workflow in a repository is part of that repository's trust boundary.
