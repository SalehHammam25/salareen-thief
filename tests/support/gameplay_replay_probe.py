"""Fresh-process deterministic replay probe."""

import json
from pathlib import Path

from replay_support import replay_actions

from salareen_thief.base_logic.action_results import ActionAccepted
from salareen_thief.base_logic.actions import (
    BarrierAction,
    CaptureClaim,
    MoveAction,
    MoveChoice,
)
from salareen_thief.base_logic.config_loader import load_config
from salareen_thief.base_logic.config_results import ConfigAccepted
from salareen_thief.base_logic.rules import BaseLogicRules
from salareen_thief.base_logic.state_factory import build_state, initial_state
from salareen_thief.base_logic.state_results import StateAccepted
from salareen_thief.base_logic.state_types import CaptureCause, Coordinate, Role


def accepted_state(config, *, thief, cop, barriers=()):
    result = build_state(config, thief=thief, cop=cop, barriers=barriers)
    assert isinstance(result, StateAccepted)
    return result.value


def summary(state):
    outcome = None
    if state.outcome is not None:
        outcome = (
            state.outcome.kind.value,
            state.outcome.capture_cause.value
            if state.outcome.capture_cause is not None
            else None,
        )
    return {
        "board": (
            state.board.grid_size,
            state.board.axis_start_index,
            state.board.axis_origin_corner,
        ),
        "positions": {
            "thief": (state.positions.thief.row, state.positions.thief.col),
            "cop": (state.positions.cop.row, state.positions.cop.col),
        },
        "barriers": sorted((item.row, item.col) for item in state.barriers),
        "barrier_usage": state.barrier_usage,
        "barrier_quota": state.barrier_quota,
        "valid_steps": state.valid_steps,
        "status": state.status.value,
        "outcome": outcome,
    }


def main() -> None:
    fixture_path = Path("tests/fixtures/gameplay-replay.json")
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    config_result = load_config(payload["config_path"])
    assert isinstance(config_result, ConfigAccepted)
    state_result = initial_state(config_result.value)
    assert isinstance(state_result, StateAccepted)
    assert payload["initial_state"] == "from_config"
    actions = tuple(
        MoveAction(Role(item["role"]), MoveChoice(item["choice"]))
        for item in payload["actions"]
    )
    rules = BaseLogicRules(config_result.value)
    results = replay_actions(rules, state_result.value, actions)
    assert all(isinstance(result, ActionAccepted) for result in results)
    states = [summary(result.state) for result in results]
    own = rules.apply(
        state_result.value,
        BarrierAction(Role.COP, state_result.value.positions.cop),
    )
    assert isinstance(own, ActionAccepted)
    states.append(summary(own.state))
    barrier_state = accepted_state(
        config_result.value,
        thief=Coordinate(0, 1),
        cop=Coordinate(0, 0),
    )
    barrier_capture = rules.apply(
        barrier_state,
        BarrierAction(
            Role.COP,
            Coordinate(0, 1),
            CaptureClaim(Role.COP, CaptureCause.BARRIER_ON_THIEF),
        ),
    )
    assert isinstance(barrier_capture, ActionAccepted)
    states.append(summary(barrier_capture.state))
    trapped = accepted_state(
        config_result.value,
        thief=Coordinate(0, 0),
        cop=Coordinate(6, 6),
        barriers=(Coordinate(0, 1), Coordinate(1, 0)),
    )
    trapped_capture = rules.apply(
        trapped, CaptureClaim(Role.COP, CaptureCause.TRAPPED_THIEF)
    )
    assert isinstance(trapped_capture, ActionAccepted)
    states.append(summary(trapped_capture.state))
    print(json.dumps(states, sort_keys=True))


if __name__ == "__main__":
    main()
