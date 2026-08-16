"""Shared configuration fixtures."""

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest


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
