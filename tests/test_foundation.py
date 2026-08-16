"""Tests for the Stage 1 package and dependency boundary."""

from __future__ import annotations

import ast
from pathlib import Path

import salareen_thief
import salareen_thief.base_logic

BASE_LOGIC = Path("src/salareen_thief/base_logic")
FORBIDDEN_IMPORT_ROOTS = {
    "anthropic",
    "cryptography",
    "fastmcp",
    "mcp",
    "openai",
    "requests",
}


def imported_roots(path: Path) -> set[str]:
    """Return top-level imported package names from one Python file."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".", 1)[0])
    return roots


def test_src_packages_are_importable() -> None:
    assert salareen_thief.__doc__ == "Thief peer package."
    assert "Deterministic game rules boundary" in salareen_thief.base_logic.__doc__


def test_base_logic_has_no_later_stage_dependencies() -> None:
    imported = set()
    for path in BASE_LOGIC.rglob("*.py"):
        imported.update(imported_roots(path))
    assert imported.isdisjoint(FORBIDDEN_IMPORT_ROOTS)


def test_no_later_stage_packages_exist() -> None:
    package_root = BASE_LOGIC.parent
    deferred = ("strategy", "llm", "networking", "cryptography")
    assert all(not (package_root / name).exists() for name in deferred)
