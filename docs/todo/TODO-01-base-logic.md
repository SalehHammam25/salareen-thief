# TODO 01 - Base Logic

**Status:** Approved for Stage 1 execution with ADR-001 clarifications
**Repository:** salareen-thief
**Related PRD:** `../prd/PRD-01-base-logic.md`
**Related PLAN:** `../PLAN.md`
**Implementation:** In progress on `feat/stage-1-gameplay`

## Traceability and Status

Every task has a stable `BLT-NNN` identifier and a `Trace` field. Trace references use:

- `PRD:<section>` or `PRD:AC<n>` for PRD sections and acceptance criteria;
- `PLAN:<section>` or `PLAN:P<n>` for exact PLAN sections and the nine proposed implementation-sequence steps;
- `PLAN:Gate` for the binary Stage 1 verification gate;
- `PDF:C3`, `PDF:C10`, `PDF:E`, and `PDF:F` for Chapter 3, Chapter 10, Appendix E, and Annex F.

`[x]` means completion has concrete implementation, command, commit, or merged
Pull Request evidence as appropriate. `[ ]` means incomplete. Former blockers
Q1-Q4 and STAY are approved in ADR-001 but remain unchecked until implemented.

## 1. Governance and Source Alignment

- [x] **BLT-001** Confirm PRD-01 is approved for planning through merged PR #3. {Trace: PRD:Status; PLAN:Approved Inputs}
- [x] **BLT-002** Confirm the Stage 1 PLAN is approved for TODO decomposition through merged PR #4. {Trace: PLAN:Status; PLAN:P9}
- [x] **BLT-003** Review TODO-01 against every PRD mandatory-requirements subsection. {Trace: PRD:Mandatory Requirements; PLAN:Gate}
- [x] **BLT-004** Review TODO-01 against all fifteen PRD acceptance criteria. {Trace: PRD:AC1-AC15; PLAN:Gate}
- [x] **BLT-005** Review TODO-01 against Chapter 3 board-physics and scoring rules. {Trace: PDF:C3; PLAN:Authority Hierarchy}
- [x] **BLT-006** Review TODO-01 against the recommended Chapter 10 Stage 1 boundary. {Trace: PDF:C10; PLAN:Recommended Stage Order}
- [x] **BLT-007** Cross-check mandatory, prohibited, and recommended classifications against Appendix E. {Trace: PDF:E; PLAN:Authority Hierarchy}
- [x] **BLT-008** Cross-check every Stage 1 numeric value and classification against Annex F. {Trace: PRD:Annex F Parameter Authority; PDF:F}
- [x] **BLT-009** Record Codex as the interface used for this TODO preparation and record actual commands truthfully. {Trace: PLAN:Project Engineering Constraints}
- [x] **BLT-010** Obtain review approval of this TODO before any Stage 1 implementation begins. {Trace: PLAN:Development Lifecycle; PLAN:Gate}

## 2. Environment and `uv` Foundation

- [x] **BLT-011** Confirm the supported Python version before creating project metadata. {Trace: PLAN:P1; PLAN:uv Environment and Dependency Workflow}
- [x] **BLT-012** Confirm `uv` is installed and record its version. {Trace: PLAN:P1; PLAN:uv Environment and Dependency Workflow}
- [x] **BLT-013** Create or validate Python project metadata through `uv`. {Trace: PLAN:P1; PLAN:uv Environment and Dependency Workflow}
- [x] **BLT-014** Define the minimal Stage 1 runtime dependency set and document each dependency's purpose. {Trace: PLAN:P1; PLAN:uv Environment and Dependency Workflow}
- [x] **BLT-015** Define the Stage 1 development dependency group containing `pytest` and approved quality tools. {Trace: PLAN:P1; PLAN:Unit-Testing Strategy}
- [x] **BLT-016** Generate the `uv` lockfile after dependency approval. {Trace: PLAN:P1; PLAN:uv Environment and Dependency Workflow}
- [x] **BLT-017** Verify a clean environment can synchronize from the lockfile. {Trace: PLAN:P1; PLAN:Planned Implementation Verification Commands and Evidence}
- [x] **BLT-018** Verify `.venv`, caches, and local tool outputs are ignored. {Trace: PLAN:P1; PLAN:Project Engineering Constraints}
- [x] **BLT-019** Verify secrets, tokens, private keys, and private configuration cannot enter the intended commit. {Trace: PLAN:P1; PLAN:Gate}
- [x] **BLT-020** Record all environment setup commands, versions, exit codes, and results. {Trace: PLAN:P1; PLAN:Planned Implementation Verification Commands and Evidence}

## 3. Deterministic Architecture and Boundaries

- [x] **BLT-021** Define source and test package boundaries before implementing rules. {Trace: PLAN:P1; PLAN:P3}
- [x] **BLT-022** Assign one clear responsibility to each planned Python module. {Trace: PLAN:P1; PLAN:Project Engineering Constraints}
- [x] **BLT-023** Define dependency direction so game rules do not import strategy code. {Trace: PRD:Deterministic Enforcement; PLAN:P3}
- [x] **BLT-024** Define dependency direction so game rules do not import LLM providers or prompts. {Trace: PRD:Deterministic Enforcement; PLAN:Non-Goals}
- [x] **BLT-025** Define dependency direction so Stage 1 does not import MCP or networking code. {Trace: PRD:Non-Goals; PLAN:Non-Goals}
- [x] **BLT-026** Define pure deterministic boundaries for validation and state transitions. {Trace: PRD:Deterministic Enforcement; PLAN:P3}
- [x] **BLT-027** Define explicit domain-result boundaries for accepted and rejected actions. {Trace: PLAN:P3; PLAN:Unit-Testing Strategy}
- [x] **BLT-028** Define immutable or copy-safe state handling so rejected actions cannot mutate prior state. {Trace: PLAN:P3; PLAN:Gate}
- [x] **BLT-029** Define terminal-state handling so completed episodes cannot be altered. {Trace: PRD:Capture and End Conditions; PLAN:Unit-Testing Strategy}
- [x] **BLT-030** Review the planned module split and confirm every Python file can remain at or below 150 lines. {Trace: PLAN:P1; PLAN:Gate}

## 4. Local Shared Configuration

- [x] **BLT-031** Identify the Base Logic keys required from local `config/game.json`. {Trace: PRD:Shared Base-Logic Configuration; PLAN:P2}
- [x] **BLT-032** Define a local configuration loader with no remote-peer communication. {Trace: PRD:AC14-AC15; PLAN:P2}
- [x] **BLT-033** Define explicit failure behavior for missing `config/game.json`. {Trace: PRD:AC14; PLAN:P2}
- [x] **BLT-034** Define explicit failure behavior for malformed JSON. {Trace: PRD:AC14; PLAN:P2}
- [x] **BLT-035** Validate the configured board size type and square-board shape. {Trace: PRD:Board and Coordinate System; PDF:F}
- [x] **BLT-036** Reject a configured board dimension below the Annex F minimum of 7x7. {Trace: PRD:Annex F Parameter Authority; PDF:F}
- [x] **BLT-037** Validate the fixed agent count is exactly two. {Trace: PRD:Board and Coordinate System; PDF:F}
- [x] **BLT-038** Validate coordinate-origin and starting-index values using the approved shared schema. {Trace: PRD:Board and Coordinate System; PLAN:P2}
- [x] **BLT-039** Validate thief and cop starting-position coordinate shapes and value types. {Trace: PRD:AC14; PDF:C3}
- [x] **BLT-040** Validate both starting positions fall inside the configured board. {Trace: PRD:Board and Coordinate System; PLAN:P2}
- [x] **BLT-041** Validate the fixed movement set is exactly four orthogonal directions plus stay. {Trace: PRD:Movement; PDF:F}
- [x] **BLT-042** Reject a barrier quota below the Annex F minimum of 14. {Trace: PRD:Barriers; PDF:F}
- [x] **BLT-043** Reject a move ceiling or survival threshold below the Annex F minimum of 35. {Trace: PRD:Capture and End Conditions; PDF:F}
- [x] **BLT-044** Validate all fixed capture, survival, and technical-loss score values. {Trace: PRD:Scoring; PDF:F}
- [x] **BLT-045** Prove deterministic rule construction consumes validated configuration values rather than duplicated configurable constants. {Trace: PRD:AC12,AC14; PLAN:P2; PLAN:Gate}

## 5. Board, Coordinates, and State Model

- [x] **BLT-046** Represent a coordinate as an explicit row-and-column value. {Trace: PRD:Board and Coordinate System; PDF:C3}
- [x] **BLT-047** Represent the finite square board using the validated configured dimension. {Trace: PRD:Board and Coordinate System; PLAN:P3}
- [x] **BLT-048** Represent the fixed cop and thief roles without adding agents. {Trace: PRD:Board and Coordinate System; PDF:F}
- [x] **BLT-049** Represent configured coordinate origin and starting index without assuming defaults. {Trace: PRD:Board and Coordinate System; PLAN:P3}
- [x] **BLT-050** Represent configured starting positions for both roles. {Trace: PRD:Board and Coordinate System; PDF:C3}
- [x] **BLT-051** Represent current positions separately from starting positions. {Trace: PLAN:P3; PRD:Purpose}
- [x] **BLT-052** Represent permanent barrier coordinates without duplicates. {Trace: PRD:Barriers; PLAN:P3}
- [x] **BLT-053** Represent used barrier quota and enforce its state invariant. {Trace: PRD:AC6; PLAN:P3}
- [x] **BLT-054** Represent the valid-step count independently from raw action attempts. {Trace: PRD:Capture and End Conditions; PLAN:P3}
- [x] **BLT-055** Represent active and terminal episode status explicitly. {Trace: PRD:Capture and End Conditions; PLAN:P3}
- [x] **BLT-056** Represent capture, survival, and technical-loss outcome types. {Trace: PRD:Capture and End Conditions; PLAN:P3}
- [x] **BLT-057** Define and test initial-state invariants before any action is accepted. {Trace: PRD:AC12; PLAN:P3}

## 6. Movement Rules

- [x] **BLT-058** Represent the five fixed movement choices independently of strategy. {Trace: PRD:Movement; PDF:F}
- [x] **BLT-059** Validate a one-cell north move under the configured coordinate convention. {Trace: PRD:AC1; PLAN:P4}
- [x] **BLT-060** Validate a one-cell south move under the configured coordinate convention. {Trace: PRD:AC1; PLAN:P4}
- [x] **BLT-061** Validate a one-cell east move under the configured coordinate convention. {Trace: PRD:AC1; PLAN:P4}
- [x] **BLT-062** Validate a one-cell west move under the configured coordinate convention. {Trace: PRD:AC1; PLAN:P4}
- [x] **BLT-063** Validate the stay action without changing the agent coordinate. {Trace: PRD:AC1; PLAN:P4}
- [x] **BLT-064** Reject every one-cell diagonal displacement. {Trace: PRD:AC2; PDF:C3}
- [x] **BLT-065** Reject multi-cell orthogonal displacement. {Trace: PRD:Movement; PLAN:P4}
- [x] **BLT-066** Reject a displacement not present in the fixed movement set. {Trace: PRD:Movement; PDF:F}
- [x] **BLT-067** Reject movement into a known barrier. {Trace: PRD:AC3; PLAN:P4}
- [x] **BLT-068** Ensure a rejected movement attempt leaves the complete state unchanged. {Trace: PLAN:Unit-Testing Strategy; PLAN:Gate}
- [x] **BLT-069** Count only accepted valid steps toward applicable episode counters. {Trace: PRD:Capture and End Conditions; PDF:C3}
- [x] **BLT-070** Specify explicit out-of-bounds rejection with exact state preservation. {Trace: ADR-001:D1; PRD:Movement; PLAN:P4}
- [x] **BLT-071** Implement and test off-board rejection in every boundary direction. {Trace: ADR-001:D1; PRD:AC1; PLAN:P4}

## 7. Barrier Rules and Thief State

- [x] **BLT-072** Represent barrier placement as a cop-only action in the local rules model. {Trace: PRD:Barriers; PLAN:P5}
- [x] **BLT-073** Reject a barrier action submitted for the thief role. {Trace: PRD:Barriers; PLAN:P5}
- [x] **BLT-074** Enforce that barrier placement replaces cop movement for the turn. {Trace: PRD:AC4; PDF:C3}
- [x] **BLT-075** Reject an action that combines cop movement and barrier placement. {Trace: PRD:Barriers; PLAN:P5}
- [x] **BLT-076** Accept a barrier target on an orthogonally adjacent cell when otherwise valid. {Trace: PRD:Barriers; PDF:C3}
- [x] **BLT-077** Validate barrier adjacency using the configured coordinate convention. {Trace: PRD:Barriers; PLAN:P5}
- [x] **BLT-078** Reject a diagonal barrier target. {Trace: PRD:Barriers; PLAN:P5}
- [x] **BLT-079** Reject a barrier target more than one orthogonal step away. {Trace: PRD:Barriers; PLAN:P5}
- [x] **BLT-080** Reject barrier placement after the configured quota is exhausted. {Trace: PRD:AC6; PDF:F}
- [x] **BLT-081** Increment barrier usage exactly once for each accepted placement. {Trace: PRD:Barriers; PLAN:P5}
- [x] **BLT-082** Preserve every accepted barrier for the remainder of the episode. {Trace: PRD:AC5; PDF:C3}
- [x] **BLT-083** Apply declared cop barriers to the thief's local deterministic state. {Trace: PRD:Purpose; PLAN:Thief-Specific Responsibilities}
- [x] **BLT-084** Define grandfathered cop occupancy after Chapter 3.4 own-cell placement. {Trace: ADR-001:D4; PDF:C3.4; PLAN:P5}
- [x] **BLT-085** Implement and test own-cell placement, exit, re-entry blocking, permanence, quota, and overlap priority. {Trace: ADR-001:D4; PRD:Barriers; PLAN:P5}

## 8. Capture Conditions

- [x] **BLT-086** Represent a non-cryptographic coordinate-overlap Capture Claim for Stage 1. {Trace: PRD:Stage 1 Engineering Decisions; PLAN:P6}
- [x] **BLT-087** Detect coordinate overlap deterministically from current state. {Trace: PRD:AC7; PLAN:P6}
- [x] **BLT-088** End the episode as capture when overlap and the Stage 1 claim representation are both valid. {Trace: PRD:AC7; PDF:C3}
- [x] **BLT-089** Prevent later actions from mutating a coordinate-overlap capture result. {Trace: PRD:Capture and End Conditions; PLAN:Gate}
- [x] **BLT-090** Map barrier-on-thief-cell capture as a distinct capture cause in the domain model. {Trace: PRD:AC8; PDF:E}
- [x] **BLT-091** Map trapped-thief capture as a distinct capture cause in the domain model. {Trace: PRD:AC9; PDF:E}
- [x] **BLT-092** Keep Capture Claim cryptographic truth verification outside Stage 1. {Trace: PRD:Non-Goals; PLAN:Non-Goals}
- [x] **BLT-093** Apply the common deterministic Capture Claim boundary to barrier-on-thief capture. {Trace: ADR-001:D3; PRD:AC8; PLAN:P6}
- [x] **BLT-094** Apply the common deterministic Capture Claim boundary to trapped-thief capture. {Trace: ADR-001:D3; PRD:AC9; PLAN:P6}
- [x] **BLT-095** Implement barrier-on-thief evidence and claimed terminal capture. {Trace: ADR-001:D3; PRD:AC8; PDF:E46}
- [x] **BLT-096** Implement adjacent-destination trapping evidence and claimed terminal capture. {Trace: ADR-001:D3,D5; PRD:AC9; PDF:E47}
- [x] **BLT-097** Enforce that STAY does not prevent genuinely trapped capture. {Trace: ADR-001:D5; PRD:Capture and End Conditions}
- [x] **BLT-098** Add trapped-state barrier, edge, available-destination, and STAY tests. {Trace: ADR-001:D5; PRD:AC9; PDF:C3.4}

## 9. Survival and Technical-Loss Representation

- [x] **BLT-099** Represent survival as a terminal outcome distinct from capture. {Trace: PRD:Capture and End Conditions; PLAN:P6}
- [x] **BLT-100** Count accepted valid steps for survival evaluation. {Trace: PRD:AC10; PDF:C3}
- [x] **BLT-101** Prevent rejected action attempts from advancing the survival count. {Trace: PRD:AC10; PLAN:Unit-Testing Strategy}
- [x] **BLT-102** End the episode as survival at the configured threshold when no capture occurred. {Trace: PRD:AC10; PLAN:P6}
- [x] **BLT-103** Test the default/minimum survival threshold value of 35. {Trace: PRD:AC10; PDF:F}
- [x] **BLT-104** Represent the configured move ceiling independently from the survival threshold. {Trace: PRD:AC13; PDF:F}
- [x] **BLT-105** Define Stage 1 equality between move ceiling and survival threshold. {Trace: ADR-001:D2; PRD:AC13; PLAN:P2}
- [x] **BLT-106** Reject unequal counter configuration with an explicit relationship issue and tests. {Trace: ADR-001:D2; PRD:AC13; PLAN:P2}
- [x] **BLT-107** Represent technical loss as an externally supplied terminal outcome. {Trace: PRD:Capture and End Conditions; PLAN:P6}
- [x] **BLT-108** Exclude crash, timeout, watchdog, and cryptographic-forgery detection from Stage 1. {Trace: PRD:Non-Goals; PLAN:Non-Goals}

## 10. Episode Scoring

- [x] **BLT-109** Represent a score pair containing cop and thief episode scores. {Trace: PRD:Scoring; PLAN:P7}
- [x] **BLT-110** Map capture to the fixed score pair cop 20 and thief 5. {Trace: PRD:AC11; PDF:F}
- [x] **BLT-111** Map survival to the fixed score pair cop 5 and thief 10. {Trace: PRD:AC11; PDF:F}
- [x] **BLT-112** Map technical loss to the fixed score pair cop 0 and thief 0. {Trace: PRD:AC11; PDF:F}
- [x] **BLT-113** Reject attempts to score an active nonterminal episode. {Trace: PLAN:P7; PLAN:Unit-Testing Strategy}
- [x] **BLT-114** Reject unsupported or malformed outcome values. {Trace: PLAN:P7; PLAN:Unit-Testing Strategy}
- [x] **BLT-115** Keep the fixed series-level tie score of 2 outside per-episode scoring. {Trace: PRD:Scoring; PDF:F}
- [x] **BLT-116** Prove scoring is independent of strategy, LLM output, networking, and wall-clock time. {Trace: PRD:Deterministic Enforcement; PLAN:Gate}

## 11. Positive Unit Tests

- [x] **BLT-117** Create configuration fixtures for default Annex F Base Logic values. {Trace: PLAN:P8; PDF:F}
- [x] **BLT-118** Test a valid board and configured starting state. {Trace: PRD:Board and Coordinate System; PLAN:P8}
- [x] **BLT-119** Parameterize tests for all four valid orthogonal moves. {Trace: PRD:AC1; PLAN:P8}
- [x] **BLT-120** Test the valid stay action. {Trace: PRD:AC1; PLAN:P8}
- [x] **BLT-121** Test a valid cop barrier action replacing movement. {Trace: PRD:AC4; PLAN:P8}
- [x] **BLT-122** Test barrier permanence across subsequent state transitions. {Trace: PRD:AC5; PLAN:P8}
- [x] **BLT-123** Test coordinate-overlap capture and its terminal score pair. {Trace: PRD:AC7,AC11; PLAN:P8}
- [x] **BLT-124** Test survival and its terminal score pair at the approved threshold. {Trace: PRD:AC10-AC11; PLAN:P8}
- [x] **BLT-125** Test externally represented technical loss and its fixed score pair. {Trace: PRD:AC11; PLAN:P8}
- [x] **BLT-126** Test a permitted configuration above each Annex F minimum. {Trace: PRD:Annex F Parameter Authority; PLAN:P8}

## 12. Negative and Invariant Tests

- [x] **BLT-127** Test malformed local JSON is rejected before state creation. {Trace: PRD:AC14; PLAN:P8}
- [x] **BLT-128** Test every missing required Base Logic key is rejected explicitly. {Trace: PRD:AC14; PLAN:P8}
- [x] **BLT-129** Test incorrect configuration value types are rejected explicitly. {Trace: PRD:AC14; PLAN:P8}
- [x] **BLT-130** Test every Annex F fixed-value deviation is rejected. {Trace: PRD:Annex F Parameter Authority; PDF:F}
- [x] **BLT-131** Test every below-minimum Stage 1 value is rejected. {Trace: PRD:Annex F Parameter Authority; PDF:F}
- [x] **BLT-132** Test diagonal movement rejection and complete no-mutation behavior. {Trace: PRD:AC2; PLAN:P8}
- [x] **BLT-133** Test barrier-cell movement rejection and complete no-mutation behavior. {Trace: PRD:AC3; PLAN:P8}
- [x] **BLT-134** Test excess barrier placement rejection and complete no-mutation behavior. {Trace: PRD:AC6; PLAN:P8}
- [x] **BLT-135** Test an action after terminal outcome is rejected without altering outcome or scores. {Trace: PLAN:Unit-Testing Strategy; PLAN:Gate}
- [x] **BLT-136** Audit all tests to ensure no fixture or assertion silently chooses a blocked interpretation. {Trace: PLAN:Blocked-Question Handling; PLAN:Gate}

## 13. Deterministic Repeatability

- [x] **BLT-137** Define a serializable fixture containing validated configuration, initial state, and ordered actions. {Trace: PRD:AC12; PLAN:Deterministic-Repeatability Strategy}
- [x] **BLT-138** Define complete-state comparison fields for repeatability checks. {Trace: PRD:AC12; PLAN:P8}
- [x] **BLT-139** Replay an identical valid movement sequence twice and compare every resulting state. {Trace: PRD:AC12; PLAN:Deterministic-Repeatability Strategy}
- [x] **BLT-140** Replay an identical barrier sequence twice and compare every resulting state. {Trace: PRD:AC12; PLAN:Deterministic-Repeatability Strategy}
- [x] **BLT-141** Replay identical terminal sequences twice and compare outcomes and score pairs. {Trace: PRD:AC12; PLAN:Deterministic-Repeatability Strategy}
- [x] **BLT-142** Repeat deterministic fixtures in fresh processes once a Stage 1 runner exists. {Trace: PLAN:Deterministic-Repeatability Strategy; PLAN:Gate}
- [x] **BLT-143** Verify deterministic tests use no random, network, LLM, or wall-clock inputs. {Trace: PRD:Deterministic Enforcement; PLAN:Gate}
- [x] **BLT-144** Retain repeatability inputs and concise result summaries as verification evidence. {Trace: PLAN:Planned Implementation Verification Commands and Evidence; PLAN:Gate}

## 14. Documentation and Traceability Evidence

- [x] **BLT-145** Create a PRD-acceptance-criterion-to-test mapping for AC1 through AC15. {Trace: PRD:AC1-AC15; PLAN:Gate}
- [x] **BLT-146** Map each implementation file and test file to its TODO category before review. {Trace: PLAN:Development Lifecycle; PLAN:P9}
- [x] **BLT-147** Record every blocked task and its question identifier in implementation evidence. {Trace: PLAN:Blocked-Question Handling; PLAN:Planned Implementation Verification Commands and Evidence}
- [x] **BLT-148** Record the actual AI interface and exact commands used during implementation. {Trace: PLAN:Project Engineering Constraints; PLAN:Planned Implementation Verification Commands and Evidence}
- [x] **BLT-149** Document local `config/game.json` behavior without claiming remote byte comparison. {Trace: PRD:AC14-AC15; PLAN:Local Configuration Boundary}
- [x] **BLT-150** Document that cryptographic exchange and remote mismatch refusal remain later-stage requirements. {Trace: PRD:Shared Base-Logic Configuration; PLAN:Non-Goals}
- [x] **BLT-151** Update task statuses only with command, test, commit, or Pull Request evidence. {Trace: PLAN:Planned Implementation Verification Commands and Evidence; PLAN:Git and Review Workflow}

## 15. Quality and Planned Verification

- [x] **BLT-152** Implement an automated check that fails when any Python file exceeds 150 lines. {Trace: PLAN:P1; PLAN:Gate}
- [x] **BLT-153** Include source files, tests, scripts, and future Python support files in the 150-line scan. {Trace: PLAN:Project Engineering Constraints; PLAN:Gate}
- [x] **BLT-154** Test the line-count checker with compliant and over-limit fixture cases. {Trace: PLAN:P8; PLAN:Gate}
- [x] **BLT-155** Split any Python file before it exceeds 150 lines while preserving single responsibility. {Trace: PLAN:Project Engineering Constraints; PLAN:Gate}
- [x] **BLT-156** Run planned `uv sync --frozen` and record its exit code during implementation verification. {Trace: PLAN:Planned Implementation Verification Commands and Evidence; PLAN:Gate}
- [x] **BLT-157** Run planned `uv run pytest -q` and record test counts and failures. {Trace: PLAN:Planned Implementation Verification Commands and Evidence; PLAN:Gate}
- [x] **BLT-158** Run the planned Python line-count command and record every violation. {Trace: PLAN:Planned Implementation Verification Commands and Evidence; PLAN:Gate}
- [x] **BLT-159** Run the approved lint command, once selected during implementation planning, and record its result. {Trace: PLAN:Project Engineering Constraints; PLAN:Planned Implementation Verification Commands and Evidence}
- [x] **BLT-160** Run `git diff --check` and record its result before implementation review. {Trace: PLAN:Planned Implementation Verification Commands and Evidence; PLAN:Gate}
- [x] **BLT-161** Run `git status -sb` and confirm only approved Stage 1 files are changed. {Trace: PLAN:Planned Implementation Verification Commands and Evidence; PLAN:Gate}

## 16. Commit, Pull Request, and Stage Gate

- [x] **BLT-162** Inspect `git diff --cached --check`, staged statistics, and the complete staged diff. {Trace: PLAN:Planned Implementation Verification Commands and Evidence; PLAN:P9}
- [x] **BLT-163** Confirm no secrets, private configuration, caches, or unrelated user changes are staged. {Trace: PLAN:Git and Review Workflow; PLAN:Gate}
- [x] **BLT-164** Commit implementation in meaningful, reviewable units on a dedicated branch. Evidence: `d6ddf3f`. {Trace: PLAN:Git and Review Workflow; PLAN:P9}
- [x] **BLT-165** Push the implementation branch and open a focused Pull Request against `main`. Evidence: PR #8. {Trace: PLAN:Git and Review Workflow; PLAN:P9}
- [x] **BLT-166** Preserve exact verification commands, exit codes, and summaries in committed verification evidence; PR #8 had no body. {Trace: PLAN:Planned Implementation Verification Commands and Evidence; PLAN:Gate}
- [x] **BLT-167** **OWNER-APPROVED EXCEPTION:** no independent human reviewer participated; Areen approved Codex-assisted adversarial review under ADR-002. {Trace: PRD:Non-Goals; PLAN:Review Policy; ADR-002}
- [x] **BLT-168** Confirm every mandatory Stage 1 path is implemented and no behavior-changing blocker remains. {Trace: PLAN:Gate; PRD:Approved Rule Clarifications}
- [x] **BLT-169** Record a binary Stage 1 PASS only when every PLAN gate condition is true; otherwise record FAIL. {Trace: PLAN:Gate; PDF:C10}
- [x] **BLT-170** PR #8 merged as `25dee6c` before review and local `main` was synchronized; the order deviation is disclosed and waived by Areen in ADR-002. {Trace: PLAN:Git and Review Workflow; PLAN:Review Policy; ADR-002}

## Stage Boundary

Stage 1 now has merged implementation evidence and a truthful owner-approved
review exception under ADR-002. The amended binary Stage 1 gate is PASS. MCP,
networking, signed configuration exchange, cryptographic verification,
strategy, LLM behavior, scent, GUI, presentation replay, Gmail, and reporting
implementation remain outside this stage. Deterministic test replay is limited
to local repeatability verification.
