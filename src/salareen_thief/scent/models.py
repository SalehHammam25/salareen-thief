"""Immutable scent observations without unresolved evolution semantics."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class ScentGrid:
    axis_start_index: int
    values: tuple[tuple[Decimal, ...], ...]

    def __post_init__(self) -> None:
        width = len(self.values[0]) if self.values else 0
        invalid_shape = (
            type(self.axis_start_index) is not int
            or not width
            or len(self.values) != width
            or any(len(row) != width for row in self.values)
        )
        invalid_value = any(
            not isinstance(value, Decimal)
            or not value.is_finite()
            or value < Decimal("0")
            or value > Decimal("0.9")
            for row in self.values
            for value in row
        )
        if invalid_shape or invalid_value:
            raise ValueError("invalid scent grid")

    def at(self, row: int, col: int) -> Decimal:
        return self.values[row - self.axis_start_index][col - self.axis_start_index]


@dataclass(frozen=True, slots=True)
class OpponentScent:
    """A peer-visible scent snapshot belonging only to its opponent."""

    turn: int
    grid: ScentGrid

    def __post_init__(self) -> None:
        if (
            isinstance(self.turn, bool)
            or not isinstance(self.turn, int)
            or self.turn < 0
        ):
            raise ValueError("turn must be a nonnegative integer")
