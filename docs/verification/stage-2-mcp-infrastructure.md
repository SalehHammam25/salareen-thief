# Stage 2 MCP Infrastructure Verification

**Branch:** `feat/stage-2-mcp-infrastructure`

**Specification:** 3.0.0

**Technical verification:** PASS

**Stage gate:** FAIL pending Pull Request, merge, and synchronization

## Authority and governance

The specification does not mandate independent human review. ADR-002 records
Areen's owner-approved exception to the project-added review rule. Pull Requests
and automated verification remain mandatory.

Independent human reviewer: None

Owner approval: Areen

Review method: Codex-assisted adversarial review and automated verification

FastMCP usage was checked against the official server and client documentation:

- `https://gofastmcp.com/servers/server`
- `https://gofastmcp.com/clients/client`

ADR-003 records Areen's approval of the current tool names, protocol version,
error vocabulary, fixture compatibility rule, and duplicate policy as the
thief's production Stage 2 contract. The historical `1.0-provisional` string
is retained to preserve compatibility. MCP-BQ-03 alone remains open.

Future contract changes must update the versioned fixture, thief contract tests,
and evidence in one focused PR. The cop repository must use the same fixture and
version for compatibility. Incompatible changes require a new version.

## Implemented boundary

- Each role runs as an independent process with a FastMCP HTTP server/client.
- `PeerOrchestrator` is the sole transport-state gateway and never owns or
  mutates Base Logic state.
- Geometry validation deterministically rejects malformed and unsupported data.
- Identical session-scoped duplicates return the cached result without mutation.
- Correlation/content mismatches reject as `DUPLICATE_MISMATCH` without mutation.
- FIFO duplicate history is local to one process and bounded to 100 by default.
- Shared JSON supplies agreed timeout/retry values; private TOML supplies local
  endpoint values and is ignored by Git.
- No strategy, LLM, tunneling, cryptography, GUI, replay, reporting, shared
  runtime state, or central server was added.

## Adversarial review and corrections

The first focused run passed 31 tests but Ruff found two import-order violations;
imports were corrected. Review also corrected non-string-key sorting, process
reaping, one-way-only integration coverage, outbound gateway validation, and an
unsupported duplicate decision. ADR-003 subsequently supplied owner authority
for a bounded session-scoped policy, which was implemented with retry, mismatch,
bounded-state, isolation, and repeatability tests.

Private `config/game.toml` exclusion is explicit. Retry backoff/max-retry values
come from shared JSON. The staged whitespace audit found and corrected Markdown
trailing spaces and extra EOF blank lines.

## Commands and results

Initial verified baseline before ADR-003:

- `uv --version` - exit 0; `uv 0.12.5`.
- `uv run python --version` - exit 0; Python `3.12.10`.
- Runtime metadata - exit 0; FastMCP `2.14.7`, MCP `1.29.0`.
- `uv lock` - exit 0; 88 packages resolved.
- `uv sync --frozen` - exit 0; 86 packages checked.
- `uv run ruff check .` - exit 0.
- `uv run pytest -q` - exit 0; 233 passed; one third-party warning.
- Line checker - exit 0; 59 Python files, all at or below 150 lines.
- `git diff --check` - exit 0.
- Credential and Base Logic dependency scans - no matches (expected exit 1).

Final ADR-003 verification:

- `uv lock` - exit 0; 88 packages resolved.
- `uv sync --frozen` - exit 0; 86 packages checked.
- Package import command - exit 0.
- `uv run ruff check .` - exit 0; all checks passed.
- `uv run pytest -q` - exit 0; 245 passed with one third-party Authlib warning.
- Separate-process integration test - exit 0; 1 passed.
- Base Logic dependency-isolation tests - exit 0; 10 passed.
- Line checker - exit 0; 60 Python files, all at or below 150 lines.
- `git diff --check` - exit 0.
- Credential scan - no matches (expected exit 1).
- Base Logic forbidden-dependency scan - no matches (expected exit 1).

Focused idempotency/FastMCP verification passed 20 tests before the final
fresh-gateway repeatability test was added. That test is included in the
245-test complete result.

## Pre-PR delivery evidence

- Initial Stage 2 implementation commit: `2d6ab3d`.
- Production contract/idempotency commit: `12aa611`.
- Both commits were pushed to `origin/feat/stage-2-mcp-infrastructure`.
- The working tree was clean and synchronized after the implementation push.
- No Pull Request, merge, or final PASS is claimed.

The localhost integration launches two separate peer processes on distinct
ports. Each process serves and calls; both are terminated and reaped afterward.

## Deferred items

- MCP-BQ-03: remote technical-loss attribution versus local infrastructure
  failure. Typed local failures do not assign blame.
- Pull Request, merge, synchronization, and final binary Stage 2 PASS are not
  claimed before those events occur.
