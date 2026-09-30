---
name: quality-of-information-check
description: Use when evidence needs grading before anyone reasons from it — the user asks "how reliable is this?", "grade this source", "check this report", "can I trust this article?", "is this corroborated?", or hands over a URL, a pasted report or a Liberty91 event ahead of an ACH or assessment. The Quality of Information Check from the CIA Tradecraft Primer, adapted for vendor and press CTI reporting. Resolves each document to its originating source, splits it into claims, and grades every claim on two written elements, access level (how the source knows) and claim support (what backs the statement), with a stated rationale, using a fixed rubric with hard caps. The grade is not an Admiralty rating. Five outlets citing one vendor report count as one source; anything that cannot be traced to a primary is capped, not guessed. Returns a graded claim table, gaps, a deception screen and JSON. /ach, /threat-assessment and /writing-assessments run it first by default.
user-invocable: true
metadata:
  version: 1.0.0
  tags: [tradecraft, sat, diagnostic, sourcing, admiralty, grading]
  tradecraft: true
---

# quality-of-information-check

Grade the evidence before you reason about it.

A structured analytic technique run by prompt alone produces output that has the shape of the technique and none of its discipline. An ACH matrix built on whatever the model felt like trusting is worse than no matrix, because it looks rigorous. This skill is the step that comes first: it establishes what the evidence is, where it came from, and how much weight each claim can bear.

**Composition.** Invokes `/source-provenance`, then `/claim-extraction`, then applies the rubric, then hands to `/quality-control`. Optionally invokes `/lookup-*` skills for corroboration and `/lookup-liberty91` for platform data. Its output is the preferred input of `/ach`, `/threat-assessment` and `/writing-assessments`, and is consumed by `/key-assumptions-check`, `/intelligence-writing`, `/stix-bundle` and `/ioc-export`.

## Three principles

1. **Grade provenance chains, not outlets.** The grade belongs to this claim arriving by this chain. The same outlet carries a vendor's own telemetry finding and an attacker's boast in the same week.
2. **Grade claims, not events.** One report contains observations, attributions and assessments of very different standing. One grade for all of them is meaningless.
3. **Data does the research, the model applies the rubric.** The chain is resolved by the platform or by a script. Corroboration is counted from data. What is left for the model is labelled as model judgement.

## Inputs

- One or more URLs, pasted text, or Liberty91 event IDs.
- First-party observations: hits from `/lookup-sentinel` or the user's own EDR. These enter the claim table directly, graded direct and established (rubric rule R12), with `provenance_basis: first-party`. Steps 1 to 4 do not apply to them.
- Optional, and worth asking for: the question or hypothesis the evidence is meant to serve. With it, the skill can mark which claims are load-bearing.

## What the model may and may not do

| Allowed (model judgement, labelled as such) | Not allowed |
|---|---|
| Judge transmission fidelity | Assert a primary the script or platform did not resolve |
| Judge claim type | Assert corroboration not established by data or lookups |
| Apply the rubric | Infer access type from an organisation's reputation |
| Write the rationale | Invent or paraphrase vendor confidence language |
| Analyse gaps | Assign a grade above a cap |
| Run the deception screen | Apply a track record modifier outside Tier 1 |

If you know something about the incident that is not in the documents, it does not enter the grade. It can go in the gaps section as a lead to check.

## Procedure

The order is fixed. Do not grade before the chain is resolved. Do not resolve corroboration after grading.

### 1. Resolve provenance

Run `/source-provenance` for each input. Record `provenance_basis`:

| Tier | Basis | Meaning |
|---|---|---|
| 1 | `platform-resolved` | Liberty91 returned provenance fields for the event |
| 2 | `script-resolved` | `resolve_provenance.py` resolved the chain for this article |
| 3 | `model-judged` | Pasted text, or a page that could not be fetched. Every provenance field is unverified |

Tier 1 applies only when the platform response carries the provenance fields listed in `/lookup-liberty91` (`primaries[]`, `independent_primaries`, `chains[]`). A configured key is not enough. The platform also returns ratings of its own: an event-level `credibility` and `verification` status, a `source_count`, and a `reliability` letter and `stance` per source. These are not provenance fields and they are not grades. Do not copy them into `grading`, do not read `source_count` as `independent_primaries`, and do not treat a source with stance `corroborates` as corroboration. If they are all the platform returned, the run is Tier 2.

State the basis at the top of the output. When inputs differ, the run takes the worst. Items observed in the user's own telemetry carry `first-party`, which ranks above all three tiers.

For Tier 3, reconstruct only what the text itself says ("according to a report by X"). Record the organisation as named, the URL as `null`, and flag `unresolved_provenance`.

### 2. Extract claims

Run `/claim-extraction`:

- on the **primary** document, where one was resolved and read;
- on the **article** only for what it adds: attributed quotes, references to other primaries, and unattributed assertions (flagged `press_originated`).

If `/source-provenance` returned `other_primaries` or `primary_cites`, the claims found in or relayed from each belong to that organisation. Run a separate chain for any that matter to the question. A claim the primary relays from an organisation in `primary_cites` is graded on that organisation's document, not on the primary's access.

The cached text keeps table rows as lines with cells separated by ` | `. A table row can be an anchor.

### 3. Judge transmission fidelity

For each claim from the primary, compare the article's wording with the primary's anchor sentence. Record one value per hop:

| Fidelity | Meaning |
|---|---|
| `faithful` | Same assertion, same strength, same scope |
| `caveats_dropped` | The hedge, confidence level or scope limit is gone ("possibly linked to" became "attributed to") |
| `embellished` | The outlet added strength, scale or detail the primary does not contain |
| `not_carried` | The outlet does not repeat this claim. Not a fault, and no flag |
| `unresolved` | The hop could not be read, so the comparison could not be made |

Quote both wordings in the hop's `notes`. Where any hop is `caveats_dropped` or `embellished`, set flag `caveats_dropped_in_chain` and grade on the primary's wording.

The primary's own hop is always `faithful`: it is the origin. A user who gives you the primary directly has a one-hop chain with `fidelity: faithful`.

### 4. Establish corroboration

Per claim. Corroboration is counted by independent primaries with separate access, never by the number of articles.

| Tier | How |
|---|---|
| 1 | Read `independent_primaries` from the platform. `basis: platform`. |
| 2 and 3 | Default is `independent_primaries: 1`, `basis: unchecked`. |

Not corroboration:

- Vendor A citing vendor B.
- A government advisory that restates vendor reporting without adding evidence.
- Two outlets covering the same report.
- A second primary linked from the same article, until you have established it had its own access.
- A platform's event-level rating. `verification: corroborated`, `credibility: 1` or a `source_count` above 1 says that several reports exist, not that independent primaries agree.

In Tier 2 and 3, offer to check. Where a claim contains indicators, run the applicable lookups (`/lookup-virustotal`, `/lookup-otx`, `/lookup-misp`, `/lookup-opencti`, `/lookup-crowdstrike`, `/lookup-reversinglabs`) and count a confirmation only where a lookup shows a different organisation reporting the same indicator from its own data. Record `basis: lookups` and list each source. An OTX pulse that cites the same vendor report is the same source.

**Matching names across vendors.** Hashes, CVEs and infrastructure match exactly, in every tier. Actor, malware and tool names do not: one vendor's APT28 is another's Sednit.

| Available | Behaviour | `alias_source` |
|---|---|---|
| `LIBERTY91_API_KEY` | Resolve names through the Threat Library via `/lookup-liberty91`, including vendor-cluster merge records | `liberty91` |
| `references/aliases.yml` | Use the user's own alias file | `user` |
| Neither | Names are not matched across vendors. Corroboration for name-based claims stays at 1, unchecked | `none` |

`alias_source` records what was used for the claim. Set it to `none` on every claim where no name matching was done, whatever is configured.

With neither, say so in the gaps section and name both options. Do not match names from memory. The file format is in [`references/aliases.example.yml`](references/aliases.example.yml).

### 5. Apply the rubric

Apply [`references/grading-rubric.md`](references/grading-rubric.md) as written. The grade is two words, written out in full. It is not the Admiralty scale: never write it as a letter and a number, and never convert it to one. For each claim:

1. Access level, from the **stated access** for the claim. Claim type does not change it.
2. Claim support, from corroboration, the primary's **stated confidence** and consistency. For attribution and assessment claims, R13 fixes the level from the stated confidence.
3. The caps, R1 to R13.
4. A rationale of one to two sentences that names the access type, the corroboration count and basis, the stated confidence, and any cap that applied.

Tier 1 only: if the platform returns a track record score for the organisation and claim type, report it next to the grade and record `track_record_applied`. It moves the claim's footing by one band and never changes the access level. In Tier 2 and 3 the field is `none`.

A rationale that says only that the vendor is reputable is a failed rationale. It grades the name.

### 6. Compute recency and flags

`age_days` from `date_observed` to today. Where `date_observed` is `unknown`, from the primary's publication date. Set every flag in the schema's vocabulary that applies. `single_source` is set whenever `independent_primaries` is 1.

### 7. Run the deception screen

Apply [`references/deception-screen.md`](references/deception-screen.md): MOM, POP, MOSES, EVE. Answer each briefly. Always run it in full for `actor_claim` items and for attribution that rests on artefacts an adversary could plant. Set `deception_indicators_present` on the claims a raised flag touches.

### 8. Derive the event aggregate

Compute `event_qoi_summary` from the items. Never assign it. Identify the weakest link: the lowest-graded claim among those the bottom line depends on.

### 9. Write gaps and next steps

- What the evidence cannot tell us.
- What corroboration was not checked, and why.
- What would raise or lower each load-bearing grade.
- Which lookups would corroborate which claims. Whether to wait for a vendor follow-up.

### 10. Emit and validate

Write the human-readable output and the JSON envelope. Save the JSON and run:

```bash
python3 skills/quality-of-information-check/scripts/validate_evidence.py <qoi.json> \
  --source-text <primary.txt> [--source-text <article.txt>]
```

The source text files are the ones `/source-provenance` wrote to the local cache. Exit `0` is valid. Exit `1` lists violations: fix them and rerun. Do not return output that fails validation. Then hand to `/quality-control`.

## Output

```markdown
# Quality of Information Check

**Provenance basis:** script-resolved
**Assessed:** 2026-09-27
**Question served:** Who is behind the intrusions at regional water utilities?
**Documents:** <article title> (outlet, date) → <primary title> (organisation, date)
**TLP:** CLEAR

## Summary
Two to four sentences in plain English. What is well supported, what is judgement,
what is unverified, and what the weakest link is.

## Graded claims
Load-bearing claims first.

| ID | Claim | Type | Primary | Stated access | Access level | Claim support | Corrob. | Flags |
|---|---|---|---|---|---|---|---|---|
| C02 | ... | observation | Northwind | ir_engagement | direct | firm | 1 (unchecked) | single_source |

### Rationale
- **C02: direct, firm.** ...

### Chain and fidelity
| Hop | Organisation | Published | Fidelity | Note |
|---|---|---|---|---|

## Event aggregate
| Field | Value |
|---|---|
| Claims graded | 9 |
| Independent primaries | 1 |
| Most recent observation | 2026-08 |
| Grade range | direct and firm, down to untraced and tentative |
| Summary line | core facts direct and firm, attribution direct and tentative, trend statement press-originated |
| Weakest link | C04 |

## Gaps
## Deception screen
## Next steps

## What in this output is model judgement
Claim typing, transmission fidelity, rationale wording, the deception screen and the
gap analysis are model judgements. The provenance chain, publication dates, the
primary's access and confidence sentences, and the classification of sources were
resolved by <platform | script>. Grades follow a fixed rubric; caps were checked by
validate_evidence.py.
```

The last section is mandatory and its content follows the tier. In Tier 3 it must say that the provenance chain is also a model reconstruction.

The JSON envelope is specified in [`references/evidence-item-schema.md`](references/evidence-item-schema.md).

## Short form

When `/cti-orchestrator` routes a bare URL here, or the user wants a quick read, return the summary, the graded claim table and the weakest link, and offer the full output. Every step still runs, and the JSON is still validated. Only the presentation is shortened.

## Common errors

| Error | Correction |
|---|---|
| One grade for the whole report | Grade each claim |
| Grading the outlet | Grade the primary by access; grade the outlet on fidelity only |
| "Widely reported" treated as corroboration | Count independent primaries |
| A vendor's attribution graded established | Attribution is a judgement. R4 rules out established without a second primary, and R13 sets claim support from the vendor's stated confidence |
| Lowering the access level because the claim is a judgement | Access level follows access. The judgement is recorded in claim support |
| Copying the platform's credibility or reliability value | Those rate the event and the outlet. Grade the claim from the rubric |
| Writing the grade as a letter and a number | The grade is two words. It is not an Admiralty rating and has no Admiralty equivalent |
| Actor's data-volume figure repeated as fact | `actor_claim`, graded adversary and unverified, until corroborated |
| Own telemetry left out of the table as "not a report" | It is the top of the scale. Enter it as an observation graded direct and established |
| CVSS or EPSS entered as evidence | They are attributes of a CVE, not claims about the event |
| Access assumed from the vendor's product line | Access is what the document states. Otherwise `undisclosed`, which gives access level indirect at best |
| Filling an unresolved chain from memory | Unresolved is a finding. Cap and report |

## References

- [`references/evidence-item-schema.md`](references/evidence-item-schema.md): the contract with every downstream skill.
- [`references/grading-rubric.md`](references/grading-rubric.md): the rubric and the caps.
- [`references/deception-screen.md`](references/deception-screen.md): MOM, POP, MOSES, EVE with CTI prompts.
- [`references/worked-examples.md`](references/worked-examples.md): three full runs, one per tier.
- [`references/doctrine.md`](references/doctrine.md): where each part of the method comes from. Use it when asked "why this grade".
- [`references/aliases.example.yml`](references/aliases.example.yml): format of the user alias file.

## Related skills

- `/source-provenance`, `/claim-extraction`: the two steps this skill orchestrates.
- `/ach`, `/threat-assessment`, `/writing-assessments`: prefer graded evidence and run this skill first by default. They run without it when the user asks, in a labelled ungraded mode capped at Moderate confidence.
- `/quality-control`: validates the output.
- `/source-assessment`: the Admiralty scale reference. The evidence grade is a different instrument and is not converted to or from it.
- `/confidence-levels`, `/likelihood-language`: for the judgements built on this evidence.
