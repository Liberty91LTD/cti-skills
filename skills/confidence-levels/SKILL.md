---
name: confidence-levels
description: Use when assigning a confidence level to an analytical judgment, the user asks "how confident are we?" / "what is the confidence on X?", or the orchestrator's tradecraft pipeline calls for a confidence level before publishing. Provides three named levels (High, Moderate, Low) with 0-100 score ranges aligned to STIX, and the rule that confidence cannot exceed what the weakest load-bearing claim supports.
user-invocable: true
metadata:
  version: 2.0.0
---

# Confidence Levels

Every analytical judgment produced by this platform MUST carry a confidence level. Confidence reflects the quality and quantity of evidence supporting the judgment, NOT the probability that the event will occur (that's likelihood — see likelihood-language skill).

## Primary Scale: Named Bands

Three levels, following ICD 203. Each band is tied to the claim support of the evidence underneath, as graded by `/quality-of-information-check`. On export, STIX `confidence` comes from claim support: established 90, firm 70, tentative 50, disputed 30, and unverified omits the property. These values are the pack's own mapping, chosen to sit inside the bands below, so a confidence level, a STIX `confidence` value and the grade of the evidence underneath all say the same thing.

| Band | Score Range | Meaning | Evidence it requires |
|------|-----------|---------|---------|
| **High** | 80-100 | Based on high-quality information from multiple independent sources. Well corroborated. High confidence does not mean the judgment is a fact. | Every load-bearing claim at claim support established, with access level direct or limited |
| **Moderate** | 60-79 | Based on credibly sourced and plausible information that is not corroborated enough to warrant higher confidence. Alternative interpretations exist. | Weakest load-bearing claim at claim support firm, or established with access level indirect |
| **Low** | 40-59 | Based on limited or fragmentary information, or on a judgment the source itself hedged. Several plausible alternative interpretations. | Weakest load-bearing claim at claim support tentative |
| **No confidence level** | none | The evidence cannot carry a judgment. Do not attach a label. State what is known, state the gap, and say what collection would close it. | Any load-bearing claim at claim support disputed or unverified |

Scores below 40 are not used. A judgment that would score there is not one the evidence supports, and it gets no confidence level.

### The ceiling

Confidence in a judgment is bounded above by the weakest load-bearing claim. Grades come from `/quality-of-information-check`. The ceiling rules, including the effect of access level, are in `/threat-assessment` under "Confidence Ceiling". First-party observation, a hit in the organisation's own telemetry, is graded direct, established and is the top of the scale.

The ceiling is a maximum, not a target. Weak reasoning or untested assumptions lower confidence further. Nothing raises it above the ceiling.

Before version 2.0 this skill had five bands, Very Low to Very High. Products written on that scale should be re-rated, not converted by arithmetic.

## What Determines Confidence

Confidence is determined by three factors:

### 1. Quality of Sources
- How do the sources know, and what backs each claim? (The evidence grade from `/quality-of-information-check` for claims from documents. The Admiralty scale from `/source-assessment` for lookup results and single items. Neither is converted into the other.)
- Are sources independent or derivative?
- Is there potential for deception or disinformation?

### 2. Quantity and Corroboration
- How many independent sources support the assessment?
- Do sources confirm each other or contradict?
- Is the evidence diverse (technical + human + open source)?

### 3. Analytical Logic
- How strong is the analytical reasoning?
- Have key assumptions been tested?
- Have alternative hypotheses been considered and evaluated?

## How to Express Confidence

### In text
> "We assess with **high confidence** that APT28 is responsible for this campaign, based on infrastructure overlaps with three previously attributed operations and consistent TTP alignment documented by two independent vendors."

### In frontmatter
```yaml
confidence: high
confidence_score: 82
confidence_rationale: "Based on corroboration from CrowdStrike and Microsoft reporting, plus internal telemetry matching known APT28 C2 patterns."
```

### In tables/structured output
| Assessment | Confidence | Rationale |
|-----------|-----------|-----------|
| APT28 attribution | High (82) | 3 independent source corroboration + TTP match |

## Confidence vs Likelihood

These are DIFFERENT concepts:

- **Confidence**: How sure are we about our assessment? (evidence quality)
- **Likelihood**: How probable is a future event? (predictive judgment)

Example:
> "We assess with **high confidence** that Group X has the capability to target financial sector organisations. It is **likely** (50-75%) that they will conduct such operations in the next 12 months."

The confidence in the capability assessment is high (strong evidence). The likelihood of future targeting is a separate judgment.

## Calibrating Confidence

### Upgrade confidence when:
- New independent source corroborates the assessment
- Technical evidence directly supports the judgment
- Key assumptions are validated through testing

### Downgrade confidence when:
- A previously reliable source is found to have errors
- New information contradicts a key assumption
- Evidence turns out to be derivative (multiple reports trace back to one source)

## Common Mistakes

- Conflating confidence with likelihood ("high confidence it will happen" — this is two concepts mashed together)
- Not explaining WHY confidence is at a given level (always include rationale)
- Defaulting to "moderate" to avoid commitment — if the evidence is strong, say so
- Giving high confidence on uncorroborated evidence — one primary with direct access is claim support firm, which supports moderate at most
- Attaching a low-confidence label where the evidence supports no judgment at all
- Changing confidence based on desired outcome rather than evidence
- Treating confidence as static — reassess when new evidence emerges
