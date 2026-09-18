# Fresh-Context Reconstruction Test

## Purpose

The architecture is not durable if it works only while the original conversation remains in context.

This test checks whether a fresh agent can reconstruct the project's legal current posture from durable evidence.

## Preconditions

- use a new conversation/session/context;
- do not provide a narrative handoff;
- provide only repository access and, if necessary, the exact target repository identity;
- do not answer technical questions during the probe unless the test explicitly records them as a failure/escape.

## Probe questions

The fresh agent must determine:

1. What product or workstream am I operating?
2. What is my role and what am I not allowed to own?
3. What current CLIENT requirements apply?
4. What unresolved product questions remain?
5. What is the current Product State?
6. What code/ref/runtime state is current?
7. Is there an active campaign?
8. If active, what charter and checkpoint/terminal govern it?
9. What verification gate is currently open?
10. What is the strongest physical evidence for the current claim?
11. What actions are legal now?
12. What actions are forbidden until another gate/authority transition?
13. What is the next strategic or tactical boundary?
14. What facts remain UNKNOWN?

## Hard failures

The probe fails if the fresh agent:

- uses historical/superseded state as current;
- activates prepared-but-inactive work;
- treats worker self-report as product acceptance;
- invents runtime/DB truth not present in evidence;
- asks the CLIENT to reconcile technical state already recoverable from the project;
- cannot identify its role boundary;
- cannot identify the next legal boundary;
- silently chooses between contradictory current owners.

## Pass classes

### PASS_STRONG

Correctly reconstructs all material authority/currentness and next-action boundaries without technical CLIENT rescue.

### PASS_WITH_LIMITATION

Core posture is correct, but one bounded non-critical UNKNOWN remains and is explicitly held.

### FAIL_RECONSTRUCTION

Material state/authority/route is wrong or unrecoverable.

### INVALID_APPARATUS

The test environment itself lacks access to evidence that the architecture expected it to read.

Do not convert INVALID_APPARATUS into a project failure.

## After a failure

Repair the causal continuity mechanism:

- navigation;
- canonical ownership;
- currentness transition;
- supersession;
- missing Product State pointer;
- checkpoint completeness;
- evidence availability.

Do not solve the test by giving the next fresh agent a larger narrative prompt.
