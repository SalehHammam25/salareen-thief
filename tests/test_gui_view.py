"""GUI board sizing and privacy compliance."""

import json
from types import SimpleNamespace

import pytest

from salareen_thief.base_logic.config_results import ConfigAccepted
from salareen_thief.gui_view import load_view
from salareen_thief.report_gui import _draw_heatmap

CONFIG = "config/game.json"


class FakeCanvas:
    def __init__(self):
        self.rectangles = []

    def create_rectangle(self, *coordinates, **options):
        self.rectangles.append((coordinates, options))


def artifact(tmp_path, heatmap, **extra):
    path = tmp_path / "gui.json"
    payload = {
        "local_position": [1, 2],
        "turn_status": "YOUR TURN",
        "belief_heatmap": heatmap,
        "public_events": [],
        **extra,
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_valid_7_by_7_heatmap_renders_49_cells(tmp_path):
    heatmap = [[row + column for column in range(7)] for row in range(7)]
    view = load_view("thief", artifact(tmp_path, heatmap), CONFIG)
    canvas = FakeCanvas()
    _draw_heatmap(canvas, view["belief_heatmap"], view["board_size"], 420)
    assert view["board_size"] == 7
    assert len(canvas.rectangles) == 49


def test_dimension_mismatch_is_rejected(tmp_path):
    with pytest.raises(ValueError, match="row count"):
        load_view("thief", artifact(tmp_path, [[0.0] * 7] * 6), CONFIG)


def test_below_minimum_board_is_rejected(tmp_path, monkeypatch):
    accepted = ConfigAccepted(SimpleNamespace(board=SimpleNamespace(grid_size=6)))
    monkeypatch.setattr("salareen_thief.gui_view.load_config", lambda path: accepted)
    with pytest.raises(ValueError, match="at least 7x7"):
        load_view("thief", artifact(tmp_path, [[0.0] * 6] * 6), CONFIG)


def test_objective_opponent_position_is_not_projected(tmp_path):
    heatmap = [[0.0] * 7 for _ in range(7)]
    path = artifact(
        tmp_path,
        heatmap,
        objective_opponent_position=[6, 6],
        public_events=[{"event": "turn", "cop_position": [6, 6]}],
    )
    view = load_view("thief", path, CONFIG)
    assert "objective_opponent_position" not in repr(view)
    assert "cop_position" not in repr(view)

