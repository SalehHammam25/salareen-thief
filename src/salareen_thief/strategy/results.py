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


class PluginError(StrEnum):
    CONFIG_READ_ERROR = "config_read_error"
    TOML_ERROR = "toml_error"
    MALFORMED_REFERENCE = "malformed_reference"
    MODULE_NOT_FOUND = "module_not_found"
    IMPORT_FAILED = "import_failed"
    CLASS_NOT_FOUND = "class_not_found"
    CONSTRUCTOR_FAILED = "constructor_failed"
    INVALID_INTERFACE = "invalid_interface"
    RUNTIME_EXCEPTION = "runtime_exception"
    INVALID_RESULT = "invalid_result"
    PROPOSAL_REJECTED = "proposal_rejected"


@dataclass(frozen=True, slots=True)
class FallbackReason:
    error: PluginError
    detail: str = ""


@dataclass(frozen=True, slots=True)
class ProposedAction:
    action: MoveAction
    explored_cells: int
    fallback_reason: FallbackReason | None = None


@dataclass(frozen=True, slots=True)
class ValidatedDecision:
    action: MoveAction
    state: GameState
    fallback_reason: FallbackReason | None = None


@dataclass(frozen=True, slots=True)
class DecisionFailure:
    error: DecisionError
    detail: str = ""
    fallback_reason: FallbackReason | None = None


ProposalResult = ProposedAction | DecisionFailure
DecisionResult = ValidatedDecision | DecisionFailure
