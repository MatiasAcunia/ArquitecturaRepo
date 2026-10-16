#!/usr/bin/env python3
"""Regression tests for dependency-aware I3 next-action ranking."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import campaignctl


def unit(unit_id: str, *, status: str = "READY", priority: int = 0,
         dependencies: tuple[str, ...] = (), writes: tuple[str, ...] = (),
         resources: tuple[str, ...] = ()) -> dict:
    return {
        "id": unit_id, "status": status, "priority": priority,
        "dependencies": list(dependencies),
        "allowed_write_surfaces": list(writes),
        "shared_resources": list(resources),
    }


def main() -> int:
    state = {"work_units": [
        unit("A", priority=50),
        unit("B", status="BLOCKED_DEPENDENCY", priority=1, dependencies=("A",)),
        unit("C", priority=100),
        unit("D", priority=100),
    ]}
    ranked = campaignctl.rank_ready_work_units(state)
    assert [(entry[0]["id"], entry[1]) for entry in ranked] == [
        ("A", 2), ("C", 1), ("D", 1),
    ]

    parked_descendant = {"work_units": [
        unit("READY", priority=10),
        unit("PARKED_CHILD", status="PARKED", dependencies=("READY",)),
        unit("INDEPENDENT", priority=10),
    ]}
    ranked_parked = campaignctl.rank_ready_work_units(parked_descendant)
    assert [(entry[0]["id"], entry[1]) for entry in ranked_parked] == [
        ("INDEPENDENT", 1), ("READY", 1),
    ]

    # Once the dependent capability is complete, ordinary priority resolves
    # the independent ready work. Terminal descendants no longer inflate paths.
    state["work_units"][1]["status"] = "DONE"
    ranked = campaignctl.rank_ready_work_units(state)
    assert [entry[0]["id"] for entry in ranked] == ["C", "D", "A"]
    assert all(score == 1 for _, score in ranked)

    cycle = {"work_units": [
        unit("X", dependencies=("Y",)), unit("Y", dependencies=("X",)),
    ]}
    try:
        campaignctl.rank_ready_work_units(cycle)
    except campaignctl.CampaignError as exc:
        assert "dependency cycle" in str(exc)
    else:
        raise AssertionError("cyclic campaign graph received a next-action ranking")

    assert campaignctl.rank_ready_work_units({"work_units": []}) == []

    leased = {"work_units": [
        unit("ACTIVE", status="ACTIVE", writes=("src/api",), resources=("db:main",)),
        unit("WRITE_CONFLICT", priority=100, writes=("src/api/routes.py",)),
        unit("RESOURCE_CONFLICT", priority=90, resources=("db:main",)),
        unit("INDEPENDENT", priority=1, writes=("docs/guide.md",), resources=("db:other",)),
    ]}
    write_conflicts = campaignctl.active_conflicts(leased, leased["work_units"][1])
    resource_conflicts = campaignctl.active_conflicts(leased, leased["work_units"][2])
    assert write_conflicts == [{
        "work_unit_id": "ACTIVE", "kind": "write_surface", "surfaces": ["src/api/routes.py"]
    }]
    assert resource_conflicts == [{
        "work_unit_id": "ACTIVE", "kind": "shared_resource", "surfaces": ["db:main"]
    }]
    assert campaignctl.active_conflicts(leased, leased["work_units"][3]) == []
    print("CAMPAIGN PLANNING SELF-TEST PASSED (dependency path, priority, terminal and cycle cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
