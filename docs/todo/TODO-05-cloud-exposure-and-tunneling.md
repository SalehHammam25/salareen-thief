# TODO 05 - Cloud Exposure and Tunneling

**Status:** Safe local subset verified; external tunnel acceptance blocked
**Related PRD:** `../prd/PRD-05-cloud-exposure-and-tunneling.md`
**Implementation:** Local lifecycle complete; external provider/machines pending
**Task ID range:** CLD-001 through CLD-065

All tasks are unchecked. A task may be checked only when its evidence exists. Items that depend on a PRD blocked question remain non-executable until the decision is approved.

**Trace legend:** tunnel/separation -> PDF Ch2.4/E1-2/10; milestone -> Ch10.3.5; timeouts -> Annex F 19; acceptance -> PRD-05 AC05.

## Authority and external actions

- [x] **CLD-001** Reconfirm mapping against Chapters 2.4/8.4/10.3.5, Appendix E 1-2/10, and Annex F 19. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-002** Retain every external cloud blocker without assumptions. Evidence: ADR-007. {Trace: PRD-05; PLAN:Stage 5; PDF:Ch2.4}
- [ ] **CLD-003** [BLOCKED: CLD-BQ-01] Approve tunnel provider without assuming ngrok. {Trace: PRD-05; PLAN:Stage 5; PDF:Ch2.4}
- [x] **CLD-004** Document required external account and operator permissions. Evidence: Stage 5 runbook. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-005** [BLOCKED: CLD-BQ-02] Approve public URL exchange mechanism. {Trace: PRD-05; PLAN:Stage 5; PDF:Ch2.4}
- [ ] **CLD-006** [BLOCKED: CLD-BQ-03] Approve reconnect/resume versus technical-loss policy. {Trace: PRD-05; PLAN:Stage 5; PDF:Ch8.4}
- [ ] **CLD-007** [BLOCKED: CLD-BQ-04] Approve provider-outage attribution policy. {Trace: PRD-05; PLAN:Stage 5; PDF:Ch8.4}
- [x] **CLD-008** Map local and external acceptance criteria to tests/runbook evidence. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-009** Document Stage 6 authentication exclusion. Evidence: ADR-007/runbook. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-010** Retain binary gate: local PASS cannot replace remote-machine proof. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}

## Tunnel abstraction

- [x] **CLD-011** Define tunnel-provider interface. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-012** Keep cloud lifecycle outside deterministic/strategy packages. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-013** Load tunnel credentials only from private environment mapping. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-014** Load opponent endpoint and local settings through typed configuration. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-015** Validate URL scheme, host, port, userinfo, fragment and path. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-016** Reject localhost/private endpoint in remote-mode acceptance. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-017** Redact credentials, fragments and secret query values. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-018** Define start/stop/health lifecycle. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-019** Define typed public endpoint readiness result. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-020** Keep all Python files under 150 lines. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}

## Remote lifecycle

- [ ] **CLD-021** [BLOCKED: CLD-BQ-01/05] Implement selected provider start adapter. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-022** Capture and validate provider-assigned public URL safely through `TunnelReady`. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-023** [BLOCKED: CLD-BQ-01/05] Expose thief FastMCP endpoint through a real public tunnel. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-024** Inject and validate a remote cop endpoint for the existing MCP client. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-025** [BLOCKED: CLD-BQ-05] Verify symmetric server/client reachability on two machines. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-026** Add provider readiness and health checks before match start. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-027** Close tunnels during controlled shutdown. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-028** Prevent orphan tunnel process through idempotent stop/context management. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-029** [BLOCKED: CLD-BQ-01/05] Record actual provider version and nonsecret settings. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-030** Write credential-safe operator startup/shutdown runbook. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}

## Failure handling

- [x] **CLD-031** Apply negotiable response timeout with Annex F default 30 seconds. {Trace: PRD-05; PLAN:Stage 5; PDF:Annex F 19}
- [x] **CLD-032** Apply negotiable watchdog timeout with Annex F default 60 seconds. {Trace: PRD-05; PLAN:Stage 5; PDF:Annex F 19}
- [x] **CLD-033** Bound connection retries and backoff. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-034** Classify DNS resolution failure. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-035** Classify TLS/certificate failure. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-036** [BLOCKED: CLD-BQ-02/03] Handle expired/rotated tunnel URL in a live exchange. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-037** Classify mid-request disconnect without leaking details. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-038** Bound high latency with timeout and retry exhaustion. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-039** Surface provider process crash through health result. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-040** [BLOCKED: CLD-BQ-03] Handle reconnect only per approved policy. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}

## Security tests

- [x] **CLD-041** Test fake remote failures and latency never hang. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-042** Test stable known and unknown attribution categories where possible. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-043** Test retry exhaustion produces one deterministic result. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-044** [BLOCKED: CLD-BQ-03] Test shutdown persistence after reconnect policy approval. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-045** Test endpoint diagnostics contain no userinfo/query secrets. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-046** [BLOCKED: CLD-BQ-05] Run two-machine thief-to-cop call. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-047** [BLOCKED: CLD-BQ-05] Run two-machine cop-to-thief call. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-048** [BLOCKED: CLD-BQ-01/05] Run complete remote match. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [ ] **CLD-049** [BLOCKED: CLD-BQ-02/03/05] Repeat remote fixture after tunnel restart. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-050** Capture fake latency/failure evidence without credentials. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}

## Verification and delivery

- [x] **CLD-051** Run complete localhost contract regression. Evidence: Stage 5 verification, 398 passing tests. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-052** Run unit/integration/negative/repeatability tests using deterministic fakes. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-053** Run uv sync, Ruff, pytest and line checker. Evidence: Stage 5 verification. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-054** Run credential, isolation, and generated-artifact scans. Evidence: Stage 5 verification. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-055** Review absent external evidence and verify redaction behavior locally. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-056** Record exact commands, versions, exits, failures, and corrections. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-057** Audit TODO and PRD traceability against local/external evidence. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-058** Inspect the complete 22-file staged diff and unrelated files. {Trace: PRD-05; PLAN:Stage 5; PDF:applicable authority}
- [x] **CLD-059** Confirm no tunnel token, private URL, generated artifact, or unrelated file is staged. {Trace: PLAN:Git workflow}
- [x] **CLD-060** Record cached names/statistics/whitespace and credential audit. {Trace: PLAN:Cross-Stage Verification}
- [x] **CLD-061** Commit only the 22 reviewed Stage 4 closeout and Stage 5 files. Evidence: `ea4a053`. {Trace: PLAN:Git workflow}
- [x] **CLD-062** Push and track `origin/feat/stage-5-cloud-tunneling`. {Trace: PLAN:Git workflow}
- [ ] **CLD-063** Open a focused Stage 5 Pull Request. {Trace: PLAN:Git workflow}
- [x] **CLD-064** Record ADR-002 owner-approved Codex adversarial review; independent human reviewer: None. {Trace: PLAN:Review Policy; PLAN:Stage 5 gate}
- [ ] **CLD-065** Record PASS only after merge and synchronization; otherwise FAIL. {Trace: PDF:Ch10.4; PLAN:Stage 5 gate}
