---
name: campaign-tracking
description: Use when documenting a named campaign across time and victims, the user asks to start or update a campaign record, or another skill identified a multi-incident cluster that warrants formal tracking. Provides the template (timeline, attribution, victimology, attack chain, Diamond Model mapping, IOC clusters) and the lifecycle from active to historical.
user-invocable: true
metadata:
  version: 1.1.0
---

# Campaign Tracking

A campaign is a coordinated set of malicious activities carried out by a threat actor against specific targets over a defined period.

## Sourcing Before Tracking

A campaign record is built from claims, and each claim belongs to the source that originated it. Before any report feeds the record:

1. **Resolve provenance.** Run `/source-provenance` on every ingested report or article. Record the primary, the chain and the `provenance_basis` (platform-resolved, script-resolved or model-judged).
2. **Dedupe by primary, not by URL.** Five outlets covering one vendor report are one source and produce one timeline row, not five. List the outlets as "via". Count corroboration by independent primaries with separate access only.
3. **Grade per claim.** Run `/quality-of-information-check` on the primary (it calls `/claim-extraction`). The intrusion, the vector, the attribution and the actor's own figures carry different grades.
4. **Store the grade with the entity.** Every timeline row, attack chain row, attribution statement and victim count carries the primary that supports it and the grade of the supporting claim.

Actor claims about victim count or data volume are graded "adversary, unverified" until an independent primary corroborates them. Record them as actor-claimed, not as findings. Grades follow the fixed rubric in `/quality-of-information-check` (`references/grading-rubric.md`). The grade is two words, access level then claim support, for example "direct, firm". It is not an Admiralty rating. Your own telemetry and SOC alerts are primaries in their own right, name them as such.

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
| **Independent primaries** | [Count of originating sources with separate access, and basis] |
| **Provenance basis** | [platform-resolved / script-resolved / model-judged (worst of the sources used)] |
| **Alias source** | [user / liberty91 / none] |

### Timeline
| Date | Event | Primary | Access level | Claim support |
|------|-------|---------|--------------|---------------|
| YYYY-MM-DD | Initial delivery emails sent | Internal telemetry | direct | established |
| YYYY-MM-DD | First successful compromise | [Vendor, report title] | limited | firm |
| YYYY-MM-DD | Lateral movement detected | SOC alert | direct | established |
| YYYY-MM-DD | Data exfiltration observed | Network forensics | direct | established |

### Attribution
[Assessment of who is behind this campaign, with confidence level. Reference threat actor profile if available.]

| Attribution statement | Primary | Stated confidence (verbatim) | Access level | Claim support | Independent primaries |
|-----------------------|---------|------------------------------|--------------|---------------|-----------------------|
| [Campaign is linked to X] | [Org, report title, date] | ["moderate confidence" / not stated] | [e.g., limited] | [e.g., tentative] | [Count, and basis] |

### Victimology
- **Sectors targeted**: [List]
- **Geographies**: [Countries/regions]
- **Number of known victims**: [Count with confidence, primary and grade. Mark actor-claimed figures as such]
- **Selection criteria**: [How were targets chosen? Opportunistic vs targeted?]
- **Common characteristics**: [What do victims have in common?]

### Attack Chain (Kill Chain / ATT&CK)
| Phase | Technique (ATT&CK) | Details | Primary | Access level | Claim support |
|-------|-------------------|---------|---------|--------------|---------------|
| Reconnaissance | T1598 Phishing for Information | Targeted LinkedIn messages to identify employees | [Org, date] | [e.g., limited] | [e.g., firm] |
| Initial Access | T1566.001 Spearphishing Attachment | Malicious Word doc with macro | [Org, date] | [e.g., direct] | [e.g., firm] |
| Execution | T1059.001 PowerShell | Macro downloads PowerShell stager | [Org, date] | [e.g., direct] | [e.g., firm] |
| Persistence | T1547.001 Registry Run Keys | Run key added for backdoor | [Org, date] | [e.g., direct] | [e.g., firm] |
| C2 | T1071.001 Application Layer Protocol | HTTPS to legitimate cloud service | [Org, date] | [e.g., limited] | [e.g., firm] |
| Exfiltration | T1567.002 Exfiltration to Cloud Storage | Data uploaded to attacker-controlled cloud | [Org, date] | [e.g., limited] | [e.g., firm] |

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
One row per primary. Outlets that carried the primary go in "Via".

| Date | Primary source | Via | Access | Access level | Key Finding |
|------|----------------|-----|--------|--------------|-------------|
```

Access level in the Sources table is the level that follows from the primary's stated access. It is the default for that primary's claims. Claim support belongs to each claim, so the full grade sits on the timeline, attribution and attack chain rows. Rows from your own telemetry, SOC alerts and forensics are first-party observations, graded "direct, established" (rule R12).

## Campaign Linking
Campaigns may be related. Document relationships:
- **Same infrastructure**: Shared C2, shared registrant
- **Same tooling**: Same malware family or builder
- **Same TTPs**: Identical techniques across campaigns
- **Same victimology**: Same sector/geography targeting
- **Temporal overlap**: Concurrent operations

Linking on infrastructure, hashes and CVEs compares values directly and needs no name matching. Linking reports that use different actor or malware names needs an alias source: your own alias file (`skills/quality-of-information-check/references/aliases.yml`, user-maintained, loaded when present, `alias_source: user`) or the Liberty91 Threat Library via `/lookup-liberty91` when `LIBERTY91_API_KEY` is set (`alias_source: liberty91`). With neither, names are not matched across vendors (`alias_source: none`), differently named reporting does not count as corroboration, and the campaign record says so, naming both options. Do not match names from memory.

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
- **Publish the campaign as a sharable artefact** — `/lookup-misp create-event` writes the cluster into your MISP instance; `/stix-bundle` produces the STIX 2.1 representation; `/lookup-opencti upload-stix` imports that bundle into your OpenCTI knowledge base (or `create-relationship` to link indicators to an existing campaign entity); `/lookup-liberty91 ingest` files the campaign write-up as a report in Liberty91, where it is enriched and matched into a Threat Event for your account (metered — confirm with the user first)
- **Seed and update the timeline from occurrences** — `/lookup-liberty91 threat-events --technique <Txxxx> --target-sector <s> --occurred-after <date>` for candidate incidents, and `entity threat-actors <id> --section threat-events` once the actor is attributed. Each occurrence is already deduplicated across its reporting, so the timeline doesn't need re-collapsing; carry its `verification` stage and `credibility` band into the campaign record as the platform's ratings rather than restating them as your own judgement, and do not copy them into an evidence grade
- **Actor attribution** — `/threat-actor-profiling` consumes the campaign output to build / update an actor profile
- **Provenance and grading** — `/source-provenance` on every ingested report, `/claim-extraction` to split it into typed claims, `/quality-of-information-check` for per-claim evidence grades (access level and claim support). `/source-assessment` remains the reference for the Admiralty scale itself, which applies to lookup results and single items. Neither is converted into the other.
- **Apply rigor to the campaign report** — `/score-source`, `/apply-tlp`, `/confidence-language`, `/likelihood-language`, `/intelligence-writing`
