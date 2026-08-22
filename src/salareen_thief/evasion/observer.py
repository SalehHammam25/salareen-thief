"""Deterministic police-position estimation from cleaned wire fields only."""

from salareen_thief.base_logic.state_types import Board, Coordinate


def manhattan(left: Coordinate, right: Coordinate) -> int:
    """Return the orthogonal grid distance between two cells."""
    return abs(left.row - right.row) + abs(left.col - right.col)


def valid_cell(value: object, board: Board) -> Coordinate | None:
    """Accept only an in-board integer ``[row, col]`` pair."""
    if type(value) is not list or len(value) != 2:
        return None
    if any(type(part) is not int for part in value):
        return None
    candidate = Coordinate(value[0], value[1])
    return candidate if board.contains(candidate) else None


def scent_peak(grid: object, board: Board) -> Coordinate | None:
    """Return the strongest in-board scent cell, ties by lowest row then col."""
    if not isinstance(grid, dict) or not grid:
        return None
    best_rank: tuple[float, int, int] | None = None
    best_cell: Coordinate | None = None
    for key, intensity in grid.items():
        if not isinstance(key, str) or isinstance(intensity, bool):
            continue
        if not isinstance(intensity, (int, float)):
            continue
        parts = key.split(",")
        if len(parts) != 2:
            continue
        try:
            cell = Coordinate(int(parts[0]), int(parts[1]))
        except ValueError:
            continue
        if not board.contains(cell):
            continue
        rank = (float(intensity), -cell.row, -cell.col)
        if best_rank is None or rank > best_rank:
            best_rank, best_cell = rank, cell
    return best_cell


class PoliceObserver:
    """Track a single police estimate, rejecting physically impossible jumps."""

    def __init__(self, board: Board, start: Coordinate) -> None:
        self.board = board
        self.estimate = start
        self.age = 0

    def update(self, message: object) -> Coordinate:
        """Fold one cleaned peer message into the current estimate."""
        self.age += 1
        if not isinstance(message, dict):
            return self.estimate
        candidate = valid_cell(message.get("capture_claim"), self.board)
        if candidate is None:
            candidate = scent_peak(message.get("smell_grid"), self.board)
        if candidate is None:
            return self.estimate
        if manhattan(candidate, self.estimate) > self.age:
            return self.estimate
        self.estimate, self.age = candidate, 0
        return self.estimate
