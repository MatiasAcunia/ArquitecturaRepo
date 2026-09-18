# Client Boundary

## Objective

Keep the human in a CLIENT/product-owner-compatible role without excluding legitimate product participation.

"Do not bother the client with engineering" must never mean "the agents silently decide the product."

## Human-involvement classes

### SYSTEM_VERIFICATION

Correctness, invariants, currentness, regression, security, lineage and properties for which the system can construct a defensible evaluator.

System-owned.

### CLIENT_ACCEPTANCE

Taste, meaning, brand, product experience, business preference and genuinely subjective product judgment.

Client-owned.

### EXTERNAL_AUTHORIZATION

Credentials/access, paid/publication/external/irreversible actions and protected destructive operations not already delegated.

Client-owned.

### EVALUATOR_CAPABILITY_GAP

The system cannot establish a required property with sufficient confidence.

This is not automatic permission to turn the CLIENT into technical QA.

## Client-compatible interaction

Examples:

- final-product intent;
- priority or requirement changes;
- subjective visual/audio/UX feedback;
- business constraints;
- approval for a paid/external action;
- materially different product trade-offs.

## Technical client escape

Examples that should normally be system-owned:

- debugging;
- architecture selection;
- code review;
- state reconciliation;
- agent coordination;
- retry/fix selection;
- technical test interpretation;
- integration/recovery routing.

## Persist material chat decisions

When conversation changes material current intent:

1. preserve recoverable intent evidence when available;
2. classify decision strength;
3. update the canonical requirements/Product State owner;
4. mark superseded directions;
5. make the result reconstructible by a fresh agent.

Do not persist casual brainstorming as a hard requirement by literalism.

## Ask fewer, better questions

Ask one high-leverage CLIENT question when the answer can materially change product architecture, quality, recurring economics or business behavior.

Do not request generic feedback every iteration.
