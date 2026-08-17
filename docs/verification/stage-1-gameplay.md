# Stage 1 Gameplay Verification

**Date:** 2026-08-17
**Branch:** `feat/stage-1-gameplay`
**AI interface:** Codex (Claude CLI remains preferred where available)
**Stage gate:** **FAIL pending commit, Pull Request, review, and merge**

## Specification and Decision Review

| Decision | Specification evidence | Classification |
|---|---|---|
| Off-board rejection | Chapter 3.4 defines legal movement but no response | PDF silent; ADR-001 project decision |
| Equal counters | Annex F table 15 lists two separate minimum-35 values | Relationship silent; ADR-001 project decision |
| Common Capture Claim | Chapters 3.4-3.5 describe Capture Claim; Appendix E 46-47 mandate special captures | Procedure ambiguous; ADR-001 project decision |
| Cop-own-cell barrier | Chapter 3.4 explicitly permits current or adjacent placement | Mandatory; ADR-001 supplies occupancy semantics |
| STAY versus trapped | Chapter 3.4 permits STAY and mandates capture when adjacent destinations are unavailable | Internally contradictory; ADR-001 resolves tension |

No approved decision now contradicts an unambiguous higher-authority rule.
Annex F remains authoritative for values and classifications. Chapter 10's
local single-process milestone remains a recommendation rather than a new rule.

## Architecture and Scope

| Responsibility | Implementation | Focused tests |
|---|---|---|
| Actions/results | `actions.py`, `action_results.py` | gameplay tests |
| Movement | `movement.py` | `test_gameplay_movement.py` |
| Barriers | `barriers.py`, `capture_transitions.py` | barrier and own-cell tests |
| Capture evidence | `capture.py` | barrier/trapped capture tests |
| Orchestration | `rules.py`, `transitions.py` | all gameplay tests |
| Outcomes/scoring | `state_types.py`, `scoring.py` | outcome/capture tests |
| Repeatability | `tests/support/replay_support.py` | repeatability and probe tests |

Production `base_logic/replay.py` was removed because replay orchestration is a
later-stage non-goal. Deterministic replay support now exists only under tests.
No network, MCP, LLM, strategy, cryptography, remote comparison, GUI, league,
wall-clock, or random input is used.

## Clarified Behavior Evidence

- Every off-board boundary direction returns `OUT_OF_BOUNDS` with original
  object identity.
- Configuration rejects unequal `max_moves` and `survival_threshold` using
  `RELATIONSHIP_MISMATCH`; default and equally increased values pass.
- All three capture causes require a typed local cop Capture Claim and record
  the correct cause. Cryptographic proof remains deferred.
- Own-cell placement adds one permanent barrier, increments quota once, retains
  cop occupancy, permits STAY and legal exit, and blocks later re-entry by both
  roles. Duplicate placement is immutable rejection. Existing overlap takes
  claim priority and does not consume a barrier.
- Trapping uses in-board, non-barrier adjacent orthogonal destinations. STAY is
  not a destination. A cop-occupied adjacent non-barrier cell remains available
  under Chapter 3.4's barrier/edge definition.
- Capture has priority over survival when a valid barrier action both captures
  and reaches the step threshold.

Every capture cause scores `(cop=20, thief=5)` and terminal states reject later
actions without mutation. Fresh-process output includes movement, own-cell,
barrier-on-thief, and trapped-capture scenarios using ordered state summaries.

## Acceptance Traceability

| Criteria | Evidence |
|---|---|
| AC1-AC3 | orthogonal/STAY values; diagonal, barrier, and off-board rejection |
| AC4-AC6 | adjacent and own-cell barriers, permanence, quota and duplicates |
| AC7-AC9 | common claim tests for overlap, barrier, and trapped causes |
| AC10 | equal-threshold accepted-step survival tests |
| AC11 | exact score-pair tests for every outcome and capture cause |
| AC12 | complete in-process and fresh-process deterministic comparisons |
| AC13 | equal-counter configuration relationship tests |
| AC14-AC15 | local validated config construction; remote behavior excluded |

## Failures and Deliberate Corrections

1. The original Q3 fixture used a nonadjacent thief target. It was corrected so
   adjacency is validated before the special-capture procedure.
2. Initial Ruff run found six import-order and two unused-import issues. Each
   was corrected manually; no automatic fixes were used.
3. The first clarified-rule suite had 189 functional passes but failed the line
   gate because one capture test file had 164 lines. It was split by capture
   cause and responsibility.
4. The first fresh-process special-capture run exposed a serializer that could
   not encode barrier coordinates. It was replaced with an explicit ordered
   complete-state summary.
5. Adversarial review found overlap/trap priority gaps and malformed explicit
   movement targets. Priority checks, simultaneous claimed trap placement, and
   exact runtime target validation were added with regression tests.

## Tooling

Ruff `0.16.3` is the approved Stage 1 linter. Configuration targets Python
3.12 and selects `E4`, `E7`, `E9`, `F`, `I`, `B`, and `UP`.

| Command | Exit | Result |
|---|---:|---|
| `uv lock` | 0 | resolved 8 packages |
| `uv sync --frozen` | 0 | synchronized lock; removed temporary `pypdf` inspection tool |
| package import command | 0 | package and `base_logic` imported |
| `uv run ruff --version` | 0 | `ruff 0.16.3` |
| `uv run ruff check .` | 0 | all checks passed |
| `uv run pytest -q` | 0 | 199 passed in 2.39s |
| Python line checker | 0 | 44 files passed |
| dependency-isolation tests | 0 | 10 passed in 0.11s |
| `git diff --check` | 0 | no whitespace errors |
| focused credential scan | 1 | no matching credential patterns |
| forbidden-dependency scan | 1 | no forbidden imports |
| staged diff audit | 0 | 38 reviewed files; cached whitespace, scope, and credential checks passed |

For both `rg` scans, exit 1 is the expected no-match result. The working tree
contains only the approved Stage 1 documentation, deterministic logic, tests,
Ruff metadata, and verification evidence.

## Deferred Integration

Nonce, Commit-Reveal, hashes, signatures, log audit, peer verification, remote
configuration comparison/refusal, networking, MCP, LLM behavior, strategy,
cloud exposure, GUI, league orchestration, and presentation replay remain out
of Stage 1. The binary gate cannot become PASS until commit, PR, review, and
merge requirements are satisfied; Stage 2 must not begin.
