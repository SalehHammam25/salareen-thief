"""Deterministic action values, independent of strategy."""

from dataclasses import dataclass
from enum import StrEnum

from .state_types import CaptureCause, Coordinate, Role


class MoveChoice(StrEnum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    STAY = "STAY"


@dataclass(frozen=True, slots=True)
class MoveAction:
    role: Role
    choice: MoveChoice
    target: Coordinate | None = None


@dataclass(frozen=True, slots=True)
class BarrierAction:
    role: Role
    target: Coordinate
    capture_claim: "CaptureClaim | None" = None


@dataclass(frozen=True, slots=True)
class CombinedAction:
    role: Role
    move: MoveChoice
    barrier_target: Coordinate


@dataclass(frozen=True, slots=True)
class CaptureClaim:
    role: Role
    cause: CaptureCause


Action = MoveAction | BarrierAction | CombinedAction | CaptureClaim
