#!/usr/bin/env python3
"""
abuseipdb.py — AbuseIPDB APIv2 CLI (stdlib only, no install).

Covers the four read-only endpoints documented at https://docs.abuseipdb.com/:

  check        — IP reputation summary
  reports      — paginated report history for an IP
  check-block  — reputation summary for a CIDR block
  blacklist    — bulk download of high-confidence blacklisted IPs

Write endpoints (report, bulk-report, clear-address) are intentionally
NOT exposed here — this CLI is for retrieval only. To contribute reports
back to AbuseIPDB, use their web UI or a separate purpose-built script.

Usage:
  abuseipdb.py check <ip> [--max-age-in-days N] [--verbose] [--dry-run]
  abuseipdb.py reports <ip> [--max-age-in-days N] [--per-page N] [--page N] [--dry-run]
  abuseipdb.py check-block <cidr> [--max-age-in-days N] [--dry-run]
  abuseipdb.py blacklist [--confidence-min N] [--limit N] [--ip-version {4,6}]
                         [--except-country CC,CC,...] [--only-countries CC,CC,...]
                         [--dry-run]

Exit codes:
  0  success
  1  network / API error
  2  missing ABUSEIPDB_API_KEY (only when not --dry-run)
  3  bad arguments
"""

import argparse
import ipaddress
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API_KEY = os.environ.get("ABUSEIPDB_API_KEY", "")
API_BASE = "https://api.abuseipdb.com/api/v2"


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def is_ip(s):
    try:
        ipaddress.ip_address(s)
        return True
    except ValueError:
        return False


def is_cidr(s):
    try:
        ipaddress.ip_network(s, strict=False)
        return "/" in s
    except ValueError:
        return False


def request(path, params=None, dry_run=False):
    """GET an AbuseIPDB endpoint. Returns parsed JSON dict on success."""
    qs = urllib.parse.urlencode(params or {}, doseq=True)
    url = f"{API_BASE}{path}" + (f"?{qs}" if qs else "")

    if dry_run:
        return {
            "dry_run": True,
            "method": "GET",
            "url": url,
            "headers": {"Key": "<redacted>" if API_KEY else "<unset>", "Accept": "application/json"},
        }

    if not API_KEY:
        die("ABUSEIPDB_API_KEY not set. Run /cti-setup or ./scripts/setup.sh", 2)

    req = urllib.request.Request(
        url,
        headers={"Key": API_KEY, "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode("utf-8")
        return json.loads(body)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        die(f"HTTP {e.code}: {body[:300]}", 1)
    except urllib.error.URLError as e:
        die(f"network error: {e.reason}", 1)
    except json.JSONDecodeError as e:
        die(f"invalid JSON response: {e}", 1)


def cmd_check(args):
    if not is_ip(args.ip):
        die(f"not an IP address: {args.ip}", 3)
    params = {"ipAddress": args.ip, "maxAgeInDays": args.max_age_in_days}
    if args.verbose:
        params["verbose"] = ""
    resp = request("/check", params, dry_run=args.dry_run)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return

    d = resp.get("data") or {}
    out = {
        "source": "abuseipdb",
        "operation": "check",
        "indicator": args.ip,
        "type": "ip",
        "query_time": now_iso(),
        "abuse_confidence": d.get("abuseConfidenceScore"),
        "total_reports": d.get("totalReports"),
        "distinct_reporters": d.get("numDistinctUsers"),
        "last_reported": d.get("lastReportedAt"),
        "isp": d.get("isp"),
        "usage_type": d.get("usageType"),
        "country": d.get("countryCode"),
        "domain": d.get("domain"),
        "hostnames": d.get("hostnames"),
        "is_tor": d.get("isTor"),
        "is_whitelisted": d.get("isWhitelisted"),
        "is_public": d.get("isPublic"),
        "ip_version": d.get("ipVersion"),
    }
    if args.verbose:
        out["reports"] = d.get("reports", [])
    print(json.dumps(out, indent=2))


def cmd_reports(args):
    if not is_ip(args.ip):
        die(f"not an IP address: {args.ip}", 3)
    params = {
        "ipAddress": args.ip,
        "maxAgeInDays": args.max_age_in_days,
        "perPage": args.per_page,
        "page": args.page,
    }
    resp = request("/reports", params, dry_run=args.dry_run)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return

    d = resp.get("data") or {}
    out = {
        "source": "abuseipdb",
        "operation": "reports",
        "indicator": args.ip,
        "query_time": now_iso(),
        "total": d.get("total"),
        "page": d.get("page"),
        "count": d.get("count"),
        "per_page": d.get("perPage"),
        "last_page": d.get("lastPage"),
        "next_page_url": d.get("nextPageUrl"),
        "previous_page_url": d.get("previousPageUrl"),
        "results": d.get("results", []),
    }
    print(json.dumps(out, indent=2))


def cmd_check_block(args):
    if not is_cidr(args.cidr):
        die(f"not a CIDR block: {args.cidr}", 3)
    params = {"network": args.cidr, "maxAgeInDays": args.max_age_in_days}
    resp = request("/check-block", params, dry_run=args.dry_run)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return

    d = resp.get("data") or {}
    out = {
        "source": "abuseipdb",
        "operation": "check-block",
        "network": args.cidr,
        "query_time": now_iso(),
        "network_address": d.get("networkAddress"),
        "netmask": d.get("netmask"),
        "min_address": d.get("minAddress"),
        "max_address": d.get("maxAddress"),
        "num_possible_hosts": d.get("numPossibleHosts"),
        "address_space_desc": d.get("addressSpaceDesc"),
        "reported_address_count": len(d.get("reportedAddress", [])),
        "reported_addresses": d.get("reportedAddress", []),
    }
    print(json.dumps(out, indent=2))


def cmd_blacklist(args):
    params = {}
    if args.confidence_min is not None:
        params["confidenceMinimum"] = args.confidence_min
    if args.limit is not None:
        params["limit"] = args.limit
    if args.ip_version:
        params["ipVersion"] = args.ip_version
    if args.except_country:
        params["exceptCountries"] = args.except_country
    if args.only_countries:
        params["onlyCountries"] = args.only_countries
    resp = request("/blacklist", params, dry_run=args.dry_run)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return

    meta = resp.get("meta") or {}
    data = resp.get("data") or []
    out = {
        "source": "abuseipdb",
        "operation": "blacklist",
        "query_time": now_iso(),
        "generated_at": meta.get("generatedAt"),
        "count": len(data),
        "params": params,
        "results": data,
    }
    print(json.dumps(out, indent=2))


def main():
    ap = argparse.ArgumentParser(
        prog="abuseipdb.py",
        description="AbuseIPDB APIv2 CLI (read-only endpoints)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check", help="IP reputation summary")
    p_check.add_argument("ip")
    p_check.add_argument("--max-age-in-days", type=int, default=90)
    p_check.add_argument("--verbose", action="store_true",
                         help="include detailed report list (uses more of your daily quota's payload)")
    p_check.add_argument("--dry-run", action="store_true")
    p_check.set_defaults(func=cmd_check)

    p_reports = sub.add_parser("reports", help="paginated report history for an IP")
    p_reports.add_argument("ip")
    p_reports.add_argument("--max-age-in-days", type=int, default=90)
    p_reports.add_argument("--per-page", type=int, default=25)
    p_reports.add_argument("--page", type=int, default=1)
    p_reports.add_argument("--dry-run", action="store_true")
    p_reports.set_defaults(func=cmd_reports)

    p_block = sub.add_parser("check-block", help="reputation summary for a CIDR block")
    p_block.add_argument("cidr")
    p_block.add_argument("--max-age-in-days", type=int, default=30)
    p_block.add_argument("--dry-run", action="store_true")
    p_block.set_defaults(func=cmd_check_block)

    p_bl = sub.add_parser("blacklist", help="download high-confidence blacklisted IPs")
    p_bl.add_argument("--confidence-min", type=int, default=None,
                      help="minimum abuse confidence (default API: 100)")
    p_bl.add_argument("--limit", type=int, default=None,
                      help="max IPs to return (default API: 10000)")
    p_bl.add_argument("--ip-version", choices=["4", "6"], default=None)
    p_bl.add_argument("--except-country", default=None,
                      help="comma-separated country codes to EXCLUDE (e.g. US,CA)")
    p_bl.add_argument("--only-countries", default=None,
                      help="comma-separated country codes to INCLUDE")
    p_bl.add_argument("--dry-run", action="store_true")
    p_bl.set_defaults(func=cmd_blacklist)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
