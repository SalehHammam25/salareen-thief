"""Sole gateway for validated peer transport events."""

from dataclasses import dataclass, replace
from typing import Any

from .contracts import ContractRejected, GeometryMessage, decode_geometry
from .phases import PeerPhase, PhaseState
from .results import TransportAccepted, TransportError, TransportRejected


@dataclass(frozen=True, slots=True)
class OrchestratorState:
    session_id: str
    phase: PhaseState = PhaseState()
    last_received: GeometryMessage | None = None
    processed: tuple[GeometryMessage, ...] = ()


class PeerOrchestrator:
    """Own transport state; never owns or mutates Base Logic state."""

    def __init__(self, session_id: str, max_tracked: int = 100) -> None:
        if type(session_id) is not str or not session_id:
            raise ValueError("session_id must be a nonempty string")
        if type(max_tracked) is not int or max_tracked <= 0:
            raise ValueError("max_tracked must be a positive integer")
        self._state = OrchestratorState(session_id=session_id)
        self._max_tracked = max_tracked

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
        previous = next(
            (
                item
                for item in before.processed
                if item.correlation_id == decoded.correlation_id
            ),
            None,
        )
        if previous is not None:
            if previous == decoded:
                return TransportAccepted(previous)
            return TransportRejected(
                TransportError.DUPLICATE_MISMATCH, decoded.correlation_id
            )
        processed = (before.processed + (decoded,))[-self._max_tracked :]
        self._state = replace(
            before,
            last_received=decoded,
            processed=processed,
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
