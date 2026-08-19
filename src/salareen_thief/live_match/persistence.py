"""Durable Stage 4 and scent runtime state."""

import json
from decimal import Decimal
from typing import Any

from salareen_thief.scent.models import ScentGrid


def point(value: Any) -> list[int]:
    return [value.row, value.col]


def restore_runtime(saved: str, current: ScentGrid, stage4: Any) -> ScentGrid:
    data = json.loads(saved)
    stage4.restore(data.get("stage4"))
    values = data.get("scent")
    if values is None:
        return current
    rows = tuple(tuple(Decimal(value) for value in row) for row in values)
    return ScentGrid(data["scent_axis"], rows)


def runtime_snapshot(scent: ScentGrid, stage4: Any) -> dict[str, Any]:
    return {
        "scent_axis": scent.axis_start_index,
        "scent": [[str(value) for value in row] for row in scent.values],
        "stage4": stage4.snapshot(),
    }
