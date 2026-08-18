"""Local deterministic capture evidence and claim validation."""

from .action_results import ActionError
from .actions import CaptureClaim
from .state_types import CaptureCause, Coordinate, GameState, Role

DIRECTIONS = ((-1, 0), (1, 0), (0, 1), (0, -1))


def adjacent_destinations(state: GameState) -> tuple[Coordinate, ...]:
    """Return in-board, non-barrier orthogonal thief destinations."""
    thief = state.positions.thief
    candidates = (
        Coordinate(thief.row + row, thief.col + col) for row, col in DIRECTIONS
    )
    return tuple(
        cell
        for cell in candidates
        if state.board.contains(cell) and cell not in state.barriers
    )


def is_trapped(state: GameState) -> bool:
    """Determine trapping without treating STAY as a destination."""
    return not adjacent_destinations(state)


def validate_claim(
    claim: object,
    expected: CaptureCause,
) -> ActionError | None:
    """Validate a local non-cryptographic cop Capture Claim."""
    if type(claim) is not CaptureClaim:
        return (
            ActionError.CAPTURE_CLAIM_REQUIRED
            if claim is None
            else (ActionError.INVALID_CAPTURE_CLAIM)
        )
    if type(claim.role) is not Role or claim.role is not Role.COP:
        return ActionError.INVALID_CAPTURE_CLAIM
    if type(claim.cause) is not CaptureCause or claim.cause is not expected:
        return ActionError.INVALID_CAPTURE_CLAIM
    return None
