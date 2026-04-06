---
name: cti-hyperloop
description: CTI Hyperloop framework — operational doctrine mapping the intelligence lifecycle across strategic, operational, and tactical levels with bidirectional feedback.
user-invocable: true
metadata:
  version: 1.0.0
---

# CTI Hyperloop Framework

The CTI Hyperloop (based on Google/Mandiant's practical implementation framework) extends the traditional intelligence cycle by running it at three levels simultaneously with continuous bidirectional feedback.

## Core Concept

Traditional intelligence cycle: linear, single-track, often stuck at the tactical level.
Hyperloop: three parallel tracks (strategic, operational, tactical) feeding each other continuously.

```
STRATEGIC  ←→  OPERATIONAL  ←→  TACTICAL
    ↓              ↓               ↓
Direction → Collection → Processing → Analysis → Dissemination → Feedback
    ↑                                                              |
    └──────────────────────────────────────────────────────────────┘
```

## Intelligence Levels

### Strategic Intelligence
- **Time horizon**: 6-24 months
- **Consumers**: CISO, Board, Risk Management, Security Architecture
- **Focus**: Threat landscape trends, emerging threats, geopolitical developments, sector risk posture
- **Products**: Threat landscape reports, strategic assessments, horizon scanning reports, maturity assessments
- **Example PIR**: "How will the ransomware threat landscape evolve over the next 12 months and what are the implications for our risk posture?"

### Operational Intelligence
- **Time horizon**: Weeks to months
- **Consumers**: SOC Manager, IR Lead, Security Operations
- **Focus**: Active campaigns, threat actor profiling, TTP analysis, vulnerability exploitation trends
- **Products**: Campaign reports, threat actor profiles, operational assessments, hunt packages
- **Example PIR**: "What TTPs are currently being used by groups targeting our sector?"

### Tactical Intelligence
- **Time horizon**: Hours to days
- **Consumers**: SOC Analysts, Detection Engineers, IR Analysts
- **Focus**: IOCs, detection rules, immediate response support, indicator enrichment
- **Products**: IOC packages, SIGMA/YARA/KQL rules, flash reports, enrichment reports
- **Example PIR**: "What IOCs are associated with the current wave of attacks targeting our VPN appliances?"

## Phase Mapping to Platform

### Phase 1: Planning & Direction
**What**: Define what intelligence is needed and set priorities.

| Level | Activity | Agent | Skills |
|-------|----------|-------|--------|
| Strategic | Set/review PIRs, horizon scanning briefs | orchestrator | pir-management, stakeholder-management |
| Operational | Define collection priorities for active investigations | orchestrator | pir-management, sops |
| Tactical | Identify IOC collection gaps, detection coverage gaps | orchestrator | sops |

### Phase 2: Collection
**What**: Gather raw data from relevant sources.

| Level | Activity | Agent | Skills |
|-------|----------|-------|--------|
| Strategic | Trend monitoring, landscape research | osint-researcher | osint-methodology |
| Operational | Threat actor tracking, campaign research, dark web monitoring | osint-researcher, tool agents | osint-methodology, darkweb-collection |
| Tactical | IOC lookups, bulk enrichment | tool agents, ioc-processor | tool-api skills, ioc-enrichment-workflow |

### Phase 3: Processing
**What**: Normalise, deduplicate, and structure collected data.

| Level | Activity | Agent | Skills |
|-------|----------|-------|--------|
| All | IOC deduplication, format normalisation, source assessment tagging | ioc-processor | ioc-enrichment-workflow, source-assessment |

### Phase 4: Analysis
**What**: Apply human judgment to produce assessed intelligence.

| Level | Activity | Agent | Skills |
|-------|----------|-------|--------|
| Strategic | Horizon scanning, maturity assessment, trend analysis | analyst | horizon-scanning, threat-assessment, maturity-assessment |
| Operational | ACH, threat actor profiling, campaign tracking | analyst | ach, threat-actor-profiling, campaign-tracking, key-assumptions-check |
| Tactical | IOC correlation, detection gap analysis, indicator pivoting | analyst | indicator-pivoting, vulnerability-intelligence |

### Phase 5: Dissemination
**What**: Deliver finished intelligence to stakeholders.

| Level | Activity | Agent | Skills |
|-------|----------|-------|--------|
| Strategic | Landscape reports, annual assessments, board briefings | report-writer | intelligence-writing, writing-assessments, stakeholder-management |
| Operational | Actor profiles, campaign reports, operational assessments | report-writer | intelligence-writing, writing-assessments |
| Tactical | IOC packages, detection rules, flash reports | detection-engineer, ioc-processor, report-writer | sigma/yara/kql-writing, ioc-export, stix-bundle |

### Phase 6: Feedback
**What**: Assess effectiveness and refine direction.

| Level | Activity | Agent | Skills |
|-------|----------|-------|--------|
| All | Consumer feedback, source quality tracking, PIR refinement | orchestrator | feedback-loops, pir-management |

## Bidirectional Flow Examples

**Tactical → Operational**: IOC enrichment reveals infrastructure pattern shared across multiple incidents → triggers campaign tracking investigation.

**Operational → Strategic**: Campaign analysis identifies new nation-state actor shifting targeting to a new sector → feeds into strategic landscape assessment and PIR update.

**Strategic → Operational**: Horizon scanning identifies AI-augmented social engineering as emerging threat → creates operational collection tasking for specific TTP monitoring.

**Operational → Tactical**: Threat actor profiling reveals preferred exploitation technique → drives creation of specific SIGMA detection rules.

**Strategic → Tactical**: Risk assessment identifies unpatched VPN as critical exposure → prioritises vulnerability intelligence and IOC monitoring for VPN exploits.

**Tactical → Strategic**: Spike in credential-stuffing alerts → informs strategic assessment of the underground economy and infostealer trend.

## Orchestrator Workflow Mapping

When the orchestrator receives a task, it maps it to the Hyperloop:

| User Request | Primary Level | Hyperloop Phases | Key Agents |
|-------------|---------------|-----------------|------------|
| "Investigate this IP" | Tactical | 2→3→4→5 | Tool agents → IOC processor → Analyst → Detection engineer |
| "Profile this threat actor" | Operational | 2→3→4→5→6 | OSINT researcher → IOC processor → Analyst → Report writer → Update knowledge cell |
| "Write a threat assessment on X" | Strategic/Operational | 1→2→3→4→5→6 | Orchestrator (PIRs) → OSINT researcher → Analyst (SATs) → Report writer → Quality reviewer |
| "Enrich this IOC list" | Tactical | 2→3→5 | Tool agents → IOC processor → Export |
| "What's the current ransomware landscape?" | Strategic | 2→4→5 | OSINT researcher → Analyst (knowledge cell) → Report writer |
| "Create detection rules for APT28 TTPs" | Tactical | 4→5 | Analyst (knowledge cell) → Detection engineer |
| "Review our PIRs" | Management | 1→6 | Orchestrator (PIR management, feedback loops) |
