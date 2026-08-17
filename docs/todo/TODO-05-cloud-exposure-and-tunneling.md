# TODO 05 - Cloud Exposure and Tunneling

**Status:** Ready for review
**Related PRD:** `../prd/PRD-05-cloud-exposure-and-tunneling.md`
**Implementation:** Not started
**Task ID range:** CLD-001 through CLD-065

All tasks are unchecked. A task may be checked only when its evidence exists. Items that depend on a PRD blocked question remain non-executable until the decision is approved.

**Trace legend:** tunnel/separation -> PDF Ch2.4/E1-2/10; milestone -> Ch10.3.5; timeouts -> Annex F 19; acceptance -> PRD-05 AC05.

## Authority and external actions

- [ ] **CLD-001** Reconfirm PRD-05 mapping against Chapters 2.4 and 10.3.5 and Appendix E 1-2/10. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-002** [BLOCKED: CLD-BQ-01..05] Resolve or retain every cloud blocker. {Trace: PRD-05; PLAN:Stage 5; PDF:Ch2.4}
- [ ] **CLD-003** [BLOCKED: CLD-BQ-01] Approve tunnel provider without assuming ngrok. {Trace: PRD-05; PLAN:Stage 5; PDF:Ch2.4}
- [ ] **CLD-004** Document required external account and operator permissions. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-005** [BLOCKED: CLD-BQ-02] Approve public URL exchange mechanism. {Trace: PRD-05; PLAN:Stage 5; PDF:Ch2.4}
- [ ] **CLD-006** [BLOCKED: CLD-BQ-03] Approve reconnect/resume versus technical-loss policy. {Trace: PRD-05; PLAN:Stage 5; PDF:Ch8.4}
- [ ] **CLD-007** [BLOCKED: CLD-BQ-04] Approve provider-outage attribution policy. {Trace: PRD-05; PLAN:Stage 5; PDF:Ch8.4}
- [ ] **CLD-008** Map acceptance criteria to remote tests. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-009** Document Stage 6 authentication exclusion. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-010** Approve binary Stage 5 gate. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}

## Tunnel abstraction

- [ ] **CLD-011** Define tunnel-provider interface. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-012** Keep provider adapter outside deterministic/strategy packages. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-013** Load tunnel credentials only from ignored private environment/config. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-014** Load public/private endpoint values through typed configuration. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-015** Validate URL scheme, host and path. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-016** Reject localhost endpoint in remote-mode acceptance. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-017** Redact credentials/query secrets from endpoint display. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-018** Define start/stop/health lifecycle. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-019** Define public endpoint readiness result. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-020** Keep all Python files under 150 lines. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}

## Remote lifecycle

- [ ] **CLD-021** Implement selected provider start adapter. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-022** Capture assigned public URL safely. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-023** Expose thief FastMCP endpoint. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-024** Connect thief client to remote cop endpoint. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-025** Verify symmetric server/client reachability. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-026** Add health check before match start. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-027** Close tunnels during controlled shutdown. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-028** Prevent orphan tunnel process. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-029** Record provider version and nonsecret settings. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-030** Write operator startup/shutdown runbook. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}

## Failure handling

- [ ] **CLD-031** Apply agreed response timeout. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-032** Apply agreed watchdog timeout. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-033** Bound connection retries and backoff. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-034** Handle DNS resolution failure. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-035** Handle TLS/certificate failure. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-036** Handle expired/rotated tunnel URL. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-037** Handle mid-request disconnect. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-038** Handle high latency and timeout. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-039** Handle provider process crash. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-040** Handle reconnect only per approved policy. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}

## Security tests

- [ ] **CLD-041** Test remote failure never hangs. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-042** Test local failure is distinguishable from peer failure where possible. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-043** Test retry exhaustion produces one outcome. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-044** Test shutdown persists required state. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-045** Test endpoint logs contain no secrets. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-046** Run two-machine thief-to-cop call. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-047** Run two-machine cop-to-thief call. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-048** Run complete remote match. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-049** Repeat remote fixture after tunnel restart. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-050** Capture latency/failure evidence without credentials. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}

## Verification and delivery

- [ ] **CLD-051** Run contract regression against localhost. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-052** Run unit/integration/negative/repeatability tests. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-053** Run uv sync, Ruff, pytest and line checker. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-054** Run credential and generated-artifact scans. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-055** Review external-action evidence and redactions. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-056** Record exact commands/versions/exits. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-057** Audit TODO and PRD traceability. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-058** Inspect staged diff and unrelated files. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-059** Confirm no tunnel token, private URL or unrelated file is staged. {Trace: PLAN:Git workflow}
- [ ] **CLD-060** Record the complete staged-diff audit. {Trace: PLAN:Cross-Stage Verification}
- [ ] **CLD-061** Commit only reviewed Stage 5 files. {Trace: PLAN:Git workflow}
- [ ] **CLD-062** Push the dedicated Stage 5 branch. {Trace: PLAN:Git workflow}
- [ ] **CLD-063** Open a focused Stage 5 Pull Request. {Trace: PLAN:Git workflow}
- [ ] **CLD-064** Obtain independent review when available or record the ADR-002 owner-approved Codex review exception. {Trace: PLAN:Review Policy; PLAN:Stage 5 gate}
- [ ] **CLD-065** Record PASS only after merge and synchronization; otherwise FAIL. {Trace: PDF:Ch10.4; PLAN:Stage 5 gate}
