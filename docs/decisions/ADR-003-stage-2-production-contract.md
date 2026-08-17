# ADR-003: Stage 2 Production Contract and Idempotency

**Status:** Owner approved

**Owner:** Areen
**Scope:** Stage 2 Basic MCP Infrastructure

## Decision

Areen approves the committed `1.0-provisional` geometry contract as the
thief repository's production Stage 2 contract. The historical version string
is retained so compatibility is not broken merely to rename it. The canonical
fixture is `tests/fixtures/mcp-geometry-v1-provisional.json`.

The symmetric tool names are `receive_geometry` and `relay_geometry`. Each peer
owns its local server and client; neither peer owns the other's runtime state.
Acknowledgements use `accepted: true` with the validated message. Rejections
use `accepted: false`, a stable code, and deterministic detail. Transport
failures remain typed local results and do not imply remote blame.

Cross-repository compatibility requires the same protocol version, tool names,
schemas, result vocabulary, and committed fixture. This decision does not
modify or claim approval inside `salareen-cop`.

## Duplicate policy

- Identity is scoped by the peer process's explicit game/session ID and the
  request correlation ID.
- An identical repeated validated request returns the same result without a
  second state mutation.
- Reusing a correlation ID with different validated content returns
  `DUPLICATE_MISMATCH` without mutation.
- Each orchestrator keeps a deterministic FIFO-bounded local history. The
  Stage 2 default bound is 100 accepted requests.
- History is process-local transport state, not shared game state.
- Evicted identifiers are no longer known locally; later replay protection and
  cryptographic identity remain outside Stage 2.

## Retained blocker

MCP-BQ-03 remains unresolved: Stage 2 represents local timeout, exhaustion,
watchdog, and transport failures but does not attribute blame or declare a
remote technical loss.
