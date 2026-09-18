# Contributing

Contributions should improve the reusable Agentic SDLC structure without turning this repository into a snapshot of a real project.

## Structure-only rule

Do not contribute:

- personal names or emails;
- real source repository/branch names;
- commit SHAs copied from another project;
- credentials, hostnames or private paths;
- provider/account-specific balances or credits;
- real project campaign IDs;
- current private product state;
- proprietary artifacts or transcripts.

Use synthetic identifiers and examples.

## Contribution test

A contribution should answer:

1. Which generic failure class or responsibility boundary does this address?
2. What canonical owner should contain it?
3. Is a new permanent mechanism necessary?
4. How can a fork falsify whether it works?
5. Can the same value be achieved with less governance?

## Keep roles clean

Do not add another first-class role just because a specialist exists.

Prefer bounded I4 specializations unless a genuinely independent strategic planning boundary is required.

## Avoid policy duplication

Before adding a new protocol, identify whether an existing canonical owner can absorb the rule.

One concern should have one current owner.

## Evidence

Do not describe a mechanism as proven merely because:

- a document exists;
- a test exists;
- a producer says PASS;
- one synthetic example works.

Keep declared design, materialization, physical exercise and accepted capability distinct.

## Validation

Run:

```bash
python tools/validate_structure.py
```

before submitting changes.
