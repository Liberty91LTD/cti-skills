---
name: source-assessment
description: NATO Admiralty Scale for assessing source reliability and information credibility. Apply to every piece of collected intelligence.
user-invocable: true
metadata:
  version: 1.0.0
---

# Source & Information Assessment — NATO Admiralty Scale

Every piece of intelligence entering this platform MUST be assessed using the Admiralty Scale. This is non-negotiable. Tag every item with a two-character code (e.g., B2).

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

- **A**: National CERTs, established security vendors (Mandiant, CrowdStrike, Microsoft), peer-reviewed research, direct forensic evidence from your own systems
- **B**: Reputable threat intelligence providers, well-known security researchers, ISACs, FIRST members
- **C**: Community threat feeds, open-source intelligence tools with mixed accuracy, semi-verified social media accounts of known researchers
- **D**: Unverified forum posts, anonymous tips, single-source claims without corroboration
- **E**: Known disinformation actors, sources with demonstrated fabrication history
- **F**: First-time sources, automated feeds without historical accuracy data, newly discovered paste sites

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
- Not reassessing ratings when new corroborating or contradicting information emerges
- Omitting the rating entirely because "it's obvious" — always be explicit
