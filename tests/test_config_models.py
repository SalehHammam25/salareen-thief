"""Tests for immutable, slotted validated configuration."""

from dataclasses import FrozenInstanceError

import pytest

from salareen_thief.base_logic.config_results import ConfigAccepted
from salareen_thief.base_logic.config_validation import validate_config


def test_validated_configuration_is_frozen_and_slotted(default_data) -> None:
    result = validate_config(default_data)
    assert isinstance(result, ConfigAccepted)
    config = result.value
    assert not hasattr(config, "__dict__")
    assert not hasattr(config.board, "__dict__")
    assert not hasattr(config.movement, "__dict__")
    assert not hasattr(config.scoring, "__dict__")
    with pytest.raises(FrozenInstanceError):
        config.board.grid_size = 8


def test_every_default_base_logic_value_is_preserved(default_data) -> None:
    result = validate_config(default_data)
    assert isinstance(result, ConfigAccepted)
    config = result.value
    assert (
        config.board.grid_size,
        config.board.num_agents,
        config.board.thief_start,
        config.board.cop_start,
        config.board.axis_origin_corner,
        config.board.axis_start_index,
    ) == (7, 2, (3, 3), (0, 0), "top-left", 0)
    assert (
        config.movement.move_set,
        config.movement.max_barriers,
        config.movement.max_moves,
        config.movement.survival_threshold,
    ) == (("N", "S", "E", "W", "STAY"), 14, 35, 35)
    assert (
        config.scoring.capture_cop,
        config.scoring.capture_thief,
        config.scoring.survival_cop,
        config.scoring.survival_thief,
        config.scoring.technical_loss,
    ) == (20, 5, 5, 10, 0)
