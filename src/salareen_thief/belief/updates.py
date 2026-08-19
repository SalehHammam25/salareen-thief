"""Exact normalized scent and qualitative-language belief updates."""

from decimal import Decimal, InvalidOperation

from salareen_thief.base_logic.state_types import Coordinate
from salareen_thief.scent.models import ScentGrid

from .models import (
    BeliefFallback,
    BeliefFallbackReason,
    BeliefMap,
    BeliefResult,
    BeliefUpdated,
    normalize_rows,
)
from .qualitative import qualitative_predicate


def _normalize(
    prior: BeliefMap, weights: tuple[tuple[Decimal, ...], ...]
) -> BeliefResult:
    try:
        weighted = tuple(
            tuple(
                probability * weight
                for probability, weight in zip(row, factors, strict=True)
            )
            for row, factors in zip(prior.probabilities, weights, strict=True)
        )
        normalized = normalize_rows(weighted)
        if normalized is None:
            return BeliefFallback(prior, BeliefFallbackReason.ZERO_WEIGHT)
        return BeliefUpdated(BeliefMap(prior.board, normalized))
    except (InvalidOperation, ValueError):
        return BeliefFallback(prior, BeliefFallbackReason.INVALID_EVIDENCE)


def update_from_scent(prior: BeliefMap, scent: ScentGrid) -> BeliefResult:
    if not isinstance(scent, ScentGrid):
        return BeliefFallback(prior, BeliefFallbackReason.INVALID_EVIDENCE)
    if scent.axis_start_index != prior.board.axis_start_index:
        return BeliefFallback(prior, BeliefFallbackReason.INVALID_EVIDENCE)
    weights = tuple(
        tuple(Decimal("1") + strength for strength in row) for row in scent.values
    )
    return _normalize(prior, weights)


def update_from_language(
    prior: BeliefMap, text: str, reliability: Decimal
) -> BeliefResult:
    if not isinstance(text, str) or not isinstance(reliability, Decimal):
        return BeliefFallback(prior, BeliefFallbackReason.INVALID_EVIDENCE)
    if not reliability.is_finite() or not Decimal("0.5") <= reliability <= Decimal("1"):
        return BeliefFallback(prior, BeliefFallbackReason.INVALID_EVIDENCE)
    predicate = qualitative_predicate(text, prior.board)
    if predicate is None:
        return BeliefUpdated(prior)
    start, end = prior.board.axis_start_index, prior.board.maximum_index
    weights = tuple(
        tuple(
            reliability
            if predicate(Coordinate(row, col))
            else Decimal("1") - reliability
            for col in range(start, end + 1)
        )
        for row in range(start, end + 1)
    )
    return _normalize(prior, weights)
