---
name: maturity-assessment
description: Use when assessing the maturity of a CTI programme, the user asks "how mature is our CTI?" / "what should we improve next?", or wants a benchmark against the five-level model across six dimensions.
user-invocable: true
metadata:
  version: 1.0.0
---

# CTI Programme Maturity Assessment

## Maturity Levels

| Level | Name | Description |
|-------|------|-------------|
| **1** | Ad-hoc | No formal CTI function. Reactive, incident-driven. Intelligence is incidental. |
| **2** | Emerging | Basic CTI capability. Some collection, limited analysis. Primarily tactical (IOC feeds). |
| **3** | Defined | Formal CTI function with documented processes. Strategic, operational, and tactical output. PIRs defined. |
| **4** | Managed | Mature CTI programme. Stakeholder-driven, measured effectiveness, feedback loops. Proactive intelligence. |
| **5** | Optimized | Intelligence-driven organisation. CTI informs all security decisions. Continuous improvement, advanced analytics, community contribution. |

## Assessment Dimensions

### 1. Collection

| Level | Indicators |
|-------|-----------|
| 1 | No systematic collection. Ad-hoc Google searches when incidents occur. |
| 2 | 1-2 threat feeds (usually free). No collection plan. |
| 3 | Multiple sources across OSINT, commercial feeds, ISACs. Collection plan exists. Source assessment applied. |
| 4 | Comprehensive collection mapped to PIRs. Source quality tracked. Dark web monitoring. Automated collection pipelines. |
| 5 | Full-spectrum collection. HUMINT relationships (ISACs, vendors, government). Predictive collection based on emerging threat indicators. |

### 2. Analysis

| Level | Indicators |
|-------|-----------|
| 1 | No analysis. Raw data forwarded to SOC. |
| 2 | Basic enrichment (VirusTotal lookups). IOC correlation. No structured techniques. |
| 3 | Structured analysis applied. Threat assessments produced. ATT&CK mapping. Confidence levels used. |
| 4 | Full SAT toolkit (ACH, red team, horizon scanning). Knowledge cells maintained. Alternative hypotheses routinely considered. |
| 5 | Advanced analytics. Machine learning augments human analysis. Predictive threat modelling. Community-leading analysis. |

### 3. Production

| Level | Indicators |
|-------|-----------|
| 1 | No intelligence products. Maybe an IOC spreadsheet. |
| 2 | Ad-hoc alerts and IOC lists. No standard templates. Inconsistent quality. |
| 3 | Standardised products (flash reports, assessments). TLP applied. Likelihood language used. Quality review process. |
| 4 | Full product suite tailored to stakeholder needs. Detection rules (SIGMA/YARA/KQL). STIX bundles for sharing. |
| 5 | Dynamic intelligence products. Real-time dashboards. Automated tactical output. Strategic foresight publications. |

### 4. Dissemination

| Level | Indicators |
|-------|-----------|
| 1 | Intelligence stays within the CTI team. |
| 2 | IOCs pushed to SIEM/EDR. Some ad-hoc briefings. |
| 3 | Products reach defined stakeholders. TLP-governed sharing. Regular briefing cadence. |
| 4 | Tailored delivery per stakeholder. Integration with SOAR/TIP. Feedback collected. ISAC participation. |
| 5 | Intelligence embedded in all security workflows. Automated dissemination. External sharing (STIX/TAXII). Industry thought leadership. |

### 5. Management

| Level | Indicators |
|-------|-----------|
| 1 | No CTI manager. Analyst works in isolation. |
| 2 | Informal CTI role. No PIRs. No stakeholder engagement. |
| 3 | Formal CTI function. PIRs defined and reviewed. Stakeholder register maintained. SOPs documented. |
| 4 | Programme measured on outcomes. KPIs tracked. Budget justified. Regular programme reviews. |
| 5 | CTI programme informs security strategy. Board-level reporting. CTI drives investment decisions. |

### 6. Tooling

| Level | Indicators |
|-------|-----------|
| 1 | Email and spreadsheets only. |
| 2 | Free tools (VirusTotal, MISP community). Manual processes. |
| 3 | TIP deployed. OSINT tools in use. Some automation. |
| 4 | Integrated toolchain. API-driven enrichment. SOAR integration. Custom tooling where needed. |
| 5 | AI-augmented analysis. Full automation of tactical workflows. Custom detection engineering pipeline. |

## Self-Assessment Questionnaire

For each dimension, select the level that BEST describes current capability:

```markdown
## CTI Maturity Self-Assessment

**Date**: YYYY-MM-DD
**Assessed by**: [Name/Role]

| Dimension | Current Level | Target Level | Gap |
|-----------|:---:|:---:|:---:|
| Collection | _ | _ | _ |
| Analysis | _ | _ | _ |
| Production | _ | _ | _ |
| Dissemination | _ | _ | _ |
| Management | _ | _ | _ |
| Tooling | _ | _ | _ |
| **Overall** | **_** | **_** | **_** |

### Key Findings
[What are the biggest gaps?]

### Recommended Actions
1. [Highest-impact improvement]
2. [Second priority]
3. [Third priority]

### Timeline
[Realistic timeline for reaching target maturity]
```

## Improvement Priorities

When improving maturity, prioritise in this order:
1. **Management** (PIRs, stakeholders) — without direction, other improvements are wasted
2. **Collection** — can't analyse what you don't have
3. **Analysis** — transform data into intelligence
4. **Production** — package intelligence effectively
5. **Dissemination** — get intelligence to decision-makers
6. **Tooling** — automate and scale (last, not first)

This order reflects a common mistake: organisations buy tools (Level 6) before establishing processes (Levels 1-5). Tools amplify process — if the process is broken, tools amplify the problem.
