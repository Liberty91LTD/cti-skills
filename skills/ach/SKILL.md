---
name: ach
description: Analysis of Competing Hypotheses — structured technique for evaluating multiple explanations against evidence. Use when facing ambiguous attribution or multiple plausible scenarios. Prefers graded evidence items from /quality-of-information-check and runs that skill first when handed raw URLs or text. Runs on ungraded evidence when asked, labelled as such, unweighted, and capped at Moderate confidence.
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

## Evidence: Graded Preferred, Ungraded Allowed

ACH works best on graded evidence items, one per claim, as produced by `/quality-of-information-check` (the QoI JSON or its claim table). The schema is in `skills/quality-of-information-check/references/evidence-item-schema.md`. Grading is the default. It is not a condition for running.

An item counts as graded when it has all of: `claim_id`, `claim`, `claim_type`, `anchor`, `grading.access_level`, `grading.claim_support`, `corroboration` and `provenance_basis`.

| What you were handed | What to do |
|---|---|
| QoI JSON or graded claim table | Proceed. If the JSON is a file, confirm it with `python3 skills/quality-of-information-check/scripts/validate_evidence.py <qoi.json>` (exit 0 = valid). Items that fail are not graded evidence: rerun the check on them or carry them as ungraded. |
| Raw URLs, articles, pasted report text | Complete Step 1, then invoke `/quality-of-information-check` on the material, passing the question. Use its output as the evidence. This is the default and needs no permission. |
| Evidence with a bare source rating but no claim table (for example "Mandiant report, Admiralty B2") | Run `/quality-of-information-check` on the underlying document if it is available. If not, carry the item as ungraded and record the rating as the analyst's own. |
| Evidence the user asserts from memory, with no document behind it | Cannot be graded. Carry it as ungraded, marked "asserted, no document". |
| A mix of graded and ungraded | Grade what can be graded. Carry the rest as ungraded. Graded rows keep their grades and weights. |
| The user asks to skip grading, or `/quality-of-information-check` cannot be run | Run in ungraded mode, below. Say once what that costs, then proceed. Do not ask again. |

### Ungraded mode

Any run with at least one ungraded row in the matrix follows these rules:

- **Label it.** The report header carries `Evidence basis: ungraded` when no row is graded and `Evidence basis: mixed` when some are. A fully graded run carries `Evidence basis: graded`.
- **Do not invent grades.** Do not grade items yourself inside this skill. An ungraded row shows `ungraded` in the Access level and Claim support columns. Where the analyst supplied a rating through `/source-assessment`, show it as `Admiralty B2 (analyst)`. It is displayed and does not change the weight. An Admiralty rating applies to a lookup result or a single item, the evidence grade applies to a claim from a document, and neither is converted into the other.
- **Ungraded rows weigh 1.** One ungraded item cannot eliminate a hypothesis alone. A hypothesis is rejected by ungraded evidence only through accumulation.
- **Confidence is capped at Moderate** when any load-bearing item is ungraded. High is reserved for conclusions whose load-bearing items are all graded and independently confirmed.
- **Give each row an id.** Ungraded rows are numbered `U01`, `U02` and so on, with the claim in one sentence and its source named.
- **Say it in Caveats.** State that the evidence was not graded, which items that applies to, and that running `/quality-of-information-check` on them may change the ranking.

First-party observations from the organisation's own telemetry are graded direct, established by rule R12 and need no check. They are graded rows in any mode.

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

### Step 2: Load the Evidence
Apply the evidence table above. Then list every evidence item relevant to the hypotheses.

For each graded item, carry over from the QoI output without changing it:
- `claim_id`, `claim` and `claim_type`
- The grade (`access_level` and `claim_support`, e.g. limited, firm)
- `load_bearing`, `flags`, and `corroboration.independent_primaries` with its `basis`
- `provenance_basis`

For each ungraded item, record an id (`U01`), the claim in one sentence, the source, and any analyst rating.

Do not regrade, merge or reword graded claims here. If a grade looks wrong, send it back through `/quality-of-information-check`. Absence of evidence ("the dog that didn't bark") is recorded as an analyst note below the matrix, not as a graded row, and carries no weight.

### Step 3: Build the Consistency Matrix

Mark each cell as:
- **C** (Consistent) — evidence supports this hypothesis
- **I** (Inconsistent) — evidence contradicts this hypothesis
- **NA** (Not Applicable) — evidence is irrelevant to this hypothesis

### Step 3a: Remove non-diagnostic rows

Diagnosticity comes first. Evidence that is consistent with every hypothesis tells you nothing about which one is true, however well graded it is.

- A row is **non-diagnostic** when every hypothesis has the same mark: all **C**, all **I**, or all **NA**.
- Move non-diagnostic rows out of the matrix into a "Non-diagnostic evidence" list in the report, with their grade. They take no part in scoring.
- Do this before any weight is applied. Grade weighting multiplies diagnosticity. It does not replace it. An observation graded direct, established that fits every hypothesis has an effective weight of zero.

### Step 3b: Weight the remaining rows by grade

Claim support sets the weight. Access level `untraced` or `adversary`, or flag `source_record_disputed`, subtracts 1, to a floor of 0.

| Claim support | Weight | With access level `untraced` or `adversary`, or flag `source_record_disputed` |
|---|:---:|:---:|
| **established** | 3 | 2 |
| **firm** | 2 | 1 |
| **tentative** | 1 | 0 |
| **disputed** | 0 | 0 |
| **unverified** | 0 | 0 |

So a claim graded direct, established weighs 3. Direct, firm and limited, firm weigh 2. Indirect, tentative weighs 1. Untraced, tentative and adversary, unverified weigh 0. An item flagged `retracted` weighs 0 whatever its grade. The table covers every grade for completeness. The rubric's caps mean some combinations cannot occur, for example untraced, established.

Ungraded rows weigh 1 whatever rating the analyst attached to them.

Weight 0 rows stay in the matrix so the reader can see them, but they do not move the score.

### Matrix Template

```markdown
| claim_id | Claim | claim_type | Access level | Claim support | Weight | H1: [Name] | H2: [Name] | H3: [Name] | H4: [Name] |
|----------|-------|------------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| C01 | [claim] | observation | direct | firm | 2 | C | I | C | NA |
| C02 | [claim] | victim_disclosure | direct | established | 3 | C | C | I | C |
| C03 | [claim] | attribution | indirect | tentative | 1 | I | C | C | NA |
| C04 | [claim] | observation | limited | firm | 2 | C | I | I | C |
| C05 | [claim] | actor_claim | adversary | unverified | 0 | C | C | C | I |
| **Inconsistencies (count)** | | | | | | **1** | **2** | **2** | **1** |
| **Weighted inconsistency score** | | | | | | **1** | **4** | **5** | **0** |
| **Heaviest inconsistent item** | | | | | | **1** (C03) | **2** (C01, C04) | **3** (C02) | **0** (C05) |

Total available weight: 8 (sum of the weights of the diagnostic rows). Separation threshold: 0.8.

Non-diagnostic evidence (not scored): C06, [claim], direct, established, consistent with all four hypotheses.
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
- Call out every linchpin that is flagged `single_source` or has claim support `unverified`. Name the `claim_id` and state what would corroborate it.

### Step 6: Draw Conclusions

- State the most likely hypothesis with confidence level. With any ungraded load-bearing item, the level is Moderate at most
- Explain why alternative hypotheses were rejected (which evidence contradicts them)
- Identify the evidence that most strongly discriminates between hypotheses
- For each rejected hypothesis, state whether one item eliminated it or several did together
- Note linchpin evidence and its grade
- Flag if the conclusion is sensitive to one or two pieces of evidence

### Step 7: Report

Carry `provenance_basis` from the QoI output into the header. Where items differ, use the worst one (`first-party` is best, then `platform-resolved`, then `script-resolved`, then `model-judged`). A run with no graded items has no provenance basis: write `none (ungraded)`.

```markdown
## ACH Analysis: [Question]
**Date**: YYYY-MM-DD | **Evidence basis**: [graded / mixed / ungraded] | **Provenance basis**: [platform-resolved / script-resolved / model-judged (unverified) / none (ungraded)] | **Evidence items**: [n] from [QoI run or document(s)]

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

| Linchpin | Access level | Claim support | Callout |
|----------|:---:|:---:|---------|
| C0x | limited | firm | single_source: [what would corroborate it] |
| C0y | adversary | unverified | claim support unverified, cannot be judged: [what would corroborate it] |

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
- **Equal weighting** — an inconsistency graded direct, established should count more than one graded untraced, disputed
- **Scoring non-diagnostic evidence** — a well-graded item that fits every hypothesis separates nothing
- **Hiding a decisive item in a sum** — one confirmed inconsistency can eliminate a hypothesis by itself; report it as such
- **Reading the evidence first** — hypotheses written after the evidence tend to fit it
- **Grading inside the matrix** — grades come from `/quality-of-information-check`, not from this skill
- **Presenting an ungraded run as a graded one** — label the evidence basis, keep ungraded rows at weight 1, and stay at Moderate or below
- **Counting outlets as sources** — five articles on one vendor report are one evidence chain
- **Stopping too early** — ACH works best when you revisit the matrix as new evidence emerges
- **Treating it as a vote** — ACH is about inconsistencies, not consistency counts
