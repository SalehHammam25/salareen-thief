"""Validation for free-language messages treated as untrusted text."""

import re
from dataclasses import dataclass
from enum import StrEnum

from .models import FreeLanguageHint

HINT_VERSION = "language-hint-v1"
DIRECT_COORDINATE = re.compile(
    r"(?<!\w)(?:\(\s*-?\d+\s*,\s*-?\d+\s*\)|"
    r"\[\s*-?\d+\s*,\s*-?\d+\s*\]|-?\d+\s*,\s*-?\d+|"
    r"[xy]\s*=\s*-?\d+\s*[,; ]+\s*[xy]\s*=\s*-?\d+)(?!\w)",
    re.IGNORECASE,
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


def validate_hint(hint: FreeLanguageHint, max_words: int) -> HintAccepted | HintRejected:
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
    if DIRECT_COORDINATE.search(text):
        return HintRejected(HintError.DIRECT_COORDINATE)
    return HintAccepted(FreeLanguageHint(hint.version, hint.game_id, text, hint.claim))
