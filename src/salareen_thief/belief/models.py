"""Immutable exact belief values and typed update results."""

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum

from salareen_thief.base_logic.state_types import Board, Coordinate

ZERO = Decimal("0")
ONE = Decimal("1")


@dataclass(frozen=True, slots=True)
class BeliefMap:
    board: Board
    probabilities: tuple[tuple[Decimal, ...], ...]

    def __post_init__(self) -> None:
        size = self.board.grid_size
        shape_ok = len(self.probabilities) == size and all(
            len(row) == size for row in self.probabilities
        )
        values = tuple(value for row in self.probabilities for value in row)
        valid = all(
            isinstance(value, Decimal) and value.is_finite() and ZERO <= value <= ONE
            for value in values
        )
        if not shape_ok or not valid or sum(values, ZERO) != ONE:
            raise ValueError("belief must be a normalized board distribution")

    def at(self, coordinate: Coordinate) -> Decimal:
        start = self.board.axis_start_index
        return self.probabilities[coordinate.row - start][coordinate.col - start]


class BeliefFallbackReason(StrEnum):
    ZERO_WEIGHT = "zero_weight"
    INVALID_EVIDENCE = "invalid_evidence"


@dataclass(frozen=True, slots=True)
class BeliefUpdated:
    belief: BeliefMap


@dataclass(frozen=True, slots=True)
class BeliefFallback:
    belief: BeliefMap
    reason: BeliefFallbackReason


BeliefResult = BeliefUpdated | BeliefFallback


def normalize_rows(
    values: tuple[tuple[Decimal, ...], ...]
) -> tuple[tuple[Decimal, ...], ...] | None:
    flat = [value for row in values for value in row]
    total = sum(flat, ZERO)
    if not total.is_finite() or total <= ZERO or any(value < ZERO for value in flat):
        return None
    normalized = [value / total for value in flat]
    index = max(position for position, value in enumerate(normalized) if value > ZERO)
    normalized[index] += ONE - sum(normalized, ZERO)
    width = len(values[0])
    return tuple(
        tuple(normalized[start : start + width])
        for start in range(0, len(normalized), width)
    )
