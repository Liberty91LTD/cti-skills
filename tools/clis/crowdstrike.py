#!/usr/bin/env python3
"""
crowdstrike.py — CrowdStrike Falcon Intelligence (Intel API) CLI.

Wraps the official crowdstrike-falconpy SDK to give an analyst a CTI-focused
slice of the Falcon Intel surface: indicator (IOC) reputation, threat-actor
(adversary) profiles, actor search by origin/target, finished intel reports,
and MITRE ATT&CK technique coverage per actor.

API reference: https://developer.crowdstrike.com/api-reference/collections/intel/
SDK reference: https://github.com/CrowdStrike/falconpy
FalconPy Intel: https://www.falconpy.io/Service-Collections/Intel.html

Auth: OAuth2 client-credentials. CROWDSTRIKE_CLIENT_ID + CROWDSTRIKE_CLIENT_SECRET.
Optional CROWDSTRIKE_BASE_URL override (default https://api.crowdstrike.com,
i.e. US-1). Other clouds: https://api.us-2.crowdstrike.com,
https://api.eu-1.crowdstrike.com, https://api.laggar.gcw.crowdstrike.com (GovCloud).
FalconPy exchanges the credentials for a bearer token at /oauth2/token.

Self-bootstraps a private venv at tools/clis/.venv-crowdstrike/ on first run.

Usage:
  crowdstrike.py indicator <value> [--limit N] [--include-deleted] [--dry-run]
  crowdstrike.py indicators [--malicious] [--type ip|domain|hash|url] [--actor NAME]
                            [--malware FAM] [--since 7d] [--filter FQL] [--limit N] [--dry-run]
  crowdstrike.py actor <name> [--limit N] [--fields F1,F2,...] [--dry-run]
  crowdstrike.py actors [--origin C] [--target-country C] [--target-industry I]
                        [--motivation M] [--filter FQL] [--sort S] [--limit N] [--dry-run]
  crowdstrike.py reports [--actor NAME] [--search Q] [--filter FQL] [--latest]
                         [--sort S] [--limit N] [--pdf REPORT_ID] [--out PATH] [--dry-run]
  crowdstrike.py ttps <actor> [--detailed] [--format csv|json|json_navigator] [--dry-run]

All subcommands accept --base-url to override CROWDSTRIKE_BASE_URL for one call.

FQL filter examples (Falcon Query Language):
  origins.slug:'ru'                  # country slugs are ISO alpha-2 codes (ru/cn/ir/kp)
  target_countries.slug:'us'
  target_industries.slug:'financial-services'
  motivations.slug:'state-sponsored'
  actors.slug:'mustang-panda'
  created_date:>'2025-01-01'
  malicious_confidence:'high'

Exit codes:
  0  success
  1  network / API error (incl. non-2xx HTTP)
  2  missing CROWDSTRIKE_CLIENT_ID or CROWDSTRIKE_CLIENT_SECRET (only when not --dry-run)
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
VENV_DIR = SCRIPT_DIR / ".venv-crowdstrike"
VENV_PY = VENV_DIR / "bin" / "python"


def _bootstrap_venv():
    print(f"first run: creating Python venv at {VENV_DIR} and installing crowdstrike-falconpy...", file=sys.stderr)
    subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)],
                          stdout=subprocess.DEVNULL)
    subprocess.check_call([str(VENV_PY), "-m", "pip", "install", "--quiet",
                           "--disable-pip-version-check", "crowdstrike-falconpy"])
    print("bootstrap complete.", file=sys.stderr)


if os.environ.get("CTI_CROWDSTRIKE_VENV") != "1":
    if not VENV_PY.exists():
        _bootstrap_venv()
    os.environ["CTI_CROWDSTRIKE_VENV"] = "1"
    os.execv(str(VENV_PY), [str(VENV_PY), str(pathlib.Path(__file__).resolve())] + sys.argv[1:])

# ---------------------------------------------------------------------------
# Inside venv from here on.
# Strip the script directory from sys.path so we don't shadow any package
# named `falconpy` if one is ever added there.
# ---------------------------------------------------------------------------
import argparse
import json
from datetime import datetime, timezone

sys.path = [p for p in sys.path if pathlib.Path(p or ".").resolve() != SCRIPT_DIR]

from falconpy import Intel  # noqa: E402


CLIENT_ID = os.environ.get("CROWDSTRIKE_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("CROWDSTRIKE_CLIENT_SECRET", "")
BASE_URL = os.environ.get("CROWDSTRIKE_BASE_URL", "https://api.crowdstrike.com")


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def make_client(base_url=None):
    if not CLIENT_ID or not CLIENT_SECRET:
        die("CROWDSTRIKE_CLIENT_ID and CROWDSTRIKE_CLIENT_SECRET must be set. "
            "Run /cti-setup or ./scripts/setup.sh", 2)
    return Intel(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        base_url=base_url or BASE_URL,
        user_agent="cti-skills/lookup-crowdstrike/1.0",
    )


def envelope(operation, indicator, type_, base_url, **extra):
    out = {
        "source": "crowdstrike",
        "operation": operation,
        "indicator": indicator,
        "type": type_,
        "base_url": base_url,
        "query_time": now_iso(),
    }
    out.update(extra)
    return out


def emit(obj):
    print(json.dumps(obj, indent=2, default=str))


def _api_call(label, fn):
    """Wrap an SDK call so transport errors become exit-code-1 dies."""
    try:
        return fn()
    except SystemExit:
        raise
    except Exception as e:  # auth / transport / SDK errors all read as API error from our POV
        die(f"CrowdStrike {label} error: {e}", 1)


def unwrap(label, resp):
    """FalconPy returns {status_code, headers, body}. Return body on 2xx, else die."""
    if not isinstance(resp, dict):
        return resp  # binary endpoints (e.g. report PDF) return raw bytes
    status = resp.get("status_code")
    body = resp.get("body", resp)
    if status is None or 200 <= int(status) < 300:
        return body
    errors = body.get("errors") if isinstance(body, dict) else None
    die(f"CrowdStrike {label} returned HTTP {status}: {errors or body}", 1)


def resources(body):
    return (body or {}).get("resources") if isinstance(body, dict) else body


def _fql_and(clauses):
    """Join FQL clauses with '+' (logical AND in Falcon Query Language)."""
    return "+".join([c for c in clauses if c]) or None


# CrowdStrike `origins.slug` and `target_countries.slug` are ISO 3166-1 alpha-2
# country codes (e.g. Russia -> 'ru'), NOT country names. Map the friendly names
# used in the skill docs; pass anything else through unchanged so a raw code or
# slug still works.
COUNTRY_SLUGS = {
    "russia": "ru", "russian federation": "ru",
    "china": "cn", "prc": "cn", "people's republic of china": "cn",
    "iran": "ir", "north korea": "kp", "dprk": "kp", "south korea": "kr",
    "united states": "us", "usa": "us", "united kingdom": "gb", "uk": "gb",
    "pakistan": "pk", "india": "in", "vietnam": "vn", "syria": "sy",
    "lebanon": "lb", "turkey": "tr", "israel": "il", "ukraine": "ua",
}


def _country_slug(value):
    key = value.strip().lower()
    return COUNTRY_SLUGS.get(key, key.replace(" ", "-"))


# Friendly indicator-type names -> CrowdStrike `type` FQL clause. `hash` matches
# any of the three digest types (parenthesised OR so it composes under AND).
INDICATOR_TYPE_FQL = {
    "ip": "type:'ip_address'", "ipv4": "type:'ip_address'", "ipv6": "type:'ip_address'",
    "domain": "type:'domain'", "url": "type:'url'", "email": "type:'email_address'",
    "hash": "(type:'hash_sha256',type:'hash_md5',type:'hash_sha1')",
    "sha256": "type:'hash_sha256'", "sha1": "type:'hash_sha1'", "md5": "type:'hash_md5'",
}


def _since_epoch(spec):
    """Parse '7d' / '24h' / '30m' into a Unix epoch cutoff (seconds ago from now)."""
    import re
    m = re.fullmatch(r"(\d+)\s*([dhm])", spec.strip().lower())
    if not m:
        die("--since must look like 7d, 24h, or 30m", 3)
    secs = int(m.group(1)) * {"d": 86400, "h": 3600, "m": 60}[m.group(2)]
    return int(datetime.now(timezone.utc).timestamp()) - secs


# ---------------------------------------------------------------------------
# indicator — IOC reputation (ip / domain / hash / url)
# ---------------------------------------------------------------------------

def cmd_indicator(args):
    fql = f"indicator:'{args.value}'"
    if args.dry_run:
        emit({"dry_run": True, "operation": "indicator_lookup", "indicator": args.value,
              "endpoint": "GET /intel/combined/indicators/v1",
              "params": {"filter": fql, "limit": args.limit,
                         "include_deleted": args.include_deleted}})
        return
    client = make_client(args.base_url)
    body = unwrap("query_indicator_entities", _api_call(
        "query_indicator_entities",
        lambda: client.query_indicator_entities(
            filter=fql, limit=args.limit, sort="published_date|desc",
            include_deleted=args.include_deleted)))
    items = resources(body) or []
    emit(envelope("indicator_lookup", args.value, "indicator",
                  args.base_url or BASE_URL, count=len(items), indicators=items))


# ---------------------------------------------------------------------------
# indicators — browse / sweep the indicator feed (latest malicious, by type, etc.)
# ---------------------------------------------------------------------------

def cmd_indicators(args):
    clauses = []
    if args.confidence:
        clauses.append(f"malicious_confidence:'{args.confidence}'")
    elif args.malicious:
        clauses.append("malicious_confidence:'high'")
    if args.type:
        t = INDICATOR_TYPE_FQL.get(args.type.strip().lower())
        if not t:
            die(f"unknown --type '{args.type}' (use ip/domain/url/hash/md5/sha1/sha256/email)", 3)
        clauses.append(t)
    if args.actor:
        clauses.append(f"actors:'{args.actor.strip().lower().replace(' ', '-')}'")
    if args.malware:
        clauses.append(f"malware_families:'{args.malware}'")
    if args.since:
        clauses.append(f"published_date:>{_since_epoch(args.since)}")
    if args.filter:
        clauses.append(args.filter)
    fql = _fql_and(clauses)

    if args.dry_run:
        emit({"dry_run": True, "operation": "indicator_search",
              "endpoint": "GET /intel/combined/indicators/v1",
              "params": {"filter": fql, "sort": args.sort, "limit": args.limit,
                         "include_deleted": args.include_deleted}})
        return
    client = make_client(args.base_url)
    body = unwrap("query_indicator_entities", _api_call(
        "query_indicator_entities",
        lambda: client.query_indicator_entities(
            filter=fql, sort=args.sort, limit=args.limit,
            include_deleted=args.include_deleted)))
    items = resources(body) or []
    emit(envelope("indicator_search", fql or "(all)", "indicator_query",
                  args.base_url or BASE_URL, filter=fql, sort=args.sort,
                  count=len(items), indicators=items))


# ---------------------------------------------------------------------------
# actor — profile a single named threat actor
# ---------------------------------------------------------------------------

def cmd_actor(args):
    fields = [f.strip() for f in args.fields.split(",") if f.strip()] if args.fields else None
    if args.dry_run:
        emit({"dry_run": True, "operation": "actor_profile", "indicator": args.name,
              "endpoint": "GET /intel/combined/actors/v1",
              "params": {"q": args.name, "limit": args.limit, "fields": fields}})
        return
    client = make_client(args.base_url)
    kwargs = {"q": args.name, "limit": args.limit, "sort": "last_activity_date|desc"}
    if fields:
        kwargs["fields"] = fields
    body = unwrap("query_actor_entities", _api_call(
        "query_actor_entities",
        lambda: client.query_actor_entities(**kwargs)))
    items = resources(body) or []
    emit(envelope("actor_profile", args.name, "actor",
                  args.base_url or BASE_URL, count=len(items), actors=items))


# ---------------------------------------------------------------------------
# actors — search actors by origin / target / motivation / raw FQL
# ---------------------------------------------------------------------------

def cmd_actors(args):
    clauses = []
    if args.origin:
        clauses.append(f"origins.slug:'{_country_slug(args.origin)}'")
    if args.target_country:
        clauses.append(f"target_countries.slug:'{_country_slug(args.target_country)}'")
    if args.target_industry:
        clauses.append(f"target_industries.slug:'{args.target_industry.lower().replace(' ', '-')}'")
    if args.motivation:
        clauses.append(f"motivations.slug:'{args.motivation.lower().replace(' ', '-')}'")
    if args.filter:
        clauses.append(args.filter)
    fql = _fql_and(clauses)
    if not fql:
        die("actors needs at least one of --origin/--target-country/--target-industry/--motivation/--filter", 3)

    if args.dry_run:
        emit({"dry_run": True, "operation": "actor_search", "indicator": fql,
              "endpoint": "GET /intel/combined/actors/v1",
              "params": {"filter": fql, "limit": args.limit, "sort": args.sort}})
        return
    client = make_client(args.base_url)
    body = unwrap("query_actor_entities", _api_call(
        "query_actor_entities",
        lambda: client.query_actor_entities(filter=fql, limit=args.limit, sort=args.sort)))
    items = resources(body) or []
    emit(envelope("actor_search", fql, "actor_query",
                  args.base_url or BASE_URL, filter=fql, count=len(items), actors=items))


# ---------------------------------------------------------------------------
# reports — finished intelligence reports (search / latest / PDF download)
# ---------------------------------------------------------------------------

def cmd_reports(args):
    if args.pdf:
        out_path = args.out or f"{args.pdf}.pdf"
        if args.dry_run:
            emit({"dry_run": True, "operation": "report_pdf", "indicator": args.pdf,
                  "endpoint": "GET /intel/entities/report-files/v1",
                  "params": {"id": args.pdf}, "out": out_path})
            return
        client = make_client(args.base_url)
        resp = _api_call("get_report_pdf", lambda: client.get_report_pdf(id=args.pdf))
        data = resp.get("body") if isinstance(resp, dict) else resp
        if not isinstance(data, (bytes, bytearray)):
            die(f"report PDF for {args.pdf} not returned as bytes: {data}", 1)
        pathlib.Path(out_path).write_bytes(data)
        emit(envelope("report_pdf", args.pdf, "report_id",
                      args.base_url or BASE_URL, saved_to=str(pathlib.Path(out_path).resolve()),
                      bytes=len(data)))
        return

    clauses = []
    if args.actor:
        # actors.slug is the reliable join; slugify a display name as a fallback hint.
        clauses.append(f"actors.slug:'{args.actor.lower().replace(' ', '-')}'")
    if args.filter:
        clauses.append(args.filter)
    fql = _fql_and(clauses)
    sort = "created_date|desc" if (args.latest or not args.sort) else args.sort

    if args.dry_run:
        emit({"dry_run": True, "operation": "report_search",
              "indicator": args.search or fql or "(all)",
              "endpoint": "GET /intel/combined/reports/v1",
              "params": {"filter": fql, "q": args.search, "sort": sort, "limit": args.limit}})
        return
    client = make_client(args.base_url)
    kwargs = {"limit": args.limit, "sort": sort}
    if fql:
        kwargs["filter"] = fql
    if args.search:
        kwargs["q"] = args.search
    body = unwrap("query_report_entities", _api_call(
        "query_report_entities",
        lambda: client.query_report_entities(**kwargs)))
    items = resources(body) or []
    emit(envelope("report_search", args.search or fql or "(all)", "report_query",
                  args.base_url or BASE_URL, filter=fql, q=args.search, sort=sort,
                  count=len(items), reports=items))


# ---------------------------------------------------------------------------
# ttps — MITRE ATT&CK tactics/techniques for an actor
# ---------------------------------------------------------------------------

def cmd_ttps(args):
    if args.dry_run:
        emit({"dry_run": True, "operation": "actor_ttps", "indicator": args.actor,
              "endpoints": ["GET /intel/combined/actors/v1 (resolve slug)",
                            "GET /intel/combined/mitre-attacks/v1",
                            "GET /intel/entities/mitre-reports/v1 (--detailed)"],
              "params": {"actor": args.actor, "detailed": args.detailed, "format": args.format}})
        return

    client = make_client(args.base_url)
    # 1) Resolve the actor to its CrowdStrike slug. A free-text `q` for e.g.
    # "charming kitten" returns every KITTEN actor; prefer an exact name/slug
    # match over the most-recently-active hit so we map the actor the user named.
    body = unwrap("query_actor_entities", _api_call(
        "query_actor_entities",
        lambda: client.query_actor_entities(q=args.actor, limit=10,
                                            sort="last_activity_date|desc")))
    actors = resources(body) or []
    if not actors:
        die(f"no CrowdStrike actor matched '{args.actor}'", 1)
    want = args.actor.strip().lower()
    want_slug = want.replace(" ", "-")
    actor = next((a for a in actors
                  if a.get("name", "").lower() == want or a.get("slug", "").lower() == want_slug),
                 actors[0])
    slug = actor.get("slug") or actor.get("id")
    name = actor.get("name", args.actor)

    # 2) Technique IDs mapped to that actor.
    attacks = unwrap("query_mitre_attacks", _api_call(
        "query_mitre_attacks",
        lambda: client.query_mitre_attacks(id=slug)))
    techniques = resources(attacks) or []

    out = envelope("actor_ttps", name, "actor", args.base_url or BASE_URL,
                   actor_slug=slug, actor={k: actor.get(k) for k in (
                       "name", "slug", "short_description", "origins",
                       "target_countries", "target_industries", "motivations")},
                   technique_ids=techniques, count=len(techniques))

    # 3) Optional full ATT&CK report (CSV / JSON / Navigator layer).
    if args.detailed:
        report = _api_call("get_mitre_report",
                           lambda: client.get_mitre_report(actor_id=slug, format=args.format))
        report_body = report.get("body") if isinstance(report, dict) else report
        out["mitre_report_format"] = args.format
        out["mitre_report"] = (report_body.decode("utf-8", "replace")
                               if isinstance(report_body, (bytes, bytearray)) else report_body)
    emit(out)


# ---------------------------------------------------------------------------
# argparse
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        prog="crowdstrike.py",
        description="CrowdStrike Falcon Intelligence (Intel API) CLI — uses crowdstrike-falconpy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--base-url", default=None,
                    help="override CROWDSTRIKE_BASE_URL for this call (US-1 default)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("indicator", help="IOC reputation for an ip / domain / hash / url")
    p.add_argument("value")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--include-deleted", action="store_true",
                   help="include indicators marked deleted by CrowdStrike")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_indicator)

    p = sub.add_parser("indicators",
                       help="browse/sweep the indicator feed — latest malicious IOCs, by type/actor/recency")
    p.add_argument("--malicious", action="store_true",
                   help="shorthand for malicious_confidence:'high'")
    p.add_argument("--confidence", choices=["high", "medium", "low", "unverified"],
                   help="exact malicious_confidence (overrides --malicious)")
    p.add_argument("--type", help="indicator type: ip|domain|url|hash|md5|sha1|sha256|email")
    p.add_argument("--actor", help="filter to an actor (slugified name, e.g. 'fancy bear')")
    p.add_argument("--malware", help="filter to a malware family")
    p.add_argument("--since", help="only indicators published within this window: 7d | 24h | 30m")
    p.add_argument("--filter", help="raw FQL filter (AND-combined with the above)")
    p.add_argument("--sort", default="published_date|desc",
                   help="FQL sort (default published_date|desc — newest first)")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--include-deleted", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_indicators)

    p = sub.add_parser("actor", help="profile a single named threat actor (adversary)")
    p.add_argument("name")
    p.add_argument("--limit", type=int, default=5,
                   help="max matching actors to return (default 5)")
    p.add_argument("--fields", help="comma list of actor fields to request (default: full entity)")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_actor)

    p = sub.add_parser("actors", help="search actors by origin / target / motivation / FQL")
    p.add_argument("--origin", help="country of origin, e.g. russia, china, iran, north-korea")
    p.add_argument("--target-country", help="targeted country, e.g. united-states")
    p.add_argument("--target-industry", help="targeted sector, e.g. financial-services")
    p.add_argument("--motivation", help="e.g. state-sponsored, criminal, hacktivism")
    p.add_argument("--filter", help="raw FQL filter (combined with the above via AND)")
    p.add_argument("--sort", default="last_activity_date|desc",
                   help="FQL sort (default last_activity_date|desc). NOTE: 'name' is not sortable on this endpoint")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_actors)

    p = sub.add_parser("reports", help="finished intel reports — search, latest, or PDF download")
    p.add_argument("--actor", help="filter reports to an actor (slugified name)")
    p.add_argument("--search", help="free-text query across report titles/bodies")
    p.add_argument("--filter", help="raw FQL filter")
    p.add_argument("--latest", action="store_true", help="sort newest-first (created_date desc)")
    p.add_argument("--sort", default=None, help="FQL sort (default created_date|desc)")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--pdf", help="download the PDF for this report ID instead of searching")
    p.add_argument("--out", help="output path for --pdf (default <id>.pdf)")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_reports)

    p = sub.add_parser("ttps", help="MITRE ATT&CK techniques mapped to an actor")
    p.add_argument("actor")
    p.add_argument("--detailed", action="store_true",
                   help="also fetch the full ATT&CK report (CSV/JSON/Navigator)")
    p.add_argument("--format", default="json",
                   choices=["csv", "json", "json_navigator"],
                   help="format for --detailed report (default json)")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_ttps)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
