"""Accepted, rejected, and specification-blocked action results."""

from dataclasses import dataclass
from enum import StrEnum

from .state_types import GameState


class ActionError(StrEnum):
    INVALID_ACTION_TYPE = "invalid_action_type"
    INVALID_ROLE = "invalid_role"
    TERMINAL_EPISODE = "terminal_episode"
    COMBINED_ACTION = "combined_action"
    BARRIER_COLLISION = "barrier_collision"
    OUT_OF_BOUNDS = "out_of_bounds"
    INVALID_DISPLACEMENT = "invalid_displacement"
    BARRIER_COP_ONLY = "barrier_cop_only"
    BARRIER_NOT_ADJACENT = "barrier_not_adjacent"
    DUPLICATE_BARRIER = "duplicate_barrier"
    BARRIER_QUOTA_EXHAUSTED = "barrier_quota_exhausted"
    INVALID_CAPTURE_CLAIM = "invalid_capture_claim"
    CAPTURE_CLAIM_REQUIRED = "capture_claim_required"


class BlockedQuestion(StrEnum):
    UNDEFINED_COORDINATE_ORIGIN = "ORIGIN"


@dataclass(frozen=True, slots=True)
class ActionAccepted:
    state: GameState


@dataclass(frozen=True, slots=True)
class ActionRejected:
    state: GameState
    error: ActionError


@dataclass(frozen=True, slots=True)
class ActionBlocked:
    state: GameState
    question: BlockedQuestion


ActionResult = ActionAccepted | ActionRejected | ActionBlocked
