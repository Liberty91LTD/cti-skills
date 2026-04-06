---
name: greynoise-api
description: GreyNoise API reference. Internet scanner/noise classification for IPs.
user-invocable: false
metadata:
  version: 1.0.0
---

# GreyNoise API

## Base URL
- Community: `https://api.greynoise.io/v3/community`
- Enterprise: `https://api.greynoise.io/v3`

## Authentication
Header: `key: $GREYNOISE_API_KEY`

## Rate Limits
- Community (free): 50 requests/day
- Enterprise: Based on plan

## Key Endpoints

### Community IP Lookup (Free)
```bash
curl -s "https://api.greynoise.io/v3/community/{ip}" \
  -H "key: $GREYNOISE_API_KEY"
```
**Response fields:**
- `noise` — true if IP is a known internet scanner
- `riot` — true if IP belongs to a known benign service (CDN, DNS, etc.)
- `classification` — benign|malicious|unknown
- `name` — actor name if identified
- `last_seen` — last observation date
- `message` — human-readable summary

### Enterprise Context (Paid)
```bash
curl -s "https://api.greynoise.io/v3/noise/context/{ip}" \
  -H "key: $GREYNOISE_API_KEY"
```
Additional fields: `tags`, `cve`, `os`, `ports`, `raw_data`

## Classification Meaning

| Classification | Meaning | Action |
|---------------|---------|--------|
| `benign` + `noise:true` | Known benign scanner (Shodan, Censys, etc.) | Likely false positive — deprioritise |
| `malicious` + `noise:true` | Known malicious scanner | Real threat, but opportunistic, not targeted |
| `unknown` + `noise:true` | Unclassified scanner | Investigate further |
| `noise:false` + `riot:false` | Not a known scanner | May be targeted — investigate |
| `riot:true` | Known benign service | Definitely deprioritise |

## CTI Value
GreyNoise answers: "Is this IP scanning the whole internet, or is it specifically targeting us?"
- If `noise:true` → opportunistic, not targeted
- If `noise:false` → potentially targeted, higher priority

## Response Summary Format
```yaml
ip: <IP>
noise: <true/false>
riot: <true/false>
classification: benign|malicious|unknown
name: <actor name or "unknown">
last_seen: <date>
message: <summary>
verdict: benign-scanner|malicious-scanner|not-scanner|benign-service
```
