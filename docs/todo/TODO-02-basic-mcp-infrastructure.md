# TODO 02 - Basic MCP Infrastructure

**Status:** Implementation verified; merge gate pending
**Related PRD:** `../prd/PRD-02-basic-mcp-infrastructure.md`
**Implementation:** Technical slice complete; blocked and delivery tasks remain
**Task ID range:** MCP-001 through MCP-065

Checked tasks have evidence in `../verification/stage-2-mcp-infrastructure.md`. Items that depend on a PRD blocked question remain non-executable until the decision is approved.

**Trace legend:** transport -> PDF Ch2/Ch10.3.2; orchestration -> Ch8; mandatory audit -> Appendix E 1-10; values -> Annex F 19; acceptance -> PRD-02 AC02.

## Documentation and contracts

- [x] **MCP-001** Reconfirm PRD-02 authority mapping against Chapters 2, 8, Appendix E 1-10 and Annex F 19. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [ ] **MCP-002** [BLOCKED: MCP-BQ-01..03] Resolve or retain every MCP blocker. {Trace: PRD-02; PLAN:Stage 2; PDF:Ch2/Ch8}
- [ ] **MCP-003** [BLOCKED: MCP-BQ-01] Approve one cross-repository protocol version and compatibility policy. {Trace: PRD-02; PLAN:Stage 2; PDF:Ch2.3}
- [ ] **MCP-004** Approve symmetric tool names and ownership with the cop repository. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [ ] **MCP-005** Define request, acknowledgement, rejection and technical-failure vocabulary. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-006** Map every PRD-02 acceptance criterion to tests and evidence. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-007** Record Stage 2 scope exclusions in implementation review checklist. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-008** Create a shared contract-change review procedure for both repositories. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-009** Document local-truth and untrusted-message threat assumptions. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-010** Approve the binary Stage 2 gate before execution. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}

## Environment and architecture

- [x] **MCP-011** Add only reviewed FastMCP/runtime dependencies through uv. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-012** Record Python, uv, FastMCP and MCP versions in evidence. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-013** Create transport/orchestration modules separate from base_logic. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-014** Keep every new Python file at or below 150 lines. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-015** Extend dependency tests against strategy, LLM, tunnels, crypto and reporting imports. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-016** Define independent thief process entry point. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-017** Define private thief endpoint configuration boundary. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-018** Verify shared JSON overrides duplicate private agreed keys. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-019** Prove thief process cannot import or read cop runtime state. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-020** Add process lifecycle cleanup fixture with no orphan server. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}

## Schemas and codecs

- [x] **MCP-021** Define versioned geometric message envelope. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-022** Define exact integer coordinate representation and reject booleans. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-023** Define correlation identifier validation. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-024** Define deterministic acknowledgement schema. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-025** Define deterministic rejection schema and stable error codes. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-026** Reject unknown fields where contract safety requires it. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-027** Reject missing, malformed and wrong-type fields. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-028** Reject unsupported protocol versions. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-029** Define canonical test fixtures reusable by cop repository. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-030** Test encode/decode repeatability in fresh processes. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}

## FastMCP server/client

- [x] **MCP-031** Create thief FastMCP server instance. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [ ] **MCP-032** Expose the approved geometric receive tool. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-033** Create thief FastMCP client connector. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-034** Call the cop fixture server over localhost. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-035** Return acknowledgement only after schema validation. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-036** Prevent untrusted messages from mutating state before validation. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-037** Test malformed tool calls and transport exceptions. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-038** Test thief serves and calls concurrently without shared state. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-039** Test symmetric contract fixture from both roles. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-040** Record localhost end-to-end transcript without secrets. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}

## Orchestration and state machine

- [x] **MCP-041** Make orchestrator the sole public subsystem gateway. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-042** Represent approved phase states and transition table. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-043** Reject every unlisted state transition. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-044** Route inbound transport events through orchestrator. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-045** Route outbound requests through orchestrator. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-046** Prevent direct connector-to-strategy/base-logic mutation. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-047** Represent pending request and deadline immutably. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [ ] **MCP-048** Handle duplicate correlation IDs per approved decision. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-049** Test rejected/out-of-phase events preserve complete state. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-050** Test completed episode rejects ordinary transport actions. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}

## Reliability, tests and delivery

- [x] **MCP-051** Load Annex F response/watchdog values from validated config. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-052** Implement bounded retry scheduling without infinite waits. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-053** Represent retry exhaustion and watchdog expiry explicitly. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-054** Test timeout, retry success, retry exhaustion and cancellation. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-055** Run unit, integration, negative and repeatability suites. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-056** Run uv sync, Ruff, pytest and the 150-line checker. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-057** Run credential, generated-file and forbidden-dependency scans. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-058** Record exact commands, versions, exits and failures in Stage 2 evidence. {Trace: PRD-02; PLAN:Stage 2; PDF:applicable authority}
- [x] **MCP-059** Audit completed checkboxes against concrete evidence. {Trace: PRD-02; PLAN:Stage 2; PDF:Ch10.4}
- [x] **MCP-060** Inspect the complete staged diff, names, statistics and whitespace. {Trace: PLAN:Cross-Stage Verification}
- [ ] **MCP-061** Commit only the reviewed Stage 2 files on the dedicated branch. {Trace: PLAN:Git workflow}
- [ ] **MCP-062** Push the Stage 2 branch without merging it. {Trace: PLAN:Git workflow}
- [ ] **MCP-063** Open a focused Stage 2 Pull Request against main. {Trace: PLAN:Git workflow}
- [x] **MCP-064** Obtain independent review when available; otherwise record Codex adversarial review, no human reviewer, and Areen's owner approval. {Trace: PLAN:Review Policy; PLAN:Stage 2 gate}
- [ ] **MCP-065** Record binary PASS only after merge and synchronization; otherwise record FAIL. {Trace: PDF:Ch10.4; PLAN:Stage 2 gate}
