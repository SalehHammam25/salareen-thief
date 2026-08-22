"""Focused tests for the deterministic lightweight thief evasion policy."""

import inspect
from pathlib import Path

from salareen_thief.base_logic.actions import MoveChoice
from salareen_thief.base_logic.movement import target_for, validate_target
from salareen_thief.base_logic.state_types import Board, Coordinate
from salareen_thief.evasion.observer import manhattan
from salareen_thief.evasion.policy import EvasionPolicy, destinations
from salareen_thief.official.engine import ThiefEngine

BOARD = Board(7, 0, "top-left")
EMPTY: frozenset[Coordinate] = frozenset()
POLICY = EvasionPolicy(BOARD)


def cell_for(origin: Coordinate, name: str) -> Coordinate:
    return target_for(origin, MoveChoice(name))


def test_does_not_freeze_in_a_corner() -> None:
    corner = Coordinate(6, 6)
    name = POLICY.choose(corner, EMPTY, Coordinate(0, 0), [corner])
    assert name != "STAY"
    assert cell_for(corner, name) != corner


def test_avoids_short_repeated_loops_from_a_corner() -> None:
    position, history = Coordinate(6, 6), [Coordinate(6, 6)]
    for _ in range(8):
        name = POLICY.choose(position, EMPTY, Coordinate(0, 0), history)
        position = cell_for(position, name)
        history.append(position)
    assert len(set(history)) >= 4
    pairs = zip(history, history[1:], strict=False)
    assert all(first != second for first, second in pairs)
    cycles = zip(history, history[2:], strict=False)
    assert all(first != third for first, third in cycles)


def test_avoids_police_adjacency_when_a_safer_move_exists() -> None:
    thief, police = Coordinate(3, 3), Coordinate(3, 4)
    name = POLICY.choose(thief, EMPTY, police, [thief])
    assert manhattan(cell_for(thief, name), police) >= 2


def test_never_steps_onto_the_estimated_police_cell() -> None:
    police = Coordinate(3, 4)
    for row in range(7):
        for col in range(7):
            thief = Coordinate(row, col)
            if thief == police:
                continue
            name = POLICY.choose(thief, EMPTY, police, [thief])
            assert cell_for(thief, name) != police


def test_prefers_higher_mobility_escape_cells() -> None:
    barriers = frozenset({Coordinate(5, 6), Coordinate(6, 5)})
    open_cell, penned_cell = Coordinate(3, 3), Coordinate(6, 6)
    reach: dict[Coordinate, int] = {open_cell: 4, penned_cell: 4}
    assert POLICY.score(open_cell, barriers, reach, []) > POLICY.score(
        penned_cell, barriers, reach, []
    )
    assert len(destinations(BOARD, open_cell, barriers)) > len(
        destinations(BOARD, penned_cell, barriers)
    )


def test_returns_a_legal_move_when_every_option_is_dangerous() -> None:
    thief, police = Coordinate(0, 0), Coordinate(1, 0)
    barriers = frozenset({Coordinate(0, 1)})
    name = POLICY.choose(thief, barriers, police, [thief])
    target = cell_for(thief, name)
    assert validate_target(BOARD, thief, target, barriers) is None
    assert manhattan(target, police) <= 1


def test_every_selected_move_is_legal_everywhere() -> None:
    barriers = frozenset({Coordinate(2, 2), Coordinate(2, 3), Coordinate(3, 2)})
    for row in range(7):
        for col in range(7):
            thief = Coordinate(row, col)
            if thief in barriers:
                continue
            for police in (Coordinate(0, 0), Coordinate(6, 6), Coordinate(3, 4)):
                if police == thief:
                    continue
                name = POLICY.choose(thief, barriers, police, [thief])
                target = cell_for(thief, name)
                assert validate_target(BOARD, thief, target, barriers) is None


def test_recent_cells_are_penalised_in_the_score() -> None:
    cell = Coordinate(3, 3)
    reach = {cell: 5}
    fresh = POLICY.score(cell, EMPTY, reach, [])
    seen = POLICY.score(cell, EMPTY, reach, [cell, cell])
    assert seen < fresh


def test_a_missing_estimate_still_yields_a_legal_move() -> None:
    name = POLICY.choose(Coordinate(3, 3), EMPTY, None, [])
    assert name in {"N", "S", "E", "W", "STAY"}


def test_policy_is_total_and_legal_over_a_wide_state_sweep() -> None:
    cells = [Coordinate(row, col) for row in range(7) for col in range(7)]
    barrier_sets = (
        EMPTY,
        frozenset({Coordinate(3, col) for col in range(7)}),
        frozenset(
            cell
            for cell in cells
            if (cell.row + cell.col) % 2 == 0 and cell != Coordinate(3, 3)
        ),
    )
    seen = 0
    for barriers in barrier_sets:
        free = [cell for cell in cells if cell not in barriers]
        for thief in free:
            for police in (*free[::5], None):
                name = POLICY.choose(thief, barriers, police, [thief, thief])
                assert name in {"N", "S", "E", "W", "STAY"}
                target = cell_for(thief, name)
                assert validate_target(BOARD, thief, target, barriers) is None
                seen += 1
    assert seen > 500


def test_production_engine_keeps_no_broad_strategy_fallback() -> None:
    source = Path(inspect.getfile(ThiefEngine)).read_text(encoding="utf-8")
    assert "except" not in source
    assert "fallback" not in source
