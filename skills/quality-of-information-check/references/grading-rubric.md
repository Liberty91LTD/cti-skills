# Grading rubric

Fixed. Apply it as written. Where a claim sits between two levels, take the lower level and say why in the rationale.

**The principle.** The grade is not a formality. It decides how much the analysis is allowed to claim. Confidence in a judgment is bounded above by the weakest load-bearing claim, and first-party observation is the top of the scale, not outside it.

The grade belongs to the claim and its provenance chain, never to the outlet that carried it. The same outlet transmits a vendor's own telemetry finding and an attacker's boast in the same week.

## The evidence grade

Every claim gets two elements, written out in words:

| Element | Question it answers | Values, strongest first |
|---|---|---|
| **Access level** | How does the source know this? | `direct`, `limited`, `indirect`, `untraced`, `adversary` |
| **Claim support** | What backs this statement? | `established`, `firm`, `tentative`, `disputed`, `unverified` |

Write both, in that order: "direct, firm". Never abbreviate them to a letter, a number or a code.

## This is not the Admiralty scale

The Admiralty scale (NATO AJP-2.1) rates a source from A to F and a piece of information from 1 to 6. The evidence grade is a different instrument. It uses none of the Admiralty letters or numbers, and an evidence grade must never be written, displayed or exported as one.

| | Admiralty scale | Evidence grade |
|---|---|---|
| First element | **Source reliability.** The source's track record: how often it has been right before | **Access level.** How the source knows this particular thing |
| Based on | History with the source, built up over time | What the document itself states about how the finding was made |
| Belongs to | The source | The claim |
| Same source, two claims | Same rating for both | Can differ: `direct` for what the source saw, `indirect` for what it repeats from public reporting |
| Second element | **Information credibility.** How likely the information is to be true | **Claim support.** What stands behind the statement: independent confirmation, direct observation, or judgement |
| Written as | A letter and a number | Two words |

Why access level and not track record:

- **Track record needs history the pack does not have.** Rating a vendor "usually reliable" requires a record of its past claims and how they turned out. Without that record, the rating is an impression of the vendor's reputation. This pack does not let the model grade by reputation.
- **Access can be read from the document.** A report either says "observed in our telemetry" or it does not. Two analysts reading the same report reach the same access level.
- **Access varies inside one report.** A vendor's report can hold its own incident response findings, a sample someone shared with it, and a summary of public reporting. One rating for the source hides that.

Track record is a separate measure. When a computed track record exists (Tier 1 only, from the Liberty91 platform), it is reported next to the grade and never changes the access level. See R10.

`/source-assessment` remains the pack's reference for the Admiralty scale itself. Use it where an Admiralty rating is asked for by name. Do not convert between the two: an evidence grade has no Admiralty equivalent.

## Access level

| Level | Criteria |
|---|---|
| **direct** | The source saw it: its own telemetry, its own incident response engagement, or the affected organisation's own formal disclosure. Also the user's own environment (first-party). |
| **limited** | The source examined an artefact but not the activity (sample analysis, partner data), or the claim is an attributed statement by a named person at the originating organisation. |
| **indirect** | The source does not say how it knows, repeats public or open-source reporting, or mixes its own findings with aggregation. A government advisory that aggregates without adding evidence. |
| **untraced** | No originating source could be found. A press report with no locatable origin. An unattributed assertion by a journalist (`press_originated`). |
| **adversary** | The attacker's own statement: leak site post, ransom note, forum or channel post. The source has a motive to mislead. |

The access level follows from the stated access:

| Stated access (`primary_source.access`) | Best access level available |
|---|---|
| `telemetry` in the user's own environment (first-party) | direct, and claim support established (R12) |
| `telemetry`, `ir_engagement` | direct |
| `victim_statement` in a regulatory filing or formal notification | direct |
| `sample_analysis` | limited |
| `statement` (attributed quote in an article) | limited |
| `osint` | indirect |
| `undisclosed` | indirect |
| `actor_statement` | adversary |
| none, primary unresolved | untraced |

Access level is set the same way for every claim type. An attribution or an assessment from a source with direct access keeps the level `direct`. What makes it a judgement is recorded in claim support (R4, R13).

Access is recorded per claim. It defaults to the access the script resolved for the document. Where the anchor sentence or its paragraph states a different basis for that claim ("public reporting indicates", "a partner shared a sample"), use the basis stated there and say so in the rationale. Never raise access above what the text states.

Access is never inferred from who the organisation is.

**A documented record of inaccurate claims** is track record, not access. It does not change the access level. Set flag `source_record_disputed`, cite the documentation in the rationale, and the claim's footing drops one band (see the schema). Do not set it from memory or reputation.

## Claim support

| Level | Criteria |
|---|---|
| **established** | An independent source with separate access reports the same thing. Or the user saw it in their own environment (R12). |
| **firm** | One source, which observed it directly. Consistent with other reporting, logical, nothing contradicts it. |
| **tentative** | One source, and either the source's access is not direct, or the claim is a judgement (attribution or assessment) that the source states with moderate confidence or with none. |
| **disputed** | Contradicted by other reporting, internally inconsistent, or a judgement the source itself states with low confidence. |
| **unverified** | Nothing to judge it by. Unresolved provenance with nothing else to go on, or an attacker's claim with no corroboration. |

## Caps and rules

These are hard limits. `validate_evidence.py` rejects output that breaks them.

| # | Rule | Effect |
|---|---|---|
| R1 | Provenance unresolved | Access level `untraced`. Claim support `tentative` at best. Flag `unresolved_provenance`. |
| R2 | Actor claim about scale, victim count or data volume | Access level `adversary`, claim support `unverified`, until an independent primary corroborates. Flag `actor_sourced`. |
| R3 | Any `actor_claim` | Access level `adversary`. Claim support `tentative` at best without corroboration. |
| R4 | Attribution claim | Claim support `firm` at best unless two independent primaries agree (`independent_primaries` of 2 or more). |
| R5 | Claim support `established` | Requires `independent_primaries` of 2 or more and a `corroboration.basis` other than `unchecked`. |
| R6 | `press_originated` claim | Access level `untraced`. Claim support `tentative` at best. Not load-bearing unless the user promotes it. |
| R7 | Caveats dropped in the chain | Grade on the primary's wording, not the outlet's. Flag `caveats_dropped_in_chain`. |
| R8 | Stated access | Access level no better than the access table allows. `undisclosed` gives `indirect` at best. |
| R9 | `age_days` above 180 on a fast-moving topic | Flag `stale`. Does not change the grade by itself; say so in the rationale. `age_days` counts from `date_observed` when the document gives it, and from `date_published` when it does not. |
| R10 | Track record | Tier 1 only. Reported next to the grade. Never changes the access level. May move the claim's footing one band, recorded as `track_record_applied`. |
| R11 | Grade imported from a STIX or MISP confidence value | Flag `derived_from_confidence`. Re-grade when a primary is available. |
| R12 | First-party observation: a hit in the user's own telemetry | Access level `direct`, claim support `established`, `claim_type: observation`, `access: telemetry`, source "user environment", `provenance_basis: first-party`. Exempt from R5: the user saw it directly, so no second primary is needed. Claim support drops to `firm` only where log tampering is suspected, with `deception_indicators_present` set. A miss is never an item. |
| R13 | Judgement claim (`attribution` or `assessment`) on fewer than two independent primaries | Claim support follows the primary's stated confidence, verbatim. High confidence: `firm` for attribution, `tentative` for assessment. Moderate: `tentative`. Low: `disputed`. Not stated: `tentative`. A hedge word in the anchor ("likely", "consistent with") is not a confidence statement and does not raise the level. |

"Fast-moving" for R9: active exploitation, live campaigns, ransomware group activity, infrastructure indicators. An actor's doctrine or a vulnerability's technical description ages more slowly; use judgement and state it.

## Grading by claim type

A single vendor report contains claims of different standing. The most common grading error is flattening them into one grade.

| Claim type | Typical grade | Reasoning |
|---|---|---|
| `observation` in the user's own environment | direct, established | First-party. Nothing is more load-bearing than seeing the indicator in your own network. R12. |
| `observation` from a vendor's own telemetry or IR | direct, firm | The source saw it. `established` only with a second independent primary. |
| KEV listing | as any government claim | A claim by CISA that exploitation was observed. Graded on the access the entry states. |
| `observation` from sample analysis | limited, firm | Direct analysis, but of an artefact, not of the intrusion. |
| `victim_disclosure` in a regulatory filing | direct, firm | The affected party, under legal obligation. Note that disclosures are often deliberately narrow. |
| `attribution` | access as stated; tentative | A judgement, even from a source with direct access. Claim support follows the vendor's own confidence language (R13) and is capped by R4. |
| `assessment` of intent or future behaviour | access as stated; tentative | Judgement about things nobody observed. `tentative` at best on one primary (R13). |
| `actor_claim` | adversary; tentative to unverified | The actor has a motive to inflate. Capped by R2 and R3. |
| `press_originated` | untraced, tentative at best | No primary behind it. |

## Writing the rationale

One to two sentences. Reference the things the grade rests on: the stated access, the corroboration count and basis, and the primary's stated confidence. Name any cap that applied.

Good:

> Direct, firm. Unit 42 states the finding comes from its own incident response engagements; no independent primary located (corroboration unchecked).

> Direct, tentative. Attribution judgement from a primary reporting its own telemetry. The primary states "moderate confidence". Single primary, so R4 rules out established and R13 places it at tentative.

> Adversary, unverified. The 400GB figure is the actor's own leak-site statement. No corroboration. R2 applies.

Bad:

> Direct, established. Mandiant is a highly reputable vendor.

That rationale grades the name. It says nothing about how Mandiant knows, whether anyone else confirmed it, or how confident Mandiant itself was.

## What the model may not do

- Assert a primary that the script or platform did not resolve.
- Assert corroboration that was not established by platform data, the script, or lookups.
- Infer access from the organisation's reputation.
- Invent or paraphrase vendor confidence language.
- Assign a grade above a cap.
- Write an evidence grade as an Admiralty rating, or convert one into the other.
- Copy a rating from a platform or feed into a grade. An event-level credibility value, a verification status or a per-source reliability letter returned by an API is that system's rating of the event or the outlet. It is not a grade for a claim.
- Apply a track record outside Tier 1, or let one change the access level.
- Treat CVSS or EPSS as evidence about an event. They are attributes of a CVE and do not enter the claim table.
