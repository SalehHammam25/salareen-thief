"""Tests for Annex F values and coordinate bounds."""

from copy import deepcopy

import pytest

from salareen_thief.base_logic.config_errors import ConfigErrorCategory as Error
from salareen_thief.base_logic.config_results import (
    ConfigAccepted,
    ConfigRejected,
)
from salareen_thief.base_logic.config_validation import validate_config

MINIMUMS = (
    ("board_and_agents", "grid_size", 7),
    ("movement_and_barriers", "max_barriers", 14),
    ("movement_and_barriers", "max_moves", 35),
    ("movement_and_barriers", "survival_threshold", 35),
)
FIXED = (
    ("board_and_agents", "num_agents", 2),
    ("scoring", "capture_cop", 20),
    ("scoring", "capture_thief", 5),
    ("scoring", "survival_cop", 5),
    ("scoring", "survival_thief", 10),
    ("scoring", "technical_loss", 0),
)


def first_error(data) -> Error:
    result = validate_config(data)
    assert isinstance(result, ConfigRejected)
    assert not hasattr(result, "value")
    return result.issues[0].category


@pytest.mark.parametrize("section,key,minimum", MINIMUMS)
def test_below_minimum_is_rejected(
    default_data, section: str, key: str, minimum: int
) -> None:
    default_data[section][key] = minimum - 1
    assert first_error(default_data) is Error.BELOW_MINIMUM


@pytest.mark.parametrize("section,key,minimum", MINIMUMS)
def test_increased_minimum_is_accepted(
    default_data, section: str, key: str, minimum: int
) -> None:
    default_data[section][key] = minimum + 1
    if key in ("max_moves", "survival_threshold"):
        default_data[section]["max_moves"] = minimum + 1
        default_data[section]["survival_threshold"] = minimum + 1
    result = validate_config(default_data)
    assert isinstance(result, ConfigAccepted)


def test_unequal_ceiling_and_survival_are_rejected(default_data) -> None:
    default_data["movement_and_barriers"]["max_moves"] = 36
    result = validate_config(default_data)
    assert isinstance(result, ConfigRejected)
    assert result.issues[-1].category is Error.RELATIONSHIP_MISMATCH
    assert result.issues[-1].path == (
        "movement_and_barriers",
        "survival_threshold",
    )


def test_equal_increased_ceiling_and_survival_are_accepted(default_data) -> None:
    movement = default_data["movement_and_barriers"]
    movement["max_moves"] = movement["survival_threshold"] = 40
    assert isinstance(validate_config(default_data), ConfigAccepted)


@pytest.mark.parametrize("section,key,expected", FIXED)
def test_fixed_deviation_is_rejected(
    default_data, section: str, key: str, expected: int
) -> None:
    default_data[section][key] = expected + 1
    assert first_error(default_data) is Error.FIXED_VALUE_DEVIATION


def test_move_set_order_is_fixed(default_data) -> None:
    default_data["movement_and_barriers"]["move_set"] = [
        "S",
        "N",
        "E",
        "W",
        "STAY",
    ]
    assert first_error(default_data) is Error.FIXED_VALUE_DEVIATION


@pytest.mark.parametrize("field", ("thief_start", "cop_start"))
def test_position_out_of_bounds(default_data, field: str) -> None:
    default_data["board_and_agents"][field] = [7, 0]
    assert first_error(default_data) is Error.OUT_OF_BOUNDS


def test_nonzero_start_index_bounds(default_data) -> None:
    board = default_data["board_and_agents"]
    board["axis_start_index"] = 1
    board["thief_start"] = [1, 7]
    board["cop_start"] = [7, 1]
    assert isinstance(validate_config(default_data), ConfigAccepted)


def test_origin_is_an_opaque_negotiated_string(default_data) -> None:
    default_data["board_and_agents"]["axis_origin_corner"] = "agreed-value"
    assert isinstance(validate_config(default_data), ConfigAccepted)


def test_same_start_cell_is_not_rejected_without_requirement(default_data) -> None:
    board = default_data["board_and_agents"]
    board["cop_start"] = deepcopy(board["thief_start"])
    assert isinstance(validate_config(default_data), ConfigAccepted)
