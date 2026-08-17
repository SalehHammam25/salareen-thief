# TODO 03 - Blind Strategy

**Status:** Unblocked implementation verified; three decisions block final gate
**Related PRD:** `../prd/PRD-03-blind-strategy.md`
**Implementation:** Complete except blocked default/tie/plugin behavior and delivery
**Task ID range:** STR-001 through STR-065

Checked tasks have evidence in `../verification/stage-3-blind-strategy.md`. Items that depend on a PRD blocked question remain non-executable until the decision is approved.

**Trace legend:** policy -> PDF Ch6; milestone -> Ch10.3.3-10.4; LLM boundary -> Appendix E 25; selector -> Annex F 22; acceptance -> PRD-03 AC03.

## Documentation and decisions

- [x] **STR-001** Reconfirm PRD-03 mapping against Chapter 6, Chapter 10, Appendix E 25 and Annex F 22. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-002** Retain STR-BQ-01 through STR-BQ-03 without inventing defaults. {Trace: PRD-03; PLAN:Stage 3; PDF:Ch6}
- [ ] **STR-003** [BLOCKED: STR-BQ-01] Approve the thief default strategy path. {Trace: PRD-03; PLAN:Stage 3; PDF:Ch6.3}
- [ ] **STR-004** [BLOCKED: STR-BQ-03] Approve deterministic equal-cost tie-breaking. {Trace: PRD-03; PLAN:Stage 3; PDF:Ch6.4}
- [ ] **STR-005** [BLOCKED: STR-BQ-02] Approve plugin import/fallback contract. {Trace: PRD-03; PLAN:Stage 3; PDF:Annex F 22}
- [x] **STR-006** Map all acceptance criteria to tests and explicit blockers. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-007** Document why Q-learning is optional. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-008** Document and test Stage 4 language/scent exclusions. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-009** Bound search to at most one visit per board cell, O(N squared), without changing rules. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-010** Preserve the binary Stage 3 gate as FAIL while decision/delivery requirements remain. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}

## Strategy architecture

- [x] **STR-011** Create strategy package separate from base_logic. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-012** Define immutable strategy input snapshot without opponent truth or Stage 4 inputs. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-013** Define typed proposed-action result. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-014** Define typed no-route/decision failure. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-015** Require Base Logic validation after every proposal. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-016** Prevent strategy from mutating immutable GameState/snapshots. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-017** Prevent strategy from importing transport internals. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-018** Prevent deterministic rules from importing strategy. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-019** Define dependency-injected deterministic tie policy without selecting a default. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-020** Keep each Python file within 150 lines. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}

## Blind policy

- [x] **STR-021** Enumerate orthogonal actions with Base Logic movement validation. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-022** Implement known-target distance evaluation. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-023** Implement shortest legal path for orthogonal geometry. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-024** Exclude barriers and off-board cells from search. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-025** Propose STAY only when already at the known target and validate it through Base Logic. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-026** Return explicit unreachable result. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-027** Return explicit terminal-state result. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-028** [BLOCKED: STR-BQ-03] Choose deterministic first step on equal routes. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-029** Test a direct one-step target through Base Logic. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-030** Test multi-turn shortest-route behavior with an injected policy. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}

## Plugin boundary

- [x] **STR-031** Test routes around permanent barriers. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-032** Test board-edge routes. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-033** Test unreachable enclosed targets. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-034** Test start-equals-target STAY behavior through Base Logic. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-035** Test repeated identical snapshots. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-036** Test fresh-process repeatability. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-037** Test no hidden opponent, scent, or language input is consumed. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-038** Test malicious diagonal and off-board outputs cannot bypass Base Logic/search. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-039** Test rejected proposal leaves state unchanged. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-040** [BLOCKED: Annex F defines a minimum grid size but no largest approved board] Measure bounded search on a formally bounded largest board. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}

## Adversarial tests

- [ ] **STR-041** [BLOCKED: STR-BQ-02] Define private strategy selector schema. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-042** [BLOCKED: STR-BQ-02] Load thief_class only from private TOML. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-043** [BLOCKED: STR-BQ-02] Reject malformed module/class references. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-044** [BLOCKED: STR-BQ-02] Require the selected class to satisfy the thief interface. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-045** [BLOCKED: STR-BQ-02] Test missing plugin and wrong-base-class failures. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-046** [BLOCKED: STR-BQ-02] Test plugin exception becomes typed decision failure. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-047** [BLOCKED: STR-BQ-02] Test plugin cannot bypass Base Logic. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-048** [BLOCKED: STR-BQ-02] Test shared JSON cannot be weakened by private strategy config. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-049** [BLOCKED: STR-BQ-01] Document the selected team algorithm if it becomes the approved default. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-050** Keep optional RL dependencies absent unless separately approved. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}

## Verification and delivery

- [x] **STR-051** Add focused positive path tests for direct, multi-turn, barrier, edge, and STAY paths. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-052** Add negative and invariant tests. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-053** [BLOCKED: STR-BQ-02] Add malicious dynamic-plugin tests after the loader contract is approved. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-054** Run full regression and dependency-boundary tests. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-055** Run uv sync, Ruff, pytest and line checker. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-056** Run credential/generated-file scans. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-057** Record exact evidence, failures, corrections, and criterion mapping. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-058** Audit TODO completion against concrete tests and retained blockers. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-059** Inspect the complete staged diff, names, statistics and whitespace. {Trace: PLAN:Cross-Stage Verification}
- [x] **STR-060** Confirm only reviewed documentation, strategy, and tests are staged; no secrets or generated files. {Trace: PLAN:Git workflow}
- [x] **STR-061** Commit only reviewed Stage 3 files. Evidence: `e01f246`. {Trace: PLAN:Git workflow}
- [x] **STR-062** Push the dedicated Stage 3 branch without creating a PR. Evidence: `origin/feat/stage-3-blind-strategy`. {Trace: PLAN:Git workflow}
- [ ] **STR-063** Open a focused Stage 3 Pull Request. {Trace: PLAN:Git workflow}
- [x] **STR-064** Record the ADR-002 owner-approved Codex adversarial review; independent human reviewer: None. {Trace: PLAN:Review Policy; PLAN:Stage 3 gate}
- [ ] **STR-065** Record PASS only after merge and synchronization; otherwise FAIL. {Trace: PDF:Ch10.4; PLAN:Stage 3 gate}
