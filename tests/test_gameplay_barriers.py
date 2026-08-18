"""General deterministic barrier behavior tests."""

from salareen_thief.base_logic.action_results import (
    ActionAccepted,
    ActionError,
    ActionRejected,
)
from salareen_thief.base_logic.actions import (
    BarrierAction,
    CombinedAction,
    MoveChoice,
)
from salareen_thief.base_logic.state_factory import build_state
from salareen_thief.base_logic.state_results import StateAccepted
from salareen_thief.base_logic.state_types import Coordinate, Role


def test_valid_barrier_replaces_movement(rules, initial_game) -> None:
    target = Coordinate(0, 1)
    result = rules.apply(initial_game, BarrierAction(Role.COP, target))
    assert isinstance(result, ActionAccepted)
    assert result.state.positions == initial_game.positions
    assert result.state.barriers == frozenset({target})
    assert result.state.barrier_usage == 1
    assert result.state.valid_steps == 1


def test_barrier_is_permanent_across_transition(rules, initial_game) -> None:
    first = rules.apply(initial_game, BarrierAction(Role.COP, Coordinate(0, 1)))
    assert isinstance(first, ActionAccepted)
    second = rules.apply(first.state, BarrierAction(Role.COP, Coordinate(1, 0)))
    assert isinstance(second, ActionAccepted)
    assert second.state.barriers == frozenset({Coordinate(0, 1), Coordinate(1, 0)})


def test_thief_cannot_place_barrier(rules, initial_game) -> None:
    action = BarrierAction(Role.THIEF, Coordinate(3, 4))
    assert rules.apply(initial_game, action) == ActionRejected(
        initial_game, ActionError.BARRIER_COP_ONLY
    )


def test_boolean_barrier_coordinate_is_rejected(rules, initial_game) -> None:
    action = BarrierAction(Role.COP, Coordinate(0, True))
    assert rules.apply(initial_game, action) == ActionRejected(
        initial_game, ActionError.INVALID_ACTION_TYPE
    )


def test_combined_action_is_rejected(rules, initial_game) -> None:
    action = CombinedAction(Role.COP, MoveChoice.SOUTH, Coordinate(0, 1))
    result = rules.apply(initial_game, action)
    assert result == ActionRejected(initial_game, ActionError.COMBINED_ACTION)
    assert result.state is initial_game


def test_nonadjacent_barriers_are_rejected(rules, initial_game) -> None:
    for target in (Coordinate(1, 1), Coordinate(0, 2)):
        result = rules.apply(initial_game, BarrierAction(Role.COP, target))
        assert result == ActionRejected(initial_game, ActionError.BARRIER_NOT_ADJACENT)


def test_exhausted_quota_rejects_without_mutation(accepted_config, rules) -> None:
    built = build_state(
        accepted_config,
        thief=Coordinate(3, 3),
        cop=Coordinate(0, 0),
        barrier_usage=14,
    )
    assert isinstance(built, StateAccepted)
    action = BarrierAction(Role.COP, Coordinate(0, 1))
    assert rules.apply(built.value, action) == ActionRejected(
        built.value, ActionError.BARRIER_QUOTA_EXHAUSTED
    )
