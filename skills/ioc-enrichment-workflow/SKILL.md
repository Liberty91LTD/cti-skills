---
name: ioc-enrichment-workflow
description: Workflow for enriching raw IOCs. Routes each IOC type to the appropriate /lookup-* skills, optionally correlates against MISP, and synthesises a single enrichment record per indicator. Use when the user has a batch of raw IOCs to process before triage or before pushing into a sharing platform.
user-invocable: false
metadata:
  version: 2.1.0
  tags: [enrichment, workflow, composition]
---

# IOC Enrichment Workflow

This workflow defines how to enrich raw indicators of compromise by routing them to the appropriate `/lookup-*` skills and synthesising results.

**Seeding the queue (optional):** when you don't already have a batch but want fresh leads, `/lookup-crowdstrike indicators --malicious --since 7d [--type … | --actor …]` returns the latest high-confidence CrowdStrike IOCs (newest-first). Feed the returned indicators into the per-type routing below to enrich each. Requires CrowdStrike credentials with the Indicators read scope.

**This skill invokes:** `/lookup-liberty91`, `/lookup-virustotal`, `/lookup-abuseipdb`, `/lookup-greynoise`, `/lookup-shodan`, `/lookup-otx`, `/lookup-censys`, `/lookup-urlscan`, `/lookup-misp`, `/lookup-opencti`, `/lookup-reversinglabs`, `/lookup-crowdstrike`, optionally `/lookup-ransomwarelive`, optionally `/lookup-sentinel` (exposure sweep of the confirmed-malicious subset against your own telemetry); then `/score-source`, `/apply-tlp`, `/confidence-language`. For deeper graph traversal, hands off to `/indicator-pivoting`.

## Enrichment routing by IOC type

### IPv4/IPv6 address

| Order | Skill | What to extract |
|-------|-------|----------------|
| 0 | `/lookup-liberty91` | **First-party — run before spending third-party quota.** `ioc-lookup <ip>` for the platform's own verdict, derived confidence, effective TLP and tags; `threat-events --q <ip>` if it appears in reporting |
| 1 | `/lookup-virustotal` | Detection ratio, community score, associated domains, last analysis results |
| 2 | `/lookup-abuseipdb` | Abuse confidence score, report count, ISP, usage type, country |
| 3 | `/lookup-greynoise` | Classification (benign/malicious/unknown), noise status, actor, tags |
| 4 | `/lookup-shodan` | Open ports, banners, services, OS, hostnames, vulns, last update |
| 5 | `/lookup-otx` | Pulse count, associated pulses, reputation, related indicators |
| 6 | `/lookup-reversinglabs` | RL classification, files seen contacting the IP (malware-corpus reputation). **Run when configured** — independent of VT/AbuseIPDB. |
| 7 | `/lookup-crowdstrike` | `indicator <ip>` — Falcon Intel malicious confidence, linked actors + malware families, report refs. **Run when configured.** |
| 8 | `/lookup-censys` | Services, certificates, autonomous system, location |
| 9 | `/lookup-misp` | Internal correlation — `search-attributes --value <ip>` to surface prior catalogued events |
| 10 | `/lookup-opencti` | Internal correlation — `lookup <ip>` to surface existing observables/indicators in your knowledge base |

### Domain

| Order | Skill | What to extract |
|-------|-------|----------------|
| 0 | `/lookup-liberty91` | **First-party — run first.** `ioc-lookup <domain>` for verdict, derived confidence, effective TLP and tags |
| 1 | `/lookup-virustotal` | Detection ratio, WHOIS, DNS records, subdomains, communicating files |
| 2 | `/lookup-urlscan` | Existing scans (search, don't re-submit by default): screenshot, page content, redirects, technologies, IPs resolved |
| 3 | `/lookup-shodan` | DNS resolution, open ports on resolved IPs |
| 4 | `/lookup-otx` | Pulse count, associated indicators, passive DNS |
| 5 | `/lookup-reversinglabs` | RL classification, files seen resolving / contacting the domain (malware-corpus reputation). **Run when configured.** |
| 6 | `/lookup-crowdstrike` | `indicator <domain>` — Falcon Intel malicious confidence, linked actors + malware families, report refs. **Run when configured.** |
| 7 | `/lookup-censys` | Certificate history, associated IPs (paid plan) |
| 8 | `/lookup-misp` | `search-attributes --value <domain>` for internal correlation |
| 9 | `/lookup-opencti` | `lookup <domain>` — existing observables/indicators in your knowledge base |
| 10 | `/lookup-ransomwarelive` | `search --q <org-candidate>` — sweep ransomware leak-site claims that match the apex (see `/domain-investigation` § Ransomware-claim hits for caveats) |

### URL

| Order | Skill | What to extract |
|-------|-------|----------------|
| 0 | `/lookup-liberty91` | **First-party — run first.** `ioc-lookup <url>` for verdict, derived confidence, effective TLP and tags |
| 1 | `/lookup-virustotal` | Detection ratio, final URL, redirections, downloaded files |
| 2 | `/lookup-urlscan` | Existing scans first; submit fresh only if no recent capture exists. Screenshot, DOM, requests, IPs contacted, technologies |
| 3 | `/lookup-otx` | Pulse associations, reputation |
| 4 | `/lookup-reversinglabs` | RL classification, files seen requesting the URL (malware-corpus reputation). **Run when configured.** Use `submit-url` only for fresh crawl + sandbox. |
| 5 | `/lookup-crowdstrike` | `indicator <url>` — Falcon Intel malicious confidence, linked actors + malware families, report refs. **Run when configured.** |
| 6 | `/lookup-misp` | `search-attributes --value <url>` for internal correlation |
| 7 | `/lookup-opencti` | `lookup <url>` — existing observables/indicators in your knowledge base |

### File hash (MD5, SHA-1, SHA-256)

| Order | Skill | What to extract |
|-------|-------|----------------|
| 0 | `/lookup-liberty91` | **First-party — run first.** `ioc-lookup <hash>` for verdict, derived confidence, effective TLP; `library malware --q <family>` once VT/RL name the family |
| 1 | `/lookup-virustotal` | Detection ratio, file type, size, names, behavioural analysis, MITRE ATT&CK tags |
| 2 | `/lookup-reversinglabs` | **Run when configured — strongest single-source verdict.** `hash --av-scanners --ticloud` for classification + threat name + AV ratio; `report --detailed` for MITRE ATT&CK mapping, sandbox, and networkthreatintelligence (C2 indicators extracted from the sample) |
| 3 | `/lookup-crowdstrike` | `indicator <hash>` — Falcon Intel verdict + the threat actors and malware families CrowdStrike links to this hash + report refs. **Run when configured.** |
| 4 | `/lookup-otx` | Pulse associations, related indicators, YARA matches |
| 5 | `/lookup-misp` | `search-attributes --value <hash>` for internal correlation |
| 6 | `/lookup-opencti` | `lookup <hash>` — existing observables/indicators in your knowledge base |
| 7 | `/lookup-ransomwarelive` | `iocs <group>` and `yara <group>` if the hash hits a known ransomware family from VT/RL classification |

### Email address

| Order | Skill | What to extract |
|-------|-------|----------------|
| 0 | `/lookup-liberty91` | **First-party — run first.** `ioc-lookup <email>` for verdict, derived confidence, effective TLP |
| 1 | `/lookup-virustotal` | Associated domains and files (premium feature, may return empty on free tier) |
| 2 | `/lookup-otx` | Pulse associations |
| 3 | `/lookup-misp` | `search-attributes --type email --value <email>` for internal correlation |
| 4 | `/lookup-opencti` | `lookup <email>` — existing observables/indicators in your knowledge base |

## Enrichment process

### Step 1: Parse and classify

Read the input IOC list. For each indicator:
1. Determine type (IPv4, IPv6, domain, URL, hash, email)
2. Validate format (regex check)
3. Deduplicate

### Step 2: Batch and route

Group IOCs by type. For each group, dispatch the relevant `/lookup-*` skills (see routing tables above).

**Parallelisation**: For a single IOC, dispatch all relevant lookups in parallel. For bulk IOCs, process in batches of 10 to respect rate limits (see `tools/REGISTRY.md` for per-API limits).

### Step 3: Synthesise results

For each IOC, combine results from all lookups into a single enrichment record:

```yaml
indicator: 203.0.113.42
type: ipv4-addr
enrichment_date: 2026-04-04
source_assessment: F6  # Automated enrichment, no human judgment yet

virustotal:
  detection_ratio: 12/87
  community_score: -45
  associated_domains: [evil.example.com, bad.example.org]

abuseipdb:
  abuse_confidence: 95
  total_reports: 234
  isp: "Bulletproof Hosting Inc"
  country: RU

greynoise:
  classification: malicious
  noise: false
  tags: [c2, cobalt-strike]

shodan:
  ports: [80, 443, 8443]
  os: Linux
  vulns: [CVE-2024-12345]

otx:
  pulse_count: 7
  tags: [apt28, fancy-bear, c2]

censys:
  services: [HTTP, HTTPS]
  certificate_issuer: "Let's Encrypt"

misp:
  matched_attributes: 3
  matched_events: [42, 137]   # event IDs in the local instance
  prior_tags: ["tlp:amber", "actor:apt28"]

opencti:
  known_as: [observable, indicator]
  indicator_score: 85          # x_opencti_score on the existing indicator
  prior_labels: [apt28, c2]

synthesis:
  verdict: malicious
  confidence: 85
  context: "Known C2 server associated with APT28 campaigns. Hosted on bulletproof infrastructure in Russia. Multiple community reports plus prior MISP events confirm malicious activity."
  tags: [apt28, c2, cobalt-strike]
  mitre_attack: [T1071.001]
```

### Step 4: Assess and tag

Apply source assessment (Admiralty Scale) to the enrichment with `/score-source`:
- Source reliability: B (established tool APIs, usually reliable)
- Information credibility: based on corroboration across tools (3+ tools agree → 1/Confirmed; 2 agree → 2/Probably true; single source → 3/Possibly true)
- A MISP or OpenCTI hit on a previously-curated event/entity lifts credibility one step (your team has already vetted it once)
- A Liberty91 hit brings its own Admiralty rating — use the occurrence's `credibility` band and each source's `reliability` grade verbatim instead of re-deriving them from tool agreement

### Step 5: Store

Write enrichment results to `data/iocs/active/YYYY-MM-DD-<context>.md` with appropriate frontmatter. Apply `/apply-tlp` before sharing outside the team.

### Step 6 (optional): Push back

If the enrichment confirms a previously-unknown malicious indicator, push it back into your own platform so future enrichments hit your catalogue first: `/lookup-misp add-attribute` (or `create-event` for a fresh cluster) for a MISP instance, `/lookup-opencti create-indicator` (with `--score` and `--labels`) for an OpenCTI knowledge base, and/or `/lookup-liberty91 ingest` to file the finding as a report in Liberty91 (it is enriched and matched into a Threat Event for your account). Liberty91 writes are metered and publish to your account — **confirm with the user first**.

### Step 6b (optional): Sweep your own telemetry

If `$SENTINEL_WORKSPACE_ID` + app credentials are set, take the **confirmed-malicious subset** (not the whole raw list) and chain `/lookup-sentinel` for a batch exposure sweep — one `let`-bound `dynamic` list per IOC type, run only against tables that skill confirms exist in the workspace. This answers the question enrichment cannot: *did any of these touch us?* Hits become incident leads (route to the matching `/*-investigation`); a clean sweep is reported as "not observed in collected telemetry over <window>", never as "not compromised".

### Step 7 (optional): Pivot

If the enrichment surfaces strong cluster candidates (cert siblings, JARM matches, communicating files), hand off to `/indicator-pivoting` for the next hop.

## Rate-limit awareness

Per-API limits live in `tools/REGISTRY.md`. Summary:

| Service | Free-tier limit | Mitigation |
|---------|-----------------|------------|
| VirusTotal (free) | 4/min, 500/day | Batch with 15s delays |
| URLScan.io (free) | 100 scans/day | Prefer `search` over `submit` |
| Shodan (free) | 1 req/sec | Sequential processing |
| AbuseIPDB (free) | 1000 checks/day | IPs only |
| GreyNoise (free) | 50 req/day | IPs only, prioritise |
| OTX | 10k req/hour | Batch freely |
| Censys | 250/month | Selective use only |
| MISP | host-bound | Local; no public limit |
| OpenCTI | host-bound | Local; no public limit |
| Liberty91 | per-key `X-RateLimit-*` + monthly credits | 1 credit per lookup; watch `_meta.credits_remaining`, and note a `429` may mean credits, not rate |
| ransomware.live (PRO) | 3000/day | Plenty for bulk org-candidate sweeps |
| ReversingLabs (A1000) | undocumented; 429 + `Retry-After` | Back off on 429. Each `--pivot` entry on the `ip` op is a separate call — fan out deliberately. |

## Handling missing API keys

If an API key is not configured for a service:
1. Skip that enrichment source
2. Note in the synthesis that the source was unavailable
3. Adjust confidence accordingly (fewer sources = lower corroboration)
4. Continue with available sources

To configure missing keys, point the user at `/cti-setup`.

## Related skills

- `/lookup-liberty91`, `/lookup-virustotal`, `/lookup-abuseipdb`, `/lookup-greynoise`, `/lookup-shodan`, `/lookup-otx`, `/lookup-censys`, `/lookup-urlscan`, `/lookup-misp`, `/lookup-opencti`, `/lookup-reversinglabs`, `/lookup-crowdstrike`, `/lookup-ransomwarelive` — the underlying lookups
- `/lookup-sentinel` — batch exposure sweep of confirmed-malicious IOCs against your own Sentinel workspace (step 6b)
- `/ip-investigation`, `/domain-investigation`, `/hash-investigation`, `/url-investigation` — single-seed first-hop chains; this workflow is the bulk-list equivalent
- `/indicator-pivoting` — when an enrichment opens new pivot candidates
- `/score-source`, `/apply-tlp`, `/confidence-language` — apply rigor to each finished enrichment record
