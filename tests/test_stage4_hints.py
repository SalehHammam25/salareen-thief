"""Free-language contract tests."""

import pytest

from salareen_thief.language.hints import (
    HINT_VERSION,
    HintAccepted,
    HintError,
    HintRejected,
    validate_hint,
)
from salareen_thief.language.models import FreeLanguageHint, HintClaim


def hint(text: str, version: str = HINT_VERSION) -> FreeLanguageHint:
    return FreeLanguageHint(version, "game-1", text, HintClaim.UNVERIFIED)


def test_unicode_free_language_is_accepted_and_trimmed() -> None:
    result = validate_hint(hint("  ליד הנהר בניו יורק  "), 15)
    assert isinstance(result, HintAccepted)
    assert result.hint.text == "ליד הנהר בניו יורק"


@pytest.mark.parametrize("text", ["", "  ", "\x00malformed"])
def test_empty_and_malformed_hints_are_rejected(text: str) -> None:
    assert isinstance(validate_hint(hint(text), 15), HintRejected)


def test_version_and_word_limit_are_enforced() -> None:
    wrong = validate_hint(hint("near the park", "v0"), 15)
    oversized = validate_hint(hint("one two three four"), 3)
    assert wrong == HintRejected(HintError.WRONG_VERSION)
    assert oversized == HintRejected(HintError.WORD_LIMIT)
    assert validate_hint(hint("safe"), True) == HintRejected(HintError.WORD_LIMIT)


@pytest.mark.parametrize(
    "text", ["I am at (3, 4)", "position 3,4", "cell [-2, 7]", "x=3 y=4"]
)
def test_direct_numeric_coordinate_protocol_is_rejected(text: str) -> None:
    assert validate_hint(hint(text), 15) == HintRejected(HintError.DIRECT_COORDINATE)


def test_non_coordinate_numbers_remain_blocked_policy_not_overrejected() -> None:
    result = validate_hint(hint("I waited for three turns near 5th Avenue"), 15)
    assert isinstance(result, HintAccepted)


def test_claim_is_unverified_not_cryptographic_truth() -> None:
    claimed = FreeLanguageHint(
        HINT_VERSION, "game-1", "near the park", HintClaim.SELF_DECLARED_TRUTH
    )
    result = validate_hint(claimed, 15)
    assert isinstance(result, HintAccepted)
    assert result.hint.claim is HintClaim.SELF_DECLARED_TRUTH


def test_missing_game_identity_is_malformed() -> None:
    malformed = FreeLanguageHint(HINT_VERSION, "", "near the park")
    assert validate_hint(malformed, 15) == HintRejected(HintError.INVALID_TEXT)
