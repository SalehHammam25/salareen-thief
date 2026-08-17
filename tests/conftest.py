"""Shared configuration fixtures."""

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from salareen_thief.base_logic.config_results import ConfigAccepted
from salareen_thief.base_logic.config_validation import validate_config
from salareen_thief.base_logic.rules import BaseLogicRules
from salareen_thief.base_logic.state_factory import initial_state
from salareen_thief.base_logic.state_results import StateAccepted


@pytest.fixture
def default_data() -> dict[str, Any]:
    data = json.loads(Path("config/game.json").read_text(encoding="utf-8"))
    return deepcopy(data)


@pytest.fixture
def write_config(tmp_path: Path):
    def write(data: Any) -> Path:
        path = tmp_path / "game.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    return write


@pytest.fixture
def accepted_config(default_data):
    result = validate_config(default_data)
    assert isinstance(result, ConfigAccepted)
    return result.value


@pytest.fixture
def initial_game(accepted_config):
    result = initial_state(accepted_config)
    assert isinstance(result, StateAccepted)
    return result.value


@pytest.fixture
def rules(accepted_config):
    return BaseLogicRules(accepted_config)
