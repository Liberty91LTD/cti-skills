---
name: lookup-censys
description: Use when you need deep host + certificate reconnaissance for an IP or need to run a Censys search query. Returns services, TLS certificates, ASN, and location. Free tier is severely limited (250 queries/month) — use sparingly. Retrieval only.
metadata:
  version: 1.0.0
  tags: [lookup, threat-intel, reconnaissance, quota-limited]
  api: censys
  default_source_reliability: A
  default_information_credibility: 2
---

# lookup-censys

Queries Censys for host and certificate reconnaissance on IPs, or runs a Censys Search query. Retrieval only. Quota-aware — free tier is 250 queries/month.

## When to invoke

- Shodan wasn't sufficient and deeper host data is needed
- TLS certificate pivoting (find other hosts sharing a cert)
- Specific Censys Search query required

**Do NOT invoke for:**
- Bulk enrichment (will exhaust quota)
- IPs you can get from Shodan first

## How to invoke

Two CLIs are provided. Pick by capability needed.

> **Auth note**: Censys migrated to a single Personal Access Token (PAT) on the new Platform. The Node CLI uses the legacy Search API (HTTP Basic Auth with `CENSYS_API_ID` + `CENSYS_API_SECRET`); the Python CLI uses the new Platform API (Bearer auth with `CENSYS_PAT`). New accounts get a PAT — use the Python CLI. Old accounts may still have working legacy credentials and can use either.

### Basic host + search — Node CLI (legacy Search API)

```bash
node tools/clis/censys.js ip <ip>
node tools/clis/censys.js search "<query>"      # Censys Search syntax
```

Requires `CENSYS_API_ID` + `CENSYS_API_SECRET` (legacy). Hits hosts/{ip} or hosts/search.

### Full Platform surface — Python CLI (new Censys Platform SDK)

```bash
python3 tools/clis/censys.py host <ip> [--at-time ISO8601]
python3 tools/clis/censys.py timeline <ip> --start ISO8601 --end ISO8601
python3 tools/clis/censys.py services <ip>
python3 tools/clis/censys.py search "<query>" [--page-size N] [--page-token TOKEN] [--fields F1,F2]
python3 tools/clis/censys.py aggregate "<query>" --field FIELD [--buckets N] [--filter-by-query]
python3 tools/clis/censys.py certs view <cert_id>
python3 tools/clis/censys.py certs list <id1,id2,...>
```

Requires `CENSYS_PAT` (new). Self-bootstraps a private venv at `tools/clis/.venv-censys/` on first run (installs `censys-platform`).

Capabilities the Node CLI doesn't have, ordered by CTI value:

1. **Aggregate** — the unsung hero. **Aggregations are free** (do not consume query credits) and let you ask "how many hosts in this query break down by country / port / ASN / product?" in a single call. Use this BEFORE a search to scope the result set without spending credits.
2. **Host timeline** — the activity history of a single IP between two timestamps. New in Platform.
3. **At-time host view** — see what a host looked like at a past timestamp (Platform-only).
4. **Service listing** — enumerate just the services on a host without the full record.
5. **Certificate view by ID** + **certificate list (bulk)** — pull cert detail or batch fetch.
6. **Cursor-based pagination** — `--page-token` for traversing large result sets.

Examples:
```bash
# Free aggregation: count hosts running Cobalt Strike by country (no credits)
python3 tools/clis/censys.py aggregate \
  'services.product: "Cobalt Strike Team Server"' \
  --field location.country_code

# Free aggregation: ASN distribution of a JARM-fingerprinted cluster
python3 tools/clis/censys.py aggregate \
  'services.tls.jarm.fingerprint: "1234567890abcdef..."' \
  --field autonomous_system.asn --buckets 50

# What was this IP doing two weeks ago? (Platform-only)
python3 tools/clis/censys.py host 185.220.101.45 \
  --at-time 2026-04-12T00:00:00Z

# Daily activity timeline for an IP
python3 tools/clis/censys.py timeline 185.220.101.45 \
  --start 2026-04-01T00:00:00Z --end 2026-04-26T00:00:00Z

# Certificate view by ID (the SHA-256 fingerprint)
python3 tools/clis/censys.py certs view 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8

# Search hosts and only return specific fields (saves payload)
python3 tools/clis/censys.py search \
  'services.tls.certificates.leaf_data.subject.common_name: "*.badcorp.example"' \
  --fields ip,location.country_code,services.port
```

Both CLIs accept `--dry-run`. Python CLI exits code 2 if `CENSYS_PAT` is unset; Node CLI exits code 2 if either of the legacy variables is unset. Report missing credentials; do not fabricate.

### Free tier reality check (Platform API)

The new Censys Platform tightened free-tier API access. As of 2026, free Community accounts can call these endpoints **only**:

- `host` — view host detail by IP ✓
- `services` — list services on a host ✓
- `timeline` — host activity timeline between two timestamps ✓
- `certs view` — certificate by ID ✓

These are restricted on free tier (return `403 "endpoint requires organization ID"`):

- `search` — paid plan with organization required
- `aggregate` — paid plan only (no longer free as it was on the legacy API)
- `certs list` — likely same restriction

For **search / aggregation / pivoting on a free account**, use the Censys web UI at https://platform.censys.io/. The web UI has full access; API access for those endpoints is a paid feature.

For **CLI use on free tier**, the Python CLI is still useful for per-IP enrichment (`host`, `services`, `timeline`) but won't replace the legacy Search API's free aggregations. If you have a legacy account with `CENSYS_API_ID` + `CENSYS_API_SECRET`, the Node CLI may give you better free-tier reach for now.

### Credits (free tier)

Each per-IP call on a free account counts against the **250 queries/month** quota. Be deliberate.

### When to use Censys vs Shodan

For bulk infrastructure mapping, **prefer Shodan** — its free-membership tier ($49 one-time) gives you proper search access, and `count` is free. Reserve Censys for high-fidelity per-IP enrichment of indicators you've already found elsewhere.

## Response format

```yaml
source: censys
indicator: <IP or search query>
query_time: <ISO8601>
services:
  - port: <port>
    service: <name>
    banner: <truncated>
certificates:
  - subject_cn: <common name>
    issuer: <issuer>
    sha256: <fingerprint>
autonomous_system:
  asn: <number>
  name: <name>
location:
  country: <country>
  city: <city>
last_updated: <date>
```

## Rate limits

Free tier: **250 queries/month** (very limited). Research tier: 10k/month. Paid: unlimited.

## Source reliability (Admiralty default)

Default rating for downstream `/score-source`: **A2** (completely reliable, probably true). Censys is an authoritative internet-scan dataset with strong data hygiene.

## Operational notes

- **Quota conservation is critical.** Before invoking, consider whether Shodan can answer the question first.
- For certificate pivoting specifically, Censys is often the right first call — Shodan has weaker cert data.
- Uses HTTP Basic Auth with `$CENSYS_API_ID` and `$CENSYS_API_SECRET`.

## Related skills

- `/lookup-shodan` — lighter-weight alternative with higher rate limits
- `/lookup-virustotal` — reputation, not reconnaissance
- `/ip-investigation`

## See also

- Integration setup: `tools/integrations/censys.md`
- Node CLI source: `tools/clis/censys.js`
- Python CLI source: `tools/clis/censys.py`
- Official Python SDK: https://github.com/censys/censys-sdk-python
- API docs: https://docs.censys.com/reference/get-started
- Search syntax: https://search.censys.io/search/language
