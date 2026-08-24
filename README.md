# AI Agent Security — Digital Product Line

Two connected premium products built on top of the secure agent platform's SecureProxy work.

## The plan
0. **AgentGuard Redact** — a small, real, working CLI shipped now (below) to
   fund and validate the rest: free regex redaction + a paid Pro key for
   LLM-assisted detection. This *is* the free validation step, with a real
   tool attached instead of just a problem breakdown.
1. **Validate free** — post it (and/or a specific problem breakdown, e.g.
   MCP PII leakage) on LinkedIn/dev.to/r/AI_Agents; watch for "how do I buy
   this" signal before investing further.
2. **Guide** — *Securing AI Agents in Production* ($150–$290 PDF). Build
   next: faster than the full tool, validates demand, drawn from real
   production experience with MCP hardening, PII redaction, and policy
   enforcement.
3. **Tool** — MCP security scanner / agent guardrail kit ($79–$149
   one-time). Build after, sold to the guide's own buyers as the natural
   next step.

## In this repo
- [`products/redact-cli/`](products/redact-cli/) — **AgentGuard Redact**,
  a working CLI/library shipping today. See `DOCUMENTATION.md` for what it
  does, `PROMPT.md` for the Pro-tier detection prompt, and `SELLING.md`
  for exactly where and how to sell it.
- [`products/guide/chapter-outline.md`](products/guide/chapter-outline.md) — full chapter outline for the guide
- [`products/tool/feature-spec.md`](products/tool/feature-spec.md) — v1 feature spec for the packaged tool

## Why this shape (market research)
Gumroad data across 146K products / $206M tracked revenue: category revenue totals are misleading, revenue *per product* is what matters. Software Development products average $60,814/product; Writing & Publishing averages $15,750/product with the lowest competition (226 products). Generic AI prompt packs underperform — winners are real tools/workflows or deep-expertise guides priced like software. Proof points: a $50 Photoshop AI script made $586K off 11,725 sales; a $290 no-software PDF guide made $568K off 1,957 sales on expertise alone.
