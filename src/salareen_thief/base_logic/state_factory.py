"""Validated construction of immutable deterministic state."""

from collections.abc import Iterable

from .config_types import BaseLogicConfig
from .state_results import StateAccepted, StateRejected, StateResult
from .state_types import (
    AgentPositions,
    Board,
    Coordinate,
    EpisodeStatus,
    GameState,
    Outcome,
)
from .state_validation import validate_state


def build_state(
    config: BaseLogicConfig,
    *,
    thief: Coordinate,
    cop: Coordinate,
    barriers: Iterable[Coordinate] = (),
    barrier_usage: int = 0,
    valid_steps: int = 0,
    status: EpisodeStatus = EpisodeStatus.ACTIVE,
    outcome: Outcome | None = None,
) -> StateResult:
    """Validate state representation invariants without applying actions."""
    board = Board(
        config.board.grid_size,
        config.board.axis_start_index,
        config.board.axis_origin_corner,
    )
    barrier_set, issues = validate_state(
        board,
        thief,
        cop,
        barriers,
        barrier_usage,
        config.movement.max_barriers,
        valid_steps,
        status,
        outcome,
    )
    if issues:
        return StateRejected(issues)
    return StateAccepted(
        GameState(
            board,
            AgentPositions(thief, cop),
            barrier_set,
            barrier_usage,
            config.movement.max_barriers,
            valid_steps,
            status,
            outcome,
        )
    )


def initial_state(config: BaseLogicConfig) -> StateResult:
    """Construct the configured empty active initial state."""
    thief = Coordinate(*config.board.thief_start)
    cop = Coordinate(*config.board.cop_start)
    return build_state(config, thief=thief, cop=cop)
