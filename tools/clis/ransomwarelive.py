#!/usr/bin/env python3
"""
ransomwarelive.py — ransomware.live PRO API CLI (stdlib only).

Tracks ransomware victim claims from leak-site scrapes, group profiles,
TTPs, IOCs, YARA rules, ransom notes, negotiation chats, and press
mentions. Useful for: scoping a breach against the ransomware ecosystem,
checking whether a domain/org has been claimed, chasing IOC/YARA pivots
on a known group, and CSIRT lookup during IR.

API base:  https://api-pro.ransomware.live
Auth:      header `X-API-KEY: $RANSOMWARE_LIVE`
Free tier: 3000 calls/day on PRO (sign up at my.ransomware.live)
           1 req/min/endpoint on api.ransomware.live (no auth, this CLI
           does not target the free unauth tier).

Usage:
  ransomwarelive.py validate
  ransomwarelive.py stats

  # ----- victims -----
  ransomwarelive.py search           [--q TEXT] [--group G] [--sector S]
                                     [--country CC] [--order discovered|published]
  ransomwarelive.py recent
  ransomwarelive.py victim           <victim_id>

  # ----- groups -----
  ransomwarelive.py groups
  ransomwarelive.py group            <groupname>          # /groups/{name} (detail)
  ransomwarelive.py group-profile    <groupname>          # /group/{name}  (profile)

  # ----- IOCs / YARA / ransomnotes -----
  ransomwarelive.py iocs             [<groupname>]
  ransomwarelive.py yara             [<groupname>]
  ransomwarelive.py ransomnotes      [<groupname>] [<note_name>]

  # ----- negotiations -----
  ransomwarelive.py negotiations     [<groupname>] [<chat_id>]

  # ----- press / sectors / CSIRTs -----
  ransomwarelive.py press            [--all]              # default: recent
  ransomwarelive.py sectors                               # /listsectors
  ransomwarelive.py csirt            <country>            # ISO-3166 alpha-2

All commands accept --dry-run (preview the request without sending) and
--insecure (skip TLS verify; not normally needed for the public API).

Exit codes:
  0  success
  1  network / API error (incl. 4xx/5xx)
  2  missing $RANSOMWARE_LIVE (only when not --dry-run)
  3  bad arguments
"""

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API_KEY = os.environ.get("RANSOMWARE_LIVE", "")
BASE_URL = os.environ.get("RANSOMWARE_LIVE_URL", "https://api-pro.ransomware.live").rstrip("/")


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def _request(path, params=None, dry_run=False, insecure=False):
    qs = ("?" + urllib.parse.urlencode([(k, v) for k, v in (params or {}).items() if v is not None and v != ""])) if params else ""
    url = f"{BASE_URL}{path}{qs}"

    if dry_run:
        return {
            "dry_run": True,
            "method": "GET",
            "url": url,
            "headers": {"X-API-KEY": "<redacted>" if API_KEY else "<unset>", "Accept": "application/json"},
        }

    if not API_KEY:
        die("RANSOMWARE_LIVE not set. Add it to .claude/settings.local.json env or export it.", 2)

    req = urllib.request.Request(
        url,
        headers={"X-API-KEY": API_KEY, "Accept": "application/json"},
        method="GET",
    )
    ctx = None
    if insecure:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
            txt = r.read().decode("utf-8", errors="replace")
            try:
                return json.loads(txt) if txt else {}
            except json.JSONDecodeError:
                return {"raw": txt}
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode("utf-8", errors="replace") if e.fp else ""
        if e.code == 401:
            die("401 Unauthorized — check $RANSOMWARE_LIVE", 1)
        if e.code == 429:
            die("429 Rate limited — PRO tier is 3000/day. Back off and retry.", 1)
        die(f"HTTP {e.code}: {body_txt[:300]}", 1)
    except urllib.error.URLError as e:
        die(f"network error: {e.reason}", 1)


def _emit(operation, data, **extra):
    out = {
        "source": "ransomware.live",
        "operation": operation,
        "query_time": now_iso(),
    }
    out.update(extra)
    if isinstance(data, dict) and "client" in data:
        # Strip the recurring `client` echo to keep output focussed
        data = {k: v for k, v in data.items() if k != "client"}
    out["data"] = data
    print(json.dumps(out, indent=2))


def _distil_victim(v):
    if not isinstance(v, dict):
        return v
    return {
        "id": v.get("id"),
        "title": v.get("post_title") or v.get("victim"),
        "group": v.get("group_name"),
        "country": v.get("country"),
        "sector": v.get("activity"),
        "discovered": v.get("discovered"),
        "published": v.get("published") or v.get("attackdate"),
        "description": v.get("description"),
        "website": v.get("website"),
        "post_url": v.get("post_url"),
        "permalink": v.get("permalink"),
        "screenshot": v.get("screenshot"),
    }


# ---------- commands ----------

def cmd_validate(args):
    resp = _request("/validate", dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2)); return
    _emit("validate", resp)


def cmd_stats(args):
    resp = _request("/stats", dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2)); return
    _emit("stats", resp)


def cmd_search(args):
    params = {
        "q": args.q,
        "group": args.group,
        "sector": args.sector,
        "country": args.country,
        "order": args.order,
    }
    resp = _request("/victims/search", params=params, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2)); return
    victims = (resp.get("victims") or []) if isinstance(resp, dict) else []
    if args.limit:
        victims = victims[: args.limit]
    _emit(
        "search",
        {
            "filters": {k: v for k, v in params.items() if v},
            "matched_total": resp.get("count") if isinstance(resp, dict) else None,
            "returned": len(victims),
            "victims": [_distil_victim(v) for v in victims],
        },
    )


def cmd_recent(args):
    resp = _request("/victims/recent", dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2)); return
    victims = (resp.get("victims") or []) if isinstance(resp, dict) else []
    if args.limit:
        victims = victims[: args.limit]
    _emit("recent", {
        "returned": len(victims),
        "victims": [_distil_victim(v) for v in victims],
    })


def cmd_victim(args):
    resp = _request(f"/victim/{urllib.parse.quote(args.victim_id, safe='')}", dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2)); return
    _emit("victim", _distil_victim(resp), raw=resp)


def cmd_groups(args):
    resp = _request("/groups", dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2)); return
    groups = (resp.get("groups") or []) if isinstance(resp, dict) else []
    distilled = [
        {
            "group": (g.get("group") if isinstance(g, dict) else g),
            "altname": (g.get("altname") if isinstance(g, dict) else None),
            "victims": (g.get("victims") if isinstance(g, dict) else None),
        }
        for g in groups
    ]
    if args.sort == "victims":
        distilled.sort(key=lambda x: x.get("victims") or 0, reverse=True)
    elif args.sort == "name":
        distilled.sort(key=lambda x: (x.get("group") or "").lower())
    if args.limit:
        distilled = distilled[: args.limit]
    _emit("groups", {"count": resp.get("count") if isinstance(resp, dict) else len(groups), "returned": len(distilled), "groups": distilled})


def cmd_group(args):
    resp = _request(f"/groups/{urllib.parse.quote(args.groupname, safe='')}", dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2)); return
    _emit("group", resp, group=args.groupname)


def cmd_group_profile(args):
    resp = _request(f"/group/{urllib.parse.quote(args.groupname, safe='')}", dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2)); return
    _emit("group-profile", resp, group=args.groupname)


def cmd_iocs(args):
    path = f"/iocs/{urllib.parse.quote(args.groupname, safe='')}" if args.groupname else "/iocs"
    resp = _request(path, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2)); return
    _emit("iocs", resp, group=args.groupname)


def cmd_yara(args):
    path = f"/yara/{urllib.parse.quote(args.groupname, safe='')}" if args.groupname else "/yara"
    resp = _request(path, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2)); return
    _emit("yara", resp, group=args.groupname)


def cmd_ransomnotes(args):
    if args.note_name and not args.groupname:
        die("--note-name requires <groupname>", 3)
    if args.note_name:
        path = f"/ransomnotes/{urllib.parse.quote(args.groupname, safe='')}/{urllib.parse.quote(args.note_name, safe='')}"
    elif args.groupname:
        path = f"/ransomnotes/{urllib.parse.quote(args.groupname, safe='')}"
    else:
        path = "/ransomnotes"
    resp = _request(path, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2)); return
    _emit("ransomnotes", resp, group=args.groupname, note_name=args.note_name)


def cmd_negotiations(args):
    if args.chat_id and not args.groupname:
        die("<chat_id> requires <groupname>", 3)
    if args.chat_id:
        path = f"/negotiations/{urllib.parse.quote(args.groupname, safe='')}/{urllib.parse.quote(args.chat_id, safe='')}"
    elif args.groupname:
        path = f"/negotiations/{urllib.parse.quote(args.groupname, safe='')}"
    else:
        path = "/negotiations"
    resp = _request(path, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2)); return
    _emit("negotiations", resp, group=args.groupname, chat_id=args.chat_id)


def cmd_press(args):
    path = "/press/all" if args.all else "/press/recent"
    resp = _request(path, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2)); return
    _emit("press-all" if args.all else "press-recent", resp)


def cmd_sectors(args):
    resp = _request("/listsectors", dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2)); return
    _emit("sectors", resp)


def cmd_csirt(args):
    resp = _request(f"/csirt/{urllib.parse.quote(args.country, safe='')}", dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2)); return
    _emit("csirt", resp, country=args.country)


# ---------- arg parsing ----------

def main():
    ap = argparse.ArgumentParser(
        prog="ransomwarelive.py",
        description="ransomware.live PRO API CLI (stdlib only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    def _common(p):
        p.add_argument("--dry-run", action="store_true")
        p.add_argument("--insecure", action="store_true")

    p = sub.add_parser("validate", help="GET /validate — check API key")
    _common(p); p.set_defaults(func=cmd_validate)

    p = sub.add_parser("stats", help="GET /stats — global counts")
    _common(p); p.set_defaults(func=cmd_stats)

    p = sub.add_parser("search", help="GET /victims/search")
    p.add_argument("--q", help="free-text search across victim names + descriptions")
    p.add_argument("--group", help="filter by group name (e.g. lockbit3, alphv)")
    p.add_argument("--sector", help="filter by sector (see /sectors for valid values)")
    p.add_argument("--country", help="ISO-3166 alpha-2 (e.g. US, NL, DE)")
    p.add_argument("--order", choices=["discovered", "published"], default=None,
                   help="ordering field (default: discovered)")
    p.add_argument("--limit", type=int, default=50, help="cap returned victims (server returns full set)")
    _common(p); p.set_defaults(func=cmd_search)

    p = sub.add_parser("recent", help="GET /victims/recent — last 100 claims")
    p.add_argument("--limit", type=int, default=20)
    _common(p); p.set_defaults(func=cmd_recent)

    p = sub.add_parser("victim", help="GET /victim/{id}")
    p.add_argument("victim_id")
    _common(p); p.set_defaults(func=cmd_victim)

    p = sub.add_parser("groups", help="GET /groups — list all groups + victim counts")
    p.add_argument("--sort", choices=["victims", "name"], default="victims")
    p.add_argument("--limit", type=int, default=50)
    _common(p); p.set_defaults(func=cmd_groups)

    p = sub.add_parser("group", help="GET /groups/{name} — group detail")
    p.add_argument("groupname")
    _common(p); p.set_defaults(func=cmd_group)

    p = sub.add_parser("group-profile", help="GET /group/{name} — group profile (TTPs, infra)")
    p.add_argument("groupname")
    _common(p); p.set_defaults(func=cmd_group_profile)

    p = sub.add_parser("iocs", help="GET /iocs[/<group>] — IOC dump")
    p.add_argument("groupname", nargs="?")
    _common(p); p.set_defaults(func=cmd_iocs)

    p = sub.add_parser("yara", help="GET /yara[/<group>] — YARA rules per group")
    p.add_argument("groupname", nargs="?")
    _common(p); p.set_defaults(func=cmd_yara)

    p = sub.add_parser("ransomnotes", help="GET /ransomnotes[/<group>[/<note>]] — ransom note samples")
    p.add_argument("groupname", nargs="?")
    p.add_argument("note_name", nargs="?")
    _common(p); p.set_defaults(func=cmd_ransomnotes)

    p = sub.add_parser("negotiations", help="GET /negotiations[/<group>[/<chat_id>]]")
    p.add_argument("groupname", nargs="?")
    p.add_argument("chat_id", nargs="?")
    _common(p); p.set_defaults(func=cmd_negotiations)

    p = sub.add_parser("press", help="GET /press/recent (default) or /press/all")
    p.add_argument("--all", action="store_true", help="full archive instead of recent")
    _common(p); p.set_defaults(func=cmd_press)

    p = sub.add_parser("sectors", help="GET /listsectors — valid sector filter values")
    _common(p); p.set_defaults(func=cmd_sectors)

    p = sub.add_parser("csirt", help="GET /csirt/{country} — CSIRT/CERT contacts")
    p.add_argument("country", help="ISO-3166 alpha-2")
    _common(p); p.set_defaults(func=cmd_csirt)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
