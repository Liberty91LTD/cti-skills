#!/usr/bin/env python3
"""
opencti.py — OpenCTI GraphQL API CLI (stdlib only, no install).

Two-way: query what's in an OpenCTI instance AND push new intel to it.
The write surface includes creating indicators/observables, labelling,
TLP markings, field updates, relationships, STIX 2.1 bundle import, and
(guarded) deletion.

Auth: header `Authorization: Bearer <OPENCTI_TOKEN>`.
Base URL is taken from $OPENCTI_URL (e.g., http://localhost:8080 — no
trailing slash). Single endpoint: POST {OPENCTI_URL}/graphql.

Targets OpenCTI >= 6.x (FilterGroup filter format). GraphQL errors come
back as HTTP 200 with an `errors` array — the CLI surfaces the first
error message and exits 1.

Usage:
  # ----- query / read -----
  opencti.py version
  opencti.py search <term> [--limit N]
  opencti.py lookup <value> [--limit N]          # observables AND indicators
  opencti.py list <type> [--label L] [--created-after D] [--created-before D]
                         [--score-gte N] [--order-by F] [--order asc|desc]
                         [--limit N] [--after CURSOR]
      types: indicators, observables, reports, incidents, campaigns,
             intrusion-sets, malware, attack-patterns, vulnerabilities, sightings
  opencti.py get <id> [--no-relationships]
  opencti.py connectors

  # ----- write / push -----
  opencti.py create-indicator --value V --type ip|domain|url|hash|email
                              [--name N] [--pattern P] [--score 0-100]
                              [--description D] [--labels L1,L2]
                              [--no-observable]
  opencti.py create-observable --value V --type ip|domain|url|hash|email
                              [--score 0-100] [--labels L1,L2]
  opencti.py add-label <id> <label> [<label> ...]
  opencti.py add-marking <id> <TLP:CLEAR|TLP:GREEN|TLP:AMBER|TLP:AMBER+STRICT|TLP:RED>
  opencti.py update <id> --field name|description|score|confidence --value V
  opencti.py create-relationship --from ID --to ID --type REL_TYPE
                              [--description D]
  opencti.py upload-stix <bundle.json> [--no-bypass] [--wait N]

  # ----- delete (destructive — confirm with the user first) -----
  opencti.py delete <id>

  All commands accept --dry-run to preview the GraphQL request without sending.
  All commands accept --insecure to skip TLS verification (self-signed certs
  on internal deployments).

Exit codes:
  0  success
  1  network / API / GraphQL error
  2  missing $OPENCTI_URL or $OPENCTI_TOKEN (only when not --dry-run)
  3  bad arguments / file not found
"""

import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone

TOKEN = os.environ.get("OPENCTI_TOKEN") or ""
BASE_URL = os.environ.get("OPENCTI_URL", "").rstrip("/")
PROXY = os.environ.get("OPENCTI_PROXY") or os.environ.get("HTTPS_PROXY") or ""

IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def _http(body_bytes, content_type, dry_run=False, insecure=False, dry_preview=None):
    """POST to /graphql. body_bytes is the encoded payload."""
    url = f"{BASE_URL}/graphql"

    if dry_run:
        return {
            "dry_run": True,
            "method": "POST",
            "url": url or "<OPENCTI_URL>/graphql",
            "headers": {
                "Authorization": "Bearer <redacted>" if TOKEN else "<unset>",
                "Content-Type": content_type,
            },
            "body": dry_preview,
            "tls_verify": not insecure,
        }

    if not BASE_URL:
        die("OPENCTI_URL not set. Add it to .claude/settings.local.json env or export it.", 2)
    if not TOKEN:
        die("OPENCTI_TOKEN not set. Add it to .claude/settings.local.json env or export it.", 2)

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json",
        "Content-Type": content_type,
    }
    req = urllib.request.Request(url, data=body_bytes, headers=headers, method="POST")
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
            response_cm = urllib.request.build_opener(*handlers).open(req, timeout=120)
        else:
            response_cm = urllib.request.urlopen(req, timeout=120, context=ctx)
        with response_cm as r:
            txt = r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode("utf-8", errors="replace") if e.fp else ""
        # Auth failures may surface as HTTP-level errors too
        die(f"HTTP {e.code} {e.reason}: {body_txt[:500]}", 1)
    except urllib.error.URLError as e:
        die(f"network error: {e.reason} — check OPENCTI_URL ({BASE_URL or 'unset'})", 1)

    try:
        resp = json.loads(txt)
    except json.JSONDecodeError:
        die(f"non-JSON response from server: {txt[:300]}", 1)
    return resp


def gql(query, variables=None, dry_run=False, insecure=False, tolerate_errors=False):
    """Run a GraphQL operation. Returns the `data` object.

    OpenCTI returns GraphQL errors as HTTP 200 with an `errors` array —
    always check it. AUTH_REQUIRED means a bad/missing token.
    """
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    body = json.dumps(payload).encode("utf-8")
    resp = _http(body, "application/json", dry_run=dry_run, insecure=insecure,
                 dry_preview=payload)
    if dry_run:
        return resp
    if isinstance(resp, dict) and resp.get("errors"):
        if tolerate_errors and resp.get("data"):
            return resp["data"]
        err = resp["errors"][0]
        name = err.get("name") or err.get("extensions", {}).get("code") or ""
        msg = err.get("message") or json.dumps(err)[:300]
        if "AUTH_REQUIRED" in (name, msg):
            die("authentication failed (AUTH_REQUIRED) — check OPENCTI_TOKEN", 1)
        die(f"GraphQL error{f' [{name}]' if name else ''}: {msg}", 1)
    return resp.get("data") or {}


def _edges(conn):
    return [e["node"] for e in (conn or {}).get("edges") or [] if e and e.get("node")]


def emit(operation, payload):
    out = {"source": "opencti", "operation": operation, "query_time": now_iso()}
    out.update(payload)
    print(json.dumps(out, indent=2))


# ---------- indicator/observable type helpers ----------

HASH_RE = {
    "MD5": re.compile(r"^[a-fA-F0-9]{32}$"),
    "SHA-1": re.compile(r"^[a-fA-F0-9]{40}$"),
    "SHA-256": re.compile(r"^[a-fA-F0-9]{64}$"),
}
IPV4_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")


def stix_pattern_for(ioc_type, value):
    """Return (pattern, main_observable_type) for a raw IOC value."""
    if ioc_type == "ip":
        if IPV4_RE.match(value):
            return f"[ipv4-addr:value = '{value}']", "IPv4-Addr"
        return f"[ipv6-addr:value = '{value}']", "IPv6-Addr"
    if ioc_type == "domain":
        return f"[domain-name:value = '{value}']", "Domain-Name"
    if ioc_type == "url":
        return f"[url:value = '{value}']", "Url"
    if ioc_type == "email":
        return f"[email-addr:value = '{value}']", "Email-Addr"
    if ioc_type == "hash":
        for alg, rx in HASH_RE.items():
            if rx.match(value):
                return f"[file:hashes.'{alg}' = '{value}']", "StixFile"
        die(f"unrecognised hash length: {value}", 3)
    die(f"unknown IOC type: {ioc_type}", 3)


# ---------- read commands ----------

SEARCH_FRAGMENTS = """
      id
      entity_type
      ... on StixDomainObject { created modified objectLabel { value } }
      ... on IntrusionSet { name description }
      ... on ThreatActor { name }
      ... on Malware { name }
      ... on Campaign { name }
      ... on Incident { name }
      ... on Report { name published }
      ... on Indicator { name pattern x_opencti_score }
      ... on AttackPattern { name x_mitre_id }
      ... on Vulnerability { name }
      ... on Tool { name }
      ... on StixCyberObservable { observable_value }
"""


def cmd_version(args):
    q = "{ about { version } }"
    data = gql(q, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(data, indent=2))
        return
    emit("version", {"version": (data.get("about") or {}).get("version")})


def cmd_search(args):
    q = f"""query Search($search: String, $first: Int) {{
  stixCoreObjects(search: $search, first: $first) {{
    pageInfo {{ globalCount }}
    edges {{ node {{{SEARCH_FRAGMENTS}}} }}
  }}
}}"""
    data = gql(q, {"search": args.term, "first": args.limit},
               dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(data, indent=2))
        return
    conn = data.get("stixCoreObjects") or {}
    nodes = _edges(conn)
    emit("search", {
        "term": args.term,
        "total_matches": (conn.get("pageInfo") or {}).get("globalCount"),
        "count": len(nodes),
        "results": nodes,
    })


def cmd_lookup(args):
    q = """query Lookup($v: String, $first: Int) {
  stixCyberObservables(search: $v, first: $first) {
    pageInfo { globalCount }
    edges { node { id entity_type observable_value created_at
                   objectLabel { value } objectMarking { definition } } }
  }
  indicators(search: $v, first: $first) {
    pageInfo { globalCount }
    edges { node { id name pattern pattern_type valid_from valid_until
                   x_opencti_score created
                   objectLabel { value } objectMarking { definition } } }
  }
}"""
    data = gql(q, {"v": args.value, "first": args.limit},
               dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(data, indent=2))
        return
    obs = _edges(data.get("stixCyberObservables"))
    ind = _edges(data.get("indicators"))
    known_as = []
    if obs:
        known_as.append("observable")
    if ind:
        known_as.append("indicator")
    emit("lookup", {
        "value": args.value,
        "known": bool(known_as),
        "known_as": known_as,
        "observables": obs,
        "indicators": ind,
    })


LIST_TYPES = {
    "indicators": {
        "field": "indicators",
        "node": "id name pattern created valid_from x_opencti_score objectLabel { value }",
        "default_order": "created",
    },
    "observables": {
        "field": "stixCyberObservables",
        "node": "id entity_type observable_value created_at objectLabel { value }",
        "default_order": "created_at",
    },
    "reports": {
        "field": "reports",
        "node": "id name published created report_types objectLabel { value }",
        "default_order": "published",
    },
    "incidents": {
        "field": "incidents",
        "node": "id name created first_seen last_seen objectLabel { value }",
        "default_order": "created",
    },
    "campaigns": {
        "field": "campaigns",
        "node": "id name created first_seen last_seen objectLabel { value }",
        "default_order": "created",
    },
    "intrusion-sets": {
        "field": "intrusionSets",
        "node": "id name created description objectLabel { value }",
        "default_order": "created",
    },
    "malware": {
        "field": "malwares",
        "node": "id name created malware_types objectLabel { value }",
        "default_order": "created",
    },
    "attack-patterns": {
        "field": "attackPatterns",
        "node": "id name x_mitre_id created objectLabel { value }",
        "default_order": "created",
    },
    "vulnerabilities": {
        "field": "vulnerabilities",
        "node": "id name created objectLabel { value }",
        "default_order": "created",
    },
    "sightings": {
        "field": "stixSightingRelationships",
        "node": "id created first_seen last_seen attribute_count confidence",
        "default_order": "created",
    },
}


def _build_filters(args):
    filters = []
    if getattr(args, "label", None):
        filters.append({"key": "objectLabel", "values": [args.label]})
    if getattr(args, "created_after", None):
        filters.append({"key": "created", "values": [args.created_after], "operator": "gt"})
    if getattr(args, "created_before", None):
        filters.append({"key": "created", "values": [args.created_before], "operator": "lt"})
    if getattr(args, "score_gte", None) is not None:
        filters.append({"key": "x_opencti_score", "values": [str(args.score_gte)], "operator": "gte"})
    if not filters:
        return None
    # FilterGroup format (OpenCTI >= 5.12): filterGroups is required even when empty
    return {"mode": "and", "filters": filters, "filterGroups": []}


def cmd_list(args):
    spec = LIST_TYPES.get(args.type)
    if not spec:
        die(f"unknown type '{args.type}'. One of: {', '.join(LIST_TYPES)}", 3)
    order_by = args.order_by or spec["default_order"]
    if not IDENT_RE.match(order_by):
        die(f"invalid --order-by field: {order_by}", 3)
    order_mode = "asc" if args.order == "asc" else "desc"
    field = spec["field"]
    q = f"""query List($first: Int, $after: ID, $filters: FilterGroup) {{
  {field}(first: $first, after: $after, filters: $filters,
          orderBy: {order_by}, orderMode: {order_mode}) {{
    pageInfo {{ globalCount endCursor hasNextPage }}
    edges {{ node {{ {spec['node']} }} }}
  }}
}}"""
    variables = {"first": args.limit, "after": args.after, "filters": _build_filters(args)}
    data = gql(q, variables, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(data, indent=2))
        return
    conn = data.get(field) or {}
    nodes = _edges(conn)
    pi = conn.get("pageInfo") or {}
    emit("list", {
        "type": args.type,
        "total_matches": pi.get("globalCount"),
        "count": len(nodes),
        "has_next_page": pi.get("hasNextPage"),
        "end_cursor": pi.get("endCursor") if pi.get("hasNextPage") else None,
        "results": nodes,
    })


def cmd_get(args):
    q = f"""query Get($id: String!) {{
  stixCoreObject(id: $id) {{
    id standard_id entity_type parent_types created_at updated_at
    objectLabel {{ value }}
    objectMarking {{ definition }}
    createdBy {{ name }}
    ... on StixDomainObject {{ created modified confidence }}
    ... on IntrusionSet {{ name description aliases }}
    ... on ThreatActor {{ name }}
    ... on Malware {{ name description malware_types }}
    ... on Campaign {{ name description first_seen last_seen }}
    ... on Incident {{ name description first_seen last_seen }}
    ... on Report {{ name description published report_types }}
    ... on Indicator {{ name description pattern pattern_type valid_from valid_until
                        x_opencti_score x_opencti_main_observable_type }}
    ... on AttackPattern {{ name description x_mitre_id }}
    ... on Vulnerability {{ name description }}
    ... on Identity {{ name description }}
    ... on Location {{ name description }}
    ... on Tool {{ name }}
    ... on StixCyberObservable {{ observable_value x_opencti_score }}
  }}
}}"""
    data = gql(q, {"id": args.id}, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(data, indent=2))
        return
    entity = data.get("stixCoreObject")
    if not entity:
        die(f"no entity found for id: {args.id}", 1)

    relationships = []
    rel_note = None
    if not args.no_relationships:
        # fromOrToId is [String] on 7.x (StixRef on some earlier schemas).
        # A relationship-query failure must not sink the entity we already have.
        rq = """query Rels($id: String, $first: Int) {
  stixCoreRelationships(fromOrToId: [$id], first: $first) {
    edges { node {
      id relationship_type created
      from { ... on StixCoreObject { id entity_type
               ... on StixDomainObject { objectLabel { value } } }
             ... on StixCyberObservable { observable_value } }
      to   { ... on StixCoreObject { id entity_type }
             ... on StixCyberObservable { observable_value } }
    } }
  }
}"""
        try:
            rdata = gql(rq, {"id": args.id, "first": 25}, insecure=args.insecure,
                        tolerate_errors=True)
            relationships = _edges((rdata or {}).get("stixCoreRelationships"))
        except SystemExit:
            rel_note = ("relationship query failed on this server's schema — "
                        "entity returned without relationships")
    payload = {"entity": entity, "relationships": relationships}
    if rel_note:
        payload["relationships_note"] = rel_note
    emit("get", payload)


def cmd_connectors(args):
    # Deliberately minimal field selection: selecting works { status } crashes
    # on some 7.x rows (non-nullable Work.status bug).
    q = "{ connectors { id name active connector_type auto } }"
    data = gql(q, dry_run=args.dry_run, insecure=args.insecure, tolerate_errors=True)
    if args.dry_run:
        print(json.dumps(data, indent=2))
        return
    conns = data.get("connectors") or []
    emit("connectors", {
        "count": len(conns),
        "active": sum(1 for c in conns if c.get("active")),
        "connectors": conns,
    })


# ---------- write commands ----------

def _split_labels(s):
    return [t.strip() for t in (s or "").split(",") if t.strip()]


def cmd_create_indicator(args):
    if args.pattern:
        pattern = args.pattern
        if not args.observable_type:
            die("--pattern requires --observable-type (e.g. IPv4-Addr, Domain-Name, Url, StixFile)", 3)
        main_type = args.observable_type
    else:
        if not (args.type and args.value):
            die("provide either --pattern + --observable-type, or --type + --value", 3)
        pattern, main_type = stix_pattern_for(args.type, args.value)

    name = args.name or (args.value or pattern)
    inp = {
        "name": name,
        "pattern": pattern,
        "pattern_type": "stix",
        "x_opencti_main_observable_type": main_type,
        # Without this the underlying observable is NOT created and raw
        # value-searches find nothing. Default on; disable via --no-observable.
        "createObservables": not args.no_observable,
    }
    if args.score is not None:
        inp["x_opencti_score"] = args.score
    if args.description:
        inp["description"] = args.description
    labels = _split_labels(args.labels)
    if labels and not args.dry_run:
        # objectLabel takes label ids on 7.x, not names — resolve (creating
        # missing labels) before the mutation.
        inp["objectLabel"] = _resolve_label_ids(labels, args.insecure)
    elif labels:
        inp["objectLabel"] = ["<resolved-label-ids>"]

    q = """mutation CreateIndicator($input: IndicatorAddInput!) {
  indicatorAdd(input: $input) {
    id standard_id name pattern x_opencti_score objectLabel { value }
  }
}"""
    data = gql(q, {"input": inp}, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(data, indent=2))
        return
    emit("create-indicator", {
        "indicator": data.get("indicatorAdd"),
        "observable_created": not args.no_observable,
    })


OBSERVABLE_INPUT_KEY = {
    "IPv4-Addr": "IPv4Addr",
    "IPv6-Addr": "IPv6Addr",
    "Domain-Name": "DomainName",
    "Url": "Url",
    "Email-Addr": "EmailAddr",
}


def cmd_create_observable(args):
    _, main_type = stix_pattern_for(args.type, args.value)
    q_common = "id standard_id entity_type observable_value objectLabel { value }"
    labels = _split_labels(args.labels)
    label_ids = None
    if labels:
        label_ids = (_resolve_label_ids(labels, args.insecure)
                     if not args.dry_run else ["<resolved-label-ids>"])
    variables = {"score": args.score, "labels": label_ids}
    if main_type == "StixFile":
        alg = next(a for a, rx in HASH_RE.items() if rx.match(args.value))
        q = f"""mutation CreateObservable($score: Int, $labels: [String], $hashes: [HashInput!]) {{
  stixCyberObservableAdd(type: "StixFile", x_opencti_score: $score, objectLabel: $labels,
                         StixFile: {{ hashes: $hashes }}) {{ {q_common} }}
}}"""
        variables["hashes"] = [{"algorithm": alg, "hash": args.value.lower()}]
    else:
        key = OBSERVABLE_INPUT_KEY[main_type]
        q = f"""mutation CreateObservable($value: String!, $score: Int, $labels: [String]) {{
  stixCyberObservableAdd(type: "{main_type}", x_opencti_score: $score, objectLabel: $labels,
                         {key}: {{ value: $value }}) {{ {q_common} }}
}}"""
        variables["value"] = args.value
    data = gql(q, variables, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(data, indent=2))
        return
    emit("create-observable", {"observable": data.get("stixCyberObservableAdd")})


def _resolve_label_ids(names, insecure):
    """Resolve label names to internal ids, creating missing labels."""
    ids = []
    for name in names:
        q = """query Labels($search: String) {
  labels(search: $search, first: 20) { edges { node { id value } } }
}"""
        data = gql(q, {"search": name}, insecure=insecure)
        match = next((n for n in _edges(data.get("labels"))
                      if n.get("value", "").lower() == name.lower()), None)
        if match:
            ids.append(match["id"])
            continue
        m = """mutation LabelAdd($input: LabelAddInput!) {
  labelAdd(input: $input) { id value }
}"""
        created = gql(m, {"input": {"value": name}}, insecure=insecure)
        ids.append(created["labelAdd"]["id"])
    return ids


def cmd_add_label(args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "add-label",
                          "id": args.id, "labels": args.labels,
                          "note": "resolves label names -> ids (creating missing labels), "
                                  "then stixCoreObjectEdit.relationAdd(object-label)"}, indent=2))
        return
    label_ids = _resolve_label_ids(args.labels, args.insecure)
    q = """mutation AddLabel($id: ID!, $toId: StixRef!) {
  stixCoreObjectEdit(id: $id) {
    relationAdd(input: { toId: $toId, relationship_type: "object-label" }) { id }
  }
}"""
    for lid in label_ids:
        gql(q, {"id": args.id, "toId": lid}, insecure=args.insecure)
    emit("add-label", {"id": args.id, "labels_applied": args.labels})


TLP_NAMES = ["TLP:CLEAR", "TLP:WHITE", "TLP:GREEN", "TLP:AMBER", "TLP:AMBER+STRICT", "TLP:RED"]


def cmd_add_marking(args):
    tlp = args.marking.upper()
    if tlp not in TLP_NAMES:
        die(f"unknown marking '{args.marking}'. One of: {', '.join(TLP_NAMES)}", 3)
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "add-marking",
                          "id": args.id, "marking": tlp,
                          "note": "resolves marking definition -> id, then "
                                  "stixCoreObjectEdit.relationAdd(object-marking)"}, indent=2))
        return
    q = """query Markings($search: String) {
  markingDefinitions(search: $search, first: 20) {
    edges { node { id definition definition_type } }
  }
}"""
    data = gql(q, {"search": tlp}, insecure=args.insecure)
    match = next((n for n in _edges(data.get("markingDefinitions"))
                  if n.get("definition", "").upper() == tlp), None)
    if not match:
        die(f"marking definition not found on server: {tlp}", 1)
    m = """mutation AddMarking($id: ID!, $toId: StixRef!) {
  stixCoreObjectEdit(id: $id) {
    relationAdd(input: { toId: $toId, relationship_type: "object-marking" }) { id }
  }
}"""
    gql(m, {"id": args.id, "toId": match["id"]}, insecure=args.insecure)
    emit("add-marking", {"id": args.id, "marking_applied": tlp})


UPDATE_FIELD_MAP = {
    "name": "name",
    "description": "description",
    "score": "x_opencti_score",
    "confidence": "confidence",
}


def _entity_kind(entity_id, insecure):
    """Return (entity_type, parent_types) for dispatching edit/delete mutations."""
    q = """query Kind($id: String!) {
  stixCoreObject(id: $id) { id entity_type parent_types }
}"""
    data = gql(q, {"id": entity_id}, insecure=insecure)
    obj = data.get("stixCoreObject")
    if not obj:
        die(f"no entity found for id: {entity_id}", 1)
    return obj.get("entity_type"), obj.get("parent_types") or []


def cmd_update(args):
    key = UPDATE_FIELD_MAP.get(args.field)
    if not key:
        die(f"unsupported --field '{args.field}'. One of: {', '.join(UPDATE_FIELD_MAP)}", 3)
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "update", "id": args.id,
                          "fieldPatch": {"key": key, "value": [args.value]},
                          "note": "dispatches to stixDomainObjectEdit or "
                                  "stixCyberObservableEdit based on entity kind"}, indent=2))
        return
    _, parents = _entity_kind(args.id, args.insecure)
    is_observable = "Stix-Cyber-Observable" in parents
    root = "stixCyberObservableEdit" if is_observable else "stixDomainObjectEdit"
    q = f"""mutation Update($id: ID!, $input: [EditInput]!) {{
  {root}(id: $id) {{
    fieldPatch(input: $input) {{ id }}
  }}
}}"""
    gql(q, {"id": args.id, "input": [{"key": key, "value": [args.value]}]},
        insecure=args.insecure)
    emit("update", {"id": args.id, "field": key, "new_value": args.value})


def cmd_create_relationship(args):
    inp = {
        "fromId": args.from_id,
        "toId": args.to_id,
        "relationship_type": args.type,
    }
    if args.description:
        inp["description"] = args.description
    q = """mutation CreateRel($input: StixCoreRelationshipAddInput!) {
  stixCoreRelationshipAdd(input: $input) { id relationship_type }
}"""
    data = gql(q, {"input": inp}, dry_run=args.dry_run, insecure=args.insecure)
    if args.dry_run:
        print(json.dumps(data, indent=2))
        return
    emit("create-relationship", {"relationship": data.get("stixCoreRelationshipAdd")})


def cmd_upload_stix(args):
    if not os.path.isfile(args.bundle):
        die(f"file not found: {args.bundle}", 3)
    try:
        with open(args.bundle, "rb") as f:
            payload = f.read()
        json.loads(payload.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        die(f"unable to read STIX bundle: {e}", 3)

    filename = os.path.basename(args.bundle)
    operations = json.dumps({
        "query": "mutation Upload($file: Upload!) { uploadImport(file: $file) { id name uploadStatus } }",
        "variables": {"file": None},
    })
    file_map = json.dumps({"0": ["variables.file"]})

    if args.dry_run:
        print(json.dumps({
            "dry_run": True,
            "method": "POST (multipart/form-data, GraphQL multipart request spec)",
            "url": f"{BASE_URL or '<OPENCTI_URL>'}/graphql",
            "headers": {"Authorization": "Bearer <redacted>" if TOKEN else "<unset>"},
            "operations": json.loads(operations),
            "map": json.loads(file_map),
            "bundle_file": args.bundle,
            "bundle_bytes": len(payload),
            "then": "mutation askJobImport(fileName, bypassValidation: %s)" % (not args.no_bypass),
            "tls_verify": not args.insecure,
        }, indent=2))
        return

    # Step 1 — multipart upload (stdlib: build the body by hand)
    boundary = f"----cti-skills-{uuid.uuid4().hex}"
    def part(name, value, filename=None, ctype=None):
        h = f'Content-Disposition: form-data; name="{name}"'
        if filename:
            h += f'; filename="{filename}"'
        h += "\r\n"
        if ctype:
            h += f"Content-Type: {ctype}\r\n"
        return f"--{boundary}\r\n{h}\r\n".encode() + (
            value if isinstance(value, bytes) else value.encode()) + b"\r\n"

    body = (part("operations", operations)
            + part("map", file_map)
            + part("0", payload, filename=filename, ctype="application/json")
            + f"--{boundary}--\r\n".encode())
    resp = _http(body, f"multipart/form-data; boundary={boundary}", insecure=args.insecure)
    if resp.get("errors"):
        die(f"upload failed: {resp['errors'][0].get('message')}", 1)
    up = (resp.get("data") or {}).get("uploadImport") or {}
    file_id = up.get("id")
    if not file_id:
        die(f"upload returned no file id: {json.dumps(resp)[:300]}", 1)

    # Step 2 — trigger the import. Without bypassValidation the bundle is
    # parked in the analyst workbench for human review and nothing imports.
    q = """mutation Ask($fileName: ID!, $bypass: Boolean) {
  askJobImport(fileName: $fileName, bypassValidation: $bypass) { id }
}"""
    imported = True
    note = "import job started (bypassValidation) — processing is asynchronous; poll with `lookup`/`search`, small bundles take seconds"
    try:
        gql(q, {"fileName": file_id, "bypass": not args.no_bypass}, insecure=args.insecure)
    except SystemExit:
        # Token lacks bypass capability (or --no-bypass rejected): the file is
        # uploaded but parked in the workbench.
        imported = False
        note = "upload succeeded but import was NOT triggered — the bundle is in the analyst workbench (Data > Import) awaiting human validation"
    if args.no_bypass and imported:
        note = "import job submitted for validation — depending on connector config it may land in the analyst workbench"

    emit("upload-stix", {
        "bundle_file": args.bundle,
        "bundle_bytes": len(payload),
        "upload_id": file_id,
        "upload_status": up.get("uploadStatus"),
        "import_triggered": imported,
        "note": note,
    })
    if args.wait and imported:
        time.sleep(args.wait)


def cmd_delete(args):
    # Destructive. The skill requires explicit user confirmation before this
    # is invoked. Deleting an indicator does NOT cascade to its observable.
    if args.dry_run:
        print(json.dumps({"dry_run": True, "operation": "delete", "id": args.id,
                          "note": "dispatches stixCyberObservableEdit.delete or "
                                  "stixDomainObjectEdit.delete based on entity kind"}, indent=2))
        return
    entity_type, parents = _entity_kind(args.id, args.insecure)
    if "Stix-Cyber-Observable" in parents:
        q = """mutation Delete($id: ID!) {
  stixCyberObservableEdit(id: $id) { delete }
}"""
    else:
        q = """mutation Delete($id: ID!) {
  stixDomainObjectEdit(id: $id) { delete }
}"""
    gql(q, {"id": args.id}, insecure=args.insecure)
    emit("delete", {
        "id": args.id,
        "entity_type": entity_type,
        "deleted": True,
        "note": "deleting an indicator does NOT cascade to its observable (and vice versa)",
    })


# ---------- arg parsing ----------

def main():
    ap = argparse.ArgumentParser(
        prog="opencti.py",
        description="OpenCTI GraphQL CLI (stdlib only). Query and write to an OpenCTI instance.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    def _common(p):
        p.add_argument("--dry-run", action="store_true")
        p.add_argument("--insecure", action="store_true",
                       help="skip TLS verification (self-signed certs)")

    p = sub.add_parser("version", help="connectivity + version check (about { version })")
    _common(p)
    p.set_defaults(func=cmd_version)

    p = sub.add_parser("search", help="global search across all entity types")
    p.add_argument("term")
    p.add_argument("--limit", type=int, default=10)
    _common(p)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("lookup", help="is this IOC known? checks observables AND indicators")
    p.add_argument("value")
    p.add_argument("--limit", type=int, default=5)
    _common(p)
    p.set_defaults(func=cmd_lookup)

    p = sub.add_parser("list", help="list/filter entities of one type")
    p.add_argument("type", help=", ".join(LIST_TYPES))
    p.add_argument("--label", help="filter by label name")
    p.add_argument("--created-after", dest="created_after", help="ISO 8601 UTC, e.g. 2026-06-01T00:00:00Z")
    p.add_argument("--created-before", dest="created_before", help="ISO 8601 UTC")
    p.add_argument("--score-gte", dest="score_gte", type=int, help="x_opencti_score >= N")
    p.add_argument("--order-by", dest="order_by", help="ordering field (default: created/published)")
    p.add_argument("--order", choices=["asc", "desc"], default="desc")
    p.add_argument("--limit", type=int, default=25, choices=range(1, 101), metavar="1-100")
    p.add_argument("--after", help="pagination cursor (end_cursor from previous page)")
    _common(p)
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("get", help="full details + relationships for one entity")
    p.add_argument("id")
    p.add_argument("--no-relationships", action="store_true")
    _common(p)
    p.set_defaults(func=cmd_get)

    p = sub.add_parser("connectors", help="list connector status")
    _common(p)
    p.set_defaults(func=cmd_connectors)

    p = sub.add_parser("create-indicator", help="create an indicator (+ its observable by default)")
    p.add_argument("--value", help="raw IOC value (with --type)")
    p.add_argument("--type", choices=["ip", "domain", "url", "hash", "email"])
    p.add_argument("--pattern", help="explicit STIX pattern (alternative to --type/--value)")
    p.add_argument("--observable-type", dest="observable_type",
                   help="x_opencti_main_observable_type when using --pattern")
    p.add_argument("--name", help="indicator name (default: the value)")
    p.add_argument("--score", type=int, help="x_opencti_score 0-100")
    p.add_argument("--description")
    p.add_argument("--labels", help="comma-separated label names (auto-created if missing)")
    p.add_argument("--no-observable", action="store_true",
                   help="do NOT create the underlying observable (value-searches won't find the raw IOC)")
    _common(p)
    p.set_defaults(func=cmd_create_indicator)

    p = sub.add_parser("create-observable", help="create a bare observable (no indicator)")
    p.add_argument("--value", required=True)
    p.add_argument("--type", required=True, choices=["ip", "domain", "url", "hash", "email"])
    p.add_argument("--score", type=int)
    p.add_argument("--labels", help="comma-separated label names")
    _common(p)
    p.set_defaults(func=cmd_create_observable)

    p = sub.add_parser("add-label", help="attach label(s) to an entity (labels auto-created)")
    p.add_argument("id")
    p.add_argument("labels", nargs="+")
    _common(p)
    p.set_defaults(func=cmd_add_label)

    p = sub.add_parser("add-marking", help="attach a TLP marking to an entity")
    p.add_argument("id")
    p.add_argument("marking", help="TLP:CLEAR | TLP:GREEN | TLP:AMBER | TLP:AMBER+STRICT | TLP:RED")
    _common(p)
    p.set_defaults(func=cmd_add_marking)

    p = sub.add_parser("update", help="update a field on an entity (fieldPatch)")
    p.add_argument("id")
    p.add_argument("--field", required=True, help="name | description | score | confidence")
    p.add_argument("--value", required=True)
    _common(p)
    p.set_defaults(func=cmd_update)

    p = sub.add_parser("create-relationship", help="relate two entities (uses, indicates, targets, ...)")
    p.add_argument("--from", dest="from_id", required=True, help="source entity id")
    p.add_argument("--to", dest="to_id", required=True, help="target entity id")
    p.add_argument("--type", required=True, help="STIX relationship type (e.g. indicates, uses, targets)")
    p.add_argument("--description")
    _common(p)
    p.set_defaults(func=cmd_create_relationship)

    p = sub.add_parser("upload-stix", help="import a STIX 2.1 bundle (upload + trigger import)")
    p.add_argument("bundle", help="path to a STIX 2.1 JSON bundle file")
    p.add_argument("--no-bypass", action="store_true",
                   help="don't bypass validation — bundle goes to the analyst workbench for review")
    p.add_argument("--wait", type=int, default=0,
                   help="seconds to wait after triggering import (processing is async)")
    _common(p)
    p.set_defaults(func=cmd_upload_stix)

    p = sub.add_parser("delete", help="delete an entity — DESTRUCTIVE, confirm with the user first")
    p.add_argument("id")
    _common(p)
    p.set_defaults(func=cmd_delete)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
