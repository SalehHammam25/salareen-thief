"""Focused tests for thief police-estimation from cleaned wire fields."""

from salareen_thief.base_logic.state_types import Board, Coordinate
from salareen_thief.evasion.observer import PoliceObserver
from salareen_thief.official.engine import ThiefEngine
from salareen_thief.official.wire import clean_turn

BOARD = Board(7, 0, "top-left")
COMMIT = "1" * 40


def rings(cell: Coordinate) -> dict[str, float]:
    grid = {}
    for row in range(7):
        for col in range(7):
            ring = max(abs(row - cell.row), abs(col - cell.col))
            if ring < 3:
                grid[f"{row},{col}"] = (0.9, 0.6, 0.3)[ring]
    return grid


def turn(step: int, **changes) -> dict:
    value = {
        "step": step,
        "sender": "police",
        "commit": f"{step:064x}",
        "hint": "",
        "smell_grid": {},
        "timestamp": "",
        "barrier_placed": None,
        "capture_claim": None,
        "claim_response": None,
        "win_claim": None,
    }
    value.update(changes)
    return clean_turn(value)


def test_capture_claim_is_preferred_over_the_scent_peak() -> None:
    observer = PoliceObserver(BOARD, Coordinate(0, 0))
    message = turn(1, capture_claim=[1, 0], smell_grid=rings(Coordinate(0, 1)))
    assert observer.update(message) == Coordinate(1, 0)


def test_the_scent_peak_is_used_when_no_claim_is_present() -> None:
    observer = PoliceObserver(BOARD, Coordinate(0, 0))
    assert observer.update(turn(1, smell_grid=rings(Coordinate(0, 1)))) == Coordinate(
        0, 1
    )


def test_malformed_empty_and_impossible_information_is_safe() -> None:
    observer = PoliceObserver(BOARD, Coordinate(0, 0))
    for payload in (
        None,
        {},
        {"capture_claim": [1, 2, 3]},
        {"capture_claim": ["a", "b"]},
        {"capture_claim": [9, 9]},
        {"capture_claim": [0.0, 1]},
        {"smell_grid": "not-a-grid"},
        {"smell_grid": {}},
        {"smell_grid": {"a,b": 0.9}},
        {"smell_grid": {"9,9": 0.9}},
        {"smell_grid": {"0,0": True}},
    ):
        assert BOARD.contains(observer.update(payload))
    assert observer.estimate == Coordinate(0, 0)


def test_impossible_jumps_are_rejected_then_allowed_as_evidence_ages() -> None:
    observer = PoliceObserver(BOARD, Coordinate(0, 0))
    assert observer.update(turn(1, capture_claim=[6, 6])) == Coordinate(0, 0)
    assert observer.update(turn(2, capture_claim=[1, 0])) == Coordinate(1, 0)
    for _ in range(12):
        observer.update({})
    assert observer.update(turn(3, capture_claim=[6, 6])) == Coordinate(6, 6)


def test_engine_leaves_the_corner_and_survives_a_silent_chaser() -> None:
    engine = ThiefEngine(1, COMMIT)
    police, incoming, seen = Coordinate(0, 0), None, []
    for step in range(1, 36):
        engine.take_turn(incoming)
        seen.append(engine.position)
        if engine.position == police:
            raise AssertionError(f"walked into the police at step {step}")
        row = police.row + (1 if police.row < engine.position.row else -1)
        col = police.col
        if police.row == engine.position.row:
            row, col = police.row, police.col + (
                1 if police.col < engine.position.col else -1
            )
        police = Coordinate(row, col)
        incoming = turn(step, smell_grid=rings(police))
        assert not engine.receive(incoming).caught
    assert len(set(seen)) >= 8


def test_repeated_runs_produce_identical_decisions() -> None:
    def transcript() -> list[str]:
        engine = ThiefEngine(1, COMMIT)
        incoming, moves = None, []
        for step in range(1, 20):
            engine.take_turn(incoming)
            moves.append(engine.records[-1]["payload"]["move"])
            incoming = turn(step, capture_claim=[min(step, 6), 0])
            engine.receive(incoming)
        return moves

    assert transcript() == transcript()


def test_only_cleaned_wire_information_reaches_the_estimate() -> None:
    engine = ThiefEngine(1, COMMIT)
    engine.receive(turn(1, smell_grid={"1,0": 0.9}))
    assert engine.observer.estimate == Coordinate(1, 0)
    assert not hasattr(engine, "cop")
