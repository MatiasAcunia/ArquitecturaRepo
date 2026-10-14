# Interaction Ledger

## Purpose

Preserve enough material CLIENT/Planner/agent interaction evidence to reconstruct product decisions and study whether technical responsibility leaked back to the human.

This ledger is evidence, not current engineering state.

## Capture when material

Record interactions that change:

- product requirements;
- product/business preference;
- acceptance/rejection;
- external/paid/publication authority;
- deadline/objective;
- model/runtime authority;
- development-system rules;
- strategic route.

Routine acknowledgements can be omitted.

## Hard truth rule

Archive only wording/evidence physically available.

Never reconstruct unavailable messages as verbatim.

If an interaction is known but unavailable, mark it unavailable and record only supported factual metadata.

## L0 vs L1

Interaction record = L0 evidence of what was said.

Normalized requirements/Product State = L1 current interpretation.

Do not use raw chat history as the only current authority.

## Client-escape classification

Where useful classify:

- CLIENT_COMPATIBLE;
- CLIENT_TECHNICAL_ESCAPE;
- NOT_APPLICABLE.

Absence of evidence is UNKNOWN, not proof that no technical escape occurred.

## Controlled reconciliation / supersession

For every material CLIENT correction, capture only recoverable evidence (source ref, time, actor, classification and supported decision meaning), link it to the corresponding normalized L1 current requirements and affected Product State surface, and identify supersession of contradictory historical decisions. Historic records are append-only unless a privacy deletion obligation applies; they are not parallel CURRENT requirements.

Reorganization may move/archive old theory within its owning repository, but must preserve lineage and mark dependent currentness invalid until reconciled. A mere chat message or Git commit cannot by itself certify acceptance, authorship, or consumption by an agent.
