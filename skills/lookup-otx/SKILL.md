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

```bash
node tools/clis/otx.js <type> <value>
# where <type> is one of: ip, domain, hash, url
```

Examples:
```bash
node tools/clis/otx.js ip 203.0.113.42
node tools/clis/otx.js domain example.com
node tools/clis/otx.js hash 44d88612fea8a8f36de82e1278abb02f
node tools/clis/otx.js url "https://example.com/path"
```

Use `--dry-run` to preview the API request.

If `$OTX_API_KEY` is unset, the CLI exits with code 2. Report missing key; do not fabricate.

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
- CLI source: `tools/clis/otx.js`
