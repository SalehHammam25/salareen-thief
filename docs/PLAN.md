# Project Implementation Plan

**Status:** Stage 1 approved; Stages 2-7 ready for review
**Repository:** salareen-thief
**Current stage:** Documentation preparation for Stages 2-7
**Implementation:** Stage 2 not started

## Development Lifecycle

The project follows this lifecycle:

Idea -> PRD -> PLAN -> TODO -> Verify -> Execute -> Push

1. **Idea:** identify the required outcome and its source.
2. **PRD:** define behavior, scope, non-goals, acceptance criteria, and unresolved requirements.
3. **PLAN:** define the approved delivery sequence, engineering constraints, test strategy, and verification gate without writing implementation code.
4. **TODO:** decompose the approved PRD and PLAN into traceable, meaningful work items.
5. **Verify:** confirm that the PRD, PLAN, and TODO agree and that blocked questions have not been answered by assumption.
6. **Execute:** implement only the reviewed scope, with unit tests and recorded evidence.
7. **Push:** push the dedicated branch, open a Pull Request, review it, and merge only after the stage is stable and verified.

Implementation must not begin until the corresponding PRD, PLAN, and TODO have been reviewed. Every mandatory PRD requirement must map to PLAN work, one or more TODO items, and verification evidence.

## Git and Review Workflow

- Work on a dedicated branch; do not develop directly on `main`.
- Keep each branch and Pull Request focused on one approved documentation or implementation concern.
- Review documentation Pull Requests before creating dependent implementation branches.
- Stage only intended files and inspect the staged diff before committing.
- Use meaningful commits that preserve the development history.
- Push the branch and use a Pull Request before merging into `main`.
- Merge only after required tests and checks pass and the review finds no unresolved scope violation.
- After a merge, synchronize local `main` with `git pull --ff-only origin main` before beginning dependent work.

### Review Policy

- Pull Requests, automated verification and truthful evidence are mandatory.
- Independent human review is recommended when available but is not an
  official specification requirement.
- When no independent reviewer is available, perform and record a strict
  Codex-assisted adversarial self-review, identify the AI interface truthfully,
  state `Independent human reviewer: None`, and obtain Areen's explicit owner
  approval before treating the review condition as satisfied.
- Never describe an owner-approved exception as independent review. ADR-002
  records the Stage 1 corrective exception and governs future stages.

## Authority Hierarchy

When planning or implementing behavior, apply this order:

1. The official specification's explicitly mandatory rules govern behavior.
2. Appendix E is the consolidated checklist of mandatory rules, prohibitions, and recommendations.
3. Annex F is the sole authority for quantitative values and their status:
   - **fixed** values cannot change;
   - **minimum** values may be increased only by mutual agreement and otherwise use the listed default;
   - **negotiable** values may change by mutual agreement and otherwise use the listed example/default.
4. The approved `docs/prd/PRD-01-base-logic.md` defines the reviewed Stage 1 interpretation and boundary.
5. Chapter 10's seven-stage order, milestones, and incremental-delivery guidance are recommendations, not additional mandatory game rules.
6. Illustrations, sample layouts, sample code, and examples are nonbinding unless explicitly identified as mandatory.
7. Engineering decisions may organize implementation but may not silently create, weaken, or resolve a game rule.

If sources genuinely conflict, record the conflict, obtain an explicit decision, and document the selected interpretation and reasoning before dependent work proceeds. Annex F remains authoritative for numeric conflicts.

## Project Engineering Constraints

- Perform project actions through terminal commands.
- Claude CLI is the project's preferred AI interface where available; Codex is currently being used. Record truthfully the actual AI interface and commands used for each applicable project action.
- Use `uv` for Python environment, interpreter, dependency, and command management.
- Require unit tests for deterministic behavior.
- Keep every Python file at or below 150 lines, including tests and scripts. Split files by responsibility before they exceed the limit.
- Keep deterministic rules independent from strategy selection, prompts, LLM providers, and other nondeterministic behavior.
- Reject invalid input explicitly and do not mutate game state after a rejected action.
- Never commit secrets, credentials, tokens, private keys, private configuration, or generated local environments.
- Record exact commands, exit results, and relevant test summaries during implementation.
- Preserve user work and unrelated changes; stage only files belonging to the approved task.
- The project-wide TODO documents should eventually contain at least 500 meaningful tasks in total. The course's 800-1000 target is guidance, not permission to pad tasks artificially.

## Recommended Stage Order

1. Base Logic
2. Basic MCP Infrastructure
3. Blind Strategy
4. Language and Scent
5. Cloud Exposure and Tunneling
6. Security and Cryptography
7. Reporting and Visualization Shell

This is the recommended Chapter 10 progression. Each stage must work end-to-end within its approved boundary before the next stage begins.

## Stage 1 - Base Logic

### Objective

Build and verify the deterministic, local, single-process game-physics foundation needed by the thief peer. Stage 1 must prove the board rules independently of networking, strategy, language models, and cryptographic enforcement.

### Approved Inputs

- `docs/prd/PRD-01-base-logic.md`, status `Approved for planning`.
- Official specification Chapter 3 for board physics and scoring.
- Official specification Chapter 10 for the recommended Stage 1 boundary and milestone.
- Appendix E for mandatory-rule cross-checking.
- Annex F for numeric values and classifications.
- `docs/todo/TODO-01-base-logic.md`, which must be expanded only after this PLAN is reviewed.

### In Scope

- local loading and validation of Base Logic values from `config/game.json`;
- a finite square board and agreed coordinate conventions;
- representation of cop and thief roles, starting positions, and current positions;
- the fixed movement set: one orthogonal cell or stay;
- deterministic validation of moves and barriers where the specification is unambiguous;
- permanent barrier state and barrier-quota accounting;
- capture and survival outcomes where their interpretation is approved;
- technical-loss outcome representation without later-stage detection mechanisms;
- fixed per-episode score mapping;
- deterministic state transitions and repeatability;
- local, single-process tests that exercise both roles as required to verify shared physics.

### Thief-Specific Responsibilities

The thief repository must:

- load and validate the local Base Logic configuration used by the thief runtime;
- represent the thief's authoritative local position and legal action set;
- validate requested thief moves before state mutation;
- reject diagonal movement and movement into a known barrier;
- apply declared cop barrier placements to the local deterministic state;
- enforce barrier permanence and treat barriers as impassable to the thief;
- evaluate capture, survival, technical-loss representation, and scoring without relying on strategy or an LLM;
- expose deterministic boundaries that later thief strategy code can call without embedding strategy inside the rules;
- produce the same result for the same validated configuration, initial state, and ordered action sequence.

Stage 1 may simulate both roles locally for verification. This does not introduce shared runtime state between the eventual distributed peers.

### Local Configuration Boundary

- Stage 1 reads its local `config/game.json` and validates the Base Logic values before creating game state.
- Deterministic Base Logic uses only validated values rather than duplicating configurable constants in rule code.
- Annex F fixed, minimum, and negotiable classifications govern validation and defaults.
- Stage 1 does not contact a remote peer to compare configuration bytes.
- Byte-identical peer comparison, signed configuration exchange, and refusal of a remotely detected mismatch remain mandatory later-stage integration work.
- Private `config/game.toml`, where later required, is local and unsigned; a duplicate shared key is overridden by the shared JSON. Stage 1 need not add unrelated private settings.
- The detailed TODO must identify the local loader, validation, fixtures, and failure cases without expanding Stage 1 into networking or cryptography.

### Numeric Baseline

Stage 1 planning uses the approved PRD's Annex F table:

- board size: 7x7 minimum/default;
- agent count: 2 fixed;
- movement: four orthogonal directions plus stay, fixed;
- barrier quota: 14 minimum/default;
- move ceiling: 35 minimum/default;
- survival threshold: 35 minimum/default;
- capture score: cop 20, thief 5, fixed;
- survival score: cop 5, thief 10, fixed;
- technical-loss score: cop 0, thief 0, fixed.

The series-level tie score of 2 is not part of Stage 1 per-episode scoring.

### Non-Goals

- FastMCP servers, clients, tools, or networking;
- separate peer processes or remote communication;
- byte comparison with a remote peer;
- signed configuration exchange or remote mismatch refusal;
- scent, pheromones, natural-language hints, or deception;
- thief path planning, heuristics, reinforcement learning, or any other strategy;
- LLM prompts, providers, or model calls;
- Commit-Reveal, Nonce generation, hashing, signatures, Capture Claim cryptographic verification, or log audit;
- watchdogs, timeouts, crash detection, or live technical-loss detection;
- tunneling or public endpoints;
- GUI, replay, Gmail, reporting, or league orchestration.

## Proposed Stage 1 Implementation Sequence

This sequence defines responsibilities and dependencies, not filenames, class names, or APIs. TODO-01 will decompose it after approval.

1. **Environment and project foundation**
   - initialize or validate the `uv` project;
   - establish source and test separation;
   - establish the automated 150-line check;
   - verify ignore rules protect environments, caches, secrets, and private configuration.

2. **Local configuration loading and validation**
   - load `config/game.json` locally;
   - validate required Base Logic keys, types, shapes, fixed values, and minimums;
   - apply documented defaults only where the approved requirements allow them;
   - fail explicitly before state creation when configuration is invalid;
   - provide deterministic configuration fixtures for tests.

3. **Core immutable values and state**
   - represent roles and coordinates;
   - represent board dimensions and coordinate conventions;
   - represent starting/current positions, barriers, barrier usage, valid-step count, episode status, outcome, and score pair;
   - define invariants and prevent rejected actions from mutating state.

4. **Movement validation**
   - accept one-cell orthogonal movement and stay;
   - reject diagonal movement;
   - reject movement into barriers;
   - reject off-board targets explicitly without mutating state.

5. **Barrier transitions**
   - permit barrier actions only for the cop in the local rules model;
   - make placement replace movement;
   - validate unambiguous placement constraints and quota;
   - preserve barriers permanently;
   - implement Chapter 3.4 own-cell placement with grandfathered occupancy,
     permanent blocking of future entry, and overlap-claim priority.

6. **End-condition evaluation**
   - implement coordinate-overlap capture with the Stage 1 non-cryptographic Capture Claim representation;
   - apply one local deterministic Capture Claim boundary to overlap,
     barrier-on-thief, and trapped-thief capture;
   - evaluate trapping from adjacent orthogonal destinations; STAY does not
     prevent a genuinely trapped capture;
   - reject configurations whose move ceiling and survival threshold differ;
   - represent technical loss without implementing detection.

7. **Scoring**
   - map approved terminal outcomes to fixed score pairs;
   - keep the series tie score outside episode logic;
   - reject scoring of a nonterminal or invalid outcome.

8. **Unit tests and deterministic fixtures**
   - map each unblocked PRD acceptance criterion to tests;
   - test valid, invalid, boundary, and no-mutation behavior;
   - test configuration defaults, minimums, fixed values, missing keys, and malformed values;
   - replay identical action sequences from identical inputs and compare complete results;
   - add tests for formerly blocked behavior only after its decision is documented.

9. **Verification and review**
   - run all required commands;
   - capture command, exit code, and concise result evidence;
   - inspect PRD-to-PLAN-to-TODO-to-test traceability;
   - open a focused implementation Pull Request only after the documentation gate is complete;
   - merge only after the binary Stage 1 gate passes.

## Unit-Testing Strategy

- Use `pytest` through `uv`; do not rely on a globally installed test runner.
- Keep deterministic rule tests independent of wall-clock time, network access, randomness, LLMs, and external services.
- Use table-driven or parameterized tests for coordinate conventions, board sizes, legal moves, score pairs, and configuration classifications.
- Test both successful transitions and explicit rejection paths.
- Assert that rejected actions preserve the complete prior state.
- Test terminal states so later actions cannot silently alter completed outcomes.
- Maintain direct traceability from each approved PRD acceptance criterion to
  at least one test or an explicit approved decision record.
- Encode clarified behavior only as recorded in PRD-01 and ADR-001.

## Deterministic-Repeatability Strategy

For each repeatability fixture:

1. load the same validated local configuration;
2. create the same initial state;
3. apply the same ordered action sequence;
4. compare every resulting state field, terminal outcome, and score pair;
5. repeat the run in a fresh process when the Stage 1 runner exists;
6. retain the input fixture and result summary as verification evidence.

No seed may be necessary for Base Logic because the rules must contain no randomness. If randomness appears, it is a scope defect unless separately approved.

## `uv` Environment and Dependency Workflow

The implementation phase must use this workflow:

1. install and confirm `uv` outside committed project data;
2. create or use the project environment through `uv`;
3. declare runtime and development dependencies in project metadata;
4. generate and commit the lockfile when dependencies are introduced;
5. synchronize from the lockfile before verification;
6. invoke Python tools through `uv run`;
7. never commit `.venv`, caches, credentials, or machine-private configuration.

Dependency additions require a documented reason. Stage 1 should prefer the Python standard library and add only dependencies needed for the approved deterministic scope and tests.

## Planned Implementation Verification Commands and Evidence

These commands are planned for the implementation phase and have not yet passed because implementation has not started. Once the planned project files exist, Stage 1 verification must run them from the repository root:

```text
uv sync --frozen
uv run pytest -q
uv run python scripts/check_python_line_lengths.py
git diff --check
git status -sb
```

Before commit, also inspect the intended staged content:

```text
git diff --cached --check
git diff --cached --stat
git diff --cached
```

Evidence must record:

- the exact command;
- execution date and commit or branch context;
- exit code;
- concise stdout/stderr summary;
- test counts and failure details, if any;
- every Python file above 150 lines, if the line check fails;
- the PRD acceptance criterion or TODO group verified;
- unresolved or skipped behavior and its blocker identifier.

Changing a command requires PLAN or TODO review before relying on the replacement as gate evidence. The planned line-length script is an implementation-support artifact and must itself remain at or below 150 lines.

## Approved Clarification Handling

ADR-001 records Areen's approval of the five former blockers. Implementation
must now follow those decisions exactly and must distinguish the PDF's explicit
rules from project interpretations:

- Chapter 3.4 explicitly permits own-cell barrier placement;
- Appendix E rules 46-47 explicitly require the special capture paths;
- off-board response, common claim procedure, and parameter relationship were
  unspecified;
- STAY and trapped capture were in tension.

Any newly discovered contradiction with higher-authority mandatory text must
stop implementation and return to PRD/ADR review. Cryptographic claim proof and
remote verification remain deferred and are not implied by the local claim.

## Binary Stage 1 Verification Gate

Stage 1 is either **PASS** or **FAIL**. It passes only when all conditions below are true:

- PRD-01, this PLAN, and TODO-01 are approved and traceable;
- every mandatory Stage 1 requirement is implemented or has an approved interpretation that is implemented;
- every former blocked question is implemented exactly as ADR-001 records;
- local `config/game.json` loading and validation pass without remote-peer communication;
- deterministic Base Logic uses the validated configuration values;
- every unblocked acceptance criterion maps to passing unit tests;
- the full unit-test suite passes;
- repeatability fixtures produce identical complete results;
- rejected actions do not mutate state;
- every Python file is at or below 150 lines;
- all required commands exit successfully and their evidence is recorded;
- no networking, strategy, LLM, cryptographic, GUI, replay, reporting, or other later-stage implementation entered Stage 1;
- no secrets or private configuration are staged or committed;
- the implementation Pull Request is reviewed and approved.

If any condition is false, the gate is **FAIL**, Stage 1 remains incomplete, and Stage 2 implementation must not begin.

## Stage 2 - Basic MCP Infrastructure

**Authority:** Chapters 2, 8 and 10.3.2; Appendix E rules 1-10; Annex F
Table 19. **Milestone:** two separate localhost processes exchange and decode a
versioned geometric message through symmetric FastMCP server/client roles.

Dependency order: (1) approve cross-repository tool/schema/error contracts;
(2) add isolated process entry points and private endpoint configuration; (3)
add deterministic codecs and validation; (4) add FastMCP server and client;
(5) route both through the sole orchestrator gateway and legal phase machine;
(6) add deadlines, bounded retries and watchdog boundaries; (7) run process,
negative, repeatability and localhost integration tests. Public tunnels,
strategy, language/scent, cryptographic trust and reporting are non-goals.

Gate: both peers serve and call the agreed tool from separate processes; no
shared state exists; malformed/out-of-phase messages do not mutate state; the
same fixtures repeat identically; all quality and evidence commands pass.
MCP-BQ-01 through MCP-BQ-03 block only their dependent contract tasks.

## Stage 3 - Blind Strategy

**Authority:** Chapter 6 and 10.3.3-10.4; Appendix E recommendation 25; Annex F
Table 22. **Milestone:** the thief autonomously follows a shortest legal route
to a known target without scent, language or manual intervention.

ADR-004 approves the built-in breadth-first policy, `N, S, E, W` tie order,
private `module.path:ClassName` plugins, no-argument construction, typed visible
fallback, and an N-squared search bound without a board maximum.

Dependency order: (1) apply the approved strategy choice, tie-breaking and plugin seam;
(2) define immutable strategy inputs and typed proposals; (3) enumerate legal
actions through Base Logic; (4) implement the chosen deterministic shortest
route policy; (5) validate every proposal through Base Logic; (6) add private
strategy selection; (7) run unreachable, malicious-plugin, performance and
fresh-process repeatability tests. Q-learning is optional, not mandatory.

Gate: all outputs are legal or typed failures; strategy cannot mutate state or
bypass rules; shortest-route fixtures pass deterministically; Stage 4 imports
are absent. ADR-004 resolves STR-BQ-01 through STR-BQ-03; the final gate still
requires Pull Request, merge, and synchronized-main evidence.

## Stage 4 - Language and Scent

**Authority:** Chapters 4, 6.4-6.5 and 10.3.4; Appendix E rules/recommendation
25-27; Annex F Tables 14, 16, 18 and 21. **Milestone:** free-language hints are
used for inference, the opponent scent map updates and decays each step, and an
LLM can produce verbal text without controlling spatial legality.

Dependency order: (1) apply the six owner-approved ADR-006 scent, language, and
belief decisions; (2) implement fixed 0.9 center, 0.10 decay and 5x5 scent value
model; (3) expose opponent scent only; (4) implement belief updates; (5) add
free-language messages and direct-coordinate rejection; (6) add private
provider abstraction, deterministic template fallback and every-N-step calls;
(7) add token accounting/budget enforcement; (8) run numeric, prompt-injection,
provider-failure and repeatability tests. Tunnels and cryptographic commitment
remain later work.

Gate: fixed scent values and approved ordering pass exact tests; no objective
opponent location leaks; direct coordinates reject; LLM output cannot mutate
state or select an unchecked move; actual tokens are accounted. ADR-006 resolves
LS-BQ-01 through LS-BQ-06; the gate now depends on implementation evidence,
Pull Request review, merge, and synchronization.

## Stage 5 - Cloud Exposure and Tunneling

**Authority:** Chapters 2.4 and 10.3.5; Appendix E rules 1-2 and 10; Annex F
network timeout values. **Milestone:** a complete match runs between remote
machines through public tunnel endpoints.

Dependency order: (1) implement the ADR-007 provider-neutral safe local boundary;
(2) obtain owner/team approval for provider, exchange, and failure policy;
(3) provision external account/token outside Git and implement its adapter;
(4) validate/redact endpoints; (5) expose both peers and
perform symmetric health checks; (6) add latency, disconnect, retry, watchdog
and shutdown behavior; (7) run two-machine match and fault-injection tests.

Gate: remote bidirectional MCP and a complete match pass; no localhost shortcut
or secret leakage exists; failures never wait indefinitely. Reachability is not
authentication. CLD-BQ-01 through CLD-BQ-05 and external account/firewall work
remain explicit blockers. Local verification may pass while the final Stage 5
gate remains FAIL until authorized two-machine public-tunnel evidence exists.

## Stage 6 - Security and Cryptography

**Authority:** Chapter 5 and 10.3.6; Appendix B; Appendix E rules 11-24 and
46-48; Annex F. **Milestone:** every move completes Commit, Acknowledge, Reveal
and final Nonce audit; signed Step-0 and byte-identical shared configuration
verify before play.

Dependency order: (1) approve canonical bytes, signatures/key trust, complete
commitment and Capture Claim schemas; (2) compare/sign/refuse shared config;
(3) sign Step-0 with hardware/model/team/game-count/exact commit; (4) generate
fresh secret Nonces and SHA-256 commitments; (5) enforce protocol phases; (6)
verify all capture causes through the common claim path; (7) append complete
logs and perform final mutual audit; (8) add tamper, forgery, replay, secrecy,
fuzz and cross-repository vectors.

Gate: one-byte config changes refuse before play; every commitment recomputes
across repositories; any changed field/false claim produces the mandated loss;
no secret enters Git/logs/errors. SEC-BQ-01 through SEC-BQ-06 block dependent
security work and may not be filled by a convenient library default.

## Stage 7 - Reporting and Visualization Shell

**Authority:** Chapters 7, 9 and 10.3.7; Appendices A, C and E; Annex F Tables
17-20. **Milestone:** both peers independently send agreeing signed JSON reports
through Gmail, the GUI shows local truth, and replay verifies a complete log.

Dependency order: (1) approve artifact schemas/identifiers/email idempotency and
GUI choice; (2) build read-only local-truth GUI with heatmap/turn lock; (3) build
deterministic Verified OK/TAMPERED replay; (4) implement fixed league counting,
diversity, caps and tie aggregation; (5) generate declaration/config/log/result
JSON; (6) provision OAuth externally with gmail.send only; (7) add quota,
token-bucket, DOS and 429 controls; (8) send separate agreeing reports; (9)
complete two-repository README/screenshots/tag/submission evidence.

Gate: GUI never reveals global truth; any log mutation disqualifies; both JSON
reports validate and agree; non-contradictory league values match Annex F;
secrets are ignored; all repository/submission checks pass. REP-BQ-01 through
REP-BQ-07 and external Google/course actions remain explicit blockers. The
Annex F six-game series versus Appendix E rule 52 one-counted-game rule is not
implemented until the terminology/relationship is formally approved.

## Cross-Stage Verification and Delivery Rules

For Stages 2-7, implementation verification is planned, not already passed:

```text
uv lock
uv sync --frozen
uv run ruff check .
uv run pytest -q
uv run python scripts/check_python_line_lengths.py
git diff --check
git status -sb
git diff --name-only
```

Each stage must also run focused integration, negative, security and
fresh-process repeatability tests appropriate to its external boundaries; scan
for credentials, private TOML, generated environments and forbidden dependency
leaks; and record exact versions, commands, exit codes, failures and corrections
in `docs/verification/`. Before commit, inspect `git diff --cached --check`, the
complete staged diff, names and statistics. Commit and push only the reviewed
scope, open a focused PR, obtain review, merge, synchronize `main`, and record a
binary PASS before implementing the next stage.

Cross-repository contracts are jointly versioned: MCP envelopes/tools/errors
(Stage 2), language/scent payloads (Stage 4), endpoint exchange (Stage 5),
canonical cryptographic/config/claim/log formats (Stage 6), and report/artifact
schemas (Stage 7). A change is not effective until both repositories approve
it. External accounts, public URLs, OAuth consent, credentials, opponent
scheduling, repository access and final submission actions must be labelled
external and may never be simulated as completed evidence.

## Mandatory-Rule Stage Ownership Audit

| Authority | Owning stage | Reason / later consumer |
|---|---:|---|
| Appendix E 1-7 | 2 | process separation, gateway, state machine and reliability |
| Appendix E 8-9 | 7 | enforced by live GUI; local-truth DTO begins in Stage 2 |
| Appendix E 10 | 5 | public tunnel exposure |
| Appendix E 11-12 | 6 | remote byte identity, signing and negotiated-value enforcement; local validation began in Stage 1 |
| Appendix E 13-16 | 1 | movement/barrier physics, already owned by Base Logic |
| Appendix E 17-24 | 6 | Commit-Reveal, Nonce, audit, Capture Claim and Step-0 |
| Appendix E 25 | 3/4 | recommendation: algorithmic movement in Stage 3; LLM verbal boundary in Stage 4 |
| Appendix E 26-27 | 4 | free language and no direct numeric-coordinate protocol |
| Appendix E 28-30 | 7 | Gmail Gatekeeper and send-only authorization |
| Appendix E 31-45 | 7 | league, reporting, secret hygiene and submission administration |
| Appendix E 46-48 | 1/6 | deterministic capture/scoring in Stage 1; cryptographic claim verification in Stage 6 |
| Appendix E 49-52 | 7 | repositories, required contents, report address and counted-game rule |
| Appendix E 53-54 | 6/7 | signed exact commit/token capture in Stage 6; final report in Stage 7 |
| Appendix E 55 | 7 | course grading statement; no implementation behavior |

This is intentional shared ownership only where one stage creates a local
deterministic fact and a later stage proves, displays or reports it. No later
stage is allowed to redefine the underlying Stage 1 outcome.

## Approved Stage 1 Execution Decisions

- the five approved ADR-001 rule clarifications;
- the detailed TODO-01 decomposition and traceability mapping;
- the proposed responsibility sequence in this PLAN;
- the exact project metadata and dependency set introduced through `uv`;
- the exact structure of the Stage 1 local `config/game.json`, constrained by the approved PRD and official shared configuration schema;
- the planned automated line-length check and its repository location.

Approval of this PLAN authorizes TODO preparation, not implementation.
