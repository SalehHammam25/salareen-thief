# TODO 03 - Blind Strategy

**Status:** Ready for review
**Related PRD:** `../prd/PRD-03-blind-strategy.md`
**Implementation:** Not started
**Task ID range:** STR-001 through STR-065

All tasks are unchecked. A task may be checked only when its evidence exists. Items that depend on a PRD blocked question remain non-executable until the decision is approved.

**Trace legend:** policy -> PDF Ch6; milestone -> Ch10.3.3-10.4; LLM boundary -> Appendix E 25; selector -> Annex F 22; acceptance -> PRD-03 AC03.

## Documentation and decisions

- [ ] **STR-001** Reconfirm PRD-03 mapping against Chapter 6, Chapter 10 and Annex F 22. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-002** [BLOCKED: STR-BQ-01..03] Resolve or retain all strategy blockers. {Trace: PRD-03; PLAN:Stage 3; PDF:Ch6}
- [ ] **STR-003** [BLOCKED: STR-BQ-01] Approve the thief default strategy path. {Trace: PRD-03; PLAN:Stage 3; PDF:Ch6.3}
- [ ] **STR-004** [BLOCKED: STR-BQ-03] Approve deterministic equal-cost tie-breaking. {Trace: PRD-03; PLAN:Stage 3; PDF:Ch6.4}
- [ ] **STR-005** [BLOCKED: STR-BQ-02] Approve plugin import/fallback contract. {Trace: PRD-03; PLAN:Stage 3; PDF:Annex F 22}
- [ ] **STR-006** Map all acceptance criteria to tests. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-007** Document why Q-learning is optional. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-008** Document Stage 4 language/scent exclusions. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-009** Define strategy performance budget without changing game rules. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-010** Approve binary Stage 3 gate. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}

## Strategy architecture

- [ ] **STR-011** Create strategy package separate from base_logic. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-012** Define immutable strategy input snapshot. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-013** Define typed proposed-action result. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-014** Define typed no-route/decision failure. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-015** Require Base Logic validation after every proposal. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-016** Prevent strategy from mutating GameState. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-017** Prevent strategy from importing transport internals. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-018** Prevent deterministic rules from importing strategy. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-019** Define dependency-injected deterministic tie policy. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-020** Keep each Python file within 150 lines. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}

## Blind policy

- [ ] **STR-021** Implement legal-action enumeration through Base Logic interfaces. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-022** Implement known-target distance evaluation. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-023** Implement shortest legal path for orthogonal geometry. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-024** Exclude barriers and off-board cells from search. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-025** Handle STAY only under approved policy. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-026** Return explicit unreachable result. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-027** Return explicit terminal-state result. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-028** Choose deterministic first step on equal routes. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-029** Test a direct one-step target. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-030** Test multi-turn shortest-route milestone. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}

## Plugin boundary

- [ ] **STR-031** Test routes around permanent barriers. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-032** Test board-edge routes. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-033** Test unreachable enclosed targets. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-034** Test start-equals-target behavior through Base Logic. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-035** Test repeated identical snapshots. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-036** Test fresh-process repeatability. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-037** Test no hidden scent/language input is consumed. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-038** Test strategy cannot create illegal diagonal/off-board actions. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-039** Test rejected proposal leaves state unchanged. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-040** Measure bounded search on largest approved test board. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}

## Adversarial tests

- [ ] **STR-041** Define private strategy selector schema. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-042** Load thief_class only from private TOML. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-043** Reject malformed module/class references. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-044** Require the selected class to satisfy the thief interface. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-045** Test missing plugin and wrong-base-class failures. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-046** Test plugin exception becomes typed decision failure. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-047** Test plugin cannot bypass Base Logic. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-048** Test shared JSON cannot be weakened by private strategy config. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-049** Document team algorithm if not the default heuristic. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-050** Keep optional RL dependencies absent unless separately approved. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}

## Verification and delivery

- [ ] **STR-051** Add table-driven positive path tests. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-052** Add negative and invariant tests. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-053** Add malicious-plugin tests. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-054** Run full regression and dependency-boundary tests. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-055** Run uv sync, Ruff, pytest and line checker. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-056** Run credential/generated-file scans. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-057** Record exact evidence and criterion mapping. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-058** Audit TODO completion against concrete tests. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [ ] **STR-059** Inspect the complete staged diff, names, statistics and whitespace. {Trace: PLAN:Cross-Stage Verification}
- [ ] **STR-060** Confirm no secrets, generated files or unrelated changes are staged. {Trace: PLAN:Git workflow}
- [ ] **STR-061** Commit only reviewed Stage 3 files. {Trace: PLAN:Git workflow}
- [ ] **STR-062** Push the dedicated Stage 3 branch. {Trace: PLAN:Git workflow}
- [ ] **STR-063** Open a focused Stage 3 Pull Request. {Trace: PLAN:Git workflow}
- [ ] **STR-064** Obtain independent strategy/boundary review. {Trace: PLAN:Stage 3 gate}
- [ ] **STR-065** Record PASS only after merge and synchronization; otherwise FAIL. {Trace: PDF:Ch10.4; PLAN:Stage 3 gate}
