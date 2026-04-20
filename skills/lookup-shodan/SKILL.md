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

```bash
node tools/clis/shodan.js ip <ip>
node tools/clis/shodan.js domain <domain>     # resolves DNS first, then queries IP
```

Use `--dry-run` to preview. Respect 1 req/sec rate limit (the CLI throttles automatically).

If `$SHODAN_API_KEY` is unset, the CLI exits with code 2.

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
- CLI source: `tools/clis/shodan.js`
