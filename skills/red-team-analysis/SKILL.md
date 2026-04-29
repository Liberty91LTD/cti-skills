---
name: red-team-analysis
description: Use when challenging a prevailing analytical judgment, the user asks "what is the opposing case?" / "argue the other side", or wants a devil's-advocate review of an assessment. Deliberately argues the opposite position to expose weaknesses.
user-invocable: true
metadata:
  version: 1.0.0
---

# Red Team Analysis (Devil's Advocate)

When consensus is strong, this technique deliberately argues the opposing position. The goal is not to be contrarian for its own sake — it's to find genuine weaknesses in the prevailing analysis before they become blind spots.

## When to Use
- Consensus is strong and unchallenged
- High-stakes assessment (wrong conclusion = significant harm)
- Analysis has been produced quickly under pressure
- The same team that collected also analysed (potential tunnel vision)
- Before publishing a product that will drive significant decisions

## Procedure

### Step 1: State the Prevailing Judgment
Write the current analytical consensus clearly and completely.

### Step 2: Argue Against It (With Maximum Effort)
Deliberately and rigorously construct the best possible case AGAINST the prevailing judgment:
- What evidence is being overweighted?
- What alternative explanations exist for the same evidence?
- What evidence has been ignored or underweighted?
- What assumptions are vulnerable? (cross-reference with key-assumptions-check)
- What would a sophisticated adversary do to make us believe the prevailing judgment?
- What historical cases looked similar but turned out differently?

### Step 3: Assess the Red Team Arguments
Honestly evaluate:
- Are any red team arguments compelling enough to change the judgment?
- Do they warrant lowering the confidence level?
- Do they identify intelligence gaps that should be filled?
- Do they suggest alternative hypotheses that should be tracked?

### Step 4: Report

```markdown
## Red Team Analysis: [Prevailing Judgment]

### Prevailing Judgment
[The assessment being challenged]

### Red Team Case
[The best case against the prevailing judgment]

#### Overweighted Evidence
- [Evidence that may be given too much weight, and why]

#### Alternative Explanations
- [Alternative explanations for the same evidence]

#### Ignored/Underweighted Evidence
- [Evidence pointing away from the prevailing judgment]

#### Vulnerable Assumptions
- [Assumptions the prevailing judgment depends on]

### Red Team Assessment
[How compelling is the red team case?]
- **Compelling**: Prevailing judgment should be revised
- **Partially compelling**: Confidence should be lowered
- **Not compelling**: Prevailing judgment stands, but the exercise identified useful intelligence gaps

### Recommendations
- [Actions: revise judgment, lower confidence, collect against gaps, track alternative hypothesis]
```

## Rules
- Argue with genuine effort — a weak red team is worse than no red team
- Separate the red team from the original analysis (different perspective, ideally different analyst)
- Red team findings must be incorporated into the final product
- A successful red team doesn't mean the original was wrong — it means we're more confident (or appropriately less confident) in the result
