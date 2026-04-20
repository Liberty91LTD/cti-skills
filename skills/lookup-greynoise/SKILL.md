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

```bash
node tools/clis/greynoise.js ip <ip>
```

Use `--dry-run` to preview. The CLI tries the community endpoint first (free, rate-limited); falls back to enterprise `/noise/context/{ip}` if the API key has enterprise access.

If `$GREYNOISE_API_KEY` is unset, the CLI exits with code 2.

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
- CLI source: `tools/clis/greynoise.js`
