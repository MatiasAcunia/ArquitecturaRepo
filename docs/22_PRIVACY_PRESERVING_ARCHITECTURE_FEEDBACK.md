# Privacy-Preserving Architecture Feedback

The starter can generate recurring architecture-usage feedback without reading or exporting project content.

## Default behavior

New scaffolds install a managed GitHub Actions workflow at:

`.github/workflows/agentic-sdlc-feedback.yml`

and a project-local config at:

`.agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json`

Defaults:

- feedback generation: enabled;
- cadence: weekly;
- GitHub Actions artifact: enabled;
- external submission: disabled;
- privacy mode: `STRICT_METADATA_ONLY`.

The workflow also has a monthly schedule. The exporter only emits on the schedule that matches the configured cadence. Manual runs always work.

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

## External submission

External submission is deliberately two-key opt-in.

It occurs only when all of these are true:

1. `external_submission_enabled` is `true` in the feedback config;
2. repository variable `AGENTIC_SDLC_FEEDBACK_SUBMIT` is exactly `true`;
3. repository variable `AGENTIC_SDLC_FEEDBACK_ENDPOINT` contains an endpoint.

No personal access token is requested by the starter.

The endpoint must accept an unauthenticated JSON POST if this mode is used.

This allows a future maintainer-owned collector to receive the already-sanitized report without giving the starter credentials to the user's project.

Until a collector is explicitly configured, nothing is sent outside the repository's normal GitHub Actions artifact storage.

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
