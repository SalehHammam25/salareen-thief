# PRD 03 - Blind Strategy
**Status:** Implementation verified; PR/merge gate pending
**Repository:** salareen-thief
**Implementation:** Complete; delivery gate pending
**Specification:** 3.0.0

## Purpose
Add a thief decision module that autonomously selects a shortest legal route to a known target without scent, language or deception (Ch10.3.3-10.4).

## Authority and Classification
- **Mandatory:** strategy is separate from legality; Base Logic validates every output; movement is algorithmic by default (Ch6.2, 6.5; E25 recommendation).
- **Equivalent options:** Manhattan/Bayesian heuristics, a team algorithm or optional Q-learning (Ch6.3-6.4; Annex F Table 22).
- **Examples:** Bellman, epsilon-greedy and sample coordinates are nonbinding.
- **Engineering decisions:** default thief policy, tie-breaking, route search and plugin contract need approval.

## Scope
Stable strategy interface; deterministic thief blind policy using known geometry; Base Logic action filtering; shortest-route milestone; private strategy selection; explicit failure results; repeatability/performance tests.

## Non-Goals
Scent, hints, belief from hidden observations, LLM calls, tunnels, cryptography, GUI, Gmail and league optimization. Q-learning is optional and separately reviewable.

## Mandatory Requirements
1. Separate strategy from deterministic legality (Ch6.2).
2. Never bypass Base Logic validation (Ch6.5).
3. Keep movement selection algorithmic unless both peers explicitly agree otherwise (Ch6.5).
4. Keep strategy selection private per Appendix B and Annex F Table 22.
5. Complete the autonomous shortest-route milestone for known geometry (Ch10.4).
6. Preserve deterministic tie behavior and keep private policy state local.
7. Return typed failure rather than inventing a legal action.

## Acceptance Criteria
- AC03-01: every chosen action passes Base Logic.
- AC03-02: reachable known targets use a shortest legal route without intervention.
- AC03-03: barriers/edges are respected and unreachable inputs fail explicitly.
- AC03-04: equal inputs repeat identically across processes.
- AC03-05: invalid plugins fail before play.
- AC03-06: malicious strategies cannot mutate state/bypass legality.
- AC03-07: Stage 4 dependencies are absent and all quality gates pass.

## Owner-approved Engineering Decisions

ADR-004 resolves STR-BQ-01 through STR-BQ-03:

- the built-in `BlindShortestPath` breadth-first policy is the default;
- equal shortest paths use shared fixed order `N, S, E, W`, excluding STAY;
- trusted private TOML uses canonical `module.path:ClassName` references;
- plugins use a no-argument constructor and restricted snapshot/proposal seam;
- every plugin failure produces a visible typed reason and deterministic
  Base-Logic-validated fallback;
- search is bounded by N squared visited cells without inventing a board maximum.

The final Stage 3 gate remains pending only for Pull Request, merge, and
synchronization evidence.
