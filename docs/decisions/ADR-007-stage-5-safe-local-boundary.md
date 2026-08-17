# ADR-007: Stage 5 Safe Local Boundary

**Status:** Accepted for local implementation; external acceptance pending

**Authority:** Specification 3.0.0 Chapters 2.4, 8.4 and 10.3.5,
Appendix E 1-2/10, Annex F Table 19

## Decision

The repository implements a provider-neutral `TunnelProvider` lifecycle,
environment-only credential and opponent-endpoint injection, public HTTPS
validation, diagnostic redaction, readiness/health/shutdown control, bounded
retry/backoff, watchdog evaluation, and typed DNS/TLS/disconnect/timeout/process
failures. Tests use deterministic fakes and never open a public tunnel.

The current safe exchange boundary is operator injection through
`SALAREEN_OPPONENT_URL`. This is not represented as the final cross-team URL
exchange agreement. No discovery service, central server, or shared runtime
state is introduced.

Infrastructure failures remain typed and visible but do not select a Base Logic
technical-loss outcome. Reconnect/resume and provider-outage attribution remain
blocked. Reachability is explicitly not authentication; Stage 6 owns trust and
cryptography.

## Retained blockers and external work

- CLD-BQ-01: Areen and the cop team must select a provider/account/plan.
- CLD-BQ-02: both teams must approve the final out-of-band URL exchange method.
- CLD-BQ-03: both teams must approve reconnect/resume versus technical loss.
- CLD-BQ-04: outage attribution remains unknown unless independently provable.
- CLD-BQ-05: a human operator must provision the client, token, firewall, and
  two independent machines and explicitly authorize a real public test.

No provider was selected or invoked, no account was created, no public tunnel
was opened, and no credentials or private URLs were written to the repository.
