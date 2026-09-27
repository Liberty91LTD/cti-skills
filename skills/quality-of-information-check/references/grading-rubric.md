# Grading rubric

Fixed. Apply it as written. Where a claim sits between two bands, take the lower band and say why in the rationale.

**The principle.** The grade is not a formality. It decides how much the analysis is allowed to claim. Confidence in a judgment is bounded above by the weakest load-bearing claim, and first-party observation is the top of the scale, not outside it.

The grade belongs to the claim and its provenance chain, never to the outlet that carried it. The same outlet transmits an A1 telemetry finding and an F6 actor claim in the same week.

## Source reliability (the primary)

| Grade | Criteria |
|---|---|
| **A** | Established vendor or government with direct access (telemetry or incident response engagement) and no known retractions on this kind of claim. A victim's own regulatory disclosure. |
| **B** | Established vendor or government reporting from sample analysis or partner data. Well-known independent researcher with a history of published work. |
| **C** | Newer vendor. Access undisclosed. Reporting that mixes own findings with aggregation. Government advisory that aggregates without adding evidence. |
| **D** | Unresolved primary. Press report with no locatable originating source. Unattributed journalist assertion (`press_originated`). |
| **E** | Source with a known, documented history of inaccurate or inflated claims. Requires a citation in the rationale. |
| **F** | Cannot be judged. An actor's own claims default here regardless of how often they turn out true. |

Reliability is driven by **access**, not by name recognition:

| Primary's stated access | Highest reliability available |
|---|---|
| `telemetry` in the user's own environment (first-party) | A, and credibility 1 (R12) |
| `telemetry`, `ir_engagement` | A |
| `victim_statement` in a regulatory filing or formal notification | A |
| `sample_analysis` | B |
| `statement` (attributed quote in an article) | B |
| `osint` | C |
| `undisclosed` | C |
| `actor_statement` | F |
| none, primary unresolved | D |

"Track record" in the A and B definitions means:

- **Tier 2 and Tier 3** (script-resolved, model-judged): the absence of known retractions. The model does not rank vendors by reputation.
- **Tier 1** (platform-resolved): the registry score returned by the platform, applied as a boundary modifier only. It can move a source between A and B, or B and C, when access alone puts it on the line. It never lifts a source past what its access type supports, and never overrides a cap. Record `track_record_applied: boundary_up` or `boundary_down`. In Tier 2 and 3 this field is always `none`.

## Information credibility (per claim)

| Grade | Criteria |
|---|---|
| **1** | Confirmed by an independent primary with separate access. |
| **2** | Probably true. Single primary with direct access, consistent with other reporting, logical, no contradiction. |
| **3** | Possibly true. Single primary with indirect access, or an attribution-type claim with stated moderate confidence. |
| **4** | Doubtful. Contradicted by other reporting, or internally inconsistent. |
| **5** | Improbable. |
| **6** | Cannot be judged. Unresolved provenance with nothing else to go on, or an actor claim with no corroboration. |

## Caps and rules

These are hard limits. `validate_evidence.py` rejects output that breaks them.

| # | Rule | Effect |
|---|---|---|
| R1 | Provenance unresolved | Reliability D. Credibility no better than 3. Flag `unresolved_provenance`. |
| R2 | Actor claim about scale, victim count or data volume | Reliability F, credibility 6, until an independent primary corroborates. Flag `actor_sourced`. |
| R3 | Any `actor_claim` | Reliability F. Credibility no better than 3 without corroboration. |
| R4 | Attribution claim | Credibility no better than 2 unless two independent primaries agree (`independent_primaries` of 2 or more). |
| R5 | Credibility 1 | Requires `independent_primaries` of 2 or more and a `corroboration.basis` other than `unchecked`. |
| R6 | `press_originated` claim | Reliability D. Credibility no better than 3. Not load-bearing unless the user promotes it. |
| R7 | Caveats dropped in the chain | Grade on the primary's wording, not the outlet's. Flag `caveats_dropped_in_chain`. |
| R8 | Primary access `undisclosed` | Reliability no better than C. |
| R9 | Older than 180 days on a fast-moving topic | Flag `stale`. Does not change the grade by itself; say so in the rationale. |
| R10 | Track record modifier | Tier 1 only. Boundary moves only. |
| R11 | Imported grade (from STIX or MISP confidence) | Flag `derived_from_confidence`. Re-grade when a primary is available. |
| R12 | First-party observation: a hit in the user's own telemetry | A1, `claim_type: observation`, `access: telemetry`, source "user environment", `provenance_basis: first-party`. Exempt from R5: the user saw it directly, so no second primary is needed. Credibility drops to 2 only where log tampering is suspected, with `deception_indicators_present` set. A miss is never an item. |

"Fast-moving" for R9: active exploitation, live campaigns, ransomware group activity, infrastructure indicators. An actor's doctrine or a vulnerability's technical description ages more slowly; use judgement and state it.

## Grading by claim type

A single vendor report contains claims of different standing. The most common grading error is flattening them into one grade.

| Claim type | Typical range | Reasoning |
|---|---|---|
| `observation` in the user's own environment | A1 | First-party. Nothing is more load-bearing than seeing the indicator in your own network. R12. |
| `observation` from a vendor's own telemetry or IR | A1 to A2 | The primary saw it directly. Credibility 1 only with a second independent primary. |
| KEV listing | as any government claim | A claim by CISA that exploitation was observed. Graded on the access the entry states. |
| `observation` from sample analysis | B2 | Direct analysis, but of an artefact, not of the intrusion. |
| `victim_disclosure` in a regulatory filing | A1 to A2 | The affected party, under legal obligation. Note that disclosures are often deliberately narrow. |
| `attribution` | B2 to C3 | An analytical judgement even from an A source. Carries the vendor's own confidence language. Capped by R4. |
| `assessment` of intent or future behaviour | B3 to C3 | Judgement about things nobody observed. |
| `actor_claim` | F3 to F6 | The actor has a motive to inflate. Capped by R2 and R3. |
| `press_originated` | D3 at best | No primary behind it. |

## Writing the rationale

One to two sentences. Reference the things the grade rests on: access type, corroboration count and basis, and the primary's stated confidence. Name any cap that applied.

Good:

> B2. Unit 42 states the finding comes from its own incident response engagements; no independent primary located (corroboration unchecked).

> C3. Attribution judgement; Microsoft states "moderate confidence". Single primary, so R4 caps credibility at 2 and the moderate confidence language places it at 3.

> F6. The 400GB figure is the actor's own leak-site statement. No corroboration. R2 applies.

Bad:

> A1. Mandiant is a highly reputable vendor.

That rationale grades the name. It says nothing about how Mandiant knows, whether anyone else confirmed it, or how confident Mandiant itself was.

## What the model may not do

- Assert a primary that the script or platform did not resolve.
- Assert corroboration that was not established by platform data, the script, or lookups.
- Infer access type from the organisation's reputation.
- Invent or paraphrase vendor confidence language.
- Assign a grade above a cap.
- Apply a track record modifier in Tier 2 or Tier 3.
- Treat CVSS or EPSS as evidence about an event. They are attributes of a CVE and do not enter the claim table.
