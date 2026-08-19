"""Validated, privacy-safe GUI data projection."""

import json
from pathlib import Path

from salareen_thief.base_logic.config_loader import load_config
from salareen_thief.base_logic.config_results import ConfigAccepted

from .security.series import privacy_safe_view

MINIMUM_BOARD_SIZE = 7


def load_view(role, artifact_path, config_path):
    loaded = load_config(config_path)
    if not isinstance(loaded, ConfigAccepted):
        raise ValueError("GUI requires a validated game configuration")
    board_size = loaded.value.board.grid_size
    if board_size < MINIMUM_BOARD_SIZE:
        raise ValueError("configured board must be at least 7x7")
    artifact = json.loads(Path(artifact_path).read_text(encoding="utf-8"))
    heatmap = artifact.get("belief_heatmap", [])
    _validate_heatmap(heatmap, board_size)
    view = privacy_safe_view(
        role,
        artifact.get("local_position", [0, 0]),
        artifact.get("public_events", []),
        heatmap,
        artifact.get("turn_status", "LOCKED"),
    )
    view["board_size"] = board_size
    return view


def _validate_heatmap(heatmap, board_size):
    if len(heatmap) != board_size:
        raise ValueError("heatmap row count does not match configured board")
    if any(len(row) != board_size for row in heatmap):
        raise ValueError("heatmap column count does not match configured board")
    try:
        for row in heatmap:
            for value in row:
                float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("heatmap values must be numeric") from exc

