# CTI Agentic Skills Platform

A fully agentic Cyber Threat Intelligence platform built on [Claude Code](https://claude.ai/claude-code). Clone this repo, configure your API keys, and get a complete CTI capability — from indicator enrichment to finished intelligence products.

Structured around the [CTI Hyperloop](https://cloud.google.com/blog/topics/threat-intelligence/cti-process-hyperloop/) framework, operating at strategic, operational, and tactical levels simultaneously.

## What's Inside

### 14 Agents

| Agent | Model | Role |
|-------|-------|------|
| **cti-orchestrator** | Opus | Central coordinator — maps all workflows to Hyperloop phases |
| **analyst** | Opus | Core analysis — ACH, threat assessment, actor profiling |
| **report-writer** | Opus | Intelligence production — reports, assessments, briefings |
| **quality-reviewer** | Opus | Quality gate — peer review before dissemination |
| **osint-researcher** | Sonnet | OSINT collection via web search/fetch |
| **detection-engineer** | Sonnet | SIGMA, YARA, KQL rule writing |
| **ioc-processor** | Sonnet | IOC enrichment, dedup, export, STIX bundles |
| **virustotal-agent** | Haiku | VirusTotal API |
| **urlscan-agent** | Haiku | URLScan.io API |
| **shodan-agent** | Haiku | Shodan API |
| **abuseipdb-agent** | Haiku | AbuseIPDB API |
| **greynoise-agent** | Haiku | GreyNoise API |
| **otx-agent** | Haiku | AlienVault OTX API |
| **censys-agent** | Haiku | Censys API |

### 52 Skills in 7 Categories

**Analytical Techniques** — ACH, horizon scanning, source assessment (NATO Admiralty Scale), structured analytic techniques, key assumptions check, red team analysis, threat assessment

**CTI Tradecraft** — Malware analysis, indicator pivoting, OSINT methodology, dark web collection, threat actor profiling, campaign tracking, vulnerability intelligence

**Production** — TLP guide, confidence levels, likelihood language, intelligence writing (with templates for flash reports, threat assessments, actor profiles, campaign reports), writing assessments, SIGMA/YARA/KQL writing, IOC export (CSV/STIX/OpenIOC/MISP), STIX 2.1 bundles, IOC enrichment workflow

**Tool APIs** — VirusTotal, URLScan.io, Shodan, AbuseIPDB, GreyNoise, AlienVault OTX, Censys, MITRE ATT&CK (local dataset)

**Knowledge Cells** — Self-learning intelligence knowledge bases, seeded with current public intelligence:
- Nation-state: China, Russia, Iran, DPRK cyber espionage
- Cybercrime: Ransomware ecosystem, carding/financial fraud, infostealers, phishing/social engineering, supply chain threats, hacktivism, initial access brokers

**Management** — Stakeholder management, PIR management, quality control, SOPs, feedback loops, maturity assessment, intelligence sharing

**Hyperloop** — Operational doctrine mapping the 6-phase intelligence lifecycle across strategic/operational/tactical levels

## Quick Start

```bash
# 1. Clone
git clone git@github.com:renzejongman/cti-agentic-skills.git
cd cti-agentic-skills

# 2. Configure API keys and download MITRE ATT&CK data
./scripts/setup.sh

# 3. Start Claude Code
claude
```

Then try:
- `Investigate 203.0.113.42` — full indicator enrichment across all tool agents
- `Profile APT28` — OSINT collection + analyst profiling + finished report
- `Write a threat assessment on ransomware targeting healthcare` — end-to-end Hyperloop workflow
- `/ach` — run Analysis of Competing Hypotheses
- `/iran-cyber-espionage` — load the Iran knowledge cell
- `/pir-management` — set up Priority Intelligence Requirements

## Architecture

```
User Request
     ↓
CTI Orchestrator (maps to Hyperloop phase)
     ↓
┌─────────────────────────────────────────────┐
│ Phase 1: Planning & Direction               │
│   PIRs, stakeholder requirements            │
├─────────────────────────────────────────────┤
│ Phase 2: Collection                         │
│   OSINT researcher + tool agents (parallel) │
├─────────────────────────────────────────────┤
│ Phase 3: Processing                         │
│   IOC processor (normalize, deduplicate)    │
├─────────────────────────────────────────────┤
│ Phase 4: Analysis                           │
│   Analyst (SATs, ACH, profiling)            │
├─────────────────────────────────────────────┤
│ Phase 5: Dissemination                      │
│   Report writer + detection engineer        │
├─────────────────────────────────────────────┤
│ Phase 6: Feedback                           │
│   PIR refinement, source quality tracking   │
└─────────────────────────────────────────────┘
```

### Permission Isolation

Each tool agent accesses exactly one external API. Analytical agents (analyst, report-writer) have no API or Bash access — they work purely with collected data. The quality reviewer has no edit access — read-only review.

### Self-Learning Knowledge Cells

Knowledge cells grow over time. When new intelligence is processed, the orchestrator dispatches the analyst to review it against the existing cell, then updates the cell with new actors, campaigns, TTPs, and sources. Every update is logged in the cell's change log.

The orchestrator can create new knowledge cells on demand as emerging threats require them.

## Data Conventions

All intelligence outputs follow mandatory standards:

- **TLP**: Every output carries a Traffic Light Protocol designation
- **Source Assessment**: Every piece of collected intelligence is rated on the NATO Admiralty Scale (source reliability A-F, information credibility 1-6)
- **Confidence Levels**: Every analytical judgment includes a confidence level with rationale
- **Likelihood Language**: Every forward-looking assessment uses standardised probability language (Remote → Almost Certain with percentage ranges)
- **MITRE ATT&CK**: TTPs are mapped to ATT&CK techniques wherever applicable

## Directory Structure

```
├── CLAUDE.md                    # Project manifest (agent/skill rules)
├── .claude/
│   ├── agents/                  # 14 agent definitions
│   └── skills/                  # 52 skills in 7 categories
├── data/
│   ├── iocs/                    # IOC collections (active + archive)
│   ├── reports/                 # Intelligence products (draft → reviewed → published)
│   ├── assessments/             # Threat, risk, and vulnerability assessments
│   ├── pirs/                    # Priority Intelligence Requirements
│   ├── stix-bundles/            # STIX 2.1 exports
│   ├── detection-rules/         # SIGMA, YARA, KQL rules
│   ├── investigations/          # Active investigation workspaces
│   └── exports/                 # IOC exports (CSV, STIX, OpenIOC, MISP)
├── mitre-attack/                # Local ATT&CK Enterprise dataset
└── scripts/                     # Setup and hook scripts
```

## API Keys

Configure via `scripts/setup.sh` or set environment variables directly:

| Service | Env Variable | Free Tier |
|---------|-------------|-----------|
| VirusTotal | `VIRUSTOTAL_API_KEY` | 4 req/min, 500/day |
| URLScan.io | `URLSCAN_API_KEY` | 100 scans/day |
| Shodan | `SHODAN_API_KEY` | 1 req/sec |
| AbuseIPDB | `ABUSEIPDB_API_KEY` | 1000 checks/day |
| GreyNoise | `GREYNOISE_API_KEY` | 50 req/day |
| AlienVault OTX | `OTX_API_KEY` | 10,000 req/hour |
| Censys | `CENSYS_API_ID` + `CENSYS_API_SECRET` | 250 queries/month |

All keys are optional — the platform degrades gracefully when a key is missing, skipping that enrichment source and noting the gap.

## License

Private repository. All rights reserved.
