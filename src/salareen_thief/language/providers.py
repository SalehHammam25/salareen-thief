"""Provider-neutral verbal generation and deterministic template fallback."""

from typing import Protocol

from .models import ProviderReply, VerbalRequest


class VerbalProvider(Protocol):
    async def generate(self, request: VerbalRequest) -> ProviderReply: ...


class TemplateProvider:
    async def generate(self, request: VerbalRequest) -> ProviderReply:
        area = request.map_area.strip()
        text = f"I kept moving near {area}." if area else "I kept moving nearby."
        return ProviderReply(text, 0, 0)
