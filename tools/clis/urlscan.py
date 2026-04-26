#!/usr/bin/env python3
"""
urlscan.py — URLScan.io API v1 CLI (stdlib only, no install).

The Node CLI submits a URL or searches by domain. The Python CLI exposes
the full public API surface — including Lucene-style search (the killer
pivot capability), quota check, and DOM/screenshot download.

API reference: https://docs.urlscan.io/apis/urlscan-openapi/live-scanning
Auth header:   API-Key: $URLSCAN_API_KEY

Usage:
  urlscan.py submit <url> [--visibility unlisted|public|private] [--country CC]
                         [--user-agent UA] [--tags tag1,tag2] [--wait]
                         [--dry-run]
  urlscan.py result <uuid> [--dry-run]
  urlscan.py search "<query>" [--size N] [--dry-run]
  urlscan.py quota [--dry-run]
  urlscan.py screenshot <uuid> [--out FILE] [--dry-run]
  urlscan.py dom <uuid> [--out FILE] [--dry-run]

Search query examples (Lucene):
  page.domain:malicious.example
  page.url:*login*
  asn:AS13335
  hash:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
  filename:*.exe AND verdicts.overall.malicious:true
  page.country:RU AND task.tags:phishing

Visibility:
  unlisted  (default — scan exists but not in public search)
  public    (listed publicly — only when explicitly requested)
  private   (Pro tier only)

Exit codes:
  0  success
  1  network / API error (incl. 429)
  2  missing URLSCAN_API_KEY (only when not --dry-run)
  3  bad arguments
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API_KEY = os.environ.get("URLSCAN_API_KEY", "")
API_BASE = "https://urlscan.io/api/v1"


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def _request(method, url, headers=None, body=None, dry_run=False, raw=False):
    headers = dict(headers or {})
    headers.setdefault("Accept", "application/json")

    if dry_run:
        return {
            "dry_run": True,
            "method": method,
            "url": url,
            "headers": {**headers, "API-Key": "<redacted>" if API_KEY else "<unset>"},
            "body_present": body is not None,
        }

    if not API_KEY:
        die("URLSCAN_API_KEY not set. Run /cti-setup or ./scripts/setup.sh", 2)

    headers["API-Key"] = API_KEY
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            content = r.read()
        if raw:
            return content
        return json.loads(content.decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode("utf-8", errors="replace") if e.fp else ""
        if e.code == 429:
            die("rate limited (429). Free tier is 100 scans/day, 5000 searches/month.", 1)
        if e.code == 404:
            die(f"not found (404): {body_txt[:200]}", 1)
        die(f"HTTP {e.code}: {body_txt[:300]}", 1)
    except urllib.error.URLError as e:
        die(f"network error: {e.reason}", 1)
    except json.JSONDecodeError as e:
        die(f"invalid JSON: {e}", 1)


def cmd_submit(args):
    body = {"url": args.url, "visibility": args.visibility}
    if args.country:
        body["country"] = args.country
    if args.user_agent:
        body["customagent"] = args.user_agent
    if args.tags:
        body["tags"] = [t.strip() for t in args.tags.split(",") if t.strip()]
    if args.referer:
        body["referer"] = args.referer

    resp = _request("POST", f"{API_BASE}/scan/", body=body, dry_run=args.dry_run)
    if args.dry_run:
        out = {"dry_run": True, "operation": "submit", "url": args.url, "call": resp}
        if args.wait:
            out["follow_up_calls"] = ["GET /api/v1/result/{uuid}/ until 200"]
        print(json.dumps(out, indent=2))
        return

    uuid = resp.get("uuid")
    out = {
        "source": "urlscan",
        "operation": "submit",
        "url": args.url,
        "visibility": args.visibility,
        "submitted_at": now_iso(),
        "uuid": uuid,
        "result": resp.get("result"),
        "api": resp.get("api"),
        "visibility_recorded": resp.get("visibility"),
    }
    if args.wait:
        out["polling"] = {"max_attempts": 12, "interval_seconds": 10}
        # First wait, then poll
        for attempt in range(12):
            time.sleep(10)
            try:
                with urllib.request.urlopen(
                    urllib.request.Request(
                        f"{API_BASE}/result/{uuid}/",
                        headers={"API-Key": API_KEY, "Accept": "application/json"},
                    ),
                    timeout=30,
                ) as r:
                    if r.status == 200:
                        out["result_data"] = _summarise_scan(json.loads(r.read().decode("utf-8")))
                        out["polling"]["resolved_after_seconds"] = (attempt + 1) * 10
                        break
            except urllib.error.HTTPError as e:
                if e.code != 404:
                    out["polling_error"] = f"HTTP {e.code}"
                    break
                # 404 = scan not ready yet, keep polling
        else:
            out["polling"]["timed_out"] = True
    print(json.dumps(out, indent=2))


def _summarise_scan(scan):
    page = scan.get("page", {}) or {}
    task = scan.get("task", {}) or {}
    verdicts = scan.get("verdicts", {}) or {}
    overall = verdicts.get("overall", {}) or {}
    lists = scan.get("lists", {}) or {}
    stats = scan.get("stats", {}) or {}

    # hasVerdicts:true only means at least one engine produced a verdict —
    # NOT that anything was flagged. The actual signal is in malicious=true,
    # a non-zero score, populated brands list, or suspicious-flavoured tags.
    score = overall.get("score") or 0
    brands = overall.get("brands") or []
    cats = overall.get("categories") or []
    if overall.get("malicious"):
        verdict = "malicious"
    elif score > 0 or brands or any(c in cats for c in ("phishing", "malware", "scam")):
        verdict = "suspicious"
    elif overall.get("hasVerdicts"):
        verdict = "clean"
    else:
        verdict = "unknown"

    return {
        "uuid": task.get("uuid"),
        "scanned_url": task.get("url"),
        "final_url": page.get("url"),
        "ip": page.get("ip"),
        "country": page.get("country"),
        "asn": page.get("asn"),
        "asn_name": page.get("asnname"),
        "server": page.get("server"),
        "title": page.get("title"),
        "verdict_overall": verdict,
        "verdict_score": score,
        "verdict_categories": cats,
        "verdict_brands": brands,
        "verdict_tags": overall.get("tags"),
        "screenshot_url": task.get("screenshotURL"),
        "report_url": task.get("reportURL"),
        "dom_url": task.get("domURL"),
        "domains_contacted": (lists.get("domains") or [])[:30],
        "ips_contacted": (lists.get("ips") or [])[:30],
        "stats": {
            "unique_ips": stats.get("uniqIPs"),
            "unique_countries": stats.get("uniqCountries"),
            "data_length": stats.get("dataLength"),
            "request_count": stats.get("requests"),
        },
    }


def cmd_result(args):
    resp = _request("GET", f"{API_BASE}/result/{args.uuid}/", dry_run=args.dry_run)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return
    out = {
        "source": "urlscan",
        "operation": "result",
        "query_time": now_iso(),
        "summary": _summarise_scan(resp),
    }
    print(json.dumps(out, indent=2))


def cmd_search(args):
    qs = urllib.parse.urlencode({"q": args.query, "size": args.size})
    resp = _request("GET", f"{API_BASE}/search/?{qs}", dry_run=args.dry_run)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return
    results = resp.get("results", [])
    out = {
        "source": "urlscan",
        "operation": "search",
        "query": args.query,
        "query_time": now_iso(),
        "total": resp.get("total"),
        "took_ms": resp.get("took"),
        "count": len(results),
        "results": [
            {
                "uuid": r.get("_id") or (r.get("task") or {}).get("uuid"),
                "scanned_url": (r.get("task") or {}).get("url"),
                "final_url": (r.get("page") or {}).get("url"),
                "domain": (r.get("page") or {}).get("domain"),
                "ip": (r.get("page") or {}).get("ip"),
                "country": (r.get("page") or {}).get("country"),
                "asn": (r.get("page") or {}).get("asn"),
                "title": (r.get("page") or {}).get("title"),
                "time": (r.get("task") or {}).get("time"),
                "verdict_malicious": (r.get("verdicts", {}) or {}).get("malicious"),
                "tags": (r.get("task") or {}).get("tags"),
                "result_url": r.get("result"),
                "screenshot_url": r.get("screenshot"),
            }
            for r in results
        ],
    }
    print(json.dumps(out, indent=2))


def cmd_quota(args):
    resp = _request("GET", f"{API_BASE}/quotas/", dry_run=args.dry_run)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return
    out = {"source": "urlscan", "operation": "quota", "query_time": now_iso(), "quota": resp}
    print(json.dumps(out, indent=2))


def cmd_screenshot(args):
    url = f"https://urlscan.io/screenshots/{args.uuid}.png"
    if args.dry_run:
        print(json.dumps({
            "dry_run": True, "operation": "screenshot",
            "url": url, "out": args.out or "<stdout>"
        }, indent=2))
        return
    if not API_KEY:
        die("URLSCAN_API_KEY not set", 2)
    req = urllib.request.Request(url, headers={"API-Key": API_KEY})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        die(f"HTTP {e.code} fetching screenshot", 1)
    if args.out:
        with open(args.out, "wb") as f:
            f.write(data)
        print(json.dumps({"source": "urlscan", "operation": "screenshot", "uuid": args.uuid,
                          "saved_to": args.out, "bytes": len(data)}, indent=2))
    else:
        sys.stdout.buffer.write(data)


def cmd_dom(args):
    url = f"{API_BASE}/dom/{args.uuid}/"
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "dom", "url": url, "out": args.out or "<stdout>"}, indent=2))
        return
    if not API_KEY:
        die("URLSCAN_API_KEY not set", 2)
    req = urllib.request.Request(url, headers={"API-Key": API_KEY})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            content = r.read()
    except urllib.error.HTTPError as e:
        die(f"HTTP {e.code} fetching DOM", 1)
    if args.out:
        with open(args.out, "wb") as f:
            f.write(content)
        print(json.dumps({"source": "urlscan", "operation": "dom", "uuid": args.uuid,
                          "saved_to": args.out, "bytes": len(content)}, indent=2))
    else:
        sys.stdout.buffer.write(content)


def main():
    ap = argparse.ArgumentParser(
        prog="urlscan.py",
        description="URLScan.io API v1 CLI (stdlib only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_sub = sub.add_parser("submit", help="submit a URL for scanning")
    p_sub.add_argument("url")
    p_sub.add_argument("--visibility", choices=["unlisted", "public", "private"], default="unlisted")
    p_sub.add_argument("--country", help="2-letter country code for the scan source")
    p_sub.add_argument("--user-agent", help="custom user-agent")
    p_sub.add_argument("--tags", help="comma-separated tags")
    p_sub.add_argument("--referer", help="custom referer header")
    p_sub.add_argument("--wait", action="store_true", help="poll for result after submission")
    p_sub.add_argument("--dry-run", action="store_true")
    p_sub.set_defaults(func=cmd_submit)

    p_res = sub.add_parser("result", help="retrieve a scan result by UUID")
    p_res.add_argument("uuid")
    p_res.add_argument("--dry-run", action="store_true")
    p_res.set_defaults(func=cmd_result)

    p_search = sub.add_parser("search", help="Lucene-style search across past scans")
    p_search.add_argument("query")
    p_search.add_argument("--size", type=int, default=20)
    p_search.add_argument("--dry-run", action="store_true")
    p_search.set_defaults(func=cmd_search)

    p_quota = sub.add_parser("quota", help="show your remaining API quota")
    p_quota.add_argument("--dry-run", action="store_true")
    p_quota.set_defaults(func=cmd_quota)

    p_shot = sub.add_parser("screenshot", help="download the screenshot PNG for a scan")
    p_shot.add_argument("uuid")
    p_shot.add_argument("--out", help="output file path (default: stdout)")
    p_shot.add_argument("--dry-run", action="store_true")
    p_shot.set_defaults(func=cmd_screenshot)

    p_dom = sub.add_parser("dom", help="download the captured DOM/HTML for a scan")
    p_dom.add_argument("uuid")
    p_dom.add_argument("--out", help="output file path (default: stdout)")
    p_dom.add_argument("--dry-run", action="store_true")
    p_dom.set_defaults(func=cmd_dom)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
