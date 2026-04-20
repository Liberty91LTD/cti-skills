---
name: shodan-api
description: Shodan API reference. Host reconnaissance, port scanning, and vulnerability data.
user-invocable: false
metadata:
  version: 1.0.0
---

# Shodan API

## Base URL
`https://api.shodan.io`

## Authentication
Query parameter: `?key=$SHODAN_API_KEY`

## Rate Limits
- Free: 1 request/second, 100 results/search
- Paid: Higher limits and more features

## Key Endpoints

### Host Information
```bash
curl -s "https://api.shodan.io/shodan/host/{ip}?key=$SHODAN_API_KEY"
```
**Useful fields:**
- `ip_str` — IP address
- `ports` — open ports
- `data[]` — service banners per port (product, version, transport)
- `os` — detected OS
- `hostnames` — reverse DNS
- `vulns` — CVE list (paid feature)
- `org` — organisation
- `isp` — ISP
- `country_code` — country
- `last_update` — last scan date

### DNS Resolution
```bash
curl -s "https://api.shodan.io/dns/resolve?hostnames={domain}&key=$SHODAN_API_KEY"
```

### Reverse DNS
```bash
curl -s "https://api.shodan.io/dns/reverse?ips={ip}&key=$SHODAN_API_KEY"
```

### Search
```bash
curl -s "https://api.shodan.io/shodan/host/search?query={query}&key=$SHODAN_API_KEY"
```
**Search filters:** `port:`, `org:`, `country:`, `product:`, `version:`, `ssl.cert.subject.cn:`, `http.title:`, `vuln:`

### API Info (check credits)
```bash
curl -s "https://api.shodan.io/api-info?key=$SHODAN_API_KEY"
```

## Common Queries
- `ssl.cert.subject.cn:example.com` — find hosts with specific SSL certificate
- `org:"Target Org"` — find hosts belonging to an org
- `product:"Apache" port:443 country:RU` — specific service in a country
- `vuln:CVE-2024-12345` — hosts vulnerable to specific CVE (paid)

## Response Summary Format
```yaml
ip: <IP>
hostnames: [<list>]
org: <organisation>
isp: <ISP>
country: <country>
os: <operating system>
open_ports: [<port list>]
services:
  - port: 80
    product: nginx
    version: 1.18.0
vulnerabilities: [<CVE list>]  # paid only
last_update: <date>
```
