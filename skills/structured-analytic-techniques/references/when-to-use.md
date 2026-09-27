# When to use which technique

One line per technique. Families follow the CIA Tradecraft Primer (2009). Techniques from Heuer and Pherson that the Primer does not list are in a separate table, followed by what the pack implements outside both.

"Not in the pack" means there is no skill for the technique. Do not route to a skill name that is not in this file. Where an existing skill covers part of a technique, the line says which part.

For any diagnostic run on documents, articles or reports, `/quality-of-information-check` goes first. `/ach`, `/threat-assessment` and `/writing-assessments` refuse ungraded evidence.

## Diagnostic

| Technique | Use when | Skill |
|---|---|---|
| Quality of Information Check | You are about to reason from reports or articles and need to know where each claim comes from and how far it can be trusted. Default first step. | `/quality-of-information-check` |
| Key Assumptions Check | Before or after a major assessment, to surface what the judgment takes for granted. | `/key-assumptions-check` |
| Analysis of Competing Hypotheses | Several explanations fit the evidence, most often in attribution. | `/ach` |
| Indicators or Signposts of Change | You need observable markers that show which hypothesis or scenario is materialising, and want to track them. | Not in the pack. `/horizon-scanning` defines early warning indicators per scenario but does not validate or track them. |

## Contrarian

| Technique | Use when | Skill |
|---|---|---|
| Devil's Advocacy | Consensus is strong and nobody has argued the other side. Input: the team's own lead judgment. Output: a rebuttal. | `/devils-advocacy` |
| Team A / Team B | Two competing views persist and each deserves a full case before reconciliation. | Not in the pack |
| High Impact / Low Probability | An unlikely event would be severe enough that the consumer needs to see how it could happen. | Not in the pack. Nearest: `/threat-assessment` combined with `/horizon-scanning`. |
| "What If?" Analysis | You want to assume an event has happened and reason back to how it came about. | Not in the pack |

## Imaginative

| Technique | Use when | Skill |
|---|---|---|
| Brainstorming | Generating hypotheses, collection ideas or detection approaches at the start of a task. | Not in the pack. No skill needed, apply freely. |
| Outside-In Thinking | The analysis is focused on the actor or incident and has not considered external forces (political, economic, technological). | Not in the pack. `/horizon-scanning` covers external drivers for forward-looking work. |
| Red Team Analysis | You need to reason as the adversary would, from their position and constraints. Input: the adversary. Output: adversary courses of action. | Not in the pack. `/devils-advocacy` was named `/red-team-analysis` before 2.0 but never modelled adversary decision-making. |
| Alternative Futures Analysis | The situation is too uncertain for one forecast and the consumer needs several scenarios built from key drivers. | Not in the pack. `/horizon-scanning` produces best, worst and most likely scenarios, not a driver matrix. |

## Other structured techniques (Heuer and Pherson)

| Technique | Use when | Skill |
|---|---|---|
| Deception Detection | A source has motive and means to mislead, for example leak-site claims or contested attribution. | Not in the pack as a skill. A short deception screen runs inside `/quality-of-information-check`. |
| Premortem Analysis | Before release, assume the assessment turned out wrong and ask why. | Not in the pack |
| Structured Self-Critique | Before release, the authors review their own analysis against a fixed set of questions. | Not in the pack. `/quality-control` is editorial and schema review, not analytic self-critique. |
| Argument Mapping | A judgment needs its claim, premises, evidence and rebuttals laid out as a tree. | Not in the pack |
| Chronology | The order of events matters and gaps in the timeline need to be visible. | Not in the pack. `/campaign-tracking` holds a timeline per campaign. |

Brainstorming variants, nominal group technique, Delphi, mind maps, SWOT, force field analysis and decision matrices are workshop or general decision tools. They are not in the pack and are not planned.

## Pack skills that support the techniques

| Skill | Use when | Relation to the techniques |
|---|---|---|
| `/source-provenance` | You have a URL and need the originating source and the chain it arrived through. | First step inside the Quality of Information Check. Usable alone. |
| `/claim-extraction` | You need a report split into atomic, typed claims anchored to source sentences. | Second step inside the Quality of Information Check. Usable alone. |
| `/source-assessment` | You need the definitions of the Admiralty scale, or a grade for a single item such as a lookup result. | Reference for the scale. Documents are graded by `/quality-of-information-check`. |
| `/threat-assessment` | You are formally evaluating a threat by intent, capability and opportunity. | Assessment method. Requires graded evidence. |
| `/horizon-scanning` | You are looking forward for weak signals and emerging threats. | Forecasting method. Covers scenarios and early warning indicators in part. |
