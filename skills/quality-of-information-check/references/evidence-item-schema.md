# Evidence item schema

One record per claim. This is the contract between `/source-provenance`, `/claim-extraction`, `/quality-of-information-check` and every skill downstream (`/ach`, `/threat-assessment`, `/writing-assessments`, `/key-assumptions-check`, `/stix-bundle`, `/ioc-export`, `/quality-control`).

`scripts/validate_evidence.py` enforces this schema. If the two disagree, the script is wrong and should be fixed to match this file.

## Evidence item

```yaml
evidence_item:
  claim_id:                  string, stable within a run (e.g. C01)
  claim:                     one sentence, the analyst-usable statement
  claim_type:                observation | attribution | assessment | actor_claim | victim_disclosure
  load_bearing:              true | false   (does the bottom line depend on this claim?)
  anchor:
    document_url:            URL of the document the claim was extracted from, or null for pasted text
    sentence:                verbatim sentence(s) the claim rests on
    location:                paragraph index or heading
  primary_source:
    org:                     e.g. Mandiant, CISA, victim name, actor name; null if unresolved
    type:                    vendor | government | victim | actor | researcher | press | first_party | unknown
    title:                   report title
    date_published:          ISO date
    url:                     URL if resolved, else null
    access:                  telemetry | ir_engagement | sample_analysis | osint | actor_statement |
                             victim_statement | statement | undisclosed
    stated_confidence:       verbatim vendor/government confidence language, or "not stated"
    interest:                commercial | governmental | victim | actor | independent
  chain:                     ordered list, outlet nearest the user first, primary last
    - org:
      url:
      date_published:
      fidelity:              faithful | embellished | caveats_dropped | unresolved
      notes:
  grading:
    source_reliability:      A | B | C | D | E | F
    information_credibility: 1 | 2 | 3 | 4 | 5 | 6
    rationale:               one to two sentences, referencing access, corroboration, stated confidence
    track_record_applied:    none | boundary_up | boundary_down   (Tier 1 only; "none" everywhere else)
  corroboration:
    independent_primaries:   integer, minimum 1 (this chain)
    basis:                   platform | script | lookups | unchecked
    sources:                 list of {org, url, date}
    alias_source:            user | liberty91 | none   (how actor/malware names were matched)
  recency:
    date_observed:           ISO date or "unknown" (when the activity happened)
    date_published:          ISO date (primary)
    age_days:                integer, computed from the assessment date
    superseded_by:           URL or null
  flags:                     subset of the flag vocabulary below
  provenance_basis:          first-party | platform-resolved | script-resolved | model-judged
```

### Field notes

- **`access: statement`** is used for an attributed quote from a named person at a primary organisation, reported in an article. The claim belongs to that organisation. A vendor employee quoted in an article is graded as the vendor, never as an independent researcher.
- **`stated_confidence`** is verbatim or `"not stated"`. It is never paraphrased and never invented.
- **`access`** is read from the primary's own text. If the primary does not say how it knows, the value is `undisclosed`. It is never inferred from the organisation's reputation.
- **First-party observations.** A hit in the user's own telemetry is an evidence item with `primary_source.type: first_party`, `org: "user environment"`, `access: telemetry`, `claim_type: observation`, grade A1 and `provenance_basis: first-party` (rubric rule R12). The anchor is the query and the result line it returned. There is no chain and no URL. It can be load-bearing. A query that returned nothing is not an item.
- **`chain`** has one entry per hop. A user who hands the skill a vendor blog directly gets a one-entry chain with `fidelity: faithful`.
- **`load_bearing`** is set by `/quality-of-information-check` when the user supplies the question or hypothesis the evidence serves. Without one, the bottom-line statements of the document are treated as the things the claims bear on.
- Any field that could not be determined is `null` with a reason recorded in `notes` or the run's `unresolved` list. Never an empty string.

### Flag vocabulary

| Flag | Set when |
|---|---|
| `single_source` | `independent_primaries` is 1 |
| `unresolved_provenance` | no primary could be resolved for the claim |
| `commercial_interest` | primary `interest` is `commercial` and the claim concerns the vendor's own product area or a competitor |
| `actor_sourced` | the claim originates from the threat actor |
| `caveats_dropped_in_chain` | any hop has `fidelity: caveats_dropped` or `embellished` |
| `press_originated` | an unattributed assertion by the journalist, not traceable to any primary |
| `retracted` | the primary has withdrawn the claim |
| `superseded` | a later report by the same primary replaces it (`superseded_by` is set) |
| `stale` | older than 180 days on a fast-moving topic |
| `deception_indicators_present` | the deception screen raised a flag that touches this claim |
| `disputed` | two credible primaries disagree |
| `derived_from_confidence` | the grade was imported from a STIX/MISP confidence value, not assessed from a primary |

## Event aggregate

Derived from the items. Never assigned directly.

```yaml
event_qoi_summary:
  claims_graded:             integer
  independent_primaries:     integer
  most_recent_observation:   ISO date or "unknown"
  grade_range:               e.g. "A1 to C3"
  summary_line:              e.g. "core facts A1 to B2, attribution C3, scale actor-claimed"
  weakest_link:              claim_id of the lowest-graded load-bearing claim
  provenance_basis:          worst of the constituent items
```

Ordering for "worst" provenance basis: `first-party` is best, then `platform-resolved`, then `script-resolved`, then `model-judged`.

Ordering for "lowest grade": place each load-bearing claim in a footing band. The weakest link is the claim in the lowest band. Ties are broken by credibility (6 lowest), then reliability (F and E lowest).

| Band | Grade | Confidence the claim can support |
|---|---|---|
| 3 | Credibility 1, with reliability A or B | High |
| 2 | Credibility 2, or credibility 1 with reliability C | Moderate |
| 1 | Credibility 3 | Low |
| 0 | Credibility 4, 5 or 6 | None. State the gap |

Reliability D, E or F lowers the band by one, to a floor of 0.

These are the bands `/threat-assessment` and `/writing-assessments` use for the confidence ceiling, so the weakest link named here is the claim that sets the ceiling there.

The aggregate is a triage filter and a display convenience. `/ach` consumes the items, not the aggregate.

## JSON envelope

`/quality-of-information-check` emits this alongside the human-readable table:

```json
{
  "qoi_version": "1.0",
  "assessed_at": "2026-09-27",
  "provenance_basis": "script-resolved",
  "question": "Who is behind the intrusion at Example Health?",
  "documents": [
    {"url": "https://...", "role": "article"},
    {"url": "https://...", "role": "primary"}
  ],
  "evidence_items": [ { "claim_id": "C01", "...": "..." } ],
  "event_qoi_summary": { "...": "..." },
  "gaps": ["..."],
  "deception_screen": {
    "mom": "...", "pop": "...", "moses": "...", "eve": "...",
    "flags_raised": []
  },
  "next_steps": ["..."],
  "model_judgements": ["claim_type", "fidelity", "rationale", "deception_screen", "gaps"]
}
```

`model_judgements` is fixed text. It states which parts of the output are the model's judgement rather than resolved data, so a reader can see the line.
