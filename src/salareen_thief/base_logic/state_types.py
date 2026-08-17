"""Immutable deterministic board and state representations."""

from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True, slots=True, order=True)
class Coordinate:
    row: int
    col: int


@dataclass(frozen=True, slots=True)
class Board:
    grid_size: int
    axis_start_index: int
    axis_origin_corner: str

    @property
    def maximum_index(self) -> int:
        return self.axis_start_index + self.grid_size - 1

    def contains(self, coordinate: Coordinate) -> bool:
        return all(
            self.axis_start_index <= value <= self.maximum_index
            for value in (coordinate.row, coordinate.col)
        )


class Role(StrEnum):
    THIEF = "thief"
    COP = "cop"


@dataclass(frozen=True, slots=True)
class AgentPositions:
    thief: Coordinate
    cop: Coordinate

    def for_role(self, role: Role) -> Coordinate:
        return self.thief if role is Role.THIEF else self.cop


class EpisodeStatus(StrEnum):
    ACTIVE = "active"
    TERMINAL = "terminal"


class OutcomeKind(StrEnum):
    CAPTURE = "capture"
    SURVIVAL = "survival"
    TECHNICAL_LOSS = "technical_loss"


class CaptureCause(StrEnum):
    COORDINATE_OVERLAP = "coordinate_overlap"
    BARRIER_ON_THIEF = "barrier_on_thief"
    TRAPPED_THIEF = "trapped_thief"


@dataclass(frozen=True, slots=True)
class Outcome:
    kind: OutcomeKind
    capture_cause: CaptureCause | None = None


@dataclass(frozen=True, slots=True)
class GameState:
    board: Board
    positions: AgentPositions
    barriers: frozenset[Coordinate]
    barrier_usage: int
    barrier_quota: int
    valid_steps: int
    status: EpisodeStatus
    outcome: Outcome | None
