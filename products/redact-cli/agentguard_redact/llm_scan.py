"""Pro-tier LLM-assisted scan. Only imported/called when a valid license key
is present, so free-tier installs never require the `anthropic` package."""

import json
import os
from pathlib import Path

_PROMPT_PATH = Path(__file__).resolve().parent.parent / "PROMPT.md"


def _load_system_prompt() -> str:
    content = _PROMPT_PATH.read_text()
    start = content.index("```\n") + 4
    end = content.index("\n```", start)
    return content[start:end]


def scan(text: str, min_confidence: float = 0.5) -> list[dict]:
    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError(
            "Pro mode needs the 'anthropic' package: pip install anthropic"
        ) from e

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Set ANTHROPIC_API_KEY to use --llm Pro mode.")

    client = anthropic.Anthropic(api_key=api_key)
    system_prompt = _load_system_prompt()

    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": text}],
    )

    raw = "".join(block.text for block in response.content if hasattr(block, "text"))

    findings = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            f = json.loads(line)
        except json.JSONDecodeError:
            continue
        if f.get("confidence", 0) < min_confidence:
            continue
        f["source"] = "llm"
        findings.append(f)
    return findings
