"""Apply findings to produce redacted text + an audit report."""


def apply(text: str, findings: list[dict], style: str = "full") -> tuple[str, dict]:
    """style: 'full' -> [REDACTED:category], 'partial' -> keep last 4 chars."""
    findings = sorted(findings, key=lambda f: f["start"])
    out = []
    last = 0
    for f in findings:
        out.append(text[last:f["start"]])
        if style == "partial" and len(f["text"]) > 4:
            tail = f["text"][-4:]
            out.append(f"[REDACTED:{f['category']}]{tail}")
        else:
            out.append(f"[REDACTED:{f['category']}]")
        last = f["end"]
    out.append(text[last:])

    report = {
        "finding_count": len(findings),
        "by_category": {},
        "findings": findings,
    }
    for f in findings:
        report["by_category"][f["category"]] = report["by_category"].get(f["category"], 0) + 1

    return "".join(out), report
