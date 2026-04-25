---
name: lookup-otx
description: Use when you need to check an IP, domain, file hash, or URL against AlienVault OTX community pulses. Returns pulse count, key pulses, tags, related indicators, and passive DNS. Commonly invoked by investigation skills to pull community context. Retrieval only — does not interpret.
metadata:
  version: 1.0.0
  tags: [lookup, threat-intel, community]
  api: otx
  default_source_reliability: C
  default_information_credibility: 3
---

# lookup-otx

Queries AlienVault OTX for community pulse context on IPs, domains, file hashes, and URLs. Retrieval only — do not interpret results.

## When to invoke

- User asks what pulses reference an indicator
- Investigation skill needs community context (who's tracking this?)
- IOC enrichment pipeline is adding pulse metadata

## How to invoke

Two CLIs are provided. Pick by capability needed:

### Basic lookup — Node CLI (zero deps)

```bash
node tools/clis/otx.js <type> <value>
# where <type> is one of: ip, domain, hash, url
```

Hits the `/general` endpoint only. Returns pulses, related indicators, passive DNS, whois. Best for fast retrieval inside an investigation chain.

### Advanced operations — Python CLI (uses official OTXv2 SDK)

```bash
python3 tools/clis/otx.py indicator <type> <value> [--section SECTION]
python3 tools/clis/otx.py pulse search <query> [--limit N]
python3 tools/clis/otx.py pulse get <pulse_id>
python3 tools/clis/otx.py pulse subscribed [--limit N]
```

Self-bootstraps a private venv at `tools/clis/.venv-otx/` on first run (requires Python 3 + a working `python3 -m venv`). No global pip install.

Capabilities the Node CLI doesn't have:
- **Full indicator details** across every OTX section (general, reputation, geo, malware, url_list, passive_dns, http_scans, analysis) instead of just `/general`. Pass `--section` to limit.
- **Pulse keyword search** (`pulse search "lazarus"`) — discover pulses by topic.
- **Pulse retrieval by ID** with full description, references, and indicator list.
- **Subscribed pulses** — list pulses your OTX account follows.

Examples:
```bash
# Basic — same shape as Node CLI but with all sections populated
python3 tools/clis/otx.py indicator domain example.com

# Just one section
python3 tools/clis/otx.py indicator ip 203.0.113.42 --section malware

# Hash type auto-detected from length (MD5/SHA1/SHA256)
python3 tools/clis/otx.py indicator hash 44d88612fea8a8f36de82e1278abb02f

# Discover pulses by keyword
python3 tools/clis/otx.py pulse search "ransomware exchange"

# Pull a specific pulse
python3 tools/clis/otx.py pulse get 5f8f3e6e2a1b3c4d5e6f7a8b
```

Both CLIs accept `--dry-run` to preview the request without calling the API. Both exit code 2 if `$OTX_API_KEY` is unset (when not in dry-run). Report missing key; do not fabricate.

## Response format

```yaml
source: otx
indicator: <value>
type: ip | domain | hash | url
query_time: <ISO8601>
pulse_count: <number>
key_pulses:
  - name: <pulse name>
    tags: [<tags>]
    created: <date>
    tlp: <TLP>
    author: <author>
related_indicators: [<list>]
passive_dns: [<resolutions>]   # only for IP/domain
```

## Rate limits

Free tier: 10,000 req/hour — effectively unconstrained for interactive use.

## Source reliability (Admiralty default)

Default rating for downstream `/score-source`: **C3** (fairly reliable, possibly true). Community-submitted pulses vary wildly in quality. Upgrade to **B2** if pulse author is a known trustworthy org (Mandiant, Unit42, Talos, etc.).

## Related skills

- `/lookup-virustotal` — reputation aggregator for the same indicator
- `/lookup-urlscan` — live scan of URLs/domains
- `/score-source` — apply Admiralty rating
- `/ip-investigation`, `/domain-investigation`, `/hash-investigation`, `/url-investigation`

## See also

- Integration setup: `tools/integrations/otx.md`
- Node CLI source: `tools/clis/otx.js`
- Python CLI source (OTXv2 SDK): `tools/clis/otx.py`
- Official Python SDK: https://github.com/AlienVault-OTX/OTX-Python-SDK
- API reference: https://otx.alienvault.com/api
