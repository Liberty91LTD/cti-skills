---
name: campaign-tracking
description: Use when documenting a named campaign across time and victims, the user asks to start or update a campaign record, or another skill identified a multi-incident cluster that warrants formal tracking. Provides the template (timeline, attribution, victimology, attack chain, Diamond Model mapping, IOC clusters) and the lifecycle from active to historical.
user-invocable: true
metadata:
  version: 1.0.0
---

# Campaign Tracking

A campaign is a coordinated set of malicious activities carried out by a threat actor against specific targets over a defined period.

## Campaign Template

```markdown
## Campaign: [Campaign ID / Name]

### Overview
| Field | Value |
|-------|-------|
| **Campaign ID** | CAMP-YYYY-MM-XXX |
| **Name** | [Descriptive name if known] |
| **Status** | Active / Dormant / Concluded |
| **First observed** | YYYY-MM-DD |
| **Last observed** | YYYY-MM-DD |
| **Attribution** | [Actor — with confidence level] |
| **Motivation** | [Espionage / Financial / Destruction / Hacktivism] |

### Timeline
| Date | Event | Source |
|------|-------|--------|
| YYYY-MM-DD | Initial delivery emails sent | Internal telemetry |
| YYYY-MM-DD | First successful compromise | Vendor report (B2) |
| YYYY-MM-DD | Lateral movement detected | SOC alert |
| YYYY-MM-DD | Data exfiltration observed | Network forensics |

### Attribution
[Assessment of who is behind this campaign, with confidence level. Reference threat actor profile if available.]

### Victimology
- **Sectors targeted**: [List]
- **Geographies**: [Countries/regions]
- **Number of known victims**: [Count with confidence]
- **Selection criteria**: [How were targets chosen? Opportunistic vs targeted?]
- **Common characteristics**: [What do victims have in common?]

### Attack Chain (Kill Chain / ATT&CK)
| Phase | Technique (ATT&CK) | Details |
|-------|-------------------|---------|
| Reconnaissance | T1598 Phishing for Information | Targeted LinkedIn messages to identify employees |
| Initial Access | T1566.001 Spearphishing Attachment | Malicious Word doc with macro |
| Execution | T1059.001 PowerShell | Macro downloads PowerShell stager |
| Persistence | T1547.001 Registry Run Keys | Run key added for backdoor |
| C2 | T1071.001 Application Layer Protocol | HTTPS to legitimate cloud service |
| Exfiltration | T1567.002 Exfiltration to Cloud Storage | Data uploaded to attacker-controlled cloud |

### Diamond Model
| Vertex | Details |
|--------|---------|
| **Adversary** | [Threat actor / group — reference profile] |
| **Capability** | [Malware, exploits, tools, techniques used] |
| **Infrastructure** | [C2 servers, staging, delivery infrastructure, domains] |
| **Victim** | [Targeted organisations, sectors, systems] |

**Meta-features:**
- **Direction**: [Adversary-to-Victim / Victim-to-Adversary / Bidirectional]
- **Methodology**: [Attack phases and progression]
- **Resources**: [Level of investment observed]
- **Social-Political**: [Geopolitical context driving the campaign]
- **Technology**: [Technology landscape enabling the campaign]

### IOC Clusters
#### Delivery Infrastructure
| Type | Value | First Seen | Status |
|------|-------|-----------|--------|
| Domain | phishing.example.com | 2026-01-15 | Active |
| IP | 203.0.113.42 | 2026-01-15 | Active |

#### C2 Infrastructure
| Type | Value | First Seen | Status |
|------|-------|-----------|--------|
| Domain | c2.badactor.net | 2026-01-20 | Active |
| IP | 198.51.100.10 | 2026-01-20 | Active |

#### Malware
| Hash (SHA-256) | Name | Type | First Seen |
|----------------|------|------|-----------|
| abc123... | loader.dll | Loader | 2026-01-15 |

### TTP Evolution During Campaign
[How have the attackers adapted? Changed tools? Modified techniques? Responded to detection?]

### Detection Guidance
[Reference to SIGMA/YARA/KQL rules created for this campaign. Link to data/detection-rules/.]

### Intelligence Gaps
[What we still don't know about this campaign]

### Sources
| Date | Source | Reliability | Key Finding |
|------|--------|-------------|-------------|
```

## Campaign Linking
Campaigns may be related. Document relationships:
- **Same infrastructure**: Shared C2, shared registrant
- **Same tooling**: Same malware family or builder
- **Same TTPs**: Identical techniques across campaigns
- **Same victimology**: Same sector/geography targeting
- **Temporal overlap**: Concurrent operations

## Campaign Lifecycle Management
1. **Detection**: Initial indicators or vendor report triggers campaign tracking
2. **Active tracking**: Continuous collection, IOC updates, TTP documentation
3. **Analysis**: Attribution, Diamond Model mapping, impact assessment
4. **Reporting**: Campaign report produced per intelligence-writing templates
5. **Conclusion**: Campaign ends (dormant or concluded), move to historical
6. **Knowledge cell update**: Feed findings into relevant knowledge cell

## Related skills

- **Build the IOC cluster** — `/indicator-pivoting` (multi-hop graph walk), `/ioc-enrichment-workflow` (bulk enrichment of raw IOCs)
- **Per-indicator first-hop investigation** — `/ip-investigation`, `/domain-investigation`, `/hash-investigation`, `/url-investigation`
- **Ransomware-group campaigns** — `/lookup-ransomwarelive group-profile <name>` returns the group's documented TTPs, leak-site infrastructure, and per-group IOC + YARA dumps; pair with `/ransomware-ecosystem` knowledge cell
- **Publish the campaign as a sharable artefact** — `/lookup-misp create-event` writes the cluster into your MISP instance; `/stix-bundle` produces the STIX 2.1 representation
- **Actor attribution** — `/threat-actor-profiling` consumes the campaign output to build / update an actor profile
- **Apply rigor to the campaign report** — `/score-source`, `/apply-tlp`, `/confidence-language`, `/likelihood-language`, `/intelligence-writing`
