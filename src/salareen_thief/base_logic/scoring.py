"""Deterministic individual-episode scoring."""

from dataclasses import dataclass

from .config_types import ScoringConfig
from .state_types import CaptureCause, EpisodeStatus, GameState, OutcomeKind


@dataclass(frozen=True, slots=True)
class ScorePair:
    cop: int
    thief: int


@dataclass(frozen=True, slots=True)
class ScoreAccepted:
    score: ScorePair


@dataclass(frozen=True, slots=True)
class ScoreRejected:
    reason: str


ScoreResult = ScoreAccepted | ScoreRejected


def score_episode(state: GameState, config: ScoringConfig) -> ScoreResult:
    """Score one valid terminal episode from validated fixed values."""
    if state.status is not EpisodeStatus.TERMINAL or state.outcome is None:
        return ScoreRejected("episode is not terminal")
    kind = state.outcome.kind
    if type(kind) is not OutcomeKind:
        return ScoreRejected("unsupported outcome")
    if kind is OutcomeKind.CAPTURE:
        if type(state.outcome.capture_cause) is not CaptureCause:
            return ScoreRejected("malformed capture outcome")
        return ScoreAccepted(ScorePair(config.capture_cop, config.capture_thief))
    if state.outcome.capture_cause is not None:
        return ScoreRejected("capture cause on non-capture outcome")
    if kind is OutcomeKind.SURVIVAL:
        return ScoreAccepted(ScorePair(config.survival_cop, config.survival_thief))
    if kind is OutcomeKind.TECHNICAL_LOSS:
        return ScoreAccepted(ScorePair(config.technical_loss, config.technical_loss))
    return ScoreRejected("unsupported outcome")
