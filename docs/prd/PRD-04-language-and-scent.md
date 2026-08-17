# PRD 04 - Language and Scent
**Status:** Approved decisions implemented; PR review pending
**Repository:** salareen-thief
**Implementation:** Complete before Pull Request
**Specification:** 3.0.0

## Purpose
Replace direct coordinates with free-language hints, add dynamic opponent scent and belief updates, and retain deterministic Python legality (Chapters 4, 6.4-6.5, 10.3.4).

## Authority and Classification
- **Mandatory:** free natural language; no direct numeric-coordinate protocol; each peer sees only opponent scent; movement stays algorithmic (E26-E27; Ch4, Ch6).
- **Fixed Annex F:** center 0.9, decay 0.10 per turn, scent window 5x5.
- **Negotiable:** map area, hint limit (default 15), series token budget (~200000).
- **Options/examples:** Bayesian belief, provider choice and template/Ollama/Claude modes.
- **Owner-approved engineering decisions:** ADR-006 defines spatial falloff, overlap aggregation, update order, clipping, numeric-language policy and belief likelihoods.

## Scope
Opponent scent emission/decay; thief belief map; free-language hint transport and coordinate rejection; bounded generation/parsing; private provider abstraction; every-N-step calls; token accounting; deterministic fallback.

## Non-Goals
LLM spatial legality, public tunnels, crypto commitments, Gmail, GUI and league execution.

## Mandatory Requirements
1. Movement/STAY emits scent and each peer observes only the opponent map (Ch4.2).
2. Apply Annex F fixed scent values (F16).
3. Maintain local belief, never objective opponent position (Ch4.4; Ch6.4).
4. Communicate in free language and reject direct numeric coordinates (E26-E27).
5. Enforce agreed map area and hint word limit (F14).
6. Keep legality/final move validation in Python (Ch6.5; E25).
7. Require explicit mutual agreement for any LLM move recommendation.
8. Count actual LLM tokens and preserve series-budget evidence (E54).
9. Keep model/provider credentials private and provide deterministic fallback.
10. Produce the complete concrete emission/decay model for both peers to exchange before a series; Stage 6 performs its cryptographic lock (Ch4.5).

## Acceptance Criteria
- AC04-01: scent fixtures emit/decay exactly at fixed values.
- AC04-02: own scent/objective opponent position is never exposed.
- AC04-03: scent/belief updates repeat identically.
- AC04-04: direct coordinate messages and over-limit hints reject.
- AC04-05: LLM output cannot mutate state/bypass legality.
- AC04-06: provider failure falls back without hanging.
- AC04-07: token budgets and adversarial hints are tested.
- AC04-08: all dependency and quality gates pass.

## Resolved Engineering Questions
- **LS-BQ-01:** resolved by exact-decimal Chebyshev rings in ADR-006.
- **LS-BQ-02:** resolved by order-independent cell-wise maximum aggregation.
- **LS-BQ-03:** resolved as transition, old-field decay, new emission, maximum, clipping, publication.
- **LS-BQ-04:** resolved by clipping without wrap, reflection or renormalization.
- **LS-BQ-05:** resolved by the deterministic prohibited-number policy in ADR-006.
- **LS-BQ-06:** resolved by the exact normalized prior and evidence model in ADR-006.
