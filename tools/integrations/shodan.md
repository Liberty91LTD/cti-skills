# Shodan integration

[Shodan](https://www.shodan.io/) is an internet-wide scanning service. It continuously probes public IPs on common ports and records banners, services, TLS certificates, and detected vulnerabilities.

## Getting an API key

1. Sign up at https://account.shodan.io/register
2. Account page → API Key → copy
3. Set `SHODAN_API_KEY` in your environment or via `./scripts/setup.sh`

## Rate limits

| Tier | Queries | Rate |
|---|---|---|
| Free | ~100 lookups | 1 req/sec |
| Membership ($5 lifetime) | 100 query credits/month | 1 req/sec |
| Paid plans | higher | higher |

The CLI throttles to 1 req/sec to stay within free-tier limits.

## Supported indicators

- IPv4 addresses (primary)
- Domains (resolved to IP via `/dns/resolve` then queried)

## Endpoints used

- `GET /shodan/host/{ip}` — host summary (services, banners, vulns)
- `GET /dns/resolve?hostnames={domain}` — DNS resolution (free, no credits)
- `GET /shodan/host/search?query={query}` — search (uses query credits)

Authentication: `?key=$SHODAN_API_KEY` query parameter.

## Admiralty defaults (for `/score-source`)

**Source reliability:** B (usually reliable) — empirical scan data.
**Information credibility:** 2 (probably true) — banners can be spoofed; data can be stale.

**Downgrades:**
- `last_update` >30 days old → **C3**
- Banner obviously spoofed (impossible service/version combo) → **D4**

**Upgrades:**
- Fresh scan (<7 days), known-vulnerable software version with confirmed CVE → **A1**

## Testing your key

```bash
curl -s "https://api.shodan.io/shodan/host/8.8.8.8?key=$SHODAN_API_KEY" | head -c 200
```

## Privacy notes

- Shodan is a public service. Your queries may be cached by Shodan but are not exposed to third parties.
- Queries consume credits (paid tiers). Free DNS resolve is unlimited.

## See also

- API docs: https://developer.shodan.io/api
- Lookup skill: `skills/lookup-shodan/SKILL.md`
- CLI source: `tools/clis/shodan.js`
