# ADR-006: Stage 4 Scent, Language, and Belief Decisions

**Status:** Owner approved

**Owner:** Areen

**Authority:** Specification 3.0.0 Chapters 4, 6.4-6.5 and 10.3.4,
Appendix E 25-27, Annex F Tables 14, 16, 18 and 21

## Decisions

1. The fixed 5x5 emission uses exact decimal Chebyshev rings: center `0.9`,
   first ring `0.6`, second ring `0.3`.
2. Overlaps use cell-wise maximum, making aggregation bounded,
   order-independent, and never additive.
3. An accepted movement first updates Base Logic state, then decays the existing
   field by the official `0.10` factor, emits from the updated position, combines
   by maximum, clips to the board, and publishes. New emission is not decayed.
   A rejected or blocked action preserves the same field object.
4. Board-edge emission is clipped without wrapping, reflection,
   renormalization, strength transfer, or modification of in-board values.
5. Hints reject all Unicode decimal digits, numeric tokens, coordinate-shaped
   tuples/lists, row/column numeric values, chess-style coordinates, and English
   number words in coordinate contexts. Qualitative language remains allowed;
   unsupported text is never converted into an exact coordinate. Provider
   prompts expressly prohibit coordinates and redact prohibited input context.
6. Belief is an immutable exact-decimal normalized distribution over publicly
   possible cells. Scent uses monotonic `1 + strength` weights. Supported
   qualitative regions use private reliability in `[0.5, 1.0]`, default `0.75`;
   matches receive `r` and nonmatches `1-r`. Unknown language is neutral. Scent
   precedes language. Invalid or zero-weight evidence preserves the previous
   valid belief with a typed visible fallback.

## Specification interpretation

The PDF fixes center intensity, decay, field size, the temporal decay factor,
free language, opponent-only scent, and Python spatial authority. It does not
fully define non-center values, repeated-emission aggregation, edge handling,
the accepted language grammar, or Bayesian likelihoods. Figure 4 is treated as
an explanatory example rather than an Annex F fixed matrix.

The PDF equation is applied exactly to decay the pre-turn field. The approved
maximum rule then combines that decayed history with the new emission. This
resolves the document's tension between additive notation and its stated
bounded `[0, 0.9]` scent domain without altering `rho = 0.10`.

## Boundaries

Base Logic remains unaware of scent and belief. The Stage 4 turn adapter calls
Base Logic first and cannot change rejection behavior. Belief receives no
objective opponent position. Language/provider results remain text evidence and
cannot apply actions or mutate Base Logic. Cryptographic locking remains Stage
6, and no real credentials are required by tests.
