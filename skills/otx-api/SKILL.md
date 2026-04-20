---
name: otx-api
description: AlienVault OTX API reference. Community threat intelligence pulses and indicator lookups.
user-invocable: false
metadata:
  version: 1.0.0
---

# AlienVault OTX API

## Base URL
`https://otx.alienvault.com/api/v1`

## Authentication
Header: `X-OTX-API-KEY: $OTX_API_KEY`

## Rate Limits
- 10,000 requests/hour

## Key Endpoints

### IPv4 Indicator
```bash
# General info
curl -s "https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general" \
  -H "X-OTX-API-KEY: $OTX_API_KEY"

# Reputation
curl -s "https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/reputation" \
  -H "X-OTX-API-KEY: $OTX_API_KEY"

# Passive DNS
curl -s "https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/passive_dns" \
  -H "X-OTX-API-KEY: $OTX_API_KEY"

# Associated malware
curl -s "https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/malware" \
  -H "X-OTX-API-KEY: $OTX_API_KEY"
```

### Domain Indicator
```bash
curl -s "https://otx.alienvault.com/api/v1/indicators/domain/{domain}/general" \
  -H "X-OTX-API-KEY: $OTX_API_KEY"
```
Sections: `/general`, `/geo`, `/malware`, `/url_list`, `/passive_dns`, `/whois`

### File Hash Indicator
```bash
curl -s "https://otx.alienvault.com/api/v1/indicators/file/{hash}/general" \
  -H "X-OTX-API-KEY: $OTX_API_KEY"
```
Sections: `/general`, `/analysis`

### URL Indicator
```bash
curl -s "https://otx.alienvault.com/api/v1/indicators/url/{url}/general" \
  -H "X-OTX-API-KEY: $OTX_API_KEY"
```

### Search Pulses
```bash
curl -s "https://otx.alienvault.com/api/v1/search/pulses?q={query}" \
  -H "X-OTX-API-KEY: $OTX_API_KEY"
```

## Key Response Fields
- `pulse_info.count` — number of pulses referencing this indicator
- `pulse_info.pulses[]` — pulse details (name, description, tags, TLP, created)
- `reputation` — community reputation score
- `validation[]` — validation results from OTX
- `passive_dns[]` — historical DNS resolutions

## CTI Value
OTX provides community-sourced intelligence. High pulse count = widely reported indicator. Useful for:
- Corroboration with other sources
- Discovering related indicators via pulse associations
- Historical passive DNS data
- Community context (pulse descriptions explain what the indicator relates to)

## Response Summary Format
```yaml
indicator: <value>
type: <ip|domain|hash|url>
pulse_count: <number>
reputation: <score>
key_pulses:
  - name: <pulse name>
    tags: [<tags>]
    created: <date>
related_indicators: [<list>]
passive_dns: [<domain/IP resolutions>]
verdict: known-malicious|suspicious|clean|unknown
```
