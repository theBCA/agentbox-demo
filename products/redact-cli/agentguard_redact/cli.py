#!/usr/bin/env python3
"""agentguard-redact: scan and redact PII/secrets from text before it hits
an LLM API call or a log file.

Usage:
    agentguard-redact scan  [FILE]           regex scan, prints redacted text
    agentguard-redact scan  [FILE] --llm      regex + Pro LLM pass (needs license)
    agentguard-redact scan  [FILE] --report   also print a JSON findings report
    agentguard-redact scan  [FILE] --style partial   keep last 4 chars per match
    agentguard-redact keygen                  (maintainer only) mint a license key
    cat prompt.txt | agentguard-redact scan   also reads from stdin
"""

import argparse
import json
import sys

from . import license as license_mod
from . import mask, patterns


def _read_input(file_arg: str | None) -> str:
    if file_arg:
        with open(file_arg, "r") as fh:
            return fh.read()
    return sys.stdin.read()


def cmd_scan(args: argparse.Namespace) -> int:
    text = _read_input(args.file)
    findings = patterns.scan(text)

    if args.llm:
        key = args.license_key or __import__("os").environ.get("AGENTGUARD_LICENSE_KEY")
        if not license_mod.is_valid(key):
            print(
                "error: --llm requires a valid Pro license key "
                "(pass --license-key or set AGENTGUARD_LICENSE_KEY)",
                file=sys.stderr,
            )
            return 1
        from . import llm_scan
        try:
            llm_findings = llm_scan.scan(text)
        except RuntimeError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
        findings.extend(llm_findings)
        findings.sort(key=lambda f: f["start"])

    redacted, report = mask.apply(text, findings, style=args.style)

    print(redacted)
    if args.report:
        print("\n--- findings report (JSON) ---", file=sys.stderr)
        print(json.dumps(report, indent=2), file=sys.stderr)

    return 0


def cmd_keygen(args: argparse.Namespace) -> int:
    print(license_mod.make_key())
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="agentguard-redact")
    sub = parser.add_subparsers(dest="command", required=True)

    scan_p = sub.add_parser("scan", help="scan and redact text")
    scan_p.add_argument("file", nargs="?", help="file to scan (default: stdin)")
    scan_p.add_argument("--llm", action="store_true", help="also run Pro LLM-assisted detection")
    scan_p.add_argument("--license-key", help="Pro license key (or set AGENTGUARD_LICENSE_KEY)")
    scan_p.add_argument("--report", action="store_true", help="print a JSON findings report to stderr")
    scan_p.add_argument("--style", choices=["full", "partial"], default="full")
    scan_p.set_defaults(func=cmd_scan)

    keygen_p = sub.add_parser("keygen", help="(maintainer) mint a license key")
    keygen_p.set_defaults(func=cmd_keygen)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
