---
name: lookup-urlscan
description: Use when you need to submit a URL for live scanning via URLScan.io and retrieve results, or search existing scans for a domain. Returns verdict, final URL after redirects, resolved IP, contacted domains/IPs, and screenshot URL. Commonly invoked by /url-investigation and /domain-investigation.
metadata:
  version: 1.0.0
  tags: [lookup, threat-intel, scanning]
  api: urlscan
  default_source_reliability: B
  default_information_credibility: 2
---

# lookup-urlscan

Submits URLs to URLScan.io for live scanning and retrieves results. For domains, searches existing scans first (uses cached scan if <24h old, else submits new one). Retrieval only — do not interpret.

## When to invoke

- User asks to scan a URL or check what a domain renders as
- Investigation skill needs redirect chain, contacted infra, or a visual snapshot
- Triaging a potentially malicious URL before clicking

## How to invoke

```bash
node tools/clis/urlscan.js url "<url>"
node tools/clis/urlscan.js domain <domain>
```

Use `--dry-run` to preview. Default `visibility` is `unlisted` to avoid exposing the IOC publicly. Override with `--visibility public` only if the user explicitly wants public listing.

The CLI handles scan submission → 30s wait → result polling (max 5 retries, 10s delay). Returns after ~45-90s on first submission; instant if cached.

If `$URLSCAN_API_KEY` is unset, the CLI exits with code 2.

## Response format

```yaml
source: urlscan
indicator: <URL or domain>
query_time: <ISO8601>
verdict: <from verdicts.overall>
final_url: <after redirects>
ip: <resolved IP>
country: <hosting country>
domains_contacted: [<list>]
ips_contacted: [<list>]
screenshot_url: <URL>
scan_url: <urlscan.io result page>
key_findings:
  - <finding>
```

## Rate limits

Free tier: 100 scans/day, 5000 searches/month.

## Source reliability (Admiralty default)

Default rating for downstream `/score-source`: **B2** (usually reliable, probably true). Live-scan evidence is strong; verdicts can be noisy — downgrade to **C3** if verdict is ambiguous.

## Operational notes

- **Always use `unlisted` visibility by default** — public submissions expose the indicator and can tip off threat actors.
- Don't submit if the URL is in the user's own infrastructure unless they explicitly request it.

## Related skills

- `/lookup-virustotal`, `/lookup-otx` — reputation/community context
- `/score-source` — apply Admiralty rating
- `/url-investigation`, `/domain-investigation`

## See also

- Integration setup: `tools/integrations/urlscan.md`
- CLI source: `tools/clis/urlscan.js`
