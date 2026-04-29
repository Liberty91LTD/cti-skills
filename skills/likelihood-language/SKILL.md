---
name: likelihood-language
description: Use when phrasing a forward-looking statement, the user asks "how likely is X?" / "what's the likelihood?", or the tradecraft pipeline applies a probability yardstick to a finished product. Standardised likelihood language across all products.
user-invocable: true
metadata:
  version: 1.0.0
---

# Likelihood Language — Probability Yardstick

Every forward-looking assessment (prediction, forecast, risk statement) MUST use standardised likelihood language. Never use vague terms like "could", "might", or "may" without mapping them to a probability band.

## The Yardstick

| Term | Probability Range | Usage |
|------|------------------|-------|
| **Almost certain** | >95% | Use sparingly. Reserved for near-inevitable outcomes with overwhelming evidence. |
| **Highly likely** | 75-95% | Strong evidence supporting the assessment. Limited plausible alternatives. |
| **Likely** | 50-75% | The weight of evidence supports this outcome, but meaningful alternatives exist. |
| **Realistic possibility** | 25-50% | Plausible outcome that cannot be discounted. Evidence is mixed or limited. |
| **Unlikely** | 15-25% | Possible but not supported by the weight of evidence. |
| **Highly unlikely** | 5-15% | Very limited evidence suggests this outcome. Most evidence points elsewhere. |
| **Remote** | <5% | Theoretically possible but requires multiple unlikely conditions to align. |

## How to Use

### Correct usage
> "It is **highly likely** (75-95%) that the threat actor will shift targeting to the financial sector in Q3, based on observed reconnaissance activity and historical pattern of seasonal targeting shifts."

> "There is a **realistic possibility** (25-50%) that the exploit will be weaponised within 30 days, given the availability of a proof-of-concept but no evidence of active exploitation."

### Incorrect usage
> "The threat actor might target financial services." ❌ (No probability band)
> "It could happen in Q3." ❌ (Vague, unquantified)
> "We think it's likely but also possible that..." ❌ (Contradictory — pick one band)

## Combining with Confidence

Likelihood and confidence are independent dimensions:

> "We assess with **moderate confidence** that it is **likely** (50-75%) that Group X will conduct destructive operations against energy sector targets in the next 6 months."

- **Moderate confidence**: We have some evidence but key assumptions are not fully validated
- **Likely**: Based on available evidence, the probability falls in the 50-75% range

A low-confidence assessment CAN have a high likelihood term — it means "if our assessment is correct, the probability is high, but we're not fully sure our assessment is correct."

## When NOT to Use Likelihood Language

- **Statements of fact**: "APT28 used Fancy Bear malware in this campaign" — this is a factual claim, not a prediction. Use confidence levels instead.
- **Historical analysis**: "The campaign began in January 2025" — past events don't need likelihood language.
- **Definitions and descriptions**: "SIGMA rules are detection rules written in YAML" — informational, not predictive.

## Mapping Informal Language

If you catch yourself writing informal probabilistic language, map it:

| Informal | Map to |
|----------|--------|
| "could", "may", "might" | Determine which band and use proper term |
| "probably" | Likely (50-75%) or Highly likely (75-95%) |
| "possibly" | Realistic possibility (25-50%) |
| "unlikely" | Already a valid term — check it maps to 15-25% |
| "almost certainly" | Almost certain (>95%) |
| "there's a chance" | Determine probability and use proper term |
| "can't rule out" | Realistic possibility (25-50%) or Unlikely (15-25%) |

## Common Mistakes

- Using multiple likelihood terms in one assessment ("likely or highly likely") — commit to one
- Hedging with "possible" instead of making a judgment — if evidence is weak, say "unlikely" with rationale
- Forgetting to include the percentage range in parentheses — always include for clarity
- Confusing likelihood with confidence (see confidence-levels skill)
- Using "almost certain" casually — this is >95% and should be rare
