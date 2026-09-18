# Security, Privacy, Rights and External Actions

## Scope

Use this protocol when a project handles secrets, personal data, third-party content/licenses, paid services, publication, destructive actions or other external side effects.

Small projects may only need a subset.

## Secrets

- never persist credentials in the repository;
- do not place tokens in logs, prompts, evidence bundles or example fixtures;
- use the platform's secret store/environment mechanism;
- treat secret availability as external authority, not a reason to weaken tests;
- rotate/revoke compromised credentials outside normal campaign mutation authority.

## Privacy

Before material use of personal/sensitive data, establish:

- legitimate purpose;
- minimum necessary data;
- storage owner;
- retention/deletion semantics;
- access boundary;
- logging/redaction behavior;
- external transfer/processors;
- release/test data restrictions.

Synthetic fixtures are preferred for public examples and routine tests.

## Rights / licenses

For third-party code, media, models, datasets or generated assets, track as applicable:

- source;
- license/terms;
- permitted use;
- attribution obligations;
- redistribution restrictions;
- modification rights;
- commercial-use restrictions;
- model/provider terms;
- exact lineage into final artifacts.

Unknown material rights status is a HOLD for the affected release/use gate.

## External actions

Classify actions before execution:

### INTERNAL_REVERSIBLE

Normal repository/test/campaign work inside delegated authority.

### EXTERNAL_REVERSIBLE

External side effect that can be safely reverted but still requires explicit current authority where policy says so.

### EXTERNAL_COSTED

Consumes paid quota/credits or creates financial liability.

### EXTERNAL_PUBLICATION

Publishes or distributes externally.

### DESTRUCTIVE_PROTECTED

Deletes/modifies protected, accepted, user-managed or external state.

The last three categories normally require an explicit authority envelope and may require CLIENT authorization.

## Evidence

A test proving API syntax does not prove:

- terms allow the intended use;
- credentials are authorized;
- cost is acceptable;
- publication is approved;
- data handling is compliant.

Keep these gates distinct.

## Fail closed

When authority, rights, privacy or destructive scope is materially uncertain, stop the affected external action while allowing unrelated internal work to continue.
