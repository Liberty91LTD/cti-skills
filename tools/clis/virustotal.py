#!/usr/bin/env python3
"""
virustotal.py — VirusTotal API v3 CLI (stdlib only, no install).

Covers reputation lookup, relationship traversal (the key pivoting capability
the Node CLI lacks), URL submission, comments, and Intel search.

API reference: https://gtidocs.virustotal.com/reference/api-responses
Auth header: x-apikey: $VIRUSTOTAL_API_KEY

Usage:
  virustotal.py file <hash> [--relationships R1,R2,...] [--limit N] [--dry-run]
  virustotal.py ip <ip> [--relationships R1,R2,...] [--limit N] [--dry-run]
  virustotal.py domain <domain> [--relationships R1,R2,...] [--limit N] [--dry-run]
  virustotal.py url <url> [--relationships R1,R2,...] [--limit N] [--dry-run]
  virustotal.py submit-url <url> [--dry-run]
  virustotal.py comments <type> <id> [--limit N] [--dry-run]
  virustotal.py search <query> [--limit N] [--dry-run]   # premium endpoint

Common relationships (each costs one API request):
  file    contacted_ips, contacted_domains, contacted_urls, dropped_files,
          similar_files, behaviours, bundled_files, execution_parents
  ip      communicating_files, downloaded_files, resolutions, urls,
          related_threat_actors, historical_whois
  domain  subdomains, resolutions, communicating_files, downloaded_files,
          urls, siblings, related_threat_actors, historical_whois
  url     contacted_ips, contacted_domains, downloaded_files,
          last_serving_ip_address

Free tier: 4 req/min, 500/day. Each --relationships entry is a SEPARATE
request, so be deliberate. Use --dry-run to preview the call plan.

Exit codes:
  0  success
  1  network / API error (incl. 429 rate limit)
  2  missing VIRUSTOTAL_API_KEY (only when not --dry-run)
  3  bad arguments
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API_KEY = os.environ.get("VIRUSTOTAL_API_KEY", "")
API_BASE = "https://www.virustotal.com/api/v3"


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def url_id(url):
    """VT v3 URL identifier: unpadded base64url of the URL."""
    return base64.urlsafe_b64encode(url.encode("utf-8")).rstrip(b"=").decode("ascii")


def _request(method, path, body=None, params=None, dry_run=False):
    qs = ("?" + urllib.parse.urlencode(params)) if params else ""
    url = f"{API_BASE}{path}{qs}"

    if dry_run:
        return {
            "dry_run": True,
            "method": method,
            "url": url,
            "headers": {"x-apikey": "<redacted>" if API_KEY else "<unset>", "Accept": "application/json"},
            "body_present": body is not None,
        }

    if not API_KEY:
        die("VIRUSTOTAL_API_KEY not set. Run /cti-setup or ./scripts/setup.sh", 2)

    data = None
    headers = {"x-apikey": API_KEY, "Accept": "application/json"}
    if body is not None:
        if isinstance(body, dict):
            data = urllib.parse.urlencode(body).encode("utf-8")
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            data = body.encode("utf-8") if isinstance(body, str) else body

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode("utf-8", errors="replace") if e.fp else ""
        if e.code == 429:
            die("rate limited (429). Free tier is 4/min, 500/day. Back off and retry.", 1)
        die(f"HTTP {e.code}: {body_txt[:300]}", 1)
    except urllib.error.URLError as e:
        die(f"network error: {e.reason}", 1)
    except json.JSONDecodeError as e:
        die(f"invalid JSON: {e}", 1)


def _summarise_object(obj):
    """Distil the noisy VT object envelope into a small dict."""
    if not obj:
        return None
    attrs = (obj.get("data") or obj).get("attributes") if isinstance(obj.get("data") or obj, dict) else {}
    if not attrs:
        return obj
    stats = attrs.get("last_analysis_stats", {}) or {}
    total = sum(v for v in stats.values() if isinstance(v, int))
    malicious = stats.get("malicious", 0)
    suspicious = stats.get("suspicious", 0)
    verdict = "unknown"
    if malicious >= 5:
        verdict = "malicious"
    elif malicious >= 1 or suspicious >= 2:
        verdict = "suspicious"
    elif total >= 10:
        verdict = "clean"
    return {
        "id": (obj.get("data") or obj).get("id") if isinstance(obj.get("data") or obj, dict) else None,
        "type": (obj.get("data") or obj).get("type") if isinstance(obj.get("data") or obj, dict) else None,
        "detection_ratio": f"{malicious}/{total}" if total else None,
        "verdict": verdict,
        "community_score": attrs.get("reputation"),
        "tags": attrs.get("tags"),
        "as_owner": attrs.get("as_owner"),
        "country": attrs.get("country"),
        "names": (attrs.get("names") or [None])[:5],
        "type_description": attrs.get("type_description"),
        "popular_threat_label": (attrs.get("popular_threat_classification") or {}).get("suggested_threat_label"),
        "registrar": attrs.get("registrar"),
        "creation_date": attrs.get("creation_date"),
        "last_analysis_date": attrs.get("last_analysis_date"),
    }


def _path_for(type_, value):
    if type_ == "ip":
        return f"/ip_addresses/{urllib.parse.quote(value, safe='')}"
    if type_ == "domain":
        return f"/domains/{urllib.parse.quote(value, safe='')}"
    if type_ in ("file", "hash"):
        return f"/files/{urllib.parse.quote(value, safe='')}"
    if type_ == "url":
        return f"/urls/{url_id(value)}"
    die(f"unknown type: {type_}", 3)


def _do_lookup(type_, value, relationships, limit, dry_run):
    base_path = _path_for(type_, value)
    obj_resp = _request("GET", base_path, dry_run=dry_run)

    out = {
        "source": "virustotal",
        "operation": f"{type_}_lookup",
        "indicator": value,
        "type": type_,
        "query_time": now_iso(),
    }
    if dry_run:
        out["calls"] = [obj_resp]
        for rel in relationships:
            out["calls"].append(_request("GET", f"{base_path}/{rel}", params={"limit": limit}, dry_run=True))
        print(json.dumps(out, indent=2))
        return

    out["object"] = _summarise_object(obj_resp)
    out["raw_attributes"] = (obj_resp.get("data") or {}).get("attributes")

    if relationships:
        out["relationships"] = {}
        for rel in relationships:
            try:
                rel_resp = _request("GET", f"{base_path}/{rel}", params={"limit": limit})
                items = rel_resp.get("data") or []
                out["relationships"][rel] = {
                    "count": len(items),
                    "items": [_summarise_object({"data": i}) or {"id": i.get("id"), "type": i.get("type")} for i in items],
                }
            except SystemExit:
                raise
            except Exception as e:
                out["relationships"][rel] = {"error": str(e)}

    print(json.dumps(out, indent=2))


def cmd_file(args):
    rels = [r.strip() for r in (args.relationships or "").split(",") if r.strip()]
    _do_lookup("file", args.hash, rels, args.limit, args.dry_run)


def cmd_ip(args):
    rels = [r.strip() for r in (args.relationships or "").split(",") if r.strip()]
    _do_lookup("ip", args.ip, rels, args.limit, args.dry_run)


def cmd_domain(args):
    rels = [r.strip() for r in (args.relationships or "").split(",") if r.strip()]
    _do_lookup("domain", args.domain, rels, args.limit, args.dry_run)


def cmd_url(args):
    rels = [r.strip() for r in (args.relationships or "").split(",") if r.strip()]
    _do_lookup("url", args.url, rels, args.limit, args.dry_run)


def cmd_submit_url(args):
    resp = _request("POST", "/urls", body={"url": args.url}, dry_run=args.dry_run)
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "submit-url", "url": args.url, "call": resp}, indent=2))
        return
    analysis_id = (resp.get("data") or {}).get("id")
    out = {
        "source": "virustotal",
        "operation": "submit-url",
        "url": args.url,
        "query_time": now_iso(),
        "analysis_id": analysis_id,
        "raw": resp,
    }
    print(json.dumps(out, indent=2))


def cmd_comments(args):
    base_path = _path_for(args.type, args.id)
    resp = _request("GET", f"{base_path}/comments", params={"limit": args.limit}, dry_run=args.dry_run)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return
    items = resp.get("data") or []
    out = {
        "source": "virustotal",
        "operation": "comments",
        "object_type": args.type,
        "object_id": args.id,
        "query_time": now_iso(),
        "count": len(items),
        "comments": [
            {
                "id": c.get("id"),
                "date": (c.get("attributes") or {}).get("date"),
                "votes": (c.get("attributes") or {}).get("votes"),
                "text": (c.get("attributes") or {}).get("text"),
            }
            for c in items
        ],
    }
    print(json.dumps(out, indent=2))


def cmd_search(args):
    resp = _request("GET", "/intelligence/search",
                    params={"query": args.query, "limit": args.limit},
                    dry_run=args.dry_run)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return
    items = resp.get("data") or []
    out = {
        "source": "virustotal",
        "operation": "intel_search",
        "query": args.query,
        "query_time": now_iso(),
        "count": len(items),
        "results": [{"id": i.get("id"), "type": i.get("type"), "summary": _summarise_object({"data": i})} for i in items],
    }
    print(json.dumps(out, indent=2))


def main():
    ap = argparse.ArgumentParser(
        prog="virustotal.py",
        description="VirusTotal API v3 CLI (stdlib only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    def _add_lookup(name, arg_name, help_text):
        p = sub.add_parser(name, help=help_text)
        p.add_argument(arg_name)
        p.add_argument("--relationships", help="comma-separated relationships to fetch (each is a separate API call)")
        p.add_argument("--limit", type=int, default=20, help="max items per relationship (default 20)")
        p.add_argument("--dry-run", action="store_true")
        return p

    _add_lookup("file", "hash", "look up a file by MD5/SHA-1/SHA-256").set_defaults(func=cmd_file)
    _add_lookup("ip", "ip", "look up an IP address").set_defaults(func=cmd_ip)
    _add_lookup("domain", "domain", "look up a domain").set_defaults(func=cmd_domain)
    _add_lookup("url", "url", "look up a URL").set_defaults(func=cmd_url)

    p_sub = sub.add_parser("submit-url", help="submit a URL for analysis")
    p_sub.add_argument("url")
    p_sub.add_argument("--dry-run", action="store_true")
    p_sub.set_defaults(func=cmd_submit_url)

    p_com = sub.add_parser("comments", help="list comments on an object")
    p_com.add_argument("type", choices=["file", "ip", "domain", "url"])
    p_com.add_argument("id")
    p_com.add_argument("--limit", type=int, default=20)
    p_com.add_argument("--dry-run", action="store_true")
    p_com.set_defaults(func=cmd_comments)

    p_search = sub.add_parser("search", help="VT Intelligence search (premium endpoint)")
    p_search.add_argument("query")
    p_search.add_argument("--limit", type=int, default=20)
    p_search.add_argument("--dry-run", action="store_true")
    p_search.set_defaults(func=cmd_search)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
