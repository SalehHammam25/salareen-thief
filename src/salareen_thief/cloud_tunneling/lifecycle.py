"""Provider-neutral start, readiness, health, and controlled shutdown."""

from dataclasses import dataclass

from .endpoints import validate_remote_endpoint
from .failures import classify_failure
from .models import FailureKind, TunnelFailure, TunnelReady, TunnelResult
from .provider import TunnelProvider


@dataclass(frozen=True, slots=True)
class LifecycleState:
    running: bool = False
    ready: TunnelReady | None = None


class TunnelController:
    def __init__(self, provider: TunnelProvider) -> None:
        self._provider = provider
        self._state = LifecycleState()

    @property
    def state(self) -> LifecycleState:
        return self._state

    async def start(self, local_url: str) -> TunnelResult:
        if self._state.running:
            return self._state.ready or TunnelFailure(FailureKind.NOT_READY)
        try:
            result = await self._provider.start(local_url)
        except Exception as error:
            failure = classify_failure(error)
            return TunnelFailure(FailureKind.START_FAILED, failure.kind)
        if isinstance(result, TunnelFailure):
            return result
        checked = validate_remote_endpoint(result.endpoint.url)
        if isinstance(checked, TunnelFailure):
            try:
                await self._provider.stop()
            except Exception:
                return TunnelFailure(FailureKind.START_FAILED, "cleanup_failed")
            return checked
        ready = TunnelReady(checked)
        self._state = LifecycleState(True, ready)
        return ready

    async def health(self) -> TunnelResult:
        if not self._state.running or self._state.ready is None:
            return TunnelFailure(FailureKind.NOT_READY)
        try:
            healthy = await self._provider.healthy()
        except Exception as error:
            return classify_failure(error)
        if not healthy:
            return TunnelFailure(FailureKind.PROCESS_EXITED)
        return self._state.ready

    async def stop(self) -> TunnelFailure | None:
        if self._state.running:
            try:
                await self._provider.stop()
            except Exception as error:
                return classify_failure(error)
        self._state = LifecycleState()
        return None

    async def __aenter__(self) -> "TunnelController":
        return self

    async def __aexit__(self, *_) -> None:
        await self.stop()
