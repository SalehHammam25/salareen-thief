"""Negative and repeatability tests for state construction."""

from salareen_thief.base_logic.config_results import ConfigAccepted
from salareen_thief.base_logic.config_validation import validate_config
from salareen_thief.base_logic.state_factory import build_state, initial_state
from salareen_thief.base_logic.state_results import (
    StateAccepted,
    StateRejected,
)
from salareen_thief.base_logic.state_results import StateErrorCategory as Error
from salareen_thief.base_logic.state_types import (
    Coordinate,
    EpisodeStatus,
    Outcome,
    OutcomeKind,
)


def config_from(data):
    result = validate_config(data)
    assert isinstance(result, ConfigAccepted)
    return result.value


def errors(result: StateRejected) -> tuple[Error, ...]:
    assert isinstance(result, StateRejected)
    return tuple(issue.category for issue in result.issues)


def build(default_data, **changes):
    config = config_from(default_data)
    values = {
        "thief": Coordinate(*config.board.thief_start),
        "cop": Coordinate(*config.board.cop_start),
    }
    values.update(changes)
    return build_state(config, **values)


def test_positions_must_be_in_bounds(default_data) -> None:
    result = build(default_data, thief=Coordinate(7, 0))
    assert errors(result) == (Error.POSITION_OUT_OF_BOUNDS,)


def test_barriers_must_be_unique(default_data) -> None:
    barrier = Coordinate(1, 1)
    result = build(default_data, barriers=(barrier, barrier))
    assert errors(result) == (Error.DUPLICATE_BARRIER,)


def test_barriers_must_be_in_bounds(default_data) -> None:
    result = build(default_data, barriers=(Coordinate(7, 0),))
    assert errors(result) == (Error.BARRIER_OUT_OF_BOUNDS,)


def test_active_thief_cannot_occupy_barrier(default_data) -> None:
    result = build(default_data, barriers=(Coordinate(3, 3),))
    assert errors(result) == (Error.INVALID_BARRIER_OCCUPANCY,)


def test_barrier_usage_must_be_nonnegative(default_data) -> None:
    assert errors(build(default_data, barrier_usage=-1)) == (
        Error.NEGATIVE_BARRIER_USAGE,
    )


def test_barrier_usage_cannot_exceed_quota(default_data) -> None:
    assert errors(build(default_data, barrier_usage=15)) == (
        Error.BARRIER_QUOTA_EXCEEDED,
    )


def test_valid_steps_must_be_nonnegative(default_data) -> None:
    assert errors(build(default_data, valid_steps=-1)) == (
        Error.NEGATIVE_VALID_STEPS,
    )


def test_bool_is_not_valid_barrier_usage(default_data) -> None:
    assert errors(build(default_data, barrier_usage=True)) == (
        Error.INCORRECT_TYPE,
    )


def test_bool_is_not_valid_step_count(default_data) -> None:
    assert errors(build(default_data, valid_steps=True)) == (
        Error.INCORRECT_TYPE,
    )


def test_bool_is_not_valid_coordinate_component(default_data) -> None:
    result = build(default_data, thief=Coordinate(True, 0))
    assert errors(result) == (Error.INCORRECT_TYPE,)


def test_bool_is_not_valid_barrier_coordinate(default_data) -> None:
    result = build(default_data, barriers=(Coordinate(0, True),))
    assert errors(result) == (Error.INCORRECT_TYPE,)


def test_unhashable_barrier_is_rejected_without_crashing(default_data) -> None:
    result = build(default_data, barriers=([0, 1],))
    assert errors(result) == (Error.INCORRECT_TYPE,)


def test_status_requires_the_explicit_enum(default_data) -> None:
    result = build(default_data, status="active")
    assert errors(result) == (Error.INCORRECT_TYPE,)


def test_outcome_kind_requires_the_explicit_enum(default_data) -> None:
    result = build(default_data, outcome=Outcome("capture"))
    assert errors(result) == (Error.INCORRECT_TYPE,)


def test_capture_outcome_requires_capture_cause(default_data) -> None:
    result = build(
        default_data,
        status=EpisodeStatus.TERMINAL,
        outcome=Outcome(OutcomeKind.CAPTURE),
    )
    assert errors(result) == (Error.STATUS_OUTCOME_MISMATCH,)


def test_active_state_cannot_have_outcome(default_data) -> None:
    result = build(default_data, outcome=Outcome(OutcomeKind.CAPTURE))
    assert errors(result) == (Error.STATUS_OUTCOME_MISMATCH,)


def test_terminal_state_requires_outcome(default_data) -> None:
    result = build(default_data, status=EpisodeStatus.TERMINAL)
    assert errors(result) == (Error.STATUS_OUTCOME_MISMATCH,)


def test_terminal_outcome_is_representable(default_data) -> None:
    result = build(
        default_data,
        status=EpisodeStatus.TERMINAL,
        outcome=Outcome(OutcomeKind.TECHNICAL_LOSS),
    )
    assert isinstance(result, StateAccepted)


def test_initial_state_is_repeatable(default_data) -> None:
    config = config_from(default_data)
    assert initial_state(config) == initial_state(config)
