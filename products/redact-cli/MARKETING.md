# Launch copy

## Gumroad listing

**Title:** AgentGuard Redact — Pro Key (PII/Secret Redaction CLI)

**Price:** $29 one-time

**Short description (subtitle):**
Stop API keys and customer PII from leaking into your LLM prompts, tool
calls, and logs. One command. Runs entirely on your machine.

**Full description:**

> Every team shipping an AI agent eventually has the same bad day: a
> customer's email ends up in a debug log, an API key gets pasted into a
> prompt and forwarded to a third-party model, a tool result gets echoed
> straight back into a transcript some vendor stores forever.
>
> **AgentGuard Redact** is a one-command filter you drop in front of any of
> those choke points — the prompt going out, the tool output coming back,
> the log line being written — and it strips the sensitive part before it
> leaves your process.
>
> ```
> pip install agentguard-redact
> echo "Email me at jane@corp.com, key sk-live-abc123..." | agentguard-redact scan
> → Email me at [REDACTED:pii_contact], key [REDACTED:credential]
> ```
>
> **Free, forever:** the regex engine catches API keys (OpenAI, Anthropic,
> AWS, GitHub, Slack, JWTs), emails, phone numbers, credit-card-shaped
> numbers, SSNs, and IPs. Zero network calls, fully auditable, MIT-licensed.
>
> **This Pro key unlocks LLM-assisted detection** — catches what regex
> structurally can't: names attached to personal detail, physical
> addresses, business-sensitive text like internal hostnames or unreleased
> product names, and secrets with no recognizable prefix. Same command,
> just add `--llm`.
>
> **What you get:**
> - A lifetime Pro license key (`AGR-xxxx-xxxx`), validated offline — no
>   account, no phone-home, no subscription
> - Full source for both the free and Pro detection logic
> - The versioned detection prompt itself, so you can see exactly what
>   it looks for and adapt it
>
> **What this is not:** a hosted API or SaaS. Nothing you scan ever leaves
> your machine except the optional Pro pass, which goes directly from your
> process to your own Anthropic API key — never through us. That's the
> point.
>
> No install limits, no seat count, no renewal. Buy once, use it
> everywhere you build agents.

**Tags:** ai-security, developer-tools, cli, python, llm, pii, data-privacy

**Cover asset:** the before/after terminal recording (see `#launch-checklist`
below) — first frame should show the raw prompt with a visible fake
email + key, since that's the whole pitch at a glance.

---

## Validation / launch post (LinkedIn, dev.to, r/AI_Agents)

Same core copy, three lengths for three platforms.

### LinkedIn (short, punchy, ends with a question to drive comments)

> Every team shipping an AI agent eventually has the same bad day: a
> customer email ends up in a debug log, or an API key gets pasted into a
> prompt and forwarded straight to a third-party model.
>
> I built a one-command tool to stop that before it happens —
> AgentGuard Redact scans text and strips PII/secrets before it hits an
> LLM call or a log file. Free tier is regex-based (API keys, emails,
> phone numbers, SSNs), runs entirely on your machine, no data leaves
> your process.
>
> `pip install agentguard-redact`
>
> Curious how many of you have actually had a leak like this happen in
> production — and whether a tool like this would've caught it before it
> did. What's leaked for you?

### dev.to (longer, technical, includes the why + a code block)

Title: **The most common "AI agent security" incident isn't a jailbreak — it's a debug log**

> Most AI agent security content is about prompt injection and jailbreaks.
> In practice, the incident I see most often is much less exciting: PII or
> a secret ends up somewhere it shouldn't because nobody put a filter in
> front of the three places text actually leaves an agent's process —
> the prompt going out, the tool output coming back, and the log line
> being written.
>
> So I built a small CLI for exactly that: [`agentguard-redact`]. Free tier
> is a deterministic regex layer (API keys for OpenAI/Anthropic/AWS/GitHub/
> Slack, JWTs, emails, phone numbers, SSNs, credit-card-shaped numbers) —
> zero network calls, fully auditable. There's a paid Pro tier that adds an
> LLM-assisted pass for what regex can't structurally catch: names tied to
> personal detail, addresses, business-sensitive text.
>
> ```bash
> pip install agentguard-redact
> cat transcript.txt | agentguard-redact scan --report
> ```
>
> It doesn't try to solve prompt injection or policy enforcement — those
> are harder, different problems. This does one job: keep sensitive text
> out of places it shouldn't go, at the exact point your code would
> otherwise send it there.
>
> Repo / install: [link]. Would genuinely like to hear what's leaked for
> other people building agents — that's the thing I want to fix next.

### r/AI_Agents (informal, invites pushback, avoid sounding like an ad)

> Built a small thing after watching a few teams (including mine)
> accidentally leak PII/API keys into LLM prompts and logs while building
> agents — no exotic attack, just nobody filtering the text before it left
> the process.
>
> `agentguard-redact` — free CLI, regex-based, pip installable, redacts
> before send instead of cleaning up after. Paid tier adds LLM-assisted
> detection for stuff regex can't pattern-match (names, addresses, etc).
>
> Genuinely asking: is this a problem for people here, or is everyone
> already handling it some other way? Happy to be told this is redundant
> with [whatever] — trying to figure out if it's worth building further.

---

## Launch checklist (do these in order, ~30 minutes total)

1. **Reserve the PyPI name** — `pip install agentguard-redact` should
   404-to-installable, not fail on a name collision. Check first.
2. **Record the terminal GIF** — `asciinema` or a plain screen recording:
   paste a fake prompt with an obvious email + fake API key, run
   `agentguard-redact scan`, show the clean output. Under 15 seconds.
   This is the Gumroad cover image and the top of the GitHub README.
3. **Publish to PyPI**, tag `v0.1.0` on the repo.
4. **Create the Gumroad listing** using the copy above + the GIF.
5. **Post the dev.to piece first** (it's evergreen and drives search
   traffic later), then LinkedIn, then Reddit a day or two after —
   staggering avoids looking like a coordinated ad blast across platforms.
6. **Watch for one signal only:** does anyone ask "how do I buy the Pro
   version" or "does this do X" unprompted. That's the demand check —
   more valuable than the sale itself this early.
