# TODO 04 - Language and Scent

**Status:** Ready for review
**Related PRD:** `../prd/PRD-04-language-and-scent.md`
**Implementation:** Not started
**Task ID range:** LST-001 through LST-065

All tasks are unchecked. A task may be checked only when its evidence exists. Items that depend on a PRD blocked question remain non-executable until the decision is approved.

**Trace legend:** scent/belief -> PDF Ch4/Ch6.4; language -> Ch6.5/E25-27; milestone -> Ch10.3.4; values -> Annex F 14/16/18/21; acceptance -> PRD-04 AC04.

## Authority and blocked design

- [ ] **LST-001** Reconfirm PRD-04 mapping against Chapters 4, 6, Appendix E 25-27 and Annex F 14/16/18/21. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-002** [BLOCKED: LS-BQ-01..06] Resolve or retain all language/scent blockers. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch4/Ch6}
- [ ] **LST-003** [BLOCKED: LS-BQ-01] Approve spatial falloff formula. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch4.3}
- [ ] **LST-004** [BLOCKED: LS-BQ-02] Approve overlap aggregation rule. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch4.3}
- [ ] **LST-005** [BLOCKED: LS-BQ-03] Approve emission/decay/movement ordering. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch4.3}
- [ ] **LST-006** [BLOCKED: LS-BQ-04] Approve edge clipping behavior. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch4.3}
- [ ] **LST-007** [BLOCKED: LS-BQ-05] Approve numeric-language policy. {Trace: PRD-04; PLAN:Stage 4; PDF:E26-27}
- [ ] **LST-008** [BLOCKED: LS-BQ-06] Approve belief prior and hint reliability model. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch6.4}
- [ ] **LST-009** Approve supported private provider modes from Annex F Table 21. {Trace: PRD-04; PLAN:Stage 4; PDF:Annex F 21}
- [ ] **LST-010** Map every acceptance criterion to evidence. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}

## Scent model

- [ ] **LST-011** Create scent package independent from strategy legality. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-012** Define immutable scent-grid value type. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-013** Load fixed center intensity 0.9. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-014** Load fixed decay rate 0.10. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-015** Load fixed 5x5 field size. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-016** Reject fixed-value deviations and bool-as-number. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-017** Emit scent for movement. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-018** Emit scent for STAY. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-019** Apply approved spatial falloff. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-020** Apply permanent per-turn decay deterministically. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}

## Belief and language

- [ ] **LST-021** Clip scent window at board boundaries per approved decision. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-022** Aggregate overlapping trails per approved decision. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-023** Prevent negative/non-finite scent values. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-024** Expose only opponent scent to each peer. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-025** Test center, neighbor, corner and boundary emissions. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-026** Test multi-turn decay with exact values. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-027** Test overlapping trail arithmetic. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-028** Test repeated/fresh-process scent equality. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-029** Define normalized thief belief map. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-030** Initialize approved prior without objective cop position. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}

## Provider boundary

- [ ] **LST-031** Update belief from cop scent. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-032** Update belief from accepted hint. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-033** Normalize after every update. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-034** Handle zero-likelihood evidence explicitly. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-035** Prevent objective position leakage in strategy/GUI DTOs. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-036** Test belief conservation and bounds. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-037** Test adversarial/outlier evidence. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-038** Define versioned free-language hint message. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-039** Reject direct numeric-coordinate protocol. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-040** Enforce negotiated hint word limit. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}

## Security and tests

- [ ] **LST-041** Load negotiated map area. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-042** Define truth/lie classification boundary without crypto proof. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-043** Parse hints as untrusted text. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-044** Test Unicode, empty, oversized and malformed hints. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-045** Test coordinate-smuggling examples after policy approval. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-046** Define provider-independent verbal interface. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-047** Implement deterministic template fallback. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-048** Keep provider/model choices in private config. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-049** Implement every_n_steps gating. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-050** Track actual request/response token consumption. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}

## Verification and delivery

- [ ] **LST-051** Enforce negotiated series token budget. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-052** Bound provider latency and cancellation. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-053** Prevent LLM output from selecting/applying moves. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-054** Test prompt injection cannot cross deterministic boundary. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-055** Test unavailable/rate-limited provider fallback. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-056** Run unit, integration, negative, security and repeatability tests. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-057** Run uv sync, Ruff, pytest and line checker. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-058** Run credential/dependency scans and verify <=150 lines. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [ ] **LST-059** Record exact commands, versions, exits, failures and corrections. {Trace: PLAN:Cross-Stage Verification}
- [ ] **LST-060** Inspect the staged diff and scan for secrets/unrelated files. {Trace: PLAN:Git workflow}
- [ ] **LST-061** Commit only reviewed Stage 4 files. {Trace: PLAN:Git workflow}
- [ ] **LST-062** Push the dedicated Stage 4 branch. {Trace: PLAN:Git workflow}
- [ ] **LST-063** Open a focused Stage 4 Pull Request. {Trace: PLAN:Git workflow}
- [ ] **LST-064** Obtain cross-peer language/scent contract review. {Trace: PLAN:Stage 4 gate}
- [ ] **LST-065** Record PASS only after merge and synchronization; otherwise FAIL. {Trace: PDF:Ch10.4; PLAN:Stage 4 gate}
