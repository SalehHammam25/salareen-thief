"""Identity-gated pause/reconnect without inventing a game outcome."""

from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True, slots=True)
class ResumeIdentity:
    game_id: str
    session_id: str
    protocol_version: str
    turn_index: int
    phase: str


class ResumeDecision(StrEnum):
    PAUSE = "pause"
    RESUME = "resume"
    ABORT = "abort"


def decide_resume(
    before: ResumeIdentity, after: ResumeIdentity | None
) -> ResumeDecision:
    if after is None:
        return ResumeDecision.PAUSE
    return ResumeDecision.RESUME if before == after else ResumeDecision.ABORT
