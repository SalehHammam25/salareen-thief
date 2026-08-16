"""Fail when a Python file exceeds the project line limit."""

from __future__ import annotations

import argparse
from collections.abc import Iterable, Sequence
from pathlib import Path

DEFAULT_ROOTS = ("src", "tests", "scripts")
MAX_LINES = 150


def iter_python_files(roots: Iterable[Path]) -> list[Path]:
    """Return Python files below existing roots in stable order."""
    files: set[Path] = set()
    for root in roots:
        if root.is_file() and root.suffix == ".py":
            files.add(root)
        elif root.is_dir():
            files.update(root.rglob("*.py"))
    return sorted(files)


def count_lines(path: Path) -> int:
    """Count physical text lines in a UTF-8 Python file."""
    with path.open(encoding="utf-8") as source:
        return sum(1 for _ in source)


def find_violations(
    roots: Iterable[Path], maximum: int = MAX_LINES
) -> list[tuple[Path, int]]:
    """Return files whose physical line count exceeds maximum."""
    return [
        (path, count)
        for path in iter_python_files(roots)
        if (count := count_lines(path)) > maximum
    ]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse optional roots and maximum line count."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="*", default=list(DEFAULT_ROOTS))
    parser.add_argument("--max-lines", type=int, default=MAX_LINES)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Check configured roots and return a process exit code."""
    args = parse_args(argv)
    roots = [Path(root) for root in args.roots]
    violations = find_violations(roots, args.max_lines)
    if violations:
        for path, count in violations:
            print(f"{path}: {count} lines (maximum {args.max_lines})")
        return 1
    checked = len(iter_python_files(roots))
    print(f"Checked {checked} Python files; maximum {args.max_lines} lines.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
