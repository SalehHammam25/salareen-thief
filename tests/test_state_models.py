"""Tests for immutable board, coordinate, role, and initial state models."""

from dataclasses import FrozenInstanceError

import pytest

from salareen_thief.base_logic.config_results import ConfigAccepted
from salareen_thief.base_logic.config_validation import validate_config
from salareen_thief.base_logic.state_factory import initial_state
from salareen_thief.base_logic.state_results import StateAccepted
from salareen_thief.base_logic.state_types import (
    Coordinate,
    EpisodeStatus,
    Role,
)


def accepted_config(data):
    result = validate_config(data)
    assert isinstance(result, ConfigAccepted)
    return result.value


def test_coordinate_equality_hashing_and_immutability() -> None:
    coordinate = Coordinate(3, 3)
    assert coordinate == Coordinate(3, 3)
    assert {coordinate, Coordinate(3, 3)} == {coordinate}
    with pytest.raises(FrozenInstanceError):
        coordinate.row = 4


def test_fixed_roles() -> None:
    assert tuple(Role) == (Role.THIEF, Role.COP)


def test_initial_state_uses_validated_configuration(default_data) -> None:
    config = accepted_config(default_data)
    result = initial_state(config)
    assert isinstance(result, StateAccepted)
    state = result.value
    assert state.board.grid_size == config.board.grid_size
    assert state.positions.thief == Coordinate(*config.board.thief_start)
    assert state.positions.cop == Coordinate(*config.board.cop_start)
    assert state.barriers == frozenset()
    assert state.barrier_usage == 0
    assert state.barrier_quota == config.movement.max_barriers
    assert state.valid_steps == 0
    assert state.status is EpisodeStatus.ACTIVE
    assert state.outcome is None
    assert not hasattr(state, "__dict__")
    with pytest.raises(FrozenInstanceError):
        state.valid_steps = 1


def test_coordinate_bounds_ignore_directional_orientation(default_data) -> None:
    board = default_data["board_and_agents"]
    board["axis_start_index"] = 10
    board["thief_start"] = [10, 16]
    board["cop_start"] = [16, 10]
    state = initial_state(accepted_config(default_data))
    assert isinstance(state, StateAccepted)
    assert state.value.board.contains(Coordinate(10, 16))
    assert not state.value.board.contains(Coordinate(9, 16))
