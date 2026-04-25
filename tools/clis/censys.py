#!/usr/bin/env python3
"""
censys.py — Censys CLI using the official censys-sdk-python.

The Node CLI does host view + basic search. The Python CLI exposes the full
SDK including certificate search, aggregations (free — count by facet without
spending result credits), and account info.

SDK reference: https://github.com/censys/censys-sdk-python
Docs:          https://docs.censys.com/reference/get-started

Self-bootstraps a private venv at tools/clis/.venv-censys/ on first run.

Usage:
  censys.py host <ip> [--dry-run]
  censys.py search "<query>" [--per-page N] [--pages N] [--dry-run]
  censys.py certs view <sha256_fingerprint> [--dry-run]
  censys.py certs search "<query>" [--per-page N] [--pages N] [--dry-run]
  censys.py aggregate "<query>" --field FIELD [--buckets N] [--dry-run]
  censys.py account [--dry-run]

QUOTA WARNING — free tier is 250 queries/month. Every host view, search page,
and certificate query costs one. Aggregations are free. Use --dry-run liberally.

Search query examples:
  services.service_name: HTTP and services.port: 8080
  services.tls.certificates.leaf_data.subject.common_name: "badcorp.example"
  services.banner: "OpenSSH_8.0" and location.country_code: RU
  autonomous_system.asn: 13335

Cert query examples:
  parsed.subject.common_name: "*.example.com"
  parsed.fingerprint_sha256: 5e884898...
  parsed.issuer.common_name: "Let's Encrypt"

Exit codes:
  0  success
  1  network / API error
  2  missing CENSYS_API_ID or CENSYS_API_SECRET (only when not --dry-run)
  3  bad arguments
"""

# ---------------------------------------------------------------------------
# Self-bootstrap
# ---------------------------------------------------------------------------
import os
import pathlib
import subprocess
import sys

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
VENV_DIR = SCRIPT_DIR / ".venv-censys"
VENV_PY = VENV_DIR / "bin" / "python"


def _bootstrap_venv():
    print(f"first run: creating Python venv at {VENV_DIR} and installing censys SDK...", file=sys.stderr)
    subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)],
                          stdout=subprocess.DEVNULL)
    subprocess.check_call([str(VENV_PY), "-m", "pip", "install", "--quiet",
                           "--disable-pip-version-check", "censys"])
    print("bootstrap complete.", file=sys.stderr)


if os.environ.get("CTI_CENSYS_VENV") != "1":
    if not VENV_PY.exists():
        _bootstrap_venv()
    os.environ["CTI_CENSYS_VENV"] = "1"
    os.execv(str(VENV_PY), [str(VENV_PY), str(pathlib.Path(__file__).resolve())] + sys.argv[1:])

# ---------------------------------------------------------------------------
# Inside venv from here on.
# Same self-shadowing fix as shodan.py: drop our own dir from sys.path so
# `import censys` finds the SDK package, not our script.
# ---------------------------------------------------------------------------
import argparse
import json
from datetime import datetime, timezone

sys.path = [p for p in sys.path if pathlib.Path(p or ".").resolve() != SCRIPT_DIR]

from censys.search import CensysHosts, CensysCerts
from censys.common.exceptions import CensysException


API_ID = os.environ.get("CENSYS_API_ID", "")
API_SECRET = os.environ.get("CENSYS_API_SECRET", "")


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def make_hosts_client():
    if not API_ID or not API_SECRET:
        die("CENSYS_API_ID and CENSYS_API_SECRET both required. Run /cti-setup or ./scripts/setup.sh", 2)
    return CensysHosts(api_id=API_ID, api_secret=API_SECRET)


def make_certs_client():
    if not API_ID or not API_SECRET:
        die("CENSYS_API_ID and CENSYS_API_SECRET both required.", 2)
    return CensysCerts(api_id=API_ID, api_secret=API_SECRET)


def _summarise_host(h):
    services = h.get("services") or []
    return {
        "ip": h.get("ip"),
        "last_updated": h.get("last_updated_at"),
        "country": (h.get("location") or {}).get("country_code"),
        "city": (h.get("location") or {}).get("city"),
        "asn": (h.get("autonomous_system") or {}).get("asn"),
        "as_name": (h.get("autonomous_system") or {}).get("name"),
        "service_count": len(services),
        "services": [
            {
                "port": s.get("port"),
                "service_name": s.get("service_name"),
                "transport": s.get("transport_protocol"),
                "software": [f"{sw.get('product','')} {sw.get('version','')}".strip() for sw in (s.get("software") or [])],
                "banner_excerpt": (s.get("banner") or "")[:300] if isinstance(s.get("banner"), str) else None,
                "tls_subject_cn": (((s.get("tls") or {}).get("certificates") or {}).get("leaf_data") or {})
                    .get("subject", {}).get("common_name", [None])[0],
                "tls_issuer": (((s.get("tls") or {}).get("certificates") or {}).get("leaf_data") or {})
                    .get("issuer", {}).get("common_name", [None])[0],
                "tls_fingerprint_sha256": (((s.get("tls") or {}).get("certificates") or {}).get("leaf_data") or {})
                    .get("fingerprint_sha256"),
            }
            for s in services[:20]
        ],
    }


def cmd_host(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "hosts.view", "ip": args.ip,
                          "cost": "1 query credit"}, indent=2))
        return
    api = make_hosts_client()
    try:
        h = api.view(args.ip)
    except CensysException as e:
        die(f"Censys API error: {e}", 1)
    print(json.dumps({"source": "censys", "operation": "host_view",
                      "indicator": args.ip, "query_time": now_iso(),
                      "host": _summarise_host(h)}, indent=2, default=str))


def cmd_search(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "hosts.search",
                          "query": args.query, "per_page": args.per_page,
                          "pages": args.pages,
                          "estimated_cost": f"up to {args.pages} query credits"}, indent=2))
        return
    api = make_hosts_client()
    try:
        cursor = api.search(args.query, per_page=args.per_page, pages=args.pages)
        hits = []
        for page in cursor:
            for hit in page:
                hits.append(hit)
    except CensysException as e:
        die(f"Censys API error: {e}", 1)
    out = {
        "source": "censys",
        "operation": "hosts_search",
        "query": args.query,
        "query_time": now_iso(),
        "count": len(hits),
        "hits": [_summarise_host(h) for h in hits],
    }
    print(json.dumps(out, indent=2, default=str))


def cmd_certs_view(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "certs.view",
                          "fingerprint": args.fingerprint, "cost": "1 query credit"}, indent=2))
        return
    api = make_certs_client()
    try:
        cert = api.view(args.fingerprint)
    except CensysException as e:
        die(f"Censys API error: {e}", 1)
    print(json.dumps({"source": "censys", "operation": "cert_view",
                      "fingerprint": args.fingerprint, "query_time": now_iso(),
                      "cert": cert}, indent=2, default=str))


def cmd_certs_search(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "certs.search",
                          "query": args.query, "per_page": args.per_page, "pages": args.pages,
                          "estimated_cost": f"up to {args.pages} query credits"}, indent=2))
        return
    api = make_certs_client()
    try:
        cursor = api.search(args.query, per_page=args.per_page, pages=args.pages)
        hits = []
        for page in cursor:
            for hit in page:
                hits.append(hit)
    except CensysException as e:
        die(f"Censys API error: {e}", 1)
    out = {
        "source": "censys",
        "operation": "certs_search",
        "query": args.query,
        "query_time": now_iso(),
        "count": len(hits),
        "hits": hits,
    }
    print(json.dumps(out, indent=2, default=str))


def cmd_aggregate(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "hosts.aggregate",
                          "query": args.query, "field": args.field, "buckets": args.buckets,
                          "cost": "FREE — does not consume query credits"}, indent=2))
        return
    api = make_hosts_client()
    try:
        result = api.aggregate(args.query, args.field, num_buckets=args.buckets)
    except CensysException as e:
        die(f"Censys API error: {e}", 1)
    print(json.dumps({"source": "censys", "operation": "hosts_aggregate",
                      "query": args.query, "field": args.field,
                      "query_time": now_iso(),
                      "result": result}, indent=2, default=str))


def cmd_account(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "account info"}, indent=2))
        return
    api = make_hosts_client()
    try:
        acct = api.account()
    except CensysException as e:
        die(f"Censys API error: {e}", 1)
    print(json.dumps({"source": "censys", "operation": "account",
                      "query_time": now_iso(), "account": acct}, indent=2, default=str))


def main():
    ap = argparse.ArgumentParser(
        prog="censys.py",
        description="Censys CLI (uses official censys-sdk-python). Free tier: 250 queries/month.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_host = sub.add_parser("host", help="view a single host by IP (1 credit)")
    p_host.add_argument("ip")
    p_host.add_argument("--dry-run", action="store_true")
    p_host.set_defaults(func=cmd_host)

    p_search = sub.add_parser("search", help="search hosts (1 credit per page)")
    p_search.add_argument("query")
    p_search.add_argument("--per-page", type=int, default=25)
    p_search.add_argument("--pages", type=int, default=1)
    p_search.add_argument("--dry-run", action="store_true")
    p_search.set_defaults(func=cmd_search)

    p_certs = sub.add_parser("certs", help="certificate operations")
    p_certs_sub = p_certs.add_subparsers(dest="certs_cmd", required=True)

    p_cert_view = p_certs_sub.add_parser("view", help="view certificate by SHA-256 fingerprint")
    p_cert_view.add_argument("fingerprint")
    p_cert_view.add_argument("--dry-run", action="store_true")
    p_cert_view.set_defaults(func=cmd_certs_view)

    p_cert_search = p_certs_sub.add_parser("search", help="search certificates")
    p_cert_search.add_argument("query")
    p_cert_search.add_argument("--per-page", type=int, default=25)
    p_cert_search.add_argument("--pages", type=int, default=1)
    p_cert_search.add_argument("--dry-run", action="store_true")
    p_cert_search.set_defaults(func=cmd_certs_search)

    p_agg = sub.add_parser("aggregate",
                           help="aggregate counts by field (FREE — no query credits)")
    p_agg.add_argument("query")
    p_agg.add_argument("--field", required=True,
                       help="field to aggregate by (e.g. location.country_code, services.port, autonomous_system.asn)")
    p_agg.add_argument("--buckets", type=int, default=20)
    p_agg.add_argument("--dry-run", action="store_true")
    p_agg.set_defaults(func=cmd_aggregate)

    p_acct = sub.add_parser("account", help="account info and remaining quota")
    p_acct.add_argument("--dry-run", action="store_true")
    p_acct.set_defaults(func=cmd_account)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
