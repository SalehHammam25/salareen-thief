"""Exact Stage 4 scent arithmetic tests."""

from decimal import Decimal

from salareen_thief.base_logic.state_types import Board, Coordinate
from salareen_thief.scent.field import decay, emit, empty_field, maximum

D = Decimal


def board(size: int = 7) -> Board:
    return Board(size, 0, "top-left")


def test_every_chebyshev_ring_value_in_five_by_five_window() -> None:
    field = emit(board(), Coordinate(3, 3))
    expected = (
        ("0.3", "0.3", "0.3", "0.3", "0.3"),
        ("0.3", "0.6", "0.6", "0.6", "0.3"),
        ("0.3", "0.6", "0.9", "0.6", "0.3"),
        ("0.3", "0.6", "0.6", "0.6", "0.3"),
        ("0.3", "0.3", "0.3", "0.3", "0.3"),
    )
    actual = tuple(
        tuple(str(field.at(row, col)) for col in range(1, 6)) for row in range(1, 6)
    )
    assert actual == expected
    assert field.at(0, 0) == D("0")


def test_center_edge_and_corner_clip_without_renormalizing() -> None:
    center = emit(board(), Coordinate(3, 3))
    edge = emit(board(), Coordinate(0, 3))
    corner = emit(board(), Coordinate(0, 0))
    assert center.at(3, 3) == edge.at(0, 3) == corner.at(0, 0) == D("0.9")
    assert edge.at(0, 1) == corner.at(0, 2) == D("0.3")
    assert corner.at(2, 2) == D("0.3")
    assert sum(value > 0 for row in corner.values for value in row) == 9


def test_decay_uses_exact_official_factor() -> None:
    decayed = decay(emit(board(), Coordinate(3, 3)))
    assert decayed.at(3, 3) == D("0.81")
    assert decayed.at(2, 3) == D("0.54")
    assert decayed.at(1, 3) == D("0.27")


def test_overlap_uses_order_independent_maximum() -> None:
    left = emit(board(), Coordinate(3, 2))
    right = emit(board(), Coordinate(3, 4))
    assert maximum(left, right) == maximum(right, left)
    combined = maximum(left, right)
    assert combined.at(3, 3) == D("0.6")
    assert all(value <= D("0.9") for row in combined.values for value in row)


def test_empty_field_matches_board_and_origin() -> None:
    shifted = Board(3, 1, "top-left")
    field = empty_field(shifted)
    assert field.axis_start_index == 1
    assert field.at(1, 1) == field.at(3, 3) == D("0")
