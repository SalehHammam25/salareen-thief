"""Capture, survival, technical-loss, and scoring tests."""

from dataclasses import replace

from salareen_thief.base_logic.action_results import (
    ActionAccepted,
    ActionError,
    ActionRejected,
)
from salareen_thief.base_logic.actions import CaptureClaim, MoveAction, MoveChoice
from salareen_thief.base_logic.scoring import (
    ScoreAccepted,
    ScorePair,
    ScoreRejected,
    score_episode,
)
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


def overlap_state(config):
    result = build_state(
        config,
        thief=Coordinate(2, 2),
        cop=Coordinate(2, 2),
    )
    assert isinstance(result, StateAccepted)
    return result.value


def test_overlap_capture_requires_valid_cop_claim(accepted_config, rules) -> None:
    state = overlap_state(accepted_config)
    invalid = rules.apply(
        state, CaptureClaim(Role.THIEF, CaptureCause.COORDINATE_OVERLAP)
    )
    assert invalid == ActionRejected(state, ActionError.INVALID_CAPTURE_CLAIM)
    result = rules.apply(
        state, CaptureClaim(Role.COP, CaptureCause.COORDINATE_OVERLAP)
    )
    assert isinstance(result, ActionAccepted)
    assert result.state.status is EpisodeStatus.TERMINAL
    assert result.state.outcome == Outcome(
        OutcomeKind.CAPTURE, CaptureCause.COORDINATE_OVERLAP
    )
    assert score_episode(result.state, accepted_config.scoring) == ScoreAccepted(
        ScorePair(20, 5)
    )


def test_overlap_requires_claim_before_ordinary_move(accepted_config, rules) -> None:
    state = overlap_state(accepted_config)
    result = rules.apply(state, MoveAction(Role.COP, MoveChoice.NORTH))
    assert result == ActionRejected(state, ActionError.CAPTURE_CLAIM_REQUIRED)
    assert result.state is state


def test_terminal_episode_rejects_later_action(accepted_config, rules) -> None:
    captured = rules.apply(
        overlap_state(accepted_config),
        CaptureClaim(Role.COP, CaptureCause.COORDINATE_OVERLAP),
    )
    assert isinstance(captured, ActionAccepted)
    action = MoveAction(Role.THIEF, MoveChoice.STAY)
    score_before = score_episode(captured.state, accepted_config.scoring)
    rejected = rules.apply(captured.state, action)
    assert rejected == ActionRejected(
        captured.state, ActionError.TERMINAL_EPISODE
    )
    assert score_episode(rejected.state, accepted_config.scoring) == score_before


def test_survival_at_default_threshold(rules, initial_game, accepted_config) -> None:
    state = initial_game
    for expected_step in range(1, 36):
        result = rules.apply(state, MoveAction(Role.THIEF, MoveChoice.STAY))
        assert isinstance(result, ActionAccepted)
        state = result.state
        assert state.valid_steps == expected_step
    assert state.outcome == Outcome(OutcomeKind.SURVIVAL)
    assert score_episode(state, accepted_config.scoring) == ScoreAccepted(
        ScorePair(5, 10)
    )


def test_external_technical_loss_and_score(rules, initial_game, accepted_config) -> None:
    result = rules.technical_loss(initial_game)
    assert isinstance(result, ActionAccepted)
    assert result.state.outcome == Outcome(OutcomeKind.TECHNICAL_LOSS)
    assert score_episode(result.state, accepted_config.scoring) == ScoreAccepted(
        ScorePair(0, 0)
    )


def test_active_and_malformed_outcomes_are_not_scored(
    initial_game, accepted_config
) -> None:
    assert isinstance(
        score_episode(initial_game, accepted_config.scoring), ScoreRejected
    )
    malformed = replace(
        initial_game,
        status=EpisodeStatus.TERMINAL,
        outcome=Outcome("unsupported"),
    )
    assert isinstance(
        score_episode(malformed, accepted_config.scoring), ScoreRejected
    )
    missing_cause = replace(
        initial_game,
        status=EpisodeStatus.TERMINAL,
        outcome=Outcome(OutcomeKind.CAPTURE),
    )
    assert isinstance(
        score_episode(missing_cause, accepted_config.scoring), ScoreRejected
    )


def test_all_capture_causes_are_representable() -> None:
    assert tuple(CaptureCause) == (
        CaptureCause.COORDINATE_OVERLAP,
        CaptureCause.BARRIER_ON_THIEF,
        CaptureCause.TRAPPED_THIEF,
    )
