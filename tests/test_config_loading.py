"""Tests for local JSON loading and decoding failures."""

from pathlib import Path

from salareen_thief.base_logic.config_errors import ConfigErrorCategory as Error
from salareen_thief.base_logic.config_loader import load_config
from salareen_thief.base_logic.config_results import (
    ConfigAccepted,
    ConfigRejected,
)


def only_error(result: ConfigRejected) -> Error:
    assert isinstance(result, ConfigRejected)
    assert len(result.issues) == 1
    return result.issues[0].category


def test_default_file_is_accepted() -> None:
    result = load_config("config/game.json")
    assert isinstance(result, ConfigAccepted)
    assert result.value.board.axis_origin_corner == "top-left"


def test_missing_file_is_rejected(tmp_path: Path) -> None:
    result = load_config(tmp_path / "missing.json")
    assert only_error(result) is Error.FILE_NOT_FOUND


def test_unreadable_file_is_rejected(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / "game.json"
    path.write_text("{}", encoding="utf-8")

    def fail_read(*args, **kwargs):
        raise OSError("denied")

    monkeypatch.setattr(Path, "read_text", fail_read)
    assert only_error(load_config(path)) is Error.FILE_READ_ERROR


def test_malformed_json_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "game.json"
    path.write_text('{"broken":', encoding="utf-8")
    assert only_error(load_config(path)) is Error.MALFORMED_JSON


def test_invalid_utf8_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "game.json"
    path.write_bytes(b"\xff")
    assert only_error(load_config(path)) is Error.MALFORMED_JSON


def test_duplicate_key_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "game.json"
    path.write_text('{"section":{"key":1,"key":2}}', encoding="utf-8")
    result = load_config(path)
    assert only_error(result) is Error.DUPLICATE_KEY
    assert result.issues[0].path == ("key",)


def test_later_stage_sections_are_ignored(default_data, write_config) -> None:
    default_data["future_stage"] = {"unvalidated": object().__class__.__name__}
    default_data["pheromones"] = {"invalid_but_ignored": True}
    result = load_config(write_config(default_data))
    assert isinstance(result, ConfigAccepted)
    assert not hasattr(result.value, "future_stage")
