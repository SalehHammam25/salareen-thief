"""Trusted private plugin selection and visible fallback tests."""

import importlib
from pathlib import Path

import pytest

from salareen_thief.base_logic.state_types import Coordinate
from salareen_thief.strategy.gateway import StrategyGateway
from salareen_thief.strategy.results import PluginError, ValidatedDecision
from salareen_thief.strategy.selector import DEFAULT_CLASS_PATH, select_strategy


def private_config(tmp_path: Path, reference: str | None) -> Path:
    path = tmp_path / "game.toml"
    content = "[network]\nmy_port = 1\n"
    if reference is not None:
        content += f'[strategy]\nthief_class = "{reference}"\n'
    path.write_text(content, encoding="utf-8")
    return path


def plugin_module(tmp_path: Path, monkeypatch, name: str, body: str) -> str:
    (tmp_path / f"{name}.py").write_text(body, encoding="utf-8")
    monkeypatch.syspath_prepend(str(tmp_path))
    importlib.invalidate_caches()
    return name


def decision(selection, rules, initial_game, target=None):
    target = Coordinate(3, 4) if target is None else target
    return StrategyGateway(rules, selection.policy).decide(initial_game, target)


def test_missing_strategy_section_selects_builtin(tmp_path, rules, initial_game) -> None:
    selection = select_strategy(private_config(tmp_path, None))
    result = decision(selection, rules, initial_game)
    assert selection.configured_reference is None
    assert selection.fallback_reason is None
    assert isinstance(result, ValidatedDecision)
    assert result.fallback_reason is None


def test_missing_and_malformed_private_files_fall_back_visibly(tmp_path) -> None:
    missing = select_strategy(tmp_path / "missing.toml")
    assert missing.fallback_reason.error is PluginError.CONFIG_READ_ERROR
    malformed = tmp_path / "malformed.toml"
    malformed.write_text("[strategy\nhidden_value = 'private'", encoding="utf-8")
    selected = select_strategy(malformed)
    assert selected.fallback_reason.error is PluginError.TOML_ERROR
    assert selected.fallback_reason.detail == ""


def test_valid_plugin_loads_and_receives_restricted_snapshot(
    tmp_path, monkeypatch, rules, initial_game
) -> None:
    name = plugin_module(
        tmp_path,
        monkeypatch,
        "valid_thief_plugin",
        "from salareen_thief.strategy.blind import BlindShortestPath\n"
        "class Good(BlindShortestPath):\n    pass\n",
    )
    selection = select_strategy(private_config(tmp_path, f"{name}:Good"))
    result = decision(selection, rules, initial_game)
    assert selection.configured_reference == f"{name}:Good"
    assert selection.fallback_reason is None
    assert isinstance(result, ValidatedDecision)


@pytest.mark.parametrize("reference", ["bad", "a:b:c", "a-b:Class", ":Class"])
def test_malformed_reference_falls_back_visibly(
    tmp_path, reference, rules, initial_game
) -> None:
    selection = select_strategy(private_config(tmp_path, reference))
    result = decision(selection, rules, initial_game)
    assert selection.fallback_reason.error is PluginError.MALFORMED_REFERENCE
    assert selection.configured_reference is None
    assert result.fallback_reason == selection.fallback_reason


def test_missing_module_and_class_are_stable(tmp_path, monkeypatch) -> None:
    missing = select_strategy(private_config(tmp_path, "no_such_module:Policy"))
    assert missing.fallback_reason.error is PluginError.MODULE_NOT_FOUND
    name = plugin_module(tmp_path, monkeypatch, "empty_plugin", "VALUE = 1\n")
    no_class = select_strategy(private_config(tmp_path, f"{name}:Missing"))
    assert no_class.fallback_reason.error is PluginError.CLASS_NOT_FOUND


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        ("class Bad:\n    pass\n", PluginError.INVALID_INTERFACE),
        (
            "class Bad:\n    def __init__(self):\n        raise RuntimeError('no')\n",
            PluginError.CONSTRUCTOR_FAILED,
        ),
    ],
)
def test_invalid_interface_and_constructor_fall_back(
    tmp_path, monkeypatch, body, expected
) -> None:
    name = plugin_module(tmp_path, monkeypatch, f"plugin_{expected}", body)
    selection = select_strategy(private_config(tmp_path, f"{name}:Bad"))
    assert selection.fallback_reason.error is expected


def test_shared_json_cannot_select_strategy(tmp_path, rules, initial_game) -> None:
    shared = tmp_path / "game.json"
    shared.write_text('{"strategy":{"thief_class":"remote:Attack"}}', encoding="utf-8")
    selection = select_strategy(private_config(tmp_path, None))
    result = decision(selection, rules, initial_game)
    assert shared.exists()
    assert selection.configured_reference is None
    assert isinstance(result, ValidatedDecision)
    assert result.fallback_reason is None


def test_default_path_is_not_read_from_shared_configuration() -> None:
    assert DEFAULT_CLASS_PATH == "salareen_thief.strategy.blind:BlindShortestPath"
