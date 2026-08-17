# Stage 2 MCP Infrastructure Verification

**Branch:** `feat/stage-2-mcp-infrastructure`

**Specification:** 3.0.0

**Technical verification:** PASS
**Stage gate:** FAIL pending cross-repository contract approval, Pull Request, merge, and synchronization

## Authority and governance

The specification does not mandate independent human review. ADR-002 records Areen's owner-approved exception to the project-added review rule. Pull Requests and automated verification remain mandatory.

Independent human reviewer: None

Owner approval: Areen
Review method: Codex-assisted adversarial review and automated verification

FastMCP usage was checked against the official FastMCP server and client documentation:

- `https://gofastmcp.com/servers/server`
- `https://gofastmcp.com/clients/client`

The implemented tool names, protocol version, error vocabulary, and duplicate handling are explicitly provisional. They are not represented as approved cop/thief contracts. MCP-BQ-01 through MCP-BQ-03 remain open.

Provisional contract changes must update the versioned fixture, thief contract
tests, and evidence in one focused PR; the cop repository must receive the same
fixture in a coordinated PR and explicitly approve production names/version
before either peer treats the contract as shared. Incompatible changes require
a new version rather than silently changing an existing fixture.

## Implemented boundary

- Each role runs as an independent Python process with its own FastMCP HTTP server and client.
- `PeerOrchestrator` is the sole transport-state gateway and never owns or mutates Base Logic state.
- Versioned geometry payloads reject unknown, missing, malformed, wrong-type, Boolean-as-integer, invalid-role, invalid-step, and unsupported-version input deterministically. Duplicate/idempotency behavior is intentionally not implemented pending MCP-BQ-02.
- Shared JSON supplies agreed timeout/retry values; private TOML supplies the local port and opponent URL. Private configuration is ignored by Git.
- Retries and watchdogs are bounded and cancellation is preserved.
- No strategy, LLM, tunneling, cryptography, GUI, replay, reporting, shared runtime state, or central server was added.

## Adversarial review and corrections

The first focused run passed 31 tests but Ruff found two import-order violations. Imports were corrected. Review then found and corrected three objective weaknesses:

1. Non-string mapping keys could reach sorting and raise a non-contract exception; the decoder now returns deterministic `INVALID_SHAPE`.
2. Integration cleanup could kill without reaping a stubborn process; cleanup now waits after both terminate and kill paths and asserts both processes exited.
3. The integration test originally proved only one relay direction; it now proves both peers serve and call independently.

The private `config/game.toml` exclusion was also made explicit, and retry backoff/max-retry values now come from shared JSON rather than private state.
The first staged whitespace check found Markdown trailing spaces and extra EOF
blank lines; those were removed, restaged, and the complete cached check passed.

## Commands and final results

The final evidence must be read with the command exit codes recorded below; implementation commands were not claimed as passed before execution.

- `uv --version` — exit 0; `uv 0.12.5`.
- `uv run python --version` — exit 0; Python `3.12.10`.
- `uv lock` — exit 0; 88 packages resolved.
- `uv sync --frozen` — exit 0; 86 packages checked.
- Runtime metadata check — exit 0; FastMCP `2.14.7`, MCP `1.29.0`.
- `uv run ruff check .` — exit 0; all checks passed.
- `uv run pytest -q` — exit 0; 233 passed; one third-party Authlib deprecation warning.
- `uv run python scripts/check_python_line_lengths.py` — exit 0; 59 Python files checked, all at or below 150 lines.
- `git diff --check` — exit 0.
- Base Logic dependency-isolation tests are included in the complete pytest result and passed.
- Focused credential/generated-file scan — exit 0; no credential material, private TOML, virtual environment, cache, or generated artifact is tracked or staged.

The localhost integration launches two separate `python -m salareen_thief.mcp_transport.peer` processes on distinct ports. The thief calls the cop and the cop calls the thief; both processes also serve tools, share no Python objects, and are terminated and reaped after the test.

## Deferred items

- MCP-BQ-01: production cross-repository tool names, version, schema, and vocabulary.
- MCP-BQ-02: approved duplicate/idempotency policy.
- MCP-BQ-03: remote technical-loss attribution versus local infrastructure failure.
- Cross-repository approval, commit/push evidence, Pull Request, merge, synchronization, and final binary Stage 2 PASS are not claimed in this pre-PR evidence.
