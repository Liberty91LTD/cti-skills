---
name: devils-advocacy
description: Use when challenging a prevailing analytical judgment, the user asks "what is the opposing case?" / "argue the other side" / "play devil's advocate", or wants an assessment stress-tested before release. Takes the team's own lead judgment and builds the strongest case that it is wrong. A contrarian technique. It does not model what an adversary would do next, which is Red Team Analysis. Formerly /red-team-analysis.
user-invocable: true
metadata:
  version: 2.0.0
---

# Devil's Advocacy

A contrarian technique from the CIA Tradecraft Primer. It takes the team's own lead judgment as its input and argues that the judgment is wrong. Its output is a rebuttal.

It is not Red Team Analysis. Red teaming is an imaginative technique: it reasons as the adversary would, from the adversary's position and constraints, and produces adversary courses of action. This pack does not have a Red Team Analysis skill. Until version 2.0 this skill carried that name.

When consensus is strong, this technique deliberately argues the opposing position. The goal is not to be contrarian for its own sake — it's to find genuine weaknesses in the prevailing analysis before they become blind spots.

## When to Use
- Consensus is strong and unchallenged
- High-stakes assessment (wrong conclusion = significant harm)
- Analysis has been produced quickly under pressure
- The same team that collected also analysed (potential tunnel vision)
- Before publishing a product that will drive significant decisions

## Procedure

### Step 1: State the Prevailing Judgment
Write the current analytical consensus clearly and completely. Where the judgment rests on graded evidence from `/quality-of-information-check`, take the claim table with it: the weakest load-bearing claim is the first place to press.

### Step 2: Argue Against It (With Maximum Effort)
Deliberately and rigorously construct the best possible case AGAINST the prevailing judgment:
- What evidence is being overweighted?
- What alternative explanations exist for the same evidence?
- What evidence has been ignored or underweighted?
- What assumptions are vulnerable? (cross-reference with key-assumptions-check)
- What would a sophisticated adversary do to make us believe the prevailing judgment?
- What historical cases looked similar but turned out differently?

### Step 3: Assess the Opposing Case
Honestly evaluate:
- Are any of the opposing arguments compelling enough to change the judgment?
- Do they warrant lowering the confidence level?
- Do they identify intelligence gaps that should be filled?
- Do they suggest alternative hypotheses that should be tracked?

### Step 4: Report

```markdown
## Devil's Advocacy: [Prevailing Judgment]

### Prevailing Judgment
[The assessment being challenged]

### The Case Against
[The best case against the prevailing judgment]

#### Overweighted Evidence
- [Evidence that may be given too much weight, and why]

#### Alternative Explanations
- [Alternative explanations for the same evidence]

#### Ignored/Underweighted Evidence
- [Evidence pointing away from the prevailing judgment]

#### Vulnerable Assumptions
- [Assumptions the prevailing judgment depends on]

### Assessment of the Case Against
[How compelling is it?]
- **Compelling**: Prevailing judgment should be revised
- **Partially compelling**: Confidence should be lowered
- **Not compelling**: Prevailing judgment stands, but the exercise identified useful intelligence gaps

### Recommendations
- [Actions: revise judgment, lower confidence, collect against gaps, track alternative hypothesis]
```

## Rules
- Argue with genuine effort — a weak devil's advocate is worse than none
- Separate the devil's advocate from the original analysis (different perspective, ideally different analyst)
- The findings must be incorporated into the final product
- A strong case against doesn't mean the original was wrong — it means we're more confident (or appropriately less confident) in the result
