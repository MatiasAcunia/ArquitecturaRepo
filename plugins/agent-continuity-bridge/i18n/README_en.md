# Agent Continuity Bridge — Agent Continuity Bridge 0.2.1

## Why it exists

ArquitecturaRepo coordinates engineering authority, plans and acceptance. This optional bridge supplies a separate, independently versioned boundary for an installed agent-continuity controller. It is not an AI model, a replacement campaign owner, or a scheduler. The portable ArquitecuraRepo core works without it.

## What currently works

Inspect a separately supplied Codex Daily Control 3.1 ZIP offline: check safe paths, inventory, every SHA-256, version and configuration consistency; register an immutable package digest in an existing project, inspect currentness and safely remove the registration. No bundled private controller, credentials, Goal IDs or project settings.

## Requirements and connection

Python 3.10 or newer; for installation, an existing ArquitecturaRepo project with a .agentic-sdlc directory; separately obtain your own 3.1 controller archive. Only running the controller itself on Windows additionally requires Windows PowerShell 5.1, compatible Codex Desktop/app-server, and separately configured Git, SQLite and optional Drive/rclone components. The bridge does not install or connect them.

## Safety and status

The 3.1 archive is a release candidate, not physically certified. Native close, Desktop handoff, quota-reactivation and remote delivery remain disabled/unverified here. A verified ZIP does not prove the controller works or authorize execution.

## CLI

```bash
python "bridge.py" inspect --package "CONTROLLER_3_1.zip"
python "bridge.py" install --project "MY_PROJECT" --package "CONTROLLER_3_1.zip"
python "bridge.py" status --project "MY_PROJECT" --package "CONTROLLER_3_1.zip"
python "bridge.py" uninstall --project "MY_PROJECT"
```


Project-local install: `python install_into_project.py --project "EXISTING_PROJECT"` then run `.agentic-sdlc/extensions/agent-continuity-bridge/pluginctl.py`. Remove any pinned controller registration first, then run `--remove`. No native controller is installed or executed.
