"""Uniform prior over publicly possible cells."""

from salareen_thief.base_logic.state_types import Board, Coordinate

from .models import ONE, ZERO, BeliefMap, normalize_rows


def uniform_prior(
    board: Board, impossible: frozenset[Coordinate] = frozenset()
) -> BeliefMap:
    possible = tuple(
        Coordinate(row, col)
        for row in range(board.axis_start_index, board.maximum_index + 1)
        for col in range(board.axis_start_index, board.maximum_index + 1)
        if Coordinate(row, col) not in impossible
    )
    if not possible:
        raise ValueError("at least one cell must remain possible")
    values = tuple(
        tuple(
            ONE if Coordinate(row, col) in possible else ZERO
            for col in range(board.axis_start_index, board.maximum_index + 1)
        )
        for row in range(board.axis_start_index, board.maximum_index + 1)
    )
    normalized = normalize_rows(values)
    assert normalized is not None
    return BeliefMap(board, normalized)
