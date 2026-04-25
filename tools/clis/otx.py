#!/usr/bin/env python3
"""
otx.py — AlienVault OTX CLI using the official OTXv2 Python SDK.

Provides richer queries than tools/clis/otx.js (which only hits the /general
endpoint). Use this for full indicator details across every OTX section,
pulse search, pulse retrieval, and subscribed-pulse listing.

The script self-bootstraps a private Python venv at tools/clis/.venv-otx/
on first run and pip-installs OTXv2 there — no global Python pollution,
no PEP 668 issues on Homebrew Python.

SDK reference: https://github.com/AlienVault-OTX/OTX-Python-SDK
API docs:      https://otx.alienvault.com/api

Usage:
  otx.py indicator <ip|ipv4|ipv6|domain|hostname|hash|url> <value> [--section SECTION] [--dry-run]
  otx.py pulse search <query> [--limit N] [--dry-run]
  otx.py pulse get <pulse_id> [--dry-run]
  otx.py pulse subscribed [--limit N] [--dry-run]

Exit codes:
  0  success
  1  network / API error
  2  missing OTX_API_KEY (only when not --dry-run)
  3  bad arguments
"""

# ---------------------------------------------------------------------------
# Self-bootstrap: create a private venv next to this script on first run,
# install OTXv2 inside it, then re-exec ourselves under the venv interpreter.
# Anything that needs the SDK lives BELOW the bootstrap.
# ---------------------------------------------------------------------------
import os
import pathlib
import subprocess
import sys

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
VENV_DIR = SCRIPT_DIR / ".venv-otx"
VENV_PY = VENV_DIR / "bin" / "python"


def _bootstrap_venv():
    print(f"first run: creating Python venv at {VENV_DIR} and installing OTXv2 SDK...", file=sys.stderr)
    subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)],
                          stdout=subprocess.DEVNULL)
    subprocess.check_call([str(VENV_PY), "-m", "pip", "install", "--quiet",
                           "--disable-pip-version-check", "OTXv2"])
    print("bootstrap complete.", file=sys.stderr)


if os.environ.get("CTI_OTX_VENV") != "1":
    if not VENV_PY.exists():
        _bootstrap_venv()
    os.environ["CTI_OTX_VENV"] = "1"
    os.execv(str(VENV_PY), [str(VENV_PY), str(pathlib.Path(__file__).resolve())] + sys.argv[1:])

# ---------------------------------------------------------------------------
# Below this line we are running inside the venv with OTXv2 importable.
# ---------------------------------------------------------------------------
import argparse
import json
from datetime import datetime, timezone

import OTXv2
from OTXv2 import IndicatorTypes


API_KEY = os.environ.get("OTX_API_KEY", "")


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def detect_hash_type(value):
    L = len(value)
    if L == 32:
        return IndicatorTypes.FILE_HASH_MD5
    if L == 40:
        return IndicatorTypes.FILE_HASH_SHA1
    if L == 64:
        return IndicatorTypes.FILE_HASH_SHA256
    return None


def resolve_indicator_type(t, value):
    t = t.lower()
    if t in ("ip", "ipv4"):
        return IndicatorTypes.IPv4
    if t == "ipv6":
        return IndicatorTypes.IPv6
    if t == "domain":
        return IndicatorTypes.DOMAIN
    if t == "hostname":
        return IndicatorTypes.HOSTNAME
    if t == "url":
        return IndicatorTypes.URL
    if t == "hash":
        ht = detect_hash_type(value)
        if not ht:
            die(f"can't infer hash type from value of length {len(value)} (expected 32/40/64 chars)", 3)
        return ht
    die(f"unsupported indicator type: {t}", 3)


def make_client():
    if not API_KEY:
        die("OTX_API_KEY not set. Run /cti-setup or ./scripts/setup.sh", 2)
    return OTXv2.OTXv2(API_KEY)


def cmd_indicator(args):
    ind_type = resolve_indicator_type(args.type, args.value)
    if args.dry_run:
        print(json.dumps({
            "dry_run": True,
            "operation": "get_indicator_details_full" if not args.section else "get_indicator_details_by_section",
            "indicator_type": str(ind_type),
            "value": args.value,
            "section": args.section,
        }, indent=2))
        return

    otx = make_client()
    if args.section:
        details = otx.get_indicator_details_by_section(ind_type, args.value, args.section)
    else:
        details = otx.get_indicator_details_full(ind_type, args.value)

    print(json.dumps({
        "source": "otx",
        "indicator": args.value,
        "type": args.type,
        "section": args.section or "full",
        "query_time": now_iso(),
        "details": details,
    }, indent=2, default=str))


def _summarise_pulse(p):
    return {
        "id": p.get("id"),
        "name": p.get("name"),
        "author": p.get("author_name") or (p.get("author") or {}).get("username"),
        "created": p.get("created"),
        "modified": p.get("modified"),
        "tlp": p.get("TLP") or p.get("tlp"),
        "tags": p.get("tags"),
        "indicator_count": p.get("indicator_count") if "indicator_count" in p else len(p.get("indicators", []) or []),
        "malware_families": [m.get("display_name") for m in (p.get("malware_families") or [])],
        "attack_ids": [a.get("id") for a in (p.get("attack_ids") or [])] if isinstance(p.get("attack_ids"), list) and p.get("attack_ids") and isinstance(p.get("attack_ids")[0], dict) else p.get("attack_ids"),
    }


def cmd_pulse_search(args):
    if args.dry_run:
        print(json.dumps({
            "dry_run": True,
            "operation": "search_pulses",
            "query": args.query,
            "limit": args.limit,
        }, indent=2))
        return

    otx = make_client()
    results = otx.search_pulses(args.query, max_results=args.limit)
    pulses = results.get("results", []) if isinstance(results, dict) else results
    out = {
        "source": "otx",
        "operation": "pulse_search",
        "query": args.query,
        "query_time": now_iso(),
        "count": len(pulses),
        "pulses": [_summarise_pulse(p) for p in pulses[:args.limit]],
    }
    print(json.dumps(out, indent=2, default=str))


def cmd_pulse_get(args):
    if args.dry_run:
        print(json.dumps({
            "dry_run": True,
            "operation": "get_pulse_details + get_pulse_indicators",
            "pulse_id": args.pulse_id,
        }, indent=2))
        return

    otx = make_client()
    details = otx.get_pulse_details(args.pulse_id)
    indicators = otx.get_pulse_indicators(args.pulse_id)
    out = {
        "source": "otx",
        "operation": "pulse_get",
        "pulse_id": args.pulse_id,
        "query_time": now_iso(),
        "pulse": _summarise_pulse(details),
        "description": details.get("description"),
        "references": details.get("references"),
        "indicators": indicators,
    }
    print(json.dumps(out, indent=2, default=str))


def cmd_pulse_subscribed(args):
    if args.dry_run:
        print(json.dumps({
            "dry_run": True,
            "operation": "getall (subscribed pulses)",
            "limit": args.limit,
        }, indent=2))
        return

    otx = make_client()
    pulses = otx.getall(limit=args.limit)
    out = {
        "source": "otx",
        "operation": "pulse_subscribed",
        "query_time": now_iso(),
        "count": len(pulses),
        "pulses": [_summarise_pulse(p) for p in pulses],
    }
    print(json.dumps(out, indent=2, default=str))


def main():
    ap = argparse.ArgumentParser(
        prog="otx.py",
        description="AlienVault OTX CLI (uses official OTXv2 Python SDK)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    # indicator
    p_ind = sub.add_parser("indicator", help="full details for an indicator")
    p_ind.add_argument("type", choices=["ip", "ipv4", "ipv6", "domain", "hostname", "hash", "url"])
    p_ind.add_argument("value")
    p_ind.add_argument("--section",
                       help="limit to one section (general, reputation, geo, malware, url_list, passive_dns, http_scans, analysis). Default: full.")
    p_ind.add_argument("--dry-run", action="store_true")
    p_ind.set_defaults(func=cmd_indicator)

    # pulse
    p_pulse = sub.add_parser("pulse", help="pulse operations")
    p_pulse_sub = p_pulse.add_subparsers(dest="pulse_cmd", required=True)

    p_search = p_pulse_sub.add_parser("search", help="search public pulses")
    p_search.add_argument("query")
    p_search.add_argument("--limit", type=int, default=20)
    p_search.add_argument("--dry-run", action="store_true")
    p_search.set_defaults(func=cmd_pulse_search)

    p_get = p_pulse_sub.add_parser("get", help="get a pulse by ID")
    p_get.add_argument("pulse_id")
    p_get.add_argument("--dry-run", action="store_true")
    p_get.set_defaults(func=cmd_pulse_get)

    p_subbed = p_pulse_sub.add_parser("subscribed", help="list pulses you've subscribed to")
    p_subbed.add_argument("--limit", type=int, default=50)
    p_subbed.add_argument("--dry-run", action="store_true")
    p_subbed.set_defaults(func=cmd_pulse_subscribed)

    args = ap.parse_args()
    try:
        args.func(args)
    except SystemExit:
        raise
    except Exception as e:
        die(f"{type(e).__name__}: {e}", 1)


if __name__ == "__main__":
    main()
