"""Immutable scent observations without unresolved evolution semantics."""

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScentGrid:
    values: tuple[tuple[float, ...], ...]

    def __post_init__(self) -> None:
        width = len(self.values[0]) if self.values else 0
        invalid_shape = not width or any(len(row) != width for row in self.values)
        invalid_value = any(
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or value < 0
            or value > 0.9
            for row in self.values
            for value in row
        )
        if invalid_shape or invalid_value:
            raise ValueError("invalid scent grid")


@dataclass(frozen=True, slots=True)
class OpponentScent:
    """A peer-visible scent snapshot belonging only to its opponent."""

    turn: int
    grid: ScentGrid

    def __post_init__(self) -> None:
        if isinstance(self.turn, bool) or not isinstance(self.turn, int) or self.turn < 0:
            raise ValueError("turn must be a nonnegative integer")
