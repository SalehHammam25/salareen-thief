"""Sole gateway for validated peer transport events."""

from dataclasses import dataclass, replace
from typing import Any

from .contracts import ContractRejected, GeometryMessage, decode_geometry
from .phases import PeerPhase, PhaseState
from .results import TransportAccepted, TransportError, TransportRejected


@dataclass(frozen=True, slots=True)
class OrchestratorState:
    phase: PhaseState = PhaseState()
    last_received: GeometryMessage | None = None


class PeerOrchestrator:
    """Own transport state; never owns or mutates Base Logic state."""

    def __init__(self) -> None:
        self._state = OrchestratorState()

    @property
    def state(self) -> OrchestratorState:
        return self._state

    def receive(self, payload: Any) -> TransportAccepted | TransportRejected:
        before = self._state
        if before.phase.phase in {PeerPhase.COMPLETE, PeerPhase.TECHNICAL_LOSS}:
            return TransportRejected(TransportError.EPISODE_TERMINAL, "terminal phase")
        if before.phase.phase is not PeerPhase.WAITING_FOR_OPPONENT:
            return TransportRejected(TransportError.OUT_OF_PHASE, before.phase.phase)
        decoded = decode_geometry(payload)
        if isinstance(decoded, ContractRejected):
            return TransportRejected(decoded.code, decoded.detail)
        self._state = replace(
            before,
            last_received=decoded,
        )
        return TransportAccepted(decoded)

    def prepare_outbound(self, payload: Any) -> TransportAccepted | TransportRejected:
        if self._state.phase.phase in {PeerPhase.COMPLETE, PeerPhase.TECHNICAL_LOSS}:
            return TransportRejected(TransportError.EPISODE_TERMINAL, "terminal phase")
        decoded = decode_geometry(payload)
        if isinstance(decoded, ContractRejected):
            return TransportRejected(decoded.code, decoded.detail)
        return TransportAccepted(decoded)

    def transition(self, target: PeerPhase) -> bool:
        updated = self._state.phase.transition(target)
        if updated is None:
            return False
        self._state = replace(self._state, phase=updated)
        return True
