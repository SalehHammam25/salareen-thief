# ADR-007: Stage 5 Safe Local Boundary

**Status:** Accepted; two-machine acceptance pending

**Authority:** Specification 3.0.0 Chapters 2.4, 8.4 and 10.3.5,
Appendix E 1-2/10, Annex F Table 19

## Decision

The repository implements a provider-neutral `TunnelProvider` lifecycle and an
ngrok v3 production adapter. Areen selected the account-assigned stable ngrok
development domain. Its bare domain comes only from ignored private
configuration or `NGROK_DOMAIN`; the authentication token remains solely in
ngrok's user-level configuration and is never passed to a subprocess.

The implementation provides public HTTPS validation, diagnostic redaction,
readiness/health/shutdown control, bounded retry/backoff, watchdog evaluation,
and typed DNS/TLS/disconnect/timeout/process failures. Tests use deterministic
fakes. An authorized temporary public check used only the test MCP endpoint and
redacted the real domain.

Endpoint exchange is manual through private configuration using
`SALAREEN_OPPONENT_URL`. Stage 6 will authenticate and sign configuration and
endpoint exchange. No discovery service, central server, or shared runtime
state is introduced.

Infrastructure failures remain typed and visible but do not select a Base Logic
technical-loss outcome. On disconnect, gameplay pauses and bounded reconnection
reuses the same domain. Resume requires exact game ID, session ID, protocol
version, turn index, and phase equality; mismatch aborts without inventing a
winner. Verified local server/ngrok failure beyond the watchdog is local
technical loss; verified remote application failure while the local path is
healthy is remote technical loss; provider, Internet, DNS, TLS, or ambiguous
failure has unknown attribution pending Stage 6 audit. Reachability is not
authentication; Stage 6 owns trust and cryptography.

## Resolved questions and retained external work

- CLD-BQ-01: resolved by Areen selecting ngrok and the stable-domain contract.
- CLD-BQ-02: resolved by manual private configuration for Stage 5.
- CLD-BQ-03: resolved by the exact identity resume contract above.
- CLD-BQ-04: resolved by the conservative attribution contract above.
- CLD-BQ-05 remains: a compatible cop endpoint and two independent machines are
  required for symmetric calls and a complete remote match.

The authorized single-endpoint public test opened and closed temporary ngrok
processes. The stable domain is redacted from evidence. No credential, private
domain, ngrok configuration content, or token was read or written to Git.
