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

Two CLIs are provided. Pick by capability needed:

### Basic check — Node CLI (zero deps)

```bash
node tools/clis/abuseipdb.js ip <ip>
```

Hits the `/check` endpoint with a 90-day window. Best for fast retrieval inside an investigation chain.

### Full read-only suite — Python CLI (stdlib only)

```bash
python3 tools/clis/abuseipdb.py check <ip> [--max-age-in-days N] [--verbose]
python3 tools/clis/abuseipdb.py reports <ip> [--per-page N] [--page N]
python3 tools/clis/abuseipdb.py check-block <cidr> [--max-age-in-days N]
python3 tools/clis/abuseipdb.py blacklist [--confidence-min N] [--limit N]
                                          [--ip-version 4|6]
                                          [--only-countries CC,CC]
                                          [--except-country CC,CC]
```

No external deps — Python 3 stdlib only, no venv needed.

Capabilities the Node CLI doesn't have:
- **Verbose check** (`check --verbose`) — full per-report list including category, comment, reporter ID, country.
- **Reports endpoint** — paginated raw report history (uses zero `check`-quota).
- **CIDR-block check** (`check-block`) — reputation summary across an entire network range. Useful for triaging suspicious /24s, hosting providers, ASN sub-ranges.
- **Blacklist download** — bulk pull of high-confidence abuse IPs filtered by country / IP version / confidence threshold. Useful for ingesting into block lists.

Examples:
```bash
# Detailed report list for a suspect IP
python3 tools/clis/abuseipdb.py check 185.220.101.45 --verbose

# What's been reported in this /24 in the last 30 days?
python3 tools/clis/abuseipdb.py check-block 185.220.101.0/24

# Pull RU-only IPs with 90%+ confidence, max 500
python3 tools/clis/abuseipdb.py blacklist --only-countries RU --confidence-min 90 --limit 500
```

Both CLIs accept `--dry-run` to preview the request without calling the API. Both exit code 2 if `$ABUSEIPDB_API_KEY` is unset (when not in dry-run). Report missing key; do not fabricate.

## Write endpoints (deferred)

AbuseIPDB also exposes `/report`, `/bulk-report`, and `/clear-address` for contributing reports back. These are **NOT** wired into either CLI by default — this skill is retrieval-focused. To contribute reports, use the AbuseIPDB web UI or write a deliberate purpose-built script with a confirmation flow.

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
- Node CLI source: `tools/clis/abuseipdb.js`
- Python CLI source: `tools/clis/abuseipdb.py`
- Official API docs: https://docs.abuseipdb.com/
