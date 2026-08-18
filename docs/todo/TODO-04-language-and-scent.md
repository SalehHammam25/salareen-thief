# TODO 04 - Language and Scent

**Status:** Complete; final Stage 4 gate PASS
**Related PRD:** `../prd/PRD-04-language-and-scent.md`
**Implementation:** Complete before Pull Request
**Task ID range:** LST-001 through LST-065

A task is checked only when its evidence exists. Blocked items remain non-executable until an approved decision resolves the cited PRD question.

**Trace legend:** scent/belief -> PDF Ch4/Ch6.4; language -> Ch6.5/E25-27; milestone -> Ch10.3.4; values -> Annex F 14/16/18/21; acceptance -> PRD-04 AC04.

## Authority and blocked design

- [x] **LST-001** Reconfirm PRD-04 mapping against Chapters 4, 6, Appendix E 25-27 and Annex F 14/16/18/21. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-002** Resolve all six former language/scent blockers through explicit owner approval. Evidence: ADR-006. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch4/Ch6}
- [x] **LST-003** Approve exact-decimal Chebyshev spatial falloff. Evidence: ADR-006. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch4.3}
- [x] **LST-004** Approve cell-wise maximum overlap aggregation. Evidence: ADR-006. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch4.3}
- [x] **LST-005** Approve transition, decay, emission, maximum, clipping, publication order. Evidence: ADR-006. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch4.3}
- [x] **LST-006** Approve clipping without wrap, reflection, or renormalization. Evidence: ADR-006. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch4.3}
- [x] **LST-007** Approve deterministic numeric-language policy. Evidence: ADR-006. {Trace: PRD-04; PLAN:Stage 4; PDF:E26-27}
- [x] **LST-008** Approve exact belief prior, likelihood, and reliability model. Evidence: ADR-006. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch6.4}
- [x] **LST-009** Record all private provider modes from Annex F Table 21 in ADR-005 and typed configuration. {Trace: PRD-04; PLAN:Stage 4; PDF:Annex F 21}
- [x] **LST-010** Map every currently executable acceptance criterion to Stage 4 tests and evidence. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}

## Scent model

- [x] **LST-011** Create scent package independent from strategy legality. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-012** Define immutable scent-grid value type. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-013** Load fixed center intensity 0.9. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-014** Load fixed decay rate 0.10. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-015** Load fixed 5x5 field size. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-016** Reject fixed-value deviations and bool-as-number. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-017** Emit scent for accepted movement. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority; ADR-006}
- [x] **LST-018** Emit scent for accepted STAY. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority; ADR-006}
- [x] **LST-019** Apply exact-decimal Chebyshev spatial falloff. {Trace: PRD-04; PLAN:Stage 4; ADR-006}
- [x] **LST-020** Apply permanent per-turn decay deterministically. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch4.3; ADR-006}

## Belief and language

- [x] **LST-021** Clip scent at board boundaries without renormalization. {Trace: PRD-04; PLAN:Stage 4; ADR-006}
- [x] **LST-022** Aggregate overlaps by order-independent maximum. {Trace: PRD-04; PLAN:Stage 4; ADR-006}
- [x] **LST-023** Prevent negative/non-finite scent values. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-024** Expose only opponent scent through the immutable peer observation contract. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-025** Test center, rings, edge, corner and clipped emissions. {Trace: PRD-04; PLAN:Stage 4; ADR-006}
- [x] **LST-026** Test exact decay and turn ordering. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch4.3; ADR-006}
- [x] **LST-027** Test maximum overlap arithmetic and order independence. {Trace: PRD-04; PLAN:Stage 4; ADR-006}
- [x] **LST-028** Test repeated and fresh-process scent equality. {Trace: PRD-04; PLAN:Stage 4; ADR-006}
- [x] **LST-029** Define immutable normalized thief belief map. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch6.4; ADR-006}
- [x] **LST-030** Initialize uniform prior without objective cop position. {Trace: PRD-04; PLAN:Stage 4; ADR-006}

## Provider boundary

- [x] **LST-031** Update belief from opponent scent with monotonic exact weights. {Trace: PRD-04; PLAN:Stage 4; ADR-006}
- [x] **LST-032** Validate hints before supported qualitative belief updates. {Trace: PRD-04; PLAN:Stage 4; ADR-006}
- [x] **LST-033** Normalize deterministically after every evidence update. {Trace: PRD-04; PLAN:Stage 4; ADR-006}
- [x] **LST-034** Preserve previous belief with typed fallback on zero/invalid weight. {Trace: PRD-04; PLAN:Stage 4; ADR-006}
- [x] **LST-035** Prevent objective position leakage in belief and strategy DTOs. {Trace: PRD-04; PLAN:Stage 4; PDF:Ch6.4}
- [x] **LST-036** Test belief conservation, bounds, and impossible cells. {Trace: PRD-04; PLAN:Stage 4; ADR-006}
- [x] **LST-037** Test neutral unknown, conflicting, and invalid evidence. {Trace: PRD-04; PLAN:Stage 4; ADR-006}
- [x] **LST-038** Define versioned free-language hint message. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-039** Reject unmistakable direct numeric-coordinate protocol forms while retaining LS-BQ-05. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-040** Enforce negotiated hint word limit. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}

## Security and tests

- [x] **LST-041** Load negotiated map area. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-042** Define self-declared/unverified truth/lie classification without crypto proof. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-043** Parse hints as untrusted text. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-044** Test Unicode, empty, oversized and malformed hints. {Trace: PRD-04; PLAN:Stage 4; PDF:applicable authority}
- [x] **LST-045** Test Unicode digits, numeric tokens, coordinate words/forms, chess coordinates, and qualitative acceptance. {Trace: PRD-04; PLAN:Stage 4; ADR-006}
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
- [x] **LST-061** Commit only reviewed Stage 4 files. Evidence: initial `0c6b2ec`; finalization `77af8b7`. {Trace: PLAN:Git workflow}
- [x] **LST-062** Push both reviewed deliveries to `origin/feat/stage-4-language-scent`. {Trace: PLAN:Git workflow}
- [x] **LST-063** Open and merge focused Stage 4 PR #12 as `48d24e6`. {Trace: PLAN:Git workflow}
- [x] **LST-064** Record ADR-002 owner-approved Codex review; independent human reviewer: None. {Trace: PLAN:Review Policy; PLAN:Stage 4 gate}
- [x] **LST-065** Record PASS after PR #12 merge, ancestor verification for `77af8b7`/`c2f8e50`, fast-forward synchronization, and clean `main`. {Trace: PDF:Ch10.4; PLAN:Stage 4 gate}

## Live-match composition backlog

- [ ] **LM-LSB-001** Connect accepted movement/STAY to scent decay/emission exactly once; exclude rejected and barrier actions.
- [ ] **LM-LSB-002** Implement versioned scent observation and language hint transport adapters.
- [ ] **LM-LSB-003** Apply scent before language evidence and expose the result only to the next thief strategy invocation.
- [ ] **LM-LSB-004** Test coordinate prohibition, provider fallback and token accounting inside complete turns.
- [ ] **LM-LSB-005** Add byte-identical Stage 4 turn fixtures and cross-process ordering tests.
