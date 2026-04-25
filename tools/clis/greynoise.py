#!/usr/bin/env python3
"""
greynoise.py — GreyNoise CLI using the official pygreynoise SDK.

The Node CLI hits the community endpoint only. The Python CLI exposes the
full API surface — context (full noise telemetry), RIOT (known-benign),
similarity, timeline, and GNQL search — gated by your tier.

SDK reference: https://github.com/GreyNoise-Intelligence/pygreynoise
API docs:      https://docs.greynoise.io/

Self-bootstraps a private venv at tools/clis/.venv-greynoise/ on first run.

Usage:
  greynoise.py community <ip> [--dry-run]
  greynoise.py context <ip> [--dry-run]
  greynoise.py riot <ip> [--dry-run]
  greynoise.py quick <ip[,ip,...]> [--dry-run]
  greynoise.py similarity <ip> [--limit N] [--dry-run]
  greynoise.py timeline <ip> [--days N] [--dry-run]
  greynoise.py query "<gnql>" [--size N] [--dry-run]
  greynoise.py stats "<gnql>" [--dry-run]
  greynoise.py metadata [--dry-run]

Tier notes:
  community     free, 50/day.
  context/riot/quick/similarity/timeline/query/stats  require Enterprise.
  metadata     no auth needed (sometimes; CLI still uses your key).

GNQL examples (query/stats):
  classification:malicious
  raw_data.scan.port:22 metadata.country:RU
  tags:"Mirai" last_seen:1d
  metadata.organization:"Hosting Co"

Exit codes:
  0  success
  1  network / API error (incl. 402 = upgrade required, 429 = rate limited)
  2  missing GREYNOISE_API_KEY (only when not --dry-run)
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
VENV_DIR = SCRIPT_DIR / ".venv-greynoise"
VENV_PY = VENV_DIR / "bin" / "python"


def _bootstrap_venv():
    print(f"first run: creating Python venv at {VENV_DIR} and installing greynoise SDK...", file=sys.stderr)
    subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)],
                          stdout=subprocess.DEVNULL)
    subprocess.check_call([str(VENV_PY), "-m", "pip", "install", "--quiet",
                           "--disable-pip-version-check", "greynoise"])
    print("bootstrap complete.", file=sys.stderr)


if os.environ.get("CTI_GREYNOISE_VENV") != "1":
    if not VENV_PY.exists():
        _bootstrap_venv()
    os.environ["CTI_GREYNOISE_VENV"] = "1"
    os.execv(str(VENV_PY), [str(VENV_PY), str(pathlib.Path(__file__).resolve())] + sys.argv[1:])

# ---------------------------------------------------------------------------
# Inside venv. sys.path fix to avoid greynoise.py self-shadowing.
# ---------------------------------------------------------------------------
import argparse
import json
from datetime import datetime, timezone

sys.path = [p for p in sys.path if pathlib.Path(p or ".").resolve() != SCRIPT_DIR]

from greynoise import GreyNoise
from greynoise.exceptions import RequestFailure, RateLimitError


API_KEY = os.environ.get("GREYNOISE_API_KEY", "")


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def make_client():
    if not API_KEY:
        die("GREYNOISE_API_KEY not set. Run /cti-setup or ./scripts/setup.sh", 2)
    return GreyNoise(api_key=API_KEY)


def _wrap(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except RateLimitError as e:
        die(f"rate limited: {e}", 1)
    except RequestFailure as e:
        die(f"GreyNoise API error: {e}", 1)
    except Exception as e:
        die(f"{type(e).__name__}: {e}", 1)


def _summarise(d):
    """Common reduce of a GreyNoise IP record."""
    if not d:
        return None
    return {
        "ip": d.get("ip"),
        "noise": d.get("noise"),
        "riot": d.get("riot"),
        "classification": d.get("classification"),
        "name": d.get("name"),
        "actor": d.get("actor"),
        "tags": d.get("tags"),
        "first_seen": d.get("first_seen"),
        "last_seen": d.get("last_seen"),
        "spoofable": d.get("spoofable"),
        "vpn": d.get("vpn"),
        "vpn_service": d.get("vpn_service"),
        "metadata_country": (d.get("metadata") or {}).get("country"),
        "metadata_country_code": (d.get("metadata") or {}).get("country_code"),
        "metadata_organization": (d.get("metadata") or {}).get("organization"),
        "metadata_asn": (d.get("metadata") or {}).get("asn"),
        "metadata_category": (d.get("metadata") or {}).get("category"),
    }


def cmd_community(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "community.ip", "ip": args.ip,
                          "tier": "free (50/day)"}, indent=2))
        return
    api = make_client()
    d = _wrap(api.ip_community, args.ip)
    print(json.dumps({"source": "greynoise", "operation": "community",
                      "indicator": args.ip, "query_time": now_iso(),
                      "result": d}, indent=2, default=str))


def cmd_context(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "noise.context", "ip": args.ip,
                          "tier": "Enterprise"}, indent=2))
        return
    api = make_client()
    d = _wrap(api.ip, args.ip)
    print(json.dumps({"source": "greynoise", "operation": "context",
                      "indicator": args.ip, "query_time": now_iso(),
                      "summary": _summarise(d), "raw": d}, indent=2, default=str))


def cmd_riot(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "riot.ip", "ip": args.ip,
                          "tier": "Enterprise"}, indent=2))
        return
    api = make_client()
    d = _wrap(api.riot, args.ip)
    print(json.dumps({"source": "greynoise", "operation": "riot",
                      "indicator": args.ip, "query_time": now_iso(),
                      "result": d}, indent=2, default=str))


def cmd_quick(args):
    ips = [i.strip() for i in args.ips.split(",") if i.strip()]
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "noise.multi.quick",
                          "ips": ips, "tier": "Enterprise"}, indent=2))
        return
    api = make_client()
    d = _wrap(api.quick, ips)
    print(json.dumps({"source": "greynoise", "operation": "quick",
                      "query_time": now_iso(),
                      "results": [_summarise(x) for x in (d or [])]},
                     indent=2, default=str))


def cmd_similarity(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "similarity.ips",
                          "ip": args.ip, "limit": args.limit, "tier": "Enterprise"}, indent=2))
        return
    api = make_client()
    d = _wrap(api.similar, args.ip, limit=args.limit) if hasattr(api, "similar") else _wrap(api.ip_similarity, args.ip, limit=args.limit)
    print(json.dumps({"source": "greynoise", "operation": "similarity",
                      "indicator": args.ip, "query_time": now_iso(),
                      "result": d}, indent=2, default=str))


def cmd_timeline(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "timeline.ip",
                          "ip": args.ip, "days": args.days, "tier": "Enterprise"}, indent=2))
        return
    api = make_client()
    fn = getattr(api, "timeline", None) or getattr(api, "ip_timeline", None)
    if fn is None:
        die("timeline endpoint not available in this SDK version", 1)
    d = _wrap(fn, args.ip, days=args.days) if "days" in fn.__code__.co_varnames else _wrap(fn, args.ip)
    print(json.dumps({"source": "greynoise", "operation": "timeline",
                      "indicator": args.ip, "days": args.days, "query_time": now_iso(),
                      "result": d}, indent=2, default=str))


def cmd_query(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "gnql.query",
                          "query": args.query, "size": args.size, "tier": "Enterprise"}, indent=2))
        return
    api = make_client()
    d = _wrap(api.query, args.query, size=args.size)
    data = d.get("data", []) if isinstance(d, dict) else (d or [])
    out = {
        "source": "greynoise",
        "operation": "gnql_query",
        "query": args.query,
        "query_time": now_iso(),
        "count": (d.get("count") if isinstance(d, dict) else len(data)),
        "results": [_summarise(r) for r in data],
    }
    print(json.dumps(out, indent=2, default=str))


def cmd_stats(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "gnql.stats",
                          "query": args.query, "tier": "Enterprise"}, indent=2))
        return
    api = make_client()
    d = _wrap(api.stats, args.query)
    print(json.dumps({"source": "greynoise", "operation": "gnql_stats",
                      "query": args.query, "query_time": now_iso(),
                      "result": d}, indent=2, default=str))


def cmd_metadata(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "metadata"}, indent=2))
        return
    api = make_client()
    fn = getattr(api, "metadata", None)
    if fn is None:
        die("metadata endpoint not available in this SDK version", 1)
    d = _wrap(fn)
    print(json.dumps({"source": "greynoise", "operation": "metadata",
                      "query_time": now_iso(), "result": d}, indent=2, default=str))


def main():
    ap = argparse.ArgumentParser(
        prog="greynoise.py",
        description="GreyNoise CLI (uses official pygreynoise SDK)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_com = sub.add_parser("community", help="community endpoint (FREE — 50/day)")
    p_com.add_argument("ip")
    p_com.add_argument("--dry-run", action="store_true")
    p_com.set_defaults(func=cmd_community)

    p_ctx = sub.add_parser("context", help="full noise context (Enterprise)")
    p_ctx.add_argument("ip")
    p_ctx.add_argument("--dry-run", action="store_true")
    p_ctx.set_defaults(func=cmd_context)

    p_riot = sub.add_parser("riot", help="rule-it-out / known-benign lookup (Enterprise)")
    p_riot.add_argument("ip")
    p_riot.add_argument("--dry-run", action="store_true")
    p_riot.set_defaults(func=cmd_riot)

    p_quick = sub.add_parser("quick", help="bulk quick noise classification (Enterprise)")
    p_quick.add_argument("ips", help="comma-separated IPs")
    p_quick.add_argument("--dry-run", action="store_true")
    p_quick.set_defaults(func=cmd_quick)

    p_sim = sub.add_parser("similarity", help="find similar IPs to a known scanner (Enterprise)")
    p_sim.add_argument("ip")
    p_sim.add_argument("--limit", type=int, default=20)
    p_sim.add_argument("--dry-run", action="store_true")
    p_sim.set_defaults(func=cmd_similarity)

    p_tl = sub.add_parser("timeline", help="IP activity timeline (Enterprise)")
    p_tl.add_argument("ip")
    p_tl.add_argument("--days", type=int, default=30)
    p_tl.add_argument("--dry-run", action="store_true")
    p_tl.set_defaults(func=cmd_timeline)

    p_q = sub.add_parser("query", help="GNQL search (Enterprise)")
    p_q.add_argument("query")
    p_q.add_argument("--size", type=int, default=20)
    p_q.add_argument("--dry-run", action="store_true")
    p_q.set_defaults(func=cmd_query)

    p_stats = sub.add_parser("stats", help="GNQL stats / aggregations (Enterprise)")
    p_stats.add_argument("query")
    p_stats.add_argument("--dry-run", action="store_true")
    p_stats.set_defaults(func=cmd_stats)

    p_meta = sub.add_parser("metadata", help="dataset metadata (tags, categories, ...)")
    p_meta.add_argument("--dry-run", action="store_true")
    p_meta.set_defaults(func=cmd_metadata)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
