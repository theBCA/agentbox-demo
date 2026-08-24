# AgentGuard Redact

Scan and redact PII and secrets from text **before** it hits an LLM API
call, a tool call, or a log file. One command, no server, no account.

```
pip install agentguard-redact
echo "Email me at jane@corp.com" | agentguard-redact scan
# -> Email me at [REDACTED:pii_contact]
```

## Why this exists

The most common real-world "AI agent security" incident isn't an exotic
jailbreak — it's mundane leakage: a customer's email ends up in a debug log,
an API key pasted into a chat gets forwarded to a third-party LLM, an
agent's tool output (a support ticket, a database row) gets echoed straight
back into a prompt and then into a transcript some vendor stores forever.

AgentGuard Redact is a filter you drop in front of any of those three
choke points — the prompt going out, the tool output coming back, or the
log line being written — and it strips the sensitive part before it leaves
your process.

## What it catches

**Free tier — regex layer** (`agentguard_redact/patterns.py`), zero network
calls, deterministic, auditable:
- Credentials: OpenAI/Anthropic-style API keys, AWS access key IDs, GitHub
  PATs, Slack tokens, JWTs, PEM private key blocks
- Contact PII: email addresses, US phone numbers
- Financial: credit-card-shaped digit runs
- Government ID: US SSN format
- Network: IPv4 addresses

**Pro tier — LLM-assisted layer** (`agentguard_redact/llm_scan.py`, gated by
license key), catches what has no fixed pattern:
- Names attached to other personal detail, physical addresses, dates of
  birth
- Context-dependent secrets (a token with no recognizable prefix)
- Business-sensitive text (internal hostnames, unreleased product names,
  named-customer references) — this needs judgment, not a pattern, which
  is why it's the paid tier
- The exact detection prompt is in `PROMPT.md`, version-pinned so results
  don't silently drift under a customer's saved config

The regex layer always runs first, even in Pro mode — the LLM pass is
additive, so a failed API call or missing license degrades to free-tier
behavior rather than doing nothing.

## Methods this tool implements (and where each fits)

| Method | What it stops | Layer |
|---|---|---|
| Pattern-based redaction | Known-shape secrets/PII leaking into prompts, logs, or third-party APIs | Free (regex) |
| Context-aware entity detection | Free-form PII/business data regex structurally can't match | Pro (LLM) |
| Redact-before-send, not after | Data never reaches the LLM provider or log sink in the first place — not a post-hoc cleanup | Both |
| Audit report (`--report`) | "What did we actually redact, how often" — the artifact you need for a compliance conversation | Both |
| Partial-mask mode (`--style partial`) | Keeps enough (last 4 chars) for support/debugging without exposing the full value | Both |

This tool does **not** do prompt-injection detection, tool-call policy
enforcement, or MCP server auditing — those are separate, harder problems
(see `products/guide/chapter-outline.md` and `products/tool/feature-spec.md`
in this repo for that larger scope). AgentGuard Redact is deliberately one
job: keep sensitive text out of places it shouldn't go.

## Usage

```bash
# scan a file
agentguard-redact scan transcript.txt

# pipe into it — e.g. wrap an LLM call
cat prompt.txt | agentguard-redact scan | your-llm-cli

# get the audit report alongside the redacted output
agentguard-redact scan transcript.txt --report 2> findings.json

# partial masking (keep last 4 chars, useful for support workflows)
agentguard-redact scan transcript.txt --style partial

# Pro mode: regex + LLM-assisted pass
export ANTHROPIC_API_KEY=sk-ant-...
agentguard-redact scan transcript.txt --llm --license-key AGR-xxxx-xxxx
```

### As a library

```python
from agentguard_redact import patterns, mask

findings = patterns.scan(text)
redacted, report = mask.apply(text, findings, style="full")
```

Drop this into any point in your pipeline: right before `client.messages.create(...)`,
right after a tool result comes back, or right before `logger.info(...)`.

## Licensing model

- Free: regex layer, unlimited use, MIT-licensed core.
- Pro (one-time key, `AGR-xxxx-xxxx`): unlocks `--llm` mode. Validated
  offline (`agentguard_redact/license.py`) — no phone-home, no account
  system. Trust-based like most small indie CLI tools; the value is in
  the working software and the maintained detection prompt, not
  enforcement.

## Limitations (say this to customers, don't let them find out)

- Regex patterns are US/common-format biased (SSN, US phone). International
  formats are a roadmap item, not a v1 promise.
- Not a network proxy — it doesn't intercept traffic automatically. You
  call it explicitly at the point in your code where text would otherwise
  leave the process. (The larger `SecureProxy`-based tool in
  `products/tool/feature-spec.md` does automatic interception; this is the
  deliberately simpler, cheaper sibling.)
- Pro-tier LLM detection costs whatever the underlying API call costs —
  this tool doesn't hide that from the user.
