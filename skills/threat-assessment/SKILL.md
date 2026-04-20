---
name: threat-assessment
description: Structured threat assessment methodology. Intent + Capability + Opportunity = Threat Level. Use when formally evaluating a threat.
user-invocable: true
metadata:
  version: 1.0.0
---

# Threat Assessment Methodology

A threat assessment evaluates the threat posed by a specific actor or scenario to a specific target. It combines Intent, Capability, and Opportunity into an overall Threat Level.

## Formula
**Threat = Intent + Capability + Opportunity**

All three must be present for a credible threat. A highly capable actor with no intent poses minimal threat. A motivated actor with no capability poses minimal threat.

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
**Date**: YYYY-MM-DD | **Confidence**: [Level] | **TLP**: [Level]

### Threat Level: [CRITICAL/HIGH/MODERATE/LOW/NEGLIGIBLE]

### Intent: [Rating]
[Assessment with evidence and confidence]

### Capability: [Rating]
[Assessment with evidence and confidence]

### Opportunity: [Rating]
[Assessment with evidence and confidence]

### Combined Assessment
[Synthesis of intent + capability + opportunity into overall threat level. Use likelihood language for forward-looking statements.]

### Key Assumptions
[Per key-assumptions-check]

### Recommended Mitigations
1. [Prioritised by impact on reducing threat level]

### Sources
[With Admiralty Scale ratings]
```
