---
name: feedback-loops
description: Feedback loop implementation for continuous CTI improvement. Consumer feedback, analyst retrospectives, source quality tracking.
user-invocable: false
metadata:
  version: 1.0.0
---

# Feedback Loops

Feedback is Phase 6 of the CTI Hyperloop. Without it, the cycle is open-ended and quality degrades over time.

## Types of Feedback

### 1. Consumer Feedback
Intelligence consumers (stakeholders) assess the value of products they receive.

**Collection points:**
- After every significant product delivery
- During quarterly PIR reviews
- During stakeholder briefings

**Questions:**
| Question | Response Options |
|----------|-----------------|
| Was this intelligence useful for your decision-making? | Very useful / Somewhat useful / Not useful |
| Was it delivered in time to act on? | Yes / Partially / No |
| Was the format appropriate for your needs? | Yes / Too technical / Too high-level / Wrong format |
| Was the confidence assessment helpful? | Yes / Unclear / Not included |
| What should we prioritise next? | Free text |

**Actions:**
- Useful + timely → Continue current approach, reinforce collection sources
- Useful + late → Improve detection/triage speed, adjust collection frequency
- Not useful → Review PIR alignment, stakeholder needs, product format
- Format wrong → Adjust per stakeholder-management skill

### 2. Source Quality Tracking
Track the reliability of intelligence sources over time.

**For each source used in products:**
- Was the information confirmed, partly confirmed, or disproven?
- Did the source's Admiralty rating need adjustment?
- Were there timeliness issues?

**Actions:**
- Consistently confirmed → Upgrade reliability rating (e.g., C → B)
- Inconsistent → Maintain or downgrade rating
- Repeatedly disproven → Downgrade to D or E
- Feed updates into source-assessment guidance

### 3. Analyst Retrospectives
After significant investigations or assessments:

**Questions:**
- What analytical techniques were applied? Were they effective?
- Were key assumptions validated or invalidated?
- Were there intelligence gaps that could have been filled?
- Were alternative hypotheses adequately considered?
- What would you do differently?

**Actions:**
- Update SOPs with lessons learned
- Adjust technique selection guidance
- Fill identified collection gaps
- Update knowledge cells with validated/invalidated assumptions

### 4. Detection Effectiveness
For detection rules produced by the platform:

**Metrics:**
- True positive rate (did the rule catch real threats?)
- False positive rate (did it generate noise?)
- Coverage (did it miss known instances?)

**Actions:**
- High FP → Refine rule, add exclusions
- Missed detections → Expand rule, add variants
- No hits → Verify rule logic, check data source availability

## Feedback Integration

All feedback feeds back into Phase 1 (Planning & Direction):

```
Consumer says "not useful" → Review and adjust PIRs
Source proves unreliable → Update Admiralty ratings, adjust collection
Analyst retrospective finds gap → Create new collection tasking
Detection rule has high FP → Refine and redeploy
```

## Tracking

The orchestrator maintains feedback state:
- Consumer feedback logged in stakeholder register
- Source quality tracked in knowledge cell Sources & References
- Retrospective outcomes logged in investigation workspace
- Detection effectiveness tracked in detection rule metadata
