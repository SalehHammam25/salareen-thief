"""Tests for required configuration structure and types."""

import pytest

from salareen_thief.base_logic.config_errors import ConfigErrorCategory as Error
from salareen_thief.base_logic.config_results import ConfigRejected
from salareen_thief.base_logic.config_validation import validate_config

REQUIRED_PATHS = (
    ("board_and_agents", "grid_size"),
    ("board_and_agents", "num_agents"),
    ("board_and_agents", "thief_start"),
    ("board_and_agents", "cop_start"),
    ("board_and_agents", "axis_origin_corner"),
    ("board_and_agents", "axis_start_index"),
    ("movement_and_barriers", "move_set"),
    ("movement_and_barriers", "max_barriers"),
    ("movement_and_barriers", "max_moves"),
    ("movement_and_barriers", "survival_threshold"),
    ("scoring", "capture_cop"),
    ("scoring", "capture_thief"),
    ("scoring", "survival_cop"),
    ("scoring", "survival_thief"),
    ("scoring", "technical_loss"),
)
INTEGER_PATHS = (
    ("board_and_agents", "grid_size"),
    ("board_and_agents", "num_agents"),
    ("board_and_agents", "axis_start_index"),
    ("movement_and_barriers", "max_barriers"),
    ("movement_and_barriers", "max_moves"),
    ("movement_and_barriers", "survival_threshold"),
    ("scoring", "capture_cop"),
    ("scoring", "capture_thief"),
    ("scoring", "survival_cop"),
    ("scoring", "survival_thief"),
    ("scoring", "technical_loss"),
)


def categories(data) -> list[Error]:
    result = validate_config(data)
    assert isinstance(result, ConfigRejected)
    return [issue.category for issue in result.issues]


@pytest.mark.parametrize(
    "section",
    ("board_and_agents", "movement_and_barriers", "scoring"),
)
def test_missing_section(default_data, section: str) -> None:
    del default_data[section]
    assert categories(default_data)[0] is Error.MISSING_KEY


@pytest.mark.parametrize("section,key", REQUIRED_PATHS)
def test_each_required_key(default_data, section: str, key: str) -> None:
    del default_data[section][key]
    assert categories(default_data)[0] is Error.MISSING_KEY


@pytest.mark.parametrize("section,key", INTEGER_PATHS)
def test_bool_is_not_an_integer(default_data, section: str, key: str) -> None:
    default_data[section][key] = True
    assert categories(default_data)[0] is Error.INCORRECT_TYPE


@pytest.mark.parametrize("bad", (None, "7", 7.0, [], {}))
def test_incorrect_grid_type(default_data, bad) -> None:
    default_data["board_and_agents"]["grid_size"] = bad
    assert categories(default_data)[0] is Error.INCORRECT_TYPE


@pytest.mark.parametrize("bad", ([1], [1, 2, 3], [True, 1], ["1", 2]))
def test_incorrect_coordinate_shape(default_data, bad) -> None:
    default_data["board_and_agents"]["thief_start"] = bad
    assert categories(default_data)[0] is Error.INCORRECT_TYPE


def test_issue_order_follows_schema(default_data) -> None:
    del default_data["board_and_agents"]["grid_size"]
    del default_data["movement_and_barriers"]["move_set"]
    result = validate_config(default_data)
    assert isinstance(result, ConfigRejected)
    assert [issue.path for issue in result.issues] == [
        ("board_and_agents", "grid_size"),
        ("movement_and_barriers", "move_set"),
    ]


def test_mixed_issue_order_is_repeatable(default_data) -> None:
    del default_data["board_and_agents"]["thief_start"]
    default_data["board_and_agents"]["grid_size"] = 6
    default_data["movement_and_barriers"]["move_set"] = ["STAY"]
    first = validate_config(default_data)
    second = validate_config(default_data)
    assert isinstance(first, ConfigRejected)
    assert first == second
    assert [issue.category for issue in first.issues] == [
        Error.MISSING_KEY,
        Error.BELOW_MINIMUM,
        Error.FIXED_VALUE_DEVIATION,
    ]
