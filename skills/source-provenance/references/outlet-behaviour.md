# How outlets cite

Informational. The script resolves every page the same way, whatever the outlet. This file explains the patterns you will see in its output, so an unresolved result is read correctly.

It describes citation habits. It does not rate outlets, and an outlet's habits say nothing about whether a given claim is true.

## Patterns observed

| Outlet tier | Typical citation habit | What the script returns |
|---|---|---|
| The Hacker News, BleepingComputer | Link the primary, usually within the first three or four paragraphs | Usually `resolved`, one hop |
| SecurityWeek, The Record | Usually link the primary when there is a document. Much of their output is original reporting from statements, where there is no document to link | `resolved` for report coverage. `unresolved` or `named_not_linked` for statement-based stories |
| GBHackers, Cyber Security News, Cyber Press | Often link another news article, or nothing. Frequently name the vendor without linking | `resolved` at two hops when the linked article links the primary. Otherwise `unresolved` |
| Wire services and national press | Original reporting with named and unnamed sources. Rarely link documents. Often block automated fetching | `unresolved`, or `blocked_by_robots` |
| Aggregators and newsletters | Link the outlet they summarise | Depends on the hop limit |

## Snapshot, 27 September 2026

The script was run on 30 URLs taken from the outlets' feeds on that date, plus three primaries given directly. The list and the expectations are in `tests/provenance/`.

| Source | Resolved |
|---|---|
| The Hacker News | 5 of 6 |
| BleepingComputer | 3 of 6 |
| GBHackers | 2 of 6 |
| SecurityWeek | 2 of 5 |
| The Record | 0 of 4 |
| Primary documents given directly (CISA, Microsoft, Google) | 3 of 3 |
| **Total** | **15 of 30** |

Reading the unresolved half:

- **The source was a social post.** Two exchange-theft stories rested on posts on X by the affected company. The script records them under `unclassified_candidates` with type `social`. The account holder is the source, and the script does not verify who holds an account.
- **The source was a statement, not a document.** "OpenAI said", "CISA warned", with no link. Returned as `named_not_linked`.
- **The source was not in the table.** Smaller vendors and independent researchers. Returned under `unclassified_candidates`. Adding a row to `source-types.md` resolves these.
- **The only primary-type links were background.** A story about a new incident linking press releases from 2021. Returned under `background_references`.
- **The article named no source and linked none.**

Every one of those is a finding about the article. An unresolved chain is capped at reliability D and credibility 3 by the grading rubric. It is not repaired by the model recalling who probably published the original.

## Why a resolved chain can still mislead

- **The linked document is older than the story.** An article about a new vulnerability links the vendor's write-up of the previous one. The script rejects documents published more than 60 days before the article, but a document from five weeks earlier passes. Compare the claims with the primary's text.
- **The article has several primaries.** A product vendor's advisory, a security vendor's exploitation report and a government alert may all be linked. Each is the primary for its own claims.
- **The primary itself aggregates.** Government advisories often restate vendor reporting. The script finds the advisory. Whether it adds independent evidence is a judgement made during grading.
