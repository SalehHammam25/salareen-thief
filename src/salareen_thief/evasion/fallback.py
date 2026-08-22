"""The previous corner-seeking thief policy, retained only as a fallback."""

from salareen_thief.base_logic.actions import MoveAction
from salareen_thief.base_logic.state_types import Board, Coordinate, EpisodeStatus
from salareen_thief.strategy.blind import BlindShortestPath
from salareen_thief.strategy.models import StrategySnapshot
from salareen_thief.strategy.results import ProposedAction

CORNERS = (Coordinate(0, 0), Coordinate(0, 6), Coordinate(6, 0), Coordinate(6, 6))


def corner_target(
    barriers: frozenset[Coordinate], threat: Coordinate, position: Coordinate
) -> Coordinate:
    """Return the legal corner furthest from the last known threat."""
    legal = [corner for corner in CORNERS if corner not in barriers]
    return max(
        legal or [position],
        key=lambda cell: (
            abs(cell.row - threat.row) + abs(cell.col - threat.col),
            cell.row,
            cell.col,
        ),
    )


def corner_choice(
    board: Board,
    position: Coordinate,
    barriers: frozenset[Coordinate],
    threat: Coordinate,
) -> str:
    """Return the legacy blind shortest-path move toward a distant corner."""
    snapshot = StrategySnapshot(
        board,
        position,
        barriers,
        EpisodeStatus.ACTIVE,
        corner_target(barriers, threat, position),
    )
    proposal = BlindShortestPath().propose(snapshot)
    if not isinstance(proposal, ProposedAction):
        return "STAY"
    if not isinstance(proposal.action, MoveAction):
        return "STAY"
    return proposal.action.choice.value
