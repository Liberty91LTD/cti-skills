---
name: pir-management
description: Use when the user asks to create, review, retire, or refine Priority Intelligence Requirements, or wants to align collection and analysis to the current PIR set. Covers the PIR lifecycle end-to-end.
user-invocable: true
metadata:
  version: 1.0.0
---

# Priority Intelligence Requirements (PIR) Management

PIRs are the foundation of relevant intelligence. They define what stakeholders need to know and drive all collection and analysis priorities. Without PIRs, a CTI team produces intelligence nobody asked for.

## What is a PIR?

A PIR is a question that, when answered, directly supports a stakeholder's decision-making. PIRs are:
- **Stakeholder-driven** — not what the analyst finds interesting
- **Decision-oriented** — answering them enables action
- **Bounded** — specific enough to collect against
- **Reviewable** — can be assessed for satisfaction

## PIR Format (SMART)

Each PIR should be:
- **S**pecific: Clear scope and focus
- **M**easurable: Can determine when it's answered
- **A**chievable: Can be collected against with available resources
- **R**elevant: Directly supports stakeholder decisions
- **T**ime-bound: Has a review/expiry date

### PIR Template

Store in `data/pirs/active/PIR-XXX-<slug>.md`:

```yaml
---
pir_id: PIR-001
title: "What ransomware groups are actively targeting the European healthcare sector?"
created: 2026-01-15
review_date: 2026-04-15
status: active
priority: high
stakeholder: CISO
collection_sources: [osint, virustotal, otx]
knowledge_cells: [ransomware-ecosystem]
last_satisfied: 2026-03-01
satisfaction_count: 3
---

## Context
Why this PIR matters to the stakeholder. What decisions depend on the answer.

## Standing Requirements
- Monitor for new ransomware campaigns targeting healthcare
- Track ransomware group infrastructure changes
- Assess likelihood of targeting our specific organisation

## Collection Guidance
- OSINT: Monitor vendor reports, ISAC feeds, government advisories
- Technical: Enrich IOCs from healthcare-targeted campaigns
- Dark web: Monitor ransomware leak sites for healthcare victims

## Satisfaction History
| Date | Product | Summary |
|------|---------|---------|
| 2026-03-01 | Flash Report FR-2026-03-01 | New BlackCat campaign targeting EU hospitals |
| 2026-02-15 | Intelligence Summary IS-2026-02-15 | Monthly ransomware landscape update |
```

## PIR Lifecycle

### 1. Creation
- Stakeholder engagement: "What do you need to know to do your job?"
- Draft PIR in SMART format
- Assign priority (Critical / High / Medium / Low)
- Map to collection sources and knowledge cells
- Set review date (default: quarterly)

### 2. Collection Planning
For each active PIR:
- Identify collection sources that can answer it
- Set up standing collection tasks
- Map to relevant knowledge cells for context
- Document collection guidance

### 3. Satisfaction
When intelligence answering a PIR is produced:
- Link the product to the PIR
- Update `last_satisfied` date
- Increment `satisfaction_count`
- Add to satisfaction history

### 4. Review (Quarterly)
For each active PIR:
- Is this still relevant to the stakeholder?
- Has it been satisfactorily answered?
- Should priority change?
- Should scope be adjusted?
- Should it be retired?

### 5. Retirement
When a PIR is no longer needed:
- Set `status: retired`
- Move from `data/pirs/active/` to `data/pirs/archive/`
- Document reason for retirement

## PIR Priority Guide

| Priority | Criteria | Collection Effort |
|----------|---------|-------------------|
| **Critical** | Imminent threat to organisation, board-level concern, regulatory requirement | Dedicated resources, daily monitoring |
| **High** | Active threat landscape relevant to organisation, CISO priority | Regular monitoring, weekly reporting |
| **Medium** | General awareness need, emerging threat area | Periodic collection, monthly reporting |
| **Low** | Background intelligence, professional development | Opportunistic collection |

## Common PIR Examples

### Strategic PIRs
- "What nation-state actors are likely to target our sector in the next 12 months?"
- "How is the ransomware threat landscape evolving, and what are the implications for our risk posture?"
- "What emerging technologies or attack vectors could change our threat profile?"

### Operational PIRs
- "What TTPs are currently being used against organisations in our sector?"
- "Which vulnerabilities are being actively exploited that affect our technology stack?"
- "Are there any active campaigns targeting our supply chain?"

### Tactical PIRs
- "What IOCs are associated with current campaigns targeting our sector?"
- "What detection rules should we prioritise for the current threat landscape?"
- "Are any of our assets or credentials appearing on dark web marketplaces?"

## Orchestrator Integration

The orchestrator should:
1. Check active PIRs before starting any new work
2. Route collection and analysis tasks to relevant PIRs
3. Tag all products with related PIR IDs
4. Alert when a Critical PIR hasn't been satisfied in 30+ days
5. Facilitate quarterly PIR reviews
