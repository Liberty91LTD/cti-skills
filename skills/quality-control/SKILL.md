---
name: quality-control
description: Peer review checklist and quality standards for intelligence products, plus schema validation for graded evidence items and claim tables from /quality-of-information-check and /claim-extraction. Rejects outputs that break the evidence schema or the grading caps. Loaded by the quality-reviewer agent.
user-invocable: false
metadata:
  version: 2.0.0
---

# Quality Control Standards

## Review Process

1. All products must be reviewed before moving to "published" status
2. Reviews are performed by the quality-reviewer agent
3. Products with CRITICAL issues are returned for revision
4. Products with 3+ MAJOR issues are returned for revision
5. MINOR issues are noted but don't block publication
6. Evidence validation runs before the checklist. A product that fails it is returned without being scored.

## Evidence Validation

This is the enforcement point for `/claim-extraction` and `/quality-of-information-check` output, and for any product built on it (`/ach`, `/threat-assessment`, `/writing-assessments`). The schema is in `skills/quality-of-information-check/references/evidence-item-schema.md`. The caps are rules R1 to R13 in `skills/quality-of-information-check/references/grading-rubric.md`.

Two passes, in this order.

### Pass 1: Script check

```bash
python3 skills/quality-of-information-check/scripts/validate_evidence.py <qoi.json> [--source-text <file>]
```

- Exit 0: valid. Go to Pass 2.
- Exit 1: violations, listed on stdout as JSON. Each one is a CRITICAL issue. Return the output for revision with the list attached. Do not fix grades or anchors yourself.
- Pass `--source-text` whenever the source document text is available, so anchors can be checked against it.
- If the script cannot be run, say so in the review and do every check in the table below by hand. Do not report the script check as passed.

### Pass 2: Reviewer check

The script covers what can be checked mechanically. The reviewer then reads the claim table against the source and confirms each rule below. Any failure is CRITICAL and the output is rejected.

| # | Reject when | How to check |
|---|---|---|
| V1 | An anchor is missing | Every item has `anchor.sentence` and `anchor.location`, non-empty |
| V2 | Anchor text is not present verbatim in the source | Find `anchor.sentence` in the source text, character for character. A paraphrase fails |
| V3 | A claim contains two assertions | One subject, one assertion. A compound "and" joining two facts that could be graded differently fails |
| V4 | `claim_type` is not one of the five values | `observation`, `attribution`, `assessment`, `actor_claim`, `victim_disclosure`. `press_originated` is a flag, not a type |
| V5 | A grade exceeds a cap | Rules R1 to R13. See the table below |
| V6 | Corroboration is asserted without basis | `independent_primaries` of 2 or more needs a `basis` other than `unchecked` and a `sources` entry for each additional primary. The same applies to any "corroborated by" wording in the rationale or the product text |
| V7 | `provenance_basis` is absent | Present on every item and in the output header, with one of `platform-resolved`, `script-resolved`, `model-judged` |
| V8 | Claim count is outside five to twelve for a primary | Count claims per primary document. Claims from attributed quotes in an article are additional and not counted. Allowed outside the range only when the user asked for it, and the output says so |
| V9 | A grade is not two words | `grading.access_level` and `grading.claim_support` each hold one of the rubric's values. The old fields `source_reliability` and `information_credibility`, a letter, a number or a code all fail |

Cap checks for V5:

| Rule | Fails when |
|---|---|
| R1 | Provenance unresolved and access level is not `untraced`, claim support is better than `tentative`, or `unresolved_provenance` is not flagged |
| R2 | Actor claim about scale, victim count or data volume, uncorroborated, graded other than adversary, unverified, or `actor_sourced` is not flagged |
| R3 | `actor_claim` with access level other than `adversary`, or claim support better than `tentative` without corroboration |
| R4 | `attribution` with claim support `established` and fewer than 2 independent primaries |
| R5 | Claim support `established` with fewer than 2 independent primaries, or with `basis: unchecked` |
| R6 | `press_originated` with access level other than `untraced`, claim support better than `tentative`, or `load_bearing: true` without a recorded user promotion |
| R7 | A hop has `fidelity: caveats_dropped` or `embellished` and the claim uses the outlet's wording, or `caveats_dropped_in_chain` is not flagged |
| R8 | Access level better than the rubric's access table allows for the stated access. Primary access `undisclosed` and access level better than `indirect` |
| R9 | Older than 180 days on a fast-moving topic and `stale` is not flagged |
| R10 | `track_record_applied` is anything other than `none` when `provenance_basis` is not `platform-resolved`, or a track record has changed the access level |
| R11 | Grade imported from a STIX or MISP confidence value and `derived_from_confidence` is not flagged |
| R12 | A first-party observation that is not `claim_type: observation`, `access: telemetry`, access level `direct` and `provenance_basis: first-party`, or `provenance_basis: first-party` on anything that is not the user's own telemetry. CVSS or EPSS entered as an evidence item |
| R13 | An `attribution` or `assessment` on fewer than two independent primaries graded above what the primary's stated confidence supports: high gives `firm` for attribution and `tentative` for assessment, moderate gives `tentative`, low gives `disputed`, "not stated" gives `tentative` |

Also reject (CRITICAL) when the access level is above what the primary's stated access supports (the access table in the rubric), when a documented record of inaccurate claims has changed the access level instead of setting `source_record_disputed`, when `stated_confidence` is paraphrased rather than verbatim or "not stated", or when a rationale grades the organisation's name instead of access, corroboration and stated confidence.

### Products built on graded evidence

| Product | Reject (CRITICAL) when |
|---|---|
| `/ach` output | No `Evidence basis` in the header. An ungraded row carries a weight other than 1, or a grade that did not come from `/quality-of-information-check` and is not an Admiralty rating marked `(analyst)`. A non-diagnostic row is scored. The heaviest inconsistent item per hypothesis is not reported. No `provenance_basis` in the header. A graded matrix row has no `claim_id`, `claim_type`, access level or claim support. A `press_originated` or non-load-bearing item is treated as a linchpin without a recorded promotion. A linchpin that is `single_source` or has claim support `unverified` is not called out |
| Assessments | Confidence is above the weakest-link ceiling defined in `/threat-assessment` (High needs every load-bearing claim at claim support established with access level direct or limited; firm, or established with access level indirect, caps at Moderate; tentative at Low; disputed or unverified means no confidence level; access level untraced or adversary, or flag `source_record_disputed`, lowers the result by one level). A confidence label is given where the ceiling is "no confidence level". The weakest link is not named in the confidence rationale. Sources lack the primary, the access level, the claim support or `provenance_basis` |
| Any product | Evidence from reporting that is not in the graded claim table appears without being marked ungraded. The product rests on ungraded evidence and the header does not say `Evidence basis: ungraded` or `mixed`. Confidence is above Moderate while a load-bearing item is ungraded. An ungraded item is shown with a grade that was not produced by `/quality-of-information-check` and is not marked `(analyst)`. An evidence grade is shown as a letter and a number, or is labelled Admiralty. An analyst's own Admiralty rating on an ungraded item is shown without the word Admiralty, for example `B2 (analyst)` instead of `Admiralty B2 (analyst)`. An evidence grade is converted into an Admiralty rating, or an Admiralty rating into an evidence grade |

## Peer Review Checklist

### A. Structural Integrity (Weight: 15%)
- [ ] Correct product template used
- [ ] Complete frontmatter (all required fields)
- [ ] TLP marking present and correctly applied
- [ ] Logical section ordering
- [ ] Appropriate length for product type

### B. Analytical Rigor (Weight: 30%)
- [ ] Conclusions supported by evidence
- [ ] Key assumptions explicitly identified
- [ ] Alternative hypotheses considered (where applicable)
- [ ] Structured analytic techniques applied appropriately
- [ ] No logical leaps or unsupported assertions
- [ ] Temporal scope specified for all predictions
- [ ] Intelligence gaps acknowledged

### C. Sourcing (Weight: 20%)
- [ ] Every claim cites its primary (the originating organisation), not the outlet that carried it
- [ ] Evidence grade (access level and claim support, in words) given per claim, not per outlet or per event
- [ ] Grade rationale references access, corroboration and stated confidence
- [ ] Corroboration counted by independent primaries with separate access. Several outlets covering one primary count as one source
- [ ] Single-source claims flagged as such
- [ ] Outlets recorded as chain hops with transmission fidelity, caveats restored to the primary's wording
- [ ] `provenance_basis` stated in the product
- [ ] No unattributed claims. Unresolved provenance is stated, not guessed

### D. Mandated Language (Weight: 20%)
- [ ] Confidence levels on all assessments (with rationale naming the weakest load-bearing claim)
- [ ] Likelihood language on all predictions (with percentage ranges)
- [ ] No hedge-stacking
- [ ] No vague probabilistic language without probability band
- [ ] Confidence and likelihood not conflated
- [ ] Facts clearly distinguished from assessments

### E. Technical Accuracy (Weight: 10%)
- [ ] MITRE ATT&CK mappings correct
- [ ] IOCs properly formatted and validated
- [ ] Technical claims verifiable
- [ ] No contradictions with known intelligence

### F. Writing Quality (Weight: 5%)
- [ ] BLUF in first paragraph
- [ ] Active voice
- [ ] Specific language (dates, numbers, names)
- [ ] No unnecessary jargon
- [ ] Clear, concise sentences

## Scoring

Calculate weighted score (0-10):
- Each section: 0 (none met) to 10 (all met)
- Weighted by percentages above
- Final score = weighted average

| Score | Verdict |
|-------|---------|
| 8-10 | Approved — publish |
| 6-7 | Approved with minor revisions — can publish after fixes |
| 4-5 | Revision required — significant issues |
| 0-3 | Rejected — fundamental problems |

## Issue Severity

- **CRITICAL**: Factual error in key finding, missing TLP on sensitive content, unsupported primary conclusion, potential harm if published as-is, any Evidence Validation failure (script violation or V1 to V9)
- **MAJOR**: Missing confidence level on assessment, vague likelihood language on prediction, missing source assessment on key evidence, logical flaw in reasoning, missing key section
- **MINOR**: Grammar/formatting, style inconsistency, minor disagreement over an Admiralty rating on a lookup result, non-essential section could be improved
