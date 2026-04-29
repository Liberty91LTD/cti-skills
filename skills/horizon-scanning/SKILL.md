---
name: horizon-scanning
description: Use when the user asks "what is coming next?", wants strategic forecasting, or is hunting weak signals of emerging threats before they materialise. Covers signal identification, trend analysis, and scenario development.
user-invocable: true
metadata:
  version: 1.0.0
---

# Horizon Scanning

Horizon scanning identifies emerging threats, opportunities, and developments that could impact the organisation's security posture in the medium to long term (6-24 months).

## Process

### 1. Define Scope
- Time horizon (6 months? 12 months? 24 months?)
- Focus areas (specific sectors, threat types, geographies)
- Stakeholder needs (what decisions will this inform?)

### 2. Identify Weak Signals
Weak signals are early indicators of emerging trends. Sources:
- Academic research and conference papers (BlackHat, DEF CON, CCC, academic journals)
- Underground forum discussions (new tools, techniques being discussed)
- Patent filings and startup activity (indicators of new capabilities)
- Geopolitical developments (sanctions, conflicts, elections)
- Regulatory changes (new compliance requirements creating new attack surfaces)
- Technology adoption trends (new tech = new attack surface)

### 3. Categorise Signals

| Category | Examples |
|----------|---------|
| **Emerging TTPs** | New exploitation techniques, novel social engineering methods, AI-augmented attacks |
| **Technology shifts** | New platforms widely adopted, legacy tech being deprecated, cloud migration patterns |
| **Threat actor evolution** | New groups emerging, existing groups changing targets, capability development |
| **Geopolitical drivers** | Conflicts, sanctions, elections, diplomatic shifts |
| **Regulatory/legal** | New laws, enforcement actions, liability changes |
| **Underground economy** | New services, market shifts, ecosystem changes |

### 4. Develop Scenarios
For each significant signal, develop three scenarios:
- **Best case**: Signal does not materialise or is mitigated
- **Worst case**: Signal materialises with maximum impact
- **Most likely**: Balanced assessment based on available evidence

### 5. Assess Impact and Likelihood
For each scenario:
- Likelihood (using probability yardstick from likelihood-language skill)
- Impact on organisation (Critical/High/Moderate/Low/Negligible)
- Time to materialise
- Confidence in assessment

### 6. Identify Early Warning Indicators
For each high-impact scenario, define:
- What observable indicators would suggest this is materialising?
- Where would we see these indicators? (collection sources)
- How frequently should we monitor?

## Output Template

```markdown
## Horizon Scanning Report: [Focus Area]
**Period**: [Time horizon]
**Date**: YYYY-MM-DD

### Executive Summary
[Key emerging threats and their implications]

### Emerging Threats

#### [Threat 1]: [Title]
- **Signal strength**: Weak / Emerging / Established
- **Time horizon**: [When could this materialise?]
- **Likelihood**: [Probability yardstick term]
- **Potential impact**: [Critical/High/Moderate/Low]
- **Confidence**: [Level with rationale]
- **Description**: [What is this threat and why does it matter?]
- **Early warning indicators**: [What to watch for]
- **Recommended action**: [Proactive steps]

### Scenario Analysis
[For top 2-3 threats, develop best/worst/most likely scenarios]

### Collection Gaps
[What we need to monitor but currently can't]
```

## Common Signals to Monitor (CTI)
- AI-powered phishing/deepfakes maturation
- Quantum computing impact on cryptography
- Supply chain security tooling gaps
- Cloud-native attack technique evolution
- Ransomware business model evolution
- Nation-state cyber capability proliferation
- Infostealer-to-ransomware pipeline evolution
- Edge device/IoT exploitation trends
