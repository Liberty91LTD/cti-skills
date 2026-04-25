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

Two CLIs are provided. Pick by capability needed:

### Basic submit + cached domain search — Node CLI (zero deps)

```bash
node tools/clis/urlscan.js url "<url>"
node tools/clis/urlscan.js domain <domain>
```

Single-shot URL submit (with built-in 30s wait + 5x10s polling) or domain search. Best for fast retrieval inside an investigation chain.

### Full API surface — Python CLI (stdlib only)

```bash
python3 tools/clis/urlscan.py submit <url> [--visibility V] [--country CC]
                                            [--tags t1,t2] [--user-agent UA]
                                            [--referer R] [--wait]
python3 tools/clis/urlscan.py result <uuid>
python3 tools/clis/urlscan.py search "<lucene-query>" [--size N]
python3 tools/clis/urlscan.py quota
python3 tools/clis/urlscan.py screenshot <uuid> [--out FILE]
python3 tools/clis/urlscan.py dom <uuid> [--out FILE]
```

Stdlib only — no install, no venv.

Capabilities the Node CLI doesn't have:
- **Lucene-style search** — the killer pivot. Query against URLScan's full database: `page.domain`, `page.url`, `asn`, `hash`, `filename`, `verdicts.overall.malicious`, `task.tags`, `page.country`, etc. Combine with AND/OR/NOT.
- **Result by UUID** — fetch a known scan without re-submitting.
- **Quota check** — see remaining scan/search/retrieve quota before committing to a batch.
- **Screenshot download** (`screenshot --out img.png`) — pull the rendered page screenshot.
- **DOM download** (`dom --out page.html`) — pull captured HTML for offline analysis.
- **Submission options** — country, custom user-agent, custom referer, tags.

Lucene search examples:
```bash
# All public scans of a domain in the last 30 days
python3 tools/clis/urlscan.py search "page.domain:malicious.example AND date:>now-30d"

# Phishing kits hosted on Russian ASNs
python3 tools/clis/urlscan.py search "task.tags:phishing AND page.country:RU"

# Pivot by favicon hash (a strong infrastructure fingerprint)
python3 tools/clis/urlscan.py search "hash:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"

# All scans hitting a specific IP
python3 tools/clis/urlscan.py search "page.ip:185.220.101.45"
```

Both CLIs accept `--dry-run`. Both exit code 2 if `$URLSCAN_API_KEY` is unset (when not in dry-run). Report missing key; do not fabricate.

### Visibility — non-negotiable default

**Always submit with `unlisted` visibility unless the user explicitly opts in to `public`.** Public submissions appear on URLScan's global feed and tip off threat actors that you're investigating their infrastructure. Both CLIs default to `unlisted`. The Python CLI also supports `private` (Pro tier).

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
- Node CLI source: `tools/clis/urlscan.js`
- Python CLI source: `tools/clis/urlscan.py`
- Official API docs: https://docs.urlscan.io/apis/urlscan-openapi/live-scanning
- Search query syntax: https://urlscan.io/search/
