"""Trapped-thief evidence and common claim tests."""

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
from salareen_thief.base_logic.capture import adjacent_destinations, is_trapped
from salareen_thief.base_logic.scoring import ScoreAccepted, ScorePair, score_episode
from salareen_thief.base_logic.state_factory import build_state
from salareen_thief.base_logic.state_results import StateAccepted
from salareen_thief.base_logic.state_types import (
    CaptureCause,
    Coordinate,
    Outcome,
    OutcomeKind,
    Role,
)


def state_at(config, *, thief, cop, barriers=()):
    result = build_state(config, thief=thief, cop=cop, barriers=barriers)
    assert isinstance(result, StateAccepted)
    return result.value


def trapped_corner(config):
    return state_at(
        config,
        thief=Coordinate(0, 0),
        cop=Coordinate(6, 6),
        barriers=(Coordinate(0, 1), Coordinate(1, 0)),
    )


def trapped_claim():
    return CaptureClaim(Role.COP, CaptureCause.TRAPPED_THIEF)


def test_stay_does_not_prevent_claimed_trapped_capture(
    accepted_config, rules
) -> None:
    state = trapped_corner(accepted_config)
    assert is_trapped(state)
    stay = rules.apply(state, MoveAction(Role.THIEF, MoveChoice.STAY))
    assert stay == ActionRejected(state, ActionError.CAPTURE_CLAIM_REQUIRED)
    result = rules.apply(state, trapped_claim())
    assert isinstance(result, ActionAccepted)
    assert result.state.outcome == Outcome(
        OutcomeKind.CAPTURE, CaptureCause.TRAPPED_THIEF
    )
    assert score_episode(result.state, accepted_config.scoring) == ScoreAccepted(
        ScorePair(20, 5)
    )


def test_one_available_destination_prevents_trapping(accepted_config) -> None:
    state = state_at(
        accepted_config,
        thief=Coordinate(0, 0),
        cop=Coordinate(6, 6),
        barriers=(Coordinate(0, 1),),
    )
    assert adjacent_destinations(state) == (Coordinate(1, 0),)
    assert not is_trapped(state)


def test_cop_adjacent_cell_is_available(accepted_config) -> None:
    state = state_at(
        accepted_config,
        thief=Coordinate(0, 0),
        cop=Coordinate(1, 0),
        barriers=(Coordinate(0, 1),),
    )
    assert adjacent_destinations(state) == (Coordinate(1, 0),)
    assert not is_trapped(state)


def test_false_trapped_claim_is_rejected(rules, initial_game) -> None:
    result = rules.apply(initial_game, trapped_claim())
    assert result == ActionRejected(
        initial_game, ActionError.INVALID_CAPTURE_CLAIM
    )


def test_barrier_completing_trap_requires_matching_claim(
    accepted_config, rules
) -> None:
    state = state_at(
        accepted_config,
        thief=Coordinate(0, 0),
        cop=Coordinate(1, 1),
        barriers=(Coordinate(0, 1),),
    )
    action = BarrierAction(Role.COP, Coordinate(1, 0))
    missing = rules.apply(state, action)
    assert missing == ActionRejected(state, ActionError.CAPTURE_CLAIM_REQUIRED)
    assert missing.state is state
    claimed = BarrierAction(
        Role.COP,
        Coordinate(1, 0),
        CaptureClaim(Role.COP, CaptureCause.TRAPPED_THIEF),
    )
    result = rules.apply(state, claimed)
    assert isinstance(result, ActionAccepted)
    assert result.state.outcome == Outcome(
        OutcomeKind.CAPTURE, CaptureCause.TRAPPED_THIEF
    )
    assert result.state.barriers == frozenset(
        {Coordinate(0, 1), Coordinate(1, 0)}
    )


def test_trapped_terminal_state_is_immutable(accepted_config, rules) -> None:
    state = trapped_corner(accepted_config)
    captured = rules.apply(state, trapped_claim())
    assert isinstance(captured, ActionAccepted)
    later = rules.apply(captured.state, trapped_claim())
    assert later == ActionRejected(captured.state, ActionError.TERMINAL_EPISODE)
    assert later.state is captured.state


def test_trapped_capture_replay_is_repeatable(accepted_config, rules) -> None:
    state = trapped_corner(accepted_config)
    assert rules.apply(state, trapped_claim()) == rules.apply(
        state, trapped_claim()
    )
