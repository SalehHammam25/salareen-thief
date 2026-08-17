# PRD 04 - Language and Scent
**Status:** Ready for review
**Repository:** salareen-thief
**Implementation:** Not started
**Specification:** 3.0.0

## Purpose
Replace direct coordinates with free-language hints, add dynamic opponent scent and belief updates, and retain deterministic Python legality (Chapters 4, 6.4-6.5, 10.3.4).

## Authority and Classification
- **Mandatory:** free natural language; no direct numeric-coordinate protocol; each peer sees only opponent scent; movement stays algorithmic (E26-E27; Ch4, Ch6).
- **Fixed Annex F:** center 0.9, decay 0.10 per turn, scent window 5x5.
- **Negotiable:** map area, hint limit (default 15), series token budget (~200000).
- **Options/examples:** Bayesian belief, provider choice and template/Ollama/Claude modes.
- **Engineering decisions:** spatial falloff, overlap aggregation, update order, clipping, hint grammar and belief likelihood require approval.

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

## Blocked Questions
- **LS-BQ-01:** non-center spatial scent falloff is not fully defined.
- **LS-BQ-02:** overlapping historical emission aggregation is unspecified.
- **LS-BQ-03:** decay/emission/movement ordering is unspecified.
- **LS-BQ-04:** edge clipping versus other behavior is unspecified.
- **LS-BQ-05:** allowable natural-language numbers short of direct coordinates need agreement.
- **LS-BQ-06:** belief prior/reliability/likelihood are strategy decisions.
