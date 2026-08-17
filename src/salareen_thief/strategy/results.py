"""Typed strategy proposal and validation results."""

from dataclasses import dataclass
from enum import StrEnum

from salareen_thief.base_logic.actions import MoveAction
from salareen_thief.base_logic.state_types import GameState


class DecisionError(StrEnum):
    TERMINAL_STATE = "terminal_state"
    INVALID_TARGET = "invalid_target"
    UNREACHABLE_TARGET = "unreachable_target"
    INVALID_TIE_CHOICE = "invalid_tie_choice"
    INVALID_PROPOSAL = "invalid_proposal"
    ILLEGAL_PROPOSAL = "illegal_proposal"
    POLICY_EXCEPTION = "policy_exception"


@dataclass(frozen=True, slots=True)
class ProposedAction:
    action: MoveAction
    explored_cells: int


@dataclass(frozen=True, slots=True)
class ValidatedDecision:
    action: MoveAction
    state: GameState


@dataclass(frozen=True, slots=True)
class DecisionFailure:
    error: DecisionError
    detail: str = ""


ProposalResult = ProposedAction | DecisionFailure
DecisionResult = ValidatedDecision | DecisionFailure
