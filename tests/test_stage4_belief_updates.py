"""Exact scent and qualitative-language belief updates."""

from decimal import Decimal

import pytest

from salareen_thief.base_logic.state_types import Board, Coordinate
from salareen_thief.belief.models import BeliefFallback, BeliefUpdated
from salareen_thief.belief.pipeline import BeliefHintRejected, apply_evidence
from salareen_thief.belief.prior import uniform_prior
from salareen_thief.belief.updates import update_from_language, update_from_scent
from salareen_thief.language.hints import HINT_VERSION
from salareen_thief.language.models import FreeLanguageHint
from salareen_thief.scent.models import ScentGrid

D = Decimal


def grid(values: tuple[tuple[str, ...], ...]) -> ScentGrid:
    return ScentGrid(0, tuple(tuple(D(value) for value in row) for row in values))


def total(result: BeliefUpdated) -> Decimal:
    return sum((value for row in result.belief.probabilities for value in row), D("0"))


def test_scent_likelihood_is_monotonic_and_normalized() -> None:
    prior = uniform_prior(Board(2, 0, "top-left"))
    result = update_from_scent(prior, grid((("0", "0.3"), ("0.6", "0.9"))))
    assert isinstance(result, BeliefUpdated)
    values = [
        result.belief.at(Coordinate(row, col)) for row in range(2) for col in range(2)
    ]
    assert values == sorted(values)
    assert total(result) == D("1")


@pytest.mark.parametrize("reliability", (D("0.5"), D("0.75"), D("1.0")))
def test_language_reliability_weights_regions(reliability: Decimal) -> None:
    prior = uniform_prior(Board(3, 0, "top-left"))
    result = update_from_language(prior, "north west", reliability)
    assert isinstance(result, BeliefUpdated)
    match = result.belief.at(Coordinate(0, 0))
    nonmatch = result.belief.at(Coordinate(2, 2))
    if reliability == D("0.5"):
        assert abs(match - nonmatch) <= D("1e-27")
    else:
        assert match > nonmatch
    assert total(result) == D("1")


def test_unknown_language_is_neutral() -> None:
    prior = uniform_prior(Board(3, 0, "top-left"))
    result = update_from_language(prior, "near the old river", D("0.75"))
    assert result == BeliefUpdated(prior)


def test_zero_weight_preserves_prior_with_visible_fallback() -> None:
    prior = uniform_prior(Board(3, 0, "top-left"))
    result = update_from_language(prior, "north south", D("1"))
    assert isinstance(result, BeliefFallback)
    assert result.belief is prior


def test_invalid_reliability_preserves_prior() -> None:
    prior = uniform_prior(Board(2, 0, "top-left"))
    assert isinstance(update_from_language(prior, "north", D("0.49")), BeliefFallback)
    assert isinstance(update_from_language(prior, "north", 0.75), BeliefFallback)


def test_pipeline_rejects_coordinates_before_belief_processing() -> None:
    prior = uniform_prior(Board(2, 0, "top-left"))
    hint = FreeLanguageHint(HINT_VERSION, "game-1", "position ٣,٤")
    result = apply_evidence(prior, grid((("0", "0"), ("0", "0"))), hint, 15, D("0.75"))
    assert isinstance(result, BeliefHintRejected)
    assert result.belief is prior


def test_pipeline_applies_scent_before_qualitative_language() -> None:
    prior = uniform_prior(Board(2, 0, "top-left"))
    scent = grid((("0.9", "0"), ("0", "0")))
    hint = FreeLanguageHint(HINT_VERSION, "game-1", "north west")
    result = apply_evidence(prior, scent, hint, 15, D("0.75"))
    scented = update_from_scent(prior, scent)
    assert isinstance(scented, BeliefUpdated)
    assert result == update_from_language(scented.belief, hint.text, D("0.75"))
