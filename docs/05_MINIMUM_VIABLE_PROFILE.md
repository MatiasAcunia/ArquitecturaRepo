# Minimum Viable Agentic SDLC Profile

Use this profile for a small project or the first installation pass.

The goal is to obtain durable continuity and clean responsibility boundaries without importing the full complexity of a mature multi-agent system.

## Required mechanisms

### 1. Client boundary

The project must distinguish:

- product intent and preference;
- technical engineering work;
- external/paid/destructive authorization.

The CLIENT must not become the routine debugger or state reconciler.

### 2. Current CLIENT requirements

Maintain one canonical current requirements surface.

It must distinguish active decisions, open questions and superseded decisions.

### 3. Product State

Maintain one compact current Product State that points to:

- objective;
- capability state;
- active campaign;
- current gate;
- strongest evidence;
- next legal boundary.

### 4. Currentness Set

Define the minimum durable surfaces a fresh agent must read to reconstruct one coherent posture.

### 5. Planner / Campaign Lead split

Planner chooses the strategic capability and charter.

Campaign Lead owns tactical engineering until a true strategic terminal.

### 6. Campaign Charter

Every material implementation campaign should define:

- capability objective;
- owner/interface/state boundaries;
- protected resources;
- required gates;
- invalidation events;
- terminal evidence.

### 7. Exact-candidate acceptance

Acceptance must bind an exact candidate/ref/state.

A producer summary alone cannot establish readiness.

### 8. Fresh-context probe

Before scaling agent autonomy, verify that a fresh context can reconstruct:

- role;
- product objective;
- current requirements;
- Product State;
- active campaign;
- gate/evidence;
- next legal action.

## Optional mechanisms at this profile

Do not add these unless the project creates the corresponding failure class:

- portfolio MASTER OWNER;
- multiple workstream Planners;
- elastic specialist pools;
- dedicated Sentinel;
- artifact storage lifecycle;
- complex execution leases;
- multiple independent review lanes;
- provider/cost orchestration;
- rich interaction instrumentation;
- cross-repository currentness joins.

Start small. Add control only when evidence justifies it.
