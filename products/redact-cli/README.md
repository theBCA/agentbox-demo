# AgentGuard Redact

**Stop API keys and customer PII from leaking into your LLM prompts, tool calls, and logs.**
One command. Runs entirely on your machine — nothing you scan ever leaves your process.

![before/after: a prompt containing an email and API key, then the redacted output](docs/demo.gif)
<!-- Record with asciinema or a screen capture per MARKETING.md's launch checklist,
     convert to GIF, and drop it at docs/demo.gif before publishing. -->

```bash
pip install agentguard-redact

echo "Email me at jane@corp.com, key sk-live-abc123..." | agentguard-redact scan
# → Email me at [REDACTED:pii_contact], key [REDACTED:credential]
```

## Why

Every team shipping an AI agent eventually has the same bad day: a
customer's email ends up in a debug log, an API key gets pasted into a
prompt and forwarded to a third-party model, a tool result gets echoed
straight back into a transcript some vendor stores forever.

AgentGuard Redact is a filter you drop in front of any of those three
choke points — the prompt going out, the tool output coming back, or the
log line being written — and it strips the sensitive part before it leaves
your process.

## What it catches

**Free, forever — regex layer.** Zero network calls, deterministic, fully
auditable:
- API keys: OpenAI, Anthropic, AWS, GitHub, Slack, JWTs, PEM private keys
- Contact PII: emails, US phone numbers
- Financial: credit-card-shaped numbers
- Government ID: US SSN format
- Network: IPv4 addresses

**Pro — LLM-assisted layer** (license key, see below). Catches what has no
fixed pattern: names tied to personal detail, physical addresses,
context-dependent secrets, and business-sensitive text like internal
hostnames or unreleased product names. Full detection prompt is in
[`PROMPT.md`](PROMPT.md), versioned so results don't drift silently.

Regex always runs first, even in Pro mode — the LLM pass is additive, so a
failed API call or missing license degrades to free-tier behavior, never to
nothing.

## Usage

```bash
# scan a file
agentguard-redact scan transcript.txt

# pipe into it — wrap an LLM call
cat prompt.txt | agentguard-redact scan | your-llm-cli

# get a JSON audit report alongside the redacted output
agentguard-redact scan transcript.txt --report 2> findings.json

# partial masking — keep the last 4 chars, useful for support workflows
agentguard-redact scan transcript.txt --style partial

# Pro: regex + LLM-assisted pass
export ANTHROPIC_API_KEY=sk-ant-...
agentguard-redact scan transcript.txt --llm --license-key AGR-xxxx-xxxx
```

As a library:

```python
from agentguard_redact import patterns, mask

findings = patterns.scan(text)
redacted, report = mask.apply(text, findings, style="full")
```

Drop this right before `client.messages.create(...)`, right after a tool
result comes back, or right before `logger.info(...)`.

## Pro license

$29 one-time — [get a key on Gumroad](#) (see [`MARKETING.md`](MARKETING.md)
for the listing). Validated fully offline, no account, no subscription, no
phone-home. You're paying for the maintained detection prompt and the LLM
pass it drives, not a service.

## What this is not

- Not a network proxy — it doesn't intercept traffic automatically. You
  call it explicitly at the point in your code where text would otherwise
  leave the process. For automatic interception, see the larger
  `SecureProxy`-based tool this project's guardrail kit is built on.
- Not prompt-injection detection or tool-call policy enforcement — separate,
  harder problems, out of scope here on purpose.
- Not a hosted API. That would contradict the whole pitch.

Full docs: [`DOCUMENTATION.md`](DOCUMENTATION.md). Detection methods and
limitations are spelled out there, including where the regex patterns are
US-format-biased today.

## License

MIT for the free core (`agentguard_redact/patterns.py`, `mask.py`, CLI).
Pro-tier detection prompt and license validation are proprietary — see
[`PROMPT.md`](PROMPT.md).
