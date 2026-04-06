# CTI Agentic Skills Platform

## Overview
Fully agentic Cyber Threat Intelligence platform built on Claude Code. Provides end-to-end intelligence lifecycle capabilities: collection, processing, analysis, production, and dissemination. Structured around the CTI Hyperloop (Google/Mandiant) framework operating at strategic, operational, and tactical levels simultaneously.

Clone this repo, configure API keys, and get a complete CTI capability.

## Quick Start
1. Clone this repository
2. Run `scripts/setup.sh` to configure API keys and download MITRE ATT&CK data
3. Start with: "Investigate 203.0.113.42" or "Profile APT28" or "/pir-management"

## Directory Structure
```
├── CLAUDE.md                       # This file — project manifest
├── .claude/
│   ├── settings.json               # Permissions and hooks
│   ├── settings.local.json         # API keys (gitignored, created by setup.sh)
│   ├── agents/                     # 14 agent definitions
│   └── skills/                     # ~50 skills in 7 categories
├── data/
│   ├── iocs/active/, archive/      # IOC collections
│   ├── reports/drafts/, reviewed/, published/  # Intelligence products
│   ├── assessments/threat/, risk/, vulnerability/
│   ├── pirs/active/, archive/      # Priority Intelligence Requirements
│   ├── stix-bundles/               # STIX 2.1 exports
│   ├── detection-rules/sigma/, yara/, kql/
│   ├── investigations/             # Active investigation workspaces
│   └── exports/                    # IOC exports (CSV, STIX, OpenIOC)
├── mitre-attack/                   # Local ATT&CK dataset
└── scripts/                        # Setup and hook scripts
```

## Agent System

14 agents in `.claude/agents/`. The `cti-orchestrator` is the main coordinator.

### Agents

| Agent | Model | Role |
|-------|-------|------|
| **cti-orchestrator** | opus | Central coordinator — Hyperloop hub, dispatches all workflows |
| **analyst** | opus | Core analysis — SATs, ACH, profiling, assessment |
| **report-writer** | opus | Intelligence production — reports, assessments, briefings |
| **quality-reviewer** | opus | Quality gate — peer review before dissemination |
| **osint-researcher** | sonnet | OSINT collection via web search/fetch |
| **detection-engineer** | sonnet | SIGMA, YARA, KQL rule writing |
| **ioc-processor** | sonnet | IOC enrichment, dedup, export, STIX bundles |
| **virustotal-agent** | haiku | VirusTotal API queries |
| **urlscan-agent** | haiku | URLScan.io submissions and results |
| **shodan-agent** | haiku | Shodan host/port queries |
| **abuseipdb-agent** | haiku | AbuseIPDB reputation lookups |
| **greynoise-agent** | haiku | GreyNoise noise/scanner classification |
| **otx-agent** | haiku | AlienVault OTX pulse queries |
| **censys-agent** | haiku | Censys host/certificate queries |

### Permission Isolation
- Each tool agent has access to exactly ONE external API
- `osint-researcher` is the only agent with WebSearch/WebFetch
- `analyst` and `report-writer` have NO Bash access (pure reasoning/writing)
- `quality-reviewer` has NO Edit access (read-only review)
- The orchestrator never calls external APIs directly — always delegates to tool agents
- Tool agents never interpret results — they retrieve and return data

### Model Assignments
- **Opus**: Reasoning-intensive roles (orchestrator, analyst, report-writer, quality-reviewer)
- **Sonnet**: Structured tasks (osint-researcher, detection-engineer, ioc-processor)
- **Haiku**: Simple query-response (all tool API agents)

## Skill Categories

### CTI Tradecraft (`skills/cti-tradecraft/`)
malware-analysis, indicator-pivoting, osint-methodology, darkweb-collection, threat-actor-profiling, campaign-tracking, vulnerability-intelligence

### Analytical Techniques (`skills/analytical-techniques/`)
ach, horizon-scanning, source-assessment, structured-analytic-techniques, key-assumptions-check, red-team-analysis, threat-assessment

### Production (`skills/production/`)
tlp-guide, confidence-levels, intelligence-writing, writing-assessments, likelihood-language, kql-writing, sigma-writing, yara-writing, ioc-export, stix-bundle, ioc-enrichment-workflow

### Tool APIs (`skills/tool-apis/`)
virustotal-api, urlscan-api, shodan-api, abuseipdb-api, greynoise-api, otx-api, censys-api, mitre-attack

### Knowledge Cells (`skills/knowledge-cells/`)
Self-learning intelligence knowledge bases: china-cyber-espionage, russia-cyber-espionage, iran-cyber-espionage, dprk-cyber-espionage, ransomware-ecosystem, carding-financial-fraud, infostealers, phishing-social-engineering, supply-chain-threats, hacktivism, initial-access-brokers

Knowledge cells are `user-invocable: true` — load on demand via slash commands. The orchestrator can create new cells as needed.

### Management (`skills/management/`)
stakeholder-management, pir-management, quality-control, sops, feedback-loops, maturity-assessment, intelligence-sharing

### Hyperloop (`skills/hyperloop/`)
cti-hyperloop — operational doctrine mapping the 6 Hyperloop phases to agents and intelligence levels

## CTI Hyperloop Mapping

All workflows follow the 6-phase Hyperloop at three levels (strategic/operational/tactical):

1. **Planning & Direction** → PIRs, stakeholder requirements (orchestrator)
2. **Collection** → OSINT researcher + tool agents
3. **Processing** → IOC processor (normalize, deduplicate, source-assess)
4. **Analysis** → Analyst (SATs, ACH, profiling, assessment)
5. **Dissemination** → Report writer + detection engineer + IOC processor (export)
6. **Feedback** → Orchestrator (feedback loops, PIR refinement)

## Data Conventions

### Mandatory on ALL outputs
- **TLP marking**: Every file must have a `tlp:` field (CLEAR/GREEN/AMBER/AMBER+STRICT/RED)
- **Source assessment**: Every piece of collected intelligence must carry an Admiralty Scale rating (e.g., B2)
- **Confidence level**: Every analytical judgment must have a confidence level (0-100 MISP scale)
- **Likelihood language**: Every forward-looking assessment must use the probability yardstick

### File naming
- Reports/assessments: `YYYY-MM-DD-<type>-<slug>.md`
- IOC collections: `YYYY-MM-DD-<context>.md`
- Investigations: `INV-YYYY-MM-DD-<slug>/`
- PIRs: `PIR-001-<slug>.md`
- SIGMA rules: `<technique-id>-<slug>.yml`
- YARA rules: `<malware-name>.yar`
- KQL queries: `<technique-id>-<slug>.kql`
- STIX bundles: `YYYY-MM-DD-<context>.json`

### Frontmatter templates

**Reports:**
```yaml
---
title: "Flash Report: [subject]"
type: flash-report|intelligence-summary|threat-assessment|threat-actor-profile|campaign-report
date: YYYY-MM-DD
tlp: AMBER
confidence: high
author: analyst
reviewer: quality-reviewer
status: draft|reviewed|published
related_pirs: [PIR-001]
mitre_attack: [T1566, T1078]
tags: [apt28, phishing]
---
```

**IOC collections:**
```yaml
---
title: "IOCs from [context]"
date: YYYY-MM-DD
tlp: GREEN
source: "[source description]"
source_reliability: B
information_credibility: 2
related_investigation: INV-YYYY-MM-DD-slug
tags: [apt28, phishing]
---
```

**PIRs:**
```yaml
---
pir_id: PIR-001
title: "What are the current cyber threats to [sector] from [actor]?"
created: YYYY-MM-DD
review_date: YYYY-MM-DD
status: active
priority: high
stakeholder: [CISO, SOC Lead]
last_satisfied: YYYY-MM-DD
---
```

## Platform Rules

1. Every intelligence output must have a TLP marking
2. Every source must have an Admiralty Scale assessment
3. Every analytical judgment must have a confidence level
4. Every forward-looking statement must use likelihood language
5. Knowledge cells must be updated when relevant new intelligence is processed
6. Quality review is required before any product moves to "published"
7. PIRs drive collection priorities — check active PIRs before starting new work
8. The orchestrator never calls external APIs directly — always delegates to tool agents
9. Tool agents never interpret results — they retrieve and return data
10. Analytical agents (analyst, report-writer) never call APIs — they work with collected data

## API Keys
Configured via `scripts/setup.sh`, stored in `.claude/settings.local.json` (gitignored):
- VIRUSTOTAL_API_KEY
- URLSCAN_API_KEY
- SHODAN_API_KEY
- ABUSEIPDB_API_KEY
- GREYNOISE_API_KEY
- OTX_API_KEY
- CENSYS_API_ID + CENSYS_API_SECRET
