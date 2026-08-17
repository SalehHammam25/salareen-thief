"""Chapter 3.4 cop-own-cell barrier semantics."""

from salareen_thief.base_logic.action_results import (
    ActionAccepted,
    ActionError,
    ActionRejected,
)
from salareen_thief.base_logic.actions import (
    BarrierAction,
    CaptureClaim,
    MoveAction,
    MoveChoice,
)
from salareen_thief.base_logic.state_factory import build_state
from salareen_thief.base_logic.state_results import StateAccepted
from salareen_thief.base_logic.state_types import (
    CaptureCause,
    Coordinate,
    Outcome,
    OutcomeKind,
    Role,
)


def place_own(rules, state):
    return rules.apply(state, BarrierAction(Role.COP, state.positions.cop))


def test_own_cell_placement_grandfathers_occupancy(rules, initial_game) -> None:
    result = place_own(rules, initial_game)
    assert isinstance(result, ActionAccepted)
    assert result.state.positions == initial_game.positions
    assert result.state.barriers == frozenset({Coordinate(0, 0)})
    assert result.state.barrier_usage == 1
    assert result.state.valid_steps == 1


def test_cop_can_stay_on_own_barrier(rules, initial_game) -> None:
    placed = place_own(rules, initial_game)
    assert isinstance(placed, ActionAccepted)
    stayed = rules.apply(placed.state, MoveAction(Role.COP, MoveChoice.STAY))
    assert isinstance(stayed, ActionAccepted)
    assert stayed.state.positions.cop == Coordinate(0, 0)
    assert stayed.state.barriers == placed.state.barriers


def test_cop_can_leave_but_cannot_reenter(rules, initial_game) -> None:
    placed = place_own(rules, initial_game)
    assert isinstance(placed, ActionAccepted)
    left = rules.apply(placed.state, MoveAction(Role.COP, MoveChoice.SOUTH))
    assert isinstance(left, ActionAccepted)
    assert left.state.positions.cop == Coordinate(1, 0)
    assert left.state.barriers == frozenset({Coordinate(0, 0)})
    returned = rules.apply(left.state, MoveAction(Role.COP, MoveChoice.NORTH))
    assert returned == ActionRejected(left.state, ActionError.BARRIER_COLLISION)
    assert returned.state is left.state


def test_thief_cannot_enter_own_cell_barrier(accepted_config, rules) -> None:
    built = build_state(
        accepted_config,
        thief=Coordinate(0, 1),
        cop=Coordinate(0, 0),
    )
    assert isinstance(built, StateAccepted)
    placed = place_own(rules, built.value)
    assert isinstance(placed, ActionAccepted)
    result = rules.apply(
        placed.state, MoveAction(Role.THIEF, MoveChoice.WEST)
    )
    assert result == ActionRejected(placed.state, ActionError.BARRIER_COLLISION)


def test_duplicate_own_cell_placement_is_unchanged(rules, initial_game) -> None:
    placed = place_own(rules, initial_game)
    assert isinstance(placed, ActionAccepted)
    duplicate = place_own(rules, placed.state)
    assert duplicate == ActionRejected(placed.state, ActionError.DUPLICATE_BARRIER)
    assert duplicate.state is placed.state


def test_overlap_claim_has_priority_over_own_placement(
    accepted_config, rules
) -> None:
    built = build_state(
        accepted_config,
        thief=Coordinate(2, 2),
        cop=Coordinate(2, 2),
    )
    assert isinstance(built, StateAccepted)
    action = BarrierAction(
        Role.COP,
        Coordinate(2, 2),
        CaptureClaim(Role.COP, CaptureCause.COORDINATE_OVERLAP),
    )
    result = rules.apply(built.value, action)
    assert isinstance(result, ActionAccepted)
    assert result.state.outcome == Outcome(
        OutcomeKind.CAPTURE, CaptureCause.COORDINATE_OVERLAP
    )
    assert result.state.barriers == frozenset()
    assert result.state.barrier_usage == 0


def test_overlap_cannot_be_bypassed_without_claim(accepted_config, rules) -> None:
    built = build_state(
        accepted_config,
        thief=Coordinate(2, 2),
        cop=Coordinate(2, 2),
    )
    assert isinstance(built, StateAccepted)
    result = rules.apply(
        built.value, BarrierAction(Role.COP, Coordinate(2, 2))
    )
    assert result == ActionRejected(
        built.value, ActionError.CAPTURE_CLAIM_REQUIRED
    )
    assert result.state is built.value


def test_terminal_capture_rejects_own_cell_action(accepted_config, rules) -> None:
    built = build_state(
        accepted_config,
        thief=Coordinate(2, 2),
        cop=Coordinate(2, 2),
    )
    assert isinstance(built, StateAccepted)
    claim = CaptureClaim(Role.COP, CaptureCause.COORDINATE_OVERLAP)
    captured = rules.apply(built.value, claim)
    assert isinstance(captured, ActionAccepted)
    later = rules.apply(
        captured.state,
        BarrierAction(Role.COP, captured.state.positions.cop),
    )
    assert later == ActionRejected(captured.state, ActionError.TERMINAL_EPISODE)
    assert later.state is captured.state


def test_own_cell_replay_is_repeatable(rules, initial_game) -> None:
    assert place_own(rules, initial_game) == place_own(rules, initial_game)
