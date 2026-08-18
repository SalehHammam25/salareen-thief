"""Visible deterministic fallback around a trusted local strategy plugin."""

from dataclasses import replace

from .models import StrategySnapshot
from .results import (
    DecisionFailure,
    FallbackReason,
    PluginError,
    ProposalResult,
    ProposedAction,
)


class FallbackPolicy:
    def __init__(self, primary, fallback, reason: FallbackReason | None = None) -> None:
        self._primary = primary
        self._fallback = fallback
        self._reason = reason

    def propose(self, snapshot: StrategySnapshot) -> ProposalResult:
        if self._reason is not None:
            return self._with_reason(self._fallback.propose(snapshot), self._reason)
        try:
            result = self._primary.propose(snapshot)
        except Exception as error:
            reason = FallbackReason(PluginError.RUNTIME_EXCEPTION, type(error).__name__)
            return self._with_reason(self._fallback.propose(snapshot), reason)
        if not isinstance(result, (ProposedAction, DecisionFailure)):
            reason = FallbackReason(PluginError.INVALID_RESULT)
            return self._with_reason(self._fallback.propose(snapshot), reason)
        return result

    def fallback(
        self, snapshot: StrategySnapshot, reason: FallbackReason
    ) -> ProposalResult:
        return self._with_reason(self._fallback.propose(snapshot), reason)

    @staticmethod
    def _with_reason(result: ProposalResult, reason: FallbackReason) -> ProposalResult:
        return replace(result, fallback_reason=reason)
