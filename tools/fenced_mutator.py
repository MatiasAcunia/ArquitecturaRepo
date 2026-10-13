#!/usr/bin/env python3
"""Optional physical-writer fencing against the existing execution-authority owner.

Never grants authority. A real mutating adapter must hold this context for its
whole local critical section. External provider effects need a separate receipt.
"""
from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from state_tx import state_lock


class StaleMutatorHold(ValueError):
    pass


@contextmanager
def fenced_local_write(control: Path, *, actor_id: str, run_id: str,
                       mutator_epoch: int) -> Iterator[None]:
    if not actor_id or not run_id or type(mutator_epoch) is not int or mutator_epoch < 0:
        raise StaleMutatorHold("INVALID_MUTATOR_IDENTITY")
    control = control.resolve()
    with state_lock(control):
        path = control / "state" / "EXECUTION_AUTHORITY_CURRENT.json"
        if not path.is_file():
            raise StaleMutatorHold("CANONICAL_AUTHORITY_MISSING")
        data = json.loads(path.read_text(encoding="utf-8"))
        current = data.get("current_mutator")
        if (data.get("authority_status") != "ACTIVE" or
            not isinstance(current, dict) or
            data.get("mutator_epoch") != mutator_epoch or
            current.get("actor_id") != actor_id or
            current.get("run_id") != run_id or
            current.get("epoch") != mutator_epoch):
            raise StaleMutatorHold("STALE_OR_UNAUTHORIZED_MUTATOR")
        # Releasing the lock before local mutation defeats fencing. Do not do so.
        yield


if __name__ == "__main__":
    raise SystemExit("Only trusted mutation adapters may enter fenced_local_write.")
