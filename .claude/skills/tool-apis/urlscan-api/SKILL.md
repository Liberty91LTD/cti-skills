---
name: urlscan-api
description: URLScan.io API reference. URL submission, scanning, and result retrieval.
user-invocable: false
metadata:
  version: 1.0.0
---

# URLScan.io API

## Base URL
`https://urlscan.io/api/v1`

## Authentication
Header: `API-Key: $URLSCAN_API_KEY`

## Rate Limits
- Free: 100 scans/day, 100 searches/day
- Paid: Higher limits based on plan

## Key Endpoints

### Submit URL for scanning
```bash
curl -s -X POST "https://urlscan.io/api/v1/scan/" \
  -H "API-Key: $URLSCAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "visibility": "unlisted"}'
```
**Response:** `{"uuid": "...", "api": "https://urlscan.io/api/v1/result/UUID/"}`

**Important:** Scan is async. Wait ~30 seconds before retrieving results. Poll the result URL until status is not 404.

### Retrieve scan results
```bash
curl -s "https://urlscan.io/api/v1/result/{uuid}/" \
  -H "API-Key: $URLSCAN_API_KEY"
```
**Useful response fields:**
- `verdicts.overall` — malicious/benign score
- `page.url` — final URL after redirects
- `page.ip` — IP address resolved
- `page.country` — hosting country
- `page.server` — web server
- `lists.ips` — all IPs contacted
- `lists.domains` — all domains contacted
- `lists.urls` — all URLs loaded
- `stats.tlsPercentage` — TLS usage
- `task.screenshotURL` — screenshot of page

### Search existing scans
```bash
curl -s "https://urlscan.io/api/v1/search/?q=domain:example.com" \
  -H "API-Key: $URLSCAN_API_KEY"
```
**Search operators:** `domain:`, `ip:`, `server:`, `filename:`, `hash:`, `page.url:`

## Scan Flow
1. Submit URL → get UUID
2. Wait 30 seconds
3. Poll result endpoint (retry on 404, max 5 attempts with 10s delay)
4. Extract and return key findings

## Response Summary Format
```yaml
url: <scanned URL>
final_url: <after redirects>
verdict: malicious|suspicious|benign|unknown
ip: <resolved IP>
country: <hosting country>
technologies: [<detected technologies>]
domains_contacted: [<list>]
ips_contacted: [<list>]
screenshot: <URL>
```
