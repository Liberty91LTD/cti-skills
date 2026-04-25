# Shodan integration

[Shodan](https://www.shodan.io/) is an internet-wide scanning service. It continuously probes public IPs on common ports and records banners, services, TLS certificates, and detected vulnerabilities.

## Getting an API key

1. Sign up at https://account.shodan.io/register
2. Account page → API Key → copy
3. Set `SHODAN_API_KEY` in your environment or via `./scripts/setup.sh`

## Rate limits and credits

Shodan plans differ along three axes — query credits (search/count/facets), scan credits (active scanning), and rate limits (req/sec). Lookups (`/shodan/host/{ip}`) and DNS calls do not consume credits.

| Plan | One-time cost | Query credits | Scan credits | Rate |
|---|---|---|---|---|
| Free | $0 | 0 | 0 | 1 req/sec |
| Membership | ~$49 | 100/month | 100/month | 1 req/sec |
| Freelancer | $89/month | 10,000/month | 10,000/month | higher |
| Small Business / Corporate | higher | unlimited | higher | higher |

The Node CLI throttles to 1 req/sec. Use `python3 tools/clis/shodan.py info` to check your remaining credits before search-heavy work.

## Supported indicators

- IPv4 addresses (primary)
- Domains (resolved to IP via `/dns/resolve`, then queried)

## Endpoints used

The **Node CLI** (`tools/clis/shodan.js`) hits:
- `GET /shodan/host/{ip}` — host summary (services, banners, vulns)
- `GET /dns/resolve?hostnames={domain}` — DNS resolution (free, no credits)

The **Python CLI** (`tools/clis/shodan.py`) wraps the official SDK and adds:
- `GET /shodan/host/search?query={q}&facets={f}` — keyword search with optional facets (consumes query credits)
- `GET /shodan/host/count?query={q}&facets={f}` — count without spending result credits
- `GET /dns/reverse?ips=...` — reverse DNS for one or many IPs
- `GET /dns/domain/{domain}` — subdomains and DNS records for a domain
- `GET /api-info` — account plan and remaining credits
- `GET /shodan/ports` — list of all ports Shodan crawls
- `GET /shodan/services` — list of all services Shodan recognises

Authentication: `?key=$SHODAN_API_KEY` query parameter (handled by SDK).

## Search query reference

Shodan's query language has filters and free-text. Combine with implicit AND.

| Filter | Example | Use |
|---|---|---|
| `product` | `product:"Cobalt Strike Team Server"` | Service fingerprint match |
| `port` | `port:443` | Port filter |
| `country` | `country:RU` | Country code |
| `org` | `org:"Hosting Co Ltd"` | Organisation/AS owner |
| `asn` | `asn:AS13335` | ASN filter |
| `hostname` | `hostname:badcorp.example` | Hostname substring |
| `ssl.cert.subject.CN` | `ssl.cert.subject.CN:"badcorp.example"` | TLS certificate CN |
| `ssl.jarm` | `ssl.jarm:1234567890abcdef...` | JARM fingerprint (very strong) |
| `http.title` | `http.title:"Login Page"` | HTTP page title |
| `http.html` | `http.html:phishkit-marker` | HTML body substring |
| `http.favicon.hash` | `http.favicon.hash:-1234567890` | Favicon mmh3 hash |
| `vuln` | `vuln:CVE-2024-21887` | Detected vulnerability |
| `tag` | `tag:c2` | Shodan-applied tag |
| `before` / `after` | `after:2026-01-01` | Time bounds |

Common useful facets (with `--facets`): `country`, `org`, `port`, `product`, `version`, `asn`, `tag`, `vuln`, `ssl.version`.

Full filter reference: https://www.shodan.io/search/filters

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
- SDK docs: https://shodan.readthedocs.io/
- Official Python SDK: https://github.com/achillean/shodan-python
- Search filters: https://www.shodan.io/search/filters
- Lookup skill: `skills/lookup-shodan/SKILL.md`
- Node CLI source: `tools/clis/shodan.js`
- Python CLI source: `tools/clis/shodan.py`
