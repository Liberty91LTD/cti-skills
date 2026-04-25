---
name: lookup-shodan
description: Use when you need host reconnaissance for an IP or domain — open ports, services, banners, OS detection, vulnerabilities. For domains, resolves DNS first then queries the IP. Commonly invoked by /ip-investigation and /domain-investigation. Retrieval only.
metadata:
  version: 1.0.0
  tags: [lookup, threat-intel, reconnaissance]
  api: shodan
  default_source_reliability: B
  default_information_credibility: 2
---

# lookup-shodan

Queries Shodan for host reconnaissance data on IPs. For domains, resolves DNS first then queries the resolved IP. Retrieval only — do not interpret results.

## When to invoke

- User asks what ports/services an IP exposes
- Investigation skill needs infrastructure fingerprinting
- Vulnerability scan context (CVEs on exposed services)

## How to invoke

Two CLIs are provided. Pick by capability needed:

### Basic host lookup — Node CLI (zero deps)

```bash
node tools/clis/shodan.js ip <ip>
node tools/clis/shodan.js domain <domain>     # resolves DNS first, then queries IP
```

Hits the host endpoint only. Best for fast retrieval inside an investigation chain. Throttles at 1 req/sec.

### Full search + DNS surface — Python CLI (uses official shodan-python SDK)

```bash
python3 tools/clis/shodan.py host <ip> [--history] [--minify]
python3 tools/clis/shodan.py search "<query>" [--limit N] [--page N] [--facets F1:N,F2:N]
python3 tools/clis/shodan.py count "<query>" [--facets F1:N,F2:N]
python3 tools/clis/shodan.py dns resolve <hostname[,hostname]>
python3 tools/clis/shodan.py dns reverse <ip[,ip]>
python3 tools/clis/shodan.py dns domain <domain>
python3 tools/clis/shodan.py info
python3 tools/clis/shodan.py ports
python3 tools/clis/shodan.py services
```

Self-bootstraps a private venv at `tools/clis/.venv-shodan/` on first run.

Capabilities the Node CLI doesn't have, ordered by CTI value:

1. **Search** — the killer pivot. Find every host on the internet matching a banner, certificate, JARM, favicon hash, HTTP title, exposed product+version, or geolocation+org combination. This is how you go from one piece of attacker infrastructure to the rest of the cluster.
2. **Count** — get the total result count for a query without burning result credits. Use this BEFORE a search to estimate scope and avoid query-credit waste on broad queries.
3. **Facets** — group result counts by `country`, `org`, `port`, `product`, `asn`, `tag`, `vuln`, etc. Single call gives you the breakdown.
4. **Domain info** — subdomains + DNS records for a domain in one call.
5. **Reverse DNS** for one or many IPs.
6. **Account info** — see remaining query credits BEFORE a campaign.
7. **History** — historical banner observations on a host (paid plans).

Search query examples:
```bash
# Find all Cobalt Strike Team Servers visible to Shodan
python3 tools/clis/shodan.py search 'product:"Cobalt Strike Team Server"'

# Count C2-pattern hosts in a country before searching
python3 tools/clis/shodan.py count 'http.title:"Login Page" country:RU'

# Facet a query — what orgs / countries host this software?
python3 tools/clis/shodan.py search 'product:"Sliver" port:443' --facets org:10,country:10

# Find all hosts presenting a specific certificate CN
python3 tools/clis/shodan.py search 'ssl.cert.subject.CN:"badcorp.example"'

# Pivot by JARM fingerprint (very strong infrastructure marker)
python3 tools/clis/shodan.py search 'ssl.jarm:1234567890abcdef...'

# Vulnerable version exposed
python3 tools/clis/shodan.py search 'vuln:CVE-2024-21887'
```

Both CLIs accept `--dry-run`. Both exit code 2 if `$SHODAN_API_KEY` is unset (when not in dry-run). Report missing key; do not fabricate.

### Credit awareness

Shodan plans have **query credits** (search/count/facets) and **scan credits** (active scans). Run `python3 tools/clis/shodan.py info` to check your balance before a search-heavy session. Free tier is severely limited — most CTI use needs the Membership ($49 one-time, 100 query credits/month) or a higher tier.

## Response format

```yaml
source: shodan
indicator: <IP or domain>
resolved_ip: <IP>    # present if input was domain
query_time: <ISO8601>
hostnames: [<list>]
org: <organisation>
isp: <ISP>
country: <country>
os: <detected OS>
open_ports: [<list>]
services:
  - port: <port>
    product: <name>
    version: <version>
    banner: <truncated>
vulnerabilities: [<CVE list>]
last_update: <date>
```

## Rate limits

Free tier: 1 request/sec, query credits limited. Paid tiers have higher limits.

## Source reliability (Admiralty default)

Default rating for downstream `/score-source`: **B2** (usually reliable, probably true). Banner grabs are empirical but can be stale — check `last_update` and downgrade to **C3** if >30 days old.

## Related skills

- `/lookup-censys` — alternative infrastructure scanner
- `/lookup-virustotal`, `/lookup-abuseipdb`, `/lookup-greynoise` — reputation context for the same IP
- `/ip-investigation`, `/domain-investigation`

## See also

- Integration setup: `tools/integrations/shodan.md`
- Node CLI source: `tools/clis/shodan.js`
- Python CLI source: `tools/clis/shodan.py`
- Official Python SDK: https://github.com/achillean/shodan-python
- SDK docs: https://shodan.readthedocs.io/
- Search query syntax: https://help.shodan.io/the-basics/search-query-fundamentals
- Filter reference: https://www.shodan.io/search/filters
