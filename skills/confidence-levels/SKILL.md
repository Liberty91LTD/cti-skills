---
name: confidence-levels
description: Use when assigning a confidence level to an analytical judgment, the user asks "how confident are we?" / "what is the confidence on X?", or the orchestrator's tradecraft pipeline calls for a confidence level before publishing. Provides the MISP 0-100 scale and qualitative-band mapping.
user-invocable: true
metadata:
  version: 1.0.0
---

# Confidence Levels

Every analytical judgment produced by this platform MUST carry a confidence level. Confidence reflects the quality and quantity of evidence supporting the judgment, NOT the probability that the event will occur (that's likelihood — see likelihood-language skill).

## Primary Scale: Named Bands

| Band | Score Range | Meaning |
|------|-----------|---------|
| **Very High** | 90-100 | Based on high-quality information from multiple independent sources. Analyst has no significant concerns about the validity of the sources. Well-corroborated assessment. |
| **High** | 75-89 | Based on high-quality information, or from multiple sources with minor inconsistencies. Key assumptions are well-supported. |
| **Moderate** | 50-74 | Based on credible information that is not sufficient to warrant higher confidence. Key assumptions are reasonable but not fully validated. Alternative interpretations exist. |
| **Low** | 25-49 | Based on limited or fragmentary information. Key assumptions have significant uncertainty. Multiple plausible alternative interpretations. |
| **Very Low** | 0-24 | Based on sparse, unreliable, or largely circumstantial information. Assessment is essentially speculative. |

## What Determines Confidence

Confidence is determined by three factors:

### 1. Quality of Sources
- How reliable are the sources? (Cross-reference with Admiralty Scale)
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
- Changing confidence based on desired outcome rather than evidence
- Treating confidence as static — reassess when new evidence emerges
