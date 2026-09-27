---
name: ach
description: Analysis of Competing Hypotheses — structured technique for evaluating multiple explanations against evidence. Use when facing ambiguous attribution or multiple plausible scenarios. Requires graded evidence items from /quality-of-information-check and runs that skill first when handed raw URLs or text. Refuses to build a matrix on ungraded evidence.
user-invocable: true
metadata:
  version: 2.0.0
---

# Analysis of Competing Hypotheses (ACH)

ACH is the most important structured analytic technique for CTI. It forces you to evaluate ALL plausible hypotheses against ALL significant evidence, reducing the impact of cognitive biases — especially confirmation bias.

## When to Use ACH

- Attribution questions: "Who is behind this campaign?"
- Ambiguous situations: Multiple plausible explanations exist
- High-stakes assessments: Getting it wrong has significant consequences
- Contested analysis: Analysts disagree on the conclusion

## Precondition: Graded Evidence Only

ACH runs on graded evidence items, one per claim, as produced by `/quality-of-information-check` (the QoI JSON or its claim table). The schema is in `skills/quality-of-information-check/references/evidence-item-schema.md`.

An item counts as graded when it has all of: `claim_id`, `claim`, `claim_type`, `anchor`, `grading.source_reliability`, `grading.information_credibility`, `corroboration` and `provenance_basis`.

| What you were handed | What to do |
|---|---|
| QoI JSON or graded claim table | Proceed. If the JSON is a file, confirm it with `python3 skills/quality-of-information-check/scripts/validate_evidence.py <qoi.json>` (exit 0 = valid). Do not build on items that fail. |
| Raw URLs, articles, pasted report text | Complete Step 1, then invoke `/quality-of-information-check` on the material, passing the question. Use its output as the evidence. |
| Evidence with a bare source rating but no claim table (for example "Mandiant report, B2") | Treat as ungraded. Run `/quality-of-information-check` on the underlying document. |
| Evidence the user asserts from memory, with no document behind it | Cannot be graded. Do not put it in the matrix. List it under Caveats as unsupported. |
| A mix of graded and ungraded | Grade the ungraded material first. Do not build a partial matrix. |

**Refuse to build a matrix on ungraded evidence.** Do not grade items yourself inside this skill, and do not fill a matrix "provisionally". If `/quality-of-information-check` cannot be run, or the user asks to skip it, stop and tell the user:

> I can't build the ACH matrix yet. ACH weights each piece of evidence by its grade, and this evidence has not been graded. Without grades the matrix would rest on whatever I happened to trust. Give me the URLs or the report text and I will run /quality-of-information-check first, or hand me an existing QoI output. I have listed the hypotheses below so they are ready when the evidence is.

Then output the Step 1 hypotheses and nothing else.

## Step-by-Step Procedure

The order is strict: hypotheses first, then evidence. Step 1 is completed and written down before any evidence item is read, graded or fetched.

### Step 1: Generate Hypotheses (before reading any evidence)
List ALL reasonable hypotheses. Include unlikely ones — the point is to avoid premature narrowing.

Rules:
- Minimum 3 hypotheses (if you only have 2, you're doing binary thinking)
- Include at least one that challenges your initial instinct
- Hypotheses should be mutually exclusive where possible
- Include "unknown actor" or "coincidence" as hypotheses when appropriate

Ordering rules:
- Generate hypotheses from the question alone. Do not open the evidence, run lookups or invoke `/quality-of-information-check` until the list is written out.
- If the evidence is already in the conversation, generate the hypotheses from the question as worded and say in the output that the evidence was visible beforehand.
- Once evidence has been read, hypotheses may be added but never removed or reworded. Mark any late addition "added after evidence" in the report. A hypothesis is only rejected through the matrix.

### Step 2: Load the Graded Evidence
Apply the precondition above. Then list every evidence item relevant to the hypotheses.

For each item, carry over from the QoI output without changing it:
- `claim_id`, `claim` and `claim_type`
- The grade (`source_reliability` + `information_credibility`, e.g. B2)
- `load_bearing`, `flags`, and `corroboration.independent_primaries` with its `basis`
- `provenance_basis`

Do not regrade, merge or reword claims here. If a grade looks wrong, send it back through `/quality-of-information-check`. Absence of evidence ("the dog that didn't bark") is recorded as an analyst note below the matrix, not as a graded row, and carries no weight.

### Step 3: Build the Consistency Matrix

Mark each cell as:
- **C** (Consistent) — evidence supports this hypothesis
- **I** (Inconsistent) — evidence contradicts this hypothesis
- **NA** (Not Applicable) — evidence is irrelevant to this hypothesis

### Step 3a: Remove non-diagnostic rows

Diagnosticity comes first. Evidence that is consistent with every hypothesis tells you nothing about which one is true, however well graded it is.

- A row is **non-diagnostic** when every hypothesis has the same mark: all **C**, all **I**, or all **NA**.
- Move non-diagnostic rows out of the matrix into a "Non-diagnostic evidence" list in the report, with their grade. They take no part in scoring.
- Do this before any weight is applied. Grade weighting multiplies diagnosticity. It does not replace it. An A1 observation that fits every hypothesis has an effective weight of zero.

### Step 3b: Weight the remaining rows by grade

Credibility sets the weight. Reliability D or worse subtracts 1, to a floor of 0.

| Reliability | Cred. 1 | Cred. 2 | Cred. 3 | Cred. 4 | Cred. 5 | Cred. 6 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **A** | 3 | 2 | 1 | 0 | 0 | 0 |
| **B** | 3 | 2 | 1 | 0 | 0 | 0 |
| **C** | 3 | 2 | 1 | 0 | 0 | 0 |
| **D** | 2 | 1 | 0 | 0 | 0 | 0 |
| **E** | 2 | 1 | 0 | 0 | 0 | 0 |
| **F** | 2 | 1 | 0 | 0 | 0 | 0 |

So A1 weighs 3, A2 and B2 weigh 2, C3 weighs 1, and D3 and F6 weigh 0. An item flagged `retracted` weighs 0 whatever its grade. The table covers every grade for completeness. The rubric's caps mean some cells cannot occur, for example D1.

Weight 0 rows stay in the matrix so the reader can see them, but they do not move the score.

### Matrix Template

```markdown
| claim_id | Claim | claim_type | Grade | Weight | H1: [Name] | H2: [Name] | H3: [Name] | H4: [Name] |
|----------|-------|------------|:---:|:---:|:---:|:---:|:---:|:---:|
| C01 | [claim] | observation | A2 | 2 | C | I | C | NA |
| C02 | [claim] | victim_disclosure | A1 | 3 | C | C | I | C |
| C03 | [claim] | attribution | C3 | 1 | I | C | C | NA |
| C04 | [claim] | observation | B2 | 2 | C | I | I | C |
| C05 | [claim] | actor_claim | F6 | 0 | C | C | C | I |
| **Inconsistencies (count)** | | | | | **1** | **2** | **2** | **1** |
| **Weighted inconsistency score** | | | | | **1** | **4** | **5** | **0** |
| **Heaviest inconsistent item** | | | | | **1** (C03) | **2** (C01, C04) | **3** (C02) | **0** (C05) |

Total available weight: 8 (sum of the weights of the diagnostic rows). Separation threshold: 0.8.

Non-diagnostic evidence (not scored): C06, [claim], A1, consistent with all four hypotheses.
```

### Step 4: Analyse the Matrix

**Critical principle: Focus on DISPROVING hypotheses, not proving them.**

Confirmation bias makes us seek evidence that confirms our preferred hypothesis. ACH counteracts this by focusing on inconsistencies.

For each hypothesis, report three numbers:

1. **Count** of inconsistent cells.
2. **Weighted inconsistency score**: the sum of the weights of its **I** cells. **C** and **NA** cells score nothing.
3. **Heaviest inconsistent item**: the highest weight among its **I** cells, with the `claim_id`.

Reading them:

- The hypothesis with the lowest weighted score is the most likely.
- **One decisive disconfirmation.** A sum hides the case where a single item does the work. When a hypothesis has an **I** cell of weight 3, say that it is eliminated by that item, name the `claim_id`, and do not describe it as rejected by accumulation. In the template, H3 is eliminated by C02 alone.
- **Accumulation.** When a hypothesis has no **I** cell above weight 2, it is rejected, if at all, by the sum. Say so, and list the items. In the template, H2 is rejected by two weight-2 items together.
- **Separation.** Two hypotheses are separated only when their weighted scores differ by more than 10% of the total available weight. Below that, the matrix does not separate them. Say so rather than picking one.
- A hypothesis whose only inconsistencies have weight 0 has not been tested by the evidence. Say that too. It is not the same as being supported.

### Step 5: Assess Sensitivity

Ask for each piece of evidence:
- If this evidence were wrong, would it change the ranking?
- Which evidence items are "linchpin" evidence (removing them changes the conclusion)?
- Are any linchpin items from single sources?

Test it by removing each diagnostic row in turn and recomputing the three numbers.

Linchpin rules:
- Only load-bearing claims can be linchpins. Items with `load_bearing: false` and items flagged `press_originated` are excluded from linchpin status unless the user explicitly promotes them. Record any promotion in the report, by `claim_id`.
- If removing an excluded item would change the ranking, the conclusion rests on evidence that is not fit to carry it. Report this as a gap and do not present the ranking as settled.
- Call out every linchpin that is flagged `single_source` or has credibility 6. Name the `claim_id` and state what would corroborate it.

### Step 6: Draw Conclusions

- State the most likely hypothesis with confidence level
- Explain why alternative hypotheses were rejected (which evidence contradicts them)
- Identify the evidence that most strongly discriminates between hypotheses
- For each rejected hypothesis, state whether one item eliminated it or several did together
- Note linchpin evidence and its grade
- Flag if the conclusion is sensitive to one or two pieces of evidence

### Step 7: Report

Carry `provenance_basis` from the QoI output into the header. Where items differ, use the worst one (`platform-resolved` is best, then `script-resolved`, then `model-judged`).

```markdown
## ACH Analysis: [Question]
**Date**: YYYY-MM-DD | **Provenance basis**: [platform-resolved / script-resolved / model-judged (unverified)] | **Evidence items**: [n] from [QoI run or document(s)]

### Hypotheses Evaluated
Generated before the evidence was read. Late additions are marked.
1. H1: [description]
2. H2: [description]
3. H3: [description]

### Consistency Matrix
[Matrix from Step 3, with count, weighted score and heaviest inconsistent item per hypothesis]

### Non-diagnostic Evidence
[Rows removed in Step 3a, with grade, or "None"]

### Assessment
[Most likely hypothesis with confidence level and rationale]

### Key Discriminating Evidence
[Evidence that most strongly separates hypotheses]

### Sensitivity Analysis
[Which evidence is linchpin? What would change the conclusion?]

| Linchpin | Grade | Callout |
|----------|:---:|---------|
| C0x | B2 | single_source: [what would corroborate it] |
| C0y | F6 | credibility 6, cannot be judged: [what would corroborate it] |

[Items promoted to load-bearing by the user, by claim_id, or "None"]

### Rejected Hypotheses
- H2 rejected by accumulation: [claim_ids and what they contradict]
- H3 eliminated by a single item: [claim_id, grade, what it contradicts]

### Caveats
[Limitations, intelligence gaps, assumptions]
```

## Common Mistakes

- **Too few hypotheses** — 2 hypotheses is binary thinking, not ACH
- **Confirmation bias in marking** — being generous with "C" for your preferred hypothesis
- **Ignoring absence of evidence** — "the dog that didn't bark" can be significant
- **Equal weighting** — an A1-rated inconsistency should count more than a D4
- **Scoring non-diagnostic evidence** — a well-graded item that fits every hypothesis separates nothing
- **Hiding a decisive item in a sum** — one confirmed inconsistency can eliminate a hypothesis by itself; report it as such
- **Reading the evidence first** — hypotheses written after the evidence tend to fit it
- **Grading inside the matrix** — grades come from `/quality-of-information-check`, not from this skill
- **Counting outlets as sources** — five articles on one vendor report are one evidence chain
- **Stopping too early** — ACH works best when you revisit the matrix as new evidence emerges
- **Treating it as a vote** — ACH is about inconsistencies, not consistency counts
