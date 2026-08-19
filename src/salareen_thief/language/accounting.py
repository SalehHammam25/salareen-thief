"""Immutable actual-token accounting for one series."""

from dataclasses import dataclass

from .models import ProviderReply


@dataclass(frozen=True, slots=True)
class TokenLedger:
    budget: int
    consumed: int = 0

    def record(self, reply: ProviderReply) -> "TokenLedger":
        values = (reply.request_tokens, reply.response_tokens)
        if any(
            isinstance(value, bool) or not isinstance(value, int) or value < 0
            for value in values
        ):
            raise ValueError("provider token counts must be nonnegative integers")
        updated = self.consumed + sum(values)
        return TokenLedger(self.budget, updated)

    @property
    def remaining(self) -> int:
        return max(0, self.budget - self.consumed)

    @property
    def exhausted(self) -> bool:
        return self.consumed >= self.budget
