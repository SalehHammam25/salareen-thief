"""Approved default tie order and unbounded-size search tests."""

import subprocess
import sys

import pytest

from salareen_thief.base_logic.actions import MoveChoice
from salareen_thief.base_logic.state_types import Board, Coordinate, EpisodeStatus
from salareen_thief.strategy.blind import BlindShortestPath
from salareen_thief.strategy.models import StrategySnapshot, snapshot_for
from salareen_thief.strategy.results import ProposedAction
from salareen_thief.strategy.selector import DEFAULT_CLASS_PATH
from salareen_thief.strategy.tie import DEFAULT_MOVEMENT_ORDER


@pytest.mark.parametrize(
    ("target", "expected"),
    [
        (Coordinate(2, 2), MoveChoice.NORTH),
        (Coordinate(2, 4), MoveChoice.NORTH),
        (Coordinate(4, 2), MoveChoice.SOUTH),
        (Coordinate(4, 4), MoveChoice.SOUTH),
    ],
)
def test_every_two_way_equal_path_uses_configured_order(
    initial_game, target, expected
) -> None:
    result = BlindShortestPath().propose(snapshot_for(initial_game, target))
    assert isinstance(result, ProposedAction)
    assert result.action.choice is expected


def test_default_class_path_imports() -> None:
    module_name, class_name = DEFAULT_CLASS_PATH.split(":")
    module = __import__(module_name, fromlist=[class_name])
    policy = getattr(module, class_name)()
    assert isinstance(policy, BlindShortestPath)


def test_default_order_matches_fixed_shared_move_set(accepted_config) -> None:
    configured = tuple(choice.value for choice in DEFAULT_MOVEMENT_ORDER)
    assert configured + (MoveChoice.STAY.value,) == accepted_config.movement.move_set


def test_default_tie_is_repeatable(initial_game) -> None:
    snapshot = snapshot_for(initial_game, Coordinate(4, 4))
    assert BlindShortestPath().propose(snapshot) == BlindShortestPath().propose(snapshot)


def test_default_tie_is_repeatable_in_fresh_processes() -> None:
    script = (
        "from salareen_thief.base_logic.state_types import *; "
        "from salareen_thief.strategy.blind import BlindShortestPath; "
        "from salareen_thief.strategy.models import StrategySnapshot; "
        "s=StrategySnapshot(Board(7,0,'top-left'),Coordinate(3,3),frozenset(),"
        "EpisodeStatus.ACTIVE,Coordinate(4,4)); print(BlindShortestPath().propose(s))"
    )
    outputs = [
        subprocess.run(
            [sys.executable, "-c", script], capture_output=True, text=True, check=True
        ).stdout
        for _ in range(2)
    ]
    assert outputs[0] == outputs[1]


@pytest.mark.parametrize("size", [50, 100, 150])
def test_representative_large_boards_obey_n_squared_bound(size) -> None:
    snapshot = StrategySnapshot(
        Board(size, 0, "top-left"),
        Coordinate(0, 0),
        frozenset(),
        EpisodeStatus.ACTIVE,
        Coordinate(size - 1, size - 1),
    )
    result = BlindShortestPath().propose(snapshot)
    assert isinstance(result, ProposedAction)
    assert result.explored_cells == size**2
    assert result.action.choice is MoveChoice.SOUTH
