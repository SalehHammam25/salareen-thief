"""Deterministic shortest-distance search over known geometry."""

from collections import deque

from salareen_thief.base_logic.actions import MoveChoice
from salareen_thief.base_logic.movement import target_for, validate_target
from salareen_thief.base_logic.state_types import Coordinate

from .models import StrategySnapshot

ORTHOGONAL = (
    MoveChoice.NORTH,
    MoveChoice.SOUTH,
    MoveChoice.EAST,
    MoveChoice.WEST,
)


def distance_map(snapshot: StrategySnapshot) -> dict[Coordinate, int]:
    """Return shortest distances to target, visiting at most N squared cells."""
    if not snapshot.board.contains(snapshot.target):
        return {}
    if snapshot.target in snapshot.barriers:
        return {}
    distances = {snapshot.target: 0}
    pending = deque([snapshot.target])
    while pending:
        current = pending.popleft()
        for choice in ORTHOGONAL:
            neighbor = target_for(current, choice)
            if (
                snapshot.board.contains(neighbor)
                and neighbor not in snapshot.barriers
                and neighbor not in distances
            ):
                distances[neighbor] = distances[current] + 1
                pending.append(neighbor)
    return distances


def shortest_first_choices(
    snapshot: StrategySnapshot, distances: dict[Coordinate, int]
) -> tuple[MoveChoice, ...]:
    candidates: list[tuple[MoveChoice, int]] = []
    for choice in ORTHOGONAL:
        target = target_for(snapshot.thief, choice)
        if (
            validate_target(snapshot.board, snapshot.thief, target, snapshot.barriers)
            is None
            and target in distances
        ):
            candidates.append((choice, distances[target]))
    if not candidates:
        return ()
    best = min(distance for _, distance in candidates)
    return tuple(choice for choice, distance in candidates if distance == best)
