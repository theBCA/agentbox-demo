# Goal

Ship one small, real, sellable thing this session — not the full platform.

**Product: AgentGuard Redact**
A single-purpose CLI/library that scans text (prompts, tool outputs, logs) and
redacts PII and secrets *before* they hit an LLM API call or a log file.

Why this specific thing, not the bigger platform:
- One job, done well. Installs in one line, runs in one command, output is
  obviously correct or obviously wrong — no onboarding call needed.
- It's the single most concrete, most-asked-for piece of "AI agent security"
  (indirect leakage of PII/secrets through prompts and tool output is the
  #1 real incident category — see the guide outline, Ch. 9–10).
- Free tier is genuinely useful standalone (regex redaction) — that's the
  distribution engine. Pro tier (LLM-assisted detection via the system
  prompt in `PROMPT.md`) is the paid unlock. This is the same shape as the
  two proof points from the market research: cheap to build, priced like
  software, sold as a finished tool not a prompt pack.

**Definition of done for this pass:**
1. `PROMPT.md` — the system prompt that powers Pro-tier LLM detection.
2. `DOCUMENTATION.md` — what it does, the security methods it implements,
   how to use it, how licensing works.
3. Working code (`agentguard_redact/`) — regex engine + optional LLM mode +
   license-key gate. Runs standalone, no server required.
4. `SELLING.md` — concrete answer to "can we actually sell this somewhere":
   named channels, listing draft, pricing, and the honest tradeoffs of each.
