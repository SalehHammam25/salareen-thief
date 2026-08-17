"""Immutable Stage 4 verbal data contracts."""

from dataclasses import dataclass
from enum import StrEnum


class ProviderMode(StrEnum):
    TEMPLATE = "template"
    OLLAMA = "ollama"
    CLAUDE_API = "claude_api"
    CLAUDE_CLI = "claude_cli"


class HintClaim(StrEnum):
    UNVERIFIED = "unverified"
    SELF_DECLARED_TRUTH = "self_declared_truth"
    SELF_DECLARED_LIE = "self_declared_lie"


@dataclass(frozen=True, slots=True)
class FreeLanguageHint:
    version: str
    game_id: str
    text: str
    claim: HintClaim = HintClaim.UNVERIFIED


@dataclass(frozen=True, slots=True)
class VerbalRequest:
    game_id: str
    turn: int
    map_area: str
    context: str
    instruction: str = (
        "Use qualitative natural language only. Never provide direct coordinates."
    )


@dataclass(frozen=True, slots=True)
class ProviderReply:
    text: str
    request_tokens: int
    response_tokens: int
