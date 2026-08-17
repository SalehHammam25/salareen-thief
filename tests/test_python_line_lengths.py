"""Tests for the standalone Python line-count quality gate."""

import subprocess
import sys
from pathlib import Path

CHECKER = Path("scripts/check_python_line_lengths.py")
MAX_LINES = 150


def run_checker(*roots: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), *(str(root) for root in roots)],
        check=False,
        capture_output=True,
        text=True,
    )


def test_repository_python_files_are_within_limit() -> None:
    result = run_checker(Path("src"), Path("tests"), Path("scripts"))
    assert result.returncode == 0
    assert "Checked" in result.stdout


def test_temporary_over_limit_python_file_fails(tmp_path: Path) -> None:
    oversized = tmp_path / "oversized.py"
    oversized.write_text("pass\n" * (MAX_LINES + 1), encoding="utf-8")
    result = run_checker(tmp_path)
    assert result.returncode == 1
    assert f"{MAX_LINES + 1} lines" in result.stdout


def test_non_python_files_are_ignored(tmp_path: Path) -> None:
    (tmp_path / "notes.txt").write_text("line\n" * 200, encoding="utf-8")
    result = run_checker(tmp_path)
    assert result.returncode == 0
    assert "Checked 0 Python files" in result.stdout
