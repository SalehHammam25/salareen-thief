"""Complete-state deterministic replay checks."""

import subprocess
import sys

from support.replay_support import replay_actions

from salareen_thief.base_logic.action_results import ActionAccepted
from salareen_thief.base_logic.actions import (
    BarrierAction,
    CaptureClaim,
    MoveAction,
    MoveChoice,
)
from salareen_thief.base_logic.scoring import score_episode
from salareen_thief.base_logic.state_types import CaptureCause, Coordinate, Role


def replay(rules, initial, actions):
    results = replay_actions(rules, initial, actions)
    assert all(isinstance(result, ActionAccepted) for result in results)
    return tuple(result.state for result in results)


def test_identical_movement_replay_is_equal(rules, initial_game) -> None:
    actions = (
        MoveAction(Role.THIEF, MoveChoice.NORTH),
        MoveAction(Role.THIEF, MoveChoice.EAST),
        MoveAction(Role.THIEF, MoveChoice.STAY),
    )
    assert replay(rules, initial_game, actions) == replay(rules, initial_game, actions)


def test_identical_barrier_replay_is_equal(rules, initial_game) -> None:
    actions = (
        BarrierAction(Role.COP, Coordinate(0, 1)),
        BarrierAction(Role.COP, Coordinate(1, 0)),
    )
    assert replay(rules, initial_game, actions) == replay(rules, initial_game, actions)


def test_identical_terminal_replay_is_equal(rules, accepted_config) -> None:
    from salareen_thief.base_logic.state_factory import build_state
    from salareen_thief.base_logic.state_results import StateAccepted

    built = build_state(
        accepted_config,
        thief=Coordinate(2, 2),
        cop=Coordinate(2, 2),
    )
    assert isinstance(built, StateAccepted)
    actions = (CaptureClaim(Role.COP, CaptureCause.COORDINATE_OVERLAP),)
    first = replay(rules, built.value, actions)
    second = replay(rules, built.value, actions)
    assert first == second
    assert score_episode(first[-1], accepted_config.scoring) == score_episode(
        second[-1], accepted_config.scoring
    )


def test_serializable_fixture_repeats_across_fresh_processes() -> None:
    command = [sys.executable, "tests/support/gameplay_replay_probe.py"]
    first = subprocess.run(command, capture_output=True, text=True, check=True)
    second = subprocess.run(command, capture_output=True, text=True, check=True)
    assert first.stdout == second.stdout
