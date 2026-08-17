"""Conservative qualitative-region interpretation."""

import re
from collections.abc import Callable

from salareen_thief.base_logic.state_types import Board, Coordinate

Predicate = Callable[[Coordinate], bool]
WORDS = re.compile(r"[^\W\d_]+", re.UNICODE)


def qualitative_predicate(text: str, board: Board) -> Predicate | None:
    words = {word.casefold() for word in WORDS.findall(text)}
    start, end = board.axis_start_index, board.maximum_index
    doubled_midpoint = start + end
    predicates: list[Predicate] = []
    if "north" in words:
        predicates.append(lambda cell: 2 * cell.row < doubled_midpoint)
    if "south" in words:
        predicates.append(lambda cell: 2 * cell.row > doubled_midpoint)
    if "west" in words or "left" in words:
        predicates.append(lambda cell: 2 * cell.col < doubled_midpoint)
    if "east" in words or "right" in words:
        predicates.append(lambda cell: 2 * cell.col > doubled_midpoint)
    if "center" in words or "centre" in words:
        predicates.append(
            lambda cell: abs(2 * cell.row - doubled_midpoint) <= 1
            and abs(2 * cell.col - doubled_midpoint) <= 1
        )
    if not predicates:
        return None
    return lambda cell: all(predicate(cell) for predicate in predicates)
