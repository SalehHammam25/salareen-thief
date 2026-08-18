"""Validation for free-language messages treated as untrusted text."""

import re
from dataclasses import dataclass
from enum import StrEnum

from .models import FreeLanguageHint

HINT_VERSION = "language-hint-v1"
NUMBER_WORD = (
    r"zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|"
    r"twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|"
    r"nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety"
)
WORD_COORDINATE = re.compile(
    rf"\b(?:row|column|col|cell|position|coordinate|x|y)\b\s*"
    rf"(?:is\s+|at\s+|=\s*|:\s*)?(?:{NUMBER_WORD})\b|"
    rf"(?:[\[(]\s*)?(?:{NUMBER_WORD})\s*[,;]\s*(?:{NUMBER_WORD})(?:\s*[\])])?",
    re.IGNORECASE,
)


def has_forbidden_numeric(text: str) -> bool:
    """Reject digits and English number words used as coordinate values."""
    return any(character.isdecimal() for character in text) or bool(
        WORD_COORDINATE.search(text)
    )


class HintError(StrEnum):
    WRONG_VERSION = "wrong_version"
    EMPTY = "empty"
    WORD_LIMIT = "word_limit"
    DIRECT_COORDINATE = "direct_coordinate"
    INVALID_TEXT = "invalid_text"


@dataclass(frozen=True, slots=True)
class HintAccepted:
    hint: FreeLanguageHint


@dataclass(frozen=True, slots=True)
class HintRejected:
    error: HintError


def validate_hint(
    hint: FreeLanguageHint, max_words: int
) -> HintAccepted | HintRejected:
    if isinstance(max_words, bool) or not isinstance(max_words, int) or max_words < 1:
        return HintRejected(HintError.WORD_LIMIT)
    if hint.version != HINT_VERSION:
        return HintRejected(HintError.WRONG_VERSION)
    if not isinstance(hint.game_id, str) or not hint.game_id.strip():
        return HintRejected(HintError.INVALID_TEXT)
    if not isinstance(hint.text, str) or "\x00" in hint.text:
        return HintRejected(HintError.INVALID_TEXT)
    text = hint.text.strip()
    if not text:
        return HintRejected(HintError.EMPTY)
    if len(text.split()) > max_words:
        return HintRejected(HintError.WORD_LIMIT)
    if has_forbidden_numeric(text):
        return HintRejected(HintError.DIRECT_COORDINATE)
    return HintAccepted(FreeLanguageHint(hint.version, hint.game_id, text, hint.claim))
