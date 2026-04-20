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

Shell out to the zero-dep CLI:

```bash
node tools/clis/virustotal.js <type> <value>
# where <type> is one of: ip, domain, hash, url
```

Examples:
```bash
node tools/clis/virustotal.js ip 203.0.113.42
node tools/clis/virustotal.js domain example.com
node tools/clis/virustotal.js hash 44d88612fea8a8f36de82e1278abb02f
node tools/clis/virustotal.js url "https://example.com/path"
```

Use `--dry-run` to preview the API request without spending quota.

If `$VIRUSTOTAL_API_KEY` is unset, the CLI exits with code 2 and prints a setup pointer. Report the missing key to the user or the invoking skill — do not fabricate results.

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
- CLI source: `tools/clis/virustotal.js`
