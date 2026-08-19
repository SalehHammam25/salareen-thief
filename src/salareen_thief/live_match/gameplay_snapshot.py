"""Canonical gameplay snapshot serialization."""

import json

from .persistence import point, runtime_snapshot


def snapshot(adapter) -> str:
    outcome = adapter.state.outcome
    data = {
        "thief": point(adapter.state.positions.thief),
        "cop": point(adapter.state.positions.cop),
        "barriers": [point(item) for item in sorted(adapter.state.barriers)],
        "barrier_usage": adapter.state.barrier_usage,
        "valid_steps": adapter.state.valid_steps,
        "status": adapter.state.status.value,
        "outcome": None if outcome is None else outcome.kind.value,
        "capture_cause": None
        if outcome is None or outcome.capture_cause is None
        else outcome.capture_cause.value,
    }
    data.update(runtime_snapshot(adapter.scent, adapter.stage4))
    return json.dumps(data, sort_keys=True, separators=(",", ":"))
