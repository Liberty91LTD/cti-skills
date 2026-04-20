---
name: virustotal-api
description: VirusTotal API v3 reference. File, IP, domain, and URL analysis endpoints.
user-invocable: false
metadata:
  version: 1.0.0
---

# VirusTotal API v3

## Base URL
`https://www.virustotal.com/api/v3`

## Authentication
Header: `x-apikey: $VIRUSTOTAL_API_KEY`

Check for key: `echo $VIRUSTOTAL_API_KEY`
If empty, inform the user to run `scripts/setup.sh` or set the environment variable.

## Rate Limits
- Free: 4 requests/minute, 500/day, 15.5K/month
- Premium: 1000 requests/minute

## Key Endpoints

### File Analysis
```bash
# Lookup by hash (MD5, SHA-1, SHA-256)
curl -s "https://www.virustotal.com/api/v3/files/{hash}" \
  -H "x-apikey: $VIRUSTOTAL_API_KEY"
```
**Useful response fields:**
- `data.attributes.last_analysis_stats` — detection counts (malicious, suspicious, undetected)
- `data.attributes.popular_threat_classification` — malware family
- `data.attributes.names` — file names
- `data.attributes.type_description` — file type
- `data.attributes.size` — file size
- `data.attributes.tags` — behavioral tags
- `data.attributes.sandbox_verdicts` — sandbox results

### IP Address
```bash
curl -s "https://www.virustotal.com/api/v3/ip_addresses/{ip}" \
  -H "x-apikey: $VIRUSTOTAL_API_KEY"
```
**Useful fields:** `last_analysis_stats`, `as_owner`, `country`, `reputation`, `last_https_certificate`

**Relationships** (communicating files, downloaded files, URLs):
```bash
curl -s "https://www.virustotal.com/api/v3/ip_addresses/{ip}/communicating_files?limit=10" \
  -H "x-apikey: $VIRUSTOTAL_API_KEY"
```

### Domain
```bash
curl -s "https://www.virustotal.com/api/v3/domains/{domain}" \
  -H "x-apikey: $VIRUSTOTAL_API_KEY"
```
**Useful fields:** `last_analysis_stats`, `registrar`, `creation_date`, `last_dns_records`, `reputation`, `categories`

### URL
URLs must be base64-encoded (without trailing `=`):
```bash
URL_ID=$(echo -n "https://example.com/path" | base64 | tr -d '=')
curl -s "https://www.virustotal.com/api/v3/urls/$URL_ID" \
  -H "x-apikey: $VIRUSTOTAL_API_KEY"
```

## Common Query Patterns

### Quick reputation check (any indicator type)
Return a summary: detection ratio, community score, key context.

### File behavior analysis
```bash
curl -s "https://www.virustotal.com/api/v3/files/{hash}/behaviours" \
  -H "x-apikey: $VIRUSTOTAL_API_KEY"
```

### Search for related indicators
```bash
curl -s "https://www.virustotal.com/api/v3/intelligence/search?query={query}" \
  -H "x-apikey: $VIRUSTOTAL_API_KEY"
```
Note: Intelligence search requires premium API.

## Response Summary Format

Return results as:
```yaml
indicator: <value>
type: <ip|domain|hash|url>
detection_ratio: X/Y
community_score: <number>
verdict: malicious|suspicious|clean|unknown
key_findings:
  - <finding 1>
  - <finding 2>
raw_api_response: <truncated key fields>
```
