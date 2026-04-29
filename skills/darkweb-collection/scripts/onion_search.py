#!/usr/bin/env python3
"""
onion_search.py — surface-web search of onion indexers (stdlib only).

Resolves current .onion mirrors for a given query by hitting *clearnet*
indexer endpoints. You do NOT need Tor to run this script — but you do
need Tor (Tails / Whonix / torsocks) to actually visit any .onion result
it returns.

Why this exists: dark-web onion addresses rot fast (forums get seized,
mirrors get phished, addresses rotate). Hard-coding onion v3 addresses
in markdown documentation creates two problems: (1) the address is stale
within months, and (2) a hijacked mirror in your docs is a phishing
trap. This script resolves them on demand instead.

Backends:
  ahmia    — https://ahmia.fi/search/?q=<query>     (free, no auth)
  darkfail — scrapes the dark.fail mirror status board (free, no auth)
  intelx   — IntelligenceX search if $INTELX_API_KEY is set (free tier
             ~50 queries/day; falls back gracefully if unset)

Usage:
  onion_search.py --query "lockbit"
  onion_search.py --query "breachforums" --backends ahmia,darkfail --limit 25
  onion_search.py --query "ransomhub"   --backends ahmia              --dry-run
  onion_search.py --status                                           # list backends + auth state

Exit codes:
  0  success (results emitted; zero results is not an error)
  1  network / parser error
  2  no usable backends configured (e.g. only intelx requested but $INTELX_API_KEY unset)
  3  bad arguments

OPSEC notes:
  - Ahmia and dark.fail will see your IP + query. Run via VPN/Tor if
    your query is operationally sensitive (e.g. revealing target name).
  - This script never connects to .onion addresses itself.
  - Output URLs may be hijacked phishing mirrors. Cross-check via
    PGP-signed mirror lists (Tor Project, dark.fail's signed list).
"""

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser

INTELX_API_KEY = os.environ.get("INTELX_API_KEY", "")
INTELX_BASE = os.environ.get("INTELX_URL", "https://2.intelx.io").rstrip("/")
USER_AGENT = os.environ.get(
    "ONION_SEARCH_UA",
    "Mozilla/5.0 (compatible; cti-skills/onion_search.py)",
)
BACKEND_NAMES = ("ahmia", "darkfail", "intelx")
ONION_RE = re.compile(r"\b([a-z2-7]{16}|[a-z2-7]{56})\.onion\b", re.IGNORECASE)


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def http_get(url, headers=None, timeout=30):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": USER_AGENT}, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


# ---------- Ahmia ----------

class _AhmiaParser(HTMLParser):
    """Pulls <li class="result"> blocks: title (<a>) + cite (URL) + first <p> (snippet)."""

    def __init__(self):
        super().__init__()
        self.in_result = False
        self.in_a = False
        self.in_cite = False
        self.in_p = False
        self.cur = {}
        self.results = []

    def handle_starttag(self, tag, attrs):
        ad = dict(attrs)
        if tag == "li" and "result" in (ad.get("class") or ""):
            self.in_result = True
            self.cur = {"title": "", "onion_url": "", "snippet": ""}
        elif self.in_result and tag == "a" and not self.cur["title"]:
            self.in_a = True
            href = ad.get("href") or ""
            if ".onion" in href:
                self.cur["onion_url"] = href
        elif self.in_result and tag == "cite":
            self.in_cite = True
        elif self.in_result and tag == "p":
            self.in_p = True

    def handle_endtag(self, tag):
        if tag == "li" and self.in_result:
            if self.cur.get("onion_url") or ONION_RE.search(self.cur.get("snippet", "")):
                self.results.append(self.cur)
            self.in_result = False
            self.cur = {}
        elif tag == "a":
            self.in_a = False
        elif tag == "cite":
            self.in_cite = False
        elif tag == "p":
            self.in_p = False

    def handle_data(self, data):
        if not self.in_result:
            return
        if self.in_a:
            self.cur["title"] += data.strip()
        elif self.in_cite:
            self.cur["onion_url"] = (self.cur["onion_url"] or data.strip())
        elif self.in_p:
            self.cur["snippet"] += data.strip() + " "


def search_ahmia(query, limit):
    url = "https://ahmia.fi/search/?" + urllib.parse.urlencode({"q": query})
    try:
        body = http_get(url)
    except urllib.error.URLError as e:
        return [], f"ahmia network error: {e}"
    parser = _AhmiaParser()
    try:
        parser.feed(body)
    except Exception as e:
        return [], f"ahmia parse error: {e}"
    results = []
    for r in parser.results[:limit]:
        results.append({
            "indexer": "ahmia",
            "title": html.unescape(r.get("title", "")).strip() or "(untitled)",
            "onion_url": r.get("onion_url", "").strip(),
            "snippet": html.unescape(r.get("snippet", "")).strip()[:400],
            "found_at": now_iso(),
            "source_url": url,
        })
    return results, None


# ---------- dark.fail ----------

DARKFAIL_URL = "https://dark.fail/"


def search_darkfail(query, limit):
    """dark.fail is a status page, not a search engine. We fetch the page,
    extract every (label, .onion) pair, and substring-filter by query."""
    try:
        body = http_get(DARKFAIL_URL)
    except urllib.error.URLError as e:
        return [], f"darkfail network error: {e}"
    # Lightweight: capture <a href="<onion>">label</a> wherever the onion sits
    pairs = re.findall(r"href=\"(http[s]?://[a-z2-7]{16,56}\.onion[^\"]*)\"[^>]*>([^<]{1,200})</a>", body, re.IGNORECASE)
    if not pairs:
        # Fallback: any onion + nearest preceding text
        pairs = [(m.group(0), "") for m in ONION_RE.finditer(body)]
    q = query.lower().strip()
    seen = set()
    results = []
    for url, label in pairs:
        key = url.lower()
        if key in seen:
            continue
        seen.add(key)
        haystack = (label + " " + url).lower()
        if q and q not in haystack:
            continue
        results.append({
            "indexer": "darkfail",
            "title": html.unescape(label).strip() or "(unlabeled)",
            "onion_url": url,
            "snippet": "",
            "found_at": now_iso(),
            "source_url": DARKFAIL_URL,
        })
        if len(results) >= limit:
            break
    return results, None


# ---------- IntelligenceX ----------

def search_intelx(query, limit):
    if not INTELX_API_KEY:
        return [], "intelx skipped: INTELX_API_KEY not set"
    # IntelligenceX has a two-step search (POST + poll). We do a minimal
    # synchronous form: POST with maxresults=limit, poll once after 2s.
    post_url = f"{INTELX_BASE}/intelligent/search"
    payload = json.dumps({
        "term": query,
        "maxresults": limit,
        "media": 0,
        "sort": 4,
        "terminate": [],
    }).encode("utf-8")
    headers = {
        "User-Agent": USER_AGENT,
        "x-key": INTELX_API_KEY,
        "Content-Type": "application/json",
    }
    try:
        req = urllib.request.Request(post_url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as r:
            init = json.loads(r.read().decode("utf-8", errors="replace") or "{}")
    except urllib.error.URLError as e:
        return [], f"intelx network error: {e}"
    sid = init.get("id")
    if not sid:
        return [], f"intelx: no search id returned ({init})"
    time.sleep(2)
    result_url = f"{INTELX_BASE}/intelligent/search/result?id={urllib.parse.quote(sid, safe='')}&limit={limit}"
    try:
        body = http_get(result_url, headers=headers)
        data = json.loads(body or "{}")
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        return [], f"intelx result error: {e}"
    out = []
    for rec in (data.get("records") or [])[:limit]:
        u = rec.get("name") or rec.get("systemid") or ""
        m = ONION_RE.search(u) or ONION_RE.search(rec.get("description", "") or "")
        if not m:
            continue
        out.append({
            "indexer": "intelx",
            "title": (rec.get("name") or "")[:200] or "(untitled)",
            "onion_url": m.group(0),
            "snippet": (rec.get("description") or "")[:400],
            "found_at": now_iso(),
            "source_url": post_url,
        })
    return out, None


# ---------- driver ----------

BACKENDS = {
    "ahmia": search_ahmia,
    "darkfail": search_darkfail,
    "intelx": search_intelx,
}


def cmd_status():
    print(json.dumps({
        "source": "onion_search",
        "operation": "status",
        "checked_at": now_iso(),
        "backends": {
            "ahmia": {"available": True, "auth": "none"},
            "darkfail": {"available": True, "auth": "none"},
            "intelx": {"available": bool(INTELX_API_KEY), "auth": "api-key (INTELX_API_KEY)"},
        },
    }, indent=2))


def main():
    ap = argparse.ArgumentParser(
        prog="onion_search.py",
        description="Surface-web search of onion indexers (stdlib only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--query", help="search term (e.g. 'lockbit', 'breachforums')")
    ap.add_argument("--backends", default="ahmia,darkfail",
                    help=f"comma-separated subset of: {','.join(BACKEND_NAMES)} (default: ahmia,darkfail)")
    ap.add_argument("--limit", type=int, default=25, help="cap results per backend (default 25)")
    ap.add_argument("--rate-limit", type=float, default=1.0,
                    help="seconds to sleep between backend calls (default 1.0)")
    ap.add_argument("--status", action="store_true", help="list backends + auth state and exit")
    ap.add_argument("--dry-run", action="store_true", help="show planned operation without calling indexers")
    args = ap.parse_args()

    if args.status:
        cmd_status(); return

    if not args.query:
        die("--query is required (or use --status)", 3)

    requested = [b.strip() for b in args.backends.split(",") if b.strip()]
    unknown = [b for b in requested if b not in BACKENDS]
    if unknown:
        die(f"unknown backend(s): {','.join(unknown)} (known: {','.join(BACKEND_NAMES)})", 3)

    usable = [b for b in requested if b != "intelx" or INTELX_API_KEY]
    if not usable:
        die("no usable backends — intelx requested but INTELX_API_KEY not set", 2)

    if args.dry_run:
        print(json.dumps({
            "dry_run": True,
            "query": args.query,
            "backends_requested": requested,
            "backends_usable": usable,
            "intelx_key_present": bool(INTELX_API_KEY),
            "limit_per_backend": args.limit,
        }, indent=2))
        return

    all_results = []
    errors = []
    for i, name in enumerate(usable):
        if i > 0 and args.rate_limit > 0:
            time.sleep(args.rate_limit)
        results, err = BACKENDS[name](args.query, args.limit)
        if err:
            errors.append({"backend": name, "error": err})
        all_results.extend(results)

    # Dedupe by onion_url, preserving order
    seen = set()
    deduped = []
    for r in all_results:
        key = r.get("onion_url", "").lower()
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(r)

    print(json.dumps({
        "source": "onion_search",
        "operation": "search",
        "query_time": now_iso(),
        "query": args.query,
        "backends": usable,
        "returned": len(deduped),
        "errors": errors,
        "results": deduped,
    }, indent=2))


if __name__ == "__main__":
    main()
