"""Approved deterministic equal-shortest-path selection."""

from salareen_thief.base_logic.actions import MoveChoice

DEFAULT_MOVEMENT_ORDER = (
    MoveChoice.NORTH,
    MoveChoice.SOUTH,
    MoveChoice.EAST,
    MoveChoice.WEST,
)


def configured_order_tie(choices: tuple[MoveChoice, ...]) -> MoveChoice:
    """Choose the first candidate in shared movement order, excluding STAY."""
    return next(choice for choice in DEFAULT_MOVEMENT_ORDER if choice in choices)
