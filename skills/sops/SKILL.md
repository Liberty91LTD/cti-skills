---
name: sops
description: Use when the user asks about CTI standard operating procedures (daily triage, IOC processing, flash-report cadence, threat-actor profile updates, briefing schedule), or wants to look up a specific SOP.
user-invocable: true
metadata:
  version: 1.0.0
---

# Standard Operating Procedures

## SOP-001: Daily Intelligence Triage

**Frequency**: Daily
**Owner**: Orchestrator

1. Review overnight intelligence feeds and alerts
2. Check active PIRs — any new information relevant to Critical/High PIRs?
3. Triage new indicators:
   - Discard noise (known benign, low confidence, duplicate)
   - Fast-track critical indicators (active exploitation, direct relevance)
   - Queue remaining for standard processing
4. Dispatch OSINT researcher for any trending threats relevant to PIRs
5. Update relevant knowledge cells with new significant intelligence
6. Produce daily intelligence brief if significant developments occurred

## SOP-002: IOC Processing

**Trigger**: New IOC list received (from internal detection, external sharing, or OSINT collection)
**Owner**: IOC Processor

1. Parse and classify all indicators
2. Validate format (reject malformed)
3. Deduplicate against existing active IOC collections
4. Enrich via enrichment workflow (dispatch tool agents)
5. Apply source assessment to enrichment results
6. Synthesise verdict (malicious/suspicious/benign/unknown)
7. Store in `data/iocs/active/`
8. If actionable: request detection rule creation from detection engineer
9. If significant: flag to orchestrator for flash report consideration
10. Export in relevant formats if sharing is appropriate

## SOP-003: Flash Report Creation

**Trigger**: Time-critical intelligence requiring immediate stakeholder action
**Owner**: Orchestrator → Analyst → Report Writer → Quality Reviewer

1. Orchestrator identifies time-critical situation
2. Dispatch analyst for rapid assessment (30-minute time box)
3. Dispatch report writer with flash report template
4. Quality reviewer performs expedited review (critical checks only):
   - TLP correct?
   - Key finding supported?
   - IOCs validated?
   - Actions clear?
5. Disseminate via appropriate TLP channel
6. Link to relevant PIRs
7. Schedule follow-up analysis if warranted

**Expedited review**: For flash reports, quality review focuses on CRITICAL issues only. MAJOR and MINOR issues are noted but don't block publication. Speed matters.

## SOP-004: Threat Actor Profile Update

**Trigger**: Significant new intelligence about a tracked threat actor
**Owner**: Orchestrator → Analyst

1. Identify which knowledge cell applies
2. Load the knowledge cell
3. Dispatch analyst to review new intelligence against existing cell
4. Analyst determines:
   - What is genuinely new?
   - What confirms existing knowledge?
   - What contradicts existing knowledge?
5. Update knowledge cell:
   - Add new campaign entries
   - Update TTP tables
   - Revise executive summary if landscape changed
   - Add to Sources & References
   - Log change in Change Log
6. If significant change: flag for stakeholder communication

## SOP-005: Stakeholder Briefing

**Trigger**: Quarterly or ad-hoc stakeholder request
**Owner**: Orchestrator → Analyst → Report Writer

1. Review active PIRs for the stakeholder
2. Gather satisfaction history since last briefing
3. Dispatch analyst to prepare briefing content:
   - Key developments since last briefing
   - PIR satisfaction status
   - Emerging threats relevant to stakeholder
   - Recommended PIR adjustments
4. Dispatch report writer to produce briefing document
5. Tailor format to stakeholder (per stakeholder-management skill)
6. Quality review
7. Deliver via appropriate channel
8. Collect feedback
9. Update PIRs based on feedback

## SOP-006: Quarterly PIR Review

**Frequency**: Quarterly
**Owner**: Orchestrator

1. List all active PIRs
2. For each PIR:
   - Review satisfaction history
   - Check stakeholder is still active/relevant
   - Assess if priority should change
   - Determine if scope needs adjustment
   - Decide: maintain / modify / retire
3. Archive retired PIRs
4. Create new PIRs based on stakeholder feedback and emerging threats
5. Update collection plans for modified PIRs
6. Document review outcomes

## SOP-007: Knowledge Cell Maintenance

**Frequency**: Monthly review, continuous updates
**Owner**: Orchestrator

1. List all knowledge cells
2. For each cell:
   - Check `last_updated` — flag any not updated in 60+ days
   - Review intelligence gaps — any now answerable?
   - Check if active campaigns have concluded → move to historical
   - Verify executive summary reflects current landscape
3. For stale cells: dispatch OSINT researcher for current intelligence
4. For cells with resolved gaps: update gap list
5. Consider: are new cells needed for emerging threats?
