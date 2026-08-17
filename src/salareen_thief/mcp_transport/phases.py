"""Immutable transport phase state machine."""

from dataclasses import dataclass, replace
from enum import StrEnum


class PeerPhase(StrEnum):
    WAITING_FOR_OPPONENT = "WAITING_FOR_OPPONENT"
    COMPUTING_MOVE = "COMPUTING_MOVE"
    SENDING = "SENDING"
    AWAITING_RESPONSE = "AWAITING_RESPONSE"
    TECHNICAL_LOSS = "TECHNICAL_LOSS"
    COMPLETE = "COMPLETE"


_TRANSITIONS = {
    PeerPhase.WAITING_FOR_OPPONENT: {PeerPhase.COMPUTING_MOVE, PeerPhase.COMPLETE},
    PeerPhase.COMPUTING_MOVE: {PeerPhase.SENDING, PeerPhase.TECHNICAL_LOSS},
    PeerPhase.SENDING: {PeerPhase.AWAITING_RESPONSE, PeerPhase.TECHNICAL_LOSS},
    PeerPhase.AWAITING_RESPONSE: {PeerPhase.WAITING_FOR_OPPONENT, PeerPhase.TECHNICAL_LOSS},
    PeerPhase.TECHNICAL_LOSS: set(),
    PeerPhase.COMPLETE: set(),
}


@dataclass(frozen=True, slots=True)
class PhaseState:
    phase: PeerPhase = PeerPhase.WAITING_FOR_OPPONENT

    def transition(self, target: PeerPhase) -> "PhaseState | None":
        if target not in _TRANSITIONS[self.phase]:
            return None
        return replace(self, phase=target)
