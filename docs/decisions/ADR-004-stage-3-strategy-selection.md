# ADR-004: Stage 3 Strategy Selection and Fallback

**Status:** Owner approved

**Owner:** Areen

**Scope:** Stage 3 Blind Strategy

## Decisions

The default thief policy is
`salareen_thief.strategy.blind:BlindShortestPath`. The path was imported and
instantiated during verification. Its no-argument constructor uses deterministic
breadth-first shortest-path search.

Equal shortest paths use the fixed shared movement order `N, S, E, W, STAY`
with `STAY` excluded. The first legal shortest move in `N, S, E, W` order wins.
STAY is proposed only when the thief already occupies the known target.

Optional trusted local plugins use `module.path:ClassName` in private TOML under
`[strategy].thief_class`. Shared JSON, MCP input, and remote peers cannot select
a strategy. The named class must import, instantiate with no arguments, expose a
callable `propose(snapshot)` method, and return `ProposedAction` or
`DecisionFailure`. The only input is the frozen restricted `StrategySnapshot`.

Load, import, class, constructor, interface, runtime, result, and Base Logic
validation failures use stable typed reasons. A failure invokes the built-in
policy, retains a visible local `fallback_reason`, never includes exception
messages or configuration values, and validates the fallback through
`BaseLogicRules`. Fallback is never silent.

## Board-size policy

No maximum board size is invented. Breadth-first search records at most one
distance per cell, so visited cells are bounded by N squared. Verification uses
representative large boards and node-count/result invariants, not wall-clock
limits. A valid negotiated board is not rejected due to a local size cap.

## Non-goals

This decision adds no scent, language, LLM, networking, cryptography, shared
runtime state, RL dependency, or Stage 4 behavior.
