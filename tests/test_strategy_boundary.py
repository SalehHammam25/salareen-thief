"""Static Stage 3 dependency-boundary tests."""

import ast
from pathlib import Path

STRATEGY_ROOT = Path("src/salareen_thief/strategy")
FORBIDDEN = (
    "fastmcp",
    "mcp",
    "salareen_thief.llm",
    "salareen_thief.language",
    "salareen_thief.mcp_transport",
    "salareen_thief.scent",
)


def imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module)
    return found


def test_strategy_has_no_transport_or_stage4_dependencies() -> None:
    violations = {
        path: module
        for path in STRATEGY_ROOT.glob("*.py")
        for module in imports(path)
        if any(module == item or module.startswith(f"{item}.") for item in FORBIDDEN)
    }
    assert violations == {}


def test_base_logic_does_not_import_strategy() -> None:
    base = Path("src/salareen_thief/base_logic")
    violations = {
        path
        for path in base.glob("*.py")
        if any(module.startswith("salareen_thief.strategy") for module in imports(path))
    }
    assert violations == set()
