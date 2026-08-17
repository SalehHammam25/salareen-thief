# TODO 03 - Blind Strategy

**Status:** Complete; final Stage 3 gate PASS
**Related PRD:** `../prd/PRD-03-blind-strategy.md`
**Implementation:** Complete; delivery tasks remain
**Task ID range:** STR-001 through STR-065

Checked tasks have evidence in `../verification/stage-3-blind-strategy.md`. Items that depend on a PRD blocked question remain non-executable until the decision is approved.

**Trace legend:** policy -> PDF Ch6; milestone -> Ch10.3.3-10.4; LLM boundary -> Appendix E 25; selector -> Annex F 22; acceptance -> PRD-03 AC03.

## Documentation and decisions

- [x] **STR-001** Reconfirm PRD-03 mapping against Chapter 6, Chapter 10, Appendix E 25 and Annex F 22. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-002** Retain STR-BQ-01 through STR-BQ-03 without inventing defaults. {Trace: PRD-03; PLAN:Stage 3; PDF:Ch6}
- [x] **STR-003** Approve built-in `salareen_thief.strategy.blind:BlindShortestPath` as the default. {Trace: PRD-03; PLAN:Stage 3; PDF:Ch6.3; ADR-004}
- [x] **STR-004** Approve deterministic `N, S, E, W` equal-cost tie-breaking with STAY excluded. {Trace: PRD-03; PLAN:Stage 3; PDF:Ch6.4; ADR-004}
- [x] **STR-005** Approve the trusted private `module.path:ClassName` plugin seam and visible fallback. {Trace: PRD-03; PLAN:Stage 3; PDF:Annex F 22; ADR-004}
- [x] **STR-006** Map all acceptance criteria to tests and explicit blockers. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-007** Document why Q-learning is optional. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-008** Document and test Stage 4 language/scent exclusions. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-009** Bound search to at most one visit per board cell, O(N squared), without changing rules. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-010** Preserve the binary Stage 3 gate as pending until PR, merge, and synchronization. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}

## Strategy architecture

- [x] **STR-011** Create strategy package separate from base_logic. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-012** Define immutable strategy input snapshot without opponent truth or Stage 4 inputs. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-013** Define typed proposed-action result. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-014** Define typed no-route/decision failure. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-015** Require Base Logic validation after every proposal. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-016** Prevent strategy from mutating immutable GameState/snapshots. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-017** Prevent strategy from importing transport internals. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-018** Prevent deterministic rules from importing strategy. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-019** Define the approved default tie policy while retaining dependency injection for tests. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority; ADR-004}
- [x] **STR-020** Keep each Python file within 150 lines. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}

## Blind policy

- [x] **STR-021** Enumerate orthogonal actions with Base Logic movement validation. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-022** Implement known-target distance evaluation. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-023** Implement shortest legal path for orthogonal geometry. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-024** Exclude barriers and off-board cells from search. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-025** Propose STAY only when already at the known target and validate it through Base Logic. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-026** Return explicit unreachable result. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-027** Return explicit terminal-state result. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-028** Choose the first legal shortest move in configured `N, S, E, W` order. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority; ADR-004}
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
- [x] **STR-040** Prove the N-squared visited-cell bound on representative large boards without inventing a maximum or timing gate. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority; ADR-004}

## Adversarial tests

- [x] **STR-041** Define private `[strategy].thief_class` selector schema. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority; ADR-004}
- [x] **STR-042** Load `thief_class` only from trusted private TOML. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority; ADR-004}
- [x] **STR-043** Reject malformed `module.path:ClassName` references with stable typed reasons. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority; ADR-004}
- [x] **STR-044** Require no-argument construction, callable `propose`, restricted snapshots, and typed results. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority; ADR-004}
- [x] **STR-045** Test missing module/class, invalid interface, and constructor failures. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority; ADR-004}
- [x] **STR-046** Test runtime plugin exceptions produce visible typed deterministic fallback. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority; ADR-004}
- [x] **STR-047** Test invalid plugin proposals cannot bypass Base Logic and fall back visibly. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority; ADR-004}
- [x] **STR-048** Test shared JSON and remote data cannot select or weaken private strategy configuration. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority; ADR-004}
- [x] **STR-049** Record that the approved default is the built-in heuristic, so no separate team algorithm applies. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority; ADR-004}
- [x] **STR-050** Keep optional RL dependencies absent unless separately approved. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}

## Verification and delivery

- [x] **STR-051** Add focused positive path tests for direct, multi-turn, barrier, edge, and STAY paths. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-052** Add negative and invariant tests. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-053** Add malicious and incompatible plugin tests covering runtime, result, role, and Base Logic boundaries. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority; ADR-004}
- [x] **STR-054** Run full regression and dependency-boundary tests. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-055** Run uv sync, Ruff, pytest and line checker. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-056** Run credential/generated-file scans. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-057** Record exact evidence, failures, corrections, and criterion mapping. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-058** Audit TODO completion against concrete tests and retained blockers. {Trace: PRD-03; PLAN:Stage 3; PDF:applicable authority}
- [x] **STR-059** Inspect the complete staged diff, names, statistics and whitespace. {Trace: PLAN:Cross-Stage Verification}
- [x] **STR-060** Confirm only reviewed documentation, strategy, and tests are staged; no secrets or generated files. {Trace: PLAN:Git workflow}
- [x] **STR-061** Commit only reviewed Stage 3 files. Evidence: `e01f246`. {Trace: PLAN:Git workflow}
- [x] **STR-062** Push the dedicated Stage 3 branch without creating a PR. Evidence: `origin/feat/stage-3-blind-strategy`. {Trace: PLAN:Git workflow}
- [x] **STR-063** Open a focused Stage 3 Pull Request. Evidence: PR #11, merged as `f66021d`. {Trace: PLAN:Git workflow}
- [x] **STR-064** Record the ADR-002 owner-approved Codex adversarial review; independent human reviewer: None. {Trace: PLAN:Review Policy; PLAN:Stage 3 gate}
- [x] **STR-065** Record PASS after PR #11 merge, fast-forward synchronization, ancestor checks for `1dd607f` and `e01f246`, and a clean worktree. {Trace: PDF:Ch10.4; PLAN:Stage 3 gate}
