"""Capture-aware barrier and claim transitions."""

from .action_results import ActionAccepted, ActionError, ActionRejected, ActionResult
from .actions import BarrierAction
from .barriers import validate_barrier
from .capture import is_trapped, validate_claim
from .config_types import BaseLogicConfig
from .state_types import (
    CaptureCause,
    EpisodeStatus,
    GameState,
    Outcome,
    OutcomeKind,
)
from .transitions import finish_step, rebuild


def capture_outcome(cause: CaptureCause) -> Outcome:
    return Outcome(OutcomeKind.CAPTURE, cause)


def claimed_capture(
    config: BaseLogicConfig,
    state: GameState,
    claim: object,
    cause: CaptureCause,
) -> ActionResult:
    """Apply a terminal capture only after local claim validation."""
    issue = validate_claim(claim, cause)
    if issue is not None:
        return ActionRejected(state, issue)
    terminal = rebuild(
        config,
        state,
        status=EpisodeStatus.TERMINAL,
        outcome=capture_outcome(cause),
    )
    return ActionAccepted(terminal)


def apply_barrier(
    config: BaseLogicConfig,
    state: GameState,
    action: BarrierAction,
) -> ActionResult:
    """Apply placement with overlap and special-capture priority."""
    if state.positions.cop == state.positions.thief:
        return claimed_capture(
            config,
            state,
            action.capture_claim,
            CaptureCause.COORDINATE_OVERLAP,
        )
    issue = validate_barrier(state, action.role, action.target)
    if issue is not None:
        return ActionRejected(state, issue)
    barriers = state.barriers | {action.target}
    usage = state.barrier_usage + 1
    if action.target == state.positions.thief:
        cause = CaptureCause.BARRIER_ON_THIEF
    else:
        preview = rebuild(
            config, state, barriers=barriers, barrier_usage=usage
        )
        cause = CaptureCause.TRAPPED_THIEF if is_trapped(preview) else None
    if cause is not None:
        claim_issue = validate_claim(action.capture_claim, cause)
        if claim_issue is not None:
            return ActionRejected(state, claim_issue)
    elif action.capture_claim is not None:
        return ActionRejected(state, ActionError.INVALID_CAPTURE_CLAIM)
    return finish_step(
        config,
        state,
        barriers=barriers,
        barrier_usage=usage,
        capture=capture_outcome(cause) if cause is not None else None,
    )
