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

- `GET /api/v1/indicators/IPv4/{ip}/general`
- `GET /api/v1/indicators/IPv4/{ip}/passive_dns` (optional pivot)
- `GET /api/v1/indicators/domain/{domain}/general`
- `GET /api/v1/indicators/file/{hash}/general`
- `GET /api/v1/indicators/url/{url}/general`

Authentication header: `X-OTX-API-KEY: $OTX_API_KEY`.

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
- CLI source: `tools/clis/otx.js`
