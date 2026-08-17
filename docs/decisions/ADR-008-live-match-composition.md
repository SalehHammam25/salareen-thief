# ADR-008: Thief Live-Match Composition

**Status:** accepted; implementation pending

**Owner:** Areen
**Review:** Codex-assisted adversarial review and automated documentation verification; independent human review not required

## Decision

Adopt `docs/contracts/live-match-orchestration-v1.md` as the shared production design. The thief repository will own an independent thief runner that composes its local configuration, Base Logic, thief strategy, transport, scent/language/belief, recovery and structured log. There will be no central runner or shared runtime state.

The current strict six-field geometry contract remains unchanged. Additional orchestration messages are separately versioned. The thief accepts game messages only from its configured cop role; this is Stage 5 protocol validation, not authentication.

Remote opponent endpoints use HTTPS, the configured exact host/permitted port and exact `/mcp` path, with no userinfo, query, fragment, localhost or private address. This strict rule replaces the current query-permitting endpoint behavior; implementation remains unchecked.

Stage 5 contains no hashing, signatures, Nonces, Commit-Reveal or cryptographic Capture Claim proof. Those remain Stage 6 work.

## Consequences

- The production thief runner and all missing adapters/tests remain unchecked implementation work.
- Capture Claim disagreement in Stage 5 aborts safely with evidence; it is not cryptographically adjudicated.
- The PDF's incomplete wire choreography is resolved narrowly by owner-approved sequential thief-first turns consistent with existing Base Logic.
- Shared contract and future fixtures must remain byte-identical with the cop repository.

## Adversarial review

The decision rejects central-server behavior, shared state, hidden opponent truth, simultaneous-action ambiguity, double application, lost-acknowledgement divergence, combined barrier/movement actions, survival-before-capture races, Stage 4 ordering drift, invented technical-loss blame, premature cryptography, endpoint divergence and claims of authenticated security.
