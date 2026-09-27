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
| Script discipline | `run_tests.py` | The script never judges fidelity. Undetermined fields are null with a reason. Access comes from the document's text. Navigation, sidebar and footer links are ignored. Output carries anchors, not full text |
| Limits | `run_tests.py` | More than 50 URLs or more than 2 hops is refused |
| Source table | `run_tests.py` | Longest prefix wins. Documentation hosts are not primaries. No duplicate domains. No reliability column and no rating words in notes |
| Grading caps | `qoi/valid-tier2.json`, `qoi/invalid-cases.json` | One complete valid run, then nineteen single-field mutations, each of which must be rejected under the expected rule. The weakest link must follow the footing bands. A first-party observation is accepted at A1 without a second primary, and the first-party label is refused on anything else |

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

Not yet done from the design's test plan: claim-extraction accuracy on five real vendor reports. Claim extraction is a model judgement, so testing it needs a model in the loop and a harness this repository does not have. The mechanical checks on its output (anchor present, anchor verbatim, type valid, count in range) are covered by the validator tests.

## Adding a case

1. Add the HTML page to `fixtures/` and its URL to `fixtures.json`. Invent the content.
2. Add the expected result to `expected-chains.json`.
3. Run the tests.

When a real page defeats the resolver, reproduce the structure that caused it in a synthetic fixture. That is how the sidebar-class and sponsored-link cases got here.
