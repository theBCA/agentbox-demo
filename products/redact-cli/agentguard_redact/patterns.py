"""Regex detectors for the free tier. No network calls, no dependencies."""

import re

# Each pattern: (category, compiled regex). Order matters for overlap resolution.
PATTERNS = [
    ("credential", re.compile(r"sk-[A-Za-z0-9]{20,}")),                       # OpenAI-style keys
    ("credential", re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}")),                 # Anthropic keys
    ("credential", re.compile(r"AKIA[0-9A-Z]{16}")),                         # AWS access key id
    ("credential", re.compile(r"ghp_[A-Za-z0-9]{36}")),                       # GitHub PAT
    ("credential", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),              # Slack tokens
    ("credential", re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),  # JWT
    ("credential", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]+?-----END [A-Z ]*PRIVATE KEY-----")),
    ("financial", re.compile(r"\b(?:\d[ -]*?){13,16}\b")),                    # credit card-ish digit runs
    ("pii_id", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),                         # US SSN
    ("pii_contact", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),  # email
    ("pii_contact", re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")),  # US phone
    ("pii_location", re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")),  # IPv4
]


def scan(text: str):
    """Return a list of finding dicts, sorted by start offset, with overlaps
    resolved in favor of the earlier/longer match (regex layer is deterministic
    by design — no confidence scoring needed, patterns are exact)."""
    findings = []
    for category, pattern in PATTERNS:
        for m in pattern.finditer(text):
            findings.append({
                "start": m.start(),
                "end": m.end(),
                "text": m.group(0),
                "category": category,
                "confidence": 1.0,
                "source": "regex",
            })

    findings.sort(key=lambda f: (f["start"], -(f["end"] - f["start"])))
    resolved = []
    last_end = -1
    for f in findings:
        if f["start"] >= last_end:
            resolved.append(f)
            last_end = f["end"]
    return resolved
