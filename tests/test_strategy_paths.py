"""Blind shortest-route positive and negative tests."""

import pytest

from salareen_thief.base_logic.state_factory import build_state
from salareen_thief.base_logic.state_results import StateAccepted
from salareen_thief.base_logic.state_types import Coordinate
from salareen_thief.strategy.blind import BlindShortestPath
from salareen_thief.strategy.gateway import StrategyGateway
from salareen_thief.strategy.models import snapshot_for
from salareen_thief.strategy.results import (
    DecisionError,
    DecisionFailure,
    ProposedAction,
    ValidatedDecision,
)


def first(choices):
    return choices[0]


def state_with(accepted_config, *, thief, cop=None, barriers=()):
    cop = Coordinate(0, 0) if cop is None else cop
    result = build_state(
        accepted_config, thief=thief, cop=cop, barriers=barriers,
        barrier_usage=len(tuple(barriers)),
    )
    assert isinstance(result, StateAccepted)
    return result.value


def test_direct_one_step_is_validated_by_base_logic(rules, initial_game) -> None:
    target = Coordinate(3, 4)
    result = StrategyGateway(rules, BlindShortestPath(first)).decide(
        initial_game, target
    )
    assert isinstance(result, ValidatedDecision)
    assert result.state.positions.thief == target
    assert initial_game.positions.thief == Coordinate(3, 3)


@pytest.mark.parametrize(
    ("target", "expected"),
    [
        (Coordinate(2, 3), Coordinate(2, 3)),
        (Coordinate(4, 3), Coordinate(4, 3)),
        (Coordinate(3, 2), Coordinate(3, 2)),
        (Coordinate(3, 4), Coordinate(3, 4)),
    ],
)
def test_table_driven_orthogonal_steps(
    rules, initial_game, target, expected
) -> None:
    result = StrategyGateway(rules, BlindShortestPath(first)).decide(
        initial_game, target
    )
    assert isinstance(result, ValidatedDecision)
    assert result.state.positions.thief == expected


def test_multi_turn_route_is_shortest(rules, initial_game) -> None:
    target = Coordinate(6, 6)
    state = initial_game
    steps = 0
    while state.positions.thief != target:
        result = StrategyGateway(rules, BlindShortestPath(first)).decide(state, target)
        assert isinstance(result, ValidatedDecision)
        state = result.state
        steps += 1
    assert steps == 6


def test_route_avoids_permanent_barriers(accepted_config, rules) -> None:
    start = Coordinate(3, 3)
    state = state_with(
        accepted_config,
        thief=start,
        barriers=(Coordinate(3, 4), Coordinate(2, 4)),
    )
    target = Coordinate(3, 5)
    result = StrategyGateway(rules, BlindShortestPath(first)).decide(state, target)
    assert isinstance(result, ValidatedDecision)
    assert result.state.positions.thief == Coordinate(4, 3)


def test_route_follows_board_edge_without_leaving_board(accepted_config, rules) -> None:
    state = state_with(accepted_config, thief=Coordinate(0, 6))
    target = Coordinate(6, 6)
    result = StrategyGateway(rules, BlindShortestPath(first)).decide(state, target)
    assert isinstance(result, ValidatedDecision)
    assert result.state.positions.thief == Coordinate(1, 6)


def test_unreachable_enclosed_target_is_explicit(accepted_config) -> None:
    target = Coordinate(1, 1)
    barriers = (
        Coordinate(0, 1), Coordinate(1, 0),
        Coordinate(1, 2), Coordinate(2, 1),
    )
    state = state_with(accepted_config, thief=Coordinate(3, 3), barriers=barriers)
    result = BlindShortestPath(first).propose(snapshot_for(state, target))
    assert result == DecisionFailure(DecisionError.UNREACHABLE_TARGET, str(target))


def test_off_board_target_is_explicit(initial_game) -> None:
    target = Coordinate(-1, 3)
    result = BlindShortestPath(first).propose(snapshot_for(initial_game, target))
    assert result == DecisionFailure(DecisionError.INVALID_TARGET)


def test_start_equals_target_proposes_valid_stay(rules, initial_game) -> None:
    result = StrategyGateway(rules, BlindShortestPath(first)).decide(
        initial_game, initial_game.positions.thief
    )
    assert isinstance(result, ValidatedDecision)
    assert result.state.positions.thief == initial_game.positions.thief
    assert result.state.valid_steps == initial_game.valid_steps + 1


def test_injected_tie_policy_controls_only_equal_shortest_choices(initial_game) -> None:
    seen = ()

    def last(choices):
        nonlocal seen
        seen = choices
        return choices[-1]

    result = BlindShortestPath(last).propose(
        snapshot_for(initial_game, Coordinate(4, 4))
    )
    assert isinstance(result, ProposedAction)
    assert len(seen) == 2
    assert result.action.choice == seen[-1]


def test_search_visits_at_most_one_entry_per_board_cell(initial_game) -> None:
    result = BlindShortestPath(first).propose(
        snapshot_for(initial_game, Coordinate(6, 6))
    )
    assert isinstance(result, ProposedAction)
    assert result.explored_cells <= initial_game.board.grid_size**2
