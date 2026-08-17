"""Uniform exact belief prior tests."""

from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from salareen_thief.base_logic.state_types import Board, Coordinate
from salareen_thief.belief.prior import uniform_prior


def test_uniform_prior_excludes_only_publicly_impossible_cells() -> None:
    board = Board(3, 0, "top-left")
    impossible = frozenset({Coordinate(0, 0), Coordinate(1, 1)})
    belief = uniform_prior(board, impossible)
    assert belief.at(Coordinate(0, 0)) == Decimal("0")
    possible = [
        belief.at(Coordinate(row, col))
        for row in range(3)
        for col in range(3)
        if Coordinate(row, col) not in impossible
    ]
    assert len(set(possible)) == 1
    assert sum((value for row in belief.probabilities for value in row), Decimal("0")) == 1


def test_prior_is_frozen_and_does_not_accept_objective_position() -> None:
    belief = uniform_prior(Board(2, 0, "top-left"))
    assert not hasattr(belief, "opponent_position")
    with pytest.raises(FrozenInstanceError):
        belief.probabilities = ()  # type: ignore[misc]


def test_prior_requires_at_least_one_possible_cell() -> None:
    board = Board(1, 0, "top-left")
    with pytest.raises(ValueError):
        uniform_prior(board, frozenset({Coordinate(0, 0)}))
