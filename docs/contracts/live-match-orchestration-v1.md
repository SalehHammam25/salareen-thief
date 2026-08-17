# Live Match Orchestration Contract v1

**Status:** owner-approved Stage 5 production design; implementation pending

**Protocol family:** `1.0-provisional`
**Authority:** requirements PDF v3.0.0, Appendix E mandatory checklist, Annex F values, and the recorded owner decisions below

## 1. Authority and boundaries

The PDF is authoritative for mandatory behavior. Appendix E is the mandatory-rule checklist and Annex F controls numerical values. Examples are not normative. This contract supplies only the missing engineering choreography needed to compose Stages 1-5.

Mandatory PDF behavior includes independent peers, local truth only, deterministic Python legality, orthogonal movement or STAY, cop-only permanent barriers, Capture Claims, survival and fixed scoring, bounded communication, watchdog/recovery, free-language hints without direct coordinates, and auditable local logs.

Annex F fixes the shared game configuration, including a 7x7 board, thief `[3,3]`, cop `[0,0]`, 14 barriers, 35 valid moves/survival threshold, scent centre `0.9`, decay `0.10`, field size 5, and the scoring table. Response 30 seconds and watchdog 60 seconds are negotiable defaults; backoff 5 seconds, retries 3, queue depth 100, request rate 30/minute and concurrency 2 retain their Annex F status.

Commit-Reveal, secret Nonces, hashes, signatures, signed Step 0 declarations, and cryptographic Capture Claim verification are Stage 6. They MUST NOT be simulated in Stage 5.

## 2. Peer ownership

- Each peer owns only its local authoritative state and local event log.
- There is no central server, central judge, shared runtime object, shared virtual environment, or shared mutable file.
- Each peer validates received facts before applying them locally.
- Neither peer reads objective opponent position, opponent belief, opponent strategy state, private provider configuration, credentials, or private logs.
- Cross-peer agreement is achieved through versioned messages and deterministic reconciliation, never shared memory.
- The cop runner and thief runner are independent production processes. A third game process is forbidden.

## 3. Match identity

Every local match context contains:

| Field | Type | Rule |
|---|---|---|
| `game_id` | non-empty restricted string | Stable for one series/game identity. |
| `session_id` | non-empty restricted string | Stable for one live/recovered session. |
| `protocol_version` | string | `1.0-provisional`. |
| `game_number` | integer | Positive and within the agreed series. |
| `turn_index` | integer | Starts at 0 and advances once per reconciled action. |
| `phase` | enum | One lifecycle state below. |
| `local_role` | enum | `cop` or `thief`. |
| `expected_remote_role` | enum | Opposite of `local_role`. |

The exact recovery identity is `(game_id, session_id, protocol_version, turn_index, phase)`. All five fields MUST match before resume. `game_number` and roles are immutable configured context and MUST also agree with the initialization record.

## 4. Lifecycle state machine

States are `uninitialized`, `configured`, `local_server_ready`, `peer_connected`, `game_initialized`, `awaiting_local_action`, `awaiting_peer_message`, `resolving_turn`, `paused_recovering`, `terminal`, `aborted`, and `shutdown`.

Legal transitions:

| From | To | Trigger |
|---|---|---|
| `uninitialized` | `configured` | Valid shared configuration and private runtime settings load. |
| `configured` | `local_server_ready` | Local `/mcp` server passes readiness. |
| `local_server_ready` | `peer_connected` | Remote endpoint is validated and responds compatibly. |
| `peer_connected` | `game_initialized` | Initialization messages agree exactly. |
| `game_initialized` | `awaiting_local_action` | Local role owns Step 0/next action. |
| `game_initialized` | `awaiting_peer_message` | Remote role owns Step 0/next action. |
| `awaiting_local_action` | `resolving_turn` | Local intent is accepted by local Base Logic and sent. |
| `awaiting_peer_message` | `resolving_turn` | Valid expected-role intent is received. |
| `resolving_turn` | `awaiting_local_action` | Turn reconciles and local role is next. |
| `resolving_turn` | `awaiting_peer_message` | Turn reconciles and remote role is next. |
| any live state | `paused_recovering` | Connection loss, retry exhaustion pending watchdog, or provider interruption. |
| `paused_recovering` | prior live state | Endpoint recovers and exact identity matches. |
| any live state | `terminal` | Reconciled capture, survival, or verified technical result. |
| any non-shutdown state | `aborted` | Identity mismatch, irreconcilable state, invalid initialization, or controlled safety abort. |
| `terminal` | `shutdown` | Terminal outcome and score reconcile; logs flush. |
| `aborted` | `shutdown` | Abort evidence flushes; no winner is invented. |

Every other transition returns `ILLEGAL_PHASE` without mutation. Ordinary game messages received in `terminal`, `aborted`, or `shutdown` return `EPISODE_TERMINAL` or `ILLEGAL_PHASE` deterministically.

## 5. Turn ownership and ordering

The PDF requires alternating role-correct actions but does not specify a complete network choreography. Owner decision LM-OD-01 adopts sequential turns, not simultaneous actions: the thief owns Step 0 because the existing initial active role and Stage 1 contract do so; roles then alternate after each accepted action. Changing that owner decision requires a versioned contract revision.

For each turn:

1. The active peer derives its next-strategy input from its reconciled local state, opponent scent, accepted language evidence and local belief.
2. Its strategy proposes exactly one movement/STAY or, for cop only, one barrier action.
3. Local Base Logic validates the proposal without mutation on rejection.
4. The active peer records an immutable prepared intent and sends it with a correlation ID.
5. The receiver validates shape, protocol, identity, expected sender role, phase, turn and duplicate status, then validates the action through its Base Logic projection.
6. The receiver applies the action exactly once, evaluates capture before survival, records the result, and acknowledges it.
7. The sender applies the acknowledged canonical result exactly once. A lost acknowledgement causes retransmission of the identical intent, never a new action.
8. Only after accepted movement/STAY, each peer decays the previous opponent-scent field, emits at the newly accepted opponent position using fixed values, combines by cell-wise maximum, clips at edges, and publishes its local observation. Rejected actions do not evolve scent.
9. A language hint is generated only at its configured interval, after the accepted action/scent update. It is qualitative, word-limited and coordinate-free. Provider failure uses deterministic fallback and does not invalidate the turn.
10. The receiving peer validates the hint, updates belief from scent before language evidence, and supplies the resulting belief only to the next strategy invocation.
11. If capture or survival occurred, peers exchange terminal outcome and score reconciliation before shutdown. Otherwise the turn index advances once and ownership changes.
12. Each boundary emits structured local events.

Barrier placement is a complete cop action, not movement plus barrier. It does not emit movement scent. Capture is evaluated after its accepted placement using the common Capture Claim boundary. Capture precedes survival when both could be observed at the same boundary.

## 6. Existing geometry contract

The existing `receive_geometry` and `relay_geometry` tools remain unchanged. Their payload has exactly six fields: `protocol_version`, `correlation_id`, `sender_role`, `x`, `y`, `step`. Identity fields MUST NOT be added because strict peers reject unknown fields. Geometry retains its current validation, FIFO-100 idempotency and `DUPLICATE_MISMATCH` behavior.

Production orchestration uses the following additional tools. All payloads are strict objects; unknown/missing fields and bool-as-int are rejected. Restricted IDs use the existing correlation identifier grammar. Enums are lowercase strings unless an existing vocabulary is cited.

## 7. Shared response and validation rules

Every new tool returns either `{"accepted": true, "correlation_id": <id>, "status": <enum>}` or `{"accepted": false, "correlation_id": <id-or-null>, "code": <code>, "detail": <safe-field>}`. Validation order is: object shape, exact keys, primitive types, protocol version, identifier syntax, expected sender role, match identity, lifecycle phase, turn, duplicate lookup, semantic/Base Logic validation. Rejection never mutates state.

Shared rejection codes are `INVALID_SHAPE`, `UNKNOWN_FIELD`, `MISSING_FIELD`, `WRONG_TYPE`, `UNSUPPORTED_VERSION`, `INVALID_CORRELATION_ID`, `INVALID_ROLE`, `WRONG_EXPECTED_ROLE`, `IDENTITY_MISMATCH`, `INVALID_GAME_NUMBER`, `INVALID_TURN`, `ILLEGAL_PHASE`, `DUPLICATE_MISMATCH`, `ACTION_REJECTED`, `BARRIER_REJECTED`, `HINT_REJECTED`, `CAPTURE_REJECTED`, `TERMINAL_MISMATCH`, `SCORE_MISMATCH`, `EPISODE_TERMINAL`, and `REMOTE_ERROR`.

All mutating messages use `(game_id, session_id, tool_name, correlation_id)` as their idempotency key. Identical duplicates return the cached response. Same key with different canonical content returns `DUPLICATE_MISMATCH`. Retry uses the same payload and correlation ID.

Except where a tool explicitly lists a smaller recovery-only set, "identity fields" means the exact fields `protocol_version:str`, `correlation_id:str`, `sender_role:role`, `game_id:str`, `session_id:str`, and `game_number:int`.

## 8. Additional tools

### `initialize_game_v1`

Fields: identity fields plus `config_schema_version:str`, `starting_role:role`. Sender/receiver: either peer to the opposite peer. The configuration itself is established out of band from the byte-identical agreed file; Stage 5 does not send or calculate a digest. The tool mutates only by creating the local initialized context after exact agreement. Accepted status: `initialized`. Retries are idempotent.

### `submit_action_v1`

Fields: identity fields above plus `turn_index:int`, `action_kind:enum(move,stay,barrier)`, `direction:enum(N,S,E,W,STAY)|null`, `x:int|null`, `y:int|null`. Sender must be the active expected role. Cop alone may send `barrier`; movement uses direction and null coordinates; barrier uses coordinates and null direction. Receiver applies an accepted action exactly once. Accepted status: `applied`.

### `acknowledge_action_v1`

Fields: identity fields plus `turn_index:int`, `action_correlation_id:str`, `result:enum(applied,rejected,terminal)`, `result_code:str`, `next_turn_index:int`, `next_role:role`. Sent by the receiver of `submit_action_v1`. It confirms the canonical result; it does not apply the action a second time. Accepted status: `acknowledged`.

No separate barrier tool is created: `submit_action_v1` already represents the mutually exclusive barrier action without ambiguity.

### `publish_scent_v1`

Fields: identity fields plus `turn_index:int`, `axis_start_index:int`, `width:int`, `height:int`, `values:list[list[str]]`. Decimal values are canonical decimal strings. Sender publishes only the opponent-visible scent field derived from the accepted action, never own/private truth. Receiver replaces the observation for that turn exactly once. Accepted status: `observed`.

### `send_language_hint_v1`

Fields: identity fields plus `turn_index:int`, `text:str`, `word_count:int`. Provider selection, credentials, raw provider metadata and token accounting remain private local state and are not sent. Receiver validates length and coordinate prohibition before belief use. Accepted status: `hint_accepted`. Invalid hints are rejected/fallback locally without undoing the action.

### `submit_capture_claim_v1`

Fields: identity fields plus `turn_index:int`, `claimant_role:role`, `capture_kind:enum(cooccupancy,trapped)`, `cop_x:int`, `cop_y:int`, `thief_x:int`, `thief_y:int`. Stage 5 performs deterministic local-rule reconciliation only. It contains no Nonce, commitment, reveal, signature or hash. Accepted status: `capture_confirmed`; disagreement is `CAPTURE_REJECTED` followed by safe abort unless deterministic replay resolves it.

### `reconcile_terminal_v1`

Fields: identity fields plus `turn_index:int`, `outcome:enum(cop_capture,thief_survival,technical_loss,tie)`, `winner_role:role|null`, `loser_role:role|null`, `attribution:enum(local,remote,unknown,none)`, `reason_code:str`. Unknown attribution MUST use null winner/loser unless a nontechnical game outcome already exists. Accepted status: `terminal_agreed`.

### `reconcile_score_v1`

Fields: identity fields plus `turn_index:int`, `outcome:str`, `cop_score:int`, `thief_score:int`. Values must equal Annex F for the reconciled outcome. Mutates only the local finalized score record after equality. Accepted status: `score_agreed`.

### `resume_match_v1`

Fields: `protocol_version`, `correlation_id`, `sender_role`, `game_id`, `session_id`, `turn_index`, `phase`. Receiver compares exact recovery identity and immutable initialized context. It does not replay acknowledged actions. Accepted status: `resume_allowed`; mismatch returns `IDENTITY_MISMATCH` and transitions to `aborted`.

### `shutdown_match_v1`

Fields: identity fields plus `turn_index:int`, `mode:enum(terminal,abort,operator)`, `reason_code:str`. It is accepted only after terminal agreement, abort, or an operator-controlled safe stop. Stop is idempotent and flushes local logs. Accepted status: `shutdown_ready`.

## 9. Exactly-once rules

- A local action becomes prepared only after strategy output passes local Base Logic.
- Preparation is logged before first send and is immutable.
- The receiver applies it only after complete validation and records the result before replying.
- Acknowledgement means the receiver durably recorded the canonical result locally; it is not cryptographic proof.
- The sender applies that result only if its pending correlation and turn match.
- Lost acknowledgements cause identical resend. The receiver returns its cached response.
- Recovery after acknowledgement resumes at the recorded next turn; neither side reapplies the acknowledged action.
- An unacknowledged prepared action is resent identically after exact-identity recovery.
- Correlation reuse with different content aborts the message and never selects one version silently.
- FIFO eviction MUST NOT evict records still needed by the current/recoverable match.

## 10. Expected-role boundary

Cop accepts game messages only from `thief`; thief accepts them only from `cop`. A valid but unexpected role returns `WRONG_EXPECTED_ROLE` without mutation. Stage 5 checks configured protocol identity only. It MUST NOT be described as authentication or spoofing resistance. Stage 6 owns cryptographic peer authentication.

## 11. Endpoint policy

In remote mode the opponent endpoint MUST use HTTPS, the configured exact host and permitted port, the exact `/mcp` path, and no userinfo, query or fragment. Localhost, loopback, link-local and private addresses are rejected in remote mode. Diagnostics redact the complete endpoint authority where necessary. This strict rule supersedes the thief behavior that previously permitted query strings.

## 12. Recovery and attribution

On disconnect the runner stops accepting new strategy actions and enters `paused_recovering` at the last recorded boundary. It performs bounded retries/backoff while the watchdog remains valid. Resume requires exact recovery identity and initialized context. Matching state returns to the prior live phase. Mismatch aborts. Acknowledged actions are never reapplied; pending unacknowledged actions are retried identically.

Verified local application/process failure may be `local`; verified remote application failure while the local path is healthy may be `remote`; DNS, TLS, Internet, provider and ambiguous observations are `unknown`. Unknown attribution never invents a winner or technical-loss score. After recovery, any already-detected terminal result must still pass terminal and score reconciliation.

## 13. Local structured log

Each peer appends ordered local JSON events with `schema_version`, `event_index`, `timestamp_monotonic`, `game_id`, `session_id`, `game_number`, `turn_index`, `phase`, `local_role`, `event_type`, `correlation_id`, `related_correlation_id`, `result_code`, and `data`. `data` contains only protocol-visible/local facts and no secrets.

Required event types: `configured`, `server_ready`, `peer_connected`, `game_initialized`, `strategy_invoked`, `action_prepared`, `message_sent`, `message_received`, `message_rejected`, `action_applied`, `ack_sent`, `ack_received`, `duplicate_replayed`, `scent_updated`, `hint_sent`, `hint_received`, `belief_updated`, `capture_evaluated`, `survival_evaluated`, `paused`, `reconnect_attempted`, `resume_accepted`, `resume_rejected`, `watchdog_expired`, `failure_attributed`, `terminal_proposed`, `terminal_agreed`, `score_agreed`, `aborted`, and `shutdown`.

Logs must reconstruct ordering and correlation deterministically. Stage 5 does not hash, sign, commit, reveal or provide Stage 7 GUI/reporting.

## 14. Production ownership

`salareen_cop` owns a local cop runner composing configuration -> Base Logic -> cop strategy -> transport -> scent/language/belief -> recovery -> local log. `salareen_thief` owns the corresponding thief runner. Neither imports the other package. Shared contracts and fixtures are copied byte-for-byte, not loaded from a shared runtime directory.

## 15. Byte-stable fixtures

Both repositories must contain byte-identical files under `tests/fixtures/live-match-v1/`:

- `initialization.json`
- `normal-turn.json`
- `cop-barrier-turn.json`
- `duplicate-acknowledgement.json`
- `capture.json`
- `survival.json`
- `disconnect-resume.json`
- `terminal-score-reconciliation.json`

Fixtures use UTF-8, LF, two-space indentation, sorted contract-defined key order, one trailing newline, canonical decimal strings and placeholder endpoints only. Tests compare bytes and Git object IDs.

## 16. Dependency alignment

Lockfiles need not be byte-identical because package names differ. Before runner implementation both manifests must align on Python `>=3.12,<3.13`, FastMCP `>=2.0,<3`, the same explicitly selected MCP dependency policy, pytest `>=8.4.2,<9`, and Ruff `>=0.16.3,<0.17`. This design task does not edit manifests or lockfiles.

## 17. Adversarial acceptance

Implementation is incomplete until tests prove: no central process/shared state/hidden truth; one unambiguous active role; barrier-action exclusivity; no double application after duplicate/lost acknowledgement/recovery; strict payload equality; capture before survival; scent then language then belief order; mismatch abort; unknown attribution without invented blame; no Stage 6 primitives; identical endpoint validation; and expected-role rejection described only as protocol validation.

## 18. Open owner decisions

- **LM-BQ-01:** The PDF does not fully prescribe Step 0 network choreography. LM-OD-01 selects thief-first sequential turns to match existing Base Logic; owner approval is recorded by this contract request.
- **LM-BQ-02:** Durability medium for the phrase "durably recorded" remains an implementation choice; it must survive the supported recovery model and be tested.
- **LM-BQ-03:** Stage 5 Capture Claim disagreement cannot be cryptographically adjudicated. Safe abort with complete local evidence is required; Stage 6 owns proof.
- **LM-BQ-04:** Technical-loss attribution across ambiguous network/provider failures remains unknown pending later audit; no winner is invented.

## 19. Review policy

Project owner Areen approved this bounded design, including the no-central-runner rule, strict endpoint policy, expected-opponent-role validation, Stage 5/6 boundary, and LM-OD-01. Review is Codex-assisted adversarial review plus automated documentation verification; an independent human reviewer is not required by the owner-approved policy.
