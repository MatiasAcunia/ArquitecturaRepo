# Review Freeze and Terminal Integrity

## Purpose

Prevent a producer from changing the object under review while retaining a favorable review certificate.

## Canonical review freeze

For a material terminal whose truth depends on mutable producer state, establish one exact review freeze before independent terminal review.

The freeze should bind, as applicable:

- exact code ref;
- exact configuration;
- exact schema/state identity;
- exact input population;
- exact artifacts/digests;
- exact current campaign/checkpoint identity.

Working-tree bytes or later summaries are not substitutes.

## Reviewer reconstruction

The reviewer should independently reconstruct enough of the frozen candidate to falsify material obligations.

A reviewer merely reading producer-populated PASS fields is not independent verification.

## Material obligation coverage

Before favorable terminal review, every material charter/DoD obligation must resolve to:

- independently supported/falsified; or
- explicitly not applicable with a defensible reason.

Unknown or self-asserted-only obligations block terminal PASS.

## Post-freeze mutation

A material producer mutation after review freeze invalidates the favorable review.

The correct sequence is:

`MUTATION -> NEW FREEZE -> FRESH REVIEW`

Do not retroactively edit the old review certificate.

## Relationship graph

Treat terminal truth as one relationship graph:

`current state -> execution authority -> checkpoint -> candidate -> review freeze -> reviewer run -> verdict -> terminal receipt`

Duplicated identities/digests across that graph must derive from one canonical source or be mechanically reconciled.

## Campaign cost/history integrity

Retry/review/rework history should not disappear from the campaign merely because the newest candidate is clean.

Current terminal evidence may summarize history, but it must not falsify the fact that prior work occurred.

## Planner acceptance

A favorable independent review returns a candidate to the strategic acceptance boundary.

It does not automatically satisfy a separate CLIENT/perceptual/release gate.
