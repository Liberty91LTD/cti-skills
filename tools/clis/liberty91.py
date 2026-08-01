#!/usr/bin/env python3
"""
liberty91.py — Liberty91 platform API v1 CLI (stdlib only, no install).

Liberty91 exposes two layers and the distinction drives every integration:

  * a **Threat Event** is a real-world occurrence — one breach, one
    exploitation campaign, one leak — deduplicated, with every source
    your account is entitled to attached.
  * an **Event** is one *report* about an occurrence. Five write-ups of
    one breach are five Events and one Threat Event.

Start at `threat-events`. Only drop to `events` when you specifically
want the individual documents.

API base: https://api.liberty91.com/api/v1   ($LIBERTY91_API_URL overrides)
Auth:     header `X-API-Key: $LIBERTY91_API_KEY`
Docs:     https://api.liberty91.com/api/v1/docs/  (public, no key)

Usage:
  # ----- connectivity / quota -----
  liberty91.py quota                                   # rate-limit + credit headers

  # ----- threat events (the occurrence layer — START HERE) -----
  liberty91.py threat-events [--relevant] [--verification V] [--min-credibility N]
                             [--event-class C] [--event-type T] [--technique T1566]
                             [--target-country CC] [--target-sector S] [--source-country CC]
                             [--source-count 1|2|3+] [--q TEXT] [--organization UUID]
                             [--intel-requirement UUID]
                             [--occurred-after D] [--occurred-before D]
                             [--last-reported-after D] [--last-reported-before D]
                             [--page-size N] [--cursor URL] [--all] [--max-pages N]
  liberty91.py threat-event <id> [--section detail|iocs|sources|stix|iocs-export] [--out FILE]
                             (--section sources paginates: [--page-size N] [--all] [--max-pages N])

  # ----- threat library (the canonical catalog) -----
  liberty91.py library <threat-actors|malware|vulnerabilities|clusters>
                             [--name N] [--alias A] [--q SUBSTR] [--tracked]
                             [--include-empty] [--page-size N] [--cursor URL] [--all]
  liberty91.py entity <entity_type> <id>
                             [--section detail|iocs|related|techniques|threat-events|stix|iocs-export]
                             [--out FILE]

  # ----- search (returns Threat Events; POST but read-only) -----
  liberty91.py search [--free-text T] [--date-from D] [--date-to D]
                      [--target-country CC ...] [--target-sector S ...]
                      [--target-region R ...] [--source-country CC ...]
                      [--actor-id ID ...] [--malware-id ID ...] [--vulnerability-id ID ...]
                      [--cluster-id ID ...] [--match-logic ALL|ANY]
                      [--query-tree-file F] [--page-size N] [--all]
  liberty91.py saved-searches
  liberty91.py saved-search <id>
  liberty91.py run-search <id> [--page-size N] [--all]

  # ----- events (individual reports) -----
  liberty91.py events [--since D] [--threat-event UUID] [--enrichment-status S] [--all]
  liberty91.py event <id>
  liberty91.py ingest --title T (--text TEXT | --text-file F) [--source S] [--url U]
                      [--actor NAME ...] [--malware NAME ...] [--vulnerability CVE ...]
                      # WRITE — publishes to your Liberty91 account. Confirm first.

  # ----- IOCs -----
  liberty91.py ioc-lookup <value>                      # exact-value lookup
  liberty91.py iocs [--kind K] [--verdict V] [--tlp T] [--search SUBSTR] [--since D]
                    [--whitelisted true|false] [--all]
  liberty91.py ioc-export [--format csv|stix] [--out FILE]

  # ----- intelligence packages -----
  liberty91.py reports [--status S] [--organization-id UUID] [--all]
  liberty91.py report <id>
  liberty91.py report-download <id> [--type md|csv|stix|sigma|pdf] --out FILE
  liberty91.py report-generate [--event-instance-id ID ...] [--organization-id ID ...]
                               [--chapter C ...] [--intelligence-requirement ID]
                               # WRITE — charged per report generated. Confirm first.

  # ----- alerts -----
  liberty91.py alerts [--all]
  liberty91.py alert-matches <id> [--results reports] [--all]

  # ----- organizations -----
  liberty91.py orgs [--all]
  liberty91.py org <org_id> --section assets|suppliers|documents [--all]
  liberty91.py org-document <org_id> <doc_id>          # extraction status
  liberty91.py upload-document <org_id> <file> [--description D]   # WRITE (orgs.write)
  liberty91.py confirm-entities <org_id> <doc_id> --id ID [--id ID ...]  # WRITE
  liberty91.py refresh-description <asset|supplier> <entity_id>          # WRITE

All commands accept --dry-run (preview the request without sending) and
--insecure (skip TLS verification; only for non-production hosts).

Every successful response carries a `_meta` block echoing the account's
rate-limit and monthly-credit headers — watch `credits_remaining`.

Exit codes:
  0  success
  1  network / API error (4xx, 5xx, rate limit, credits exhausted)
  2  missing $LIBERTY91_API_KEY (only when not --dry-run)
  3  bad arguments / file not found
"""

import argparse
import json
import mimetypes
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone

API_KEY = os.environ.get("LIBERTY91_API_KEY", "")
BASE_URL = os.environ.get("LIBERTY91_API_URL", "https://api.liberty91.com/api/v1").rstrip("/")
PROXY = os.environ.get("LIBERTY91_PROXY") or os.environ.get("HTTPS_PROXY") or ""

ENTITY_TYPES = ["threat-actors", "malware", "vulnerabilities", "clusters"]
# Sub-resources the library returns 400 for on account-local clusters.
CLUSTER_UNSUPPORTED = {"techniques", "threat-events", "related"}

MAX_PAGES_DEFAULT = 10


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


# ---------- HTTP ----------

def _abs(path):
    return f"{BASE_URL}{path}"


def _qs(params):
    pairs = [(k, v) for k, v in (params or {}).items() if v is not None and v != ""]
    flat = []
    for k, v in pairs:
        if isinstance(v, (list, tuple)):
            flat.extend((k, str(i)) for i in v)
        elif isinstance(v, bool):
            flat.append((k, "true" if v else "false"))
        else:
            flat.append((k, str(v)))
    return ("?" + urllib.parse.urlencode(flat)) if flat else ""


def _opener(insecure):
    handlers = []
    ctx = None
    if insecure:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    if PROXY:
        handlers.append(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
    if ctx is not None:
        handlers.append(urllib.request.HTTPSHandler(context=ctx))
    return urllib.request.build_opener(*handlers) if handlers else None


def _meta_from(headers):
    """Echo the rate-limit and credit headers the platform sets on every response."""
    def h(name):
        return headers.get(name) if headers else None
    meta = {
        "rate_limit": h("X-RateLimit-Limit"),
        "rate_limit_remaining": h("X-RateLimit-Remaining"),
        "rate_limit_reset": h("X-RateLimit-Reset"),
        "credits_limit": h("X-Credits-Limit"),
        "credits_remaining": h("X-Credits-Remaining"),
    }
    return {k: v for k, v in meta.items() if v is not None}


def _fail_http(status, reason, body_txt, headers):
    """Map the documented status codes onto actionable messages."""
    detail = ""
    try:
        detail = (json.loads(body_txt) or {}).get("detail") or ""
    except (json.JSONDecodeError, AttributeError):
        detail = body_txt[:300]
    hints = {
        400: "unknown filter value, malformed date, or invalid body — `detail` names the field "
             "(an unrecognised filter value is a 400, never an empty result set)",
        401: "missing, malformed, revoked or expired key — check $LIBERTY91_API_KEY",
        403: "the key lacks a required scope — grant the scope named in `detail`",
        404: "not found, or not in your billing account — the two are indistinguishable by "
             "design. If an entire collection 404s (e.g. /threat-events/), the host may predate "
             "API v2.0 — run `liberty91.py quota` to see which surface is deployed",
        409: "the user who created this key is no longer active on the account — rotate the key",
        503: "an upstream dependency is unavailable — retry with backoff; writes are NOT retried "
             "server-side, resubmit them",
    }
    hint = hints.get(status, "")
    if status == 429:
        credits = (headers or {}).get("X-Credits-Remaining")
        retry_after = (headers or {}).get("Retry-After")
        if credits is not None and str(credits).strip() in ("0", "0.0"):
            hint = "monthly credits exhausted (X-Credits-Remaining: 0) — this is not a rate limit"
        else:
            hint = f"rate limited — back off for Retry-After={retry_after or 'unknown'}s " \
                   f"(credits remaining: {credits if credits is not None else 'unknown'})"
    msg = f"HTTP {status} {reason}"
    if detail:
        msg += f": {detail}"
    if hint:
        msg += f"\nhint: {hint}"
    die(msg, 1)


def _http(method, url, body=None, content_type=None, accept="application/json",
          dry_run=False, insecure=False, dry_body=None, tolerate_statuses=()):
    """Perform one request. Returns (body_bytes, headers_dict).

    A status listed in `tolerate_statuses` returns (None, headers) instead of
    exiting — used by `quota` to probe whether an endpoint exists at all.
    """
    if dry_run:
        preview = {
            "dry_run": True,
            "method": method,
            "url": url,
            "headers": {
                "X-API-Key": "<redacted>" if API_KEY else "<unset>",
                "Accept": accept,
                **({"Content-Type": content_type} if content_type else {}),
            },
            "body": dry_body,
            "tls_verify": not insecure,
        }
        print(json.dumps(preview, indent=2))
        sys.exit(0)

    if not API_KEY:
        die("LIBERTY91_API_KEY not set. Add it to .claude/settings.local.json env or export it.", 2)

    headers = {"X-API-Key": API_KEY, "Accept": accept}
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    opener = _opener(insecure)
    try:
        if opener is not None:
            resp = opener.open(req, timeout=120)
        else:
            resp = urllib.request.urlopen(req, timeout=120)
        with resp as r:
            return r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf-8", errors="replace") if e.fp else ""
        if e.code in tolerate_statuses:
            return None, dict(e.headers or {})
        _fail_http(e.code, e.reason, txt, dict(e.headers or {}))
    except urllib.error.URLError as e:
        die(f"network error: {e.reason} — check LIBERTY91_API_URL ({BASE_URL})", 1)


def get_json(url, args, accept="application/json"):
    raw, headers = _http("GET", url, accept=accept,
                         dry_run=getattr(args, "dry_run", False),
                         insecure=getattr(args, "insecure", False))
    try:
        return json.loads(raw.decode("utf-8")), headers
    except (json.JSONDecodeError, UnicodeDecodeError):
        die(f"non-JSON response from {url}: {raw[:300]!r}", 1)


def post_json(url, payload, args):
    body = json.dumps(payload).encode("utf-8")
    raw, headers = _http("POST", url, body=body, content_type="application/json",
                         dry_run=getattr(args, "dry_run", False),
                         insecure=getattr(args, "insecure", False),
                         dry_body=payload)
    if not raw:
        return {}, headers
    try:
        return json.loads(raw.decode("utf-8")), headers
    except (json.JSONDecodeError, UnicodeDecodeError):
        die(f"non-JSON response from {url}: {raw[:300]!r}", 1)


def emit(operation, payload, meta=None):
    out = {"source": "liberty91", "operation": operation, "query_time": now_iso()}
    out.update(payload)
    if meta:
        out["_meta"] = meta
    print(json.dumps(out, indent=2))


def write_out(path, data, operation, extra=None, meta=None):
    """Write a binary/large artifact to disk and report where it went."""
    try:
        with open(path, "wb") as f:
            f.write(data)
    except OSError as e:
        die(f"could not write {path}: {e}", 3)
    payload = {"file": os.path.abspath(path), "bytes": len(data)}
    payload.update(extra or {})
    emit(operation, payload, meta)


# ---------- cursor pagination ----------

def paginate(url, args, method="GET", payload=None):
    """Walk cursor pages. Returns (results, next_url, pages_walked, meta, envelope).

    `next` is a complete URL — never build cursor params by hand. POST-backed
    endpoints (search, run-search) are re-POSTed with the same body against the
    cursor URL, which is how DRF cursor pagination behaves for POST list views.
    """
    follow_all = getattr(args, "all", False)
    max_pages = getattr(args, "max_pages", None) or MAX_PAGES_DEFAULT
    results, pages, envelope, meta = [], 0, {}, {}
    next_url = None
    while url:
        if method == "POST":
            envelope, headers = post_json(url, payload or {}, args)
        else:
            envelope, headers = get_json(url, args)
        meta = _meta_from(headers)
        results.extend(envelope.get("results") or [])
        next_url = envelope.get("next")
        pages += 1
        if not follow_all or not next_url or pages >= max_pages:
            break
        url = next_url
    truncated = bool(next_url) and follow_all and pages >= max_pages
    return results, next_url, pages, meta, envelope, truncated


def emit_list(operation, results, next_url, pages, meta, envelope, truncated, extra=None):
    payload = {
        "count": len(results),
        "pages_walked": pages,
        "next": next_url,
        "results": results,
    }
    if truncated:
        payload["truncated"] = True
        payload["note"] = ("stopped at --max-pages; more pages remain — pass the `next` URL "
                           "via --cursor or raise --max-pages")
    if "unlinked_report_count" in (envelope or {}):
        payload["unlinked_report_count"] = envelope["unlinked_report_count"]
    payload.update(extra or {})
    emit(operation, payload, meta)


# ---------- connectivity ----------

def cmd_quota(args):
    """Cheapest authenticated call (1 credit) that returns the quota headers.

    Also reports whether the Threat Event (occurrence) layer is reachable on
    this host — a 404 there means the deployment predates API v2.0 and only
    the report-level surface (`events`, `iocs`, `reports`, `alerts`,
    `organizations`) will answer.
    """
    raw, headers = _http("GET", _abs("/threat-events/") + _qs({"page_size": 1}),
                         dry_run=args.dry_run, insecure=args.insecure,
                         tolerate_statuses=(404,))
    occurrence_layer = raw is not None
    payload = {"authenticated": True, "base_url": BASE_URL,
               "occurrence_layer_available": occurrence_layer}
    if not occurrence_layer:
        # Fall back to a surface that exists on every deployment, so the quota
        # headers still come back.
        raw, headers = _http("GET", _abs("/iocs/") + _qs({"page_size": 1}),
                             insecure=args.insecure)
        payload["note"] = (
            "`/threat-events/` returned 404 — this host does not serve the API v2.0 "
            "occurrence layer (also no `/search/` or `/threat-library/`). Use `events`, "
            "`iocs`, `reports`, `alerts` and `organizations`, and dedupe reports yourself. "
            "Check https://api.liberty91.com/api/v1/schema/ for the surface actually deployed."
        )
    else:
        payload["note"] = "one read costs 1 credit; failed requests (4xx/5xx) are never charged"
    emit("quota", payload, _meta_from(headers))


# ---------- threat events ----------

def cmd_threat_events(args):
    params = {
        "relevant": "true" if args.relevant else None,
        "verification": args.verification,
        "min_credibility": args.min_credibility,
        "event_class": args.event_class,
        "event_type": args.event_type,
        "technique": args.technique,
        "target_country": args.target_country,
        "target_sector": args.target_sector,
        "source_country": args.source_country,
        "source_count": args.source_count,
        "q": args.q,
        "organization": args.organization,
        "intel_requirement": args.intel_requirement,
        "occurred_after": args.occurred_after,
        "occurred_before": args.occurred_before,
        "last_reported_after": args.last_reported_after,
        "last_reported_before": args.last_reported_before,
        "page_size": args.page_size,
    }
    url = args.cursor or (_abs("/threat-events/") + _qs(params))
    results, nxt, pages, meta, env, trunc = paginate(url, args)
    emit_list("threat-events", results, nxt, pages, meta, env, trunc,
              extra={"filters": {k: v for k, v in params.items() if v not in (None, "")}})


THREAT_EVENT_SECTIONS = {
    "detail": ("", "application/json"),
    "iocs": ("iocs/", "application/json"),
    # v2.1: the full, paginated report list. The detail's embedded sources[] is capped,
    # so for counting or citing reporting this is the record and that is a sample.
    # Needs threat-events.read + events.read.
    "sources": ("sources/", "application/json"),
    "stix": ("stix/", "application/stix+json"),
    "iocs-export": ("iocs/export/", "application/stix+json"),
}


def cmd_threat_event(args):
    suffix, accept = THREAT_EVENT_SECTIONS[args.section]
    if args.section == "sources":
        # Paginated, unlike every other section — walk it rather than reading one page.
        url = args.cursor or (_abs(f"/threat-events/{args.id}/sources/")
                              + _qs({"page_size": args.page_size}))
        results, nxt, pages, meta, env, trunc = paginate(url, args)
        emit_list("threat-event-sources", results, nxt, pages, meta, env, trunc,
                  extra={"threat_event_id": args.id,
                         "note": "the complete report list; the detail's embedded sources[] "
                                 "is capped and is only a sample. Masked to what this "
                                 "account is entitled to."})
        return
    url = _abs(f"/threat-events/{args.id}/{suffix}")
    raw, headers = _http("GET", url, accept=accept,
                         dry_run=args.dry_run, insecure=args.insecure)
    meta = _meta_from(headers)
    if args.out:
        write_out(args.out, raw, f"threat-event-{args.section}",
                  {"threat_event_id": args.id}, meta)
        return
    try:
        data = json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        die("response was not JSON — pass --out to save it to a file", 1)
    if args.section == "detail":
        emit("threat-event", {"threat_event": data}, meta)
    elif args.section == "iocs":
        emit("threat-event-iocs", {
            "threat_event_id": args.id,
            "count": len(data.get("results") or []),
            "truncated": data.get("truncated"),
            "results": data.get("results") or [],
        }, meta)
    else:
        emit(f"threat-event-{args.section}", {
            "threat_event_id": args.id,
            "bundle": data,
            "note": "parented STIX bundle — carries the occurrence plus relationships to its "
                    "indicators, so a TIP keeps the context",
        }, meta)


# ---------- threat library ----------

def cmd_library(args):
    params = {
        "name": args.name,
        "alias": args.alias,
        "q": args.q,
        "tracked": "true" if args.tracked else None,
        "include_empty": "true" if args.include_empty else None,
        "page_size": args.page_size,
    }
    url = args.cursor or (_abs(f"/threat-library/{args.entity_type}/") + _qs(params))
    results, nxt, pages, meta, env, trunc = paginate(url, args)
    emit_list("library", results, nxt, pages, meta, env, trunc,
              extra={"entity_type": args.entity_type,
                     "filters": {k: v for k, v in params.items() if v not in (None, "")}})


ENTITY_SECTIONS = {
    "detail": ("", "application/json"),
    "iocs": ("iocs/", "application/json"),
    "related": ("related/", "application/json"),
    "techniques": ("techniques/", "application/json"),
    "threat-events": ("threat-events/", "application/json"),
    "stix": ("stix/", "application/stix+json"),
    "iocs-export": ("iocs/export/", "application/stix+json"),
}


def cmd_entity(args):
    if args.entity_type == "clusters" and args.section in CLUSTER_UNSUPPORTED:
        die(f"clusters are account-local groupings with no canonical record — "
            f"`{args.section}` returns 400 for them", 3)
    suffix, accept = ENTITY_SECTIONS[args.section]
    url = _abs(f"/threat-library/{args.entity_type}/{args.id}/{suffix}")
    raw, headers = _http("GET", url, accept=accept,
                         dry_run=args.dry_run, insecure=args.insecure)
    meta = _meta_from(headers)
    if args.out:
        write_out(args.out, raw, f"entity-{args.section}",
                  {"entity_type": args.entity_type, "id": args.id}, meta)
        return
    try:
        data = json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        die("response was not JSON — pass --out to save it to a file", 1)
    payload = {"entity_type": args.entity_type, "id": args.id}
    if args.section == "detail":
        payload["entity"] = data
    elif isinstance(data, dict) and "results" in data:
        payload["count"] = len(data.get("results") or [])
        payload["results"] = data["results"]
    else:
        payload["bundle"] = data
    emit(f"entity-{args.section}" if args.section != "detail" else "entity", payload, meta)


# ---------- search ----------

def _search_body(args):
    body = {}
    simple = {
        "free_text": args.free_text,
        "date_from": args.date_from,
        "date_to": args.date_to,
        "match_logic": args.match_logic,
    }
    for k, v in simple.items():
        if v:
            body[k] = v
    lists = {
        "threat_actor_ids": args.actor_id,
        "malware_ids": args.malware_id,
        "vulnerability_ids": args.vulnerability_id,
        "threat_cluster_ids": args.cluster_id,
        "asset_technology_ids": args.asset_id,
        "supplier_ids": args.supplier_id,
        "target_regions": args.target_region,
        "target_countries": args.target_country,
        "source_countries": args.source_country,
        "target_states": args.target_state,
        "target_sectors": args.target_sector,
    }
    for k, v in lists.items():
        if v:
            body[k] = list(v)
    if args.query_tree_file:
        if not os.path.isfile(args.query_tree_file):
            die(f"file not found: {args.query_tree_file}", 3)
        try:
            with open(args.query_tree_file, "r", encoding="utf-8") as f:
                body["query_tree"] = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            die(f"could not read query tree: {e}", 3)
    if not body:
        die("search needs at least one criterion (e.g. --free-text)", 3)
    return body


def cmd_search(args):
    body = _search_body(args)
    url = _abs("/search/") + _qs({"page_size": args.page_size})
    results, nxt, pages, meta, env, trunc = paginate(url, args, method="POST", payload=body)
    emit_list("search", results, nxt, pages, meta, env, trunc,
              extra={"criteria": body,
                     "note": "results are Threat Events (deduplicated occurrences), not reports"})


def cmd_saved_searches(args):
    data, headers = get_json(_abs("/searches/"), args)
    results = data.get("results") or []
    emit("saved-searches", {"count": len(results), "results": results}, _meta_from(headers))


def cmd_saved_search(args):
    data, headers = get_json(_abs(f"/searches/{args.id}/"), args)
    emit("saved-search", {"search": data}, _meta_from(headers))


def cmd_run_search(args):
    url = _abs(f"/searches/{args.id}/run/") + _qs({"page_size": args.page_size})
    results, nxt, pages, meta, env, trunc = paginate(url, args, method="POST", payload={})
    emit_list("run-search", results, nxt, pages, meta, env, trunc,
              extra={"saved_search_id": args.id})


# ---------- events (individual reports) ----------

def cmd_events(args):
    params = {
        "since": args.since,
        "threat_event": args.threat_event,
        "enrichment_status": args.enrichment_status,
        "page_size": args.page_size,
    }
    url = args.cursor or (_abs("/events/") + _qs(params))
    results, nxt, pages, meta, env, trunc = paginate(url, args)
    emit_list("events", results, nxt, pages, meta, env, trunc, extra={
        "note": "one row per report — `threat_event_id` names the deduplicated occurrence; "
                "several rows sharing one id are several write-ups of the same thing",
    })


def cmd_event(args):
    data, headers = get_json(_abs(f"/events/{args.id}/"), args)
    emit("event", {"event": data}, _meta_from(headers))


def cmd_ingest(args):
    if args.text_file:
        if not os.path.isfile(args.text_file):
            die(f"file not found: {args.text_file}", 3)
        try:
            with open(args.text_file, "r", encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            die(f"could not read {args.text_file}: {e}", 3)
    else:
        text = args.text
    if not text:
        die("provide --text or --text-file (an empty body ingests an empty report)", 3)

    body = {"title": args.title, "text": text}
    if args.source:
        body["source"] = args.source
    if args.url:
        body["url"] = args.url
    for key, values in (("threat_actors", args.actor),
                        ("malwares", args.malware),
                        ("vulnerabilities", args.vulnerability)):
        if values:
            body[key] = [{"name": v} for v in values]

    data, headers = post_json(_abs("/events/ingest/"), body, args)
    emit("ingest", {
        "event_id": data.get("event_id"),
        "event_instance_id": data.get("event_instance_id"),
        "status": data.get("status"),
        "note": "202 accepted — enrichment is asynchronous. Poll "
                "`liberty91.py event <event_id>` until enrichment_status is `complete`, "
                "then read `threat_event_id` for the occurrence it matched into. "
                "Ingested reports are private to your account; extracted IOCs are TLP:RED.",
    }, _meta_from(headers))


# ---------- IOCs ----------

def cmd_ioc_lookup(args):
    url = _abs("/iocs/lookup/") + _qs({"value": args.value})
    data, headers = get_json(url, args)
    emit("ioc-lookup", {
        "value": data.get("value", args.value),
        "found": data.get("found"),
        "count": len(data.get("results") or []),
        "results": data.get("results") or [],
        "note": "confidence is derived at read time and is null when there is genuinely no "
                "signal — do not read null as 'medium'",
    }, _meta_from(headers))


def cmd_iocs(args):
    params = {
        "kind": args.kind,
        "verdict": args.verdict,
        "tlp": args.tlp,
        "search": args.search,
        "since": args.since,
        "whitelisted": args.whitelisted,
        "page_size": args.page_size,
    }
    url = args.cursor or (_abs("/iocs/") + _qs(params))
    results, nxt, pages, meta, env, trunc = paginate(url, args)
    emit_list("iocs", results, nxt, pages, meta, env, trunc,
              extra={"filters": {k: v for k, v in params.items() if v not in (None, "")}})


def cmd_ioc_export(args):
    accept = "application/stix+json" if args.format == "stix" else "text/csv"
    url = _abs("/iocs/export/") + _qs({"format": args.format})
    raw, headers = _http("GET", url, accept=accept,
                         dry_run=args.dry_run, insecure=args.insecure)
    meta = _meta_from(headers)
    note = ("flat indicator list with no occurrence context — right for a blocklist, wrong for "
            "a TIP. For TIP sync use `threat-event <id> --section iocs-export` (parented).")
    if args.out:
        write_out(args.out, raw, "ioc-export",
                  {"format": args.format, "note": note}, meta)
        return
    if args.format == "csv":
        sys.stdout.write(raw.decode("utf-8", errors="replace"))
        return
    try:
        emit("ioc-export", {"format": "stix", "bundle": json.loads(raw.decode("utf-8")),
                            "note": note}, meta)
    except (json.JSONDecodeError, UnicodeDecodeError):
        die("STIX export was not valid JSON — pass --out to save the raw body", 1)


# ---------- intelligence packages ----------

def cmd_reports(args):
    params = {"status": args.status, "organization_id": args.organization_id,
              "page_size": args.page_size}
    url = args.cursor or (_abs("/reports/") + _qs(params))
    results, nxt, pages, meta, env, trunc = paginate(url, args)
    emit_list("reports", results, nxt, pages, meta, env, trunc)


def cmd_report(args):
    data, headers = get_json(_abs(f"/reports/{args.id}/"), args)
    emit("report", {"report": data}, _meta_from(headers))


def cmd_report_download(args):
    url = _abs(f"/reports/{args.id}/download/") + _qs({"type": args.type})
    raw, headers = _http("GET", url, accept="application/octet-stream",
                         dry_run=args.dry_run, insecure=args.insecure)
    write_out(args.out, raw, "report-download",
              {"report_id": args.id, "type": args.type}, _meta_from(headers))


def cmd_report_generate(args):
    body = {}
    if args.event_instance_id:
        body["event_instance_ids"] = list(args.event_instance_id)
    if args.organization_id:
        body["organization_ids"] = list(args.organization_id)
    if args.chapter:
        body["chapters"] = list(args.chapter)
    if args.intelligence_requirement:
        body["intelligence_requirement"] = args.intelligence_requirement
    if not body:
        die("report-generate needs at least one of --event-instance-id / --organization-id / "
            "--chapter / --intelligence-requirement", 3)
    data, headers = post_json(_abs("/reports/generate/"), body, args)
    emit("report-generate", {
        "response": data,
        "note": "queued — poll `liberty91.py report <id>` until status leaves GENERATING. "
                "Charged 50 credits per report generated.",
    }, _meta_from(headers))


# ---------- alerts ----------

def cmd_alerts(args):
    url = args.cursor or (_abs("/alerts/") + _qs({"page_size": args.page_size}))
    results, nxt, pages, meta, env, trunc = paginate(url, args)
    emit_list("alerts", results, nxt, pages, meta, env, trunc)


def cmd_alert_matches(args):
    params = {"page_size": args.page_size}
    if args.results:
        params["results"] = args.results
    url = args.cursor or (_abs(f"/alerts/{args.id}/matches/") + _qs(params))
    results, nxt, pages, meta, env, trunc = paginate(url, args)
    emit_list("alert-matches", results, nxt, pages, meta, env, trunc, extra={
        "alert_id": args.id,
        "shape": "reports" if args.results == "reports" else "threat-events",
    })


# ---------- organizations ----------

def cmd_orgs(args):
    url = args.cursor or (_abs("/organizations/") + _qs({"page_size": args.page_size}))
    results, nxt, pages, meta, env, trunc = paginate(url, args)
    emit_list("orgs", results, nxt, pages, meta, env, trunc)


ORG_SECTIONS = {"assets": "assets/", "suppliers": "suppliers/", "documents": "documents/"}


def cmd_org(args):
    url = args.cursor or (_abs(f"/organizations/{args.org_id}/{ORG_SECTIONS[args.section]}")
                          + _qs({"page_size": args.page_size}))
    results, nxt, pages, meta, env, trunc = paginate(url, args)
    emit_list(f"org-{args.section}", results, nxt, pages, meta, env, trunc,
              extra={"organization_id": args.org_id})


def cmd_org_document(args):
    data, headers = get_json(
        _abs(f"/organizations/{args.org_id}/documents/{args.doc_id}/"), args)
    emit("org-document", {"document": data}, _meta_from(headers))


def cmd_upload_document(args):
    if not os.path.isfile(args.file):
        die(f"file not found: {args.file}", 3)
    size = os.path.getsize(args.file)
    if size > 10 * 1024 * 1024:
        die(f"file is {size} bytes — the endpoint caps uploads at 10 MB", 3)
    ext = os.path.splitext(args.file)[1].lower().lstrip(".")
    if ext not in {"pdf", "txt", "csv", "xlsx", "xls", "docx", "pptx"}:
        die(f"unsupported file type '.{ext}' — allowed: pdf, txt, csv, xlsx, xls, docx, pptx", 3)
    try:
        with open(args.file, "rb") as f:
            content = f.read()
    except OSError as e:
        die(f"could not read {args.file}: {e}", 3)

    filename = os.path.basename(args.file)
    ctype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    boundary = f"----cti-skills-{uuid.uuid4().hex}"

    def part(name, value, fname=None, part_ctype=None):
        head = f'Content-Disposition: form-data; name="{name}"'
        if fname:
            head += f'; filename="{fname}"'
        head += "\r\n"
        if part_ctype:
            head += f"Content-Type: {part_ctype}\r\n"
        payload = value if isinstance(value, bytes) else value.encode("utf-8")
        return f"--{boundary}\r\n{head}\r\n".encode("utf-8") + payload + b"\r\n"

    body = part("file", content, fname=filename, part_ctype=ctype)
    if args.description:
        body += part("description", args.description)
    body += f"--{boundary}--\r\n".encode("utf-8")

    url = _abs(f"/organizations/{args.org_id}/documents/")
    raw, headers = _http("POST", url, body=body,
                         content_type=f"multipart/form-data; boundary={boundary}",
                         dry_run=args.dry_run, insecure=args.insecure,
                         dry_body={"file": filename, "bytes": size,
                                   "description": args.description})
    try:
        data = json.loads(raw.decode("utf-8")) if raw else {}
    except (json.JSONDecodeError, UnicodeDecodeError):
        data = {"raw": raw[:300].decode("utf-8", errors="replace")}
    emit("upload-document", {
        "organization_id": args.org_id,
        "file": filename,
        "bytes": size,
        "response": data,
        "note": "extraction is asynchronous — poll `liberty91.py org-document <org_id> <doc_id>` "
                "until extraction_status is done, then confirm the entities you want kept. "
                "Costs 25 credits.",
    }, _meta_from(headers))


def cmd_confirm_entities(args):
    body = {"confirmed_ids": list(args.id)}
    url = _abs(f"/organizations/{args.org_id}/documents/{args.doc_id}/entities/confirm/")
    data, headers = post_json(url, body, args)
    emit("confirm-entities", {
        "organization_id": args.org_id,
        "document_id": args.doc_id,
        "confirmed_ids": body["confirmed_ids"],
        "response": data,
        "note": "only confirmed entities become assets or suppliers",
    }, _meta_from(headers))


def cmd_refresh_description(args):
    url = _abs(f"/entities/{args.entity_type}/{args.entity_id}/update-description/")
    data, headers = post_json(url, {}, args)
    emit("refresh-description", {
        "entity_type": args.entity_type,
        "entity_id": args.entity_id,
        "response": data,
        "note": "poll the supplier or asset list until analysis_status is ready",
    }, _meta_from(headers))


# ---------- arg parsing ----------

def main():
    ap = argparse.ArgumentParser(
        prog="liberty91.py",
        description="Liberty91 platform API v1 CLI (stdlib only). Threat Events are the "
                    "deduplicated occurrence layer — start there, not at /events/.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--dry-run", action="store_true",
                       help="print the request that would be sent, then exit 0")
        p.add_argument("--insecure", action="store_true",
                       help="skip TLS verification (non-production hosts only)")

    def paged(p):
        p.add_argument("--page-size", type=int, default=None,
                       help="results per page. Omitted unless set, so the server's own "
                            "default applies: 25 (max 100) from API v2.1, 100 (max 500) "
                            "on older hosts. A v2.1 walk costs up to 4x the credits")
        p.add_argument("--cursor", help="a `next` URL from a previous page (opaque — do not build)")
        p.add_argument("--all", action="store_true", help="follow `next` until exhausted")
        p.add_argument("--max-pages", type=int, default=MAX_PAGES_DEFAULT,
                       help=f"page cap for --all (default {MAX_PAGES_DEFAULT}); each page costs credits")

    p = sub.add_parser("quota", help="connectivity check + rate-limit/credit headers")
    common(p)
    p.set_defaults(func=cmd_quota)

    # --- threat events ---
    p = sub.add_parser("threat-events", help="list deduplicated occurrences (START HERE)")
    p.add_argument("--relevant", action="store_true", help="only events matched to your account")
    p.add_argument("--verification",
                   choices=["auto", "corroborated", "verified", "disputed", "rejected", "merged"])
    p.add_argument("--min-credibility", type=int, choices=range(1, 7), metavar="1-6",
                   help="1 (best) .. 6; returns bands at least this good")
    p.add_argument("--event-class", help="e.g. security-incident, vulnerability, "
                                         "threat-development, data-exposure")
    p.add_argument("--event-type", help="taxonomy type within the class")
    p.add_argument("--technique", help="ATT&CK technique id, e.g. T1566 or T1566.001")
    p.add_argument("--target-country", help="country name or ISO code")
    p.add_argument("--target-sector", help="sector name or code")
    p.add_argument("--source-country", help="country the reporting originates from")
    p.add_argument("--source-count", choices=["1", "2", "3+"])
    p.add_argument("--q", help="free text over title and summary")
    p.add_argument("--organization", help="organization UUID — only events affecting it")
    p.add_argument("--intel-requirement", help="intelligence requirement UUID")
    p.add_argument("--occurred-after")
    p.add_argument("--occurred-before")
    p.add_argument("--last-reported-after")
    p.add_argument("--last-reported-before")
    paged(p)
    common(p)
    p.set_defaults(func=cmd_threat_events)

    p = sub.add_parser("threat-event",
                       help="one occurrence: detail, IOCs, its full source list, or STIX")
    p.add_argument("id")
    p.add_argument("--section", choices=list(THREAT_EVENT_SECTIONS), default="detail")
    p.add_argument("--out", help="write the response to this file (required for large bundles)")
    paged(p)          # only --section sources paginates; harmless elsewhere
    common(p)
    p.set_defaults(func=cmd_threat_event)

    # --- threat library ---
    p = sub.add_parser("library", help="list the canonical catalog; resolve a name to an id")
    p.add_argument("entity_type", choices=ENTITY_TYPES)
    p.add_argument("--name", help="case-insensitive exact name match")
    p.add_argument("--alias", help="case-insensitive exact alias match (vendor's name → canonical entry)")
    p.add_argument("--q", help="substring match on name (min 3 characters)")
    p.add_argument("--tracked", action="store_true", help="only entries your account tracks")
    p.add_argument("--include-empty", action="store_true",
                   help="include catalog entries with no reporting behind them yet")
    paged(p)
    common(p)
    p.set_defaults(func=cmd_library)

    p = sub.add_parser("entity", help="one catalog entry and its sub-resources")
    p.add_argument("entity_type", choices=ENTITY_TYPES)
    p.add_argument("id")
    p.add_argument("--section", choices=list(ENTITY_SECTIONS), default="detail")
    p.add_argument("--out", help="write the response to this file")
    common(p)
    p.set_defaults(func=cmd_entity)

    # --- search ---
    p = sub.add_parser("search", help="search occurrences (POST, but a read)")
    p.add_argument("--free-text")
    p.add_argument("--date-from")
    p.add_argument("--date-to")
    p.add_argument("--match-logic", choices=["ALL", "ANY"])
    p.add_argument("--actor-id", action="append")
    p.add_argument("--malware-id", action="append")
    p.add_argument("--vulnerability-id", action="append")
    p.add_argument("--cluster-id", action="append")
    p.add_argument("--asset-id", action="append", help="asset/technology id")
    p.add_argument("--supplier-id", action="append")
    p.add_argument("--target-region", action="append")
    p.add_argument("--target-country", action="append")
    p.add_argument("--target-state", action="append")
    p.add_argument("--target-sector", action="append")
    p.add_argument("--source-country", action="append")
    p.add_argument("--query-tree-file",
                   help="JSON file holding a query_tree (groups ORed, conditions within ANDed)")
    paged(p)
    common(p)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("saved-searches", help="list your account's saved searches")
    common(p)
    p.set_defaults(func=cmd_saved_searches)

    p = sub.add_parser("saved-search", help="retrieve one saved search's criteria")
    p.add_argument("id")
    common(p)
    p.set_defaults(func=cmd_saved_search)

    p = sub.add_parser("run-search", help="run a saved search, returning Threat Events")
    p.add_argument("id")
    paged(p)
    common(p)
    p.set_defaults(func=cmd_run_search)

    # --- events ---
    p = sub.add_parser("events", help="individual reports (use threat-events unless you want documents)")
    p.add_argument("--since", help="ISO 8601 date or datetime")
    p.add_argument("--threat-event", help="only reports describing this occurrence")
    p.add_argument("--enrichment-status",
                   choices=["new", "in_progress", "enriched_for_user",
                            "enriched_for_billing_account", "complete", "failed"])
    paged(p)
    common(p)
    p.set_defaults(func=cmd_events)

    p = sub.add_parser("event", help="one report (poll enrichment_status after ingest)")
    p.add_argument("id")
    common(p)
    p.set_defaults(func=cmd_event)

    p = sub.add_parser("ingest", help="WRITE — push your own report into your account")
    p.add_argument("--title", required=True)
    p.add_argument("--text", help="the report body")
    p.add_argument("--text-file", help="read the report body from a file")
    p.add_argument("--source")
    p.add_argument("--url")
    p.add_argument("--actor", action="append", help="named threat actor (repeatable)")
    p.add_argument("--malware", action="append", help="named malware family (repeatable)")
    p.add_argument("--vulnerability", action="append", help="CVE id (repeatable)")
    common(p)
    p.set_defaults(func=cmd_ingest)

    # --- IOCs ---
    p = sub.add_parser("ioc-lookup", help="exact-value IOC lookup (SIEM enrichment)")
    p.add_argument("value")
    common(p)
    p.set_defaults(func=cmd_ioc_lookup)

    p = sub.add_parser("iocs", help="list/filter IOCs")
    p.add_argument("--kind", choices=["ip", "domain", "url", "url-path", "md5", "sha1",
                                      "sha256", "filename", "other"])
    p.add_argument("--verdict", choices=["MALICIOUS", "SUSPICIOUS", "BENIGN", "UNKNOWN"])
    p.add_argument("--tlp", help="effective handling marking, e.g. TLP:RED")
    p.add_argument("--search", help="substring match on value (min 3 chars)")
    p.add_argument("--since", help="ISO 8601 created_at floor")
    p.add_argument("--whitelisted", choices=["true", "false"])
    paged(p)
    common(p)
    p.set_defaults(func=cmd_iocs)

    p = sub.add_parser("ioc-export", help="bulk IOC export (CSV max 10k rows / STIX max 5k)")
    p.add_argument("--format", choices=["csv", "stix"], default="csv")
    p.add_argument("--out", help="write to this file instead of stdout")
    common(p)
    p.set_defaults(func=cmd_ioc_export)

    # --- reports ---
    p = sub.add_parser("reports", help="list intelligence packages")
    p.add_argument("--status", choices=["GENERATING", "DRAFT", "STAGED", "SENT", "FAILED"])
    p.add_argument("--organization-id")
    paged(p)
    common(p)
    p.set_defaults(func=cmd_reports)

    p = sub.add_parser("report", help="intelligence package detail")
    p.add_argument("id")
    common(p)
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("report-download", help="download a package artifact")
    p.add_argument("id")
    p.add_argument("--type", choices=["md", "csv", "stix", "sigma", "pdf"], default="pdf")
    p.add_argument("--out", required=True)
    common(p)
    p.set_defaults(func=cmd_report_download)

    p = sub.add_parser("report-generate", help="WRITE — queue report generation (50 credits each)")
    p.add_argument("--event-instance-id", action="append")
    p.add_argument("--organization-id", action="append")
    p.add_argument("--chapter", action="append")
    p.add_argument("--intelligence-requirement")
    common(p)
    p.set_defaults(func=cmd_report_generate)

    # --- alerts ---
    p = sub.add_parser("alerts", help="list alert rules and their criteria")
    paged(p)
    common(p)
    p.set_defaults(func=cmd_alerts)

    p = sub.add_parser("alert-matches", help="what an alert rule matched")
    p.add_argument("id")
    p.add_argument("--results", choices=["reports"],
                   help="return individual reports instead of Threat Events")
    paged(p)
    common(p)
    p.set_defaults(func=cmd_alert_matches)

    # --- organizations ---
    p = sub.add_parser("orgs", help="list your customer organizations")
    paged(p)
    common(p)
    p.set_defaults(func=cmd_orgs)

    p = sub.add_parser("org", help="an organization's assets, suppliers, or documents")
    p.add_argument("org_id")
    p.add_argument("--section", choices=list(ORG_SECTIONS), required=True)
    paged(p)
    common(p)
    p.set_defaults(func=cmd_org)

    p = sub.add_parser("org-document", help="document extraction status")
    p.add_argument("org_id")
    p.add_argument("doc_id")
    common(p)
    p.set_defaults(func=cmd_org_document)

    p = sub.add_parser("upload-document", help="WRITE — upload a document for entity extraction")
    p.add_argument("org_id")
    p.add_argument("file", help="pdf, txt, csv, xlsx, xls, docx or pptx — max 10 MB")
    p.add_argument("--description")
    common(p)
    p.set_defaults(func=cmd_upload_document)

    p = sub.add_parser("confirm-entities", help="WRITE — confirm entities extracted from a document")
    p.add_argument("org_id")
    p.add_argument("doc_id")
    p.add_argument("--id", action="append", required=True, help="entity id to confirm (repeatable)")
    common(p)
    p.set_defaults(func=cmd_confirm_entities)

    p = sub.add_parser("refresh-description", help="WRITE — regenerate an asset/supplier profile")
    p.add_argument("entity_type", choices=["asset", "supplier"])
    p.add_argument("entity_id")
    common(p)
    p.set_defaults(func=cmd_refresh_description)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
