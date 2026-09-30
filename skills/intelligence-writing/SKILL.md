---
name: intelligence-writing
description: Use when writing a finished intelligence product, the user asks for a flash-report / threat-assessment / briefing / FINTEL template, or wants the BLUF + active-voice + clear-sourcing conventions. Covers all product types.
user-invocable: true
metadata:
  version: 1.1.0
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
- Source assessment: per the source-assessment skill (the Admiralty scale, for lookup results and single items) and the quality-of-information-check skill (the evidence grade, access level and claim support, for claims from documents and articles). Neither is converted into the other
- TLP: per the tlp-guide skill

### 5. Be Specific
- ❌ "Recently, a sophisticated threat actor..."
- ✅ "In March 2026, APT41 (also tracked as Winnti, Barium)..."
- ❌ "Multiple indicators were found"
- ✅ "We identified 14 IP addresses and 3 domain names associated with this campaign"

### 6. Write From Claims, Not From Articles
A product is best written from graded claims, not from raw articles. The input is the claim table from `/claim-extraction` or the graded evidence items from `/quality-of-information-check`. If you are handed raw URLs or pasted reports, run `/quality-of-information-check` first. If the user asks to skip it, write from the material as given, say in the sourcing paragraph that the evidence was not graded, and keep confidence at Moderate or below.

- Each statement in the product traces to a claim ID. Observations are written as facts, attribution and assessment claims as assessments (see principle 3).
- Keep the primary's hedge. If the primary says "possibly linked to", the product does not say "attributed to", whatever the outlet wrote.
- Confidence in a judgment cannot exceed what its weakest load-bearing claim supports.
- Actor claims (victim counts, data volumes) are reported as the actor's claim, never as a finding.

## Sourcing

### Cite the Primary, Not the Outlet
The Sources section lists the originating source of each claim. The outlet that carried it is listed as "via". Five outlets covering one vendor report are one row. Every product template below uses this table for its Sources section:

```markdown
| Primary source | Via | Access | Access level | Claim support | Claims supported |
|----------------|-----|--------|--------------|---------------|------------------|
| [Org, report title, date] | [Outlet(s), or "direct"] | [telemetry / ir_engagement / sample_analysis / osint / undisclosed] | [e.g., direct for C01-C04] | [e.g., firm for C01-C03, tentative for C04] | [What it contributed] |
| Unresolved | [Outlet] | none | untraced | [tentative at best] | [What it contributed] |
```

Grades are per claim. Where one primary supports claims with different grades, give each.

### Sourcing Paragraph
Every product carries a short Sourcing paragraph directly above the Sources table, in the style of ICD 206. It states, in prose:

1. **Source descriptors**: how many primaries, of what type (vendor, government, victim, actor, researcher).
2. **Stated access**: how each primary says it knows (own telemetry, incident response engagement, sample analysis, open sources), or "access undisclosed". Taken from the primary's own text, never from its reputation.
3. **Derivative or original**: whether we read the primary directly or received it through press coverage, and whether any caveat was dropped on the way.
4. **Single-source flagging**: which judgments rest on one primary.
5. **Provenance basis**: `platform-resolved`, `script-resolved` or `model-judged`, carried through from the QoI output.

Template:

```markdown
## Sourcing
This product draws on [N] originating source(s): [descriptor, e.g., "one security vendor and one government advisory"]. [Primary 1] states its findings come from [stated access]; [Primary 2] [stated access, or "does not disclose its access"]. We reviewed [the primary reporting directly / press coverage by [outlets], which is derivative of [primary]]. [Where relevant: "Press coverage strengthened the vendor's wording; this product uses the vendor's own wording."] The judgment that [X] rests on a single source. [The government advisory cites the vendor report and adds no independent evidence, so it is not counted as corroboration.] Provenance basis: [platform-resolved / script-resolved / model-judged (unverified)]. The weakest load-bearing claim is [claim, access level and claim support].
```

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

## Sourcing
[Sourcing paragraph, 2-3 sentences for a flash report]

## Sources
| Primary source | Via | Access | Access level | Claim support | Claims supported |
|----------------|-----|--------|--------------|---------------|------------------|
| [Primary] | [Outlet or "direct"] | [Access] | [Per claim] | [Per claim] | [What it contributed] |
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

## Sourcing
[Sourcing paragraph]

## Sources
[Sources table: primary, via, access, per-claim access level and claim support]
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

## Sourcing
[Sourcing paragraph]

## Sources
[Sources table: primary, via, access, per-claim access level and claim support]
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

## Sourcing
[Sourcing paragraph]

## Sources
[Sources table: primary, via, access, per-claim access level and claim support]
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

## Sourcing
[Sourcing paragraph]

## Sources
[Sources table: primary, via, access, per-claim access level and claim support]
```

## Writing Checklist

Before submitting any product:
- [ ] BLUF in first paragraph?
- [ ] TLP marking present and appropriate?
- [ ] All assessments carry confidence levels?
- [ ] All forward-looking statements use likelihood language?
- [ ] Written from graded claims, not raw articles?
- [ ] Every claim from a document graded with access level and claim support, per claim, written in words?
- [ ] Sources section cites the primary, with the outlet as "via"?
- [ ] Sourcing paragraph present, with single-source judgments flagged and provenance basis stated?
- [ ] Facts distinguished from assessments?
- [ ] Active voice throughout?
- [ ] Specific dates, numbers, and names (not "recently" or "several")?
- [ ] Key assumptions identified?
- [ ] MITRE ATT&CK techniques mapped where applicable?
