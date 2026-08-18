import asyncio
from pathlib import Path

from salareen_thief.base_logic.config_loader import load_config
from salareen_thief.base_logic.config_results import ConfigAccepted
from salareen_thief.base_logic.state_factory import initial_state
from salareen_thief.base_logic.state_results import StateAccepted
from salareen_thief.language.accounting import TokenLedger
from salareen_thief.live_match.stage4 import Stage4Boundary
from salareen_thief.scent.field import empty_field

CONFIG = Path(__file__).parents[1] / "config" / "game.json"


def boundary(tmp_path, cadence=1):
    loaded = load_config(CONFIG)
    assert isinstance(loaded, ConfigAccepted)
    state = initial_state(loaded.value)
    assert isinstance(state, StateAccepted)
    private = tmp_path / "private.toml"
    private.write_text(f"[trash_talk]\nprovider='template'\nevery_n_steps={cadence}\n")
    return Stage4Boundary(CONFIG, state.value.board, private), state.value.board


def test_template_cadence_and_actual_accounting(tmp_path):
    stage4, board = boundary(tmp_path, cadence=2)
    scent = empty_field(board)
    _, first = asyncio.run(stage4.outbound("game", 1, scent))
    _, second = asyncio.run(stage4.outbound("game", 2, scent))
    assert first is None and second is not None
    assert stage4.ledger.consumed == 0


def test_exhausted_budget_uses_template_without_consumption(tmp_path):
    stage4, board = boundary(tmp_path)
    stage4.ledger = TokenLedger(0)
    _, hint = asyncio.run(stage4.outbound("game", 1, empty_field(board)))
    assert hint is not None and stage4.ledger == TokenLedger(0)


def test_scent_precedes_language_and_invalid_hint_is_immutable(tmp_path):
    stage4, board = boundary(tmp_path)
    scent = empty_field(board)
    payload = {
        "axis_start_index": scent.axis_start_index,
        "values": [[str(value) for value in row] for row in scent.values],
    }
    assert stage4.receive_scent(1, payload)
    before = stage4.belief
    assert not stage4.receive_hint(1, "go to row 3")
    assert stage4.belief == before
    assert stage4.receive_hint(1, "I kept moving nearby.")
