# Stage 3 Blind Strategy Verification

**Branch:** `feat/stage-3-blind-strategy`

**Specification:** 3.0.0

**Technical verification:** PASS

**Final Stage 3 gate:** PASS

## Authority review

The official PDF was read for Chapter 6, Chapter 10.3.3-10.4, Appendix E rule
25, and Annex F Table 22. Chapter 6 explicitly treats pure heuristics, a team
algorithm, and optional reinforcement learning as equal alternatives. Appendix
E recommends that an LLM not choose spatial moves. Annex F documents private
`thief_class` reference syntax but does not fully define import validation or
fallback behavior. No mandatory equal-cost tie-break is specified.

ADR-004 records Areen's approval of the built-in breadth-first default,
`N, S, E, W` tie order, trusted private plugin syntax and constructor contract,
visible typed fallback, and N-squared board-size invariant. STR-BQ-01 through
STR-BQ-03 are resolved without representing those choices as PDF mandates.

## Architecture and scope

- `StrategySnapshot` is frozen and contains only board geometry, thief position,
  barriers, status, and an explicit known target. It excludes cop truth, scent,
  language, LLM, and transport data.
- `BlindShortestPath` is the import-verified default and performs bounded
  breadth-first search. It defaults to shared fixed `N, S, E, W` order while
  retaining dependency injection for focused tests.
- `selector.py` reads only trusted private TOML `module.path:ClassName` values.
  Load/validation/runtime failures invoke a visible deterministic built-in
  fallback without exposing exception messages or private values.
- `StrategyGateway` converts the local state into a blind snapshot and validates
  every proposal through `BaseLogicRules` before returning a new state.
- Invalid proposals, terminal states, unreachable targets, invalid tie choices,
  and policy exceptions return typed failures without mutating the input state.
- Base Logic does not import strategy. Strategy does not import MCP or Stage 4.
- Q-learning and all RL dependencies remain absent.

## Acceptance mapping

- AC03-01: gateway and malicious-policy tests prove Base Logic validation.
- AC03-02: direct, multi-turn, every-quadrant tie, repeated, and fresh-process
  default shortest-route tests pass.
- AC03-03: barrier, edge, off-board, and unreachable tests.
- AC03-04: repeated snapshot and fresh-process tests.
- AC03-05: valid, malformed, missing, incompatible, constructor, runtime, result,
  and illegal-action plugin paths are covered with typed visible fallback.
- AC03-06: frozen snapshot, wrong-role, diagonal, and exception tests.
- AC03-07: static dependency tests, Ruff, pytest, and line checks.

## Failures and corrections

The first focused run passed 18 tests. Ruff reported one import-order issue and
one function-call default; both were corrected with no behavior change. A
focused board-edge test and a fresh-gateway coverage review were then added.
The finalization review corrected two additional Ruff findings, added explicit
session-independent default import verification, prevented malformed references
from being reflected in fallback state, and made Base Logic rejection trigger
validated fallback rather than merely returning a plugin failure.

## Review disclosure

Independent human reviewer: None

Owner approval: Areen

Review method: Codex-assisted adversarial review and automated verification

## Final commands and results

- `uv lock` - exit 0; 88 packages resolved.
- `uv sync --frozen` - exit 0; 86 packages checked.
- Package-boundary import command - exit 0.
- `uv run ruff check .` - exit 0; all checks passed.
- `uv run pytest -q` - exit 0; 296 passed with one third-party Authlib warning.
- Focused Stage 3 suite - exit 0; 51 passed.
- Focused dependency-isolation suite - exit 0; 12 passed.
- Line checker - exit 0; 76 Python files, all at or below 150 lines.
- `git diff --check` - exit 0.
- Credential scan - no matches (expected exit 1).
- Strategy forbidden-dependency scan - no matches (expected exit 1).
- Base Logic strategy-import scan - no matches (expected exit 1).
- Ignored generated artifacts were limited to `.venv`, Ruff/Python caches, and
  test caches; none is eligible for staging.

The largest Stage 3 file is `tests/test_strategy_paths.py` at 142 lines. The
largest production strategy files are `gateway.py` and `selector.py` at 85
lines each.

The adversarial review found no remaining objective defect within the unblocked
scope. It confirmed input immutability, absence of opponent/Stage 4 data,
bounded search, Base Logic validation, typed exception handling, and stable
fresh-process output, stable fallback visibility, private-only selection, and
N-squared stress invariants.

The finalization cached audit passed whitespace validation and contained exactly
14 reviewed ADR/PLAN/PRD/TODO/evidence, strategy, and test files. No private
configuration, cache, environment, credential, generated artifact, unrelated
file, or Stage 4 implementation was staged.

## Delivery evidence

- Implementation commit: `e01f246`.
- Push to `origin/feat/stage-3-blind-strategy`: successful.
- Pull Request: #11, merged into `main` as `f66021d`.
- Synchronization: local `main` fast-forwarded to `f66021d`; implementation
  commits `1dd607f` and `e01f246` are ancestors of `origin/main`.
- Closeout worktree: clean before creation of the Stage 4 branch.
- Final Stage 3 gate: PASS.
