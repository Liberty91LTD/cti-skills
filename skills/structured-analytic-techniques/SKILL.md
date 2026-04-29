---
name: structured-analytic-techniques
description: Use when the user asks "which SAT should I use for X?", wants the index of Structured Analytic Techniques, or is choosing between ACH, key-assumptions-check, red-team-analysis, indicators of change, etc.
user-invocable: true
metadata:
  version: 1.0.0
---

# Structured Analytic Techniques (SATs) Index

SATs are formal methods that externalise analytical thinking, making it transparent, challengeable, and less susceptible to cognitive biases. Choose the right technique based on the analytical challenge.

## When to Use SATs

- When the stakes are high (wrong answer = significant consequence)
- When multiple plausible explanations exist
- When cognitive biases are likely (confirmation, anchoring, availability)
- When you need to communicate your reasoning transparently
- When building on analysis from multiple analysts

## Technique Categories

### Diagnostic Techniques
**Purpose**: Evaluate existing analysis for quality and bias.

| Technique | When to Use | Skill |
|-----------|-------------|-------|
| **Key Assumptions Check** | Before or after any major assessment — surface and challenge unstated assumptions | `key-assumptions-check` |
| **Quality of Information Check** | When evidence quality is uncertain — assess source reliability and information gaps | Use `source-assessment` skill |
| **Indicators Validation** | When monitoring a developing situation — define observable markers of change | Part of horizon-scanning |

### Contrarian Techniques
**Purpose**: Challenge prevailing judgments and expose blind spots.

| Technique | When to Use | Skill |
|-----------|-------------|-------|
| **Analysis of Competing Hypotheses** | Multiple plausible explanations — systematically evaluate each against evidence | `ach` |
| **Devil's Advocate / Red Team** | When consensus is strong — deliberately argue the opposing position | `red-team-analysis` |
| **What-If Analysis** | Explore low-probability but high-impact scenarios | Part of horizon-scanning |
| **High-Impact / Low-Probability** | Ensure unlikely but catastrophic scenarios are considered | Combine `threat-assessment` + `horizon-scanning` |

### Imaginative Techniques
**Purpose**: Generate new ideas, hypotheses, and indicators.

| Technique | When to Use | Skill |
|-----------|-------------|-------|
| **Brainstorming** | Generate hypotheses, IOC types to collect, detection approaches | No dedicated skill — apply freely |
| **Scenario Development** | Explore multiple futures for strategic planning | `horizon-scanning` |
| **Indicators Generation** | Define early warning indicators for a scenario | `horizon-scanning` |

## Decision Guide: Which Technique?

```
Are you evaluating WHO did something?
  → ACH (ach skill)

Are you assessing a THREAT?
  → Threat Assessment (threat-assessment skill)

Are you challenging your OWN analysis?
  → Key Assumptions Check (key-assumptions-check skill)

Are you challenging SOMEONE ELSE's analysis?
  → Red Team / Devil's Advocate (red-team-analysis skill)

Are you looking FORWARD (emerging threats)?
  → Horizon Scanning (horizon-scanning skill)

Are you unsure if your evidence is RELIABLE?
  → Source Assessment (source-assessment skill)

Do you have MULTIPLE plausible explanations?
  → ACH (ach skill)
```

## Combining Techniques

For complex assessments, combine techniques:
1. **Key Assumptions Check** first (surface your assumptions)
2. **ACH** for the core analysis (evaluate hypotheses)
3. **Red Team** to challenge the result (stress-test conclusions)
4. **Horizon Scanning** for forward-looking implications
