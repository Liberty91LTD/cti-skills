---
name: lookup-abuseipdb
description: Use when you need abuse-report history for an IPv4/IPv6 address — confidence score, total reports, distinct reporters, usage type. IP-only. Commonly invoked by /ip-investigation. Retrieval only.
metadata:
  version: 1.0.0
  tags: [lookup, threat-intel, reputation, ip-only]
  api: abuseipdb
  default_source_reliability: C
  default_information_credibility: 3
---

# lookup-abuseipdb

Queries AbuseIPDB for IP reputation data. IP addresses only (v4 and v6). Retrieval only — do not interpret.

## When to invoke

- User asks about abuse reports for an IP
- Investigation skill needs community-reported abuse context
- Triaging whether an IP has a history of malicious behavior

## How to invoke

```bash
node tools/clis/abuseipdb.js ip <ip>
```

Use `--dry-run` to preview.

If `$ABUSEIPDB_API_KEY` is unset, the CLI exits with code 2.

## Response format

```yaml
source: abuseipdb
indicator: <IP>
query_time: <ISO8601>
abuse_confidence: <0-100>
total_reports: <number>
distinct_reporters: <number>
last_reported: <date>
isp: <ISP>
usage_type: <type>
country: <country>
is_tor: <boolean>
recent_report_categories: [<list of category IDs>]
```

## Rate limits

Free tier: 1000 checks/day. Paid tiers have higher limits.

## Source reliability (Admiralty default)

Default rating for downstream `/score-source`: **C3** (fairly reliable, possibly true). Community-reported; false positives possible. Upgrade to **B2** if `distinct_reporters` >10 and `abuse_confidence` >75.

## Operational notes

- IP addresses only. The CLI rejects non-IP inputs.
- A low abuse score does NOT mean the IP is clean — just that it hasn't been widely reported.

## Related skills

- `/lookup-greynoise` — scanner/noise classification for the same IP
- `/lookup-virustotal`, `/lookup-shodan`, `/lookup-otx` — additional IP context
- `/ip-investigation`

## See also

- Integration setup: `tools/integrations/abuseipdb.md`
- CLI source: `tools/clis/abuseipdb.js`
