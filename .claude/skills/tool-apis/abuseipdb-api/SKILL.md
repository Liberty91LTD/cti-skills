---
name: abuseipdb-api
description: AbuseIPDB API reference. IP reputation and abuse report lookups.
user-invocable: false
metadata:
  version: 1.0.0
---

# AbuseIPDB API v2

## Base URL
`https://api.abuseipdb.com/api/v2`

## Authentication
Header: `Key: $ABUSEIPDB_API_KEY`
Also: `Accept: application/json`

## Rate Limits
- Free: 1000 checks/day, 500 reports/day
- Premium: Higher limits

## Key Endpoints

### Check IP
```bash
curl -s "https://api.abuseipdb.com/api/v2/check" \
  -G -d "ipAddress={ip}" -d "maxAgeInDays=90" -d "verbose" \
  -H "Key: $ABUSEIPDB_API_KEY" -H "Accept: application/json"
```
**Useful fields:**
- `data.abuseConfidenceScore` — 0-100 abuse confidence
- `data.totalReports` — number of abuse reports
- `data.numDistinctUsers` — unique reporters
- `data.lastReportedAt` — most recent report
- `data.isp` — ISP name
- `data.usageType` — usage type (Data Center, ISP, etc.)
- `data.countryCode` — country
- `data.domain` — associated domain
- `data.isTor` — Tor exit node flag
- `data.reports[]` — individual reports (with `verbose`)

### Check Network (CIDR)
```bash
curl -s "https://api.abuseipdb.com/api/v2/check-block" \
  -G -d "network={cidr}" -d "maxAgeInDays=90" \
  -H "Key: $ABUSEIPDB_API_KEY" -H "Accept: application/json"
```

## Confidence Score Interpretation
| Score | Meaning |
|-------|---------|
| 0 | No reports, clean |
| 1-25 | Low confidence of abuse |
| 26-50 | Moderate — some reports |
| 51-75 | High — significant abuse reports |
| 76-100 | Very high — widely reported as abusive |

## Response Summary Format
```yaml
ip: <IP>
abuse_confidence: <0-100>
total_reports: <number>
distinct_reporters: <number>
last_reported: <date>
isp: <ISP>
usage_type: <type>
country: <country>
is_tor: <true/false>
verdict: clean|low-risk|suspicious|malicious
```
