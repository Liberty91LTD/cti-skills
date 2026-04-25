# AlienVault OTX integration

[AlienVault OTX](https://otx.alienvault.com/) (now part of LevelBlue) is a community threat intelligence sharing platform. Users publish "pulses" — collections of IOCs and TTPs tied to a campaign, malware family, or actor.

## Getting an API key

1. Sign up at https://otx.alienvault.com/signup (free)
2. Settings → API Integration → copy API key
3. Set `OTX_API_KEY` in your environment or via `./scripts/setup.sh`

## Rate limits

| Tier | Requests/hour |
|---|---|
| Free | 10,000 |

Effectively unconstrained for interactive use.

## Supported indicators

- IPv4 / IPv6 addresses
- Domains / hostnames
- File hashes: MD5, SHA-1, SHA-256, PEHASH, IMPHASH
- URLs

## Endpoints used

The **Node CLI** (`tools/clis/otx.js`) hits these directly:
- `GET /api/v1/indicators/IPv4/{ip}/general`
- `GET /api/v1/indicators/IPv4/{ip}/passive_dns` (optional pivot)
- `GET /api/v1/indicators/domain/{domain}/general`
- `GET /api/v1/indicators/file/{hash}/general`
- `GET /api/v1/indicators/url/{url}/general`

Authentication header: `X-OTX-API-KEY: $OTX_API_KEY`.

The **Python CLI** (`tools/clis/otx.py`) wraps the official **OTXv2 SDK** for richer operations: full indicator details across every section (reputation, geo, malware, url_list, http_scans, analysis), pulse search, pulse retrieval, and subscribed-pulse listing.

## Python SDK

- Repo: https://github.com/AlienVault-OTX/OTX-Python-SDK
- PyPI: `pip install OTXv2`
- License: Apache 2.0 (per the upstream repo)

The Python CLI self-bootstraps a venv at `tools/clis/.venv-otx/` on first invocation, so users don't need to install OTXv2 globally and aren't blocked by PEP 668 on Homebrew Python. The venv directory is gitignored.

Key SDK methods used:
- `OTXv2.get_indicator_details_full(IndicatorTypes.X, value)` — pulls all sections at once
- `OTXv2.get_indicator_details_by_section(...)` — single section
- `OTXv2.search_pulses(query, max_results=N)` — keyword/tag search
- `OTXv2.get_pulse_details(pulse_id)` + `get_pulse_indicators(pulse_id)` — pulse retrieval
- `OTXv2.getall(limit=N)` — subscribed pulses

## Admiralty defaults (for `/score-source`)

**Source reliability:** C (fairly reliable) — crowd-sourced. Quality varies dramatically.
**Information credibility:** 3 (possibly true) — requires corroboration.

**Upgrades:**
- Pulse author is a known-reliable organization (Mandiant, Unit42, Talos, Cisco Talos, CrowdStrike, Microsoft Threat Intelligence, AbuseCH, etc.) → **B2**
- Multiple independent pulses (3+) reference the same indicator → **B3**

**Downgrades:**
- Single pulse with a new/unknown author → **D4**
- Pulse has no references or IOCs look scraped → **E5**

## Testing your key

```bash
curl -s "https://otx.alienvault.com/api/v1/indicators/IPv4/8.8.8.8/general" \
  -H "X-OTX-API-KEY: $OTX_API_KEY" | head -c 200
```

## See also

- API docs: https://otx.alienvault.com/api
- Lookup skill: `skills/lookup-otx/SKILL.md`
- Node CLI source: `tools/clis/otx.js`
- Python CLI source: `tools/clis/otx.py`
- Official Python SDK repo: https://github.com/AlienVault-OTX/OTX-Python-SDK
