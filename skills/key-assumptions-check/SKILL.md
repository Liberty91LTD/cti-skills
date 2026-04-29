---
name: key-assumptions-check
description: Use when surfacing the assumptions underlying an analytical judgment, the user asks "what are we assuming?" / "are these assumptions still valid?", or before publishing a high-impact assessment. Standard SAT applied during major assessments.
user-invocable: true
metadata:
  version: 1.0.0
---

# Key Assumptions Check

Every analytical judgment rests on assumptions — often unstated. This technique surfaces them and evaluates whether the analysis holds if assumptions are wrong.

## Procedure

### Step 1: State the Analytical Line
Write the current assessment or conclusion in one clear sentence.

### Step 2: List All Assumptions
Brainstorm every assumption underlying the assessment. Include:
- Assumptions about threat actor intent or capability
- Assumptions about data completeness or accuracy
- Assumptions about the relevance of historical patterns
- Assumptions about the target environment
- Assumptions about timing or sequencing

### Step 3: Evaluate Each Assumption

| Assumption | Importance | Confidence | Status |
|-----------|:---:|:---:|:---:|
| [Assumption 1] | High | High | Validated |
| [Assumption 2] | High | Low | **FLAG** |
| [Assumption 3] | Medium | Medium | Monitor |
| [Assumption 4] | Low | High | Accepted |

**Importance**: How much does the conclusion depend on this assumption?
- **High**: If wrong, the conclusion changes significantly
- **Medium**: If wrong, the conclusion weakens but may still hold
- **Low**: If wrong, the conclusion is largely unaffected

**Confidence**: How sure are we this assumption is correct?
- **High**: Strong evidence supports it
- **Medium**: Some evidence, but not fully validated
- **Low**: Little or no evidence; assumed by default

### Step 4: Flag Critical Assumptions
Any assumption that is **High Importance + Low Confidence** is critical. These are the assumptions most likely to invalidate your analysis.

### Step 5: Determine Impact
For each flagged assumption:
- What would the conclusion be if this assumption is wrong?
- Can this assumption be validated through additional collection?
- Should the confidence level of the overall assessment be lowered?

## Output Template

```markdown
## Key Assumptions Check: [Assessment Title]

### Analytical Line
[The assessment being checked]

### Assumptions Matrix
| # | Assumption | Importance | Confidence | Status |
|---|-----------|:---:|:---:|:---:|
| 1 | ... | H/M/L | H/M/L | ... |

### Flagged Assumptions (High Importance + Low/Medium Confidence)
1. **[Assumption]**: If wrong, [impact on conclusion]. Collection gap: [what would validate this].

### Impact on Assessment
[Does the assumptions check change the confidence level? Should the conclusion be qualified?]

### Recommended Actions
- [Validate assumption X through Y collection]
- [Lower confidence from High to Moderate because of assumption Z]
```
