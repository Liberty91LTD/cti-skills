---
name: ioc-enrichment-workflow
description: Workflow for enriching raw IOCs. Routes each IOC type to appropriate tool agents and synthesises results.
user-invocable: false
metadata:
  version: 1.0.0
---

# IOC Enrichment Workflow

This workflow defines how to enrich raw indicators of compromise by routing them to the appropriate tool agents and synthesising results.

## Enrichment Routing by IOC Type

### IPv4/IPv6 Address
| Order | Agent | What to extract |
|-------|-------|----------------|
| 1 | virustotal-agent | Detection ratio, community score, associated domains, last analysis results |
| 2 | abuseipdb-agent | Abuse confidence score, report count, ISP, usage type, country |
| 3 | greynoise-agent | Classification (benign/malicious/unknown), noise status, actor, tags |
| 4 | shodan-agent | Open ports, banners, services, OS, hostnames, vulns, last update |
| 5 | otx-agent | Pulse count, associated pulses, reputation, related indicators |
| 6 | censys-agent | Services, certificates, autonomous system, location |

### Domain
| Order | Agent | What to extract |
|-------|-------|----------------|
| 1 | virustotal-agent | Detection ratio, WHOIS, DNS records, subdomains, communicating files |
| 2 | urlscan-agent | Screenshot, page content, redirects, technologies, IPs resolved |
| 3 | shodan-agent | DNS resolution history, open ports on resolved IPs |
| 4 | otx-agent | Pulse count, associated indicators, passive DNS |
| 5 | censys-agent | Certificate history, associated IPs |

### URL
| Order | Agent | What to extract |
|-------|-------|----------------|
| 1 | virustotal-agent | Detection ratio, final URL, redirections, downloaded files |
| 2 | urlscan-agent | Screenshot, DOM content, requests made, IPs contacted, technologies |
| 3 | otx-agent | Pulse associations, reputation |

### File Hash (MD5, SHA-1, SHA-256)
| Order | Agent | What to extract |
|-------|-------|----------------|
| 1 | virustotal-agent | Detection ratio, file type, size, names, behavioural analysis, MITRE ATT&CK tags |
| 2 | otx-agent | Pulse associations, related indicators, YARA matches |

### Email Address
| Order | Agent | What to extract |
|-------|-------|----------------|
| 1 | virustotal-agent | Associated domains, files |
| 2 | otx-agent | Pulse associations |

## Enrichment Process

### Step 1: Parse and Classify
Read the input IOC list. For each indicator:
1. Determine type (IPv4, IPv6, domain, URL, hash, email)
2. Validate format (regex check)
3. Deduplicate

### Step 2: Batch and Route
Group IOCs by type. For each group, request the orchestrator to dispatch the appropriate tool agents (see routing table above).

**Parallelisation**: For a single IOC, dispatch all relevant agents in parallel. For bulk IOCs, process in batches of 10 to respect rate limits.

### Step 3: Synthesise Results
For each IOC, combine results from all agents into a single enrichment record:

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

synthesis:
  verdict: malicious
  confidence: 85
  context: "Known C2 server associated with APT28 campaigns. Hosted on bulletproof infrastructure in Russia. Multiple community reports confirm malicious activity."
  tags: [apt28, c2, cobalt-strike]
  mitre_attack: [T1071.001]
```

### Step 4: Assess and Tag
Apply source assessment (Admiralty Scale) to the enrichment:
- Source reliability: B (established tool APIs, usually reliable)
- Information credibility: Based on corroboration across tools (if 3+ tools agree → 1/Confirmed; if 2 agree → 2/Probably true; single source → 3/Possibly true)

### Step 5: Store
Write enrichment results to `data/iocs/active/YYYY-MM-DD-<context>.md` with appropriate frontmatter.

## Rate Limit Awareness

| Service | Rate limit | Mitigation |
|---------|-----------|------------|
| VirusTotal (free) | 4 requests/min | Batch with 15s delays |
| VirusTotal (premium) | 1000 requests/min | Batch freely |
| URLScan.io (free) | 100 searches/day | Prioritise domains/URLs |
| Shodan (free) | 1 request/sec | Sequential processing |
| AbuseIPDB (free) | 1000 requests/day | IPs only |
| GreyNoise (free) | 50 requests/day | IPs only, prioritise |
| OTX | 10,000 requests/hour | Batch freely |
| Censys (free) | 250 requests/month | Selective use only |

## Handling Missing API Keys

If an API key is not configured for a service:
1. Skip that enrichment source
2. Note in the synthesis that the source was unavailable
3. Adjust confidence accordingly (fewer sources = lower corroboration)
4. Continue with available sources
