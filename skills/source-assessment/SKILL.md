---
name: source-assessment
description: Use when rating a source with the NATO Admiralty Scale, the user asks "is this reliable?" / "rate this source", or the tradecraft pipeline calls for source assessment before publishing. Reliability A-F, credibility 1-6.
user-invocable: true
metadata:
  version: 1.1.0
---

# Source & Information Assessment — NATO Admiralty Scale

Every piece of intelligence entering this platform MUST be assessed using the Admiralty Scale. This is non-negotiable. Tag every item with a two-character code (e.g., B2).

## Scope of This Skill

This skill is the reference for the Admiralty scale itself: what the letters and digits mean and how to apply them to a single item, such as a lookup result, a feed entry or a tip.

Documents, articles and reports are graded per claim by `/quality-of-information-check`, using its fixed rubric (`references/grading-rubric.md` in that skill). It resolves the article to its originating source first, then grades each claim on the chain it arrived through. One report usually contains claims of different standing, so one grade for the whole report is wrong.

The pack does not store reliability opinions about named organisations. Where the guides and examples below name a vendor or agency, they illustrate a kind of access and track record. They are not standing grades for that organisation. The same organisation can publish an A2 observation and a C3 attribution in one report.

## Source Reliability

How trustworthy is the **source** based on its track record?

| Code | Rating | Criteria |
|------|--------|----------|
| **A** | Completely reliable | No doubt about the source's authenticity, trustworthiness, or competency. History of complete reliability. |
| **B** | Usually reliable | Minor doubt. Source has been reliable in most instances. |
| **C** | Fairly reliable | Doubt about reliability. Source has provided valid information in the past but not consistently. |
| **D** | Not usually reliable | Significant doubt. Source has been unreliable in the past. |
| **E** | Unreliable | Source has a track record of being unreliable, or the information is obtained under duress/deception. |
| **F** | Reliability cannot be judged | No basis for evaluating the source's reliability. New or unknown source. |

### Source Reliability Decision Guide

Judge the source on how it knows and how it has performed, not on its name.

- **A**: Direct access to what it reports (own telemetry, an incident response engagement, forensic evidence from your own systems, a victim's own regulatory disclosure) and no known retractions on this kind of claim
- **B**: Established source reporting from indirect access, such as sample analysis or partner data; well-known researcher with a history of published work; vetted sharing community relaying member reporting
- **C**: Access not disclosed; reporting that mixes own findings with aggregation; community feeds and open-source tools with mixed accuracy; advisory that aggregates others' reporting without adding evidence
- **D**: No originating source can be located; unverified forum posts and anonymous tips; source that has been wrong before
- **E**: Documented history of inaccurate, inflated or fabricated claims
- **F**: No basis to judge: first-time sources, automated feeds without historical accuracy data, newly discovered paste sites, a threat actor's own statements

## Information Credibility

How likely is the **information itself** to be accurate, regardless of source?

| Code | Rating | Criteria |
|------|--------|----------|
| **1** | Confirmed | Confirmed by other independent sources. Logical, consistent with other information on the subject. |
| **2** | Probably true | Not confirmed, but logical and consistent with other information. |
| **3** | Possibly true | Not confirmed. Reasonably logical but not fully consistent with other information. |
| **4** | Doubtful | Not confirmed. Possible but not logical. No other information on the subject. |
| **5** | Improbable | Not confirmed. Not logical. Contradicted by other information on the subject. |
| **6** | Truth cannot be judged | No basis for evaluating the information's veracity. |

### Information Credibility Decision Guide

- **1**: Corroborated by 2+ independent sources; matches observed technical evidence; confirmed by forensic analysis
- **2**: From a reliable source; logically consistent with known threat landscape; partially corroborated
- **3**: Plausible but from a single source; consistent with general trends but not specifically corroborated
- **4**: Unconfirmed claim; contradicts some known information; possible but requires further investigation
- **5**: Contradicts well-established intelligence; logically inconsistent; likely disinformation
- **6**: Cannot evaluate — insufficient context, entirely new domain, or conflicting assessment criteria

## Combined Rating Examples

These illustrate the reasoning. They are not standing grades for the organisations named.

| Rating | Example |
|--------|---------|
| **A1** | Microsoft publishes CVE details with MSRC forensic analysis, confirmed by CISA KEV listing |
| **B2** | CrowdStrike reports new APT campaign TTPs; consistent with own telemetry but not independently confirmed |
| **C3** | Security blogger reports new malware variant with partial technical analysis; plausible but unverified |
| **D4** | Anonymous Telegram channel claims zero-day in popular software; no technical details provided |
| **F6** | First-time automated feed delivers IOCs with no historical accuracy baseline |

## How to Apply

1. **At collection time**: Tag every piece of incoming intelligence with its Admiralty rating
2. **In analysis**: Weight evidence by reliability — A1 evidence outweighs D4 evidence
3. **In products**: Include the rating in the Sources & References section
4. **When ratings change**: If new information changes the credibility assessment, update and log the change

## Common Mistakes

- Confusing source reliability with information credibility (a reliable source can relay inaccurate information)
- Rating all vendor reports as A1 (vendors can have biases and errors)
- Grading the outlet instead of the chain (a news article relaying a vendor report is graded on the vendor's access and wording, plus how faithfully the outlet transmitted it; five outlets covering one report are one source)
- Not reassessing ratings when new corroborating or contradicting information emerges
- Omitting the rating entirely because "it's obvious" — always be explicit
