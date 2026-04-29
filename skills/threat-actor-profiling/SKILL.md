---
name: threat-actor-profiling
description: Use when the user asks to build or update a threat-actor profile, "tell me about actor X" / "profile actor Y", or another skill needs the canonical profile template (attribution, TTPs, campaigns, infrastructure patterns, intelligence gaps).
user-invocable: true
metadata:
  version: 1.0.0
---

# Threat Actor Profiling

A threat actor profile is a living document that consolidates everything known about a threat group. It grows over time as new intelligence is collected.

## Profile Template

```markdown
## Threat Actor Profile: [Primary Name]

### Summary
| Field | Value |
|-------|-------|
| **Primary Name** | [Most commonly used name] |
| **Aliases** | [All known aliases across vendors] |
| **Attribution** | [State sponsor / Criminal group / Hacktivist — with confidence level] |
| **Affiliation** | [Specific agency/unit if known, e.g., GRU Unit 26165] |
| **Motivation** | [Espionage / Financial / Disruption / Hacktivism / Mixed] |
| **Active Since** | [Year of first known activity] |
| **Status** | [Active / Dormant / Disbanded] |
| **Sophistication** | [Low / Medium / High / Advanced] |
| **Primary Targets** | [Sectors and geographies] |
| **Assessment Date** | [Date of this profile version] |

### Attribution Assessment
[Detailed attribution discussion with confidence level. Who attributes this group and based on what evidence? Where do vendors disagree?]

### Targeting
**Sectors**: [List targeted sectors with evidence]
**Geographies**: [Targeted countries/regions]
**Selection criteria**: [How does this group choose targets? Opportunistic vs targeted?]
**Evolution**: [How has targeting changed over time?]

### TTPs (MITRE ATT&CK)
| Tactic | Technique | ID | Notes |
|--------|-----------|-----|-------|
| Initial Access | Spearphishing Attachment | T1566.001 | Primary delivery method |
| Execution | PowerShell | T1059.001 | Used for download and execute |
| ... | ... | ... | ... |

### Tooling
| Tool | Type | Custom/Commodity | First Seen | Status | Notes |
|------|------|-----------------|-----------|--------|-------|
| [Tool 1] | Backdoor | Custom | 2024 | Active | Primary implant |
| Cobalt Strike | C2 | Commodity | 2023 | Active | Used with modified profiles |

### Infrastructure Patterns
- **Hosting preferences**: [Cloud providers, bulletproof hosting, compromised infrastructure]
- **Registrars**: [Preferred domain registrars]
- **TLS patterns**: [Self-signed? Let's Encrypt? Specific CAs?]
- **C2 protocols**: [HTTP/HTTPS, DNS, custom protocols]
- **IP ranges**: [Known IP blocks or ASNs]

### Campaign History
#### [Campaign 1] (YYYY-MM to YYYY-MM)
- **Targets**: [Who was targeted]
- **TTPs**: [Specific techniques used]
- **Outcome**: [Impact, attribution confidence]
- **References**: [Vendor reports]

### Relationships
- **Related groups**: [Parent/child groups, shared infrastructure, shared tools]
- **Overlap with**: [Groups that share TTPs or infrastructure]
- **Distinction from**: [Commonly confused groups and how to distinguish]

### Intelligence Gaps
- [What we don't know and need to collect]
- [Specific questions for future collection]

### Sources
| Date | Source | Reliability | Key Contribution |
|------|--------|-------------|-----------------|
| YYYY-MM-DD | [Source] | [Admiralty] | [What this source contributed to the profile] |
```

## Alias Mapping
Different vendors use different names for the same group:

| Vendor | Naming Convention | Example |
|--------|------------------|---------|
| Microsoft | Weather + element | Forest Blizzard |
| CrowdStrike | Animal + adjective | Fancy Bear |
| Mandiant/Google | APT + number | APT28 |
| MITRE | Group ID | G0007 |
| Kaspersky | Varies | Sofacy |
| Recorded Future | TAG-XX | TAG-110 |

Always list all known aliases and cross-reference when building profiles.

## Profile Maintenance
- Update when new campaigns are attributed
- Update when new tools are discovered
- Update when targeting patterns change
- Review quarterly for staleness
- Move concluded campaigns from Active to Historical
- Update intelligence gaps as gaps are filled or new ones identified

## Related skills

- **Ransomware-group profiles (highest leverage)** — `/lookup-ransomwarelive group <name>` and `group-profile <name>` return curated TTPs, leak-site `.onion` infrastructure, vulnerabilities exploited, and per-group IOC + YARA dumps. Use these as the *primary* feed for any ransomware actor profile, then enrich.
- **Community attribution** — `/lookup-otx pulse-search "<actor-or-alias>"` for community-tagged indicators; `/lookup-misp search-events --tag "actor=<name>"` for prior internal cataloguing
- **Build the infrastructure cluster** — `/indicator-pivoting` walks the IOC graph (hand off `pivot_candidates` from the lookups above)
- **Underground-forum and Telegram footprint** — `/darkweb-collection` for forum/channel monitoring of an actor's known aliases
- **Campaigns attributed to the actor** — `/campaign-tracking` for per-campaign records that roll up into the profile
- **Knowledge cells the profile may feed into** — `/ransomware-ecosystem`, `/initial-access-brokers`, `/infostealers`, plus any country/sector knowledge cells (e.g., `/iran-cyber-espionage`)
- **Apply rigor** — `/score-source`, `/apply-tlp`, `/confidence-language`, `/likelihood-language`, `/intelligence-writing`
