"""Watchdog and architectural isolation tests."""

import ast
from pathlib import Path

import pytest

from salareen_thief.cloud_tunneling.watchdog import evaluate_watchdog


def test_watchdog_uses_strict_negotiated_threshold() -> None:
    assert evaluate_watchdog(10, 70, 60).expired is False
    status = evaluate_watchdog(10, 70.001, 60)
    assert status.expired is True
    assert status.elapsed == pytest.approx(60.001)


def test_watchdog_rejects_bool_and_invalid_timeline() -> None:
    with pytest.raises(TypeError):
        evaluate_watchdog(False, 10, 60)
    with pytest.raises(ValueError):
        evaluate_watchdog(10, 9, 60)


def test_cloud_package_has_no_base_strategy_language_or_crypto_imports() -> None:
    forbidden = {
        "salareen_thief.base_logic",
        "salareen_thief.strategy",
        "salareen_thief.language",
        "salareen_thief.belief",
        "cryptography",
    }
    violations: list[tuple[str, str]] = []
    for path in Path("src/salareen_thief/cloud_tunneling").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            for name in names:
                if any(name == item or name.startswith(f"{item}.") for item in forbidden):
                    violations.append((str(path), name))
    assert violations == []


def test_no_real_provider_adapter_or_credential_literal_exists() -> None:
    files = tuple(Path("src/salareen_thief/cloud_tunneling").glob("*.py"))
    source = "\n".join(path.read_text(encoding="utf-8") for path in files)
    assert "ngrok" not in source.casefold()
    assert "localtonet" not in source.casefold()
    assert "auth_token" not in source.casefold()
