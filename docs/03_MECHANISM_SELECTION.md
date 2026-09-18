# Mechanism Selection Criteria

This repository contains reusable Agentic SDLC structure only.

It intentionally excludes any source project's names, repositories, branches, identifiers, providers, budgets, product counts, artifacts, prompts, current queues, private state and historical transcripts.

## What belongs in the starter

A mechanism belongs here only when it is:

1. domain-agnostic enough to reuse;
2. connected to a concrete failure class or responsibility boundary;
3. useful without private or project-specific state;
4. expressible as a compact protocol, template, schema or executable check;
5. falsifiable in a fork.

## Reusable mechanism families

The starter may contain generic mechanisms for:

- role and authority boundaries;
- client/product authority;
- currentness and supersession;
- fresh-context reconstruction;
- Product State versus Engineering State;
- capability planning;
- campaign delegation;
- tactical execution and recovery;
- independent review;
- layered verification gates;
- resource/write isolation;
- interaction provenance;
- artifact lifecycle;
- systemic escalation;
- governance minimization.

## What does not belong

Do not add:

- real project names;
- real repository names or branch names;
- exact commit SHAs from another project;
- private paths, hosts, accounts or identities;
- provider/account-specific credits or prices;
- real product quantities or schedules;
- current campaign IDs from another system;
- copied historical decisions;
- proprietary prompts or artifacts;
- domain rules that are not needed by a generic SDLC.

## Examples

Use synthetic placeholders such as:

- `PROJECT_A`
- `WORKSTREAM_ALPHA`
- `CAPABILITY_AUTH`
- `CAMPAIGN_001`
- `example/repo@main`

Examples must teach the mechanism without revealing or depending on a real source project.
