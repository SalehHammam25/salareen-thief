# PRD 02 - Basic MCP Infrastructure
**Status:** Ready for review
**Repository:** salareen-thief
**Implementation:** Not started
**Specification:** 3.0.0

## Purpose
Separate the peers into independent processes and prove that a geometric message sent through FastMCP over localhost is received and decoded correctly (Chapter 10.3.2).

## Authority and Classification
- **Mandatory:** symmetric FastMCP server/client peers, separate processes/configuration, no shared state, orchestrator gateway, legal state machine, bounded waits, local truth (Chapters 2, 8; Appendix E 1-9).
- **Recommended/example:** A2A/ACP, sample tool names/classes and sample FastMCP code.
- **Annex F:** response timeout 30 seconds and watchdog 60 seconds are negotiable; requests/minute 30, concurrency 2, backoff 5 seconds, retries 3 and queue 100 are minimums.
- **Engineering decisions:** versioned envelopes, exact tool/error names, correlation/idempotency and codec need cross-repository approval.

## Scope
Independent thief server/client runtime; localhost MCP tools; transport schemas; acknowledgement and error boundaries; orchestrator-only subsystem entry; legal phase transitions; deadline/retry/watchdog boundaries; process-isolation and repeatability tests.

## Thief and Shared Contract
The thief owns only local truth and never reads cop memory/files. Both repositories must share tool names, versions, schemas, acknowledgement/error semantics and contract fixtures. Messages remain unauthenticated until Stage 6.

## Non-Goals
Public tunnels, strategy, scent/language, cryptography, signed config comparison, Gmail, GUI, replay and league behavior.

## Mandatory Requirements
1. Run peers as wholly separate processes/configuration roots with no shared live state (Ch2.4.2; E1-E2).
2. Each peer is both FastMCP server and client and uses MCP for peer tool exchange (Ch2.3).
3. Route subsystem interaction through one orchestrator entry point (Ch8.3; E3).
4. Reject illegal state-machine transitions (Ch8.3; E4-E5).
5. Bound requests, retries and waits; never wait indefinitely (Ch8.4; E6).
6. Represent watchdog/crash recovery and controlled technical-loss escalation (Ch8.4; E7).
7. Expose only local truth (Ch7.2; E8-E9).
8. Preserve deterministic rules and no mutation on rejected messages.

## Acceptance Criteria
- AC02-01: two local processes exchange a versioned geometric message over localhost.
- AC02-02: each process demonstrably serves and calls an MCP tool.
- AC02-03: tests detect shared-memory/file shortcuts.
- AC02-04: malformed, unknown-version, duplicate, stale and out-of-phase messages reject without state mutation.
- AC02-05: only legal phase transitions pass.
- AC02-06: deadline/retry exhaustion produces one typed result.
- AC02-07: repeated/fresh-process fixtures decode identically.
- AC02-08: no later-stage dependencies leak in; all quality gates pass.

## Blocked Questions
- **MCP-BQ-01:** production tool names, schemas, protocol versions and error vocabulary are unspecified.
- **MCP-BQ-02:** exact idempotency/duplicate-message policy is unspecified.
- **MCP-BQ-03:** attribution of remote technical loss versus local infrastructure failure is unspecified.
