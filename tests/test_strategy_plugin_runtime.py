"""Runtime plugin fallback and Base Logic enforcement tests."""

import importlib

import pytest

from salareen_thief.base_logic.state_types import Coordinate
from salareen_thief.strategy.gateway import StrategyGateway
from salareen_thief.strategy.results import PluginError, ValidatedDecision
from salareen_thief.strategy.selector import select_strategy


def selection(tmp_path, monkeypatch, name: str, method: str):
    source = (
        "from salareen_thief.base_logic.actions import MoveAction, MoveChoice\n"
        "from salareen_thief.base_logic.state_types import Coordinate, Role\n"
        "from salareen_thief.strategy.results import ProposedAction\n"
        f"class Plugin:\n{method}\n"
    )
    (tmp_path / f"{name}.py").write_text(source, encoding="utf-8")
    monkeypatch.syspath_prepend(str(tmp_path))
    importlib.invalidate_caches()
    private = tmp_path / f"{name}.toml"
    private.write_text(f'[strategy]\nthief_class = "{name}:Plugin"\n', encoding="utf-8")
    return select_strategy(private)


@pytest.mark.parametrize(
    ("name", "method", "error"),
    [
        (
            "raising_plugin",
            "    def propose(self, snapshot):\n        raise RuntimeError('secret')",
            PluginError.RUNTIME_EXCEPTION,
        ),
        (
            "wrong_result_plugin",
            "    def propose(self, snapshot):\n        return object()",
            PluginError.INVALID_RESULT,
        ),
        (
            "illegal_plugin",
            "    def propose(self, snapshot):\n"
            "        return ProposedAction(MoveAction(Role.THIEF, MoveChoice.NORTH, "
            "Coordinate(2, 4)), 0)",
            PluginError.PROPOSAL_REJECTED,
        ),
        (
            "wrong_role_plugin",
            "    def propose(self, snapshot):\n"
            "        return ProposedAction(MoveAction(Role.COP, MoveChoice.STAY), 0)",
            PluginError.PROPOSAL_REJECTED,
        ),
    ],
)
def test_runtime_failure_uses_visible_validated_fallback(
    tmp_path, monkeypatch, rules, initial_game, name, method, error
) -> None:
    selected = selection(tmp_path, monkeypatch, name, method)
    before = initial_game
    result = StrategyGateway(rules, selected.policy).decide(
        initial_game, Coordinate(3, 4)
    )
    assert isinstance(result, ValidatedDecision)
    assert result.state.positions.thief == Coordinate(3, 4)
    assert result.fallback_reason.error is error
    assert initial_game is before


def test_runtime_fallback_is_repeatable(
    tmp_path, monkeypatch, rules, initial_game
) -> None:
    selected = selection(
        tmp_path,
        monkeypatch,
        "repeat_plugin",
        "    def propose(self, snapshot):\n        raise ValueError('private value')",
    )
    gateway = StrategyGateway(rules, selected.policy)
    first = gateway.decide(initial_game, Coordinate(4, 4))
    second = gateway.decide(initial_game, Coordinate(4, 4))
    assert first == second
    assert first.fallback_reason.detail == "ValueError"
    assert "private value" not in first.fallback_reason.detail
