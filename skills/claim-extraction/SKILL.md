---
name: claim-extraction
description: Use when a report or article needs to be split into individual claims before it is graded, cited or used as evidence — the user asks "what does this report actually claim?", "split this into claims", "separate the facts from the judgements", or another skill needs a claim list. Turns one document into five to twelve atomic claims, each typed (observation, attribution, assessment, actor claim, victim disclosure) and anchored to the verbatim sentence it rests on, so every extraction can be checked against the source. Preserves the source's own hedging. Does not grade. Invoked by /quality-of-information-check; its output feeds /ach, /key-assumptions-check, /intelligence-writing, /writing-assessments and /threat-actor-profiling.
user-invocable: true
metadata:
  version: 1.0.0
  tags: [tradecraft, claims, sourcing, sat]
  tradecraft: true
---

# claim-extraction

An event is a bundle of claims with very different evidentiary standing. "Akira exploited a SonicWall zero-day to hit a US hospital and exfiltrated 400GB" is at least four claims:

| Claim | Type | Where it comes from |
|---|---|---|
| The hospital suffered an intrusion | `victim_disclosure` | The hospital's own notification |
| Initial access was through a SonicWall vulnerability | `observation` | A vendor's incident response finding |
| The intrusion was carried out by Akira | `attribution` | A leak-site posting plus TTP overlap |
| 400GB of data was taken | `actor_claim` | The actor's own statement |

One grade on the event either averages these into something meaningless or takes the strongest and inflates the weakest. This skill splits the document so each claim can be graded on its own.

**Composition.** Uses the fetcher in `/source-provenance`. Invoked by `/quality-of-information-check`. Output is consumed by `/ach`, `/key-assumptions-check`, `/intelligence-writing`, `/writing-assessments`, `/threat-actor-profiling` and `/campaign-tracking`.

## Inputs

- Document text, or a URL.
- Optional focus: "attribution only", "IOCs and TTPs only", or the question the claims are meant to serve.
- Optional: the provenance result from `/source-provenance`, so that article-only material can be told apart from the primary's claims.

For a URL, get the text through the provenance fetcher, which honours `robots.txt` and keeps the full text in a local cache:

```bash
python3 skills/source-provenance/scripts/resolve_provenance.py text <url>
```

It prints the path to a local text file. Read that file. If the fetch fails, ask the user to paste the text.

## Output

A claim table, and a short note on what was deliberately left out.

```markdown
**Document:** <title> (<organisation>, <date>)
**URL:** <url>
**Claims extracted:** 8

| ID | Claim | Type | Anchor (verbatim) | Location |
|---|---|---|---|---|
| C01 | ... | observation | "..." | paragraph 3 |

**Not extracted:** background on the actor's 2023 activity (restated from earlier
reporting, not load-bearing); product recommendations; mitigation guidance.
```

And the same as JSON, matching the `claim_id`, `claim`, `claim_type` and `anchor` fields of the evidence item schema in `/quality-of-information-check`:

```json
{
  "document": {"url": "https://...", "title": "...", "org": "...", "date_published": "2026-09-25"},
  "claims": [
    {
      "claim_id": "C01",
      "claim": "The actor used a WAF bypass to reach exposed PeopleSoft servers.",
      "claim_type": "observation",
      "anchor": {
        "document_url": "https://...",
        "sentence": "verbatim sentence from the document",
        "location": "paragraph 3"
      },
      "date_observed": "2026-09-18",
      "flags": []
    }
  ],
  "not_extracted": ["..."]
}
```

`date_observed` is when the activity happened, if the document says. Otherwise `"unknown"`. It is not the publication date.

## Procedure

### 1. Read the document once

Identify the bottom-line statements and the facts they rest on. Do not start writing claims until you have read to the end: the caveats are often in the last section.

### 2. Write each claim

For each candidate:

1. Rewrite it as one atomic sentence. One subject, one assertion, no compound "and".
2. Tag the type (rules below).
3. Copy the anchor sentence or sentences verbatim. Copy, do not retype from memory. Every character must be findable in the source.
4. Record the location: paragraph number or the heading it sits under.

### 3. Type rules

| Type | It is | Examples |
|---|---|---|
| `observation` | Something seen or measured | A hash, an IP address, a technique executed, the date of activity, a count from telemetry |
| `attribution` | Linking activity to an actor, a country or a campaign | "We track this as UNC1234", "linked to the MSS" |
| `assessment` | A judgement about intent, capability, future behaviour or significance | "The group is likely to expand to OT targets" |
| `actor_claim` | A statement that originates with the threat actor | Leak-site posting, ransom note, forum post, statement to a journalist |
| `victim_disclosure` | A statement from the affected organisation, or its regulatory filing | 8-K, breach notification letter, press statement |

When a claim could be two types, pick by asking what would have to be true for the source to know it:

- If the source would have to have **seen** it: `observation`.
- If the source would have to have **reasoned** to it: `attribution` or `assessment`.
- If the source is **repeating what the actor or victim said**: `actor_claim` or `victim_disclosure`, whoever is relaying it.

The boundary cases are worked through in [`references/claim-typing-guide.md`](references/claim-typing-guide.md).

### 4. Preserve the hedge

Where the document hedges, the hedge is part of the claim.

| Source says | Claim reads | Not |
|---|---|---|
| "We assess with moderate confidence that the activity is linked to APT41" | "Vendor assesses with moderate confidence that the activity is linked to APT41." | "The activity is linked to APT41." |
| "overlaps with infrastructure previously used by" | "The infrastructure overlaps with infrastructure previously used by X." | "X is responsible." |
| "the group claims to have stolen 400GB" | "The actor claims to have taken 400GB of data." | "400GB of data was stolen." |

Stripping a hedge is the most damaging extraction error. It is how "possibly linked to" becomes "attributed to".

### 5. Do not over-split

- Merge claims that would always be graded together. Twelve hashes from one telemetry set are one observation claim with a list, not twelve claims.
- Skip background and context restated from earlier reporting, unless the document's conclusion depends on it.
- Skip marketing, product descriptions and generic mitigation advice.

Target five to twelve claims for a primary document. Fewer is fine for a short advisory. If you have more than twelve, you are probably splitting things that belong together. If the user asked for a specific focus or an exhaustive extraction, the range does not apply; say so in the output.

### 6. Output the table and stop

Grading is not this skill's job. Do not add grades or ratings of any kind, do not comment on how far a source can be trusted, do not say which claims are convincing.

## Articles: material that is not in the primary

When the input is a press article about a primary, extract from the primary first. Then look at what the article adds. Article-only material is kept and classified, not discarded:

| What the article contains | How it is handled |
|---|---|
| **An attributed quote** from a named person at a primary organisation ("a Mandiant analyst told us") | A claim of that organisation. `primary_source.access` will be `statement`, with a one-hop chain through the article. A vendor employee quoted in an article is the vendor speaking, never an independent researcher. |
| **A reference to another primary** ("CISA separately warned that...") | Not a claim of this chain. Flag it for a second provenance chain via `/source-provenance`. |
| **An unattributed assertion by the journalist** ("the group has been increasingly active") | Kept, with flag `press_originated`. It will be graded access level untraced, claim support tentative at best, and excluded from load-bearing status in `/ach` unless the user promotes it. |
| **A restatement of the primary's claim with changed strength** ("attributed to" where the primary said "possibly linked to") | Not a new claim. Record it against the chain hop as a fidelity note for `/quality-of-information-check`. |

The five-to-twelve target applies to the primary. Interview claims from the article are additional.

## What you may not do

- Extract a claim without an anchor.
- Paraphrase the anchor. It is verbatim or it is not an anchor.
- Supply a claim from your own knowledge of the incident. If it is not in the document, it is not a claim of the document.
- Upgrade or drop the source's hedging.
- Grade.

## Quality checks

`/quality-control` enforces these, and `validate_evidence.py` in `/quality-of-information-check` checks the mechanical ones:

- Every claim has an anchor.
- The anchor text is present verbatim in the source.
- No claim contains two assertions.
- The claim count is within five to twelve for a primary, unless the user asked otherwise.
- The type is one of the five values.

## References

- [`references/claim-typing-guide.md`](references/claim-typing-guide.md): worked examples for each type, the boundary cases, and vendor hedging language.
- [`references/worked-examples.md`](references/worked-examples.md): two full extractions, one from a vendor report and one from a press article with added material.

## Related skills

- `/source-provenance`: resolves where the document came from.
- `/quality-of-information-check`: grades the claims.
- `/ach`: takes graded claims as evidence.
- `/key-assumptions-check`: looks for assessment-type claims being treated as observations.
