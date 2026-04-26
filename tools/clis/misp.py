#!/usr/bin/env python3
"""
misp.py — MISP REST API CLI (stdlib only, no install).

Two-way: query what's in a MISP instance AND push new intel to it. The
write surface includes adding attributes to existing events and creating
new events from a STIX 2 bundle.

Auth: header `Authorization: <MISP_API_KEY>` (NOT `Bearer <key>`).
Base URL is taken from $MISP_URL (e.g., https://misp.example.org).

Usage:
  # ----- query / read -----
  misp.py search-events     [--value V] [--type T] [--tag T] [--from D] [--to D]
                            [--published true|false] [--limit N] [--page P]
                            [--returnFormat json|stix2|csv|...]
  misp.py search-attributes [--value V] [--type T] [--category C] [--tag T]
                            [--from D] [--to D] [--limit N] [--page P]
                            [--returnFormat json|stix2|csv|...]
  misp.py search-objects    [--event-id E] [--name N] [--limit N] [--page P]
  misp.py get-event         <event_id> [--include-attachments]
  misp.py list-tags         [--search T]

  # ----- write / push -----
  misp.py add-attribute     <event_id> --type T --value V [--category C]
                            [--comment X] [--to-ids true|false]
                            [--distribution 0..5] [--tags TAG1,TAG2]
  misp.py create-event      --info "Event title" [--distribution 0..5]
                            [--threat-level 1..4] [--analysis 0..2]
                            [--tags TAG1,TAG2] [--published true|false]
  misp.py upload-stix       <bundle.json> [--publish] [--galaxies-as-tags]
                            [--force-contextual-data]
  misp.py tag-event         <event_id> <tag> [--local]
  misp.py publish-event     <event_id>
  misp.py delete-event      <event_id>

  All commands accept --dry-run to preview the HTTP request without sending.
  All commands accept --insecure to skip TLS verification (self-signed certs
  are common on internal MISP deployments).

Distribution levels (MISP):
  0 = Your organisation only
  1 = This community only
  2 = Connected communities
  3 = All communities
  4 = Sharing group (requires --sharing-group)
  5 = Inherit event

Threat level: 1=High, 2=Medium, 3=Low, 4=Undefined
Analysis:     0=Initial, 1=Ongoing, 2=Completed

Exit codes:
  0  success
  1  network / API error (incl. 4xx/5xx)
  2  missing $MISP_URL or $MISP_API_KEY (only when not --dry-run)
  3  bad arguments / file not found
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

API_KEY = os.environ.get("MISP_API_KEY") or os.environ.get("MISP_KEY") or ""
BASE_URL = os.environ.get("MISP_URL", "").rstrip("/")
PROXY = os.environ.get("MISP_PROXY") or os.environ.get("HTTPS_PROXY") or ""


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def _bool(s):
    if isinstance(s, bool):
        return s
    if s is None:
        return None
    return str(s).strip().lower() in ("1", "true", "yes", "y", "on")


def _request(method, path, body=None, params=None, dry_run=False, insecure=False, raw_body=False):
    """Make a MISP API request. Body is JSON-serialised unless raw_body=True."""
    qs = ("?" + urllib.parse.urlencode(params)) if params else ""
    url = f"{BASE_URL}{path}{qs}"

    if dry_run:
        return {
            "dry_run": True,
            "method": method,
            "url": url or f"<MISP_URL>{path}{qs}",
            "headers": {
                "Authorization": "<redacted>" if API_KEY else "<unset>",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            "body": body,
            "tls_verify": not insecure,
        }

    if not BASE_URL:
        die("MISP_URL not set. Add it to .claude/settings.local.json env or export it.", 2)
    if not API_KEY:
        die("MISP_API_KEY (or MISP_KEY) not set. Add it to .claude/settings.local.json env or export it.", 2)

    data = None
    headers = {
        "Authorization": API_KEY,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if body is not None:
        if raw_body:
            data = body if isinstance(body, (bytes, bytearray)) else body.encode("utf-8")
        else:
            data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    ctx = None
    if insecure:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    try:
        if PROXY:
            handlers = [urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})]
            if ctx is not None:
                handlers.append(urllib.request.HTTPSHandler(context=ctx))
            response_cm = urllib.request.build_opener(*handlers).open(req, timeout=60)
        else:
            response_cm = urllib.request.urlopen(req, timeout=60, context=ctx)
        with response_cm as r:
            txt = r.read().decode("utf-8", errors="replace")
            if not txt:
                return {}
            try:
                return json.loads(txt)
            except json.JSONDecodeError:
                return {"raw": txt}
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode("utf-8", errors="replace") if e.fp else ""
        die(f"HTTP {e.code} {e.reason}: {body_txt[:500]}", 1)
    except urllib.error.URLError as e:
        die(f"network error: {e.reason}", 1)


# ---------- distillers ----------

def _distil_event(ev):
    """Pull a small summary out of an Event envelope."""
    if not ev:
        return None
    e = ev.get("Event", ev) if isinstance(ev, dict) else ev
    if not isinstance(e, dict):
        return ev
    attrs = e.get("Attribute") or []
    objs = e.get("Object") or []
    tags = e.get("Tag") or []
    return {
        "id": e.get("id"),
        "uuid": e.get("uuid"),
        "info": e.get("info"),
        "date": e.get("date"),
        "published": e.get("published"),
        "threat_level_id": e.get("threat_level_id"),
        "analysis": e.get("analysis"),
        "distribution": e.get("distribution"),
        "org": (e.get("Org") or {}).get("name"),
        "orgc": (e.get("Orgc") or {}).get("name"),
        "attribute_count": len(attrs) if attrs else e.get("attribute_count"),
        "object_count": len(objs) if objs else None,
        "tags": [t.get("name") for t in tags if isinstance(t, dict)],
    }


def _distil_attribute(at):
    if not at:
        return None
    a = at.get("Attribute", at) if isinstance(at, dict) else at
    if not isinstance(a, dict):
        return at
    tags = a.get("Tag") or []
    return {
        "id": a.get("id"),
        "uuid": a.get("uuid"),
        "event_id": a.get("event_id"),
        "type": a.get("type"),
        "category": a.get("category"),
        "value": a.get("value"),
        "to_ids": a.get("to_ids"),
        "comment": a.get("comment"),
        "timestamp": a.get("timestamp"),
        "tags": [t.get("name") for t in tags if isinstance(t, dict)],
    }


# ---------- read commands ----------

def _build_search_filters(args, defaults=None):
    """Translate CLI flags into a MISP restSearch JSON body."""
    f = dict(defaults or {})
    if getattr(args, "value", None):
        f["value"] = args.value
    if getattr(args, "type", None):
        f["type"] = args.type
    if getattr(args, "category", None):
        f["category"] = args.category
    if getattr(args, "tag", None):
        f["tags"] = args.tag
    if getattr(args, "from_", None):
        f["from"] = args.from_
    if getattr(args, "to", None):
        f["to"] = args.to
    if getattr(args, "published", None) is not None:
        f["published"] = _bool(args.published)
    if getattr(args, "event_id", None):
        f["eventid"] = args.event_id
    if getattr(args, "name", None):
        f["object_name"] = args.name
    f["limit"] = args.limit
    f["page"] = args.page
    f["returnFormat"] = getattr(args, "returnFormat", None) or "json"
    return f


def cmd_search_events(args):
    body = _build_search_filters(args)
    resp = _request("POST", "/events/restSearch", body=body, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return
    # When returnFormat is non-json, MISP returns raw text/binary — pass through.
    if body["returnFormat"] != "json":
        print(json.dumps({
            "source": "misp",
            "operation": "search-events",
            "returnFormat": body["returnFormat"],
            "query_time": now_iso(),
            "raw": resp.get("raw") if isinstance(resp, dict) and "raw" in resp else resp,
        }, indent=2))
        return
    items = (resp.get("response") or []) if isinstance(resp, dict) else []
    out = {
        "source": "misp",
        "operation": "search-events",
        "query_time": now_iso(),
        "filters": {k: v for k, v in body.items() if v not in (None, "", "json")},
        "count": len(items),
        "events": [_distil_event(it) for it in items],
    }
    print(json.dumps(out, indent=2))


def cmd_search_attributes(args):
    body = _build_search_filters(args)
    resp = _request("POST", "/attributes/restSearch", body=body, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return
    if body["returnFormat"] != "json":
        print(json.dumps({
            "source": "misp",
            "operation": "search-attributes",
            "returnFormat": body["returnFormat"],
            "query_time": now_iso(),
            "raw": resp.get("raw") if isinstance(resp, dict) and "raw" in resp else resp,
        }, indent=2))
        return
    container = (resp.get("response") or {}) if isinstance(resp, dict) else {}
    items = container.get("Attribute") or []
    out = {
        "source": "misp",
        "operation": "search-attributes",
        "query_time": now_iso(),
        "filters": {k: v for k, v in body.items() if v not in (None, "", "json")},
        "count": len(items),
        "attributes": [_distil_attribute(it) for it in items],
    }
    print(json.dumps(out, indent=2))


def cmd_search_objects(args):
    body = _build_search_filters(args)
    resp = _request("POST", "/objects/restsearch", body=body, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return
    container = (resp.get("response") or {}) if isinstance(resp, dict) else {}
    items = container.get("Object") or []
    out = {
        "source": "misp",
        "operation": "search-objects",
        "query_time": now_iso(),
        "count": len(items),
        "objects": [
            {
                "id": (o.get("Object") or o).get("id"),
                "uuid": (o.get("Object") or o).get("uuid"),
                "name": (o.get("Object") or o).get("name"),
                "event_id": (o.get("Object") or o).get("event_id"),
                "attribute_count": len(((o.get("Object") or o).get("Attribute") or [])),
            }
            for o in items
        ],
    }
    print(json.dumps(out, indent=2))


def cmd_get_event(args):
    path = f"/events/view/{urllib.parse.quote(str(args.event_id), safe='')}"
    if args.include_attachments:
        path += "/includeAttachments:1"
    resp = _request("GET", path, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return
    out = {
        "source": "misp",
        "operation": "get-event",
        "query_time": now_iso(),
        "event": _distil_event(resp),
        "raw": resp,
    }
    print(json.dumps(out, indent=2))


def cmd_list_tags(args):
    path = f"/tags/search/{urllib.parse.quote(args.search, safe='')}" if args.search else "/tags"
    resp = _request("GET", path, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return
    if isinstance(resp, list):
        items = resp
    else:
        items = resp.get("Tag") or resp.get("tags") or []
    out = {
        "source": "misp",
        "operation": "list-tags",
        "query_time": now_iso(),
        "count": len(items),
        "tags": [
            {
                "id": (t.get("Tag") or t).get("id"),
                "name": (t.get("Tag") or t).get("name"),
                "colour": (t.get("Tag") or t).get("colour"),
            }
            for t in items if isinstance(t, dict)
        ],
    }
    print(json.dumps(out, indent=2))


# ---------- write commands ----------

def cmd_add_attribute(args):
    body = {
        "type": args.type,
        "value": args.value,
    }
    if args.category:
        body["category"] = args.category
    if args.comment:
        body["comment"] = args.comment
    if args.to_ids is not None:
        body["to_ids"] = _bool(args.to_ids)
    if args.distribution is not None:
        body["distribution"] = args.distribution
    if args.tags:
        body["Tag"] = [{"name": t.strip()} for t in args.tags.split(",") if t.strip()]

    path = f"/attributes/add/{urllib.parse.quote(str(args.event_id), safe='')}"
    resp = _request("POST", path, body=body, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return
    out = {
        "source": "misp",
        "operation": "add-attribute",
        "query_time": now_iso(),
        "event_id": args.event_id,
        "attribute": _distil_attribute(resp),
        "raw": resp,
    }
    print(json.dumps(out, indent=2))


def cmd_create_event(args):
    body = {"Event": {"info": args.info}}
    e = body["Event"]
    if args.distribution is not None:
        e["distribution"] = args.distribution
    if args.threat_level is not None:
        e["threat_level_id"] = args.threat_level
    if args.analysis is not None:
        e["analysis"] = args.analysis
    if args.published is not None:
        e["published"] = _bool(args.published)
    if args.tags:
        e["Tag"] = [{"name": t.strip()} for t in args.tags.split(",") if t.strip()]

    resp = _request("POST", "/events/add", body=body, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return
    out = {
        "source": "misp",
        "operation": "create-event",
        "query_time": now_iso(),
        "event": _distil_event(resp),
        "raw": resp,
    }
    print(json.dumps(out, indent=2))


def cmd_upload_stix(args):
    if not os.path.isfile(args.bundle):
        die(f"file not found: {args.bundle}", 3)
    try:
        with open(args.bundle, "rb") as f:
            payload = f.read()
        # Validate JSON before sending so the user gets a clearer error
        json.loads(payload.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        die(f"unable to read STIX bundle: {e}", 3)

    # MISP routes named arguments via path segments: /events/upload_stix/2/<flag>:<value>
    path = "/events/upload_stix/2"
    if args.publish:
        path += "/publish:1"
    if args.galaxies_as_tags:
        path += "/galaxies_as_tags:1"
    if args.force_contextual_data:
        path += "/force_contextual_data:1"

    if args.dry_run:
        print(json.dumps({
            "dry_run": True,
            "method": "POST",
            "url": f"{BASE_URL or '<MISP_URL>'}{path}",
            "headers": {"Authorization": "<redacted>" if API_KEY else "<unset>",
                        "Accept": "application/json",
                        "Content-Type": "application/json"},
            "bundle_file": args.bundle,
            "bundle_bytes": len(payload),
            "tls_verify": not args.insecure,
        }, indent=2))
        return

    resp = _request("POST", path, body=payload, raw_body=True, insecure=args.insecure)
    out = {
        "source": "misp",
        "operation": "upload-stix",
        "query_time": now_iso(),
        "bundle_file": args.bundle,
        "bundle_bytes": len(payload),
        "result": resp,
    }
    print(json.dumps(out, indent=2))


def cmd_tag_event(args):
    # MISP needs the tag id, but accepts a tag name via /tags/search first.
    tag_id = args.tag
    if not str(tag_id).isdigit():
        # resolve name -> id
        if args.dry_run:
            tag_id = "<resolved-from-name>"
        else:
            search = _request("GET", f"/tags/search/{urllib.parse.quote(args.tag, safe='')}", insecure=args.insecure)
            items = search if isinstance(search, list) else (search.get("Tag") or [])
            match = None
            for t in items:
                tt = t.get("Tag") if isinstance(t, dict) and "Tag" in t else t
                if isinstance(tt, dict) and tt.get("name") == args.tag:
                    match = tt
                    break
            if not match and items:
                match = items[0].get("Tag") if "Tag" in items[0] else items[0]
            if not match:
                die(f"tag not found: {args.tag}", 1)
            tag_id = match.get("id")

    local = "1" if args.local else "0"
    path = f"/events/addTag/{urllib.parse.quote(str(args.event_id), safe='')}/{urllib.parse.quote(str(tag_id), safe='')}/local:{local}"
    resp = _request("POST", path, body={}, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return
    print(json.dumps({
        "source": "misp",
        "operation": "tag-event",
        "query_time": now_iso(),
        "event_id": args.event_id,
        "tag": args.tag,
        "tag_id": tag_id,
        "local": args.local,
        "result": resp,
    }, indent=2))


def cmd_publish_event(args):
    path = f"/events/publish/{urllib.parse.quote(str(args.event_id), safe='')}"
    resp = _request("POST", path, body={}, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return
    print(json.dumps({
        "source": "misp",
        "operation": "publish-event",
        "query_time": now_iso(),
        "event_id": args.event_id,
        "result": resp,
    }, indent=2))


def cmd_delete_event(args):
    path = f"/events/delete/{urllib.parse.quote(str(args.event_id), safe='')}"
    resp = _request("DELETE", path, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(resp, indent=2))
        return
    print(json.dumps({
        "source": "misp",
        "operation": "delete-event",
        "query_time": now_iso(),
        "event_id": args.event_id,
        "result": resp,
    }, indent=2))


# ---------- arg parsing ----------

def main():
    ap = argparse.ArgumentParser(
        prog="misp.py",
        description="MISP REST API CLI (stdlib only). Query and write to a MISP instance.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    def _common(p):
        p.add_argument("--dry-run", action="store_true")
        p.add_argument("--insecure", action="store_true",
                       help="skip TLS verification (self-signed MISP certs)")

    def _search_common(p, default_limit=50):
        p.add_argument("--value", help="indicator value substring")
        p.add_argument("--type", help="MISP attribute type (e.g., ip-dst, domain, sha256)")
        p.add_argument("--tag", action="append", help="tag filter (repeat for multiple)")
        p.add_argument("--from", dest="from_", help="from date (YYYY-MM-DD)")
        p.add_argument("--to", help="to date (YYYY-MM-DD)")
        p.add_argument("--published", help="true|false")
        p.add_argument("--limit", type=int, default=default_limit)
        p.add_argument("--page", type=int, default=1)
        p.add_argument("--returnFormat", default="json",
                       help="json|stix2|csv|xml|... (default json)")
        _common(p)

    p = sub.add_parser("search-events", help="POST /events/restSearch")
    _search_common(p)
    p.set_defaults(func=cmd_search_events)

    p = sub.add_parser("search-attributes", help="POST /attributes/restSearch")
    _search_common(p)
    p.add_argument("--category", help="MISP category (e.g., 'Network activity')")
    p.set_defaults(func=cmd_search_attributes)

    p = sub.add_parser("search-objects", help="POST /objects/restsearch")
    p.add_argument("--event-id", dest="event_id")
    p.add_argument("--name", help="object template name")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--returnFormat", default="json")
    _common(p)
    p.set_defaults(func=cmd_search_objects)

    p = sub.add_parser("get-event", help="GET /events/view/{id}")
    p.add_argument("event_id")
    p.add_argument("--include-attachments", action="store_true")
    _common(p)
    p.set_defaults(func=cmd_get_event)

    p = sub.add_parser("list-tags", help="GET /tags or /tags/search/{term}")
    p.add_argument("--search", help="filter tag name")
    _common(p)
    p.set_defaults(func=cmd_list_tags)

    p = sub.add_parser("add-attribute", help="POST /attributes/add/{event_id}")
    p.add_argument("event_id")
    p.add_argument("--type", required=True, help="MISP attribute type (ip-dst, domain, sha256, ...)")
    p.add_argument("--value", required=True)
    p.add_argument("--category", help="MISP category")
    p.add_argument("--comment")
    p.add_argument("--to-ids", dest="to_ids", help="true|false — flag for IDS export")
    p.add_argument("--distribution", type=int, choices=[0, 1, 2, 3, 4, 5])
    p.add_argument("--tags", help="comma-separated tag names")
    _common(p)
    p.set_defaults(func=cmd_add_attribute)

    p = sub.add_parser("create-event", help="POST /events/add")
    p.add_argument("--info", required=True, help="event title / one-line description")
    p.add_argument("--distribution", type=int, choices=[0, 1, 2, 3, 4])
    p.add_argument("--threat-level", dest="threat_level", type=int, choices=[1, 2, 3, 4],
                   help="1=High, 2=Medium, 3=Low, 4=Undefined")
    p.add_argument("--analysis", type=int, choices=[0, 1, 2],
                   help="0=Initial, 1=Ongoing, 2=Completed")
    p.add_argument("--published", help="true|false")
    p.add_argument("--tags", help="comma-separated tag names")
    _common(p)
    p.set_defaults(func=cmd_create_event)

    p = sub.add_parser("upload-stix", help="POST /events/upload_stix/2 — create event(s) from a STIX 2 bundle")
    p.add_argument("bundle", help="path to a STIX 2.x JSON bundle file")
    p.add_argument("--publish", action="store_true", help="publish the resulting event(s)")
    p.add_argument("--galaxies-as-tags", dest="galaxies_as_tags", action="store_true",
                   help="map STIX objects to MISP galaxies as tags")
    p.add_argument("--force-contextual-data", dest="force_contextual_data", action="store_true",
                   help="keep STIX context objects (identity, marking-definition, ...)")
    _common(p)
    p.set_defaults(func=cmd_upload_stix)

    p = sub.add_parser("tag-event", help="POST /events/addTag/{event_id}/{tag_id}/local:{0|1}")
    p.add_argument("event_id")
    p.add_argument("tag", help="tag name (resolved to id) or numeric id")
    p.add_argument("--local", action="store_true", help="apply as local tag")
    _common(p)
    p.set_defaults(func=cmd_tag_event)

    p = sub.add_parser("publish-event", help="POST /events/publish/{event_id}")
    p.add_argument("event_id")
    _common(p)
    p.set_defaults(func=cmd_publish_event)

    p = sub.add_parser("delete-event", help="DELETE /events/delete/{event_id}")
    p.add_argument("event_id")
    _common(p)
    p.set_defaults(func=cmd_delete_event)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
