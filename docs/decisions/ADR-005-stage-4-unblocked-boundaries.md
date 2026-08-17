# ADR-005: Stage 4 Unblocked Boundaries

**Status:** Accepted for the unblocked Stage 4 subset

**Authority:** Specification 3.0.0 Chapters 4, 6.4-6.5 and 10.3.4,
Appendix E 25-27, Annex F Tables 14, 16, 18 and 21

## Decision

- Shared JSON supplies the fixed scent values (0.9, 0.10 and 5x5), negotiated
  map area, hint word limit and series token budget. Stage 4 validates only
  these owned values and ignores unrelated later-stage sections.
- `OpponentScent` is an immutable peer-facing observation. No own-scent or
  objective opponent-position field exists in that contract.
- Stage 4 accepts free-language text and rejects unmistakable direct numeric
  coordinate forms. Other uses of numbers remain governed by LS-BQ-05 and are
  not silently prohibited.
- Provider mode, cadence and timeout come only from private local TOML. Missing
  private configuration selects the zero-token deterministic template mode.
- Provider replies contain text and actual token counts only. They contain no
  action or state field and cannot call Base Logic or strategy transitions.
- Provider failure, timeout, invalid output, or budget exhaustion produces a
  visible typed reason and deterministic template fallback. Exceptions and
  private values are not exposed.

Annex F Table 21 documents `template`, `ollama`, `claude_api`, and
`claude_cli`. This implementation validates those private mode names but does
not require external credentials or contact those services in tests.

## Retained blockers

LS-BQ-01 through LS-BQ-04 prevent emission, decay, overlap, and board-edge
arithmetic. LS-BQ-06 prevents construction and updating of a Bayesian belief
map. LS-BQ-05 prevents claiming a comprehensive number-smuggling grammar.
Those tasks remain unchecked and no placeholder behavior represents them as
resolved.

## Consequences

The unblocked configuration, contracts, provider boundary, accounting, and
fallback behavior can be reviewed now. The complete Stage 4 acceptance gate
cannot pass until the six blockers are resolved and the missing scent/belief
behavior is implemented and verified.
