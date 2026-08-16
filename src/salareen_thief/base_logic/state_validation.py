"""Deterministic validation of state representation invariants."""

from collections.abc import Iterable

from .state_results import StateErrorCategory as Category
from .state_results import StateIssue
from .state_types import Board, Coordinate, EpisodeStatus, Outcome, OutcomeKind


def _issue(category: Category, field: str, message: str) -> StateIssue:
    return StateIssue(category, field, message)


def _coordinate_is_exact(coordinate: object) -> bool:
    return (
        type(coordinate) is Coordinate
        and type(coordinate.row) is int
        and type(coordinate.col) is int
    )


def validate_state(
    board: Board,
    thief: Coordinate,
    cop: Coordinate,
    barriers: Iterable[Coordinate],
    barrier_usage: int,
    barrier_quota: int,
    valid_steps: int,
    status: EpisodeStatus,
    outcome: Outcome | None,
) -> tuple[frozenset[Coordinate], tuple[StateIssue, ...]]:
    """Return normalized barriers and ordered representation issues."""
    barrier_items = tuple(barriers)
    valid_barriers = tuple(
        item for item in barrier_items if _coordinate_is_exact(item)
    )
    barrier_set = frozenset(valid_barriers)
    issues: list[StateIssue] = []
    for field, position in (("thief", thief), ("cop", cop)):
        if not _coordinate_is_exact(position):
            issues.append(
                _issue(Category.INCORRECT_TYPE, field, "invalid coordinate type")
            )
        elif not board.contains(position):
            issues.append(
                _issue(Category.POSITION_OUT_OF_BOUNDS, field, "outside board")
            )
    invalid_barriers = len(valid_barriers) != len(barrier_items)
    if invalid_barriers:
        issues.append(
            _issue(Category.INCORRECT_TYPE, "barriers", "invalid coordinate type")
        )
    elif any(not board.contains(item) for item in sorted(barrier_set)):
        issues.append(
            _issue(Category.BARRIER_OUT_OF_BOUNDS, "barriers", "outside board")
        )
    if not invalid_barriers and len(barrier_items) != len(barrier_set):
        issues.append(
            _issue(Category.DUPLICATE_BARRIER, "barriers", "must be unique")
        )
    if type(barrier_usage) is not int:
        issues.append(
            _issue(Category.INCORRECT_TYPE, "barrier_usage", "expected integer")
        )
    elif barrier_usage < 0:
        issues.append(
            _issue(Category.NEGATIVE_BARRIER_USAGE, "barrier_usage", "negative")
        )
    elif barrier_usage > barrier_quota:
        issues.append(
            _issue(Category.BARRIER_QUOTA_EXCEEDED, "barrier_usage", "over quota")
        )
    if type(valid_steps) is not int:
        issues.append(
            _issue(Category.INCORRECT_TYPE, "valid_steps", "expected integer")
        )
    elif valid_steps < 0:
        issues.append(
            _issue(Category.NEGATIVE_VALID_STEPS, "valid_steps", "negative")
        )
    valid_status = type(status) is EpisodeStatus
    valid_outcome = outcome is None or (
        type(outcome) is Outcome and type(outcome.kind) is OutcomeKind
    )
    if not valid_status or not valid_outcome:
        issues.append(
            _issue(Category.INCORRECT_TYPE, "status_outcome", "invalid type")
        )
    elif (status is EpisodeStatus.ACTIVE) != (outcome is None):
        issues.append(
            _issue(Category.STATUS_OUTCOME_MISMATCH, "status", "inconsistent")
        )
    return barrier_set, tuple(issues)
