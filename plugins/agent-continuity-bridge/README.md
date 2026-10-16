# Agent Continuity Bridge (ACB) · ArquitecturaRepo v1.3

Optional, vendor-neutral *integration boundary* for external agent-continuity controllers. It lets ArquitecturaRepo inspect and locally register the integrity-pinned Codex Daily Control 3.1 release candidate **without** bundling it, overwriting an installed controller, assuming authority over Codex Goals or starting a native effect.

**Current support:** offline, read-only package verification and project-local plugin registration only. **Not supported/verified:** native Goal actions, app-server ownership handoff, quota activation, Windows Desktop closing, daypack delivery, or paid provider calls. The external 3.1 archive itself states live Windows/Codex validation was not performed. The bridge is an optional engineering candidate, **not** a production-certified v1.3 feature. The portable core needs no Codex account.

## Choose a language

[English](i18n/README_en.md) · [Español](i18n/README_es.md) · [Português](i18n/README_pt.md) · [Français](i18n/README_fr.md) · [Deutsch](i18n/README_de.md) · [Italiano](i18n/README_it.md) · [日本語](i18n/README_ja.md) · [中文](i18n/README_zh.md)

## Zero-side-effect usage (Python 3.10+)

From the unpacked bridge directory, with your **own separately obtained** 3.1 ZIP:

```bash
python "bridge.py" inspect --package "PATH_TO_YOUR_3_1_CONTROLLER.zip"
python "bridge.py" install --project "PATH_TO_EXISTING_AR_PROJECT" --package "PATH_TO_YOUR_3_1_CONTROLLER.zip"
python "bridge.py" status --project "PATH_TO_EXISTING_AR_PROJECT" --package "PATH_TO_YOUR_3_1_CONTROLLER.zip"
python "bridge.py" uninstall --project "PATH_TO_EXISTING_AR_PROJECT"
```

The `--project` directory must already contain `.agentic-sdlc/`. `inspect` checks the 3.1 manifest, all listed SHA-256, mandatory files, package version, slot consistency and path safety. Optional `--sha256` pins the exact archive. `install` creates only `.agentic-sdlc/plugins/agent-continuity-bridge/acb-registration.json`, containing generic schema/version + archive SHA-256; it writes **no new Product State** and does not copy controller ZIPs or configuration. `status` revalidates archive identity when `--package` is supplied. `uninstall` only removes an untouched registration that belongs to the plugin and leaves the external controller and project intact.

The bridge **never invokes** PowerShell, Codex CLI, Desktop, GUI, app-server, rclone or paid models. Native capability acceptance must be separately proven on an expressly authorized Windows host with real app-server receipts and permission enforcement; the plugin does not offer a hidden native invocation bypass. The external 3.1 controller's hardwired four-slot configuration is not compatible with arbitrary new projects without a separate generalized-controller engineering effort.

## Isolation and dependency boundaries

Only Python standard-library modules are needed for the bridge. Its tests use `pytest`. The external 3.1 controller is separately installable on Windows with appropriate PowerShell, Codex Desktop, Git, SQLite and any other configured optional integrations; these are **not** installed by the bridge. Do not import its personal `config/slots.json`, `config/drive.json`, project prompts, transcripts or archive into a public starter. No automatic controller installation, remote operations or startup hooks are created.

## QA and limitations

Run `python -m pytest -q tests` from this directory. Security tests include tampered manifests, malicious archive paths, duplicate case-insensitive names, unapproved versions, nonexistent source package, local registration tampering, uninstall isolation and privacy of report content. A passing test means the bridge's scoped offline features are verified, not that Codex Daily Control 3.1 works on a Windows machine. Do not promote support tier beyond `PACKAGE_VERIFIED_HOST_UNVERIFIED` without independent physical host tests.

Dependency diagnostic (no execution): `python "bridge.py" doctor --package "PATH_TO_YOUR_3_1_CONTROLLER.zip"`.
