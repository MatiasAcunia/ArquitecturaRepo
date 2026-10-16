#!/usr/bin/env python3
"""Public v1.3 release-contract negative test. Never executes any release action."""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
assert (ROOT/'VERSION').read_text().strip() == '1.3.0'
manifest = json.loads((ROOT/'state/STARTER_MANIFEST.json').read_text())
assert manifest['version'] == '1.3.0' and manifest['status'] == 'PUBLIC_STARTER_STABLE'
manual = (ROOT/'.github/workflows/publish-v1-3-manual.yml').read_text()
auto = (ROOT/'.github/workflows/publish-version-release.yml').read_text()
ci = (ROOT/'.github/workflows/validate-starter.yml').read_text()
notes = (ROOT/'docs/43_V1_3_RELEASE_NOTES_AND_UPGRADE.md').read_text()
assert 'workflow_dispatch:' in manual and 'workflow_run:' not in manual and 'push:' not in manual
assert "github.ref == 'refs/heads/main'" in manual
assert "github.actor == 'MatiasAcunia'" in manual
assert 'RELEASE_V1_3_0' in manual and 'exact_commit_sha' in manual
assert 'gh release create' in manual and 'git ls-remote origin refs/heads/main' in manual
assert '1.3.0)' in auto and 'skip=true' in auto and auto.count("steps.identity.outputs.skip != 'true'") == 2
assert 'python tools/selftest_v13_installed_lifecycle.py' in ci
assert ci.count('run: python tools/selftest_v13_installed_lifecycle.py') == 2
assert 'no automatic in-place upgrade' in notes.lower() and 'release candidate' in notes.lower()
assert 'codex desktop' in notes.lower()
assert (ROOT/'LICENSE').read_text().startswith('MIT License')
print('V1.3 RELEASE CONTRACT PASSED — manual-only tag, exact SHA, installer matrix, no upgrade/native claims')
