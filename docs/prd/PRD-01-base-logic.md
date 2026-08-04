# PRD 01 — Base Logic

**Status:** Draft
**Repository:** salareen-thief
**Implementation:** Not started

## Purpose

This PRD defines the deterministic local game-physics foundation used by the thief peer: the discrete board, the coordinate system, legal movement, barriers, capture and survival conditions, and per-episode scoring.

The thief peer must calculate and validate the same board state, legal movement, barriers, capture conditions, survival conditions, and scores as the cop peer.

This PRD defines behavior only. It contains no networking and no intelligence (heuristic, LLM, or reinforcement-learning) content.

## Mandatory Requirements

### Board and Coordinate System

- Exactly 2 agents participate (cop and thief).
- [גודל הלוח] — default 7×7 — status: **minimum**.
- Cells are represented as `(row, col)`.
- [ראשית מערכת הצירים] (coordinate origin) — default: the top-left corner, i.e. the corner where cell (0,0) sits — status: **negotiable**.
- [אינדקס התחלת הצירים] (starting index) — default: 0 — status: **negotiable**.
- [עמדת פתיחה – גנב] and [עמדת פתיחה – שוטר] (starting positions) — default example: thief at center (3,3), cop at corner (0,0) — status: **negotiable**; the specific center/corner layout is stated as **example only**.
- Whatever coordinate-origin, starting-index, and starting-position values are agreed must be identical between both peers — a mismatch between what each side counts from or starts at breaks the shared physics.

### Movement

- On its turn, the active agent performs exactly one action.
- That action is either: moving one cell in one of the four orthogonal directions (N/S/E/W), or staying in place.
- Diagonal movement is prohibited.
- An illegal diagonal-move attempt is rejected deterministically.
- Blocked (barrier) cells cannot be crossed by either agent.

Off-grid movement behavior is not invented here — see Open Questions.

### Barriers

- Only the cop may place barriers.
- Placing a barrier replaces movement for that turn (the cop cannot move and place a barrier in the same turn).
- Placement is allowed on the cop's current cell or on one orthogonally adjacent cell.
- [מכסת המחסומים] — default 14 — status: **minimum** (even though it functions as a maximum quota on the number of barriers the cop may place).
- Barriers are permanent and impassable to both agents for the rest of the episode.
- Every barrier placement, and its exact location, must be declared truthfully.
- Hidden placement and lying about a barrier's location are prohibited.

### Capture and End Conditions

An episode ends as a **capture** when any of the following occurs:
- the cop's and thief's coordinates overlap, and the cop declares a Capture Claim;
- the cop places a barrier on the thief's current cell;
- the thief has no legal move because all adjacent cells are blocked by barriers and/or board edges.

An episode ends as a **survival** when the thief survives [סף ההישרדות] valid steps without capture.

[תקרת הצעדים] is a separate mandatory parameter (a per-episode move ceiling). Its precise relationship to [סף ההישרדות] — whether they must coincide or can be negotiated to different values with different consequences — is left unresolved here; see Open Questions.

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

Annex F status of every numerical parameter referenced above:
- [גודל הלוח] — minimum
- [מכסת המחסומים] — minimum
- [סף ההישרדות] — minimum
- [תקרת הצעדים] — minimum
- [ראשית מערכת הצירים] — negotiable
- [אינדקס התחלת הצירים] — negotiable
- [עמדת פתיחה – גנב] / [עמדת פתיחה – שוטר] — negotiable
- Capture, survival, and technical-loss scores — fixed
- Tie score — fixed (league/series-level, not per-episode)

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

## Acceptance Criteria

1. On its turn, an agent can move one cell orthogonally or remain in place.
2. A diagonal move is rejected.
3. Movement into a barrier is rejected.
4. The cop can replace movement with a valid barrier placement.
5. A barrier remains impassable for the rest of the episode.
6. A placement beyond [מכסת המחסומים] is rejected.
7. Coordinate overlap with a valid Capture Claim ends the episode as capture.
8. A barrier placed on the thief's cell ends the episode as capture.
9. A thief with no legal moves is captured.
10. Reaching [סף ההישרדות] valid steps without capture ends the episode as survival.
11. Capture, survival, and technical loss return the correct fixed score pairs.
12. The same agreed physics configuration produces the same deterministic outcome.

The following is a **recommended Chapter-10 milestone**, not an additional mandatory requirement:
- both agents move legally;
- excess barriers are rejected;
- coordinate overlap triggers capture.

## Open Questions

1. What exact response is required when a move targets a coordinate outside the board?
2. What is the precise relationship between [תקרת הצעדים] and [סף ההישרדות] if negotiated to different values?
3. Do barrier-on-thief-cell capture and trapped-thief capture require the same Capture Claim and later cryptographic truth-verification flow as coordinate-overlap capture?
4. When the cop places a barrier on the cell it currently occupies, how is its immediate occupancy handled after that cell becomes impassable to both agents?
5. Is `config/game.json` used directly during Base Logic, or introduced only after the configuration layer is implemented?
