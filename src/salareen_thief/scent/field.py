"""Exact deterministic scent-field arithmetic."""

from decimal import Decimal

from salareen_thief.base_logic.state_types import Board, Coordinate

from .models import ScentGrid

ZERO = Decimal("0")
RINGS = (Decimal("0.9"), Decimal("0.6"), Decimal("0.3"))
DECAY = Decimal("0.10")


def empty_field(board: Board) -> ScentGrid:
    row = (ZERO,) * board.grid_size
    return ScentGrid(board.axis_start_index, (row,) * board.grid_size)


def emit(board: Board, center: Coordinate) -> ScentGrid:
    rows: list[tuple[Decimal, ...]] = []
    for row in range(board.axis_start_index, board.maximum_index + 1):
        values: list[Decimal] = []
        for col in range(board.axis_start_index, board.maximum_index + 1):
            ring = max(abs(row - center.row), abs(col - center.col))
            values.append(RINGS[ring] if ring < len(RINGS) else ZERO)
        rows.append(tuple(values))
    return ScentGrid(board.axis_start_index, tuple(rows))


def decay(field: ScentGrid) -> ScentGrid:
    factor = Decimal("1") - DECAY
    values = tuple(
        tuple(max(ZERO, value * factor) for value in row) for row in field.values
    )
    return ScentGrid(field.axis_start_index, values)


def maximum(left: ScentGrid, right: ScentGrid) -> ScentGrid:
    if left.axis_start_index != right.axis_start_index:
        raise ValueError("scent origins differ")
    if len(left.values) != len(right.values):
        raise ValueError("scent dimensions differ")
    values = tuple(
        tuple(max(first, second) for first, second in zip(a, b, strict=True))
        for a, b in zip(left.values, right.values, strict=True)
    )
    return ScentGrid(left.axis_start_index, values)


def evolve(field: ScentGrid, board: Board, position: Coordinate) -> ScentGrid:
    """Decay the old field, then maximum-aggregate a clipped new emission."""
    return maximum(decay(field), emit(board, position))
