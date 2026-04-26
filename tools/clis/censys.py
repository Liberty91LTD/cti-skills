#!/usr/bin/env python3
"""
censys.py — Censys Platform CLI using the official censys-platform SDK.

Uses the new Censys Platform API (PAT-authenticated). The legacy Search API
(api_id + api_secret with the `censys` package) is not supported here —
new accounts get a Personal Access Token from
https://accounts.censys.io/settings/personal-access-tokens.

SDK reference: pip package `censys-platform`
API docs:      https://docs.censys.com/reference/get-started

Self-bootstraps a private venv at tools/clis/.venv-censys/ on first run.

Usage:
  censys.py host <ip> [--at-time ISO8601] [--dry-run]
  censys.py timeline <ip> --start ISO8601 --end ISO8601 [--dry-run]
  censys.py services <ip> [--dry-run]
  censys.py search "<query>" [--page-size N] [--page-token TOKEN] [--fields F1,F2] [--dry-run]
  censys.py aggregate "<query>" --field FIELD [--buckets N] [--filter-by-query] [--dry-run]
  censys.py certs view <cert_id> [--dry-run]
  censys.py certs list <id1,id2,...> [--dry-run]

Auth: set $CENSYS_PAT to your Personal Access Token.

Search query examples (Censys Search Language):
  services.service_name: HTTP and services.port: 8080
  services.tls.certificates.leaf_data.subject.common_name: "badcorp.example"
  services.banner: "OpenSSH_8.0" and location.country_code: RU
  autonomous_system.asn: 13335

Free aggregations stay free in the new platform — use them generously.

Exit codes:
  0  success
  1  network / API error
  2  missing CENSYS_PAT (only when not --dry-run)
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
    print(f"first run: creating Python venv at {VENV_DIR} and installing censys-platform SDK...", file=sys.stderr)
    subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)],
                          stdout=subprocess.DEVNULL)
    subprocess.check_call([str(VENV_PY), "-m", "pip", "install", "--quiet",
                           "--disable-pip-version-check", "censys-platform"])
    print("bootstrap complete.", file=sys.stderr)


if os.environ.get("CTI_CENSYS_VENV") != "1":
    if not VENV_PY.exists():
        _bootstrap_venv()
    os.environ["CTI_CENSYS_VENV"] = "1"
    os.execv(str(VENV_PY), [str(VENV_PY), str(pathlib.Path(__file__).resolve())] + sys.argv[1:])

# ---------------------------------------------------------------------------
# Inside venv. sys.path fix to avoid censys.py self-shadowing.
# ---------------------------------------------------------------------------
import argparse
import json
from datetime import datetime, timezone

sys.path = [p for p in sys.path if pathlib.Path(p or ".").resolve() != SCRIPT_DIR]

from censys_platform import SDK, SDKError


PAT = os.environ.get("CENSYS_PAT", "")


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def make_sdk():
    if not PAT:
        die("CENSYS_PAT not set. Get a token at https://accounts.censys.io/settings/personal-access-tokens "
            "and run /cti-setup or ./scripts/setup.sh", 2)
    return SDK(personal_access_token=PAT)


def _to_dict(model):
    """Pydantic model → plain dict for JSON output."""
    if hasattr(model, "model_dump"):
        return model.model_dump(mode="json", exclude_none=True)
    if hasattr(model, "dict"):
        return model.dict(exclude_none=True)
    return model


def _extract_result(resp):
    """SDK responses are envelopes of shape {headers, result}. Drop headers
    and return only the result payload as a plain dict."""
    if hasattr(resp, "result"):
        inner = resp.result
        # Some endpoints nest one more level: result.result holds the payload.
        if inner is not None and hasattr(inner, "result"):
            return _to_dict(inner.result)
        return _to_dict(inner)
    return _to_dict(resp)


def _wrap(fn, **kwargs):
    try:
        return fn(**kwargs)
    except SDKError as e:
        msg = f"{e.status_code} {e.message}" if hasattr(e, "status_code") else str(e)
        die(f"Censys API error: {msg}", 1)
    except Exception as e:
        die(f"{type(e).__name__}: {e}", 1)


def _parse_iso(s):
    """Parse ISO 8601, accepting trailing Z."""
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)


# --- subcommands -----------------------------------------------------------

def cmd_host(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "global_data.get_host",
                          "host_id": args.ip, "at_time": args.at_time,
                          "cost": "1 query credit"}, indent=2))
        return
    sdk = make_sdk()
    kwargs = {"host_id": args.ip}
    if args.at_time:
        kwargs["at_time"] = _parse_iso(args.at_time)
    resp = _wrap(sdk.global_data.get_host, **kwargs)
    print(json.dumps({"source": "censys", "operation": "host",
                      "indicator": args.ip, "query_time": now_iso(),
                      "result": _extract_result(resp)}, indent=2, default=str))


def cmd_timeline(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "global_data.get_host_timeline",
                          "host_id": args.ip, "start": args.start, "end": args.end}, indent=2))
        return
    sdk = make_sdk()
    resp = _wrap(sdk.global_data.get_host_timeline,
                 host_id=args.ip,
                 start_time=_parse_iso(args.start),
                 end_time=_parse_iso(args.end))
    print(json.dumps({"source": "censys", "operation": "timeline",
                      "indicator": args.ip, "start": args.start, "end": args.end,
                      "query_time": now_iso(),
                      "result": _extract_result(resp)}, indent=2, default=str))


def cmd_services(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "global_data.list_services_on_host",
                          "host_id": args.ip}, indent=2))
        return
    sdk = make_sdk()
    from censys_platform.models.v3_globaldata_service_on_hostop import V3GlobaldataServiceOnHostRequest
    resp = _wrap(sdk.global_data.list_services_on_host,
                 request=V3GlobaldataServiceOnHostRequest(host_id=args.ip))
    print(json.dumps({"source": "censys", "operation": "services",
                      "indicator": args.ip, "query_time": now_iso(),
                      "result": _extract_result(resp)}, indent=2, default=str))


def cmd_search(args):
    fields = [f.strip() for f in args.fields.split(",")] if args.fields else None
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "global_data.search",
                          "query": args.query, "page_size": args.page_size,
                          "page_token": args.page_token, "fields": fields,
                          "estimated_cost": "1 query credit per page"}, indent=2))
        return
    sdk = make_sdk()
    body = {"query": args.query, "page_size": args.page_size}
    if args.page_token:
        body["page_token"] = args.page_token
    if fields:
        body["fields"] = fields
    resp = _wrap(sdk.global_data.search, search_query_input_body=body)
    print(json.dumps({"source": "censys", "operation": "search",
                      "query": args.query, "query_time": now_iso(),
                      "result": _extract_result(resp)}, indent=2, default=str))


def cmd_aggregate(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "global_data.aggregate",
                          "query": args.query, "field": args.field,
                          "buckets": args.buckets, "filter_by_query": args.filter_by_query,
                          "cost": "FREE — does not consume query credits"}, indent=2))
        return
    sdk = make_sdk()
    body = {
        "query": args.query,
        "field": args.field,
        "number_of_buckets": args.buckets,
    }
    if args.filter_by_query:
        body["filter_by_query"] = True
    resp = _wrap(sdk.global_data.aggregate, search_aggregate_input_body=body)
    print(json.dumps({"source": "censys", "operation": "aggregate",
                      "query": args.query, "field": args.field,
                      "query_time": now_iso(),
                      "result": _extract_result(resp)}, indent=2, default=str))


def cmd_cert_view(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "global_data.get_certificate",
                          "certificate_id": args.cert_id, "cost": "1 query credit"}, indent=2))
        return
    sdk = make_sdk()
    resp = _wrap(sdk.global_data.get_certificate, certificate_id=args.cert_id)
    print(json.dumps({"source": "censys", "operation": "certificate_view",
                      "certificate_id": args.cert_id, "query_time": now_iso(),
                      "result": _extract_result(resp)}, indent=2, default=str))


def cmd_cert_list(args):
    cert_ids = [c.strip() for c in args.cert_ids.split(",") if c.strip()]
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "global_data.get_certificates",
                          "certificate_ids": cert_ids}, indent=2))
        return
    sdk = make_sdk()
    resp = _wrap(sdk.global_data.get_certificates,
                 asset_certificate_list_input_body={"certificate_ids": cert_ids})
    print(json.dumps({"source": "censys", "operation": "certificate_list",
                      "query_time": now_iso(),
                      "result": _extract_result(resp)}, indent=2, default=str))


def main():
    ap = argparse.ArgumentParser(
        prog="censys.py",
        description="Censys Platform CLI (uses official censys-platform SDK + PAT auth)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_host = sub.add_parser("host", help="view a single host by IP (1 credit)")
    p_host.add_argument("ip")
    p_host.add_argument("--at-time", help="ISO 8601 timestamp for historical view")
    p_host.add_argument("--dry-run", action="store_true")
    p_host.set_defaults(func=cmd_host)

    p_tl = sub.add_parser("timeline", help="host activity timeline between two timestamps")
    p_tl.add_argument("ip")
    p_tl.add_argument("--start", required=True, help="ISO 8601 start time")
    p_tl.add_argument("--end", required=True, help="ISO 8601 end time")
    p_tl.add_argument("--dry-run", action="store_true")
    p_tl.set_defaults(func=cmd_timeline)

    p_svc = sub.add_parser("services", help="list services exposed on a host")
    p_svc.add_argument("ip")
    p_svc.add_argument("--dry-run", action="store_true")
    p_svc.set_defaults(func=cmd_services)

    p_search = sub.add_parser("search", help="search hosts (1 credit per page)")
    p_search.add_argument("query")
    p_search.add_argument("--page-size", type=int, default=25)
    p_search.add_argument("--page-token", help="continuation token from prior page")
    p_search.add_argument("--fields", help="comma-separated fields to include in result")
    p_search.add_argument("--dry-run", action="store_true")
    p_search.set_defaults(func=cmd_search)

    p_agg = sub.add_parser("aggregate", help="aggregate counts by field (FREE — no query credits)")
    p_agg.add_argument("query")
    p_agg.add_argument("--field", required=True,
                       help="field to aggregate by (e.g. location.country_code, services.port, autonomous_system.asn)")
    p_agg.add_argument("--buckets", type=int, default=20)
    p_agg.add_argument("--filter-by-query", action="store_true",
                       help="restrict bucket counts to results matching query")
    p_agg.add_argument("--dry-run", action="store_true")
    p_agg.set_defaults(func=cmd_aggregate)

    p_certs = sub.add_parser("certs", help="certificate operations")
    p_certs_sub = p_certs.add_subparsers(dest="certs_cmd", required=True)

    p_cv = p_certs_sub.add_parser("view", help="get a certificate by ID")
    p_cv.add_argument("cert_id")
    p_cv.add_argument("--dry-run", action="store_true")
    p_cv.set_defaults(func=cmd_cert_view)

    p_cl = p_certs_sub.add_parser("list", help="get multiple certificates by ID list")
    p_cl.add_argument("cert_ids", help="comma-separated certificate IDs")
    p_cl.add_argument("--dry-run", action="store_true")
    p_cl.set_defaults(func=cmd_cert_list)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
