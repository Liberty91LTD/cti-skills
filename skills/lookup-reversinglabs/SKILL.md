---
name: lookup-reversinglabs
description: Use when you need authoritative classification, threat-name, MITRE ATT&CK mapping, dynamic-analysis or sandbox results on a file hash, or when you need network threat intelligence for a URL/domain/IP from ReversingLabs Spectra Analyze (A1000). Returns verdict, risk score, AV detection ratio, threat name, behavioural tags, and pivot candidates (parent containers, extracted files, related samples by family). Commonly invoked by /hash-investigation and /malware-analysis. Other agents/skills can chain this for deeper malware enrichment beyond VirusTotal.
metadata:
  version: 1.0.0
  tags: [lookup, threat-intel, malware-analysis, sandbox]
  api: reversinglabs
  default_source_reliability: A
  default_information_credibility: 2
---

# lookup-reversinglabs

Queries ReversingLabs Spectra Analyze (the A1000 appliance API) for authoritative classification, full enrichment reports, sandbox behaviour, MITRE ATT&CK mappings, and network indicator reputation. Retrieval only — do not interpret, assess, or conclude. The invoking skill or agent reasons about the result.

## When to invoke

- User asks to check a hash against ReversingLabs / A1000 / Spectra Analyze
- VirusTotal returned thin signal on a hash and you need a vendor-validated verdict
- Investigation needs MITRE ATT&CK technique coverage from a sample's behaviour
- Need parent/child relationships (which container did this drop from? what was unpacked?) for pivoting
- Want to find sibling samples by threat name or AV-detection signature (`/lookup-reversinglabs search`)
- Need network reputation on a URL, domain, or IP from RL's malware-analysis corpus
- Submitting a sample for fresh static + dynamic analysis (slower; produces a full TitaniumCore + sandbox report)

## How to invoke

One CLI: a Python wrapper around the official `reversinglabs-sdk-py3`. Self-bootstraps a private venv at `tools/clis/.venv-reversinglabs/` on first run; no global install. The SDK exchanges your username + password for a session token via `/api-token-auth/` automatically.

```bash
# Hash classification — fast verdict + AV detection
python3 tools/clis/reversinglabs.py hash <hash> [--av-scanners] [--ticloud]

# Full enrichment report (default detailed; pass --summary for the lighter shape)
python3 tools/clis/reversinglabs.py report <hash> [--summary|--detailed] [--fields F1,F2,...]

# File / URL submission (use --wait to block until analysis completes)
python3 tools/clis/reversinglabs.py submit-file <path> [--wait] [--rl-cloud-sandbox windows10]
python3 tools/clis/reversinglabs.py submit-url <url> [--wait] [--crawler local|tcb|cape|fireeye|vmray]

# Network threat intelligence (no submission — reads existing corpus)
python3 tools/clis/reversinglabs.py url <url>
python3 tools/clis/reversinglabs.py domain <domain>
python3 tools/clis/reversinglabs.py ip <ip> [--pivot files,domains,urls] [--max-results 50]

# Advanced search — pivot by threat name, classification, AV signature
python3 tools/clis/reversinglabs.py search "<query>" [--ticloud] [--max-results 100]

# Parent / child sample relationships
python3 tools/clis/reversinglabs.py containers <hash>
python3 tools/clis/reversinglabs.py extracted <hash> [--max-results 200]

# Read-only: which samples matched a YARA ruleset
python3 tools/clis/reversinglabs.py yara-matches <ruleset_name> [--max-results 200]
```

All subcommands accept `--dry-run` to preview the request plan without spending an API call. All exit code 2 if `$REVERSINGLABS_USER` or `$REVERSINGLABS_PASSWORD` is unset (when not in dry-run). Report missing credentials; do not fabricate.

### Examples

```bash
# 1) Fast verdict on a hash, including TitaniumCloud reputation
python3 tools/clis/reversinglabs.py hash 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 \
  --av-scanners --ticloud

# 2) Full enrichment incl. MITRE ATT&CK and network indicators extracted from the sample
python3 tools/clis/reversinglabs.py report 5e884898... --detailed \
  --fields classification,riskscore,classification_result,attack,networkthreatintelligence,tags

# 3) Pivot from a known sample to siblings in the same family
python3 tools/clis/reversinglabs.py search 'threatname:Win32.Ransomware.Lockbit classification:malicious' \
  --max-results 50

# 4) Pivot from an extracted hash to its parent container, then siblings dropped by the same parent
python3 tools/clis/reversinglabs.py containers <child-hash>
python3 tools/clis/reversinglabs.py extracted <parent-hash>

# 5) IP reputation + fan-out to files + domains seen on that IP
python3 tools/clis/reversinglabs.py ip 185.220.101.45 --pivot files,domains,urls --max-results 25
```

### Quota awareness

ReversingLabs does not publicly document per-minute / per-day rate limits for A1000. The API returns **HTTP 429** with a `Retry-After` header when limits are hit. Submission endpoints poll at 2-second intervals up to 10 retries (SDK defaults) before giving up. Each `--pivot` entry is a *separate* API call on top of the base IP report. Use `--dry-run` first when fanning out broadly.

## Response format

The CLI emits JSON to stdout. Skills consuming it should treat it as:

```yaml
source: reversinglabs
operation: hash_classification | report_summary | report_detailed | submit_file | submit_url |
           network_url_report | network_domain_report | network_ip_report |
           advanced_search | containers | extracted_files | yara_matches
indicator: <queried value>
type: hash | url | domain | ip | file | query | ruleset
host: https://a1000.reversinglabs.com
query_time: <ISO8601>
# operation-specific payload — typically the SDK's deserialised JSON body
classification: { ... }   # for `hash`
report: { ... }            # for `report`, `url`, `domain`, `ip`
results: [ ... ]           # for `search`
files | containers: [...]  # for `extracted`, `containers`
```

Common fields inside a detailed `report`:

| Field | Meaning |
|---|---|
| `classification` | Verdict: `malicious` / `suspicious` / `goodware` / `unknown` |
| `riskscore` | Numeric 0–10 risk score |
| `classification_result` | Threat name string (e.g. `Win32.Ransomware.Lockbit`) |
| `av_scanners_summary` | `{scanner_count, scanner_match, scanner_percent}` |
| `av_scanners` | Per-engine scan results |
| `tags` | Analyst + system-applied tags |
| `ticore` | Full TitaniumCore static analysis (format, headers, imports, strings) |
| `attack` | MITRE ATT&CK tactics + techniques mapped from observed behaviour |
| `rl_cloud_sandbox` | Dynamic analysis output |
| `networkthreatintelligence` | Network indicators extracted from the sample |
| `ticloud` | Spectra Intelligence reputation (when `--ticloud`) |

## Rate limits

No public per-minute/day quota. API returns 429 with `Retry-After`. SDK polls submissions with `wait_time_seconds=2`, `retries=10`. Back off and retry on 429.

## Source reliability (Admiralty default)

Default rating for downstream `/score-source`: **A2** (completely reliable, probably true). Vendor-authoritative static + dynamic analysis pipeline; verdicts are well validated against ground truth. A1000 is single-tenant — classification overrides applied by other tenants do not affect this lookup.

**Downgrade to B3** if:
- `classification` is `unknown` or `suspicious` (analyst should still verify)
- Sample is very fresh (<24h since first-seen) — sandbox detonation may have been incomplete
- Dynamic analysis was skipped or errored (no `rl_cloud_sandbox` payload)

**Stay at A2 / consider A1** if:
- `classification` is `malicious` AND `av_scanners_summary.scanner_match >= 5` AND sandbox produced behavioural evidence
- Threat name maps to a known family with public reporting

## Related skills

- `/lookup-virustotal` — community-aggregated detection; complements RL's authoritative verdict
- `/lookup-otx` — community pulse context for the same indicator
- `/malware-analysis` — methodology for interpreting static + dynamic analysis output
- `/hash-investigation` — chains this lookup with VirusTotal and OTX
- `/score-source` — apply Admiralty rating to the result

## See also

- Integration setup: `tools/integrations/reversinglabs.md`
- Python CLI source: `tools/clis/reversinglabs.py`
- Companion API reference (non-invokable): `skills/reversinglabs-api/SKILL.md`
- Official product docs: https://docs.reversinglabs.com/SpectraAnalyze/
- SDK source: https://github.com/reversinglabs/reversinglabs-sdk-py3
