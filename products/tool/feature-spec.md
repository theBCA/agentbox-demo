# MCP Security Scanner / Agent Guardrail Kit
### Packaged tool — feature spec

**Positioning:** A sellable slice of the secure agent platform's SecureProxy — one-time purchase ($79–$149), sold as the natural next step to guide buyers. Not a SaaS subscription: a self-hosted CLI + library that developers drop into their agent stack in an afternoon. No customer data ever leaves their infrastructure — that's the trust pitch.

**Target buyer:** Developer/team who read the guide (or has the same problem) and wants the working implementation instead of building it from the chapters themselves. Ships as: npm/pip package + CLI + a proxy binary.

---

## v1 scope (what ships at launch)

### 1. MCP Scanner (static/audit mode)
- CLI command: `agentguard scan <mcp-server-url-or-config>`
- Connects to an MCP server, enumerates its declared tools/resources, and flags:
  - Overly broad tool schemas (free-text params where structured ones are possible)
  - Missing auth on the transport
  - Tools with destructive-sounding names/descriptions lacking a confirmation flag
  - Unsigned/unversioned tool manifests
  - Known-bad patterns from a maintained ruleset (updatable via `agentguard scan --update-rules`)
- Output: terminal report (pass/warn/fail per finding) + `--json` for CI integration
- This is the direct, demoable "free value" companion to the guide's Ch. 7 audit checklist — doubles as the free-tier hook product.

### 2. Guardrail Proxy (runtime enforcement)
- A lightweight reverse proxy that sits between the agent and its MCP servers / tool-calling layer.
- Config file (YAML) defines policy: allow/deny/require-approval per tool name + argument pattern, per session or per API key.
- Modes: `enforce` (block), `monitor` (log only, for rollout), `dry-run` (report what would've blocked).
- Human-in-the-loop hook: policy can route a matched call to a webhook/CLI prompt for manual approval before execution.

### 3. Input/Output Inspection
- Pluggable inspection pipeline on both tool-call arguments (input) and tool results (output):
  - **PII redaction**: regex + lightweight NER model for names/emails/phone/SSN/tokens/API keys/internal IDs; configurable redact vs. block vs. tokenize (reversible pseudonymization for internal use)
  - **Prompt injection heuristics** on tool output before it re-enters the agent's context (delimiter stripping, known injection-pattern matching, provenance tagging)
  - **Exfiltration checks** on outbound tool arguments (suspicious URL encoding, base64 blobs, unexpected external destinations vs. an egress allowlist)
- Sync inline for latency-tolerant calls, async/log-and-alert mode for high-throughput ones.

### 4. Audit Log
- Every intercepted tool call logged (redacted args + result, policy decision, timestamp, session/user).
- Local-first (JSONL/SQLite) — no external service required. Optional export to the user's own SIEM/log pipeline.
- `agentguard audit replay <session-id>` to replay a session's tool-call sequence for incident review.

### 5. Setup & Integration
- Drop-in adapters for the 2–3 most common agent frameworks/runtimes at launch (e.g. Claude Agent SDK / MCP client, LangChain, a raw MCP client) — minimize integration friction, this is the #1 churn risk for a self-hosted dev tool.
- `agentguard init` scaffolds a starter policy + redaction config from a short interactive questionnaire (what tools do you expose, what data is sensitive).
- Reference policy files matching the guide's Part 4 examples, so guide buyers can paste the tool in as literally the code from the book.

---

## Explicitly out of scope for v1
- Hosted/SaaS dashboard (v2 candidate, would shift pricing to subscription — keep v1 one-time-purchase to match the proven price point)
- Multi-tenant / enterprise RBAC
- ML-based anomaly detection beyond the heuristic ruleset (v2, once there's usage data to train on)
- Support for tool-calling agents outside the MCP/common-framework adapters (custom-only integration is "bring your own adapter" via documented interface, not officially supported)

## Pricing/packaging notes
- $79: CLI scanner + guardrail proxy + PII redaction, single-seat license, community rule updates
- $149: adds framework adapters, audit replay, and priority rule updates for 1 year
- Sold as an upsell inside the guide's PDF (last chapter + email sequence to buyers) and via the same landing page, not a separate cold-launch — reuses the guide's validated audience per the sequencing plan.

## Build order (mirrors guide chapter order for consistency)
1. Guardrail Proxy core (policy engine, enforce/monitor/dry-run) — this is SecureProxy's existing core, least new work
2. Input/Output inspection pipeline (PII redaction first, then injection/exfil heuristics)
3. MCP Scanner (audit mode) — good standalone free-tier/demo artifact, can launch slightly ahead of full v1 as a lead magnet
4. Audit log + replay
5. Framework adapters + `init` scaffolding — polish pass once core is validated by early buyers
