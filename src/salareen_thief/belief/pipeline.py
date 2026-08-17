"""Validate language, then combine scent before language evidence."""

from dataclasses import dataclass
from decimal import Decimal

from salareen_thief.language.hints import HintRejected, validate_hint
from salareen_thief.language.models import FreeLanguageHint
from salareen_thief.scent.models import ScentGrid

from .models import BeliefFallback, BeliefMap, BeliefResult, BeliefUpdated
from .updates import update_from_language, update_from_scent


@dataclass(frozen=True, slots=True)
class BeliefHintRejected:
    rejection: HintRejected
    belief: BeliefMap


def apply_evidence(
    prior: BeliefMap,
    scent: ScentGrid,
    hint: FreeLanguageHint,
    max_words: int,
    reliability: Decimal,
) -> BeliefResult | BeliefHintRejected:
    checked = validate_hint(hint, max_words)
    if isinstance(checked, HintRejected):
        return BeliefHintRejected(checked, prior)
    scented = update_from_scent(prior, scent)
    if isinstance(scented, BeliefFallback):
        return scented
    assert isinstance(scented, BeliefUpdated)
    return update_from_language(scented.belief, checked.hint.text, reliability)
