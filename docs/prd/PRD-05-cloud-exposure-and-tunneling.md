# PRD 05 - Cloud Exposure and Tunneling
**Status:** Safe local subset implemented; external acceptance blocked
**Repository:** salareen-thief
**Implementation:** Local lifecycle complete; real tunnel proof pending
**Specification:** 3.0.0

## Purpose
Expose each working FastMCP peer through a public tunnel and complete a match between remote machines (Ch2.4; Ch10.3.5).

## Authority and Classification
- **Mandatory:** public tunnel exposure for league play, independent environments and symmetric access (E10; Ch2.4).
- **Options/examples:** ngrok and Localtonet; no provider is uniquely required.
- **Annex F:** response 30 seconds and watchdog 60 seconds are negotiable.
- **Engineering/external:** provider/account, URL lifecycle, TLS/firewall and operator runbook need approval and human authorization.

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

## Blocked Questions
- **CLD-BQ-01:** provider/account/plan is not mandated.
- **CLD-BQ-02:** URL discovery/exchange is unspecified.
- **CLD-BQ-03:** reconnect/resume versus technical loss is unspecified.
- **CLD-BQ-04:** attribution of provider outage is unresolved.
- **CLD-BQ-05:** account, firewall and token provisioning are external actions.
