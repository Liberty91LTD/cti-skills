#!/usr/bin/env python3
"""
shodan.py — Shodan CLI using the official shodan-python SDK.

The Node CLI does host lookup. The Python CLI exposes the full search,
faceting, DNS, and account surface — the parts of Shodan that turn an IP
lookup into infrastructure mapping.

SDK reference: https://github.com/achillean/shodan-python
Docs:          https://shodan.readthedocs.io/

Self-bootstraps a private venv at tools/clis/.venv-shodan/ on first run.

Usage:
  shodan.py host <ip> [--history] [--minify] [--dry-run]
  shodan.py search "<query>" [--limit N] [--page N] [--facets F1:N,F2:N] [--dry-run]
  shodan.py count "<query>" [--facets F1:N,F2:N] [--dry-run]
  shodan.py dns resolve <hostname[,hostname...]> [--dry-run]
  shodan.py dns reverse <ip[,ip...]> [--dry-run]
  shodan.py dns domain <domain> [--dry-run]
  shodan.py info [--dry-run]
  shodan.py ports [--dry-run]
  shodan.py services [--dry-run]

Search query examples:
  product:"Cobalt Strike Team Server"
  hash:5e884898 country:RU
  ssl.cert.subject.CN:"badcorp.example"
  port:22 country:CN org:"Hosting Provider"
  http.title:"Login Page" http.html:phishkit-string
  vuln:CVE-2024-21887

Each search uses query credits. Use `count` first to estimate scope. Free
plans have very limited credits — `info` will show your current balance.

Exit codes:
  0  success
  1  network / API error
  2  missing SHODAN_API_KEY (only when not --dry-run)
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
VENV_DIR = SCRIPT_DIR / ".venv-shodan"
VENV_PY = VENV_DIR / "bin" / "python"


def _bootstrap_venv():
    print(f"first run: creating Python venv at {VENV_DIR} and installing shodan SDK...", file=sys.stderr)
    subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)],
                          stdout=subprocess.DEVNULL)
    subprocess.check_call([str(VENV_PY), "-m", "pip", "install", "--quiet",
                           "--disable-pip-version-check", "shodan"])
    print("bootstrap complete.", file=sys.stderr)


if os.environ.get("CTI_SHODAN_VENV") != "1":
    if not VENV_PY.exists():
        _bootstrap_venv()
    os.environ["CTI_SHODAN_VENV"] = "1"
    os.execv(str(VENV_PY), [str(VENV_PY), str(pathlib.Path(__file__).resolve())] + sys.argv[1:])

# ---------------------------------------------------------------------------
# Inside venv from here on.
# Important: this script is named shodan.py, which shadows the `shodan`
# package on sys.path[0]. Remove our own directory from sys.path before
# importing the SDK so Python finds the venv-installed package.
# ---------------------------------------------------------------------------
import argparse
import json
from datetime import datetime, timezone

sys.path = [p for p in sys.path if pathlib.Path(p or ".").resolve() != SCRIPT_DIR]

import shodan
import shodan.exception


API_KEY = os.environ.get("SHODAN_API_KEY", "")


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def make_client():
    if not API_KEY:
        die("SHODAN_API_KEY not set. Run /cti-setup or ./scripts/setup.sh", 2)
    return shodan.Shodan(API_KEY)


def parse_facets(s):
    """'product:5,country:10' → [('product', 5), ('country', 10)]"""
    if not s:
        return None
    out = []
    for part in s.split(","):
        if ":" in part:
            name, n = part.split(":", 1)
            out.append((name.strip(), int(n)))
        else:
            out.append(part.strip())
    return out


def _service_summary(svc):
    """Reduce a single service entry to the bits an analyst usually wants."""
    data = svc.get("data", "")
    if isinstance(data, str) and len(data) > 400:
        data = data[:400] + "..."
    return {
        "port": svc.get("port"),
        "transport": svc.get("transport"),
        "product": svc.get("product"),
        "version": svc.get("version"),
        "module": svc.get("_shodan", {}).get("module"),
        "ip_str": svc.get("ip_str"),
        "hostnames": svc.get("hostnames"),
        "domains": svc.get("domains"),
        "tags": svc.get("tags"),
        "ssl_subject": (svc.get("ssl") or {}).get("cert", {}).get("subject", {}).get("CN") if svc.get("ssl") else None,
        "ssl_issuer": (svc.get("ssl") or {}).get("cert", {}).get("issuer", {}).get("CN") if svc.get("ssl") else None,
        "http_title": (svc.get("http") or {}).get("title"),
        "http_server": (svc.get("http") or {}).get("server"),
        "banner": data if isinstance(data, str) else None,
        "timestamp": svc.get("timestamp"),
        "vulns": list(svc.get("vulns", {}).keys()) if isinstance(svc.get("vulns"), dict) else svc.get("vulns"),
    }


def _host_summary(h):
    services = h.get("data", []) or []
    return {
        "ip_str": h.get("ip_str"),
        "country": h.get("country_name"),
        "city": h.get("city"),
        "org": h.get("org"),
        "isp": h.get("isp"),
        "asn": h.get("asn"),
        "os": h.get("os"),
        "hostnames": h.get("hostnames"),
        "domains": h.get("domains"),
        "tags": h.get("tags"),
        "ports": h.get("ports"),
        "vulns": h.get("vulns"),
        "last_update": h.get("last_update"),
        "service_count": len(services),
        "services": [_service_summary(s) for s in services[:20]],
    }


def cmd_host(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "host", "ip": args.ip,
                          "history": args.history, "minify": args.minify}, indent=2))
        return
    api = make_client()
    try:
        h = api.host(args.ip, history=args.history, minify=args.minify)
    except shodan.exception.APIError as e:
        die(f"Shodan API error: {e}", 1)
    print(json.dumps({"source": "shodan", "operation": "host",
                      "indicator": args.ip, "query_time": now_iso(),
                      "host": _host_summary(h)}, indent=2, default=str))


def cmd_search(args):
    facets = parse_facets(args.facets)
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "search", "query": args.query,
                          "limit": args.limit, "page": args.page, "facets": facets}, indent=2))
        return
    api = make_client()
    try:
        kwargs = {"page": args.page}
        if args.limit is not None:
            kwargs["limit"] = args.limit
        if facets:
            kwargs["facets"] = facets
        results = api.search(args.query, **kwargs)
    except shodan.exception.APIError as e:
        die(f"Shodan API error: {e}", 1)

    matches = results.get("matches", [])
    out = {
        "source": "shodan",
        "operation": "search",
        "query": args.query,
        "query_time": now_iso(),
        "total": results.get("total"),
        "facets": results.get("facets"),
        "match_count": len(matches),
        "matches": [_service_summary(m) for m in matches],
    }
    print(json.dumps(out, indent=2, default=str))


def cmd_count(args):
    facets = parse_facets(args.facets)
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "count", "query": args.query,
                          "facets": facets}, indent=2))
        return
    api = make_client()
    try:
        results = api.count(args.query, facets=facets)
    except shodan.exception.APIError as e:
        die(f"Shodan API error: {e}", 1)
    print(json.dumps({"source": "shodan", "operation": "count",
                      "query": args.query, "query_time": now_iso(),
                      "total": results.get("total"),
                      "facets": results.get("facets")}, indent=2, default=str))


def cmd_dns_resolve(args):
    hostnames = [h.strip() for h in args.hostnames.split(",") if h.strip()]
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "dns_resolve",
                          "hostnames": hostnames}, indent=2))
        return
    api = make_client()
    try:
        results = api.dns.resolve(hostnames)
    except shodan.exception.APIError as e:
        die(f"Shodan API error: {e}", 1)
    print(json.dumps({"source": "shodan", "operation": "dns_resolve",
                      "query_time": now_iso(), "results": results}, indent=2))


def cmd_dns_reverse(args):
    ips = [i.strip() for i in args.ips.split(",") if i.strip()]
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "dns_reverse", "ips": ips}, indent=2))
        return
    api = make_client()
    try:
        results = api.dns.reverse(ips)
    except shodan.exception.APIError as e:
        die(f"Shodan API error: {e}", 1)
    print(json.dumps({"source": "shodan", "operation": "dns_reverse",
                      "query_time": now_iso(), "results": results}, indent=2))


def cmd_dns_domain(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "dns_domain_info",
                          "domain": args.domain}, indent=2))
        return
    api = make_client()
    try:
        results = api.dns.domain_info(args.domain)
    except shodan.exception.APIError as e:
        die(f"Shodan API error: {e}", 1)
    print(json.dumps({"source": "shodan", "operation": "dns_domain_info",
                      "domain": args.domain, "query_time": now_iso(),
                      "info": results}, indent=2, default=str))


def cmd_info(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "info"}, indent=2))
        return
    api = make_client()
    try:
        info = api.info()
    except shodan.exception.APIError as e:
        die(f"Shodan API error: {e}", 1)
    print(json.dumps({"source": "shodan", "operation": "info",
                      "query_time": now_iso(), "account": info}, indent=2, default=str))


def cmd_ports(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "ports"}, indent=2))
        return
    api = make_client()
    try:
        ports = api.ports()
    except shodan.exception.APIError as e:
        die(f"Shodan API error: {e}", 1)
    print(json.dumps({"source": "shodan", "operation": "ports",
                      "query_time": now_iso(), "count": len(ports),
                      "ports": ports}, indent=2))


def cmd_services(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "services"}, indent=2))
        return
    api = make_client()
    try:
        services = api.services()
    except shodan.exception.APIError as e:
        die(f"Shodan API error: {e}", 1)
    print(json.dumps({"source": "shodan", "operation": "services",
                      "query_time": now_iso(), "services": services}, indent=2, default=str))


def main():
    ap = argparse.ArgumentParser(
        prog="shodan.py",
        description="Shodan CLI (uses official shodan-python SDK)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_host = sub.add_parser("host", help="full host detail for an IP")
    p_host.add_argument("ip")
    p_host.add_argument("--history", action="store_true",
                        help="include historical banners (paid plans)")
    p_host.add_argument("--minify", action="store_true",
                        help="reduced banner detail (saves credits on some plans)")
    p_host.add_argument("--dry-run", action="store_true")
    p_host.set_defaults(func=cmd_host)

    p_search = sub.add_parser("search", help="search Shodan with a query")
    p_search.add_argument("query")
    p_search.add_argument("--limit", type=int, default=20)
    p_search.add_argument("--page", type=int, default=1)
    p_search.add_argument("--facets", help="comma list 'name:size' (e.g. country:5,org:5)")
    p_search.add_argument("--dry-run", action="store_true")
    p_search.set_defaults(func=cmd_search)

    p_count = sub.add_parser("count", help="count matches without spending result credits")
    p_count.add_argument("query")
    p_count.add_argument("--facets", help="comma list 'name:size'")
    p_count.add_argument("--dry-run", action="store_true")
    p_count.set_defaults(func=cmd_count)

    p_dns = sub.add_parser("dns", help="DNS operations")
    p_dns_sub = p_dns.add_subparsers(dest="dns_cmd", required=True)

    p_resolve = p_dns_sub.add_parser("resolve", help="forward DNS for one or more hostnames")
    p_resolve.add_argument("hostnames", help="comma-separated hostnames")
    p_resolve.add_argument("--dry-run", action="store_true")
    p_resolve.set_defaults(func=cmd_dns_resolve)

    p_reverse = p_dns_sub.add_parser("reverse", help="reverse DNS for one or more IPs")
    p_reverse.add_argument("ips", help="comma-separated IPs")
    p_reverse.add_argument("--dry-run", action="store_true")
    p_reverse.set_defaults(func=cmd_dns_reverse)

    p_domain = p_dns_sub.add_parser("domain", help="subdomain + DNS-record info for a domain")
    p_domain.add_argument("domain")
    p_domain.add_argument("--dry-run", action="store_true")
    p_domain.set_defaults(func=cmd_dns_domain)

    p_info = sub.add_parser("info", help="account info, plan, query credits remaining")
    p_info.add_argument("--dry-run", action="store_true")
    p_info.set_defaults(func=cmd_info)

    p_ports = sub.add_parser("ports", help="list of all ports Shodan scans")
    p_ports.add_argument("--dry-run", action="store_true")
    p_ports.set_defaults(func=cmd_ports)

    p_services = sub.add_parser("services", help="list of all services Shodan recognises")
    p_services.add_argument("--dry-run", action="store_true")
    p_services.set_defaults(func=cmd_services)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
