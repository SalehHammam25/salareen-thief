# ADR-005: Stage 4 Unblocked Boundaries

**Status:** Superseded in part by ADR-006

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

## Former blockers

LS-BQ-01 through LS-BQ-04 prevent emission, decay, overlap, and board-edge
arithmetic. LS-BQ-06 prevents construction and updating of a Bayesian belief
map. LS-BQ-05 prevents claiming a comprehensive number-smuggling grammar.
ADR-006 records Areen's later approval of all six decisions. Until that ADR was
implemented, these tasks correctly remained unchecked and no placeholder
behavior represented them as resolved.

## Consequences

The original unblocked configuration, contracts, provider boundary, accounting,
and fallback behavior remain valid. ADR-006 and its implementation complete the
formerly deferred scent, belief, and numeric-language responsibilities.
