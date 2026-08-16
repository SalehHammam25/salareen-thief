# PRD 01 — Base Logic

**Status:** Approved for planning
**Repository:** salareen-thief
**Implementation:** Not started

## Purpose

This PRD defines the deterministic local game-physics foundation used by the thief peer: the discrete board, the coordinate system, legal movement, barriers, capture and survival conditions, and per-episode scoring.

The thief peer must calculate and validate the same board state, legal movement, barriers, capture conditions, survival conditions, and scores as the cop peer.

This PRD defines behavior only. It contains no networking and no intelligence (heuristic, LLM, or reinforcement-learning) content.

## Requirement Classification

- **Mandatory** rules are explicitly binding game or project requirements. Appendix E consolidates these rules.
- **Fixed** Annex F values cannot be changed.
- **Minimum** Annex F values may be increased only by mutual agreement. When there is no explicit agreement, the Annex F example value is the required default; it may not be reduced.
- **Negotiable** Annex F values may be changed by mutual agreement. When there is no explicit agreement, the Annex F example value is the required default.
- **Examples** illustrate a permitted configuration or behavior and are not independently binding.
- **Recommendations**, including the Chapter 10 development order and milestones, guide implementation but are not mandatory game rules.
- **Engineering decisions** in this PRD define Stage 1 scope without changing the official game rules.

## Mandatory Requirements

### Board and Coordinate System

- Exactly 2 agents participate (cop and thief).
- [גודל הלוח] — default 7×7 — Annex F status: **minimum**. A mutually agreed value may be higher, never lower.
- Cells are represented as `(row, col)`.
- [ראשית מערכת הצירים] (coordinate origin) — default: the top-left corner, i.e. the corner where cell (0,0) sits — status: **negotiable**.
- [אינדקס התחלת הצירים] (starting index) — default: 0 — status: **negotiable**.
- [עמדת פתיחה – גנב] and [עמדת פתיחה – שוטר] (starting positions) — default example: thief at center (3,3), cop at corner (0,0) — status: **negotiable**; the specific center/corner layout is stated as **example only**.
- Whatever coordinate-origin, starting-index, and starting-position values are agreed must be identical between both peers — a mismatch between what each side counts from or starts at breaks the shared physics.

### Shared Base-Logic Configuration

- Chapter 3.3 explicitly states that the starting positions are loaded from `config/game.json`.
- Annex B defines `config/game.json` as the shared game constitution. Values relevant to the opponent or relied upon by both peers belong in this shared JSON, not only in private `config/game.toml`.
- The complete distributed project requires both peers to use the same agreed shared configuration. Annex B and Appendix E require identical shared physics, and Appendix E rule 11 requires the configuration to be identical byte-for-byte between peers.
- When the same key is present in the shared JSON and private TOML, the shared JSON value takes precedence.
- Stage 1 loads and validates its local `config/game.json` values and the deterministic Base Logic uses those validated values. Because Stage 1 runs locally in one process, it does not compare configuration bytes with a remote peer.
- Byte-identical peer comparison, signed configuration exchange, and refusal of a remotely detected mismatch are mandatory later-stage integration requirements. They are not implemented or exercised by Stage 1.
- The precise module boundary and delivery order for the local Stage 1 loader are **engineering decisions for PLAN**, not unresolved game rules.

### Movement

- On its turn, the active agent performs exactly one action.
- The fixed [מערך התנועה] is moving one cell in one of the four orthogonal directions (N/S/E/W), or staying in place (`4 + stay`).
- Diagonal movement is prohibited.
- An illegal diagonal-move attempt is rejected deterministically.
- Blocked (barrier) cells cannot be crossed by either agent.

Off-grid movement behavior is not invented here — see Blocked Specification Questions.

### Barriers

- Only the cop may place barriers.
- Placing a barrier replaces movement for that turn (the cop cannot move and place a barrier in the same turn).
- Placement is allowed on the cop's current cell or on one orthogonally adjacent cell.
- [מכסת המחסומים] — default 14 — Annex F status: **minimum**. It functions as the maximum number of barriers the cop may place, but the configured quota itself may be increased by mutual agreement and may not be below 14.
- Barriers are permanent and impassable to both agents for the rest of the episode.
- Every barrier placement, and its exact location, must be declared truthfully.
- Hidden placement and lying about a barrier's location are prohibited.

### Capture and End Conditions

An episode ends as a **capture** when any of the following occurs:
- the cop's and thief's coordinates overlap, and the cop declares a Capture Claim;
- the cop places a barrier on the thief's current cell;
- the thief has no legal move because all adjacent cells are blocked by barriers and/or board edges.

The second and third capture paths are mandatory in Appendix E rules 46 and 47. The PDF does not state clearly whether they use the same Capture Claim and later truth-verification flow as coordinate-overlap capture; that protocol question remains blocked.

The trapped-thief rule also has an unresolved tension with the fixed permission to stay in place. The PDF describes a thief with no legal move because all adjacent cells are blocked or outside the board as captured, while [מערך התנועה] includes staying. This PRD records both statements and does not decide whether staying prevents trapped capture.

An episode ends as a **survival** when the thief survives [סף ההישרדות] valid steps without capture. Annex F gives [סף ההישרדות] a default/minimum value of **35**.

[תקרת הצעדים] is a separate mandatory parameter (a per-episode move ceiling). Annex F gives it a default/minimum value of **35**. Its precise relationship to [סף ההישרדות] — whether they must coincide or can be negotiated to different values with different consequences — is left unresolved here; see Blocked Specification Questions.

A **technical-loss** outcome (a side crashing, exceeding time, or committing cryptographic forgery) is recognized as an end condition by Base Logic. Detection of crashes, timeouts, and cryptographic forgery itself belongs to later stages (orchestrator/watchdog, cryptography), not to this PRD.

### Scoring

Fixed per-episode scores (Annex F status: **fixed** for all values below):

| End condition | Cop score | Thief score |
|---|---|---|
| Capture | 20 | 5 |
| Survival | 5 | 10 |
| Technical loss | 0 | 0 |

The tie score (2) is a league/series-level rule — it applies when the *cumulative* score across a whole series of episodes ends level between two teams. It is outside the per-episode responsibility of PRD-01.

### Deterministic Enforcement

- There is no external judge; the agents themselves enforce the game's physics.
- Legality of moves, state transitions, capture conditions, and scores are all enforced by deterministic code.
- An LLM must not decide whether a move is legal or whether a capture occurred.
- Strategy selection (how an agent chooses its moves or barrier placements) is outside this PRD.

### Annex F Parameter Authority

| Parameter | Annex F value/default | Status |
|---|---:|---|
| [גודל הלוח] | 7×7 | Minimum |
| [מספר הסוכנים] | 2 | Fixed |
| [ראשית מערכת הצירים] | upper-left `(0,0)` corner | Negotiable |
| [אינדקס התחלת הצירים] | 0 | Negotiable |
| [עמדת פתיחה – גנב] | center `(3,3)` on the default board | Negotiable example/default |
| [עמדת פתיחה – שוטר] | corner `(0,0)` on the default board | Negotiable example/default |
| [מערך התנועה] | four orthogonal directions plus stay | Fixed |
| [מכסת המחסומים] | 14 | Minimum |
| [תקרת הצעדים] | 35 | Minimum |
| [סף ההישרדות] | 35 | Minimum |
| Capture score | cop 20, thief 5 | Fixed |
| Survival score | cop 5, thief 10 | Fixed |
| Technical-loss score | cop 0, thief 0 | Fixed |
| League/series tie score | 2 per side | Fixed; outside individual episode scoring |

## Non-Goals

- FastMCP and networking
- Distributed processes
- Scent and pheromones
- Natural-language hints
- LLM integration
- Strategy selection and path planning
- Commit-Reveal, Nonce, hashing, and log audit
- Watchdog and timeout detection
- GUI
- Replay
- Gmail and reporting

## Stage 1 Engineering Decisions

- Following the Chapter 10 recommendation, Stage 1 is exercised locally in a single process before the peers are separated by MCP infrastructure.
- Base Logic remains deterministic and independent of future strategy and LLM behavior.
- Stage 1 represents technical-loss outcomes and their fixed scores, but later watchdog, timeout, and cryptographic stages detect their real-world causes.
- Stage 1 may define data and interface boundaries needed by later verification, but it does not implement Commit-Reveal, Nonce generation, hashing, Capture Claim cryptographic verification, or log audit.
- Loading and validating local `config/game.json` values is required, and deterministic Base Logic uses those validated values. PLAN will determine the responsible module and implementation order without creating a separate unapproved game rule. Remote peer comparison, signed exchange, and remote mismatch refusal remain later-stage integration work.

## Acceptance Criteria

1. On its turn, an agent can move one cell orthogonally or remain in place.
2. A diagonal move is rejected.
3. Movement into a barrier is rejected.
4. The cop can replace movement with a valid barrier placement.
5. A barrier remains impassable for the rest of the episode.
6. A placement beyond [מכסת המחסומים] is rejected.
7. Coordinate overlap with a valid Capture Claim ends the episode as capture.
8. A barrier placed on the thief's cell ends the episode as capture.
9. Subject to resolution of the stay-versus-trapped tension, the mandatory trapped-thief capture rule is implemented exactly as the approved interpretation specifies.
10. Reaching [סף ההישרדות] valid steps without capture ends the episode as survival; its default/minimum is 35.
11. Capture, survival, and technical loss return the correct fixed score pairs.
12. The same agreed physics configuration produces the same deterministic outcome.
13. [תקרת הצעדים] has a default/minimum of 35; behavior when it differs from [סף ההישרדות] remains blocked until specified.
14. Stage 1 loads and validates its local Base Logic parameters from `config/game.json`, and deterministic Base Logic uses those validated values.
15. Stage 1 configuration acceptance is verified locally and does not require communication with a remote peer; byte comparison, signed exchange, and remote mismatch refusal are verified in later integration stages.

The following is a **recommended Chapter-10 milestone**, not an additional mandatory requirement:
- both agents move legally;
- excess barriers are rejected;
- coordinate overlap triggers capture.

## Blocked Specification Questions

1. What exact response is required when a move targets a coordinate outside the board?
2. What is the precise relationship between [תקרת הצעדים] and [סף ההישרדות] if negotiated to different values?
3. Do barrier-on-thief-cell capture and trapped-thief capture require the same Capture Claim and later cryptographic truth-verification flow as coordinate-overlap capture?
4. When the cop places a barrier on the cell it currently occupies, how is its immediate occupancy handled after that cell becomes impassable to both agents?

These questions must remain visibly blocked in PLAN, TODO, implementation, and acceptance testing wherever behavior depends on them. The stay-versus-trapped tension documented above is an additional blocked interpretation issue. No behavior may be selected by assumption.
