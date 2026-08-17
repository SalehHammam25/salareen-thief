"""Pure unblocked barrier placement rules."""

from .action_results import ActionError
from .state_types import Coordinate, GameState, Role


def validate_barrier(
    state: GameState, role: Role, target: Coordinate
) -> ActionError | None:
    """Validate Chapter 3.4 current-or-adjacent placement."""
    if type(role) is not Role:
        return ActionError.INVALID_ROLE
    if (
        type(target) is not Coordinate
        or type(target.row) is not int
        or type(target.col) is not int
    ):
        return ActionError.INVALID_ACTION_TYPE
    if role is not Role.COP:
        return ActionError.BARRIER_COP_ONLY
    if not state.board.contains(target):
        return ActionError.BARRIER_NOT_ADJACENT
    if target in state.barriers:
        return ActionError.DUPLICATE_BARRIER
    if state.barrier_usage >= state.barrier_quota:
        return ActionError.BARRIER_QUOTA_EXHAUSTED
    cop = state.positions.cop
    distance = abs(target.row - cop.row) + abs(target.col - cop.col)
    if distance not in (0, 1):
        return ActionError.BARRIER_NOT_ADJACENT
    return None
