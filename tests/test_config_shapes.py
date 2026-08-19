"""Focused tests for JSON structure and forward-compatible extras."""

import pytest

from salareen_thief.base_logic.config_errors import ConfigErrorCategory as Error
from salareen_thief.base_logic.config_results import (
    ConfigAccepted,
    ConfigRejected,
)
from salareen_thief.base_logic.config_validation import validate_config


def first_error(data) -> Error:
    result = validate_config(data)
    assert isinstance(result, ConfigRejected)
    return result.issues[0].category


@pytest.mark.parametrize("root", (None, [], "object", 3, True))
def test_root_must_be_object(root) -> None:
    assert first_error(root) is Error.INCORRECT_TYPE


@pytest.mark.parametrize(
    "section",
    ("board_and_agents", "movement_and_barriers", "scoring"),
)
@pytest.mark.parametrize("bad", (None, [], "object", 3, True))
def test_required_section_must_be_object(default_data, section: str, bad) -> None:
    default_data[section] = bad
    assert first_error(default_data) is Error.INCORRECT_TYPE


@pytest.mark.parametrize("bad", (None, [], {}, 0, True))
def test_origin_must_be_string(default_data, bad) -> None:
    default_data["board_and_agents"]["axis_origin_corner"] = bad
    assert first_error(default_data) is Error.INCORRECT_TYPE


@pytest.mark.parametrize("bad", (None, "N", {}, 0, True, ["N", 1]))
def test_move_set_must_be_string_array(default_data, bad) -> None:
    default_data["movement_and_barriers"]["move_set"] = bad
    assert first_error(default_data) is Error.INCORRECT_TYPE


def test_extra_base_logic_keys_are_ignored(default_data) -> None:
    default_data["board_and_agents"]["future_key"] = {"anything": True}
    assert isinstance(validate_config(default_data), ConfigAccepted)
