---
name: structured-analytic-techniques
description: Use when the user asks "which SAT should I use for X?", wants the index of Structured Analytic Techniques, or is choosing between quality-of-information-check, ACH, key-assumptions-check, devils-advocacy, indicators of change, etc. Quality of Information Check is the default first step of any diagnostic run.
user-invocable: true
metadata:
  version: 2.0.0
---

# Structured Analytic Techniques (SATs) Index

SATs are formal methods that externalise analytical thinking, making it transparent, challengeable, and less susceptible to cognitive biases. Choose the right technique based on the analytical challenge.

## When to Use SATs

- When the stakes are high (wrong answer = significant consequence)
- When multiple plausible explanations exist
- When cognitive biases are likely (confirmation, anchoring, availability)
- When you need to communicate your reasoning transparently
- When building on analysis from multiple analysts

## Start With the Evidence

The Quality of Information Check is the default first step of any diagnostic run. Before hypotheses are tested or an assessment is written, run `/quality-of-information-check` on the reports and articles the analysis will rest on. It resolves each one to its originating source, splits it into claims and grades each claim. `ach`, `threat-assessment` and `writing-assessments` refuse ungraded evidence.

Skip it only when the evidence already arrives as graded evidence items, or when there are no documents to grade. Hits in the organisation's own telemetry enter as A1 observations (rubric rule R12). Third-party lookup results are rated through `source-assessment`.

## Technique Categories

Families follow the CIA Tradecraft Primer. The full list, one line per technique with the covering skill or "not in the pack", is in [references/when-to-use.md](references/when-to-use.md).

### Diagnostic Techniques
**Purpose**: Evaluate existing analysis for quality and bias.

| Technique | When to Use | Skill |
|-----------|-------------|-------|
| **Quality of Information Check** | First, before any other diagnostic technique. Resolve provenance, split reports into claims, grade each claim, list gaps | `quality-of-information-check` |
| **Key Assumptions Check** | Before or after any major assessment — surface and challenge unstated assumptions | `key-assumptions-check` |
| **Analysis of Competing Hypotheses** | Multiple plausible explanations — systematically evaluate each against evidence | `ach` |
| **Indicators or Signposts of Change** | When monitoring a developing situation — define observable markers of change | Not in the pack. `horizon-scanning` defines early warning indicators in part |

### Contrarian Techniques
**Purpose**: Challenge prevailing judgments and expose blind spots.

| Technique | When to Use | Skill |
|-----------|-------------|-------|
| **Devil's Advocacy** | When consensus is strong — take the team's own lead judgment and argue it is wrong | `devils-advocacy` |
| **What-If Analysis** | Assume an event has happened and reason back to how | Not in the pack |
| **High-Impact / Low-Probability** | Ensure unlikely but catastrophic scenarios are considered | Not in the pack. Nearest: combine `threat-assessment` + `horizon-scanning` |
| **Team A / Team B** | Two competing views each deserve a full case | Not in the pack |

### Imaginative Techniques
**Purpose**: Generate new ideas, hypotheses, and indicators.

| Technique | When to Use | Skill |
|-----------|-------------|-------|
| **Brainstorming** | Generate hypotheses, IOC types to collect, detection approaches | No dedicated skill — apply freely |
| **Scenario Development** | Explore multiple futures for strategic planning | `horizon-scanning` |
| **Indicators Generation** | Define early warning indicators for a scenario | `horizon-scanning` |

## Decision Guide: Which Technique?

```
Are you about to reason from reports or articles? (default first step)
  → Quality of Information Check (quality-of-information-check skill)

Are you evaluating WHO did something?
  → ACH (ach skill)

Are you assessing a THREAT?
  → Threat Assessment (threat-assessment skill)

Are you challenging your OWN analysis?
  → Key Assumptions Check (key-assumptions-check skill)

Are you challenging SOMEONE ELSE's analysis?
  → Devil's Advocacy (devils-advocacy skill)

Are you looking FORWARD (emerging threats)?
  → Horizon Scanning (horizon-scanning skill)

Are you unsure if your evidence is RELIABLE, or where it comes from?
  → Quality of Information Check (quality-of-information-check skill)

Do you need the Admiralty scale DEFINITIONS, or a grade for a single lookup result?
  → Source Assessment (source-assessment skill)

Do you have MULTIPLE plausible explanations?
  → ACH (ach skill)
```

## Combining Techniques

For complex assessments, combine techniques:
1. **Quality of Information Check** first (grade the evidence before reasoning from it)
2. **Key Assumptions Check** (surface your assumptions)
3. **ACH** for the core analysis (evaluate hypotheses against the graded claims)
4. **Devil's Advocacy** to challenge the result (stress-test conclusions)
5. **Horizon Scanning** for forward-looking implications

`ach` writes its hypotheses before it reads any evidence. When the sequence is run for ACH, state the question first, let `ach` list the hypotheses, then run the Quality of Information Check.
