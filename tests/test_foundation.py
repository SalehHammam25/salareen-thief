"""Tests for the Stage 1 package and dependency boundary."""

from __future__ import annotations

import ast
from importlib.util import resolve_name
from pathlib import Path

import pytest

import salareen_thief
import salareen_thief.base_logic

SOURCE_ROOT = Path("src")
BASE_LOGIC = SOURCE_ROOT / "salareen_thief" / "base_logic"
EXTERNAL_FORBIDDEN = {
    "anthropic",
    "cryptography",
    "fastmcp",
    "mcp",
    "openai",
    "requests",
}
INTERNAL_FORBIDDEN = (
    "salareen_thief.cryptography",
    "salareen_thief.llm",
    "salareen_thief.networking",
    "salareen_thief.strategy",
)


def package_for_path(path: Path) -> str:
    """Return the containing import package for a source file."""
    parts = path.relative_to(SOURCE_ROOT).with_suffix("").parts
    package_parts = parts if path.name == "__init__.py" else parts[:-1]
    return ".".join(package_parts)


def imported_modules(path: Path, package: str | None = None) -> set[str]:
    """Return absolute module targets imported by one Python file."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    current_package = package or package_for_path(path)
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            relative = "." * node.level + (node.module or "")
            base = (
                resolve_name(relative, current_package)
                if node.level
                else node.module
            )
            if base:
                modules.add(base)
                modules.update(
                    f"{base}.{alias.name}"
                    for alias in node.names
                    if alias.name != "*"
                )
    return modules


def is_forbidden(module: str) -> bool:
    """Return whether a module crosses the deterministic boundary."""
    root = module.split(".", 1)[0]
    external = root in EXTERNAL_FORBIDDEN
    internal = any(
        module == prefix or module.startswith(f"{prefix}.")
        for prefix in INTERNAL_FORBIDDEN
    )
    return external or internal


def forbidden_imports(path: Path, package: str | None = None) -> set[str]:
    """Return forbidden imports found in a Python source file."""
    return {
        module
        for module in imported_modules(path, package)
        if is_forbidden(module)
    }


def test_src_packages_are_importable() -> None:
    assert salareen_thief.__doc__ == "Thief peer package."
    assert "Deterministic game rules boundary" in salareen_thief.base_logic.__doc__


def test_base_logic_has_no_later_stage_dependencies() -> None:
    violations = {
        path: forbidden_imports(path)
        for path in BASE_LOGIC.rglob("*.py")
        if forbidden_imports(path)
    }
    assert violations == {}


@pytest.mark.parametrize(
    "statement, expected",
    [
        ("import salareen_thief.strategy\n", "salareen_thief.strategy"),
        ("from .. import networking\n", "salareen_thief.networking"),
    ],
)
def test_scanner_detects_internal_import(
    tmp_path: Path, statement: str, expected: str
) -> None:
    fixture = tmp_path / "fixture.py"
    fixture.write_text(statement, encoding="utf-8")
    assert expected in forbidden_imports(
        fixture, package="salareen_thief.base_logic"
    )


@pytest.mark.parametrize("dependency", sorted(EXTERNAL_FORBIDDEN))
def test_scanner_detects_external_import(
    tmp_path: Path, dependency: str
) -> None:
    fixture = tmp_path / "fixture.py"
    fixture.write_text(f"import {dependency}\n", encoding="utf-8")
    assert dependency in forbidden_imports(
        fixture, package="salareen_thief.base_logic"
    )
