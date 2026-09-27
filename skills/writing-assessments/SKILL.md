---
name: writing-assessments
description: Use when the user asks to write a threat / risk / vulnerability assessment, or wants the appropriate template for each type. Distinct structures and section ordering per assessment kind. Requires graded evidence items from /quality-of-information-check and runs that skill first when handed raw URLs or text. Confidence is capped by the weakest load-bearing claim.
user-invocable: true
metadata:
  version: 2.0.0
---

# Writing Assessments

Three types of assessments, each with distinct purpose and structure. Do not conflate them.

## Precondition: Graded Evidence Only

Reporting used as evidence must arrive as graded evidence items, one per claim, as produced by `/quality-of-information-check` (the QoI JSON or its claim table). The schema is in `skills/quality-of-information-check/references/evidence-item-schema.md`.

- Handed a QoI output: proceed.
- Handed raw URLs, articles, vendor reports or pasted text: invoke `/quality-of-information-check` first, passing the assessment question so it can mark which claims are load-bearing. Build the assessment from its output.
- Handed a mix: grade the ungraded material before starting.
- If `/quality-of-information-check` cannot be run, or the user asks to skip it, do not write the assessment. Tell the user: "I can't write this assessment yet. Its confidence level is set by the weakest claim the conclusion depends on, and this evidence has not been graded. Give me the URLs or report text and I will run /quality-of-information-check first, or hand me an existing QoI output."

Three kinds of input are not reports. They are handled differently from each other:

| Input | What it is | How it is treated |
|---|---|---|
| **First-party observation**: a hit in the organisation's own telemetry (`/lookup-sentinel`, EDR, internal incident records) | The best-graded evidence there is | An evidence item graded **A1**, `claim_type: observation`, `access: telemetry`, source "user environment", `provenance_basis: first-party` (rubric rule R12). It participates fully, can be load-bearing, and can raise the ceiling. A miss is not evidence of absence and is not an item |
| **KEV listing** | A claim by CISA that exploitation has been observed | Evidence. Graded like any government claim through `/quality-of-information-check` |
| **CVSS and EPSS** | Attributes of a CVE | Not claims and not evidence about the event. They do not enter the claim table and have no effect on the ceiling. List them in Sources as reference data |

## Confidence Ceiling: The Weakest Link

The confidence level of the assessment cannot exceed what the weakest load-bearing claim supports. Apply the table below to every item with `load_bearing: true`. The lowest result is the ceiling, and the claim that produced it is the weakest link. This is the claim named in `event_qoi_summary.weakest_link`, which uses the same bands.

| Weakest load-bearing claim | Maximum confidence |
|---|---|
| Credibility 1, with reliability A or B | **High** |
| Credibility 2, or credibility 1 with reliability C | **Moderate** |
| Credibility 3 | **Low** |
| Credibility 4, 5 or 6 | **No confidence level.** State the gap |

Reliability D, E or F lowers the result by one level, so a D3 or F3 claim carrying the conclusion gives no confidence level.

Why the threshold for High is credibility 1: high confidence is for judgments resting on high-quality information from more than one source. Credibility 2 is, by the rubric's own definition, a single primary with direct access and no independent confirmation. Credibility 1 is the independently confirmed grade.

Where a numeric score is required, it stays inside the band for that level in `/confidence-levels`: 80 to 100 for High, 60 to 79 for Moderate, 40 to 59 for Low.

When the ceiling is "no confidence level", do not publish a judgment with a confidence label. Write what is known, state that the claim the conclusion depends on cannot carry it, and say what collection would change that.

Rules:
- This is a ceiling, not a target. Weak analytical logic or untested assumptions lower confidence further. Nothing raises it above the ceiling.
- Claims flagged `press_originated` and claims with `load_bearing: false` cannot carry the conclusion. If the conclusion needs one of them, the user must promote it, and it then counts as the weakest link.
- To raise the ceiling, corroborate the weakest link or rewrite the conclusion so it no longer depends on that claim. Do not drop the claim from Sources to get a higher level.
- State the weakest link in the confidence rationale, by `claim_id` and grade:

> "Confidence: low. The weakest load-bearing claim is C04 (attribution, A3): a single primary stating moderate confidence, corroboration unchecked. Core observations are A2, which would support moderate. Independent confirmation of the attribution would raise the ceiling."

This applies to all three assessment types below.

## Threat Assessment

**Purpose**: Evaluate a threat actor or threat scenario against a specific target.

**Formula**: Threat = Intent + Capability + Opportunity

### Structure

**1. Intent** — What does the adversary want?
- Stated objectives (if known)
- Historical targeting patterns
- Geopolitical/economic motivations
- Assessment of intent with confidence level

**2. Capability** — What can the adversary do?
- Technical sophistication
- Resources (financial, human, infrastructure)
- Known tooling and TTPs
- Track record of successful operations
- Assessment of capability with confidence level

**3. Opportunity** — What attack surface exists?
- Target's exposure (internet-facing services, supply chain)
- Known vulnerabilities relevant to the adversary's TTPs
- Access pathways (initial access vectors)
- Defensive posture gaps
- Assessment of opportunity with confidence level

**4. Combined Threat Level**

| Level | Criteria |
|-------|---------|
| **Critical** | Demonstrated intent, advanced capability, and clear opportunity. Attack is imminent or ongoing. |
| **High** | Strong intent indicators, significant capability, and exploitable opportunity. Attack is highly likely in assessment period. |
| **Moderate** | Some intent indicators, moderate capability, and some opportunity. Attack is a realistic possibility. |
| **Low** | Limited intent indicators, basic capability, or minimal opportunity. Attack is unlikely. |
| **Negligible** | No credible intent, minimal capability, or no meaningful opportunity. |

### Example assessment statement
> "We assess the threat level from APT41 to European pharmaceutical companies as **HIGH** (confidence: moderate). APT41 has demonstrated intent through active reconnaissance (observed since November 2025), possesses advanced capability including zero-day exploitation, and the sector presents significant opportunity due to widespread legacy VPN infrastructure. The weakest load-bearing claim is C03 (observation, B2): the reconnaissance activity, reported by a single primary from its own telemetry."

## Risk Assessment

**Purpose**: Evaluate the potential impact of a threat materialising.

**Formula**: Risk = Threat × Vulnerability × Impact

### Structure

**1. Threat** (reference or summarise from threat assessment)
- Threat level from threat assessment
- Key threat characteristics

**2. Vulnerability** — How exposed is the target?
- Technical vulnerabilities (CVEs, misconfigurations)
- Process vulnerabilities (gaps in detection, response)
- Human vulnerabilities (social engineering susceptibility)
- Supply chain vulnerabilities

**3. Impact** — What happens if the threat materialises?
- Operational impact (business disruption, data loss)
- Financial impact (direct costs, regulatory fines, market impact)
- Reputational impact (customer trust, brand damage)
- Strategic impact (competitive advantage, IP loss)
- Impact severity: Critical / High / Moderate / Low / Negligible

**4. Combined Risk Level**

Use a risk matrix:

|  | Negligible Impact | Low Impact | Moderate Impact | High Impact | Critical Impact |
|--|---|---|---|---|---|
| **Critical Threat** | Moderate | High | Very High | Very High | Very High |
| **High Threat** | Low | Moderate | High | Very High | Very High |
| **Moderate Threat** | Low | Low | Moderate | High | Very High |
| **Low Threat** | Very Low | Low | Low | Moderate | High |
| **Negligible Threat** | Very Low | Very Low | Low | Low | Moderate |

### Example assessment statement
> "The risk of APT41 compromising sensitive R&D data is assessed as **VERY HIGH** (confidence: moderate). The high threat level (demonstrated intent and capability) combined with critical impact (loss of proprietary pharmaceutical research valued at €500M+) and significant vulnerability (unpatched VPN appliances matching APT41's known initial access vector) drive this assessment."

## Vulnerability Assessment

**Purpose**: Evaluate the exploitability and impact of a specific vulnerability.

**Formula**: Vulnerability Severity = Exposure + Susceptibility − Resilience

### Structure

**1. Vulnerability Description**
- CVE identifier (if applicable)
- Affected systems/software
- Technical description of the vulnerability

**2. Exposure** — How visible/accessible is the vulnerable system?
- Internet-facing vs internal only
- Number of affected systems
- Public availability of exploit code (PoC, weaponised)

**3. Susceptibility** — How easy is it to exploit?
- CVSS base score
- EPSS (Exploit Prediction Scoring System) score
- Technical complexity of exploitation
- Authentication requirements
- Known exploitation in the wild (CISA KEV listing)

**4. Resilience** — What mitigations exist?
- Patch availability
- Compensating controls
- Detection capability (do we have rules for this?)
- Recovery capability

**5. Prioritisation**

| Priority | Criteria |
|----------|---------|
| **P1 — Patch immediately** | Actively exploited OR high EPSS + internet-facing + no compensating controls |
| **P2 — Patch within 72h** | PoC available + internet-facing OR actively exploited + internal with compensating controls |
| **P3 — Patch within 30 days** | High CVSS + no active exploitation + compensating controls in place |
| **P4 — Patch in next cycle** | Moderate CVSS + internal only + compensating controls |
| **P5 — Accept risk** | Low CVSS + internal only + strong compensating controls + low impact |

## General Assessment Writing Rules

1. **Always state the assessment explicitly** — "We assess that..." not "It appears that..."
2. **Always include confidence level** — Per confidence-levels skill, never above the weakest-link ceiling, with the weakest link named in the rationale
3. **Always use likelihood language** — Per likelihood-language skill for future-looking statements
4. **Always identify key assumptions** — What must be true for this assessment to hold?
5. **Always separate facts from judgments** — Per intelligence-writing skill
6. **Never hedge-stack** — Pick one likelihood band, don't combine ("likely or highly likely")
7. **Always include temporal scope** — "Over the next 12 months" not "in the future"
8. **Always cite the primary** — Sources name the originating organisation, not the outlet that carried the story

## Sources Section (all assessment types)

Every assessment ends with this section, filled from the graded evidence items.

```markdown
### Sources
**Provenance basis**: [platform-resolved / script-resolved / model-judged (unverified)]

| claim_id | Claim | claim_type | Primary (org, title, date) | Grade | Independent primaries (basis) | Flags |
|----------|-------|------------|----------------------------|:---:|:---:|-------|
| C01 | [claim] | observation | [Vendor], "[Report title]", YYYY-MM-DD | A2 | 1 (unchecked) | single_source |

[Cite the primary, not the outlet that carried it. Several outlets covering one primary are one source. First-party observations appear in the table as graded items. CVSS and EPSS are listed separately as reference data.]
```
