"""Scent evolution ordering around Base Logic results."""

from decimal import Decimal

from salareen_thief.base_logic.action_results import ActionAccepted, ActionRejected
from salareen_thief.base_logic.actions import MoveAction, MoveChoice
from salareen_thief.base_logic.state_types import Coordinate, Role
from salareen_thief.scent.field import emit, empty_field
from salareen_thief.scent.turns import apply_scent_turn

D = Decimal


def test_move_then_decay_then_emit_order(rules, initial_game) -> None:
    old = emit(initial_game.board, Coordinate(3, 2))
    turn = apply_scent_turn(
        rules,
        initial_game,
        MoveAction(Role.THIEF, MoveChoice.EAST),
        old,
    )
    assert isinstance(turn.action_result, ActionAccepted)
    assert turn.action_result.state.positions.thief == Coordinate(3, 4)
    assert turn.scent.at(3, 4) == D("0.9")
    assert turn.scent.at(3, 2) == D("0.81")


def test_stay_emits_without_immediate_decay(rules, initial_game) -> None:
    turn = apply_scent_turn(
        rules,
        initial_game,
        MoveAction(Role.THIEF, MoveChoice.STAY),
        empty_field(initial_game.board),
    )
    assert turn.scent.at(3, 3) == D("0.9")


def test_rejected_action_preserves_exact_field_identity(rules, initial_game) -> None:
    field = emit(initial_game.board, Coordinate(1, 1))
    rejected = MoveAction(Role.THIEF, MoveChoice.NORTH, Coordinate(6, 6))
    turn = apply_scent_turn(rules, initial_game, rejected, field)
    assert isinstance(turn.action_result, ActionRejected)
    assert turn.action_result.state is initial_game
    assert turn.scent is field


def test_repeated_scent_turns_are_equal(rules, initial_game) -> None:
    field = empty_field(initial_game.board)
    action = MoveAction(Role.THIEF, MoveChoice.SOUTH)
    assert apply_scent_turn(rules, initial_game, action, field) == apply_scent_turn(
        rules, initial_game, action, field
    )
