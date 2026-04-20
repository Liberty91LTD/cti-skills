---
name: quality-control
description: Peer review checklist and quality standards for intelligence products. Loaded by the quality-reviewer agent.
user-invocable: false
metadata:
  version: 1.0.0
---

# Quality Control Standards

## Review Process

1. All products must be reviewed before moving to "published" status
2. Reviews are performed by the quality-reviewer agent
3. Products with CRITICAL issues are returned for revision
4. Products with 3+ MAJOR issues are returned for revision
5. MINOR issues are noted but don't block publication

## Peer Review Checklist

### A. Structural Integrity (Weight: 15%)
- [ ] Correct product template used
- [ ] Complete frontmatter (all required fields)
- [ ] TLP marking present and correctly applied
- [ ] Logical section ordering
- [ ] Appropriate length for product type

### B. Analytical Rigor (Weight: 30%)
- [ ] Conclusions supported by evidence
- [ ] Key assumptions explicitly identified
- [ ] Alternative hypotheses considered (where applicable)
- [ ] Structured analytic techniques applied appropriately
- [ ] No logical leaps or unsupported assertions
- [ ] Temporal scope specified for all predictions
- [ ] Intelligence gaps acknowledged

### C. Sourcing (Weight: 20%)
- [ ] All sources assessed with Admiralty Scale
- [ ] Source ratings justified and reasonable
- [ ] Source diversity (not single-source unless noted)
- [ ] Derivative vs independent sources distinguished
- [ ] No unattributed claims

### D. Mandated Language (Weight: 20%)
- [ ] Confidence levels on all assessments (with rationale)
- [ ] Likelihood language on all predictions (with percentage ranges)
- [ ] No hedge-stacking
- [ ] No vague probabilistic language without probability band
- [ ] Confidence and likelihood not conflated
- [ ] Facts clearly distinguished from assessments

### E. Technical Accuracy (Weight: 10%)
- [ ] MITRE ATT&CK mappings correct
- [ ] IOCs properly formatted and validated
- [ ] Technical claims verifiable
- [ ] No contradictions with known intelligence

### F. Writing Quality (Weight: 5%)
- [ ] BLUF in first paragraph
- [ ] Active voice
- [ ] Specific language (dates, numbers, names)
- [ ] No unnecessary jargon
- [ ] Clear, concise sentences

## Scoring

Calculate weighted score (0-10):
- Each section: 0 (none met) to 10 (all met)
- Weighted by percentages above
- Final score = weighted average

| Score | Verdict |
|-------|---------|
| 8-10 | Approved — publish |
| 6-7 | Approved with minor revisions — can publish after fixes |
| 4-5 | Revision required — significant issues |
| 0-3 | Rejected — fundamental problems |

## Issue Severity

- **CRITICAL**: Factual error in key finding, missing TLP on sensitive content, unsupported primary conclusion, potential harm if published as-is
- **MAJOR**: Missing confidence level on assessment, vague likelihood language on prediction, missing source assessment on key evidence, logical flaw in reasoning, missing key section
- **MINOR**: Grammar/formatting, style inconsistency, minor Admiralty rating disagreement, non-essential section could be improved
