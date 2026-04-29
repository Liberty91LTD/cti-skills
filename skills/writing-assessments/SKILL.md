---
name: writing-assessments
description: Use when the user asks to write a threat / risk / vulnerability assessment, or wants the appropriate template for each type. Distinct structures and section ordering per assessment kind.
user-invocable: true
metadata:
  version: 1.0.0
---

# Writing Assessments

Three types of assessments, each with distinct purpose and structure. Do not conflate them.

## Threat Assessment

**Purpose**: Evaluate a threat actor or threat scenario against a specific target.

**Formula**: Threat = Intent + Capability + Opportunity

### Structure

**1. Intent** — What does the adversary want?
- Stated objectives (if known)
- Historical targeting patterns
- Geopolitical/economic motivations
- Assessment of intent with confidence level

**2. Capability** — What can the adversary do?
- Technical sophistication
- Resources (financial, human, infrastructure)
- Known tooling and TTPs
- Track record of successful operations
- Assessment of capability with confidence level

**3. Opportunity** — What attack surface exists?
- Target's exposure (internet-facing services, supply chain)
- Known vulnerabilities relevant to the adversary's TTPs
- Access pathways (initial access vectors)
- Defensive posture gaps
- Assessment of opportunity with confidence level

**4. Combined Threat Level**

| Level | Criteria |
|-------|---------|
| **Critical** | Demonstrated intent, advanced capability, and clear opportunity. Attack is imminent or ongoing. |
| **High** | Strong intent indicators, significant capability, and exploitable opportunity. Attack is highly likely in assessment period. |
| **Moderate** | Some intent indicators, moderate capability, and some opportunity. Attack is a realistic possibility. |
| **Low** | Limited intent indicators, basic capability, or minimal opportunity. Attack is unlikely. |
| **Negligible** | No credible intent, minimal capability, or no meaningful opportunity. |

### Example assessment statement
> "We assess the threat level from APT41 to European pharmaceutical companies as **HIGH** (confidence: high). APT41 has demonstrated intent through active reconnaissance (observed since November 2025), possesses advanced capability including zero-day exploitation, and the sector presents significant opportunity due to widespread legacy VPN infrastructure."

## Risk Assessment

**Purpose**: Evaluate the potential impact of a threat materialising.

**Formula**: Risk = Threat × Vulnerability × Impact

### Structure

**1. Threat** (reference or summarise from threat assessment)
- Threat level from threat assessment
- Key threat characteristics

**2. Vulnerability** — How exposed is the target?
- Technical vulnerabilities (CVEs, misconfigurations)
- Process vulnerabilities (gaps in detection, response)
- Human vulnerabilities (social engineering susceptibility)
- Supply chain vulnerabilities

**3. Impact** — What happens if the threat materialises?
- Operational impact (business disruption, data loss)
- Financial impact (direct costs, regulatory fines, market impact)
- Reputational impact (customer trust, brand damage)
- Strategic impact (competitive advantage, IP loss)
- Impact severity: Critical / High / Moderate / Low / Negligible

**4. Combined Risk Level**

Use a risk matrix:

|  | Negligible Impact | Low Impact | Moderate Impact | High Impact | Critical Impact |
|--|---|---|---|---|---|
| **Critical Threat** | Moderate | High | Very High | Very High | Very High |
| **High Threat** | Low | Moderate | High | Very High | Very High |
| **Moderate Threat** | Low | Low | Moderate | High | Very High |
| **Low Threat** | Very Low | Low | Low | Moderate | High |
| **Negligible Threat** | Very Low | Very Low | Low | Low | Moderate |

### Example assessment statement
> "The risk of APT41 compromising sensitive R&D data is assessed as **VERY HIGH** (confidence: moderate). The high threat level (demonstrated intent and capability) combined with critical impact (loss of proprietary pharmaceutical research valued at €500M+) and significant vulnerability (unpatched VPN appliances matching APT41's known initial access vector) drive this assessment."

## Vulnerability Assessment

**Purpose**: Evaluate the exploitability and impact of a specific vulnerability.

**Formula**: Vulnerability Severity = Exposure + Susceptibility − Resilience

### Structure

**1. Vulnerability Description**
- CVE identifier (if applicable)
- Affected systems/software
- Technical description of the vulnerability

**2. Exposure** — How visible/accessible is the vulnerable system?
- Internet-facing vs internal only
- Number of affected systems
- Public availability of exploit code (PoC, weaponised)

**3. Susceptibility** — How easy is it to exploit?
- CVSS base score
- EPSS (Exploit Prediction Scoring System) score
- Technical complexity of exploitation
- Authentication requirements
- Known exploitation in the wild (CISA KEV listing)

**4. Resilience** — What mitigations exist?
- Patch availability
- Compensating controls
- Detection capability (do we have rules for this?)
- Recovery capability

**5. Prioritisation**

| Priority | Criteria |
|----------|---------|
| **P1 — Patch immediately** | Actively exploited OR high EPSS + internet-facing + no compensating controls |
| **P2 — Patch within 72h** | PoC available + internet-facing OR actively exploited + internal with compensating controls |
| **P3 — Patch within 30 days** | High CVSS + no active exploitation + compensating controls in place |
| **P4 — Patch in next cycle** | Moderate CVSS + internal only + compensating controls |
| **P5 — Accept risk** | Low CVSS + internal only + strong compensating controls + low impact |

## General Assessment Writing Rules

1. **Always state the assessment explicitly** — "We assess that..." not "It appears that..."
2. **Always include confidence level** — Per confidence-levels skill
3. **Always use likelihood language** — Per likelihood-language skill for future-looking statements
4. **Always identify key assumptions** — What must be true for this assessment to hold?
5. **Always separate facts from judgments** — Per intelligence-writing skill
6. **Never hedge-stack** — Pick one likelihood band, don't combine ("likely or highly likely")
7. **Always include temporal scope** — "Over the next 12 months" not "in the future"
