---
name: key-assumptions-check
description: Use when surfacing the assumptions underlying an analytical judgment, the user asks "what are we assuming?" / "are these assumptions still valid?", or before publishing a high-impact assessment. Standard SAT applied during major assessments.
user-invocable: true
metadata:
  version: 1.1.0
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

### Step 3: Walk the Claim Table (when one exists)
If the assessment was built on graded evidence items from `/quality-of-information-check`, go through the claim table row by row. Assumptions are usually hiding in judgements that the analysis treats as observations. If there is no claim table, skip this step and leave the Claim column as "n/a".

For each claim, compare its `claim_type` with how the analytical line uses it:

| In the claim table | How the analysis uses it | Assumption to record |
|---|---|---|
| `assessment` | Stated as fact, or as a premise for a further judgement | That the source's judgement about intent, capability or future behaviour is correct |
| `attribution` | Actor named without the source's hedge | That the attribution holds. Quote `stated_confidence` verbatim |
| `actor_claim` | Scale, victim or data figures repeated as fact | That the actor is telling the truth |
| Any type, flagged `caveats_dropped_in_chain` | Outlet's stronger wording used | That the claim is as strong as the outlet made it, not as the primary wrote it |
| Any type, flagged `single_source` or with corroboration `unchecked` | Relied on without qualification | That the one primary is right |
| Any type, flagged `stale` or `superseded` | Used as current | That nothing has changed since publication |

Rules:
- Every `assessment` and `attribution` claim with `load_bearing: true` gets a row in the matrix, even when the assumption looks safe.
- Carry the `claim_id` into the matrix. One claim can produce more than one assumption, and an assumption can rest on several claims.
- Do not regrade claims here. The grade informs the Confidence column: claim support tentative or worse on a claim used as fact is Low or Medium confidence, never High.
- Assumptions from Step 2 that trace to no claim are kept, with "none" in the Claim column. These have no evidence behind them at all, which is worth stating.

### Step 4: Evaluate Each Assumption

| Assumption | Claim | Importance | Confidence | Status |
|-----------|:---:|:---:|:---:|:---:|
| [Assumption 1] | C01 | High | High | Validated |
| [Assumption 2] | C04 | High | Low | **FLAG** |
| [Assumption 3] | none | Medium | Medium | Monitor |
| [Assumption 4] | C02, C06 | Low | High | Accepted |

**Importance**: How much does the conclusion depend on this assumption?
- **High**: If wrong, the conclusion changes significantly
- **Medium**: If wrong, the conclusion weakens but may still hold
- **Low**: If wrong, the conclusion is largely unaffected

**Confidence**: How sure are we this assumption is correct?
- **High**: Strong evidence supports it
- **Medium**: Some evidence, but not fully validated
- **Low**: Little or no evidence; assumed by default

### Step 5: Flag Critical Assumptions
Any assumption that is **High Importance + Low Confidence** is critical. These are the assumptions most likely to invalidate your analysis.

### Step 6: Determine Impact
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
| # | Assumption | Claim | Claim type | Access level | Claim support | Importance | Confidence | Status |
|---|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | ... | C04 | attribution | indirect | tentative | H/M/L | H/M/L | ... |

### Flagged Assumptions (High Importance + Low/Medium Confidence)
1. **[Assumption]** (C04): If wrong, [impact on conclusion]. Collection gap: [what would validate this].

### Impact on Assessment
[Does the assumptions check change the confidence level? Should the conclusion be qualified?]

### Recommended Actions
- [Validate assumption X through Y collection]
- [Lower confidence from High to Moderate because of assumption Z]
```
