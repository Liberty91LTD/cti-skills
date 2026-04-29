---
name: stakeholder-management
description: Use when the user asks "who are our customers?" / "how do we tailor for X stakeholder?" / "who should this report go to?", or wants to map / re-map stakeholder needs. Ensures intelligence reaches the right people in the right format.
user-invocable: true
metadata:
  version: 1.0.0
---

# Stakeholder Management

Intelligence that doesn't reach the right person in the right format might as well not exist. This skill ensures every product is tailored to its audience.

## Stakeholder Identification

### Common CTI Stakeholders

| Stakeholder | Needs | Format | Cadence |
|-------------|-------|--------|---------|
| **CISO** | Strategic risk, business impact, investment justification | Executive summary, risk scores, trend analysis | Monthly + ad-hoc |
| **SOC Manager** | Operational context, detection priorities, hunt leads | Operational briefs, IOC packages, hunt playbooks | Weekly + real-time |
| **SOC Analysts** | Tactical indicators, detection rules, response guidance | IOCs, SIGMA/YARA rules, enriched alerts | Daily + real-time |
| **IR Team** | Campaign context, TTP detail, forensic indicators | Detailed campaign reports, investigation leads | Per-incident |
| **Security Architecture** | Threat landscape, emerging attack vectors, control gaps | Threat assessments, ATT&CK mapping, control recommendations | Quarterly |
| **Risk Management** | Threat trends, probability assessments, sector comparisons | Risk assessments, likelihood language, quantified impact | Quarterly |
| **Board / Executive** | High-level risk posture, material incidents, peer benchmarks | 1-page dashboard, non-technical language, visual aids | Quarterly + material events |
| **Legal / Compliance** | Regulatory threat intelligence, breach notification triggers | Compliance-focused briefs, attribution (when needed) | Ad-hoc |
| **IT Operations** | Vulnerability intelligence, patch priorities, asset exposure | Vulnerability assessments, prioritised patch lists | Weekly |

## Stakeholder Register Template

Maintain in `data/pirs/stakeholder-register.md`:

```markdown
| Stakeholder | Role | PIRs | Products | Format Preference | Cadence | Feedback Method |
|-------------|------|------|----------|-------------------|---------|-----------------|
| [Name/Title] | [Role] | PIR-001, PIR-003 | Threat assessments, weekly brief | Executive summary, max 1 page | Monthly | Email response |
```

## Tailoring Intelligence Products

### For Executives (CISO, Board)
- **Lead with business impact**, not technical detail
- Use risk language: "This threat could result in..."
- Include peer comparisons: "Organisations in our sector have seen..."
- Recommend actions in business terms: "Investment in X reduces risk by..."
- Maximum 1-2 pages
- Visual aids (charts, traffic lights, risk matrices)

### For Security Operations (SOC, IR)
- **Lead with actionable indicators**
- Include detection rules and hunt queries
- Provide full TTP chain with ATT&CK mapping
- Technical detail is expected and valued
- Response playbook pointers
- Real-time delivery for active threats

### For Risk / Compliance
- **Lead with likelihood and impact assessments**
- Use standardised likelihood language (probability yardstick)
- Map to frameworks (NIST CSF, ISO 27001)
- Quantify where possible
- Regulatory implications highlighted

## Dissemination Matrix

| TLP | Distribution Channel | Notes |
|-----|---------------------|-------|
| RED | Direct communication only (in-person, encrypted message) | Named recipients only |
| AMBER+STRICT | Internal secure channel (encrypted email, restricted SharePoint) | Organisation only |
| AMBER | Secure channel + need-to-know partners | May share with clients/partners |
| GREEN | Community channels (ISAC portal, closed mailing lists) | Not public |
| CLEAR | Any channel (blog, public advisories) | Unrestricted |

## Feedback Collection

After every significant product delivery:
1. Was the intelligence useful? (Yes/Partially/No)
2. Was it timely? (Yes/Too late/Too early)
3. Was the format appropriate? (Yes/Too technical/Too high-level)
4. What should we cover next? (Free text)

Track feedback in stakeholder register. Feed into PIR refinement (see feedback-loops skill).
