"""ngrok process-exit, readiness, resume, and attribution tests."""

import asyncio

import pytest

from salareen_thief.cloud_tunneling.attribution import (
    FailureAttribution,
    attribute_failure,
)
from salareen_thief.cloud_tunneling.models import FailureKind, TunnelFailure
from salareen_thief.cloud_tunneling.ngrok_adapter import NgrokProvider
from salareen_thief.cloud_tunneling.ngrok_config import NgrokConfig
from salareen_thief.cloud_tunneling.reconnection import (
    ResumeDecision,
    ResumeIdentity,
    decide_resume,
)


class DeadProcess:
    def running(self) -> bool:
        return False


def provider(command_ok: bool = True, command=None) -> NgrokProvider:
    async def probe(_: str) -> bool:
        return True

    async def urls(_: str) -> tuple[str, ...]:
        return ()

    async def sleep(_: float) -> None:
        return None

    return NgrokProvider(
        NgrokConfig(8802, "stable.example.test", readiness_attempts=1),
        process_factory=lambda *_: DeadProcess(),
        probe=probe,
        urls=urls,
        command_check=command or (lambda *_: command_ok),
        sleep=sleep,
    )


def test_agent_not_ready_and_process_exit_are_typed() -> None:
    async def scenario() -> None:
        not_ready = await provider(False).start("http://127.0.0.1:8802/mcp")
        assert not_ready == TunnelFailure(FailureKind.START_FAILED, "ngrok_not_ready")
        exited = await provider().start("http://127.0.0.1:8802/mcp")
        assert exited == TunnelFailure(FailureKind.PROCESS_EXITED, "ngrok")

    asyncio.run(scenario())


def test_missing_ngrok_command_is_a_typed_readiness_failure() -> None:
    def missing(*_):
        raise FileNotFoundError("private path")

    adapter = provider(command=missing)
    result = asyncio.run(adapter.start("http://127.0.0.1:8802/mcp"))
    assert result == TunnelFailure(FailureKind.START_FAILED, "ngrok_not_ready")
    assert "private" not in repr(result)


def test_process_start_error_is_redacted_and_typed() -> None:
    async def probe(_: str) -> bool:
        return True

    def failed_factory(*_):
        raise OSError("private machine detail")

    async def scenario() -> None:
        adapter = NgrokProvider(
            NgrokConfig(8802, "stable.example.test"),
            process_factory=failed_factory,
            probe=probe,
            command_check=lambda *_: True,
        )
        result = await adapter.start("http://127.0.0.1:8802/mcp")
        assert result == TunnelFailure(FailureKind.START_FAILED, "ngrok")
        assert "private" not in repr(result)

    asyncio.run(scenario())


def identity(**changes) -> ResumeIdentity:
    values = {
        "game_id": "game-1",
        "session_id": "session-1",
        "protocol_version": "1.0-provisional",
        "turn_index": 4,
        "phase": "WAITING_FOR_OPPONENT",
    }
    values.update(changes)
    return ResumeIdentity(**values)


def test_resume_requires_every_identity_field_to_match() -> None:
    before = identity()
    assert decide_resume(before, None) is ResumeDecision.PAUSE
    assert decide_resume(before, identity()) is ResumeDecision.RESUME
    for field, value in (
        ("game_id", "other"),
        ("session_id", "other"),
        ("protocol_version", "other"),
        ("turn_index", 5),
        ("phase", "VERIFYING"),
    ):
        assert decide_resume(before, identity(**{field: value})) is ResumeDecision.ABORT


@pytest.mark.parametrize(
    "values,expected",
    [
        ((False, True, False, False), FailureAttribution.LOCAL_TECHNICAL_LOSS),
        ((True, False, False, False), FailureAttribution.LOCAL_TECHNICAL_LOSS),
        ((True, True, True, False), FailureAttribution.REMOTE_TECHNICAL_LOSS),
        ((False, False, False, True), FailureAttribution.UNKNOWN),
        ((True, True, False, False), FailureAttribution.UNKNOWN),
    ],
)
def test_failure_attribution_policy(values, expected) -> None:
    result = attribute_failure(
        local_server_healthy=values[0],
        local_tunnel_healthy=values[1],
        remote_application_failure_verified=values[2],
        network_or_provider_ambiguous=values[3],
    )
    assert result is expected
