---
name: intelligence-writing
description: Intelligence writing guide with product templates. BLUF, active voice, clear sourcing. Templates for all product types.
user-invocable: true
metadata:
  version: 1.0.0
---

# Intelligence Writing Guide

Intelligence writing is not creative writing. It is precise, structured, and audience-driven. Every word must earn its place.

## Core Principles

### 1. Bottom Line Up Front (BLUF)
The most important finding goes in the first paragraph. If the reader stops after two sentences, they should have the key takeaway.

**Bad**: "Over the past several months, we have observed various indicators that suggest a potential shift in threat actor targeting patterns across multiple sectors..."

**Good**: "APT41 is actively targeting European pharmaceutical companies using a new loader variant. We assess with high confidence that at least three organisations in this sector have been compromised since January 2026."

### 2. Active Voice
Use active voice. Name the actor.

- ❌ "The malware was deployed by the threat actor"
- ✅ "The threat actor deployed the malware"
- ❌ "It was assessed that..."
- ✅ "We assess that..."

### 3. Distinguish Facts, Assessments, and Assumptions

| Type | Signal words | Example |
|------|-------------|---------|
| **Fact** | "observed", "confirmed", "identified" | "We identified three C2 domains registered in January 2026." |
| **Assessment** | "we assess", "indicates", "suggests" | "We assess with high confidence that these domains are linked to APT41." |
| **Assumption** | "assuming", "if", "given that" | "Assuming the registration pattern continues, we expect additional infrastructure in Q2." |

### 4. Use Mandated Language
- Confidence levels: per the confidence-levels skill
- Likelihood language: per the likelihood-language skill
- Source assessment: per the source-assessment skill
- TLP: per the tlp-guide skill

### 5. Be Specific
- ❌ "Recently, a sophisticated threat actor..."
- ✅ "In March 2026, APT41 (also tracked as Winnti, Barium)..."
- ❌ "Multiple indicators were found"
- ✅ "We identified 14 IP addresses and 3 domain names associated with this campaign"

## Product Templates

### Flash Report
Time-critical intelligence requiring immediate attention. 1-2 pages maximum.

```markdown
---
title: "Flash Report: [Subject]"
type: flash-report
date: YYYY-MM-DD
tlp: AMBER
confidence: [level]
author: analyst
status: draft
related_pirs: []
mitre_attack: []
tags: []
---

# Flash Report: [Subject]
**TLP:[LEVEL]** | **Date:** YYYY-MM-DD | **Confidence:** [Level]

## Key Finding
[1-2 sentences. BLUF. What happened, who is affected, what should be done.]

## Details
[3-5 paragraphs maximum. What we know, how we know it, what it means.]

## Indicators of Compromise
| Type | Value | Context |
|------|-------|---------|
| IP | x.x.x.x | C2 server |
| Domain | example.com | Phishing landing page |
| SHA256 | abc123... | Loader variant |

## Recommended Actions
1. [Immediate action]
2. [Detection action]
3. [Investigation action]

## Sources
| Source | Reliability | Key Information |
|--------|------------|-----------------|
| [Source] | [Admiralty] | [What it contributed] |
```

### Intelligence Summary
Periodic overview of a topic or time period. 2-4 pages.

```markdown
---
title: "Intelligence Summary: [Subject/Period]"
type: intelligence-summary
date: YYYY-MM-DD
tlp: GREEN
confidence: [level]
author: analyst
status: draft
related_pirs: []
tags: []
---

# Intelligence Summary: [Subject/Period]
**TLP:[LEVEL]** | **Date:** YYYY-MM-DD | **Period:** [Coverage period]

## Executive Summary
[2-3 paragraphs. Key developments, trends, and implications.]

## Key Developments
### [Development 1]
[Assessment with confidence level and likelihood language where applicable.]

### [Development 2]
[...]

## Trend Analysis
[How does this period compare to previous? What's changing?]

## Outlook
[Forward-looking assessment using likelihood language.]

## Sources
[Sourcing table with Admiralty ratings]
```

### Threat Assessment
Structured assessment of a specific threat. 3-6 pages.

```markdown
---
title: "Threat Assessment: [Subject]"
type: threat-assessment
date: YYYY-MM-DD
tlp: AMBER
confidence: [level]
author: analyst
status: draft
related_pirs: []
mitre_attack: []
tags: []
---

# Threat Assessment: [Subject]
**TLP:[LEVEL]** | **Date:** YYYY-MM-DD | **Confidence:** [Level]

## Executive Summary
[BLUF: Overall threat level and key finding.]

## Threat Level: [CRITICAL/HIGH/MODERATE/LOW/NEGLIGIBLE]

## Intent
[What does the threat actor want to achieve? Evidence for assessed intent.]

## Capability
[What can the threat actor do? Technical sophistication, resources, tooling.]

## Opportunity
[What attack surface exists? Vulnerability landscape, exposure.]

## Assessment
[Combined analysis: Intent × Capability × Opportunity. Confidence and likelihood language.]

## Key Assumptions
[List and evaluate key assumptions underlying this assessment.]

## MITRE ATT&CK Mapping
| Tactic | Technique | Notes |
|--------|-----------|-------|
| Initial Access | T1566 Phishing | Primary delivery method |

## Recommended Mitigations
1. [Prioritised by impact]

## Sources
[Sourcing table with Admiralty ratings]
```

### Threat Actor Profile
Comprehensive profile of a threat group. 4-8 pages.

```markdown
---
title: "Threat Actor Profile: [Name/Designation]"
type: threat-actor-profile
date: YYYY-MM-DD
tlp: GREEN
confidence: [level]
author: analyst
status: draft
tags: []
---

# Threat Actor Profile: [Name/Designation]
**TLP:[LEVEL]** | **Last Updated:** YYYY-MM-DD

## Summary
| Field | Value |
|-------|-------|
| **Aliases** | [List all known aliases] |
| **Attribution** | [State/criminal group + confidence] |
| **Motivation** | [Espionage/Financial/Disruption/Hacktivism] |
| **Active Since** | [Year] |
| **Primary Targets** | [Sectors, geographies] |
| **Sophistication** | [Low/Medium/High/Advanced] |

## Overview
[2-3 paragraphs summarising the group, its activities, and significance.]

## Targeting
[Who they target, how targeting has evolved, victimology patterns.]

## TTPs (MITRE ATT&CK)
| Tactic | Technique | Description |
|--------|-----------|-------------|

## Tooling
| Tool | Type | First Seen | Notes |
|------|------|-----------|-------|

## Infrastructure
[Known infrastructure patterns, hosting preferences, C2 frameworks.]

## Campaign History
### [Campaign Name] (Date range)
[Summary of campaign, victims, TTPs, outcomes.]

## Intelligence Gaps
[What we don't know and need to collect.]

## Sources
[Sourcing table with Admiralty ratings]
```

### Campaign Report
Documentation of a specific campaign. 3-6 pages.

```markdown
---
title: "Campaign Report: [Name/Identifier]"
type: campaign-report
date: YYYY-MM-DD
tlp: AMBER
confidence: [level]
author: analyst
status: draft
related_pirs: []
mitre_attack: []
tags: []
---

# Campaign Report: [Name/Identifier]
**TLP:[LEVEL]** | **Date:** YYYY-MM-DD | **Confidence:** [Level]

## Executive Summary
[BLUF: Who, what, when, where, impact.]

## Timeline
| Date | Event |
|------|-------|
| YYYY-MM-DD | [Event description] |

## Attribution
[Assessment with confidence level. Link to threat actor profile.]

## Victimology
[Targeted organisations, sectors, geographies. Selection criteria if known.]

## Attack Chain
[Step-by-step technical description mapped to MITRE ATT&CK.]

## Diamond Model
| Vertex | Details |
|--------|---------|
| **Adversary** | [Actor/group] |
| **Capability** | [Tools, exploits, techniques] |
| **Infrastructure** | [C2, staging, delivery infrastructure] |
| **Victim** | [Targeted entities] |

## IOCs
[Full IOC table]

## Detection Guidance
[SIGMA/YARA/KQL rules or detection logic]

## Sources
[Sourcing table with Admiralty ratings]
```

## Writing Checklist

Before submitting any product:
- [ ] BLUF in first paragraph?
- [ ] TLP marking present and appropriate?
- [ ] All assessments carry confidence levels?
- [ ] All forward-looking statements use likelihood language?
- [ ] All sources assessed with Admiralty Scale?
- [ ] Facts distinguished from assessments?
- [ ] Active voice throughout?
- [ ] Specific dates, numbers, and names (not "recently" or "several")?
- [ ] Key assumptions identified?
- [ ] MITRE ATT&CK techniques mapped where applicable?
