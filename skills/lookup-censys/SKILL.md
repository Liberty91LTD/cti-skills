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

Two CLIs are provided. Pick by capability needed:

### Basic host + search — Node CLI (zero deps)

```bash
node tools/clis/censys.js ip <ip>
node tools/clis/censys.js search "<query>"      # Censys Search syntax
```

Hits hosts/{ip} or hosts/search. Best for fast retrieval inside an investigation chain.

### Full SDK surface — Python CLI (uses official censys-sdk-python)

```bash
python3 tools/clis/censys.py host <ip>
python3 tools/clis/censys.py search "<query>" [--per-page N] [--pages N]
python3 tools/clis/censys.py certs view <sha256_fingerprint>
python3 tools/clis/censys.py certs search "<query>" [--per-page N] [--pages N]
python3 tools/clis/censys.py aggregate "<query>" --field FIELD [--buckets N]
python3 tools/clis/censys.py account
```

Self-bootstraps a private venv at `tools/clis/.venv-censys/` on first run.

Capabilities the Node CLI doesn't have, ordered by CTI value:

1. **Aggregate** — the unsung hero. **Aggregations are free** (do not consume query credits) and let you ask "how many hosts in this query break down by country / port / ASN / product?" in a single call. Use this BEFORE a search to scope the result set without spending credits.
2. **Certificate search** — find every cert matching a query (subject CN, issuer, SAN, fingerprint pattern). The strongest TLS-pivoting capability.
3. **Certificate view by fingerprint** — pull full cert detail including all hosts that have served it.
4. **Multi-page search** with cursor — collect more than `per_page` results when a single page isn't enough.
5. **Account** — see remaining query credits BEFORE a search-heavy session.

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

# Cert search: every certificate signed for *.badcorp.example
python3 tools/clis/censys.py certs search \
  'parsed.names: "*.badcorp.example"'

# Pivot from a cert fingerprint to all hosts that served it
python3 tools/clis/censys.py search \
  'services.tls.certificates.leaf_data.fingerprint_sha256: 5e884898...'

# Quota check before committing to a sweep
python3 tools/clis/censys.py account
```

Both CLIs accept `--dry-run`. Both exit code 2 if credentials are missing (when not in dry-run). Report missing credentials; do not fabricate.

### Quota awareness — read this first

Censys free tier is **250 queries/month**, period. Each `host`, `search` page, and `certs` call costs one credit. Before a sweep:
1. Run `account` to check balance.
2. Run `aggregate` (free) to understand scope.
3. Only then run targeted `search` or `host` calls.

For bulk infrastructure mapping, **prefer Shodan** unless you specifically need Censys' superior certificate or scan-quality data.

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
