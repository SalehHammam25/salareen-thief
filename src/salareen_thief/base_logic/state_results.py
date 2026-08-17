"""Accepted and rejected deterministic state construction."""

from dataclasses import dataclass
from enum import StrEnum

from .state_types import GameState


class StateErrorCategory(StrEnum):
    INCORRECT_TYPE = "incorrect_type"
    POSITION_OUT_OF_BOUNDS = "position_out_of_bounds"
    DUPLICATE_BARRIER = "duplicate_barrier"
    BARRIER_OUT_OF_BOUNDS = "barrier_out_of_bounds"
    INVALID_BARRIER_OCCUPANCY = "invalid_barrier_occupancy"
    NEGATIVE_BARRIER_USAGE = "negative_barrier_usage"
    BARRIER_QUOTA_EXCEEDED = "barrier_quota_exceeded"
    NEGATIVE_VALID_STEPS = "negative_valid_steps"
    STATUS_OUTCOME_MISMATCH = "status_outcome_mismatch"


@dataclass(frozen=True, slots=True)
class StateIssue:
    category: StateErrorCategory
    field: str
    message: str


@dataclass(frozen=True, slots=True)
class StateAccepted:
    value: GameState


@dataclass(frozen=True, slots=True)
class StateRejected:
    issues: tuple[StateIssue, ...]


StateResult = StateAccepted | StateRejected
