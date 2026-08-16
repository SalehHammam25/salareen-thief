# Stage 1 Batch 1 Verification Evidence

**Date:** 2026-08-16
**Last verified:** 2026-08-17
**Branch:** `feat/stage-1-foundation`
**AI interface:** Codex
**Scope:** BLT-003 through BLT-023, BLT-030, and BLT-152 through BLT-154

## Engineering Decisions

- Python 3.12 is the approved interpreter line; the active interpreter is 3.12.10.
- The project uses `uv` 0.12.5 and commits `uv.lock`.
- Runtime dependencies are empty because Batch 1 contains no game behavior.
- `pytest` is the only development dependency and is used for foundation checks.
- The project uses a packaged `src` layout with import package `salareen_thief`.
- `uv_build>=0.12.5,<0.13` builds and installs the project into the uv environment.
- `salareen_thief.base_logic` is an intentionally behavior-free deterministic boundary.
- Pytest does not inject `src` or the repository root into `sys.path`.
- Tests import `salareen_thief` from the installed project.
- The standalone line checker is exercised through subprocess calls and `scripts`
  is not an importable package.
- The line checker scans `src`, `tests`, and `scripts`, with a 150-line maximum.
- Existing `.gitignore` rules already cover `.venv`, caches, environments, and secret-bearing local files, so it was not changed.

## Command Record

| Command | Exit | Result |
|---|---:|---|
| `uv --version` | 0 | `uv 0.12.5 (210d1f678 2026-08-14 x86_64-pc-windows-msvc)` |
| `python --version` | 0 | `Python 3.12.10` |
| `git status -sb` before edits | 0 | Clean on `feat/stage-1-foundation` |
| `uv lock` | 0 | Resolved 7 packages |
| `uv sync --frozen` | 0 | Checked 6 installed packages |
| `uv run pytest -q` | 1 | Initial collection failed because `scripts` was not importable |
| `uv run pytest -q` | 1 | Second collection failed because pytest's path contained only `src` |
| `uv run pytest -q` | 0 | 6 passed in 0.13s after correcting the test import boundary |
| `uv run python scripts/check_python_line_lengths.py` | 0 | Checked 6 Python files; maximum 150 lines |
| secret-pattern scan over intended source files | 1 | Expected no-match exit; no findings |
| `git status -sb --ignored` | 0 | `.venv` and generated caches are ignored |

The two failed collection attempts above belong to the superseded non-packaged
draft. The packaging correction removed pytest path injection, removed
`scripts/__init__.py`, and changed checker tests to invoke the script by
subprocess.

The over-limit test creates a temporary 151-line Python file through pytest's
`tmp_path` fixture. No intentionally oversized fixture is stored in the repository.

## Final Verification

| Command | Exit | Result |
|---|---:|---|
| `uv lock` | 0 | Resolved 7 packages in 370 ms |
| `uv sync --frozen` | 0 | Built and installed `salareen-thief==0.1.0` |
| `uv run python -c "import salareen_thief; import salareen_thief.base_logic"` | 0 | Both installed-package imports succeeded |
| `uv run pytest -q` | 0 | 6 passed in 0.75s |
| `uv run python scripts/check_python_line_lengths.py` | 0 | Checked 5 Python files; maximum 150 lines |
| `git diff --check` | 0 | No whitespace errors |
| `git status -sb` | 0 | Expected Batch 1 files only; nothing staged |
| `git diff --name-only` | 0 | Only the tracked TODO update; new files are listed by status |

## Scope Confirmation

No board, coordinate, configuration, movement, barrier, capture, survival,
scoring, networking, strategy, LLM, or cryptographic behavior was implemented.
Remote configuration comparison and signing remain later-stage dependencies.
