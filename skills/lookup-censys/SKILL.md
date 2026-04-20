---
name: lookup-censys
description: Use when you need deep host + certificate reconnaissance for an IP or need to run a Censys search query. Returns services, TLS certificates, ASN, and location. Free tier is severely limited (250 queries/month) — use sparingly. Retrieval only.
metadata:
  version: 1.0.0
  tags: [lookup, threat-intel, reconnaissance, quota-limited]
  api: censys
  default_source_reliability: A
  default_information_credibility: 2
---

# lookup-censys

Queries Censys for host and certificate reconnaissance on IPs, or runs a Censys Search query. Retrieval only. Quota-aware — free tier is 250 queries/month.

## When to invoke

- Shodan wasn't sufficient and deeper host data is needed
- TLS certificate pivoting (find other hosts sharing a cert)
- Specific Censys Search query required

**Do NOT invoke for:**
- Bulk enrichment (will exhaust quota)
- IPs you can get from Shodan first

## How to invoke

```bash
node tools/clis/censys.js ip <ip>
node tools/clis/censys.js search "<query>"      # Censys Search syntax
```

Use `--dry-run` to preview and avoid spending quota.

If `$CENSYS_API_ID` or `$CENSYS_API_SECRET` is unset, the CLI exits with code 2.

## Response format

```yaml
source: censys
indicator: <IP or search query>
query_time: <ISO8601>
services:
  - port: <port>
    service: <name>
    banner: <truncated>
certificates:
  - subject_cn: <common name>
    issuer: <issuer>
    sha256: <fingerprint>
autonomous_system:
  asn: <number>
  name: <name>
location:
  country: <country>
  city: <city>
last_updated: <date>
```

## Rate limits

Free tier: **250 queries/month** (very limited). Research tier: 10k/month. Paid: unlimited.

## Source reliability (Admiralty default)

Default rating for downstream `/score-source`: **A2** (completely reliable, probably true). Censys is an authoritative internet-scan dataset with strong data hygiene.

## Operational notes

- **Quota conservation is critical.** Before invoking, consider whether Shodan can answer the question first.
- For certificate pivoting specifically, Censys is often the right first call — Shodan has weaker cert data.
- Uses HTTP Basic Auth with `$CENSYS_API_ID` and `$CENSYS_API_SECRET`.

## Related skills

- `/lookup-shodan` — lighter-weight alternative with higher rate limits
- `/lookup-virustotal` — reputation, not reconnaissance
- `/ip-investigation`

## See also

- Integration setup: `tools/integrations/censys.md`
- CLI source: `tools/clis/censys.js`
