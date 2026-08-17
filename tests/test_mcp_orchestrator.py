"""Orchestrator and transport state-machine tests."""

from salareen_thief.mcp_transport.contracts import PROTOCOL_VERSION
from salareen_thief.mcp_transport.orchestrator import PeerOrchestrator
from salareen_thief.mcp_transport.phases import PeerPhase
from salareen_thief.mcp_transport.results import TransportAccepted, TransportError


def payload(correlation: str = "message-1") -> dict[str, object]:
    return {
        "protocol_version": PROTOCOL_VERSION,
        "correlation_id": correlation,
        "sender_role": "cop",
        "x": 1,
        "y": 2,
        "step": 0,
    }


def test_valid_receive_updates_only_transport_state() -> None:
    gateway = PeerOrchestrator()
    result = gateway.receive(payload())
    assert isinstance(result, TransportAccepted)
    assert gateway.state.last_received == result.message


def test_rejected_contract_does_not_mutate() -> None:
    gateway = PeerOrchestrator()
    before = gateway.state
    result = gateway.receive(payload() | {"x": True})
    assert result.as_dict()["accepted"] is False
    assert gateway.state is before


def test_outbound_payload_is_validated_by_gateway() -> None:
    gateway = PeerOrchestrator()
    accepted = gateway.prepare_outbound(payload())
    rejected = gateway.prepare_outbound(payload() | {"x": True})
    assert isinstance(accepted, TransportAccepted)
    assert rejected.as_dict()["accepted"] is False
    assert gateway.state == PeerOrchestrator().state


def test_only_listed_transitions_are_accepted() -> None:
    gateway = PeerOrchestrator()
    assert gateway.transition(PeerPhase.SENDING) is False
    assert gateway.state.phase.phase is PeerPhase.WAITING_FOR_OPPONENT
    assert gateway.transition(PeerPhase.COMPUTING_MOVE) is True
    assert gateway.transition(PeerPhase.SENDING) is True
    assert gateway.transition(PeerPhase.AWAITING_RESPONSE) is True
    assert gateway.transition(PeerPhase.WAITING_FOR_OPPONENT) is True


def test_out_of_phase_receive_preserves_state() -> None:
    gateway = PeerOrchestrator()
    gateway.transition(PeerPhase.COMPUTING_MOVE)
    before = gateway.state
    result = gateway.receive(payload())
    assert result.code is TransportError.OUT_OF_PHASE
    assert gateway.state is before


def test_terminal_phase_rejects_messages() -> None:
    gateway = PeerOrchestrator()
    gateway.transition(PeerPhase.COMPLETE)
    before = gateway.state
    result = gateway.receive(payload())
    assert result.code is TransportError.EPISODE_TERMINAL
    assert gateway.state is before
