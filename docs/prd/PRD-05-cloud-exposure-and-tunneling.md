# PRD 05 - Cloud Exposure and Tunneling
**Status:** ngrok adapter verified; two-machine acceptance blocked
**Repository:** salareen-thief
**Implementation:** Local and single-endpoint public proof complete
**Specification:** 3.0.0

## Purpose
Expose each working FastMCP peer through a public tunnel and complete a match between remote machines (Ch2.4; Ch10.3.5).

## Authority and Classification
- **Mandatory:** public tunnel exposure for league play, independent environments and symmetric access (E10; Ch2.4).
- **Options/examples:** ngrok and Localtonet; no provider is uniquely required.
- **Annex F:** response 30 seconds and watchdog 60 seconds are negotiable.
- **Approved engineering:** ngrok stable development domain, manual private URL exchange, identity-safe bounded reconnect, and conservative failure attribution (ADR-007).
- **External:** a compatible cop endpoint and two machines remain required.

## Scope
Tunnel abstraction/runbook; private endpoint injection; health checks/redacted diagnostics; remote two-machine integration; latency, disconnect, retry, reconnect and shutdown behavior; removal of localhost assumptions.

## Non-Goals
Cryptographic trust, signatures, Commit-Reveal, Gmail, GUI, replay and league scoring. Reachability is not authentication.

## Mandatory Requirements
1. Expose each FastMCP server through a public tunnel (Ch2.4; E10).
2. Preserve symmetric server/client roles and total process separation.
3. Do not share memory/files/private config.
4. Apply mutually agreed Annex F timeouts.
5. Bound retries and surface explicit terminal infrastructure results.
6. Never log or commit tunnel credentials.
7. Prove a complete remote-machine match before Stage 6.

## Acceptance Criteria
- AC05-01: remote cop reaches thief and thief reaches cop through tunnels.
- AC05-02: a complete match runs across two machines.
- AC05-03: expired URLs, DNS/TLS failure, disconnect and latency never hang.
- AC05-04: retry exhaustion/watchdog behavior is observable.
- AC05-05: logs redact secrets and contracts match localhost schemas.
- AC05-06: all integration, credential and quality gates pass.

## Approved Decisions and Remaining Blocker
- **CLD-BQ-01 through CLD-BQ-04:** resolved by ADR-007 and Areen's ngrok contract.
- **CLD-BQ-05:** symmetric calls and a complete match require a compatible cop endpoint on another machine.

## Live runner and strict endpoint extension

ADR-008 and the shared live-match contract own independent runner composition, exact-identity pause/resume, acknowledged-action protection, terminal reconciliation and controlled shutdown. Remote endpoints must use HTTPS, exact configured host/permitted port and `/mcp`, with no userinfo, query, fragment, localhost or private address. Expected-role checking is protocol validation only. The current query-permitting endpoint behavior must be corrected during implementation; the runner, adapters and full-match tests remain unimplemented.
