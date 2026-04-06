---
name: intelligence-sharing
description: Guide to intelligence sharing models, standards, and communities. ISAC participation, TLP-governed sharing, STIX/TAXII, FIRST, MISP.
user-invocable: true
metadata:
  version: 1.0.0
---

# Intelligence Sharing

## Why Share?

Intelligence sharing creates a network effect — threats identified by one organisation protect the entire community. However, sharing must be governed, reciprocal, and risk-managed.

## Sharing Models

### 1. ISACs (Information Sharing and Analysis Centers)
Sector-specific sharing communities.

| ISAC | Sector | URL |
|------|--------|-----|
| FS-ISAC | Financial Services | fs-isac.com |
| H-ISAC | Healthcare | h-isac.org |
| IT-ISAC | Technology | it-isac.org |
| E-ISAC | Energy | eisac.com |
| A-ISAC | Aviation | a-isac.com |
| Auto-ISAC | Automotive | automotiveisac.com |

**Benefits**: Sector-relevant intelligence, trusted community, pre-vetted members, established TLP norms.

### 2. FIRST (Forum of Incident Response and Security Teams)
Global incident response community. Membership-based, includes national CERTs and enterprise security teams.

**Sharing via**: FIRST mailing lists, TF-CSIRT community, CTI SIG.

### 3. MISP (Malware Information Sharing Platform)
Open-source threat intelligence platform for sharing IOCs and threat data.

**How to share via MISP:**
1. Create an event with appropriate distribution
2. Add attributes (IOCs) with correct types
3. Tag with TLP, ATT&CK techniques, and galaxies
4. Set distribution: Organisation only / Community / Connected communities / All
5. Publish event

### 4. STIX/TAXII (Automated Sharing)
Standards for structured intelligence exchange.

- **STIX 2.1**: Format for representing intelligence (see stix-bundle skill)
- **TAXII 2.1**: Transport protocol for exchanging STIX bundles

**TAXII channels:**
- Collections: Server-hosted repositories of STIX objects
- Channels: Push-based distribution
- API roots: Discovery endpoints

### 5. Bilateral/Multilateral Sharing
Direct sharing with trusted partners under agreed terms.

**Requirements:**
- Sharing agreement (legal framework)
- TLP adherence by both parties
- Secure communication channel
- Reciprocity expectation

## TLP and Sharing

| TLP | Sharing Scope | Automated Sharing? |
|-----|--------------|-------------------|
| RED | Named recipients only | No |
| AMBER+STRICT | Own organisation | No |
| AMBER | Organisation + need-to-know | Restricted TAXII |
| GREEN | Community | ISAC portals, MISP community |
| CLEAR | Unrestricted | Public TAXII feeds, blogs |

## What to Share

### Do Share
- IOCs from confirmed incidents (with context)
- TTPs observed in your environment
- Detection rules that work
- Vulnerability intelligence relevant to sector
- Anonymised incident lessons learned

### Don't Share
- Source-identifying information without source consent
- Victim-identifying information without victim consent
- Raw internal telemetry or logs
- Information that reveals your security posture
- Speculation presented as intelligence

## Sharing Quality

Shared intelligence should meet the same quality standards as internal products:
- Source assessment (Admiralty Scale)
- Confidence levels
- MITRE ATT&CK mapping
- Proper TLP marking
- Context (not just raw IOCs — explain what they mean)

The number one complaint about shared intelligence: "Just IOCs with no context." Always share the WHY alongside the WHAT.

## Legal Considerations

- Comply with data protection regulations (GDPR, sector-specific rules)
- Ensure sharing agreements cover liability
- TLP is a trust agreement, not a legal framework — complement with contracts
- Be aware of export control regulations for certain technical intelligence
- Document all sharing decisions for audit trail
