---
name: ach
description: Analysis of Competing Hypotheses — structured technique for evaluating multiple explanations against evidence. Use when facing ambiguous attribution or multiple plausible scenarios.
user-invocable: true
metadata:
  version: 1.0.0
---

# Analysis of Competing Hypotheses (ACH)

ACH is the most important structured analytic technique for CTI. It forces you to evaluate ALL plausible hypotheses against ALL significant evidence, reducing the impact of cognitive biases — especially confirmation bias.

## When to Use ACH

- Attribution questions: "Who is behind this campaign?"
- Ambiguous situations: Multiple plausible explanations exist
- High-stakes assessments: Getting it wrong has significant consequences
- Contested analysis: Analysts disagree on the conclusion

## Step-by-Step Procedure

### Step 1: Generate Hypotheses
List ALL reasonable hypotheses. Include unlikely ones — the point is to avoid premature narrowing.

Rules:
- Minimum 3 hypotheses (if you only have 2, you're doing binary thinking)
- Include at least one that challenges your initial instinct
- Hypotheses should be mutually exclusive where possible
- Include "unknown actor" or "coincidence" as hypotheses when appropriate

### Step 2: List Significant Evidence
Enumerate all evidence and arguments relevant to the hypotheses.

For each piece of evidence, record:
- Description of the evidence
- Source (with Admiralty Scale rating)
- Whether it's direct evidence, circumstantial, or absence of evidence

### Step 3: Build the Consistency Matrix

Mark each cell as:
- **C** (Consistent) — evidence supports this hypothesis
- **I** (Inconsistent) — evidence contradicts this hypothesis
- **NA** (Not Applicable) — evidence is irrelevant to this hypothesis

### Matrix Template

```markdown
| Evidence | Source Rating | H1: [Name] | H2: [Name] | H3: [Name] | H4: [Name] |
|----------|:---:|:---:|:---:|:---:|:---:|
| E1: [description] | B2 | C | I | C | NA |
| E2: [description] | A1 | C | C | I | C |
| E3: [description] | C3 | I | C | C | NA |
| E4: [description] | B2 | C | I | I | C |
| E5: [description] | D4 | C | C | C | I |
| **Inconsistencies** | | **1** | **2** | **2** | **1** |
```

### Step 4: Analyse the Matrix

**Critical principle: Focus on DISPROVING hypotheses, not proving them.**

Confirmation bias makes us seek evidence that confirms our preferred hypothesis. ACH counteracts this by focusing on inconsistencies.

- Count inconsistencies for each hypothesis
- Weight inconsistencies by evidence quality (an A1-rated inconsistency matters more than a D4)
- The hypothesis with the fewest (and weakest) inconsistencies is the most likely

### Step 5: Assess Sensitivity

Ask for each piece of evidence:
- If this evidence were wrong, would it change the ranking?
- Which evidence items are "linchpin" evidence (removing them changes the conclusion)?
- Are any linchpin items from single sources?

### Step 6: Draw Conclusions

- State the most likely hypothesis with confidence level
- Explain why alternative hypotheses were rejected (which evidence contradicts them)
- Identify the evidence that most strongly discriminates between hypotheses
- Note linchpin evidence and its reliability
- Flag if the conclusion is sensitive to one or two pieces of evidence

### Step 7: Report

```markdown
## ACH Analysis: [Question]

### Hypotheses Evaluated
1. H1: [description]
2. H2: [description]
3. H3: [description]

### Consistency Matrix
[Matrix from Step 3]

### Assessment
[Most likely hypothesis with confidence level and rationale]

### Key Discriminating Evidence
[Evidence that most strongly separates hypotheses]

### Sensitivity Analysis
[Which evidence is linchpin? What would change the conclusion?]

### Rejected Hypotheses
- H2 rejected because: [specific evidence contradicts it]
- H3 rejected because: [specific evidence contradicts it]

### Caveats
[Limitations, intelligence gaps, assumptions]
```

## Common Mistakes

- **Too few hypotheses** — 2 hypotheses is binary thinking, not ACH
- **Confirmation bias in marking** — being generous with "C" for your preferred hypothesis
- **Ignoring absence of evidence** — "the dog that didn't bark" can be significant
- **Equal weighting** — an A1-rated inconsistency should count more than a D4
- **Stopping too early** — ACH works best when you revisit the matrix as new evidence emerges
- **Treating it as a vote** — ACH is about inconsistencies, not consistency counts
