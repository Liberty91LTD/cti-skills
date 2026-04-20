---
name: censys-api
description: Censys API v2 reference. Host reconnaissance and certificate data.
user-invocable: false
metadata:
  version: 1.0.0
---

# Censys API v2

## Base URL
`https://search.censys.io/api/v2`

## Authentication
Basic Auth: `$CENSYS_API_ID:$CENSYS_API_SECRET`

```bash
curl -s "https://search.censys.io/api/v2/hosts/{ip}" \
  -u "$CENSYS_API_ID:$CENSYS_API_SECRET"
```

## Rate Limits
- Free: 250 queries/month, 5 results/query
- Paid: Higher limits based on plan

**Important:** Free tier is very limited. Use selectively — prioritise high-value lookups.

## Key Endpoints

### View Host
```bash
curl -s "https://search.censys.io/api/v2/hosts/{ip}" \
  -u "$CENSYS_API_ID:$CENSYS_API_SECRET"
```
**Useful fields:**
- `result.services[]` — port, service_name, transport_protocol, banner
- `result.services[].tls.certificates` — TLS certificate chain
- `result.autonomous_system` — ASN info
- `result.location` — geographic location
- `result.operating_system` — OS detection
- `result.last_updated_at` — scan freshness

### Search Hosts
```bash
curl -s "https://search.censys.io/api/v2/hosts/search?q={query}" \
  -u "$CENSYS_API_ID:$CENSYS_API_SECRET"
```
**Search syntax:** `services.port: 443 AND services.tls.certificates.leaf_data.subject.common_name: example.com`

### View Certificate
```bash
curl -s "https://search.censys.io/api/v2/certificates/{fingerprint}" \
  -u "$CENSYS_API_ID:$CENSYS_API_SECRET"
```

## Common Search Queries
- `ip: {ip}` — specific host
- `services.tls.certificates.leaf_data.subject.common_name: {domain}` — hosts with cert for domain
- `services.http.response.body_hash: {hash}` — hosts serving same content
- `services.jarm.fingerprint: {jarm}` — hosts with same JARM fingerprint (C2 detection)
- `labels: {label}` — Censys-labeled hosts

## CTI Value
Censys excels at:
- Certificate transparency analysis (finding related infrastructure)
- JARM fingerprinting (identifying C2 frameworks)
- Service banner analysis
- Historical infrastructure changes

## Response Summary Format
```yaml
ip: <IP>
services:
  - port: <port>
    service: <name>
    banner: <truncated>
certificates:
  - subject_cn: <common name>
    issuer: <issuer>
    valid_from: <date>
    valid_to: <date>
autonomous_system:
  asn: <number>
  name: <name>
location:
  country: <country>
  city: <city>
last_updated: <date>
```
