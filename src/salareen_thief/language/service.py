"""Bounded verbal generation that cannot execute spatial actions."""

import asyncio
from dataclasses import dataclass, replace
from enum import StrEnum

from .accounting import TokenLedger
from .hints import HINT_VERSION, HintAccepted, has_forbidden_numeric, validate_hint
from .models import FreeLanguageHint, VerbalRequest
from .providers import TemplateProvider, VerbalProvider


class FallbackReason(StrEnum):
    NOT_SCHEDULED = "not_scheduled"
    PROVIDER_ERROR = "provider_error"
    TIMEOUT = "timeout"
    INVALID_OUTPUT = "invalid_output"
    BUDGET = "budget"


@dataclass(frozen=True, slots=True)
class VerbalResult:
    hint: FreeLanguageHint | None
    ledger: TokenLedger
    fallback_reason: FallbackReason | None = None


class VerbalService:
    def __init__(self, provider: VerbalProvider, every_n_steps: int, timeout: float):
        if every_n_steps < 1 or timeout <= 0:
            raise ValueError("invalid verbal service limits")
        self._provider = provider
        self._every = every_n_steps
        self._timeout = timeout
        self._fallback = TemplateProvider()

    async def generate(
        self, request: VerbalRequest, ledger: TokenLedger, max_words: int
    ) -> VerbalResult:
        if request.turn % self._every:
            return VerbalResult(None, ledger, FallbackReason.NOT_SCHEDULED)
        if ledger.exhausted:
            return await self._use_fallback(
                request, ledger, max_words, FallbackReason.BUDGET
            )
        try:
            safe_request = request
            if has_forbidden_numeric(request.context):
                safe_request = replace(
                    request, context="[direct-coordinate content removed]"
                )
            reply = await asyncio.wait_for(
                self._provider.generate(safe_request), timeout=self._timeout
            )
            updated = ledger.record(reply)
            if updated.consumed > updated.budget:
                return await self._use_fallback(
                    request, updated, max_words, FallbackReason.BUDGET
                )
            checked = validate_hint(
                FreeLanguageHint(HINT_VERSION, request.game_id, reply.text), max_words
            )
            if not isinstance(checked, HintAccepted):
                return await self._use_fallback(
                    request, updated, max_words, FallbackReason.INVALID_OUTPUT
                )
            return VerbalResult(checked.hint, updated)
        except TimeoutError:
            return await self._use_fallback(
                request, ledger, max_words, FallbackReason.TIMEOUT
            )
        except ValueError:
            return await self._use_fallback(
                request, ledger, max_words, FallbackReason.PROVIDER_ERROR
            )
        except Exception:
            return await self._use_fallback(
                request, ledger, max_words, FallbackReason.PROVIDER_ERROR
            )

    async def _use_fallback(
        self,
        request: VerbalRequest,
        ledger: TokenLedger,
        max_words: int,
        reason: FallbackReason,
    ) -> VerbalResult:
        reply = await self._fallback.generate(request)
        checked = validate_hint(
            FreeLanguageHint(HINT_VERSION, request.game_id, reply.text), max_words
        )
        hint = checked.hint if isinstance(checked, HintAccepted) else None
        return VerbalResult(hint, ledger, reason)
