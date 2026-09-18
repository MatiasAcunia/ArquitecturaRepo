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
- materially different product trade-offs;
- scope/exclusion clarification;
- target dates or hard external deadlines;
- where/how the product is expected to be used when that changes product behavior.

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

During initial product discovery, an intentional conversation is expected.

Ask coherent groups of high-leverage questions and synthesize between rounds. A useful default is 3-7 related questions per round rather than one-question-at-a-time interrogation.

After the baseline is coherent, return to sparse high-leverage questions only when the answer can materially change product behavior, quality, recurring economics, schedule or external authority.

Do not request generic feedback every iteration.

Before the first material campaign, ask one explicit baseline-confirmation question after presenting the complete current functional/non-functional/security/network/UI/data/cost/date/exclusion summary.

That confirmation is not a legal signature and must not be used to transfer technical architecture responsibility to the CLIENT.


## Architecture feedback consent

Recurring architecture feedback is process-improvement telemetry, not product authority.

A new scaffold may enable local strict-metadata report generation by default, but the CLIENT must be told that it exists and how to disable it.

External submission is different: it requires explicit CLIENT opt-in.

Do not treat silence as permission to transmit outside the repository's normal GitHub Actions artifact storage.

The feedback exporter must not include project identifiers, requirement text, code, paths, SHAs, free text, users, emails or credentials.
