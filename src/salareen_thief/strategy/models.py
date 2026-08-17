"""Immutable, blind strategy input values."""

from dataclasses import dataclass

from salareen_thief.base_logic.state_types import (
    Board,
    Coordinate,
    EpisodeStatus,
    GameState,
)


@dataclass(frozen=True, slots=True)
class StrategySnapshot:
    board: Board
    thief: Coordinate
    barriers: frozenset[Coordinate]
    status: EpisodeStatus
    target: Coordinate


def snapshot_for(state: GameState, target: Coordinate) -> StrategySnapshot:
    """Expose only geometry needed by blind thief navigation."""
    return StrategySnapshot(
        state.board,
        state.positions.thief,
        state.barriers,
        state.status,
        target,
    )
