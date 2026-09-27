# Worked examples

Three runs, one per tier. The vendor, actor, victims, indicators and documents are invented. Outlets are described by their citation habit, not named. The first example continues the extraction in `/claim-extraction`'s worked examples, and its full JSON is kept as a test fixture in `tests/provenance/qoi/`.

## Example 1: an article that resolves to a vendor report (Tier 2)

**Input.** The URL of a press article, "State hackers burrow into water utilities", from an outlet that links its primary in the second paragraph. No Liberty91 key. Question served: *who is behind the intrusions at regional water utilities?*

**Step 1, provenance.** `resolve_provenance.py` returns `status: resolved`, a two-hop chain, and the primary: Northwind Security, "Crimson Heron targets regional water utilities", published 2026-09-18. Access evidence: "During three incident response engagements..." so `access: ir_engagement`. Confidence evidence: "We assess with moderate confidence that this activity was conducted by Crimson Heron."

**Step 2, claims.** Seven from the primary (C01 to C07), one attributed quote (C08), one press-originated assertion (C09).

**Step 3, fidelity.** The article says the campaign "has been attributed to Crimson Heron". The primary says "we assess with moderate confidence". Hop fidelity: `caveats_dropped`. The article says "across the region"; the primary reports three engagements. Same hop, noted as scope widened.

**Step 4, corroboration.** Default 1, unchecked. The user accepts the offer to check the two C2 addresses in C03. `/lookup-otx` returns one pulse that cites the Northwind report: same source, not counted. `/lookup-virustotal` shows detections but no independent reporting organisation. Result: still 1, `basis: lookups`, for C03. The article mentions a national cyber agency advisory; that is a second chain, not yet run. No alias file and no key, so `alias_source: none` and the Crimson Heron name is not matched against other vendors' names.

**Steps 5 to 8.**

| ID | Claim | Type | Access | Grade | Corrob. | Flags |
|---|---|---|---|---|---|---|
| C04 | Vendor assesses with moderate confidence that the activity was conducted by Crimson Heron. | attribution | ir_engagement | **A3** | 1 (unchecked) | single_source, caveats_dropped_in_chain, commercial_interest |
| C02 | In all three cases initial access was through exploitation of CVE-2026-0001. | observation | ir_engagement | **A2** | 1 (unchecked) | single_source |
| C01 | The vendor identified a previously undocumented backdoor, Embers, in three engagements. | observation | ir_engagement | **A2** | 1 (unchecked) | single_source |
| C03 | Embers uses HTTPS C2 with a hard-coded list including 203.0.113.42 and 198.51.100.17. | observation | ir_engagement | **A2** | 1 (lookups) | single_source |
| C05 | The intruders collected network diagrams and credentials; no destruction was observed. | observation | ir_engagement | **A2** | 1 (unchecked) | single_source |
| C06 | Vendor believes the objective is pre-positioning. | assessment | ir_engagement | **A3** | 1 (unchecked) | single_source |
| C07 | Vendor judges the group is likely to target additional utilities. | assessment | ir_engagement | **A3** | 1 (unchecked) | single_source |
| C08 | Two of the three utilities were unaware until the vendor told them. | observation | statement | **B2** | 1 (unchecked) | single_source |
| C09 | Attacks on water infrastructure have been rising sharply this year. | assessment | undisclosed | **D3** | 1 (unchecked) | single_source, press_originated, unresolved_provenance |

Rationale, for the load-bearing claim:

> **C04, A3.** Northwind states its findings come from three incident response engagements, which supports reliability A. The attribution is an analytical judgement stated with moderate confidence, from a single primary; R4 caps attribution at credibility 2 without a second independent primary, and the vendor's own moderate confidence places it at 3. The article dropped the confidence statement; graded on the primary's wording (R7).

**Aggregate.** Nine claims. One independent primary. Grade range A2 to D3. Summary line: "core facts A2, attribution A3 on a single primary, trend statement press-originated". Weakest link: C04.

**Gaps.** No independent confirmation of the attribution. The agency advisory has not been traced. Actor names could not be matched across vendors: provide `aliases.yml` or a Liberty91 key. The report does not name the utilities, so victim disclosures cannot be looked for.

**Deception screen.** MOM: attribution rests on infrastructure patterns and tool reuse, both reproducible by another actor. POP: not established. MOSES: evidence comes from the vendor's own engagements, low manipulability. EVE: consistent; basis for attribution is stated. No flags raised.

**What this tells the reader.** The facts of the intrusions are well founded on one source. Who did it is a moderate-confidence judgement by that same source, which the press reported as settled.

## Example 2: an article that does not resolve (Tier 2)

**Input.** The URL of an article, "New stealer hits finance teams", from an outlet that commonly links other news articles or nothing.

**Step 1, provenance.** `resolve_provenance.py` exits 2. `status: unresolved`. The article's only links are to the outlet's own earlier stories. `unattributed_sourcing` contains "Researchers say the malware is sold on underground forums." `unclassified_candidates` contains one link to a host that is not in `source-types.md`, in paragraph 6.

Reported as:

> This article could not be traced to an originating source. It links no vendor, government, victim or actor document. It cites one site the script does not classify (listed below). Provenance is unresolved.

The unclassified host is shown to the user. It is not classified from memory. If the user knows the organisation, adding a row to `source-types.md` and rerunning resolves the chain.

**Step 2, claims.** Six, all extracted from the article because there is no primary.

**Steps 3 to 5.** Fidelity is `unresolved` on the single hop. Corroboration 1, unchecked. R1 applies to every claim.

| ID | Claim | Type | Grade | Flags |
|---|---|---|---|---|
| C01 | The stealer is delivered through invoice-themed email attachments. | observation | **D3** | single_source, unresolved_provenance |
| C02 | It collects browser credentials and session cookies. | observation | **D3** | single_source, unresolved_provenance |
| C03 | The sample's SHA-256 is given in the article. | observation | **D3** | single_source, unresolved_provenance |
| C04 | The malware is sold on underground forums. | observation | **D3** | single_source, unresolved_provenance |
| C05 | The developer is likely Russian-speaking. | attribution | **D3** | single_source, unresolved_provenance |
| C06 | Finance teams are being deliberately targeted. | assessment | **D3** | single_source, unresolved_provenance |

**Next steps.** C03 contains a hash. `/lookup-virustotal` and `/lookup-reversinglabs` can establish whether the sample exists and what it does, from data. If a lookup shows an organisation reporting the same sample from its own analysis, that organisation becomes a resolved primary for C02 and C03, and those two claims are regraded. C05 and C06 stay where they are.

**What this tells the reader.** Nothing in this article can carry an assessment yet. One claim is checkable within minutes.

## Example 3: a Liberty91 event with three independent primaries (Tier 1)

This example shows the shape of a Tier 1 run. It applies when `/lookup-liberty91` returns provenance fields for the event. If the response does not carry them, the run falls back to Tier 2 and is labelled `script-resolved`.

**Input.** A Liberty91 event ID. Question served: *was CVE-2026-0002 exploited before the patch was released?*

**Step 1, provenance.** `/lookup-liberty91` returns the event with 14 secondary reports and `independent_primaries: 3`:

| Primary | Type | Access | Published | Stated confidence |
|---|---|---|---|---|
| Northwind Security | vendor | telemetry | 2026-09-10 | not stated |
| A national CERT | government | ir_engagement | 2026-09-12 | not stated |
| Harbour Freight Lines, regulatory filing | victim | victim_statement | 2026-09-15 | not stated |

Fourteen articles, three sources.

**Step 2, claims.** Extracted from each primary. The same assertion made by more than one primary is one claim with several sources.

**Step 4, corroboration.** Read from the platform, `basis: platform`. The platform matched the three on the CVE identifier and on two shared indicators. Names were resolved through the Threat Library, `alias_source: liberty91`.

**Step 5, grading.**

| ID | Claim | Type | Grade | Corrob. | Flags |
|---|---|---|---|---|---|
| C01 | CVE-2026-0002 was exploited against internet-facing gateways from 2 September 2026, eight days before the patch. | observation | **A1** | 3 (platform) | |
| C02 | Harbour Freight Lines states it detected unauthorised access on 4 September 2026. | victim_disclosure | **A2** | 1 (platform) | single_source |
| C03 | The national CERT responded to intrusions at two government bodies using the same exploit. | observation | **A2** | 1 (platform) | single_source |
| C04 | Vendor attributes the exploitation to Crimson Heron. | attribution | **B2** | 1 (platform) | single_source |
| C05 | The actor claims on its leak site to have taken 1.2TB from Harbour Freight Lines. | actor_claim | **F6** | 1 (platform) | single_source, actor_sourced, deception_indicators_present |

> **C01, A1.** Three primaries with separate access report exploitation before the patch date: vendor telemetry, a government incident response engagement, and the victim's own filing. Corroboration is platform-resolved on the CVE and two shared indicators.

> **C04, B2.** Attribution by one primary only; the CERT and the victim do not name an actor. R4 caps credibility at 2. Reliability moved from A to B by the platform's track record for this organisation's attribution claims (`track_record_applied: boundary_down`).

> **C05, F6.** The actor's own figure. No primary corroborates the volume; the victim's filing confirms access and says nothing about data taken. R2 applies.

**Aggregate.** Five claims. Three independent primaries. Grade range A1 to F6. Summary line: "pre-patch exploitation A1 on three primaries, attribution B2 single-source, volume actor-claimed". Weakest link for the question asked: C01 is the only load-bearing claim, at A1.

**What this tells the reader.** The answer to the question is yes, on the strongest footing available. Attribution and the scale of the theft are separate matters with much weaker support, and the grade on the first does not transfer to them.
