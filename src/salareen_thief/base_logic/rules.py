"""Deterministic orchestration of Stage 1 rules."""

from dataclasses import dataclass

from .action_results import (
    ActionAccepted,
    ActionBlocked,
    ActionError,
    ActionRejected,
    ActionResult,
    BlockedQuestion,
)
from .actions import (
    Action,
    BarrierAction,
    CaptureClaim,
    CombinedAction,
    MoveAction,
    MoveChoice,
)
from .capture import is_trapped
from .capture_transitions import apply_barrier, claimed_capture
from .config_types import BaseLogicConfig
from .movement import target_for, validate_target
from .state_types import (
    AgentPositions,
    CaptureCause,
    Coordinate,
    EpisodeStatus,
    GameState,
    Outcome,
    OutcomeKind,
    Role,
)
from .transitions import finish_step, rebuild


@dataclass(frozen=True, slots=True)
class BaseLogicRules:
    config: BaseLogicConfig

    def apply(self, state: GameState, action: Action) -> ActionResult:
        if state.status is EpisodeStatus.TERMINAL:
            return ActionRejected(state, ActionError.TERMINAL_EPISODE)
        if isinstance(action, CaptureClaim):
            return self._claim(state, action)
        overlap = state.positions.cop == state.positions.thief
        if overlap and isinstance(action, BarrierAction):
            return apply_barrier(self.config, state, action)
        if overlap:
            return ActionRejected(state, ActionError.CAPTURE_CLAIM_REQUIRED)
        if is_trapped(state):
            return ActionRejected(state, ActionError.CAPTURE_CLAIM_REQUIRED)
        if isinstance(action, CombinedAction):
            return ActionRejected(state, ActionError.COMBINED_ACTION)
        if isinstance(action, MoveAction):
            return self._move(state, action)
        if isinstance(action, BarrierAction):
            return self._barrier(state, action)
        return ActionRejected(state, ActionError.INVALID_ACTION_TYPE)

    def _move(self, state: GameState, action: MoveAction) -> ActionResult:
        if type(action.role) is not Role:
            return ActionRejected(state, ActionError.INVALID_ROLE)
        if type(action.choice) is not MoveChoice:
            return ActionRejected(state, ActionError.INVALID_ACTION_TYPE)
        if state.board.axis_origin_corner != "top-left":
            return ActionBlocked(state, BlockedQuestion.UNDEFINED_COORDINATE_ORIGIN)
        origin = state.positions.for_role(action.role)
        expected = target_for(origin, action.choice)
        target = action.target if action.target is not None else expected
        valid_target = (
            type(target) is Coordinate
            and type(target.row) is int
            and type(target.col) is int
        )
        if not valid_target:
            return ActionRejected(state, ActionError.INVALID_ACTION_TYPE)
        issue = validate_target(state.board, origin, target, state.barriers)
        if issue is not None:
            return ActionRejected(state, issue)
        if target != expected:
            return ActionRejected(state, ActionError.INVALID_DISPLACEMENT)
        positions = AgentPositions(
            target if action.role is Role.THIEF else state.positions.thief,
            target if action.role is Role.COP else state.positions.cop,
        )
        return finish_step(self.config, state, positions=positions)

    def _barrier(self, state: GameState, action: BarrierAction) -> ActionResult:
        return apply_barrier(self.config, state, action)

    def _claim(self, state: GameState, claim: CaptureClaim) -> ActionResult:
        if state.positions.cop == state.positions.thief:
            cause = CaptureCause.COORDINATE_OVERLAP
        elif is_trapped(state):
            cause = CaptureCause.TRAPPED_THIEF
        else:
            return ActionRejected(state, ActionError.INVALID_CAPTURE_CLAIM)
        return claimed_capture(self.config, state, claim, cause)

    def technical_loss(self, state: GameState) -> ActionResult:
        """Accept an externally detected technical loss; perform no detection."""
        if state.status is EpisodeStatus.TERMINAL:
            return ActionRejected(state, ActionError.TERMINAL_EPISODE)
        terminal = rebuild(
            self.config,
            state,
            status=EpisodeStatus.TERMINAL,
            outcome=Outcome(OutcomeKind.TECHNICAL_LOSS),
        )
        return ActionAccepted(terminal)
