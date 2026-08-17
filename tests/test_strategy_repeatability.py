"""Fresh-process and repeated-input strategy tests."""

import subprocess
import sys

from salareen_thief.base_logic.state_types import Board, Coordinate, EpisodeStatus
from salareen_thief.strategy.blind import BlindShortestPath
from salareen_thief.strategy.models import StrategySnapshot


def snapshot() -> StrategySnapshot:
    return StrategySnapshot(
        Board(7, 0, "top-left"),
        Coordinate(3, 3),
        frozenset({Coordinate(3, 4)}),
        EpisodeStatus.ACTIVE,
        Coordinate(6, 6),
    )


def test_repeated_snapshot_is_identical() -> None:
    policy = BlindShortestPath(lambda choices: choices[0])
    assert policy.propose(snapshot()) == policy.propose(snapshot())


def test_fresh_process_repeatability() -> None:
    script = (
        "from salareen_thief.base_logic.state_types import *; "
        "from salareen_thief.strategy.blind import BlindShortestPath; "
        "from salareen_thief.strategy.models import StrategySnapshot; "
        "s=StrategySnapshot(Board(7,0,'top-left'),Coordinate(3,3),"
        "frozenset({Coordinate(3,4)}),EpisodeStatus.ACTIVE,Coordinate(6,6)); "
        "print(BlindShortestPath(lambda c:c[0]).propose(s))"
    )
    outputs = [
        subprocess.run(
            [sys.executable, "-c", script],
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        for _ in range(2)
    ]
    assert outputs[0] == outputs[1]
