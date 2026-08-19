"""Barrier-on-thief capture and common claim tests."""

import pytest

from salareen_thief.base_logic.action_results import (
    ActionAccepted,
    ActionError,
    ActionRejected,
)
from salareen_thief.base_logic.actions import BarrierAction, CaptureClaim
from salareen_thief.base_logic.scoring import ScoreAccepted, ScorePair, score_episode
from salareen_thief.base_logic.state_factory import build_state
from salareen_thief.base_logic.state_results import StateAccepted
from salareen_thief.base_logic.state_types import (
    CaptureCause,
    Coordinate,
    EpisodeStatus,
    Outcome,
    OutcomeKind,
    Role,
)


def capture_state(config):
    result = build_state(config, thief=Coordinate(0, 1), cop=Coordinate(0, 0))
    assert isinstance(result, StateAccepted)
    return result.value


def claim(role=Role.COP, cause=CaptureCause.BARRIER_ON_THIEF):
    return CaptureClaim(role, cause)


def test_barrier_on_thief_with_valid_claim_captures(accepted_config, rules) -> None:
    state = capture_state(accepted_config)
    action = BarrierAction(Role.COP, state.positions.thief, claim())
    result = rules.apply(state, action)
    assert isinstance(result, ActionAccepted)
    assert result.state.status is EpisodeStatus.TERMINAL
    assert result.state.outcome == Outcome(
        OutcomeKind.CAPTURE, CaptureCause.BARRIER_ON_THIEF
    )
    assert result.state.barriers == frozenset({Coordinate(0, 1)})
    assert result.state.barrier_usage == 1
    assert result.state.valid_steps == 1
    assert score_episode(result.state, accepted_config.scoring) == ScoreAccepted(
        ScorePair(20, 5)
    )


@pytest.mark.parametrize(
    "capture_claim,error",
    (
        (None, ActionError.CAPTURE_CLAIM_REQUIRED),
        ("claim", ActionError.INVALID_CAPTURE_CLAIM),
        (claim(Role.THIEF), ActionError.INVALID_CAPTURE_CLAIM),
        (
            claim(Role.COP, CaptureCause.TRAPPED_THIEF),
            ActionError.INVALID_CAPTURE_CLAIM,
        ),
        (
            CaptureClaim(True, CaptureCause.BARRIER_ON_THIEF),
            ActionError.INVALID_CAPTURE_CLAIM,
        ),
    ),
)
def test_invalid_claims_preserve_identity(
    accepted_config, rules, capture_claim, error
) -> None:
    state = capture_state(accepted_config)
    result = rules.apply(
        state, BarrierAction(Role.COP, state.positions.thief, capture_claim)
    )
    assert result == ActionRejected(state, error)
    assert result.state is state


def test_false_barrier_claim_is_rejected(rules, initial_game) -> None:
    action = BarrierAction(Role.COP, Coordinate(0, 1), claim())
    result = rules.apply(initial_game, action)
    assert result == ActionRejected(initial_game, ActionError.INVALID_CAPTURE_CLAIM)


def test_barrier_capture_replay_is_repeatable(accepted_config, rules) -> None:
    state = capture_state(accepted_config)
    action = BarrierAction(Role.COP, state.positions.thief, claim())
    assert rules.apply(state, action) == rules.apply(state, action)
