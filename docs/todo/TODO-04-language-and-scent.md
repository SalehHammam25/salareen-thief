# TODO 04 - Language and Scent

**Status:** Unblocked subset implemented; six specification blockers retained
**Related PRD:** `../prd/PRD-04-language-and-scent.md`
**Implementation:** In progress; blocked scent evolution and belief work excluded
**Task ID range:** LST-001 through LST-065

A task is checked only when its evidence exists. Blocked items remain non-executable until an approved decision resolves the cited PRD question.

**Trace legend:** scent/belief -> PDF Ch4/Ch6.4; language -> Ch6.5/E25-27; milestone -> Ch10.3.4; values -> Annex F 14/16/18/21; acceptance -> PRD-04 AC04.

## Authority and blocked design

- [x] **LST-001** Reconfirm PRD-04 mapping against Chapters 4, 6, Appendix E 25-27 and Annex F 14/16/18/21. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-002** Retain and document all six language/scent blockers without assumptions. Evidence: ADR-005. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch4/Ch6}
- [ ] **LST-003** [BLOCKED: LS-BQ-01] Approve spatial falloff formula. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch4.3}
- [ ] **LST-004** [BLOCKED: LS-BQ-02] Approve overlap aggregation rule. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch4.3}
- [ ] **LST-005** [BLOCKED: LS-BQ-03] Approve emission/decay/movement ordering. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch4.3}
- [ ] **LST-006** [BLOCKED: LS-BQ-04] Approve edge clipping behavior. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch4.3}
- [ ] **LST-007** [BLOCKED: LS-BQ-05] Approve numeric-language policy. {Trace: PRD-04; PLAN:Stage 4; PDF:E26-27}
- [ ] **LST-008** [BLOCKED: LS-BQ-06] Approve belief prior and hint reliability model. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch6.4}
- [x] **LST-009** Record all private provider modes from Annex F Table 21 in ADR-005 and typed configuration. {Trace: PRD-04; PLAN:Stage 4; PDF:Annex F 21}
- [x] **LST-010** Map every currently executable acceptance criterion to Stage 4 tests and evidence. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}

## Scent model

- [x] **LST-011** Create scent package independent from strategy legality. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-012** Define immutable scent-grid value type. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-013** Load fixed center intensity 0.9. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-014** Load fixed decay rate 0.10. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-015** Load fixed 5x5 field size. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-016** Reject fixed-value deviations and bool-as-number. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-017** [BLOCKED: LS-BQ-01..04] Emit scent for movement. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-018** [BLOCKED: LS-BQ-01..04] Emit scent for STAY. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-019** [BLOCKED: LS-BQ-01] Apply approved spatial falloff. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-020** [BLOCKED: LS-BQ-02..03] Apply permanent per-turn decay deterministically. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}

## Belief and language

- [ ] **LST-021** [BLOCKED: LS-BQ-04] Clip scent window at board boundaries per approved decision. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-022** [BLOCKED: LS-BQ-02] Aggregate overlapping trails per approved decision. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-023** Prevent negative/non-finite scent values. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-024** Expose only opponent scent through the immutable peer observation contract. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-025** [BLOCKED: LS-BQ-01/04] Test center, neighbor, corner and boundary emissions. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-026** [BLOCKED: LS-BQ-02/03] Test multi-turn decay with exact values. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-027** [BLOCKED: LS-BQ-02] Test overlapping trail arithmetic. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-028** [BLOCKED: LS-BQ-01..04] Test repeated/fresh-process scent equality. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-029** [BLOCKED: LS-BQ-06] Define normalized thief belief map. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-030** [BLOCKED: LS-BQ-06] Initialize approved prior without objective cop position. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}

## Provider boundary

- [ ] **LST-031** [BLOCKED: LS-BQ-06] Update belief from cop scent. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-032** [BLOCKED: LS-BQ-05/06] Update belief from accepted hint. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-033** [BLOCKED: LS-BQ-06] Normalize after every update. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-034** [BLOCKED: LS-BQ-06] Handle zero-likelihood evidence explicitly. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-035** [BLOCKED: LS-BQ-06] Prevent objective position leakage in strategy/GUI DTOs. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-036** [BLOCKED: LS-BQ-06] Test belief conservation and bounds. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-037** [BLOCKED: LS-BQ-06] Test adversarial/outlier evidence. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-038** Define versioned free-language hint message. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-039** Reject unmistakable direct numeric-coordinate protocol forms while retaining LS-BQ-05. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-040** Enforce negotiated hint word limit. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}

## Security and tests

- [x] **LST-041** Load negotiated map area. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-042** Define self-declared/unverified truth/lie classification without crypto proof. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-043** Parse hints as untrusted text. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-044** Test Unicode, empty, oversized and malformed hints. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-045** [BLOCKED: LS-BQ-05] Test comprehensive coordinate-smuggling examples after policy approval. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-046** Define provider-independent verbal interface. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-047** Implement deterministic template fallback. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-048** Keep provider/model choices in private config. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-049** Implement every_n_steps gating. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-050** Track actual request/response token consumption. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}

## Verification and delivery

- [x] **LST-051** Enforce negotiated series token budget. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-052** Bound provider latency and preserve caller cancellation. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-053** Prevent LLM output from selecting/applying moves. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-054** Test prompt injection cannot cross deterministic boundary. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-055** Test unavailable/rate-limited provider fallback. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-056** Run unit, integration, negative, security and repeatability tests. Evidence: Stage 4 verification. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-057** Run uv sync, Ruff, pytest and line checker. Evidence: Stage 4 verification. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-058** Run credential/dependency scans and verify <=150 lines. Evidence: Stage 4 verification. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-059** Record exact commands, versions, exits, failures and corrections. Evidence: Stage 4 verification. {Trace: PLAN:Cross-Stage Verification}
- [x] **LST-060** Inspect the 20-file staged diff; whitespace and credential scans passed with no unrelated files. {Trace: PLAN:Git workflow}
- [x] **LST-061** Commit only the 20 reviewed Stage 3 closeout and Stage 4 files. Evidence: `0c6b2ec`. {Trace: PLAN:Git workflow}
- [x] **LST-062** Push the dedicated Stage 4 branch and establish upstream tracking. Evidence: `origin/feat/stage-4-language-scent`. {Trace: PLAN:Git workflow}
- [ ] **LST-063** Open a focused Stage 4 Pull Request. {Trace: PLAN:Git workflow}
- [x] **LST-064** Record ADR-002 owner-approved Codex review; independent human reviewer: None. {Trace: PLAN:Review Policy; PLAN:Stage 4 gate}
- [ ] **LST-065** Record PASS only after merge and synchronization; otherwise FAIL. {Trace: PDF:Ch10.4; PLAN:Stage 4 gate}
