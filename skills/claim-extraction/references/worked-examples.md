# Worked examples

Two extractions. The organisations, actors, indicators and documents are invented for illustration. IP addresses are from documentation ranges.

## Example 1: a vendor report

**Input.** A vendor research post, "Crimson Heron targets regional water utilities", published by Northwind Security on 18 September 2026.

Relevant text, by paragraph:

> (2) During three incident response engagements between June and August 2026, we identified a previously undocumented backdoor we call Embers.
>
> (3) In all three cases, initial access was obtained through exploitation of CVE-2026-0001 in an internet-facing remote access gateway.
>
> (5) Embers communicates with its command and control server over HTTPS, using a hard-coded list that in our samples included 203.0.113.42 and 198.51.100.17.
>
> (8) We assess with moderate confidence that this activity was conducted by Crimson Heron. The assessment rests on overlaps in infrastructure registration patterns and on reuse of a custom credential-dumping tool previously documented in Crimson Heron intrusions.
>
> (9) Crimson Heron has been linked by several governments to a state intelligence service.
>
> (11) We did not observe data destruction or manipulation of control systems. The intruders collected network diagrams and credentials.
>
> (12) We believe the objective is pre-positioning, and that the group is likely to target additional utilities in the region over the coming months.
>
> (14) Customers of Northwind Managed Detection are protected against this threat.

**Output.**

**Document:** Crimson Heron targets regional water utilities (Northwind Security, 2026-09-18)
**Claims extracted:** 7

| ID | Claim | Type | Anchor (verbatim) | Location |
|---|---|---|---|---|
| C01 | The vendor identified a previously undocumented backdoor, Embers, in three incident response engagements between June and August 2026. | observation | "During three incident response engagements between June and August 2026, we identified a previously undocumented backdoor we call Embers." | paragraph 2 |
| C02 | In all three cases initial access was through exploitation of CVE-2026-0001 in an internet-facing remote access gateway. | observation | "In all three cases, initial access was obtained through exploitation of CVE-2026-0001 in an internet-facing remote access gateway." | paragraph 3 |
| C03 | Embers uses HTTPS command and control with a hard-coded server list that included 203.0.113.42 and 198.51.100.17 in the vendor's samples. | observation | "Embers communicates with its command and control server over HTTPS, using a hard-coded list that in our samples included 203.0.113.42 and 198.51.100.17." | paragraph 5 |
| C04 | Vendor assesses with moderate confidence that the activity was conducted by Crimson Heron. | attribution | "We assess with moderate confidence that this activity was conducted by Crimson Heron." | paragraph 8 |
| C05 | The intruders collected network diagrams and credentials, and the vendor did not observe data destruction or manipulation of control systems. | observation | "We did not observe data destruction or manipulation of control systems. The intruders collected network diagrams and credentials." | paragraph 11 |
| C06 | Vendor believes the objective is pre-positioning. | assessment | "We believe the objective is pre-positioning, and that the group is likely to target additional utilities in the region over the coming months." | paragraph 12 |
| C07 | Vendor judges the group is likely to target additional utilities in the region over the coming months. | assessment | "We believe the objective is pre-positioning, and that the group is likely to target additional utilities in the region over the coming months." | paragraph 12 |

**Not extracted:**

- Paragraph 9, the link between Crimson Heron and a state intelligence service. The vendor is relaying other organisations' attribution. Flagged for a separate provenance chain if the user's question depends on state sponsorship.
- Paragraph 14, product coverage statement. Marketing.
- The basis for the attribution (infrastructure overlap, tool reuse) is kept with C04 as supporting detail and not split out, because it would always be graded with C04.

**Notes on the choices.**

- C01 to C03 keep their scope: "in three engagements", "in the vendor's samples". The report does not claim these are the only cases.
- C05 merges two sentences. Both come from the same engagements and would receive the same grade. "Did not observe" is kept exactly: it is a statement about what the vendor saw, not a statement that nothing was destroyed.
- C06 and C07 share an anchor sentence but are separate claims. One is about the present objective, the other about future behaviour, and a hypothesis could be consistent with one and inconsistent with the other.
- `date_observed` for C01, C02 and C05 is "2026-06 to 2026-08". For C03 it is unknown.

## Example 2: a press article about that report

**Input.** A news article, "State hackers burrow into water utilities", published 19 September 2026, which links the Northwind report in its second paragraph.

Relevant text:

> (1) State-sponsored hackers have broken into water utilities across the region and planted a new backdoor, security firm Northwind said on Thursday.
>
> (3) The campaign has been attributed to Crimson Heron, a group tied to a foreign intelligence service.
>
> (4) "What worries us is how quiet they were. Two of the three utilities had no idea until we told them," said Dana Reyes, head of incident response at Northwind.
>
> (6) The national cyber agency said in a separate advisory that it had seen scanning for the same vulnerability against government networks.
>
> (7) Attacks on water infrastructure have been rising sharply this year.

**Step 1.** The primary's claims are C01 to C07 above. They are extracted from the primary, not from the article.

**Step 2.** What the article adds:

| ID | Claim | Type | Anchor (verbatim) | Location | Handling |
|---|---|---|---|---|---|
| C08 | Northwind's head of incident response states that two of the three utilities were unaware of the intrusion until the vendor told them. | observation | "\"What worries us is how quiet they were. Two of the three utilities had no idea until we told them,\" said Dana Reyes, head of incident response at Northwind." | article, paragraph 4 | Attributed quote. A claim of Northwind, access `statement`, one-hop chain through the article |
| C09 | Attacks on water infrastructure have been rising sharply this year. | assessment | "Attacks on water infrastructure have been rising sharply this year." | article, paragraph 7 | Unattributed journalist assertion. Flag `press_originated` |

**Not extracted as claims:**

- Paragraph 3, "has been attributed to Crimson Heron". This restates C04 with the hedge removed. The primary said "we assess with moderate confidence". Recorded as a fidelity note on the article's hop: caveat dropped.
- Paragraph 1, "State-sponsored hackers have broken into...". Restates C01 and C04 together, again without the hedge, and presents the state sponsorship the primary only relayed as settled. Same fidelity note.
- Paragraph 1, "across the region". The primary reported three engagements. Recorded as a fidelity note: scope widened.
- Paragraph 6, the national cyber agency's advisory. A different primary. Flagged for a second provenance chain.

**What this gives the grader.** Seven claims from the primary, one interview claim that belongs to the vendor, one press-originated assertion, three fidelity notes against the article, and one pointer to a second source that may or may not turn out to be independent.
