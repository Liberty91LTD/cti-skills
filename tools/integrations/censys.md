# Censys integration

[Censys](https://censys.io/) is an internet-wide scanning and certificate-transparency dataset. It's the strongest option for TLS certificate pivoting and high-fidelity host reconnaissance, but the free tier is severely quota-limited.

## Auth — two models

Censys runs two products with different auth:

1. **Censys Platform** (new, recommended) — single **Personal Access Token (PAT)** with Bearer auth.
   - Sign up at https://accounts.censys.io/register
   - Get token at https://accounts.censys.io/settings/personal-access-tokens
   - Set `CENSYS_PAT` in env or via `/cti-setup` / `./scripts/setup.sh`
   - The full token value is shown **once** at creation — copy immediately.
   - Used by the Python CLI (`tools/clis/censys.py`) via the `censys-platform` SDK.

2. **Censys Search (legacy)** — **API ID + API Secret** pair with HTTP Basic Auth.
   - Older accounts only; new signups don't get this.
   - Set `CENSYS_API_ID` and `CENSYS_API_SECRET`.
   - Used by the Node CLI (`tools/clis/censys.js`).

If you're on a new account, use only `CENSYS_PAT`. The Python CLI is the path forward.

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

The **Node CLI** (`tools/clis/censys.js`) hits the legacy Search API:
- `GET https://search.censys.io/api/v2/hosts/{ip}` — host summary
- `GET https://search.censys.io/api/v2/hosts/search?q={query}` — search

Auth: HTTP Basic with `CENSYS_API_ID:CENSYS_API_SECRET`.

The **Python CLI** (`tools/clis/censys.py`) hits the new Censys Platform API via the `censys-platform` SDK:
- `GET /v3/global/asset/host/{ip}` — host detail (with optional `?at_time=`)
- `GET /v3/global/asset/host/{ip}/timeline` — host activity timeline
- `GET /v3/global/service/{host_id}` — service listing on a host
- `POST /v3/global/search/query` — host search (Bearer body)
- `POST /v3/global/search/aggregate` — **FREE aggregation** (no credits)
- `GET /v3/global/asset/certificate/{cert_id}` — certificate by ID
- `POST /v3/global/asset/certificate` — bulk certificate retrieval

Auth: `Authorization: Bearer $CENSYS_PAT`.

## Platform free-tier API limits (verified 2026-04-26)

Confirmed by live test: on the new Censys Platform, free Community accounts get **per-IP endpoints only** via API. The aggregation and search endpoints return:

```
403 Forbidden — "This endpoint requires an organization ID for API access.
Free users can only access this endpoint through the Platform UI."
```

So on the free tier you can:
- `GET /v3/global/asset/host/{ip}` — host detail ✓
- `GET /v3/global/asset/host/{ip}/timeline` — host timeline ✓
- `GET /v3/global/service/{host_id}` — service listing ✓
- `GET /v3/global/asset/certificate/{cert_id}` — certificate by ID ✓

But NOT:
- `POST /v3/global/search/query` — host search ✗ (requires org_id, paid)
- `POST /v3/global/search/aggregate` — aggregations ✗ (paid; this is a regression from the legacy API where they were free)
- `POST /v3/global/asset/certificate` — bulk cert list ✗ (likely same)

Search and aggregation are still available through the web UI at https://platform.censys.io/. For CLI access to those endpoints you need a paid Platform plan (the platform pricing page lists Researcher / Pro tiers).

If you need free CLI access to search and aggregate, your options are:
1. **Use Shodan instead** — Membership ($49 one-time) gives search access, and `count` is free.
2. **Use a legacy Censys Search account** — older accounts with `CENSYS_API_ID` + `CENSYS_API_SECRET` may still have free search/aggregate access via the legacy API. The Node CLI uses that path.
3. **Pay for a Platform plan** if you specifically need the new platform's threat-hunting capabilities.

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
