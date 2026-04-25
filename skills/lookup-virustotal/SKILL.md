---
name: lookup-virustotal
description: Use when you need to check an IP, domain, file hash, or URL against VirusTotal's reputation database. Returns detection ratio, verdict, community score, and key findings. Commonly invoked by investigation skills (/ip-investigation, /domain-investigation, /hash-investigation, /url-investigation) and by analysts enriching IOCs. Other agents/skills can chain this for VirusTotal enrichment.
metadata:
  version: 1.0.0
  tags: [lookup, threat-intel, reputation]
  api: virustotal
  default_source_reliability: B
  default_information_credibility: 2
---

# lookup-virustotal

Queries VirusTotal API v3 for reputation data on IPs, domains, file hashes, and URLs. Retrieval only — do not interpret, assess, or conclude. The invoking skill or agent reasons about the result.

## When to invoke

- User asks to check an IP, domain, hash, or URL against VirusTotal
- Investigation skill needs reputation context for a collected indicator
- IOC enrichment pipeline is deduplicating + scoring a batch

## How to invoke

Two CLIs are provided. Pick by capability needed:

### Basic lookup — Node CLI (zero deps)

```bash
node tools/clis/virustotal.js <type> <value>
# where <type> is one of: ip, domain, hash, url
```

Hits the basic object endpoint only and distils to a verdict. Best for fast retrieval inside an investigation chain.

### Full surface — Python CLI (stdlib only)

```bash
python3 tools/clis/virustotal.py file <hash> [--relationships R1,R2] [--limit N]
python3 tools/clis/virustotal.py ip <ip> [--relationships R1,R2] [--limit N]
python3 tools/clis/virustotal.py domain <domain> [--relationships R1,R2] [--limit N]
python3 tools/clis/virustotal.py url <url> [--relationships R1,R2] [--limit N]
python3 tools/clis/virustotal.py submit-url <url>
python3 tools/clis/virustotal.py comments <type> <id>
python3 tools/clis/virustotal.py search <query>     # Intel — premium
```

Stdlib only — no install, no venv.

Capabilities the Node CLI doesn't have:
- **Relationship traversal** — the killer feature for pivoting. For an IP, fetch `communicating_files`, `downloaded_files`, `resolutions`, `urls`, `related_threat_actors`, `historical_whois`. For a file: `contacted_ips`, `contacted_domains`, `dropped_files`, `similar_files`, `behaviours`. For a domain: `subdomains`, `siblings`, `resolutions`. For a URL: `contacted_ips`, `contacted_domains`, `last_serving_ip_address`. Each `--relationships` entry is a separate API request — be deliberate about which to pull.
- **URL submission** (`submit-url`) — push a URL into the analysis queue; returns an analysis ID.
- **Comments** — community comments on any object.
- **Intel search** — VT Intelligence query language (`type:peexe size:1mb+ p:5+`). Premium endpoint; will 403 on free.

Examples:
```bash
# Pivot from a malicious IP to communicating samples and resolutions
python3 tools/clis/virustotal.py ip 185.220.101.45 --relationships communicating_files,resolutions

# Get a hash plus its sandbox behaviours and contacted infrastructure
python3 tools/clis/virustotal.py file 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 \
  --relationships behaviours,contacted_ips,contacted_domains,dropped_files

# Submit a suspicious URL for fresh analysis
python3 tools/clis/virustotal.py submit-url "http://suspicious-site.example/login"
```

Both CLIs accept `--dry-run` to preview the request(s) without spending quota. Both exit code 2 if `$VIRUSTOTAL_API_KEY` is unset (when not in dry-run). Report missing key; do not fabricate.

### Quota awareness

Free tier is **4 req/min, 500/day**. Each `--relationships` entry is a *separate* API call on top of the base lookup. A single `ip 1.2.3.4 --relationships a,b,c,d` burns 5 requests. Use `--dry-run` first to count calls before live runs.

## Response format

The CLI returns JSON. Skills consuming it should treat it as:

```yaml
source: virustotal
indicator: <queried value>
type: ip | domain | hash | url
query_time: <ISO8601>
detection_ratio: <malicious>/<total>
community_score: <number>
verdict: malicious | suspicious | clean | unknown
key_findings:
  - <finding 1>
  - <finding 2>
additional_context:
  <relevant fields from API response>
```

## Rate limits

Free tier: 4 req/min, 500/day, 15.5k/month. Premium: 1000 req/min. Back off on 429.

## Source reliability (Admiralty default)

Default rating for downstream `/score-source`: **B2** (usually reliable, probably true). Community-driven detection aggregator; high-volume but vendor signals vary in quality. Downgrade to **C3** if only 1-2 engines detect.

## Related skills

- `/lookup-otx` — community pulse context for the same indicator
- `/lookup-urlscan` — live scan of URLs/domains
- `/lookup-abuseipdb` — IP abuse reports
- `/score-source` — apply Admiralty rating to the result
- `/ip-investigation`, `/domain-investigation`, `/hash-investigation`, `/url-investigation` — skills that chain this lookup

## See also

- Integration setup: `tools/integrations/virustotal.md`
- Node CLI source: `tools/clis/virustotal.js`
- Python CLI source: `tools/clis/virustotal.py`
- Official API reference: https://gtidocs.virustotal.com/reference/api-responses
- Endpoint docs: https://docs.virustotal.com/reference/overview
