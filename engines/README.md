# Engine navigation

This directory is the entrypoint for individually modeled engines. [catalog.json](catalog.json) is the complete machine-readable inventory; each listed `engine.json` links to its actual source, interface contract, tests and release evidence. These are links, not copies of code or mutable Product State.

- [Portable Goal Engineering](portable-goal/engine.json) · [design](portable-goal/DESIGN.md) · [contract](portable-goal/CONTRACT.md) · [history](portable-goal/CHANGELOG.md)
- [Repository operation rules](../AGENTS.md) · [documentation guide](../docs/README.md)

Portable read-only probe: `python tools/engine_registry.py validate-navigation --root .` (or `navigation` for the expanded path map). It checks every `engines/*/engine.json` is registered and that every declared source, test, contract and navigation path resolves safely. It does **not** grant execution authority, validate historical release bytes, or imply host/currentness/product acceptance. The existing strict `validate` command retains release verification.

Do not move code/evidence into this directory merely to make the tree look uniform. Follow the manifest to its canonical owner.
