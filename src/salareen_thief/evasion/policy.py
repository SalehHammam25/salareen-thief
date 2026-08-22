"""Deterministic single-ply thief evasion scoring over legal geometry."""

from collections import deque

from salareen_thief.base_logic.state_types import Board, Coordinate

from .observer import manhattan

ORDER = (("N", -1, 0), ("S", 1, 0), ("E", 0, 1), ("W", 0, -1), ("STAY", 0, 0))
UNREACHABLE = 99
SAFE_DISTANCE = 2
RECENT_WINDOW = 6
ROOM_RADIUS = 2
DISTANCE_WEIGHT = 8
MOBILITY_WEIGHT = 5
ROOM_WEIGHT = 1
RECENT_WEIGHT = 7


def destinations(
    board: Board, origin: Coordinate, barriers: frozenset[Coordinate]
) -> tuple[Coordinate, ...]:
    """Return the legal orthogonal destinations, never counting STAY."""
    cells = []
    for _, row_delta, col_delta in ORDER[:4]:
        cell = Coordinate(origin.row + row_delta, origin.col + col_delta)
        if board.contains(cell) and cell not in barriers:
            cells.append(cell)
    return tuple(cells)


def distance_map(
    board: Board, origin: Coordinate, barriers: frozenset[Coordinate]
) -> dict[Coordinate, int]:
    """Return barrier-aware breadth-first distances from one origin."""
    distances = {origin: 0}
    pending = deque([origin])
    while pending:
        current = pending.popleft()
        for cell in destinations(board, current, barriers):
            if cell not in distances:
                distances[cell] = distances[current] + 1
                pending.append(cell)
    return distances


def room_size(
    board: Board,
    origin: Coordinate,
    barriers: frozenset[Coordinate],
    radius: int = ROOM_RADIUS,
) -> int:
    """Count legal cells within a bounded radius, penalising corners."""
    seen = {origin}
    frontier = [origin]
    for _ in range(radius):
        following: list[Coordinate] = []
        for cell in frontier:
            for step in destinations(board, cell, barriers):
                if step not in seen:
                    seen.add(step)
                    following.append(step)
        frontier = following
    return len(seen)


def recent_penalty(cell: Coordinate, history: object) -> int:
    """Count recent occupations of one cell inside the memory window."""
    if not isinstance(history, (list, tuple)) or not history:
        return 0
    return sum(1 for visited in history[-RECENT_WINDOW:] if visited == cell)


class EvasionPolicy:
    """Choose the safest reachable cell without search, randomness, or clocks."""

    def __init__(self, board: Board) -> None:
        self.board = board

    def candidates(
        self, position: Coordinate, barriers: frozenset[Coordinate]
    ) -> tuple[tuple[str, Coordinate], ...]:
        """Return legal ``(choice, destination)`` pairs in fixed order."""
        options: list[tuple[str, Coordinate]] = []
        for name, row_delta, col_delta in ORDER:
            if name == "STAY":
                options.append((name, position))
                continue
            cell = Coordinate(position.row + row_delta, position.col + col_delta)
            if self.board.contains(cell) and cell not in barriers:
                options.append((name, cell))
        return tuple(options)

    def score(
        self,
        cell: Coordinate,
        barriers: frozenset[Coordinate],
        reach: dict[Coordinate, int],
        history: object,
    ) -> int:
        """Rank one destination by distance, mobility, room, and novelty."""
        distance = min(reach.get(cell, UNREACHABLE), UNREACHABLE)
        mobility = len(destinations(self.board, cell, barriers))
        return (
            DISTANCE_WEIGHT * distance
            + MOBILITY_WEIGHT * mobility
            + ROOM_WEIGHT * room_size(self.board, cell, barriers)
            - RECENT_WEIGHT * recent_penalty(cell, history)
        )

    def choose(
        self,
        position: Coordinate,
        barriers: frozenset[Coordinate],
        police: Coordinate | None,
        history: object = (),
    ) -> str:
        """Return one legal move choice; STAY is always a legal last resort."""
        options = self.candidates(position, barriers)
        reach = {} if police is None else distance_map(self.board, police, barriers)
        safe = [
            item
            for item in options
            if police is None or manhattan(item[1], police) >= SAFE_DISTANCE
        ]
        pool = safe or list(options)
        ranked = [
            (self.score(cell, barriers, reach, history), -index, name)
            for index, (name, cell) in enumerate(pool)
        ]
        return max(ranked)[2]
