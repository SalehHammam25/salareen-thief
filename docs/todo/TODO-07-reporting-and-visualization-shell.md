# TODO 07 - Reporting and Visualization Shell

**Status:** Ready for review
**Related PRD:** `../prd/PRD-07-reporting-and-visualization-shell.md`
**Implementation:** Not started
**Task ID range:** REP-001 through REP-065

All tasks are unchecked. A task may be checked only when its evidence exists. Items that depend on a PRD blocked question remain non-executable until the decision is approved.

**Trace legend:** GUI/replay -> PDF Ch7/E8-9/20; league/reporting -> Ch9/E28-38/51-55; OAuth -> Appendix A; submission -> Appendix C/E39-50; values -> Annex F 17-20; acceptance -> PRD-07 AC07.

## Authority and schemas

- [ ] **REP-001** Reconfirm PRD-07 against Chapters 7/9, Appendices A/C/E and Annex F. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-002** [BLOCKED: REP-BQ-01..07] Resolve or retain every reporting blocker. {Trace: PRD-07; PLAN:Stage 7; PDF:Ch7/Ch9}
- [ ] **REP-003** [BLOCKED: REP-BQ-01] Approve declaration/config/log/result schemas. {Trace: PRD-07; PLAN:Stage 7; PDF:Ch9.3.3/F20}
- [ ] **REP-004** [BLOCKED: REP-BQ-04] Approve game_id/game_uid derivation. {Trace: PRD-07; PLAN:Stage 7; PDF:Ch9.3.3/F20}
- [ ] **REP-005** [BLOCKED: REP-BQ-02] Approve Gmail subject/body/idempotency contract. {Trace: PRD-07; PLAN:Stage 7; PDF:Ch9.3}
- [ ] **REP-006** [BLOCKED: REP-BQ-03] Approve GUI toolkit and accessibility baseline. {Trace: PRD-07; PLAN:Stage 7; PDF:Ch7.3}
- [ ] **REP-007** Document external Google/submission actions. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-008** Map all acceptance criteria to tests/evidence. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-009** Document local-truth privacy boundary. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-010** Approve final binary project gate. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}

## Live GUI and replay

- [ ] **REP-011** Define read-only local GUI view model. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-012** Display thief position/local barriers only as locally known. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-013** Display thief belief heatmap. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-014** Display YOUR TURN and LOCKED states. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-015** Disable action input while locked. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-016** Prevent objective cop position/global board exposure. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-017** Drive UI updates from orchestrator events. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-018** Test local-truth leakage adversarially. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-019** Capture required belief-map screenshot. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-020** Keep GUI modules under 150 lines. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}

## League accounting

- [ ] **REP-021** Load final game log in replay viewer. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-022** Recompute every complete commitment. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-023** Show Verified OK only after all steps verify. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-024** Show TAMPERED on first mismatch. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-025** Disqualify tampered match without override. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-026** Provide forward/backward step controls. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-027** Keep replay deterministic and read-only. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-028** Test every-field tamper and truncated log. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-029** Capture required Verified OK screenshot. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-030** Keep replay responsibility outside production game rules. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}

## Gmail and Gatekeeper

- [ ] **REP-031** [BLOCKED: REP-BQ-07] Enforce fixed six games per opponent series. {Trace: PRD-07; PLAN:Stage 7; PDF:Annex F 18}
- [ ] **REP-032** [BLOCKED: REP-BQ-07] Count one scored game per opponent. {Trace: PRD-07; PLAN:Stage 7; PDF:Appendix E 52}
- [ ] **REP-033** Keep warm-ups uncounted. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-034** Enforce diversity reward 10. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-035** Enforce minimum two different-team games. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-036** Enforce maximum ten games per team. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-037** Apply fixed tie score 2 to aggregate ties. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-038** Declare actual counted games truthfully. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-039** Reject contradictory peer results. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-040** Require both peers' independent agreeing reports. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}

## Submission artifacts

- [ ] **REP-041** Define declaration_<game_id>.json validation. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-042** Reuse signed config_<game_id>_g<NN>.json. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-043** Define log_<game_id>_g<NN>.json validation. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-044** Define result_<game_id>.json validation. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-045** Include both repositories and exact commits. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-046** Include per-game and series token totals. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-047** Use Annex F reporting email address. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-048** Enable Gmail API through authorized external action. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-049** Configure OAuth consent/test users. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-050** Request gmail.send scope only. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}

## Final verification and delivery

- [ ] **REP-051** Create credentials.json/token.json outside Git. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-052** Verify both secret files are ignored. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-053** Build JSON attachment-only report sender. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-054** Implement quota manager, token bucket and DOS detector. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-055** Use Annex F rate-limit minimums and 429 backoff. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-056** Test quota exhaustion/burst/DOS/duplicate send. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-057** Send separate thief test report without exposing secrets. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-058** Verify both repositories are accessible/cross-linked. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-059** Complete academic README requirements and screenshots. {Trace: PRD-07; PLAN:Stage 7; PDF:applicable authority}
- [ ] **REP-060** Run all tests/checks and record final evidence before staging. {Trace: PLAN:Cross-Stage Verification}
- [ ] **REP-061** Inspect staged diff and prove no OAuth secret/unrelated file is staged. {Trace: PLAN:Git workflow}
- [ ] **REP-062** Commit and push only reviewed Stage 7 files. {Trace: PLAN:Git workflow}
- [ ] **REP-063** Open a focused Stage 7 Pull Request and obtain independent review. {Trace: PLAN:Git workflow}
- [ ] **REP-064** After merge, create/push the reviewed annotated submission tag. {Trace: PDF:Appendix C}
- [ ] **REP-065** Record final binary project PASS only when every submission gate is true. {Trace: PDF:Ch10.4/Appendix C; PLAN:Stage 7 gate}
