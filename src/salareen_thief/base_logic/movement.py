"""Pure movement target and legality rules."""

from .action_results import ActionError, BlockedQuestion
from .actions import MoveChoice
from .state_types import Board, Coordinate

DELTAS = {
    MoveChoice.NORTH: (-1, 0),
    MoveChoice.SOUTH: (1, 0),
    MoveChoice.EAST: (0, 1),
    MoveChoice.WEST: (0, -1),
    MoveChoice.STAY: (0, 0),
}


def target_for(origin: Coordinate, choice: MoveChoice) -> Coordinate:
    """Calculate one fixed movement choice in row-column space."""
    row_delta, col_delta = DELTAS[choice]
    return Coordinate(origin.row + row_delta, origin.col + col_delta)


def validate_target(
    board: Board,
    origin: Coordinate,
    target: Coordinate,
    barriers: frozenset[Coordinate],
) -> ActionError | BlockedQuestion | None:
    """Validate an explicit movement target."""
    if not board.contains(target):
        return ActionError.OUT_OF_BOUNDS
    displacement = (abs(target.row - origin.row), abs(target.col - origin.col))
    if displacement not in ((0, 0), (1, 0), (0, 1)):
        return ActionError.INVALID_DISPLACEMENT
    if target in barriers and target != origin:
        return ActionError.BARRIER_COLLISION
    return None
