# Censys integration

[Censys](https://censys.io/) is an internet-wide scanning and certificate-transparency dataset. It's the strongest option for TLS certificate pivoting and high-fidelity host reconnaissance, but the free tier is severely quota-limited.

## Getting API credentials

1. Sign up at https://accounts.censys.io/register (free)
2. Account → API → copy **API ID** and **API Secret** (two values, both required)
3. Set `CENSYS_API_ID` and `CENSYS_API_SECRET` in your environment or via `./scripts/setup.sh`

## Rate limits

| Tier | Queries/month | Notes |
|---|---|---|
| Community (free) | **250** | Very limited — use sparingly |
| Research | 10,000 | Requires application, free for academic/researchers |
| Paid plans | higher | Contract-based |

**Quota conservation is critical on the free tier.** Prefer Shodan for most IP reconnaissance; reserve Censys for certificate pivoting or when Shodan data is insufficient.

## Supported indicators

- IPv4 / IPv6 addresses
- Censys Search queries (full search syntax)

## Endpoints used

The **Node CLI** (`tools/clis/censys.js`) hits:
- `GET /api/v2/hosts/{ip}` — host summary
- `GET /api/v2/hosts/search?q={query}` — search

The **Python CLI** (`tools/clis/censys.py`) wraps the official SDK and adds:
- `GET /api/v2/hosts/aggregate?q={query}&field={field}` — **FREE aggregation** (no credits)
- `GET /api/v2/certificates/{sha256}` — certificate detail by fingerprint
- `GET /api/v2/certificates/search?q={query}` — certificate search
- `GET /api/v1/account` — remaining quota
- Multi-page cursor traversal for hosts.search and certs.search

Authentication: HTTP Basic Auth with `CENSYS_API_ID:CENSYS_API_SECRET` (handled by SDK).

## The killer feature: aggregations are free

Most CTI tooling treats every query as paid. Censys's `aggregate` endpoint is the exception — it returns bucket counts for any field across a query without consuming credits. Use it relentlessly before paid searches:

```bash
# How many hosts match a JARM fingerprint, broken down by country?
python3 tools/clis/censys.py aggregate \
  'services.tls.jarm.fingerprint: "1234..."' \
  --field location.country_code

# What ASNs are hosting Cobalt Strike servers?
python3 tools/clis/censys.py aggregate \
  'services.product: "Cobalt Strike Team Server"' \
  --field autonomous_system.asn --buckets 50

# Distribution of services on a /24 of suspect infrastructure
python3 tools/clis/censys.py aggregate \
  'ip: 185.220.101.0/24' \
  --field services.port
```

Use the bucket counts to decide whether a paid `search` is worthwhile and how to scope it.

## Admiralty defaults (for `/score-source`)

**Source reliability:** A (completely reliable) — Censys is an authoritative internet-scan dataset with strong data hygiene and frequent re-scans.
**Information credibility:** 2 (probably true) — empirical but can be stale.

**Downgrades:**
- `last_updated` >30 days old → **B3**

## Testing your credentials

```bash
curl -s -u "$CENSYS_API_ID:$CENSYS_API_SECRET" \
  "https://search.censys.io/api/v2/hosts/8.8.8.8" | head -c 200
```

## Privacy notes

- Censys is a public scanning service. Your queries may be logged but are not exposed to third parties.
- Queries count against monthly quota — use `--dry-run` when testing invocation logic.

## Common pivots

- **Cert → other hosts** — find every IP serving a specific TLS certificate (by SHA-256 fingerprint or subject CN)
- **JARM fingerprint** — find hosts with a matching TLS stack fingerprint
- **Banner string** — find hosts with a specific service banner

These are the situations where Censys beats Shodan.

## See also

- API docs: https://docs.censys.com/reference/get-started
- Search syntax: https://search.censys.io/search/language
- Official Python SDK: https://github.com/censys/censys-sdk-python
- Lookup skill: `skills/lookup-censys/SKILL.md`
- Node CLI source: `tools/clis/censys.js`
- Python CLI source: `tools/clis/censys.py`
