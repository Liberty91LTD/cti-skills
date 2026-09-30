---
name: threat-assessment
description: Structured threat assessment methodology. Intent + Capability + Opportunity = Threat Level. Use when formally evaluating a threat. Prefers graded evidence items from /quality-of-information-check and runs that skill first when handed raw URLs or text. Confidence is capped by the weakest load-bearing claim, and at Moderate when the evidence is ungraded.
user-invocable: true
metadata:
  version: 2.0.0
---

# Threat Assessment Methodology

A threat assessment evaluates the threat posed by a specific actor or scenario to a specific target. It combines Intent, Capability, and Opportunity into an overall Threat Level.

## Formula
**Threat = Intent + Capability + Opportunity**

All three must be present for a credible threat. A highly capable actor with no intent poses minimal threat. A motivated actor with no capability poses minimal threat.

## Evidence: Graded Preferred, Ungraded Allowed

An assessment is best built on graded evidence items, one per claim, as produced by `/quality-of-information-check` (the QoI JSON or its claim table). The schema is in `skills/quality-of-information-check/references/evidence-item-schema.md`. Grading is the default. It is not a condition for writing the assessment.

- Handed a QoI output: proceed.
- Handed raw URLs, articles, vendor reports or pasted text: invoke `/quality-of-information-check` first, passing the assessment question so it can mark which claims are load-bearing. Build the assessment from its output. This is the default and needs no permission.
- Handed a mix: grade what can be graded and carry the rest as ungraded.
- The user asks to skip grading, or `/quality-of-information-check` cannot be run: write the assessment in ungraded mode. Say once what that costs, then proceed. Do not ask again.

### Ungraded mode

Any assessment that uses at least one ungraded item from reporting follows these rules:

- **Label it.** The header carries `Evidence basis: ungraded` when nothing is graded, `mixed` when some items are, and `graded` when all are.
- **Do not invent grades.** An ungraded item is listed in Sources as `ungraded`. Where the analyst supplied a rating through `/source-assessment`, show it as `Admiralty B2 (analyst)`. An Admiralty rating applies to a lookup result or a single item, the evidence grade applies to a claim from a document, and neither is converted into the other.
- **Confidence is capped at Moderate** when any item the conclusion depends on is ungraded. High is reserved for conclusions whose load-bearing claims are all graded and independently confirmed. Weak logic or a single unverified source lowers it further, as always.
- **Name the ungraded items** in the confidence rationale, and say that running `/quality-of-information-check` on them may raise or lower the level:

> "Confidence: moderate, capped. The conclusion depends on two vendor reports that were not graded (U01, U02). Running /quality-of-information-check on them would establish whether they rest on one primary or two."

Three kinds of input are not reports. They are handled differently from each other:

| Input | What it is | How it is treated |
|---|---|---|
| **First-party observation**: a hit in the organisation's own telemetry (`/lookup-sentinel`, EDR, internal incident records) | The best-graded evidence there is | An evidence item graded **direct, established**, `claim_type: observation`, `access: telemetry`, source "user environment", `provenance_basis: first-party` (rubric rule R12). It participates fully, can be load-bearing, and can raise the ceiling. A miss is not evidence of absence and is not an item |
| **KEV listing** | A claim by CISA that exploitation has been observed | Evidence. Graded like any government claim through `/quality-of-information-check` |
| **CVSS and EPSS** | Attributes of a CVE | Not claims and not evidence about the event. They do not enter the claim table and have no effect on the ceiling. List them in Sources as reference data |

## Confidence Ceiling: The Weakest Link

The confidence level of the assessment cannot exceed what the weakest load-bearing claim supports. Apply the table below to every graded item with `load_bearing: true`. An ungraded item the conclusion depends on sets the ceiling at Moderate, unless a graded item sets it lower. The lowest result is the ceiling, and the claim that produced it is the weakest link. This is the claim named in `event_qoi_summary.weakest_link`, which uses the same bands.

| Weakest load-bearing claim | Maximum confidence |
|---|---|
| Established, with access level direct or limited | **High** |
| Firm, or established with access level indirect | **Moderate** |
| Tentative | **Low** |
| Disputed or unverified | **No confidence level.** State the gap |

Access level untraced or adversary lowers the result by one level. So does flag `source_record_disputed`. A claim graded untraced, tentative or adversary, tentative that carries the conclusion therefore gives no confidence level.

Why the threshold for High is claim support established: high confidence is for judgments resting on high-quality information from more than one source. Firm is, by the rubric's own definition, a single source that observed the thing directly, with no independent confirmation. Established is the independently confirmed level.

Where a numeric score is required, it stays inside the band for that level in `/confidence-levels`: 80 to 100 for High, 60 to 79 for Moderate, 40 to 59 for Low.

When the ceiling is "no confidence level", do not publish a judgment with a confidence label. Write what is known, state that the claim the conclusion depends on cannot carry it, and say what collection would change that.

Rules:
- This is a ceiling, not a target. Weak analytical logic or untested assumptions lower confidence further. Nothing raises it above the ceiling.
- Claims flagged `press_originated` and claims with `load_bearing: false` cannot carry the conclusion. If the conclusion needs one of them, the user must promote it, and it then counts as the weakest link.
- To raise the ceiling, corroborate the weakest link or rewrite the conclusion so it no longer depends on that claim. Do not drop the claim from Sources to get a higher level.
- State the weakest link in the confidence rationale, by `claim_id` and grade:

> "Confidence: low. The weakest load-bearing claim is C04 (attribution; direct, tentative): a single primary stating moderate confidence, corroboration unchecked. Core observations are direct, firm, which would support moderate. Independent confirmation of the attribution would raise the ceiling."

## Assessment Components

### Intent — What does the adversary want?
| Rating | Criteria |
|--------|---------|
| **Demonstrated** | Active targeting observed, stated objectives, ongoing operations against similar targets |
| **Probable** | Historical targeting of similar organisations/sectors, geopolitical alignment, inferred from capability development |
| **Possible** | General capability exists, sector/geography falls within known interests, no direct indicators |
| **Unlikely** | No known interest in sector/geography, no historical targeting of similar targets |

**Evidence to assess intent:**
- Direct targeting of the organisation or sector
- Stated objectives (manifestos, claims, leaked documents)
- Historical targeting patterns
- Geopolitical/economic motivations
- Reconnaissance activity observed

### Capability — What can the adversary do?
| Rating | Criteria |
|--------|---------|
| **Advanced** | Zero-day exploitation, custom tooling, state-level resources, proven track record of complex operations |
| **Significant** | Sophisticated TTPs, modified tools, professional operations, ability to adapt |
| **Moderate** | Known exploits and commodity tools, some custom capability, competent operations |
| **Basic** | Script-kiddie level, publicly available tools only, limited operational security |

**Evidence to assess capability:**
- Known tools and malware sophistication
- Historical operations and their complexity
- Resources (financial, human, infrastructure)
- Ability to develop or acquire zero-days
- Operational security and counter-intelligence capability

### Opportunity — What attack surface exists?
| Rating | Criteria |
|--------|---------|
| **Significant** | Large internet-facing footprint, known unpatched vulnerabilities, supply chain exposure, limited security controls |
| **Moderate** | Some internet exposure, generally patched but gaps exist, reasonable security controls |
| **Limited** | Minimal attack surface, strong security controls, rapid patching, limited supply chain exposure |
| **Minimal** | Air-gapped or highly restricted, advanced security controls, comprehensive monitoring |

**Evidence to assess opportunity:**
- Internet-facing services and known vulnerabilities
- Supply chain relationships and third-party access
- Security control maturity (detection, response)
- Employee exposure (social media, conferences)
- Historical incidents and near-misses

## Combining into Threat Level

| Level | Criteria |
|-------|---------|
| **CRITICAL** | Demonstrated intent + Advanced capability + Significant opportunity. Attack is imminent or ongoing. |
| **HIGH** | Strong intent indicators + Significant capability + Exploitable opportunity. Attack is highly likely. |
| **MODERATE** | Some intent indicators + Moderate capability + Some opportunity. Attack is a realistic possibility. |
| **LOW** | Limited intent indicators + Basic/Moderate capability + Limited opportunity. Attack is unlikely. |
| **NEGLIGIBLE** | No credible intent OR minimal capability OR no meaningful opportunity. |

## Output Template

```markdown
## Threat Assessment: [Subject]
**Date**: YYYY-MM-DD | **Confidence**: [Level] | **TLP**: [Level] | **Evidence basis**: [graded / mixed / ungraded] | **Provenance basis**: [Basis]

### Threat Level: [CRITICAL/HIGH/MODERATE/LOW/NEGLIGIBLE]

### Confidence Rationale
[Level and why. Weakest load-bearing claim: claim_id, claim_type, grade, and what would raise it.]

### Intent: [Rating]
[Assessment with evidence and confidence]

### Capability: [Rating]
[Assessment with evidence and confidence]

### Opportunity: [Rating]
[Assessment with evidence and confidence]

### Combined Assessment
[Synthesis of intent + capability + opportunity into overall threat level. Use likelihood language for forward-looking statements.]

### Key Assumptions
[List each assumption the conclusion rests on, its basis, and what changes if it is wrong. Invoke `/key-assumptions-check` for the full technique when the user asks for it, when confidence is High, or when the assessment will be disseminated outside the team. Otherwise list the assumptions here and state "A full /key-assumptions-check was not run."]

### Recommended Mitigations
1. [Prioritised by impact on reducing threat level]

### Sources
**Evidence basis**: [graded / mixed / ungraded]
**Provenance basis**: [platform-resolved / script-resolved / model-judged (unverified) / none (ungraded)]

| claim_id | Claim | claim_type | Primary (org, title, date) | Access level | Claim support | Independent primaries (basis) | Flags |
|----------|-------|------------|----------------------------|:---:|:---:|:---:|-------|
| C01 | [claim] | observation | [Vendor], "[Report title]", YYYY-MM-DD | direct | firm | 1 (unchecked) | single_source |

[Cite the primary, not the outlet that carried it. Several outlets covering one primary are one source. First-party observations appear in the table as graded items. CVSS and EPSS are listed separately as reference data.]
```
