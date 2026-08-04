#!/usr/bin/env python3
"""
sentinel.py — Microsoft Sentinel / Azure Log Analytics query CLI (stdlib only, no install).

Read-only: runs KQL against a Sentinel (Log Analytics) workspace and reports
which tables the workspace actually has. It never writes to the workspace.

The core purpose is **workspace-adaptive hunting**: not every Sentinel
environment ingests the same tables (they depend on connectors and agents),
so discover first (`tables`, `ingestion`, `probe`) and only then generate
KQL for tables that verifiably exist. See skills/lookup-sentinel/SKILL.md.

Auth: OAuth2 client-credentials (Entra ID app registration).
  POST {SENTINEL_LOGIN_BASE}/{tenant}/oauth2/v2.0/token
  scope = {SENTINEL_API_BASE}/.default
The app registration needs the Log Analytics Reader (or Microsoft Sentinel
Reader) role on the workspace. Setup walkthrough: tools/integrations/sentinel.md

Env vars:
  SENTINEL_TENANT_ID      Entra ID directory (tenant) GUID   [falls back to AZURE_TENANT_ID]
  SENTINEL_CLIENT_ID      app registration client GUID       [falls back to AZURE_CLIENT_ID]
  SENTINEL_CLIENT_SECRET  app registration client secret     [falls back to AZURE_CLIENT_SECRET]
  SENTINEL_WORKSPACE_ID   Log Analytics workspace GUID (workspace Overview blade)
  SENTINEL_API_BASE       optional — default https://api.loganalytics.io (sovereign clouds differ)
  SENTINEL_LOGIN_BASE     optional — default https://login.microsoftonline.com
  SENTINEL_PROXY          optional HTTP(S) proxy (falls back to HTTPS_PROXY)

Usage:
  sentinel.py check                             # auth + workspace reachability
  sentinel.py tables      [--filter STR]        # all tables the workspace schema knows (metadata endpoint)
  sentinel.py ingestion   [--days 30]           # tables that actually received data recently (Usage-based)
  sentinel.py probe T1,T2,...  [--days 7]       # per-table existence + row count over the window
  sentinel.py schema <Table>                    # column names + types for one table
  sentinel.py query '<kql>' [--timespan P7D] [--max-rows 100]
  sentinel.py query --file hunt.kql [--timespan P30D]

  All commands accept --dry-run to preview the HTTP request(s) without sending.

Notes:
  - `query` always sends a server-side timespan (default P7D, ISO 8601 duration);
    the effective window is the intersection of the timespan and any `ago()`
    filters inside the query itself. There is no unbounded query path.
  - Row output is truncated at --max-rows (default 100); the JSON reports
    `truncated: true` plus the total row count so a cap never reads as a full result.

Exit codes:
  0  success
  1  network / API error (incl. 4xx/5xx)
  2  missing credentials or workspace id (only when not --dry-run)
  3  bad arguments / file not found / invalid table name
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

TENANT = os.environ.get("SENTINEL_TENANT_ID") or os.environ.get("AZURE_TENANT_ID") or ""
CLIENT_ID = os.environ.get("SENTINEL_CLIENT_ID") or os.environ.get("AZURE_CLIENT_ID") or ""
CLIENT_SECRET = os.environ.get("SENTINEL_CLIENT_SECRET") or os.environ.get("AZURE_CLIENT_SECRET") or ""
WORKSPACE = os.environ.get("SENTINEL_WORKSPACE_ID", "")
API_BASE = (os.environ.get("SENTINEL_API_BASE") or "https://api.loganalytics.io").rstrip("/")
LOGIN_BASE = (os.environ.get("SENTINEL_LOGIN_BASE") or "https://login.microsoftonline.com").rstrip("/")
PROXY = os.environ.get("SENTINEL_PROXY") or os.environ.get("HTTPS_PROXY") or ""

TABLE_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def _require_creds():
    missing = []
    if not TENANT:
        missing.append("SENTINEL_TENANT_ID")
    if not CLIENT_ID:
        missing.append("SENTINEL_CLIENT_ID")
    if not CLIENT_SECRET:
        missing.append("SENTINEL_CLIENT_SECRET")
    if not WORKSPACE:
        missing.append("SENTINEL_WORKSPACE_ID")
    if missing:
        die(
            f"{', '.join(missing)} not set. Add to .claude/settings.local.json env, "
            "run ./scripts/setup.sh, or export in your shell. "
            "Setup walkthrough: tools/integrations/sentinel.md",
            2,
        )


def _open(req, timeout=240):
    handlers = []
    if PROXY:
        handlers.append(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
    return urllib.request.build_opener(*handlers).open(req, timeout=timeout)


def _http(method, url, headers, body=None, timeout=240):
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with _open(req, timeout=timeout) as r:
            txt = r.read().decode("utf-8", errors="replace")
            return json.loads(txt) if txt else {}
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode("utf-8", errors="replace") if e.fp else ""
        hint = ""
        if e.code == 401:
            hint = " (token rejected — check tenant/client id and whether the client secret has expired)"
        elif e.code == 403:
            hint = " (authenticated but not authorised — the app registration needs the Log Analytics Reader role on this workspace)"
        elif e.code == 404:
            hint = " (workspace not found — check SENTINEL_WORKSPACE_ID is the workspace GUID from the Overview blade)"
        elif e.code == 429:
            retry = e.headers.get("Retry-After", "?") if e.headers else "?"
            hint = f" (throttled — the query API allows 200 requests per 30s; retry after {retry}s)"
        raise ApiError(e.code, f"HTTP {e.code} {e.reason}{hint}: {body_txt[:600]}")
    except urllib.error.URLError as e:
        die(f"network error: {e.reason}", 1)


class ApiError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message


def get_token():
    url = f"{LOGIN_BASE}/{TENANT}/oauth2/v2.0/token"
    form = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": f"{API_BASE}/.default",
    }).encode("utf-8")
    try:
        resp = _http("POST", url, {"Content-Type": "application/x-www-form-urlencoded"}, form, timeout=60)
    except ApiError as e:
        die(f"token request failed: {e.message}", 1)
    token = resp.get("access_token")
    if not token:
        die(f"token response missing access_token: {json.dumps(resp)[:400]}", 1)
    return token


def _dry(method, url, body=None, note=None):
    out = {
        "dry_run": True,
        "method": method,
        "url": url,
        "headers": {"Authorization": "Bearer <redacted>" if CLIENT_SECRET else "Bearer <unset>",
                    "Content-Type": "application/json"},
        "body": body,
    }
    if note:
        out["note"] = note
    print(json.dumps(out, indent=2))


def run_query(token, kql, timespan):
    url = f"{API_BASE}/v1/workspaces/{urllib.parse.quote(WORKSPACE, safe='')}/query"
    body = json.dumps({"query": kql, "timespan": timespan}).encode("utf-8")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return _http("POST", url, headers, body)


def distil_result(resp, max_rows):
    """Flatten the API's tables/columns/rows envelope into a list of dicts."""
    tables = resp.get("tables") or []
    if not tables:
        return {"row_count": 0, "rows": [], "truncated": False}
    t = tables[0]
    cols = [c.get("name") for c in (t.get("columns") or [])]
    rows = t.get("rows") or []
    out_rows = [dict(zip(cols, r)) for r in rows[:max_rows]]
    return {
        "columns": cols,
        "row_count": len(rows),
        "rows": out_rows,
        "truncated": len(rows) > max_rows,
    }


def _emit(operation, payload):
    out = {"source": "sentinel", "operation": operation, "query_time": now_iso(),
           "workspace_id": WORKSPACE or "<unset>"}
    out.update(payload)
    print(json.dumps(out, indent=2))


# ---------- commands ----------

def cmd_check(args):
    kql = "print check='ok'"
    if args.dry_run:
        _dry("POST", f"{API_BASE}/v1/workspaces/{WORKSPACE or '<SENTINEL_WORKSPACE_ID>'}/query",
             {"query": kql, "timespan": "PT5M"},
             note="preceded by a client-credentials token POST to "
                  f"{LOGIN_BASE}/{TENANT or '<SENTINEL_TENANT_ID>'}/oauth2/v2.0/token")
        return
    _require_creds()
    token = get_token()
    try:
        run_query(token, kql, "PT5M")
    except ApiError as e:
        die(e.message, 1)
    _emit("check", {"status": "ok",
                    "auth": "token issued and accepted",
                    "workspace": "reachable and queryable"})


def cmd_tables(args):
    url = f"{API_BASE}/v1/workspaces/{urllib.parse.quote(WORKSPACE, safe='') or '<SENTINEL_WORKSPACE_ID>'}/metadata"
    if args.dry_run:
        _dry("GET", url)
        return
    _require_creds()
    token = get_token()
    try:
        resp = _http("GET", url, {"Authorization": f"Bearer {token}"})
    except ApiError as e:
        die(e.message, 1)
    tables = resp.get("tables") or []
    items = []
    for t in tables:
        name = t.get("name")
        if args.filter and args.filter.lower() not in (name or "").lower():
            continue
        items.append({
            "name": name,
            "description": (t.get("description") or "").strip()[:160] or None,
            "column_count": len(t.get("columns") or []),
        })
    items.sort(key=lambda x: x["name"] or "")
    _emit("tables", {
        "note": "schema-known tables; a table can be schema-known yet empty — "
                "confirm with `ingestion` or `probe` before hunting in it",
        "filter": args.filter,
        "count": len(items),
        "tables": items,
    })


def cmd_ingestion(args):
    kql = (
        f"Usage | where TimeGenerated > ago({int(args.days)}d) "
        "| summarize ingested_mb = round(sum(Quantity), 2), last_record = max(TimeGenerated) by DataType "
        "| sort by ingested_mb desc"
    )
    if args.dry_run:
        _dry("POST", f"{API_BASE}/v1/workspaces/{WORKSPACE or '<SENTINEL_WORKSPACE_ID>'}/query",
             {"query": kql, "timespan": f"P{int(args.days)}D"})
        return
    _require_creds()
    token = get_token()
    try:
        resp = run_query(token, kql, f"P{int(args.days)}D")
    except ApiError as e:
        die(e.message, 1)
    result = distil_result(resp, max_rows=500)
    _emit("ingestion", {
        "note": f"tables with billable ingestion in the last {int(args.days)}d, from the Usage table; "
                "free/system tables may not appear here even when populated",
        "days": int(args.days),
        "count": result["row_count"],
        "tables": result["rows"],
    })


def cmd_probe(args):
    names = [t.strip() for t in args.tables.split(",") if t.strip()]
    if not names:
        die("no table names given", 3)
    for n in names:
        if not TABLE_NAME_RE.match(n):
            die(f"invalid table name: {n!r} (letters, digits, underscore only)", 3)
    if args.dry_run:
        _dry("POST", f"{API_BASE}/v1/workspaces/{WORKSPACE or '<SENTINEL_WORKSPACE_ID>'}/query",
             {"query": f"<per-table> {names[0]} | where TimeGenerated > ago({int(args.days)}d) | summarize rows=count()",
              "timespan": f"P{int(args.days)}D"},
             note=f"one query per table for {len(names)} table(s)")
        return
    _require_creds()
    token = get_token()
    results = []
    for name in names:
        kql = f"{name} | where TimeGenerated > ago({int(args.days)}d) | summarize rows = count()"
        try:
            resp = run_query(token, kql, f"P{int(args.days)}D")
            rows = distil_result(resp, max_rows=1)["rows"]
            count = rows[0].get("rows") if rows else 0
            results.append({"table": name, "available": True, "rows_in_window": count,
                            "populated": bool(count)})
        except ApiError as e:
            if e.status == 400:
                results.append({"table": name, "available": False, "rows_in_window": None,
                                "populated": False, "reason": "table not present in this workspace"})
            else:
                die(e.message, 1)
    _emit("probe", {
        "days": int(args.days),
        "count": len(results),
        "tables": results,
        "available": [r["table"] for r in results if r["available"] and r["populated"]],
        "empty": [r["table"] for r in results if r["available"] and not r["populated"]],
        "missing": [r["table"] for r in results if not r["available"]],
    })


def cmd_schema(args):
    if not TABLE_NAME_RE.match(args.table):
        die(f"invalid table name: {args.table!r} (letters, digits, underscore only)", 3)
    kql = f"{args.table} | getschema | project ColumnName, ColumnType"
    if args.dry_run:
        _dry("POST", f"{API_BASE}/v1/workspaces/{WORKSPACE or '<SENTINEL_WORKSPACE_ID>'}/query",
             {"query": kql, "timespan": "P1D"})
        return
    _require_creds()
    token = get_token()
    try:
        resp = run_query(token, kql, "P1D")
    except ApiError as e:
        if e.status == 400:
            die(f"table not present in this workspace: {args.table}", 1)
        die(e.message, 1)
    result = distil_result(resp, max_rows=500)
    _emit("schema", {
        "table": args.table,
        "column_count": result["row_count"],
        "columns": result["rows"],
    })


def cmd_query(args):
    if args.file:
        if not os.path.isfile(args.file):
            die(f"file not found: {args.file}", 3)
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                kql = f.read()
        except OSError as e:
            die(f"unable to read {args.file}: {e}", 3)
    else:
        kql = args.kql
    if not kql or not kql.strip():
        die("no KQL given (positional argument or --file)", 3)

    if args.dry_run:
        _dry("POST", f"{API_BASE}/v1/workspaces/{WORKSPACE or '<SENTINEL_WORKSPACE_ID>'}/query",
             {"query": kql, "timespan": args.timespan})
        return
    _require_creds()
    token = get_token()
    try:
        resp = run_query(token, kql, args.timespan)
    except ApiError as e:
        die(e.message, 1)
    result = distil_result(resp, max_rows=args.max_rows)
    _emit("query", {
        "timespan": args.timespan,
        "kql": kql if len(kql) <= 2000 else kql[:2000] + " …<truncated in echo, sent in full>",
        "columns": result.get("columns"),
        "row_count": result["row_count"],
        "truncated": result["truncated"],
        "rows": result["rows"],
    })


# ---------- arg parsing ----------

def main():
    ap = argparse.ArgumentParser(
        prog="sentinel.py",
        description="Microsoft Sentinel / Log Analytics query CLI (stdlib only, read-only).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    def _common(p):
        p.add_argument("--dry-run", action="store_true")

    p = sub.add_parser("check", help="verify auth + workspace reachability (print check='ok')")
    _common(p)
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("tables", help="GET /metadata — all tables the workspace schema knows")
    p.add_argument("--filter", help="case-insensitive substring filter on table name")
    _common(p)
    p.set_defaults(func=cmd_tables)

    p = sub.add_parser("ingestion", help="tables with recent billable ingestion (Usage table)")
    p.add_argument("--days", type=int, default=30, help="lookback window in days (default 30)")
    _common(p)
    p.set_defaults(func=cmd_ingestion)

    p = sub.add_parser("probe", help="per-table existence + row count over a window")
    p.add_argument("tables", help="comma-separated table names, e.g. DeviceNetworkEvents,SigninLogs")
    p.add_argument("--days", type=int, default=7, help="lookback window in days (default 7)")
    _common(p)
    p.set_defaults(func=cmd_probe)

    p = sub.add_parser("schema", help="column names + types for one table (getschema)")
    p.add_argument("table")
    _common(p)
    p.set_defaults(func=cmd_schema)

    p = sub.add_parser("query", help="run arbitrary KQL with a server-side timespan bound")
    p.add_argument("kql", nargs="?", help="the KQL query (or use --file)")
    p.add_argument("--file", help="read the KQL from a file instead")
    p.add_argument("--timespan", default="P7D",
                   help="ISO 8601 duration for the server-side window (default P7D); "
                        "intersects with any ago() filters inside the query")
    p.add_argument("--max-rows", type=int, default=100,
                   help="truncate emitted rows (default 100); truncated flag + total count always reported")
    _common(p)
    p.set_defaults(func=cmd_query)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
