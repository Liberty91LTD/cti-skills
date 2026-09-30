# Provenance and grading tests

How we know `/source-provenance` and `/quality-of-information-check` do what they say.

```bash
python3 tests/provenance/run_tests.py
```

Offline, standard library only, a few seconds. CI runs it on every push and pull request.

## What is tested

| Area | File | Checks |
|---|---|---|
| Chain resolution | `expected-chains.json`, `fixtures/` | Ten scenarios: one hop, two hops, no source, outlets citing each other, source named but not linked, sponsored link, background link, unreadable primary, primary given directly, several primaries |
| Script discipline | `run_tests.py` | The script never judges fidelity. Undetermined fields are null with a reason. Access comes from the document's text. Navigation, sidebar and footer links are ignored. A body split across sibling sections is kept whole. Table rows are kept. A primary that relays another organisation's research is reported. Access phrases after a negation are ignored. Output carries anchors, not full text |
| Limits | `run_tests.py` | More than 50 URLs or more than 2 hops is refused |
| Source table | `run_tests.py` | Longest prefix wins. Documentation hosts are not primaries. No duplicate domains. No reliability column and no rating words in notes |
| Grading caps | `qoi/valid-tier2.json`, `qoi/invalid-cases.json` | One complete valid run, then twenty-two single-field mutations, each of which must be rejected under the expected rule. The weakest link must follow the footing bands. A first-party observation is accepted as direct and established without a second primary, and the first-party label is refused on anything else |

## Fixtures

`fixtures/` holds synthetic HTML pages. The content is invented. They reproduce page structures and citation patterns seen on real sites: a content wrapper with a class name containing "sidebar", a sponsored link with tracking parameters, an undated vendor bulletin. No third-party article text is stored in this repository.

`fixtures.json` maps URLs to those files. When the resolver is given `--fixtures`, it does not touch the network.

`qoi/primary.txt` and `qoi/article.txt` are the invented report and article from the worked examples. `qoi/valid-tier2.json` is the full output of worked example 1.

## Live run

`live-urls.tsv` records a run against 30 real URLs on 27 September 2026, with the result for each.

| Source | Resolved |
|---|---|
| The Hacker News | 5 of 6 |
| BleepingComputer | 3 of 6 |
| GBHackers | 2 of 6 |
| SecurityWeek | 2 of 5 |
| The Record | 0 of 4 |
| Primary documents given directly | 3 of 3 |
| **Total** | **15 of 30** |

Of 61 fetches, 58 succeeded, 2 were blocked by `robots.txt` and 1 returned HTTP 401.

Half unresolved is the expected result, not a defect. The unresolved articles rested on social posts, on statements with no document, on sources not yet in `source-types.md`, or on nothing at all. Each of those is reported as a finding and capped by the grading rubric. See `skills/source-provenance/references/outlet-behaviour.md`.

## Claim extraction run

Claim extraction is a model judgement, so it cannot run in CI. It was tested by hand on 29 September 2026 on five vendor reports, found through the Liberty91 API and fetched with the resolver. Each report was extracted by a model instance given only the skill, checked by the validator, then reviewed claim by claim by a second model instance against the source text. The reviewer was a model, not a person. No report text is stored here.

| Report | Claims | Anchors verbatim | Pass all five review points |
|---|---|---|---|
| Microsoft, Storm-3168 (25 September 2026) | 12 | 12 | 12 |
| Google Threat Intelligence, ShinyHunters and Oracle PeopleSoft (September 2026) | 12 | 12 | 11 |
| Socket, MemTensor package compromise (September 2026) | 12 | 12 | 11 |
| CERT Polska, MikroTrick technical analysis (September 2026) | 12 | 12 | 11 |
| Sysdig, JADEPUFFER (1 July 2026) | 12 | 12 | 8 |
| **Total** | **60** | **60** | **53** |

The five review points: the anchor supports the claim, the type is right, the claim is atomic, the hedge is preserved, and the claim belongs to the party it is assigned to.

What failed, across seven claims:

- Five had an anchor that stopped short of the claim. The fact was in the report, in the next sentence or in the bullets under a lead-in sentence, and the anchor did not include it.
- One added a count the source did not give ("three vectors" for an open list).
- One changed a hedge ("essentially random" became "randomly generated").
- Two of the seven also joined two assertions in one claim.

No claim had the wrong type.

What the review found missing. Every extraction reached the twelve-claim ceiling and left findings out to stay under it. The omissions were mostly negative findings, scope statements and the observations that an extracted assessment rests on. Dense technical reports hold more than twelve gradeable claims.

A sixth document, a vendor blog relaying another organisation's research, was run as well. The extraction recognised the relay. The resolver did not: it classified the vendor blog as the primary. That is fixed: the resolver now reports `primary_relays` and the cited organisation. The validator rejected the extraction on claim count, because it counts only claims that are not `press_originated`. That is open.

## Adding a case

1. Add the HTML page to `fixtures/` and its URL to `fixtures.json`. Invent the content.
2. Add the expected result to `expected-chains.json`.
3. Run the tests.

When a real page defeats the resolver, reproduce the structure that caused it in a synthetic fixture. That is how the sidebar-class and sponsored-link cases got here.
