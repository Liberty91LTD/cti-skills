---
name: source-provenance
description: Use when you need to know where a piece of reporting actually came from — the user gives an article URL and asks "where does this come from?", "who is the original source?", "is this just a rewrite?", or another skill needs the provenance chain before grading or citing a report. Follows an article's links and named attributions back to the originating vendor, government, victim or actor document and returns the chain, the primary's stated access and confidence language, publication dates, and every hop it could not resolve. Deterministic — a script or the Liberty91 platform resolves the chain; the model does not reconstruct it from memory. Invoked by /quality-of-information-check, /threat-actor-profiling, /campaign-tracking and /intelligence-writing. Works on any URL with no API key.
user-invocable: true
metadata:
  version: 1.0.0
  tags: [tradecraft, provenance, sourcing, sat]
  tradecraft: true
---

# source-provenance

Most CTI reporting that reaches an analyst is derivative. An outlet rewrites another outlet, which summarised a vendor blog, which reported on the vendor's telemetry. Five outlets covering one vendor report look like five sources. They are one.

This skill resolves a URL to its originating source and returns the chain as data. It does not grade anything. Grading is `/quality-of-information-check`.

**Composition.** Invokes `/lookup-liberty91` when a key is configured. Invoked by `/quality-of-information-check`, `/claim-extraction` (for the fetcher), `/threat-actor-profiling`, `/campaign-tracking`, `/intelligence-writing` and `/cti-orchestrator`.

## The rule that matters

**The chain comes from data, never from recollection.** You may know that a story "was originally a Mandiant report". That knowledge does not go in the output. If the platform or the script did not resolve a hop, the hop is unresolved, and you say so.

## Inputs

- One or more URLs (up to 50 per run).
- Optional: a Liberty91 event ID, in which case platform data is returned instead of resolving.

Pasted text with no URL cannot be resolved by this skill. Say so and hand it to `/quality-of-information-check`, which treats it as Tier 3.

## Tiers

| Tier | When | Who resolves the chain | `provenance_basis` |
|---|---|---|---|
| 1 | `LIBERTY91_API_KEY` is set and the platform returns provenance fields for the event | Liberty91 ingestion pipeline, across the whole deduplicated event | `platform-resolved` |
| 2 | No key, or the platform has no provenance for this URL | `scripts/resolve_provenance.py`, for the single article given | `script-resolved` |
| 3 | The page cannot be fetched, or the input is pasted text | The model, from the text alone, every field marked unverified | `model-judged` |

Every output carries `provenance_basis` at the top. Downstream skills carry it through unchanged.

## Procedure

### 1. Try the platform

If `LIBERTY91_API_KEY` is set, ask `/lookup-liberty91` for the event that contains this URL and read its provenance fields (`primaries[]`, `independent_primaries`, `chains[]`, `most_recent_observation`, `superseded_by`). If they are present, return them with `provenance_basis: platform-resolved` and stop.

If the key is absent, the URL is not an ingested article, or the response carries no provenance fields, continue to step 2. Do not label anything `platform-resolved` unless the fields were in the response.

### 2. Run the script

```bash
python3 skills/source-provenance/scripts/resolve_provenance.py resolve <url> [<url> ...]
```

Standard library only, no install. Options:

| Option | Effect |
|---|---|
| `--max-hops 1` | Article to primary only. Default is 2 (article to article to primary), which is also the hard limit. |
| `--no-cache` | Do not read or write the local cache. |
| `--cache-dir DIR` | Default `~/.cache/cti-skills/provenance`, or `$CTI_SKILLS_CACHE`. |

Two helper commands:

```bash
# Classify URLs against the source-types table. No network.
python3 skills/source-provenance/scripts/resolve_provenance.py classify <url> [<url> ...]

# Extract an article's body text to the local cache and print the file path.
python3 skills/source-provenance/scripts/resolve_provenance.py text <url>
```

Exit codes: `0` every input resolved, `2` at least one did not, `3` refused (over 50 URLs or over 2 hops), `1` error.

### 3. Read the result

For each URL the script returns:

| Field | Meaning |
|---|---|
| `status` | `resolved` or `unresolved` |
| `chain[]` | Ordered hops, the outlet nearest the user first, the primary last. Each hop has `org`, `type`, `url`, `date_published`, `title`, and `anchor_in_previous_hop` (the sentence in which the previous hop cited this one). |
| `primary_source` | `org`, `type`, `title`, `date_published`, `url`, `access`, `access_evidence[]`, `stated_confidence`, `confidence_evidence[]`, `hedges[]`, `interest`, `resolution` |
| `other_primaries[]` | Other originating documents linked from the same article, read where possible. Their claims belong to them. |
| `background_references[]` | Primary-type links published well before the article, or whose date could not be checked and which sit deep in the text. Context, not origin. |
| `unclassified_candidates[]` | Links to hosts not in the table, and social posts. Not followed. |
| `attribution_sentences[]` | Sentences where the outlet says where its information came from, with organisations named and links found. |
| `unattributed_sourcing[]` | "Researchers say", "sources familiar with the matter". Findings, not gaps to fill. |
| `unresolved[]` | Every field the script could not determine, with the reason. |
| `summary` | One paragraph, generated from the fields above. |

`fidelity` is `null` on every resolved hop. Judging whether an outlet transmitted the primary faithfully is a model judgement and belongs to `/quality-of-information-check`.

`primary_source.resolution` is one of:

| Value | Meaning |
|---|---|
| `linked` | The document was linked, fetched and read. |
| `linked_not_read` | The document was linked but could not be fetched (robots, paywall, 4xx, PDF). The organisation is known; its access and confidence are not. |
| `named_not_linked` | The outlet names an organisation as its source but links no document. Status stays `unresolved`. |

### 4. Present the chain

Lead with `provenance_basis` and the one-paragraph summary. Then the chain, then what was not resolved. Use this shape:

```markdown
**Provenance basis:** script-resolved
**Assessed:** 2026-09-27

This GBHackers article traces to a document from Microsoft Threat Intelligence (vendor),
"Storm-3168: ...", published 2026-09-25. Its text indicates access by telemetry; no
confidence statement was found.

| Hop | Organisation | Type | Published | URL |
|---|---|---|---|---|
| 1 | GBHackers | press | 2026-09-26 | https://... |
| 2 (primary) | Microsoft Threat Intelligence | vendor | 2026-09-25 | https://... |

**Primary's stated access:** telemetry ("We observed ..." , paragraph 4)
**Primary's stated confidence:** not stated
**Other primaries linked:** none
**Not resolved:** date of the activity itself (recorded during claim extraction)
```

If any hop is unresolved, say so in plain words and do not guess. "This article names no source and links none" is a complete and useful answer.

### 5. Hand off

If the user wants to know how reliable the report is, or whether the outlet changed the primary's meaning, hand off to `/quality-of-information-check`. Do not judge fidelity or assign Admiralty grades here.

## What "resolved" does and does not mean

`resolved` means a document from an originating organisation was located and, in most cases, read. It does not mean every statement in the article comes from that document. Articles add quotes, background and the journalist's own framing. `/claim-extraction` separates those, and `/quality-of-information-check` compares each claim's wording against the primary.

Check these before relying on a resolved chain:

- **`date_check: not verified`** on the primary. The script could not compare publication dates, so the linked document may be background rather than the origin.
- **More than one primary.** A vendor's vulnerability advisory and a second vendor's exploitation report are both primaries, for different claims.
- **`access_evidence`.** Read the sentences. A vendor blog that quotes "CISA said it observed" has matched a telemetry phrase that describes someone else's access.

## Rules for what was not established

| Situation | What to output |
|---|---|
| No primary resolved | `provenance: unresolved`. State the reason the script gave. The grade will be capped downstream. |
| Organisation named, nothing linked | `named_not_linked`. Name the organisation, state that its document was not read. |
| Primary does not say how it knows | `access: undisclosed`. Never inferred from the organisation's reputation. |
| Primary states no confidence | `stated_confidence: "not stated"`. Never invented, never paraphrased. |
| Host not in the table | `unknown`. Report it under unclassified candidates. Do not classify it from memory. Suggest adding a row. |
| Corroboration | Not assessed by this skill. One chain is one source. |

## Failure modes

| Failure | Handling |
|---|---|
| Paywalled or JavaScript-rendered page | Report the fetch failure. Offer the user the option to paste the text, which drops to Tier 3. |
| `robots.txt` disallows the page | Reported as `blocked_by_robots`. There is no override. Offer paste. |
| Outlets citing each other | The script detects the cycle and reports "circular press citations, no primary found". |
| Press release wire | Classified as vendor-authored. The issuing organisation is the source, not the wire. Access `undisclosed` unless the release states it. |
| PDF | Not parsed by the script. The hop is recorded as `linked_not_read`; route the document to a PDF reader and continue from the text. |
| Sponsored links in the article | Links carrying tracking parameters or pointing at product and sales pages are ignored. |
| More than 50 URLs | Refused. Bulk provenance is what the Liberty91 API is for; chains are resolved once at ingest. |

## Fetcher policy

Fixed. There are no flags to loosen it.

- User agent `cti-skills-provenance/2.0 (+https://github.com/Liberty91LTD/cti-skills)`.
- `robots.txt` honoured.
- One request in flight per host, two seconds between requests to the same host, four hosts in flight.
- On 429 or 503: honour `Retry-After`, otherwise back off from 10 seconds, three attempts, then skip the host for the run.
- Local cache keyed by URL, revalidated with `ETag` and `Last-Modified`. Seven days for press, thirty for primaries. Never uploaded, never committed.
- 10 second connect timeout, 20 second read timeout, 5 MB size limit.
- Output contains extracted fields and anchor sentences only. Full text stays in the local cache.

## References

- [`references/source-types.md`](references/source-types.md): the classification table the script reads. Type, access profile and interest. No reliability column.
- [`references/attribution-phrases.md`](references/attribution-phrases.md): the attribution, confidence, hedging and access patterns, with false-positive notes.
- [`references/outlet-behaviour.md`](references/outlet-behaviour.md): how common outlets cite, and what the script makes of each pattern.

## Related skills

- `/quality-of-information-check`: grades the claims once the chain is known.
- `/claim-extraction`: splits the primary into typed, anchored claims.
- `/lookup-liberty91`: platform-resolved provenance across a whole deduplicated event.
- `/source-assessment`: the Admiralty scale reference.
