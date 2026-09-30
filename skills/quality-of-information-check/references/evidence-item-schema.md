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
      fidelity:              faithful | embellished | caveats_dropped | not_carried | unresolved
      notes:
  grading:
    access_level:            direct | limited | indirect | untraced | adversary
    claim_support:           established | firm | tentative | disputed | unverified
    rationale:               one to two sentences, referencing access, corroboration, stated confidence
    track_record_applied:    none | boundary_up | boundary_down   (Tier 1 only; "none" everywhere else)
  corroboration:
    independent_primaries:   integer, minimum 1 (this chain)
    basis:                   platform | script | lookups | unchecked
    sources:                 list of {org, url, date}
    alias_source:            user | liberty91 | none   (what was used to match actor/malware names for this claim)
  recency:
    date_observed:           ISO date or "unknown" (when the activity happened)
    date_published:          ISO date (primary)
    age_days:                integer, days from date_observed to the assessment date;
                             from date_published when date_observed is "unknown"
    superseded_by:           URL or null
  flags:                     subset of the flag vocabulary below
  provenance_basis:          first-party | platform-resolved | script-resolved | model-judged
```

### Field notes

- **The grade is two words, not a code.** `access_level` says how the source knows. `claim_support` says what backs the statement. It is written "direct, firm". It is not the Admiralty scale, uses none of its letters or numbers, and is never converted to or from an Admiralty rating. The old fields `source_reliability` and `information_credibility` are rejected by the validator. See the rubric for the difference.
- **`track_record_applied`** records a computed track record from the platform (Tier 1). It never changes `access_level`. It moves the claim's footing band by one.

- **`access: statement`** is used for an attributed quote from a named person at a primary organisation, reported in an article. The claim belongs to that organisation. A vendor employee quoted in an article is graded as the vendor, never as an independent researcher.
- **`stated_confidence`** is verbatim or `"not stated"`. It is never paraphrased and never invented.
- **`access`** is read from the primary's own text. If the primary does not say how it knows, the value is `undisclosed`. It is never inferred from the organisation's reputation. It is recorded per claim. The default is the access `/source-provenance` resolved for the document. Where the anchor sentence or its paragraph states a different basis for this claim, that basis is used and the rationale says so.
- **First-party observations.** A hit in the user's own telemetry is an evidence item with `primary_source.type: first_party`, `org: "user environment"`, `access: telemetry`, `claim_type: observation`, graded direct and established, and `provenance_basis: first-party` (rubric rule R12). The anchor is the query and the result line it returned. There is no chain and no URL. It can be load-bearing. A query that returned nothing is not an item.
- **`chain`** has one entry per hop. A user who hands the skill a vendor blog directly gets a one-entry chain with `fidelity: faithful`.
- **`fidelity`** describes how a hop transmitted the claim. The primary's own hop is always `faithful`: it is the origin, so there is nothing to compare it with. An outlet that does not repeat the claim at all gets `not_carried`. That is not a fault and sets no flag.
- **`alias_source`** records what was used, not what was available. It is `none` whenever no name matching was done for the claim, including when a key or an alias file is configured and the claim contains no actor, malware or tool name.
- **`load_bearing`** is set by `/quality-of-information-check` when the user supplies the question or hypothesis the evidence serves. Without one, the bottom-line statements of the document are treated as the things the claims bear on.
- Any field that could not be determined is `null` with a reason recorded in `notes` or the run's `unresolved` list. Never an empty string.

### Flag vocabulary

| Flag | Set when |
|---|---|
| `single_source` | `independent_primaries` is 1 |
| `unresolved_provenance` | no primary could be resolved for the claim |
| `commercial_interest` | primary `interest` is `commercial` and believing the claim favours the vendor: the claim says the vendor's product detected, blocked or would have prevented the activity, describes a weakness in a competitor's product, or is a trend or scale statement that supports demand for what the vendor sells. Reporting on activity seen in the vendor's own platform or telemetry does not set the flag by itself |
| `actor_sourced` | the claim originates from the threat actor |
| `caveats_dropped_in_chain` | any hop has `fidelity: caveats_dropped` or `embellished` |
| `press_originated` | an unattributed assertion by the journalist, not traceable to any primary |
| `retracted` | the primary has withdrawn the claim |
| `superseded` | a later report by the same primary replaces it (`superseded_by` is set) |
| `stale` | `age_days` above 180 on a fast-moving topic (R9) |
| `deception_indicators_present` | the deception screen raised a flag that touches this claim |
| `disputed` | two credible primaries disagree |
| `derived_from_confidence` | the grade was imported from a STIX/MISP confidence value, not assessed from a primary |
| `source_record_disputed` | the source has a documented record of inaccurate claims, cited in the rationale. This is track record, not access: it lowers the footing band by one and leaves `access_level` unchanged |

## Event aggregate

Derived from the items. Never assigned directly.

```yaml
event_qoi_summary:
  claims_graded:             integer
  independent_primaries:     integer
  most_recent_observation:   ISO date or "unknown"
  grade_range:               e.g. "direct and established, down to indirect and tentative"
  summary_line:              e.g. "core facts direct and firm, attribution tentative, scale claimed
                             by the actor and unverified"
  weakest_link:              claim_id of the lowest-graded load-bearing claim
  provenance_basis:          worst of the constituent items
```

Ordering for "worst" provenance basis: `first-party` is best, then `platform-resolved`, then `script-resolved`, then `model-judged`.

Ordering for "lowest grade": place each load-bearing claim in a footing band. The weakest link is the claim in the lowest band. Ties are broken by claim support (`unverified` lowest), then access level (`adversary` lowest), then `claim_id` (the lowest id is named). Where claims tie on band, claim support and access level, name the first as the weakest link and list the others with it in the summary line and in the confidence rationale.

| Band | Grade | Confidence the claim can support |
|---|---|---|
| 3 | Established, with access level direct or limited | High |
| 2 | Firm, or established with access level indirect | Moderate |
| 1 | Tentative | Low |
| 0 | Disputed or unverified | None. State the gap |

Access level `untraced` or `adversary` lowers the band by one, to a floor of 0. So does flag `source_record_disputed`. `track_record_applied` moves it one band down or up, to a ceiling of 3.

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
