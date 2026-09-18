# Product Discovery, Requirements and Technical Baseline

## Purpose

Require real product discovery and engineering planning before a material engineering campaign begins.

The Planner must behave like a technical consultant: understand what the CLIENT wants, reconstruct the operating environment, normalize requirements, choose and persist a technical baseline, define security/network/deployment assumptions, and create a dated delivery plan.

This protocol does not transfer technical decisions to the CLIENT.

## Required planning sequence

For a new product or materially re-anchored product:

`DISCOVER -> INTERVIEW -> SYNTHESIZE -> CLIENT BASELINE CONFIRMATION -> TECHNICAL BASELINE -> DELIVERY PLAN -> BASELINE GATE -> CAMPAIGN`.

Do not jump from a vague idea directly into implementation.

## Product discovery conversation

The Planner opens with a real product conversation and learns:

- who uses the product and why;
- primary workflows and CRUD/business operations;
- data and business rules;
- must-have functions and explicit exclusions;
- non-functional expectations;
- interface expectations;
- where the product will run;
- local/LAN/Internet/cloud exposure;
- security/privacy;
- backup/recovery;
- budget/paid services;
- target dates/deadlines.

Ask coherent groups of high-leverage questions. A useful default is 3-7 related questions per round, then summarize what was understood.

When physical evidence can answer a technical question, inspect it instead of asking the CLIENT. Examples: OS, CPU/RAM/storage, existing project files, package manager, DB and tests.

Do not scan external networks or protected infrastructure without authority.

## Requirements baseline

The canonical CLIENT requirements surface distinguishes:

- product objective;
- functional requirements;
- non-functional requirements;
- data/state requirements;
- UI/UX requirements;
- security/privacy requirements;
- deployment/network requirements;
- performance/reliability;
- backup/recovery;
- budget/cost;
- target dates/deadlines;
- explicit exclusions;
- open questions;
- superseded decisions.

Before the first material campaign, the Planner presents one compact baseline review.

The CLIENT confirmation means only:

> this document accurately represents my current product requirements, known exclusions and target expectations.

It is not a legal signature and it is not approval of technical architecture.

Requirements may evolve later. Material changes are persisted, versioned/superseded and reconciled against architecture and schedule.

## Technical baseline / stack frame

After product requirements are coherent, the Planner owns the technical baseline.

Persist at least:

- development/runtime OS assumptions;
- deployment target;
- available machine/resources when material;
- network exposure model;
- language/runtime;
- backend;
- frontend/UI;
- database/persistence/migrations;
- package/dependency management;
- test strategy;
- state/transaction/idempotency semantics when material;
- authentication/authorization;
- secrets handling;
- data classification;
- backup/recovery;
- listen/bind/port/TLS/firewall assumptions when networked;
- UI quality strategy;
- observability/logging;
- paid/external services and recurring cost assumptions;
- rationale and unresolved technical risks.

The stack frame is CURRENT until deliberately superseded.

A material stack change requires evidence, impact analysis and explicit supersession. Do not casually reselect frameworks or databases during ordinary implementation.

## Machine and environment assessment

When the product runs on a known machine, record only the useful capability summary:

- OS family/version;
- CPU summary;
- RAM;
- free storage;
- GPU only if relevant;
- expected users/processes;
- network mode;
- deployment constraints.

Do not persist usernames, passwords, host secrets or unrelated personal paths.

## Security and networking

Security depth is proportional to exposure.

### Local single-user

- localhost-only by default;
- no external exposure unless requested;
- local DB ownership and backup;
- secrets outside source control;
- explicit recovery.

### LAN / multi-user

- explicit authentication decision;
- least privilege;
- firewall/bind scope;
- backup/recovery;
- concurrent-write semantics.

### Internet-facing

- authentication/session security;
- authorization when needed;
- TLS;
- secrets management;
- request protections;
- dependency/update policy;
- abuse controls when applicable;
- backup/recovery;
- safe logging;
- deployment/rollback.

Simple is allowed. Unspecified is not.

## UI quality

If bespoke visual polish is not a product requirement, prefer a simple, coherent interface over decorative complexity.

The system should verify:

- controls work;
- forms validate;
- labels/actions are understandable;
- navigation is not broken;
- supported screens do not visibly overflow/break;
- loading/empty/error states are coherent when material;
- destructive actions are not accidental.

The CLIENT owns taste. The system owns obvious functional defects.

## Delivery plan and dates

Every material milestone has:

- target date;
- capability/outcome;
- dependencies;
- done condition;
- confidence;
- risks/assumptions.

The overall plan has:

- planning start date;
- target release date when one exists;
- next schedule review date;
- external deadlines;
- schedule risks.

Dates are forecasts/targets unless explicitly hard external deadlines.

Use HIGH/MEDIUM/LOW confidence rather than fake certainty.

If a date changes, record the old date, new date and reason. Do not silently slide the plan.

## Status tracker

Do not create a second manual truth for project status.

Derive the human-facing tracker from Product State, requirements baseline, technical baseline, delivery plan and active campaign/checkpoint.

## Operating review / pilot evidence

Keep a small project-local operating review separate from product truth.

Record:

- quality of Planner questions;
- technical questions that escaped to CLIENT;
- schedule forecast quality;
- execution/recovery problems;
- repository/commit/sync/workspace incidents;
- what worked;
- what created friction;
- corrective action and owner;
- next review date.

This exists to improve the Agentic SDLC from real use.

## Pre-campaign baseline gate

For new scaffolds that materialize baseline surfaces, a material campaign is blocked until:

- requirements baseline is CLIENT_CONFIRMED;
- technical baseline is CURRENT;
- technical unresolved list is empty for campaign-blocking decisions;
- delivery plan is CURRENT;
- target dates and milestone done conditions exist;
- delivery unresolved list is empty for campaign-blocking decisions.

The baseline guard is a planning gate, not product acceptance.
