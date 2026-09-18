# Product Discovery, Stack Frame and Delivery Planning

Version 1.1 adds a pre-campaign planning baseline for new scaffolds.

The goal is to prevent this failure mode:

`vague product idea -> random stack -> coding starts -> requirements appear midstream -> dates drift -> security/network/deployment are discovered late`.

The intended route is:

`conversation -> requirements baseline -> CLIENT confirmation -> technical baseline -> dated delivery plan -> baseline guard -> engineering campaign`.

## CLIENT conversation

The Planner actively asks product questions early.

It should understand users, workflows, data, scope, quality, environment, security, cost and timing.

The CLIENT is not expected to choose frameworks, DB engines, ports, migration tools, Git branches or test frameworks.

## Requirements confirmation

The canonical requirements file records:

- baseline status;
- baseline version;
- CLIENT confirmation;
- confirmation timestamp.

Confirmation is not a legal signature.

It means the Planner can engineer against one explicit current baseline.

Requirements remain changeable.

## Technical baseline

`state/TECHNICAL_BASELINE_CURRENT.json` persists the Planner-owned stack frame.

It includes environment/machine capability, stack, security, networking, UI strategy, operations/recovery and costs.

This avoids casual stack drift across contexts.

## Delivery plan

`state/DELIVERY_PLAN_CURRENT.json` persists target dates and milestone outcomes.

Each milestone has a target date, done condition, dependencies and confidence.

Date changes are explicit history, not silent edits.

## Baseline guard

```bash
python .agentic-sdlc/tools/baseline_guard.py --control-root .agentic-sdlc
```

For new scaffolds, `campaignctl init` refuses to create a material campaign while this gate is blocked.

Older installations without these baseline surfaces keep backward compatibility until they deliberately adopt the new mechanism.

## Project status

The human-facing tracker is derived rather than duplicated:

```bash
python .agentic-sdlc/tools/project_status.py --control-root .agentic-sdlc
```

It reports Product State, current gate, baseline readiness, deployment/network posture, target release, next milestone, overdue milestones, blockers and next legal boundary.

## Simple UI default

When high visual polish is not a product requirement, the technical baseline should normally choose a simple functional UI.

The system still verifies broken controls, validation, navigation, error/empty states and obvious layout defects.

## Operating review

`governance/AGENTIC_SDLC_OPERATING_REVIEW_CURRENT.md` records how well the architecture is working in actual use without becoming a second Product State.

For one project it is Planner-managed. In a portfolio installation, the MASTER OWNER may aggregate/systemically reconcile these reviews.

## Security/network examples

A local-only CRUD can explicitly choose localhost-only exposure and avoid unnecessary Internet security machinery.

A LAN or Internet product requires correspondingly stronger authentication, secrets, firewall/TLS, backup and operational controls.

The important property is not maximum complexity. It is an explicit posture appropriate to real exposure.
