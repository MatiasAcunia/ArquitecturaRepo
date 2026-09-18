# Adaptation Decision Tree

Use this before installing optional mechanisms.

## 1. How many independently planned product boundaries exist?

### One

Use one I2 Planner.

Do not activate a separate MASTER OWNER role unless there is a real shared/systemic layer to govern.

### Multiple workstreams contributing to one final product

Use one I2 per independently planned workstream plus a product-level integration/system owner.

Keep local volatile state isolated.

### Multiple separate products

Use one I2 per product/workstream. Add MASTER OWNER only for shared portfolio/process/runtime concerns.

## 2. Does the project own persistent state?

### No

The minimum profile may be enough.

### Yes

Install:

- state/DB/lineage/idempotency rules;
- migration/recovery evidence;
- current vs history semantics;
- currentness/readback gates.

## 3. Does the project generate many/large/expensive artifacts?

### Yes

Install:

- artifact lifecycle;
- storage preflight;
- lineage;
- cost/yield measurement;
- representative physical/perceptual evidence;
- cleanup reconciliation.

## 4. Are external APIs/services materially metered or time-sensitive?

### Yes

Install:

- cost/capacity/external service protocol;
- current provider/model/version binding;
- spend authority;
- idempotent/restartable external operations.

## 5. Does the project handle secrets, personal data, third-party rights or publication?

### Yes

Install:

- security/privacy/rights/external-action protocol;
- explicit release/authorization gates;
- synthetic or redacted test data.

## 6. Will multiple agents write concurrently?

### Yes

Install:

- identity/execution authority;
- capability DAG/isolation;
- singular integration owner;
- shared-resource serialization.

## 7. Is product quality partly semantic/perceptual?

### Yes

Keep machine correctness and product/human acceptance as separate gates.

Add representative exact-candidate review rather than using implementation tests as a proxy.

## 8. Will campaigns survive multiple sessions/context windows?

### Yes

Install durable:

- campaign identity;
- checkpoint;
- tactical DAG state;
- resume procedure;
- execution authority reconstruction.

## 9. Is there meaningful risk of stale/conflicting project state?

For any nontrivial long-running project, assume yes until disproven.

Define:

- Currentness Set;
- supersession rules;
- fresh-context test;
- fail-closed reconciliation.

## 10. Final minimization pass

For every installed mechanism ask:

- Which failure class requires this?
- Who owns it?
- How is it physically enforced/observed?
- How is it falsified?
- What simpler mechanism would be sufficient?

Remove mechanisms that cannot justify their cost.
