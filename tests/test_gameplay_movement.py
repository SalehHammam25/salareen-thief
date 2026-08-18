"""Positive and negative deterministic movement tests."""

from dataclasses import replace

import pytest

from salareen_thief.base_logic.action_results import (
    ActionAccepted,
    ActionBlocked,
    ActionError,
    ActionRejected,
    BlockedQuestion,
)
from salareen_thief.base_logic.actions import MoveAction, MoveChoice
from salareen_thief.base_logic.rules import BaseLogicRules
from salareen_thief.base_logic.state_factory import build_state
from salareen_thief.base_logic.state_results import StateAccepted
from salareen_thief.base_logic.state_types import Coordinate, Role


@pytest.mark.parametrize(
    "choice,expected",
    (
        (MoveChoice.NORTH, Coordinate(2, 3)),
        (MoveChoice.SOUTH, Coordinate(4, 3)),
        (MoveChoice.EAST, Coordinate(3, 4)),
        (MoveChoice.WEST, Coordinate(3, 2)),
    ),
)
def test_four_orthogonal_moves(rules, initial_game, choice, expected) -> None:
    result = rules.apply(initial_game, MoveAction(Role.THIEF, choice))
    assert isinstance(result, ActionAccepted)
    assert result.state.positions.thief == expected
    assert result.state.valid_steps == 1


def test_stay_preserves_position_and_counts(rules, initial_game) -> None:
    result = rules.apply(initial_game, MoveAction(Role.THIEF, MoveChoice.STAY))
    assert isinstance(result, ActionAccepted)
    assert result.state.positions == initial_game.positions
    assert result.state.valid_steps == 1


@pytest.mark.parametrize("target", (Coordinate(4, 4), Coordinate(5, 3)))
def test_invalid_displacement_rejects_without_mutation(
    rules, initial_game, target
) -> None:
    action = MoveAction(Role.THIEF, MoveChoice.SOUTH, target)
    result = rules.apply(initial_game, action)
    assert result == ActionRejected(initial_game, ActionError.INVALID_DISPLACEMENT)
    assert result.state is initial_game


def test_barrier_collision_rejects_without_mutation(accepted_config, rules) -> None:
    state = build_state(
        accepted_config,
        thief=Coordinate(3, 3),
        cop=Coordinate(0, 0),
        barriers=(Coordinate(3, 2),),
    )
    assert isinstance(state, StateAccepted)
    result = rules.apply(state.value, MoveAction(Role.THIEF, MoveChoice.WEST))
    assert result == ActionRejected(state.value, ActionError.BARRIER_COLLISION)


@pytest.mark.parametrize(
    "position,choice",
    (
        (Coordinate(0, 3), MoveChoice.NORTH),
        (Coordinate(6, 3), MoveChoice.SOUTH),
        (Coordinate(3, 6), MoveChoice.EAST),
        (Coordinate(3, 0), MoveChoice.WEST),
    ),
)
def test_every_off_board_direction_rejects_with_identity(
    accepted_config, rules, position, choice
) -> None:
    built = build_state(
        accepted_config,
        thief=position,
        cop=Coordinate(1, 1),
    )
    assert isinstance(built, StateAccepted)
    result = rules.apply(built.value, MoveAction(Role.THIEF, choice))
    assert result == ActionRejected(built.value, ActionError.OUT_OF_BOUNDS)
    assert result.state is built.value


def test_unknown_movement_choice_is_rejected(rules, initial_game) -> None:
    action = MoveAction(Role.THIEF, "DIAGONAL")
    assert rules.apply(initial_game, action) == ActionRejected(
        initial_game, ActionError.INVALID_ACTION_TYPE
    )


@pytest.mark.parametrize("target", ("north", Coordinate(True, 3)))
def test_malformed_explicit_target_is_rejected(rules, initial_game, target) -> None:
    action = MoveAction(Role.THIEF, MoveChoice.NORTH, target)
    result = rules.apply(initial_game, action)
    assert result == ActionRejected(initial_game, ActionError.INVALID_ACTION_TYPE)
    assert result.state is initial_game


def test_alternative_origin_direction_is_not_invented(
    accepted_config, initial_game
) -> None:
    board = replace(initial_game.board, axis_origin_corner="agreed-other")
    state = replace(initial_game, board=board)
    rules = BaseLogicRules(accepted_config)
    result = rules.apply(state, MoveAction(Role.THIEF, MoveChoice.NORTH))
    assert result == ActionBlocked(state, BlockedQuestion.UNDEFINED_COORDINATE_ORIGIN)
