# Reference Project Layout

A fork does not need to preserve these exact filenames, but the ownership structure should remain clear.

## Small single-project example

```text
project/
├─ AGENTS.md
├─ state/
│  ├─ CLIENT_REQUIREMENTS_CURRENT.md
│  ├─ PRODUCT_STATE_CURRENT.json
│  ├─ CURRENT_BOOTSTRAP_STATE.json
│  ├─ IDENTITY_REGISTRY_CURRENT.json          # optional
│  └─ EXECUTION_AUTHORITY_CURRENT.json        # optional
├─ governance/
│  └─ PROJECT_OVERLAY.md
├─ campaigns/
│  └─ CAMPAIGN_001/
│     ├─ CHARTER.json
│     ├─ CHECKPOINT_CURRENT.json
│     └─ TERMINAL.json
├─ interactions/                              # optional but recommended for material client decisions
├─ src/
├─ tests/
└─ ...
```

## Multi-workstream product

Prefer:

```text
shared-owner/
  shared process/current cross-workstream authority only

workstream-alpha/
  local Product State
  local Planner overlay
  local campaigns
  local implementation

workstream-beta/
  local Product State
  local Planner overlay
  local campaigns
  local implementation
```

Do not copy volatile local Product State into a shared OWNER repository merely to make a dashboard convenient.

## Multi-product portfolio

Each product remains authoritative for its own current product/engineering state.

MASTER OWNER keeps only:

- shared process/runtime authority;
- cross-product/portfolio strategy when genuinely shared;
- systemic findings/routes;
- compact pointers needed for portfolio reconciliation.

## Naming rule

Names are less important than ownership.

A repository can use different paths if a fresh agent can answer:

- where current CLIENT requirements live;
- where Product State lives;
- what the Currentness Set is;
- what activates execution;
- where the active campaign checkpoint lives;
- what evidence establishes acceptance.
