#!/usr/bin/env python3
"""
reversinglabs.py — ReversingLabs Spectra Analyze (A1000) CLI.

Wraps the official reversinglabs-sdk-py3 to give an analyst a CTI-focused
slice of the A1000 surface: hash classification, full enrichment reports,
file/URL submission, network indicator reputation, advanced search, and
parent/child sample pivoting.

SDK reference: https://github.com/reversinglabs/reversinglabs-sdk-py3
Product docs:  https://docs.reversinglabs.com/SpectraAnalyze/

Auth: REVERSINGLABS_USER + REVERSINGLABS_PASSWORD. Optional REVERSINGLABS_HOST
override (default https://a1000.reversinglabs.com). The SDK exchanges the
credentials for a token via /api-token-auth/ at init.

Self-bootstraps a private venv at tools/clis/.venv-reversinglabs/ on first
run.

Usage:
  reversinglabs.py hash <hash> [--av-scanners] [--ticloud] [--dry-run]
  reversinglabs.py report <hash> [--summary|--detailed] [--fields F1,F2,...] [--dry-run]
  reversinglabs.py submit-file <path> [--wait] [--rl-cloud-sandbox] [--dry-run]
  reversinglabs.py submit-url <url> [--wait] [--crawler tcb|cape|fireeye] [--dry-run]
  reversinglabs.py url <url> [--dry-run]
  reversinglabs.py domain <domain> [--dry-run]
  reversinglabs.py ip <ip> [--pivot files,domains,urls] [--max-results N] [--dry-run]
  reversinglabs.py search "<query>" [--ticloud] [--max-results N] [--dry-run]
  reversinglabs.py containers <hash> [--dry-run]
  reversinglabs.py extracted <hash> [--max-results N] [--dry-run]
  reversinglabs.py yara-matches <ruleset_name> [--max-results N] [--dry-run]

Advanced search query examples:
  threatname:Win32.Backdoor.Prorat
  classification:malicious sampletype:PE32
  av-detection:Lockbit firstseen:>2025-01-01
  tlsh:T1A2B3C4...
  positives:>=20

Exit codes:
  0  success
  1  network / API error
  2  missing REVERSINGLABS_USER or REVERSINGLABS_PASSWORD (only when not --dry-run)
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
VENV_DIR = SCRIPT_DIR / ".venv-reversinglabs"
VENV_PY = VENV_DIR / "bin" / "python"


def _bootstrap_venv():
    print(f"first run: creating Python venv at {VENV_DIR} and installing reversinglabs-sdk-py3...", file=sys.stderr)
    subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)],
                          stdout=subprocess.DEVNULL)
    subprocess.check_call([str(VENV_PY), "-m", "pip", "install", "--quiet",
                           "--disable-pip-version-check", "reversinglabs-sdk-py3"])
    print("bootstrap complete.", file=sys.stderr)


if os.environ.get("CTI_REVERSINGLABS_VENV") != "1":
    if not VENV_PY.exists():
        _bootstrap_venv()
    os.environ["CTI_REVERSINGLABS_VENV"] = "1"
    os.execv(str(VENV_PY), [str(VENV_PY), str(pathlib.Path(__file__).resolve())] + sys.argv[1:])

# ---------------------------------------------------------------------------
# Inside venv from here on.
# Strip the script directory from sys.path so we don't shadow any package
# named `reversinglabs` or `ReversingLabs` if one is ever added there.
# ---------------------------------------------------------------------------
import argparse
import json
from datetime import datetime, timezone

sys.path = [p for p in sys.path if pathlib.Path(p or ".").resolve() != SCRIPT_DIR]

from ReversingLabs.SDK.a1000 import A1000  # noqa: E402


USER = os.environ.get("REVERSINGLABS_USER", "")
PASSWORD = os.environ.get("REVERSINGLABS_PASSWORD", "")
HOST = os.environ.get("REVERSINGLABS_HOST", "https://a1000.reversinglabs.com")

# Default field lists for v2 reports. Match the SDK's __FIELDS_V2 in spirit
# but trimmed to the fields a CTI analyst actually consumes.
DEFAULT_DETAILED_FIELDS = (
    "id,sha1,sha256,md5,filename,size,sampletype,classification,riskscore,"
    "classification_result,classification_reason,classification_origin,"
    "av_scanners_summary,av_scanners,tags,ticore,ticloud,attack,"
    "rl_cloud_sandbox,networkthreatintelligence,domainthreatintelligence,"
    "extracted_file_count,sources,aliases,first_seen,last_seen"
).split(",")

DEFAULT_SUMMARY_FIELDS = (
    "id,sha1,sha256,md5,filename,size,sampletype,classification,riskscore,"
    "classification_result,av_scanners_summary,tags,first_seen,last_seen"
).split(",")


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def make_client():
    if not USER or not PASSWORD:
        die("REVERSINGLABS_USER and REVERSINGLABS_PASSWORD must be set. "
            "Run /cti-setup or ./scripts/setup.sh", 2)
    return A1000(
        host=HOST,
        username=USER,
        password=PASSWORD,
        verify=True,
        user_agent="cti-skills/lookup-reversinglabs/1.0",
    )


def envelope(operation, indicator, type_, **extra):
    out = {
        "source": "reversinglabs",
        "operation": operation,
        "indicator": indicator,
        "type": type_,
        "host": HOST,
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
    except Exception as e:  # SDK raises a variety of subclasses; any of them = network/API error from our POV
        die(f"ReversingLabs {label} error: {e}", 1)


# ---------------------------------------------------------------------------
# Hash / report
# ---------------------------------------------------------------------------

def cmd_hash(args):
    if args.dry_run:
        emit({"dry_run": True, "operation": "hash", "indicator": args.hash,
              "endpoint": "/api/samples/v3/{hash}/classification/",
              "params": {"localOnly": not args.ticloud, "av_scanners": args.av_scanners}})
        return
    client = make_client()
    resp = _api_call("classification",
                     lambda: client.get_classification_v3(
                         sample_hash=args.hash,
                         local_only=not args.ticloud,
                         av_scanners=args.av_scanners,
                     ))
    body = resp.json() if hasattr(resp, "json") else resp
    emit(envelope("hash_classification", args.hash, "hash", classification=body))


def cmd_report(args):
    fields = [f.strip() for f in args.fields.split(",") if f.strip()] if args.fields else None
    detailed = args.detailed or not args.summary  # default to detailed
    if not fields:
        fields = DEFAULT_DETAILED_FIELDS if detailed else DEFAULT_SUMMARY_FIELDS

    if args.dry_run:
        emit({"dry_run": True,
              "operation": "report_detailed" if detailed else "report_summary",
              "indicator": args.hash,
              "endpoint": "/api/samples/v2/list/details/" if detailed else "/api/samples/v2/list/",
              "fields": fields})
        return

    client = make_client()
    if detailed:
        resp = _api_call("detailed_report",
                         lambda: client.get_detailed_report_v2(
                             sample_hashes=args.hash,
                             retry=True,
                             fields=fields,
                         ))
    else:
        resp = _api_call("summary_report",
                         lambda: client.get_summary_report_v2(
                             sample_hashes=args.hash,
                             retry=True,
                             fields=fields,
                         ))
    body = resp.json() if hasattr(resp, "json") else resp
    emit(envelope(
        "report_detailed" if detailed else "report_summary",
        args.hash, "hash",
        report=body,
    ))


# ---------------------------------------------------------------------------
# Submission
# ---------------------------------------------------------------------------

def cmd_submit_file(args):
    if args.dry_run:
        emit({"dry_run": True, "operation": "submit-file",
              "path": args.path, "wait": args.wait,
              "rl_cloud_sandbox": args.rl_cloud_sandbox,
              "endpoint": "/api/uploads/"})
        return

    if not pathlib.Path(args.path).is_file():
        die(f"file not found: {args.path}", 3)

    client = make_client()
    if args.wait:
        resp = _api_call("submit_file_and_get_detailed_report",
                         lambda: client.submit_file_and_get_detailed_report(
                             file_path=args.path,
                             rl_cloud_sandbox=args.rl_cloud_sandbox,
                         ))
    else:
        resp = _api_call("submit_file",
                         lambda: client.submit_file_from_path(
                             file_path=args.path,
                             rl_cloud_sandbox=args.rl_cloud_sandbox,
                         ))
    body = resp.json() if hasattr(resp, "json") else resp
    emit(envelope("submit_file", args.path, "file",
                  waited=args.wait, response=body))


def cmd_submit_url(args):
    if args.dry_run:
        emit({"dry_run": True, "operation": "submit-url",
              "url": args.url, "wait": args.wait, "crawler": args.crawler,
              "endpoint": "/api/uploads/url"})
        return

    client = make_client()
    if args.wait:
        resp = _api_call("submit_url_and_get_report",
                         lambda: client.submit_url_and_get_report(
                             url_string=args.url, crawler=args.crawler))
    else:
        resp = _api_call("submit_url",
                         lambda: client.submit_url(
                             url_string=args.url, crawler=args.crawler))
    body = resp.json() if hasattr(resp, "json") else resp
    emit(envelope("submit_url", args.url, "url",
                  waited=args.wait, crawler=args.crawler, response=body))


# ---------------------------------------------------------------------------
# Network threat intelligence (URL / domain / IP)
# ---------------------------------------------------------------------------

def cmd_url(args):
    if args.dry_run:
        emit({"dry_run": True, "operation": "network_url_report",
              "url": args.url,
              "endpoint": "/api/network-threat-intel/url/"})
        return
    client = make_client()
    resp = _api_call("network_url_report",
                     lambda: client.network_url_report(requested_url=args.url))
    body = resp.json() if hasattr(resp, "json") else resp
    emit(envelope("network_url_report", args.url, "url", report=body))


def cmd_domain(args):
    if args.dry_run:
        emit({"dry_run": True, "operation": "network_domain_report",
              "domain": args.domain,
              "endpoint": "/api/network-threat-intel/domain/{domain}/"})
        return
    client = make_client()
    resp = _api_call("network_domain_report",
                     lambda: client.network_domain_report(domain=args.domain))
    body = resp.json() if hasattr(resp, "json") else resp
    emit(envelope("network_domain_report", args.domain, "domain", report=body))


def cmd_ip(args):
    pivots = [p.strip() for p in (args.pivot or "").split(",") if p.strip()]
    if args.dry_run:
        emit({"dry_run": True, "operation": "network_ip_report",
              "ip": args.ip, "pivots": pivots, "max_results": args.max_results,
              "endpoints": [
                  "/api/network-threat-intel/ip/{ip}/report/",
                  "/api/network-threat-intel/ip/{ip}/downloaded_files/" if "files" in pivots else None,
                  "/api/network-threat-intel/ip/{ip}/resolutions/" if "domains" in pivots else None,
                  "/api/network-threat-intel/ip/{ip}/urls/" if "urls" in pivots else None,
              ]})
        return

    client = make_client()
    resp = _api_call("network_ip_addr_report",
                     lambda: client.network_ip_addr_report(ip_addr=args.ip))
    report = resp.json() if hasattr(resp, "json") else resp

    pivots_out = {}
    if "files" in pivots:
        files = _api_call("network_files_from_ip",
                          lambda: client.network_files_from_ip_aggregated(
                              ip_addr=args.ip, max_results=args.max_results))
        pivots_out["files"] = files
    if "domains" in pivots:
        domains = _api_call("network_ip_to_domain",
                            lambda: client.network_ip_to_domain_aggregated(
                                ip_addr=args.ip, max_results=args.max_results))
        pivots_out["domains"] = domains
    if "urls" in pivots:
        urls = _api_call("network_urls_from_ip",
                         lambda: client.network_urls_from_ip_aggregated(
                             ip_addr=args.ip, max_results=args.max_results))
        pivots_out["urls"] = urls

    out = envelope("network_ip_report", args.ip, "ip", report=report)
    if pivots_out:
        out["pivots"] = pivots_out
    emit(out)


# ---------------------------------------------------------------------------
# Advanced search
# ---------------------------------------------------------------------------

def cmd_search(args):
    if args.dry_run:
        emit({"dry_run": True, "operation": "advanced_search",
              "query": args.query, "ticloud": args.ticloud,
              "max_results": args.max_results,
              "endpoint": "/api/samples/v2/advanced_search/"})
        return
    client = make_client()
    results = _api_call("advanced_search_v3",
                        lambda: client.advanced_search_v3_aggregated(
                            query_string=args.query,
                            ticloud=args.ticloud,
                            max_results=args.max_results))
    emit(envelope("advanced_search", args.query, "query",
                  ticloud=args.ticloud, count=len(results) if hasattr(results, "__len__") else None,
                  results=results))


# ---------------------------------------------------------------------------
# Container / extracted relationships
# ---------------------------------------------------------------------------

def cmd_containers(args):
    if args.dry_run:
        emit({"dry_run": True, "operation": "containers",
              "indicator": args.hash,
              "endpoint": "/api/samples/containers/"})
        return
    client = make_client()
    resp = _api_call("list_containers_for_hashes",
                     lambda: client.list_containers_for_hashes(sample_hashes=[args.hash]))
    body = resp.json() if hasattr(resp, "json") else resp
    emit(envelope("containers", args.hash, "hash", containers=body))


def cmd_extracted(args):
    if args.dry_run:
        emit({"dry_run": True, "operation": "extracted",
              "indicator": args.hash, "max_results": args.max_results,
              "endpoint": "/api/samples/v2/{hash}/extracted-files/"})
        return
    client = make_client()
    results = _api_call("list_extracted_files_v2",
                        lambda: client.list_extracted_files_v2_aggregated(
                            sample_hash=args.hash,
                            max_results=args.max_results))
    emit(envelope("extracted_files", args.hash, "hash",
                  count=len(results) if hasattr(results, "__len__") else None,
                  files=results))


# ---------------------------------------------------------------------------
# YARA — read-only matches lookup
# ---------------------------------------------------------------------------

def cmd_yara_matches(args):
    if args.dry_run:
        emit({"dry_run": True, "operation": "yara_matches",
              "ruleset": args.ruleset_name, "max_results": args.max_results,
              "endpoint": "/api/yara/v2/ruleset/{ruleset_name}/matches/"})
        return
    client = make_client()
    # The SDK's get_yara_ruleset_matches_v2 paginates manually. Walk pages
    # until exhausted or max_results reached.
    matches = []
    page = None
    page_size = 100
    while True:
        resp = _api_call("get_yara_ruleset_matches_v2",
                         lambda: client.get_yara_ruleset_matches_v2(
                             ruleset_name=args.ruleset_name,
                             page=page, page_size=page_size))
        body = resp.json() if hasattr(resp, "json") else resp
        items = (body or {}).get("results") or (body or {}).get("matches") or []
        matches.extend(items)
        next_url = (body or {}).get("next")
        if not next_url or len(matches) >= args.max_results:
            break
        # SDK uses cursor-style 'next' URLs; the page param is a positional offset
        # for some endpoints. Fall back to page increment if next is opaque.
        page = (page or 1) + 1
    matches = matches[: args.max_results]
    emit(envelope("yara_matches", args.ruleset_name, "ruleset",
                  count=len(matches), matches=matches))


# ---------------------------------------------------------------------------
# argparse
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        prog="reversinglabs.py",
        description="ReversingLabs Spectra Analyze (A1000) CLI — uses reversinglabs-sdk-py3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("hash", help="classification + AV detection ratio for a hash")
    p.add_argument("hash")
    p.add_argument("--av-scanners", action="store_true",
                   help="include per-AV-engine results")
    p.add_argument("--ticloud", action="store_true",
                   help="extend to Spectra Intelligence (TitaniumCloud) — uses appliance license")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_hash)

    p = sub.add_parser("report", help="full enrichment report on a hash (incl. MITRE ATT&CK)")
    p.add_argument("hash")
    grp = p.add_mutually_exclusive_group()
    grp.add_argument("--summary", action="store_true",
                     help="condensed report (faster, fewer fields)")
    grp.add_argument("--detailed", action="store_true",
                     help="full report (default)")
    p.add_argument("--fields",
                   help="comma list of fields to request (overrides default)")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("submit-file", help="upload a file for analysis")
    p.add_argument("path", help="local filesystem path to the file")
    p.add_argument("--wait", action="store_true",
                   help="block until analysis completes and return the detailed report")
    p.add_argument("--rl-cloud-sandbox", default=None,
                   help="cloud sandbox platform (e.g. windows10, windows11, linux). Default: appliance config.")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_submit_file)

    p = sub.add_parser("submit-url", help="submit a URL for analysis")
    p.add_argument("url")
    p.add_argument("--wait", action="store_true",
                   help="block until analysis completes")
    p.add_argument("--crawler", default="local",
                   help="crawler backend: local | tcb | cape | fireeye | vmray (appliance-dependent)")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_submit_url)

    p = sub.add_parser("url", help="network reputation for a URL (no submission)")
    p.add_argument("url")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_url)

    p = sub.add_parser("domain", help="network reputation for a domain")
    p.add_argument("domain")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_domain)

    p = sub.add_parser("ip", help="network reputation for an IP, optional pivots to files/domains/urls")
    p.add_argument("ip")
    p.add_argument("--pivot", help="comma list of pivots: files,domains,urls (each is a separate API call)")
    p.add_argument("--max-results", type=int, default=50,
                   help="max items per pivot (default 50)")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_ip)

    p = sub.add_parser("search", help="advanced search — pivot by threatname, classification, AV signature")
    p.add_argument("query")
    p.add_argument("--ticloud", action="store_true",
                   help="extend search to Spectra Intelligence corpus")
    p.add_argument("--max-results", type=int, default=100)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("containers", help="parent-container files for an extracted hash")
    p.add_argument("hash")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_containers)

    p = sub.add_parser("extracted", help="files unpacked from a container hash")
    p.add_argument("hash")
    p.add_argument("--max-results", type=int, default=200)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_extracted)

    p = sub.add_parser("yara-matches", help="samples matched by a YARA ruleset (read-only)")
    p.add_argument("ruleset_name")
    p.add_argument("--max-results", type=int, default=200)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_yara_matches)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
