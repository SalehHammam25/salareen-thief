"""Provider contract; concrete account selection remains external."""

from typing import Protocol

from .models import TunnelResult


class TunnelProvider(Protocol):
    @property
    def version(self) -> str: ...

    async def start(self, local_url: str) -> TunnelResult: ...

    async def healthy(self) -> bool: ...

    async def stop(self) -> None: ...
