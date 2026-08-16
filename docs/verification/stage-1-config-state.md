# Stage 1 Configuration and State Verification

**Date:** 2026-08-17
**Branch:** `feat/stage-1-config-state`
**AI interface:** Codex

## Scope

This change combines the approved configuration and state-model batches. It
contains local JSON decoding, Base Logic validation, immutable configuration,
coordinates, board representation, roles, immutable state construction, and
representation invariants. It contains no game actions or transitions.

Completed TODO IDs:

- BLT-024 and BLT-025;
- BLT-031 through BLT-044;
- BLT-046 through BLT-057;
- BLT-117, BLT-118, and BLT-126 through BLT-131.

BLT-026 through BLT-029 and BLT-045 remain unchecked because their full
wording requires a future action/transition or rule-construction boundary.

## Architecture

- Frozen, slotted dataclasses represent validated configuration and state.
- Configuration results are explicitly accepted or rejected; rejection never
  contains a partial `BaseLogicConfig`.
- State construction is explicitly accepted or rejected and never mutates an
  input object.
- The loader reads one local UTF-8 JSON file and performs no remote operation.
- Stage 1 extracts only three Base Logic sections. Later-stage and unknown
  sections are ignored, not copied, and not claimed valid.
- The committed complete shared JSON uses Annex F values, including six league
  games, and contains no private TOML settings.
- Coordinate bounds use `S <= value <= S + N - 1`. Origin text remains opaque.

## Error Categories

Configuration errors are: `FILE_NOT_FOUND`, `FILE_READ_ERROR`,
`MALFORMED_JSON`, `DUPLICATE_KEY`, `MISSING_KEY`, `INCORRECT_TYPE`,
`BELOW_MINIMUM`, `FIXED_VALUE_DEVIATION`, and `OUT_OF_BOUNDS`.
Issues are emitted in deterministic schema and constraint order. Boolean values
are rejected wherever integers are required.

State errors cover incorrect runtime types, out-of-bounds positions and
barriers, duplicate barriers, negative barrier usage, quota excess, negative
valid steps, and status/outcome mismatch. State coordinates and counters reject
booleans rather than treating them as integers.

## Failures and Corrections

The first line-count run failed because `config_validation.py` had 159 lines.
Structural extraction was split into `config_extract.py`; the semantic
validator now has a separate responsibility and the full tree passes.

The first complete functional run passed 93 tests. A quality audit identified
missing focused coverage for root/section/string/move-set shapes and explicit
slotted immutability. Those tests were added before final verification.

The pre-commit audit found that state counters and coordinate components could
accept booleans through Python's integer subtype behavior. It also found that
invalid barrier objects could fail before producing a rejected result and that
status/outcome runtime types were not enforced. A separate state-validation
module and focused regression tests corrected these defects. The same audit
reverted BLT-027 to unchecked because its wording requires action results, and
this batch intentionally contains no action processing.

## Tool Versions

| Command | Exit | Result |
|---|---:|---|
| `uv --version` | 0 | `uv 0.12.5 (210d1f678 2026-08-14 x86_64-pc-windows-msvc)` |
| `python --version` | 0 | `Python 3.12.10` |

## Final Verification

| Command | Exit | Result |
|---|---:|---|
| `uv lock` | 0 | Resolved 7 packages |
| `uv sync --frozen` | 0 | Checked 7 packages |
| installed-package import command | 0 | `salareen_thief` and `base_logic` imported |
| `uv run pytest -q` | 0 | 135 tests passed |
| Python line checker | 0 | 25 files checked; no file above 150 lines |
| `git diff --check` | 0 | No whitespace errors |
| focused secret/credential `rg` scan | 1 | No matching credential patterns |

`git status -sb` showed only the authorized TODO modification and the new
configuration, Base Logic, test, and verification files. `git diff
--name-only` listed only the tracked TODO file because all other batch files
were new and untracked. Nothing was staged, committed, or pushed.

## Deferred Risks

- No allowed vocabulary or directional semantics is invented for alternative
  coordinate origins.
- Duplicate-key errors identify the duplicate name but not a full nested path.
- Identical cop/thief starting cells are not rejected because the approved PRD
  does not require distinct starts.
- No action processing exists, so rejected-action immutability and terminal
  transition enforcement are not claimed.
- No peer comparison, negotiation, signature, networking, MCP, LLM, scoring,
  movement, barrier placement, capture, or survival behavior is implemented.
