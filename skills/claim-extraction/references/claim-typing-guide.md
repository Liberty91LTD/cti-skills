# Claim typing guide

Five types. The type decides how the claim can be graded, so getting it right matters more than getting the wording elegant.

The examples use invented organisations and actors.

## The test

Ask what would have to be true for the source to know this.

| The source would have to have... | Type |
|---|---|
| seen or measured it | `observation` |
| reasoned from evidence to a conclusion about who | `attribution` |
| reasoned from evidence to a conclusion about why, how capable, or what next | `assessment` |
| been told it by the actor | `actor_claim` |
| been told it by the victim | `victim_disclosure` |

The last two follow the originator, not the relay. A vendor blog that reports "the group states on its leak site that it took 400GB" contains an `actor_claim`. The vendor observed the posting; it did not observe the theft.

## Observation

Something seen or measured.

| Source text | Claim | Notes |
|---|---|---|
| "The loader contacts 203.0.113.42 over TCP/8443." | "The loader communicates with 203.0.113.42 on TCP/8443." | Direct technical finding |
| "We first observed this activity on 3 September." | "The activity was first observed on 3 September 2026." | Set `date_observed` |
| "The intruders used Cobalt Strike for lateral movement." | "The intruders used Cobalt Strike for lateral movement." | A tool seen in use |
| "Across our customer base we identified 41 affected organisations." | "The vendor identified 41 affected organisations in its own customer base." | Keep the scope. "41 victims" is a different and larger claim |

Observations carry a scope. "In our telemetry", "in the cases we responded to", "among the samples we analysed". Keep it in the claim. Without it the reader assumes the observation covers the world.

## Attribution

Linking activity to an actor, a country or a campaign.

| Source text | Claim | Notes |
|---|---|---|
| "We attribute this activity to Crimson Heron with high confidence." | "Vendor attributes the activity to Crimson Heron with high confidence." | Hedge preserved |
| "The infrastructure overlaps with that used in the 2025 Tidewater campaign." | "The infrastructure overlaps with infrastructure used in the 2025 Tidewater campaign." | Campaign linkage is attribution |
| "The operators are likely based in a UTC+3 time zone, judging by working hours." | "Vendor judges the operators are likely based in a UTC+3 time zone, from observed working hours." | Attribution to a geography |
| "Crimson Heron, which Agency X has linked to the Ministry of State Security" | Not this document's claim | The source is relaying another organisation's attribution. Flag for a second chain |

## Assessment

A judgement about intent, capability, future behaviour or significance.

| Source text | Claim |
|---|---|
| "We expect the group to expand targeting to operational technology." | "Vendor expects the group to expand targeting to operational technology." |
| "The objective appears to be long-term intelligence collection." | "Vendor judges the objective to be long-term intelligence collection." |
| "This represents a significant escalation in capability." | "Vendor judges the activity to represent a significant escalation in capability." |

Assessments often arrive dressed as observations. "The group is targeting the energy sector" sounds like something seen. If what was seen is three intrusions at energy companies, the observation is the three intrusions and the targeting statement is an assessment built on them.

## Actor claim

A statement originating with the threat actor.

| Source text | Claim |
|---|---|
| "The group listed the company on its leak site on 12 September." | "The actor listed the company on its leak site on 12 September 2026." (`observation`: someone saw the listing) |
| "The listing claims 400GB of data including patient records." | "The actor claims to hold 400GB of data including patient records." (`actor_claim`) |
| "A spokesperson for the group told the outlet they exploited a zero-day." | "The actor states it used a zero-day for access." (`actor_claim`) |

Note the split in the first two rows. That the listing exists is an observation. What the listing says is the actor's claim.

## Victim disclosure

A statement from the affected organisation or its regulatory filing.

| Source text | Claim |
|---|---|
| "In an 8-K filed Tuesday, the company said it detected unauthorised access on 2 September." | "The company states it detected unauthorised access on 2 September 2026." |
| "The hospital said patient care was not affected." | "The hospital states patient care was not affected." |
| "The notification letter says names and Social Security numbers were involved." | "The company's notification states names and Social Security numbers were involved." |

Victim disclosures are often deliberately narrow. "We have no evidence that data was taken" is a statement about the victim's evidence. Keep the wording.

## Boundary cases

### The Cobalt Strike triplet

| Text | Type | Why |
|---|---|---|
| "uses Cobalt Strike" | `observation` | The tool was seen in use |
| "is likely a Cobalt Strike affiliate of the group" | `attribution` | A judgement about who the operator is |
| "will expand to OT targets" | `assessment` | A judgement about future behaviour |

### "Exploited in the wild"

| Text | Type |
|---|---|
| "We observed exploitation attempts against our honeypots from 14 September." | `observation` |
| "The vulnerability is being exploited in the wild." with no statement of how the source knows | `observation`, with a note that access is not stated. It will be graded accordingly |
| "Exploitation is likely given the availability of a public proof of concept." | `assessment` |

### Victim counts

| Text | Type |
|---|---|
| "We identified 41 compromised hosts in our telemetry." | `observation` |
| "The campaign has likely affected hundreds of organisations." | `assessment` |
| "The group claims more than 200 victims." | `actor_claim` |

### Malware naming

"The sample is a variant of Lumen Stealer" is an `observation` when it rests on code comparison the source performed. "The sample was developed by the authors of Lumen Stealer" is an `attribution`.

### Motive

Any statement about what the actor wanted is an `assessment`, unless the actor said it, in which case it is an `actor_claim`.

## Hedging language and how to keep it

Sources hedge in three ways. All three stay in the claim.

**Explicit confidence statements.** Quote the level.

> "We assess with moderate confidence..." becomes "Vendor assesses with moderate confidence that..."

**Estimative words.** Keep the word the source used. Do not translate it into another scale.

> likely, unlikely, probably, possibly, almost certainly, we believe, we suspect, appears to, may have

**Relational hedges.** These describe a link that is weaker than identity. They are the ones most often flattened.

| Source says | It means | It does not mean |
|---|---|---|
| "overlaps with" | Some shared indicators or techniques | The same actor |
| "consistent with" | Nothing observed contradicts it | It is confirmed |
| "linked to" | Some connection, often unspecified | Attributed to |
| "associated with" | As above | As above |
| "shares code with" | Code reuse | Same developer or operator |
| "has been attributed to" | Someone else attributed it | This source attributes it |

If the source gives no hedge and no confidence statement, the claim carries none. Do not add one. The absence is recorded later as `stated_confidence: "not stated"`.

## Atomicity

One subject, one assertion.

| Compound | Split into |
|---|---|
| "Crimson Heron exploited CVE-2026-0001 to deploy the Embers backdoor." | (1) CVE-2026-0001 was exploited for initial access. `observation`. (2) The Embers backdoor was deployed after access. `observation`. (3) The activity is attributed to Crimson Heron. `attribution`. |
| "The group, which is state-sponsored, stole 2TB of data." | (1) The group is state-sponsored. `attribution`. (2) 2TB of data was taken. Type depends on who says so. |

Do not split further than grading requires. If three technique observations come from the same incident response engagement and would always receive the same grade, one claim listing the three techniques is correct.
