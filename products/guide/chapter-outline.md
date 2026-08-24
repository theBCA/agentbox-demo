# Securing AI Agents in Production
### Premium technical guide — chapter outline

**Positioning:** Priced like software ($150–$290), not an impulse-buy prompt pack. Sold to engineers/teams shipping AI agents with real tool access (MCP servers, browser automation, code execution, internal APIs) who need to close the gap between "demo works" and "safe to run against production data."

**Format:** PDF + companion repo (checklists, config templates, example policies). ~120–160 pages. Every chapter ends with a "Production Checklist" and a copy-pasteable artifact (policy file, regex set, config snippet).

---

## Part 1 — The Threat Model
1. **Why agent security is a different problem**
   Traditional appsec assumes a fixed code path; agents assume an LLM choosing the path. What breaks: trust boundaries, input/output are now the same channel, tool calls are unreviewed code execution.
2. **The attack surface of a tool-using agent**
   Prompt injection (direct + indirect via tool output), confused deputy via delegated credentials, MCP server compromise, over-permissioned tool grants, output-side exfiltration.
3. **Case studies from production incidents**
   3–4 anonymized/public real incidents (indirect injection via web content, MCP server leaking secrets, agent over-calling a destructive tool). What the postmortem actually found.

## Part 2 — MCP Hardening
4. **MCP trust boundaries**
   Where an MCP server sits relative to your agent's privilege — treat every MCP server as untrusted input, not as your own code.
5. **Server-level hardening**
   Auth between agent and MCP server, transport security, capability scoping (what tools a server is allowed to expose per session), rate limits, sandboxing execution.
6. **Tool-definition hygiene**
   Minimal tool surfaces, explicit parameter schemas, rejecting free-text tool arguments where structured ones exist, versioning and signing tool manifests.
7. **Detecting a compromised or malicious MCP server**
   Anomaly signals (unexpected tool additions, schema drift, exfil-shaped outputs), a practical audit checklist for third-party MCP servers before you connect one.

## Part 3 — Input & Output Inspection
8. **Prompt injection defense in depth**
   Why you can't fully solve this with a prompt; layered mitigations (instruction hierarchy, delimiters, provenance tagging of tool output, spotlighting).
9. **PII detection and redaction**
   What counts as PII in agent contexts (not just names/emails — session tokens, internal IDs, file paths). Redaction at ingress vs. egress, structured vs. unstructured data, false-positive tradeoffs.
10. **Output-side exfiltration control**
    Blocking agents from encoding data into URLs, image alt text, or tool calls that phone home; egress allowlisting for tool network access.
11. **Building an inspection pipeline**
    Where inspection sits (proxy layer vs. inline), latency budget, sync vs. async redaction, what to log vs. what to block silently.

## Part 4 — Policy Enforcement
12. **Designing an agent permission model**
    Capability-based tool grants, per-session vs. per-user policy, least privilege for delegated credentials (OAuth scopes, short-lived tokens).
13. **Writing enforceable policies**
    Declarative policy examples (allow/deny/require-approval per tool+argument pattern), human-in-the-loop escalation for high-risk actions.
14. **Runtime enforcement patterns**
    Proxy-based interception vs. SDK-level hooks vs. sandboxed execution; where SecureProxy-style architectures fit; enforcing policy without breaking agent UX.
15. **Auditing and incident response**
    What to log (full tool call + args + result, redacted), retention/compliance considerations, building a replayable audit trail, responding to a caught injection attempt.

## Part 5 — Shipping It
16. **A production readiness checklist**
    Consolidated go/no-go checklist across Parts 2–4.
17. **Reference architecture**
    End-to-end diagram: agent → policy layer → inspection layer → MCP servers → external tools, with the redaction/policy layer called out.
18. **Appendix: config templates**
    Sample MCP hardening config, redaction regex/model config, policy DSL examples — the copy-paste starter kit.

---

## Notes for drafting order
- Write Part 2 (MCP Hardening) and Part 3 (Input/Output Inspection) first — most directly mirrors SecureProxy work already built, fastest to draft with real detail, and is the strongest differentiator vs. generic "AI security" content on Gumroad.
- Part 1 can be written last as framing/hook material once the technical chapters exist.
- Chapter 9 (PII redaction) and Chapter 13 (policy enforcement) are the two chapters that map directly to the tool's future feature set — keep terminology consistent with the tool spec so guide buyers recognize the tool as "the thing from the book" at launch.
