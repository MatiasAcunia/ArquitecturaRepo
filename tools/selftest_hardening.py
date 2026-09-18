#!/usr/bin/env python3
from __future__ import annotations

import json
import py_compile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"


def require_absent(path: Path, fragments: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for fragment in fragments:
        if fragment in text:
            raise AssertionError(f"{path.name} reintroduced duplicated primitive: {fragment}")


def main() -> int:
    for path in sorted(TOOLS.glob("*.py")):
        py_compile.compile(str(path), doraise=True)

    campaignctl = TOOLS / "campaignctl.py"
    migrate = TOOLS / "migrate_state.py"
    adoption = TOOLS / "apply_adoption.py"

    require_absent(
        campaignctl,
        [
            "def campaign_lock(",
            "def recover_pending_transaction(",
            "def transaction_write_json(",
            "def sha256_file(",
            "def fsync_dir(",
        ],
    )
    require_absent(
        migrate,
        [
            "def migration_lock(",
            "def atomic_json(",
            "def fsync_dir(",
        ],
    )

    for path in (campaignctl, migrate, adoption):
        text = path.read_text(encoding="utf-8")
        if "state_tx" not in text:
            raise AssertionError(f"{path.name} does not use shared state_tx primitives")

    profiles = json.loads((ROOT / "profiles" / "profiles.json").read_text(encoding="utf-8"))
    small = profiles["profiles"]["SMALL"]
    if small["optional_protocols"] != []:
        raise AssertionError("SMALL profile accumulated optional governance")

    manifest = json.loads(
        (ROOT / "state" / "STARTER_MANIFEST.json").read_text(encoding="utf-8")
    )
    core = manifest["core_protocols"]
    if len(core) != len(set(core)):
        raise AssertionError("core protocol list contains duplicates")

    if "MASTER_OWNER_OS" in core:
        raise AssertionError("MASTER OWNER must remain optional, not core")

    if "STATE_DB_LINEAGE_AND_IDEMPOTENCY" in core:
        raise AssertionError("stateful protocol must remain optional for SMALL projects")

    if (ROOT / "tools" / "campaignctl.py").name not in {"campaignctl.py"}:
        raise AssertionError("unexpected runtime surface")

    print("HARDENING SELF-TEST PASSED")
    print("- all Python tools compile")
    print("- campaign runtime uses shared state_tx primitives")
    print("- schema migrations use shared state_tx primitives")
    print("- adoption uses shared state_tx primitives")
    print("- SMALL profile carries no optional protocols")
    print("- MASTER OWNER/stateful machinery remain outside the core set")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
