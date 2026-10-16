#!/usr/bin/env python3
"""Versioned optional-plugin consumer for ArquitecturaRepo.

Only imports the pinned, repository-owned optional bridge module; never imports
or runs untrusted externally supplied controller ZIPs or scripts.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BRIDGE = REPO_ROOT / 'plugins' / 'agent-continuity-bridge' / 'bridge.py'


def main(argv: list[str] | None = None) -> int:
    if not BRIDGE.is_file() or BRIDGE.is_symlink():
        print('HOLD: Agent Continuity Bridge not installed in this ArquitecturaRepo source tree', file=sys.stderr)
        return 2
    spec = importlib.util.spec_from_file_location('_ar_optional_agent_continuity', BRIDGE)
    if spec is None or spec.loader is None:
        print('HOLD: verified plugin module unavailable', file=sys.stderr)
        return 2
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.main(argv)


if __name__ == '__main__':
    raise SystemExit(main())
