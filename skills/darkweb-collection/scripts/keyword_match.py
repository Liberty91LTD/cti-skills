#!/usr/bin/env python3
"""
keyword_match.py — local regex/keyword scanner over collected text dumps (stdlib only).

Companion to telegram_monitor.py and onion_search.py: takes the JSONL
output (or any directory of text/JSONL files) and scans every line/value
against a list of selectors. Emits one JSONL match record per hit.

Selector file format — one selector per line, with optional prefix:
  literal:Acme Corporation        # case-insensitive substring (default if no prefix)
  regex:CVE-202[3-6]-\\d{4,5}      # arbitrary Python regex
  domain:acme\\.(com|net|io)       # word-boundary anchored regex on a domain
  email:@acme\\.com                # word-boundary anchored regex on an email tail
Lines starting with '#' or empty are ignored.

Usage:
  keyword_match.py --input ./collected --selectors-file selectors.txt
  keyword_match.py --input msgs.jsonl  --selectors-file selectors.txt --context 200
  keyword_match.py --input ./collected --selectors-file selectors.txt --dedupe-by match
  keyword_match.py --input ./collected --selectors-file selectors.txt --dry-run

Exit codes:
  0  success (matches printed; absence of matches is not an error)
  1  I/O error
  2  no selectors loaded
  3  bad arguments
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

PREFIXES = ("literal:", "regex:", "domain:", "email:")


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load_selectors(path):
    selectors = []
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.rstrip("\n").strip()
            if not line or line.startswith("#"):
                continue
            kind = "literal"
            value = line
            for p in PREFIXES:
                if line.startswith(p):
                    kind = p[:-1]
                    value = line[len(p):]
                    break
            try:
                if kind == "literal":
                    pattern = re.compile(re.escape(value), re.IGNORECASE)
                elif kind == "regex":
                    pattern = re.compile(value, re.IGNORECASE)
                elif kind == "domain":
                    pattern = re.compile(rf"(?<![\w.-]){value}(?![\w.-])", re.IGNORECASE)
                elif kind == "email":
                    pattern = re.compile(rf"[\w.+-]+{value}", re.IGNORECASE)
            except re.error as e:
                die(f"bad selector on line: {line!r}: {e}", 3)
            selectors.append({"raw": line, "kind": kind, "value": value, "pattern": pattern})
    return selectors


def iter_files(input_path):
    if os.path.isfile(input_path):
        yield input_path
        return
    if not os.path.isdir(input_path):
        die(f"input path does not exist: {input_path}")
    for root, _, files in os.walk(input_path):
        for name in files:
            if name.startswith("."):
                continue
            yield os.path.join(root, name)


def iter_lines(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for i, line in enumerate(fh, start=1):
                yield i, line.rstrip("\n")
    except OSError as e:
        print(f"warn: could not read {path}: {e}", file=sys.stderr)


def extract_text(line):
    """If the line is a JSON object, return a flattened string of its scalar
    values (so we match against text fields, not the structural JSON braces).
    Otherwise return the line as-is."""
    s = line.strip()
    if not (s.startswith("{") and s.endswith("}")):
        return line
    try:
        obj = json.loads(s)
    except json.JSONDecodeError:
        return line
    parts = []

    def walk(v):
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, dict):
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
    walk(obj)
    return "\n".join(parts)


def context_window(text, span, radius):
    start, end = span
    before = text[max(0, start - radius):start]
    after = text[end:end + radius]
    return before, after


def main():
    ap = argparse.ArgumentParser(
        prog="keyword_match.py",
        description="Local regex/keyword scanner over collected text dumps",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--input", required=True, help="file or directory to scan")
    ap.add_argument("--selectors-file", required=True, help="path to selector list")
    ap.add_argument("--context", type=int, default=120, help="chars of context before/after each match (default 120)")
    ap.add_argument("--dedupe-by", choices=["match", "match+selector", "none"], default="match+selector",
                    help="suppress duplicate hits (default: match+selector)")
    ap.add_argument("--max-matches-per-line", type=int, default=10,
                    help="cap matches reported per line per selector (default 10)")
    ap.add_argument("--dry-run", action="store_true", help="load selectors, list files, exit without scanning")
    args = ap.parse_args()

    selectors = load_selectors(args.selectors_file)
    if not selectors:
        die("no selectors loaded — file is empty or all comments", 2)

    files = list(iter_files(args.input))

    if args.dry_run:
        print(json.dumps({
            "dry_run": True,
            "input": os.path.abspath(args.input),
            "files_to_scan": len(files),
            "selectors_loaded": len(selectors),
            "selector_kinds": sorted({s["kind"] for s in selectors}),
            "context_radius": args.context,
            "dedupe_by": args.dedupe_by,
        }, indent=2))
        return

    seen = set()
    total_matches = 0
    for path in files:
        for line_no, line in iter_lines(path):
            haystack = extract_text(line)
            for sel in selectors:
                hits = 0
                for m in sel["pattern"].finditer(haystack):
                    if hits >= args.max_matches_per_line:
                        break
                    hits += 1
                    matched_text = m.group(0)
                    if args.dedupe_by == "match":
                        key = matched_text.lower()
                        if key in seen:
                            continue
                        seen.add(key)
                    elif args.dedupe_by == "match+selector":
                        key = (sel["raw"], matched_text.lower())
                        if key in seen:
                            continue
                        seen.add(key)
                    before, after = context_window(haystack, m.span(), args.context)
                    record = {
                        "source": "keyword_match",
                        "scanned_at": now_iso(),
                        "file": path,
                        "line_no": line_no,
                        "selector": sel["raw"],
                        "selector_kind": sel["kind"],
                        "match": matched_text,
                        "context_before": before,
                        "context_after": after,
                    }
                    print(json.dumps(record, ensure_ascii=False))
                    total_matches += 1

    print(json.dumps({
        "source": "keyword_match",
        "operation": "summary",
        "scanned_at": now_iso(),
        "files_scanned": len(files),
        "selectors_loaded": len(selectors),
        "matches_emitted": total_matches,
    }), file=sys.stderr)


if __name__ == "__main__":
    main()
