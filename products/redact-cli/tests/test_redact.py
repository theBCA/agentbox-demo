import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agentguard_redact import license as license_mod
from agentguard_redact import mask, patterns


def test_email_and_key_redacted():
    text = "Contact john@example.com. Key: sk-abcdefghijklmnopqrstuvwx1234."
    findings = patterns.scan(text)
    redacted, report = mask.apply(text, findings)
    assert "john@example.com" not in redacted
    assert "sk-abcdefghijklmnopqrstuvwx1234" not in redacted
    assert report["finding_count"] == 2
    assert report["by_category"]["pii_contact"] == 1
    assert report["by_category"]["credential"] == 1


def test_no_findings_passthrough():
    text = "Nothing sensitive here."
    findings = patterns.scan(text)
    redacted, report = mask.apply(text, findings)
    assert redacted == text
    assert report["finding_count"] == 0


def test_partial_style_keeps_tail():
    text = "Email jane@corp.com now."
    findings = patterns.scan(text)
    redacted, _ = mask.apply(text, findings, style="partial")
    assert redacted.endswith(".com now.") or "corp.com" in redacted


def test_license_roundtrip():
    key = license_mod.make_key()
    assert license_mod.is_valid(key)
    assert not license_mod.is_valid("AGR-0000000000000000-ffff")
    assert not license_mod.is_valid(None)
    assert not license_mod.is_valid("garbage")


if __name__ == "__main__":
    test_email_and_key_redacted()
    test_no_findings_passthrough()
    test_partial_style_keeps_tail()
    test_license_roundtrip()
    print("all tests passed")
