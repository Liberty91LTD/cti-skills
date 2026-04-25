---
name: lookup-greynoise
description: Use when you need to classify an IP as internet scanner noise vs. targeted activity. Returns noise/riot flags, classification (benign/malicious/unknown), actor name if known. IP-only. Commonly invoked by /ip-investigation to filter out mass-scanning noise. Retrieval only.
metadata:
  version: 1.0.0
  tags: [lookup, threat-intel, noise-filtering, ip-only]
  api: greynoise
  default_source_reliability: B
  default_information_credibility: 2
---

# lookup-greynoise

Queries GreyNoise to classify whether an IP is internet background noise (opportunistic scanners, search engines, etc.) or targeted. IP-only. Retrieval only.

## When to invoke

- User asks if an IP is scanner noise or targeted
- Investigation skill wants to filter out mass-scanning IPs from indicator lists
- Deciding if an IP hitting your perimeter is worth investigating

## How to invoke

Two CLIs are provided. Pick by capability needed:

### Basic noise check — Node CLI (zero deps)

```bash
node tools/clis/greynoise.js ip <ip>
```

Hits the `/v3/community/{ip}` endpoint (free, 50/day). Best for fast retrieval inside an investigation chain.

### Full surface — Python CLI (uses official pygreynoise SDK)

```bash
python3 tools/clis/greynoise.py community <ip>          # FREE (50/day)
python3 tools/clis/greynoise.py context <ip>            # Enterprise
python3 tools/clis/greynoise.py riot <ip>               # Enterprise
python3 tools/clis/greynoise.py quick <ip,ip,...>       # Enterprise (bulk)
python3 tools/clis/greynoise.py similarity <ip>         # Enterprise
python3 tools/clis/greynoise.py timeline <ip> [--days N]  # Enterprise
python3 tools/clis/greynoise.py query "<gnql>"          # Enterprise
python3 tools/clis/greynoise.py stats "<gnql>"          # Enterprise
python3 tools/clis/greynoise.py metadata
```

Self-bootstraps a private venv at `tools/clis/.venv-greynoise/` on first run.

Capabilities the Node CLI doesn't have (Enterprise tier required for most):

1. **Context** — full per-IP telemetry: every port/protocol/payload combination GreyNoise has observed, broken down by date.
2. **GNQL search** (`query`) — find every IP matching a query: `classification:malicious tags:Mirai metadata.country:RU`. The killer pivot — discover scanner clusters by characteristic.
3. **GNQL stats** — bucket counts (countries, ASNs, tags, categories) for a query without pulling individual results.
4. **Similarity** — given an IP, find behaviorally similar scanners (often used to expand a single observation into a cluster).
5. **Timeline** — daily activity history for an IP — useful for distinguishing a brief campaign from persistent scanning.
6. **Quick (bulk)** — classify many IPs in one call (cheaper than N individual lookups).
7. **RIOT** — explicit known-benign check (CDNs, search engines, ISPs) without the noise classification.

GNQL examples:
```bash
# All malicious scanners hitting port 22 from Russia in the last day
python3 tools/clis/greynoise.py query 'classification:malicious raw_data.scan.port:22 metadata.country:RU last_seen:1d'

# Stats: country distribution of Mirai-tagged IPs
python3 tools/clis/greynoise.py stats 'tags:"Mirai" last_seen:30d'

# Find IPs similar to a known scanner
python3 tools/clis/greynoise.py similarity 185.220.101.45 --limit 50
```

Both CLIs accept `--dry-run`. Both exit code 2 if `$GREYNOISE_API_KEY` is unset (when not in dry-run). Report missing key; do not fabricate.

### Tier awareness

- **Community endpoint** is free (50/day) and good enough for "is this a known scanner?" — that's most investigation use.
- **Enterprise endpoints** unlock the pivoting power but require a paid tier. The CLI returns a 402 / "upgrade required" error if your key doesn't have access — that's the signal to fall back to community.

## Response format

```yaml
source: greynoise
indicator: <IP>
query_time: <ISO8601>
noise: <boolean>          # seen as internet background noise
riot: <boolean>           # rule-it-out: known-benign common service
classification: benign | malicious | unknown
name: <actor name or unknown>
last_seen: <date>
message: <summary>
```

## Rate limits

Community endpoint: 50 req/day free. Enterprise: much higher.

## Source reliability (Admiralty default)

Default rating for downstream `/score-source`: **B2** (usually reliable, probably true). Empirical signal. A `noise: true` result is strong evidence the IP is not targeted.

## Operational notes

- IP addresses only. The CLI rejects non-IP inputs.
- `riot: true` is a strong signal the IP is a benign common service (CDN, search engine, etc.) — downgrade severity of any detection against it.
- `classification: malicious` + `noise: true` = mass-scanning threat actor infrastructure, not a targeted campaign.

## Related skills

- `/lookup-abuseipdb` — abuse reports for the same IP
- `/lookup-virustotal`, `/lookup-shodan` — additional IP context
- `/ip-investigation` — uses GreyNoise to filter noise early in the pipeline

## See also

- Integration setup: `tools/integrations/greynoise.md`
- Node CLI source: `tools/clis/greynoise.js`
- Python CLI source: `tools/clis/greynoise.py`
- Official Python SDK: https://github.com/GreyNoise-Intelligence/pygreynoise
- API docs: https://docs.greynoise.io/
- GNQL syntax: https://docs.greynoise.io/docs/using-the-greynoise-query-language-gnql
