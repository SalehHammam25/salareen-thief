# Project Implementation Plan

**Status:** Approved for TODO decomposition
**Repository:** salareen-thief
**Current stage:** Stage 1 - Base Logic
**Implementation:** Not started

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
   - keep off-board response behavior blocked pending an approved specification decision.

5. **Barrier transitions**
   - permit barrier actions only for the cop in the local rules model;
   - make placement replace movement;
   - validate unambiguous placement constraints and quota;
   - preserve barriers permanently;
   - keep cop-on-own-new-barrier occupancy behavior blocked.

6. **End-condition evaluation**
   - implement coordinate-overlap capture with the Stage 1 non-cryptographic Capture Claim representation;
   - represent barrier-on-thief and trapped-thief capture only after their blocked procedural interpretations are approved;
   - implement survival only after move-ceiling/threshold precedence is approved where values may differ;
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
- Maintain direct traceability from each approved PRD acceptance criterion to at least one test or an explicit blocked record.
- Do not encode a blocked interpretation in fixtures, helper defaults, or expected values.

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

## Blocked-Question Handling

The following approved PRD questions remain blocked:

1. the exact response to an off-board movement target;
2. the relationship and precedence between move ceiling and survival threshold when they differ;
3. whether barrier-on-thief and trapped-thief capture use the same Capture Claim and later truth-verification flow as overlap capture;
4. immediate cop occupancy after placing a barrier on the cop's own cell.

An additional recorded tension remains blocked: the fixed permission to stay versus capture when all adjacent thief cells are unavailable.

For every blocker:

- TODO-01 must label all dependent tasks as blocked;
- implementation must not choose a behavior through defaults, tests, exception types, control flow, or comments;
- unaffected work may continue;
- resolution requires an explicit documented decision and approval;
- after approval, update the relevant documentation and tests before closing the dependent task;
- Stage 1 cannot pass its final binary gate while a mandatory acceptance path remains undefined.

## Binary Stage 1 Verification Gate

Stage 1 is either **PASS** or **FAIL**. It passes only when all conditions below are true:

- PRD-01, this PLAN, and TODO-01 are approved and traceable;
- every mandatory Stage 1 requirement is implemented or has an approved interpretation that is implemented;
- no blocked question remains capable of changing required Stage 1 behavior;
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

## Later Stages - High-Level Only

- **Stage 2 - Basic MCP Infrastructure:** separate the peers and exchange geometric messages over localhost.
- **Stage 3 - Blind Strategy:** introduce strategy behind deterministic rule interfaces, without scent or language uncertainty.
- **Stage 4 - Language and Scent:** add natural-language interaction, scent dynamics, and the approved LLM boundary.
- **Stage 5 - Cloud Exposure and Tunneling:** connect remote peers through approved public tunneling.
- **Stage 6 - Security and Cryptography:** add Commit-Reveal, Nonce, signed configuration exchange, peer byte comparison, remote mismatch refusal, and audit mechanisms.
- **Stage 7 - Reporting and Visualization Shell:** add reporting, Gmail/OAuth, GUI, and replay capabilities.

Each later stage requires its own reviewed PRD, expanded PLAN content, detailed TODO, tests, and verification gate before implementation.

## Decisions Requiring Approval Before Stage 1 Execution

- the four blocked PRD questions;
- the stay-versus-trapped interpretation;
- the detailed TODO-01 decomposition and traceability mapping;
- the proposed responsibility sequence in this PLAN;
- the exact project metadata and dependency set introduced through `uv`;
- the exact structure of the Stage 1 local `config/game.json`, constrained by the approved PRD and official shared configuration schema;
- the planned automated line-length check and its repository location.

Approval of this PLAN authorizes TODO preparation, not implementation.
