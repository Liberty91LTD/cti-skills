---
name: threat-actor-profiling
description: Use when the user asks to build or update a threat-actor profile, "tell me about actor X" / "profile actor Y", or another skill needs the canonical profile template (attribution, TTPs, campaigns, infrastructure patterns, intelligence gaps).
user-invocable: true
metadata:
  version: 1.1.0
---

# Threat Actor Profiling

A threat actor profile is a living document that consolidates everything known about a threat group. It grows over time as new intelligence is collected.

## Sourcing Before Profiling

A profile is built from claims, and each claim belongs to the source that originated it. Before any report feeds the profile:

1. **Resolve provenance.** Run `/source-provenance` on every ingested report or article. Record the primary, the chain and the `provenance_basis` (platform-resolved, script-resolved or model-judged).
2. **Dedupe by primary, not by URL.** Five outlets covering one vendor report are one source. Merge them into a single Sources row for the primary and list the outlets as "via". Count corroboration by independent primaries with separate access only.
3. **Grade per claim.** Run `/quality-of-information-check` on the primary (it calls `/claim-extraction`). Observations, attribution and assessments from the same report carry different grades. Do not give a report one grade and apply it to everything in it.
4. **Store the grade with the entity.** Every TTP row, tooling row, attribution statement and campaign entry carries the primary that supports it and the grade of the supporting claim. When two primaries support the same row, list both and keep the grades separate.

An entity with no resolved primary stays in the profile only with grade D3 or lower and the note "unresolved provenance". Grades follow the fixed rubric in `/quality-of-information-check` (`references/grading-rubric.md`).

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
| **Provenance basis** | [platform-resolved / script-resolved / model-judged (worst of the sources used)] |
| **Alias source** | [user / liberty91 / none] |

### Attribution Assessment
[Detailed attribution discussion with confidence level. Who attributes this group and based on what evidence? Where do vendors disagree?]

| Attribution statement | Primary | Stated confidence (verbatim) | Grade | Independent primaries |
|-----------------------|---------|------------------------------|-------|-----------------------|
| [Actor is linked to X] | [Org, report title, date] | ["moderate confidence" / not stated] | [e.g., B3] | [Count, and basis] |

### Targeting
**Sectors**: [List targeted sectors with evidence]
**Geographies**: [Targeted countries/regions]
**Selection criteria**: [How does this group choose targets? Opportunistic vs targeted?]
**Evolution**: [How has targeting changed over time?]

### TTPs (MITRE ATT&CK)
| Tactic | Technique | ID | Notes | Primary | Grade |
|--------|-----------|-----|-------|---------|-------|
| Initial Access | Spearphishing Attachment | T1566.001 | Primary delivery method | [Org, date] | [e.g., A2] |
| Execution | PowerShell | T1059.001 | Used for download and execute | [Org, date] | [e.g., B2] |
| ... | ... | ... | ... | ... | ... |

### Tooling
| Tool | Type | Custom/Commodity | First Seen | Status | Notes | Primary | Grade |
|------|------|-----------------|-----------|--------|-------|---------|-------|
| [Tool 1] | Backdoor | Custom | 2024 | Active | Primary implant | [Org, date] | [e.g., B2] |
| Cobalt Strike | C2 | Commodity | 2023 | Active | Used with modified profiles | [Org, date] | [e.g., A2] |

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
- **References**: [Primary reports, each with the grade of the claim it supports]

### Relationships
- **Related groups**: [Parent/child groups, shared infrastructure, shared tools]
- **Overlap with**: [Groups that share TTPs or infrastructure]
- **Distinction from**: [Commonly confused groups and how to distinguish]

### Intelligence Gaps
- [What we don't know and need to collect]
- [Specific questions for future collection]

### Sources
One row per primary. Outlets that carried the primary go in "Via".

| Date | Primary source | Via | Access | Reliability | Key Contribution |
|------|----------------|-----|--------|-------------|-----------------|
| YYYY-MM-DD | [Originating org and report title] | [Outlets, or "direct"] | [telemetry / ir_engagement / sample_analysis / osint / undisclosed] | [A-F] | [What this source contributed to the profile] |
```

Reliability in the Sources table is the primary's reliability letter. The credibility digit belongs to each claim, so the full grade sits on the entity rows above.

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

### Matching names across vendors

The naming conventions above help you recognise a vendor's name. They do not tell you that two names are the same group. Merging reports under one profile needs an alias source, and the profile states which one was used:

| Alias source | When | Label |
|--------------|------|-------|
| Your own alias file | `skills/quality-of-information-check/references/aliases.yml` is present. User-maintained, with `canonical`, `aliases` and `note` per entry. | `alias_source: user` |
| Liberty91 Threat Library | `LIBERTY91_API_KEY` is set. Resolve with `/lookup-liberty91 library threat-actors --alias "<vendor-name>"`. | `alias_source: liberty91` |
| Neither | No file and no key. | `alias_source: none` |

With `alias_source: none`, names are not matched across vendors. Reports that use a different name stay in a separate "Possibly related reporting (names not matched)" list, they do not count as corroboration, and the profile says so in the Summary and in Intelligence Gaps, naming both options above. Do not match names from memory. Hash, CVE and infrastructure overlap can still be compared directly, because those do not depend on names.

## Profile Maintenance
- Update when new campaigns are attributed
- Update when new tools are discovered
- Update when targeting patterns change
- Review quarterly for staleness
- Move concluded campaigns from Active to Historical
- Update intelligence gaps as gaps are filled or new ones identified

## Related skills

- **Vendor finished intelligence (highest leverage for state-sponsored / espionage actors)** — when CrowdStrike credentials are configured, `/lookup-crowdstrike actor "<name>"` returns the Falcon Intel adversary profile (origins, target countries/industries, motivations, capability, aliases); `/lookup-crowdstrike ttps "<name>"` returns the actor's MITRE ATT&CK technique set (feed into the TTPs section); `/lookup-crowdstrike reports --actor "<name>" --latest` surfaces the newest finished reporting. Use these as a *primary* feed for the profile, then enrich. Resolve the returned `technique_ids` against `/mitre-attack`.
- **Ransomware-group profiles (highest leverage for ransomware actors)** — `/lookup-ransomwarelive group <name>` and `group-profile <name>` return curated TTPs, leak-site `.onion` infrastructure, vulnerabilities exploited, and per-group IOC + YARA dumps. Use these as the *primary* feed for any ransomware actor profile, then enrich.
- **Community attribution** — `/lookup-otx pulse-search "<actor-or-alias>"` for community-tagged indicators; `/lookup-misp search-events --tag "actor=<name>"` for prior internal cataloguing
- **First-party catalog** — `/lookup-liberty91 library threat-actors --name "<actor>"` (or `--alias "<vendor-name>"`) resolves the actor to its canonical id; then `entity threat-actors <id>` for aliases, origin, target sectors and countries, `--section techniques` for dated ATT&CK observations (first/last observed in reporting, not a co-occurrence score), `--section threat-events` for the occurrences the actor has been named in, and `--section related` for co-occurring malware and tooling. Track the id, not the name string.
- **Internal knowledge base** — `/lookup-opencti search "<actor-or-alias>"` surfaces the intrusion sets, reports, campaigns, and malware your OpenCTI instance already links to the actor; `get <id>` walks the relationships. Check this before rebuilding a profile from scratch.
- **Build the infrastructure cluster** — `/indicator-pivoting` walks the IOC graph (hand off `pivot_candidates` from the lookups above)
- **Underground-forum and Telegram footprint** — `/darkweb-collection` for forum/channel monitoring of an actor's known aliases
- **Campaigns attributed to the actor** — `/campaign-tracking` for per-campaign records that roll up into the profile
- **Knowledge cells the profile may feed into** — `/ransomware-ecosystem`, `/initial-access-brokers`, `/infostealers`, plus any country/sector knowledge cells (e.g., `/iran-cyber-espionage`)
- **Provenance and grading** — `/source-provenance` on every ingested report, `/claim-extraction` to split it into typed claims, `/quality-of-information-check` for per-claim grades. `/source-assessment` remains the reference for the Admiralty scale itself.
- **Apply rigor** — `/score-source`, `/apply-tlp`, `/confidence-language`, `/likelihood-language`, `/intelligence-writing`
