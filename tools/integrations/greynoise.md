# GreyNoise integration

[GreyNoise](https://www.greynoise.io/) classifies internet-wide scanning and background noise. Their honeypots observe opportunistic scanning activity, and they flag IPs as either "noise" (mass scanning, not targeting you specifically) or "RIOT" (rule-it-out: known-benign common services like CDNs, search engines, ISPs).

## Getting an API key

1. Sign up at https://www.greynoise.io/ (free community access)
2. Account → API keys → copy
3. Set `GREYNOISE_API_KEY` in your environment or via `./scripts/setup.sh`

## Rate limits

| Tier | Queries/day | Endpoints |
|---|---|---|
| Community (free) | 50 | `/community/{ip}` |
| Enterprise | higher | `/noise/context/{ip}`, search, pivots |

The CLI tries `/community/{ip}` first; falls back to `/noise/context/{ip}` if the key has enterprise access.

## Supported indicators

- IPv4 addresses

**IP only.** The CLI rejects non-IP inputs.

## Endpoints used

The **Node CLI** (`tools/clis/greynoise.js`) hits:
- `GET /v3/community/{ip}` (community, free)

The **Python CLI** (`tools/clis/greynoise.py`) wraps the official SDK and adds:
- `GET /v2/noise/context/{ip}` — full noise telemetry (Enterprise)
- `GET /v3/community/{ip}` — community noise classification (free)
- `GET /v3/riot/{ip}` — known-benign check (Enterprise)
- `GET /v2/noise/multi/quick` — bulk quick classification (Enterprise)
- `GET /v3/similarity/ips/{ip}` — find similar scanners (Enterprise)
- `GET /v3/timeline/{ip}` — IP activity timeline (Enterprise)
- `GET /v2/experimental/gnql` — GNQL query (Enterprise)
- `GET /v2/experimental/gnql/stats` — GNQL stats (Enterprise)
- `GET /v2/meta/metadata` — dataset tags/categories

Authentication header: `key: $GREYNOISE_API_KEY` (handled by SDK).

## GNQL — the pivot language

GreyNoise Query Language is field-based with implicit AND, OR, NOT, and grouping:

| Field | Example | Use |
|---|---|---|
| `classification` | `classification:malicious` | benign/malicious/unknown |
| `noise` | `noise:true` | seen as background scanning |
| `riot` | `riot:true` | known-benign service |
| `tags` | `tags:"Mirai"` | actor/family tags |
| `actor` | `actor:"unknown"` | named actor cluster |
| `metadata.country` | `metadata.country:RU` | scanner origin country |
| `metadata.asn` | `metadata.asn:13335` | ASN |
| `metadata.organization` | `metadata.organization:"Hosting Co"` | org/ISP |
| `metadata.category` | `metadata.category:hosting` | infrastructure type |
| `raw_data.scan.port` | `raw_data.scan.port:22` | port/protocol observed |
| `last_seen` | `last_seen:1d` | time window (1d, 7d, 30d) |
| `first_seen` | `first_seen:>2026-01-01` | absolute date filter |
| `vpn` | `vpn:true` | known VPN exit node |
| `spoofable` | `spoofable:false` | non-spoofable (real source IP) |

Combine with `AND`, `OR`, `NOT`, parentheses. Full syntax: https://docs.greynoise.io/docs/using-the-greynoise-query-language-gnql

## Admiralty defaults (for `/score-source`)

**Source reliability:** B (usually reliable) — empirical honeypot observations.
**Information credibility:** 2 (probably true) — GreyNoise has strong data hygiene.

**Operational signal interpretation:**
- `noise: true` → IP is mass-scanning the internet. Strong evidence it is NOT a targeted threat to you specifically. Downgrade the severity of any detection.
- `riot: true` → IP is a known-benign common service (Googlebot, CDN, etc.). Likely a false positive if flagged by other tools.
- `classification: malicious` + `noise: true` → opportunistic scanner with known-bad intent (exploit scanner, credential stuffer). Still not targeted, but worth blocking.
- `classification: malicious` + `noise: false` → potential targeted activity. Investigate further.
- Unknown / no record → GreyNoise has not observed this IP in background noise. Does NOT mean clean — check other sources.

## Testing your key

```bash
curl -s "https://api.greynoise.io/v3/community/8.8.8.8" \
  -H "key: $GREYNOISE_API_KEY" | head -c 200
```

## See also

- API docs: https://docs.greynoise.io/
- Community endpoint: https://docs.greynoise.io/reference/get_v3-community-ip
- GNQL syntax: https://docs.greynoise.io/docs/using-the-greynoise-query-language-gnql
- Official Python SDK: https://github.com/GreyNoise-Intelligence/pygreynoise
- Lookup skill: `skills/lookup-greynoise/SKILL.md`
- Node CLI source: `tools/clis/greynoise.js`
- Python CLI source: `tools/clis/greynoise.py`
