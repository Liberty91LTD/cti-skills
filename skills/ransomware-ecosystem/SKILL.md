---
name: ransomware-ecosystem
description: Use when the user asks about the ransomware ecosystem, RaaS dynamics, affiliate markets, attribution between groups, leak-site behaviour, or recent group activity (LockBit lineage, ALPHV/BlackCat, RansomHub, Akira, Play, Qilin, Cl0p, Medusa, etc.). Self-updating knowledge cell.
user-invocable: true
metadata:
  category: knowledge-cell
  created: 2026-04-05
  last_updated: 2026-04-05
  update_count: 0
  confidence: moderate
---

# Ransomware Ecosystem

## Executive Summary

The ransomware ecosystem operates predominantly through a Ransomware-as-a-Service (RaaS) model, where operator groups develop and maintain ransomware payloads, negotiate with victims, and manage leak sites, while affiliates — independent contractors — handle the actual intrusion, lateral movement, and deployment. This division of labor has driven the industrialization of ransomware since roughly 2019, enabling groups to scale operations far beyond what a single team could achieve. Revenue sharing typically follows a 70/30 or 80/20 split favoring the affiliate, though elite affiliates can negotiate better terms. The double-extortion model (encrypting data AND threatening to leak it) is now standard, with some groups pursuing triple extortion by adding DDoS threats or contacting victims' customers directly.

Law enforcement has achieved significant disruptions in 2023-2025, including the takedown of Hive (January 2023), the disruption of LockBit infrastructure in Operation Cronos (February 2024), the ALPHV/BlackCat exit scam following the Change Healthcare payment, and sustained pressure on Cl0p. However, the ecosystem demonstrates remarkable resilience: displaced affiliates migrate to new platforms, operators rebrand, and new RaaS programs emerge to fill gaps. The total ransomware economy is estimated at over $1 billion annually in direct payments, with substantially higher costs when accounting for downtime, remediation, and reputational damage.

The current landscape as of early 2026 features a more fragmented ecosystem following the disruptions of the major groups. RansomHub emerged as a significant player absorbing former LockBit and ALPHV affiliates. Akira, Play, and Black Basta continue active operations. Smaller, more agile groups proliferate, potentially making the ecosystem harder to disrupt through single-point takedowns. Healthcare, education, manufacturing, and critical infrastructure remain heavily targeted sectors.

## Key Actors

| Group | Status | Notable Characteristics | Peak Activity |
|-------|--------|------------------------|---------------|
| LockBit | Disrupted (Feb 2024), attempted comeback | Most prolific RaaS 2022-2024; LockBitSupp identified as Dmitry Khoroshev | 2022-2024 |
| ALPHV/BlackCat | Defunct (exit scam, Mar 2024) | Rust-based ransomware; $22M Change Healthcare payment; FBI seized leak site Dec 2023, group reclaimed it | 2022-2024 |
| Cl0p | Intermittently active | Specializes in mass exploitation of file transfer vulnerabilities (MOVEit, GoAnywhere, Cleo) | 2023 |
| Play | Active | Closed affiliate model; targets Latin America and Europe heavily | 2022-present |
| Akira | Active | Emerged mid-2023; possible Conti lineage; targets SMBs and VPN vulnerabilities | 2023-present |
| Black Basta | Active | Conti successor; uses sophisticated social engineering; internal chat leaks in early 2025 | 2022-present |
| RansomHub | Active | Emerged 2024; absorbed former LockBit/ALPHV affiliates; aggressive 90/10 split to attract affiliates | 2024-present |
| Medusa | Active | Increasing activity through 2024-2025; targets education sector | 2023-present |
| Royal/BlackSuit | Active | Conti lineage; rebranded from Royal to BlackSuit | 2022-present |
| BianLian | Active | Shifted to exfiltration-only (no encryption) model | 2022-present |

## Current Activity

### RansomHub's Rise as Ecosystem Leader (2024-2025)
Following the disruptions of LockBit and ALPHV/BlackCat, RansomHub rapidly filled the vacuum by offering affiliates an extremely generous 90/10 revenue split and fewer restrictions on targeting. The group attracted experienced affiliates displaced from defunct operations, enabling rapid scaling. RansomHub demonstrated sophisticated operations including exploitation of recent CVEs and the use of EDR-killing tools.

### Shift Toward Exfiltration-Only Operations
An increasing number of groups, led by BianLian and followed by others, have abandoned encryption entirely in favor of pure data theft and extortion. This approach reduces operational complexity, avoids triggering endpoint detection that monitors for encryption behavior, and still provides significant leverage over victims. This trend suggests the ecosystem is optimizing for stealth and reliability over maximum disruption.

### Healthcare Sector Escalation
The Change Healthcare attack (February 2024) demonstrated the catastrophic potential of ransomware against healthcare infrastructure, disrupting prescription processing for millions. Despite increased scrutiny, healthcare targeting has continued, with groups exploiting the sector's high willingness to pay and complex, often outdated IT environments.

## Historical Events

| Date | Event | Impact |
|------|-------|--------|
| May 2019 | Baltimore city ransomware attack (RobbinHood) | $18M+ in damages; highlighted municipal vulnerability |
| May 2021 | Colonial Pipeline (DarkSide) | Fuel shortages in US Southeast; $4.4M ransom (partially recovered); triggered executive order on cybersecurity |
| Jul 2021 | Kaseya VSA attack (REvil) | 1,500+ businesses affected via supply chain; $70M ransom demand |
| Jan 2022 | Conti internal leaks | 60,000+ messages exposed Conti operations; accelerated group's fragmentation into Akira, Royal, Black Basta, etc. |
| Jan 2023 | Hive takedown | FBI infiltrated Hive for 7 months, saved $130M in ransom demands, seized infrastructure |
| Jun 2023 | MOVEit exploitation (Cl0p) | 2,500+ organizations affected; estimated $10B+ in total damages |
| Feb 2024 | Operation Cronos (LockBit) | NCA/FBI/Europol seized LockBit infrastructure, obtained decryption keys, identified LockBitSupp |
| Feb 2024 | Change Healthcare (ALPHV/BlackCat) | $22M ransom paid; ALPHV exit scammed affiliate; disrupted US healthcare billing nationwide |
| Dec 2024 | Continued law enforcement pressure | Multiple arrests of ransomware affiliates across Europe and North America |

## TTP Evolution

**Initial Access**: Ransomware groups have shifted from relying on phishing and RDP brute-forcing (2019-2021) to purchasing access from Initial Access Brokers (IABs) and exploiting zero-day/one-day vulnerabilities in edge devices (VPNs, firewalls, file transfer appliances). Credential theft via infostealers has become a primary pipeline.

**Defense Evasion**: Modern ransomware operations routinely employ EDR killers (Terminator, AuKill, Poortry/Stonestop using signed driver exploits), BYOVD (Bring Your Own Vulnerable Driver) techniques, and living-off-the-land approaches. Safe Mode reboots to disable security tools remain in use.

**Lateral Movement**: Heavy reliance on legitimate tools — Cobalt Strike, Brute Ratel, Sliver for C2; Impacket, PsExec, RDP for movement; Mimikatz, SharpHound/BloodHound for credential harvesting and AD enumeration. Increasingly, groups use RMM tools (AnyDesk, ConnectWise/ScreenConnect, Splashtop) to blend with legitimate admin traffic.

**Exfiltration**: Rclone to cloud storage and custom exfiltration tools remain dominant. WinSCP, FileZilla, and MEGA uploads are common. Some groups use purpose-built exfiltration tools like BlackCat's ExMatter or Black Basta's custom tools.

**Encryption**: Modern ransomware uses intermittent encryption (encrypting portions of files) for speed, multi-threaded encryption, and targets VMware ESXi environments with Linux variants. Rust and Go-based payloads are increasingly common for cross-platform support.

## Ecosystem & Infrastructure Patterns

**RaaS Economic Model**: The RaaS ecosystem mirrors legitimate SaaS businesses with admin panels, customer support, SLAs for decryptor delivery, and reputation management. Affiliate recruitment occurs on underground forums (Exploit, XSS, RAMP) with vetting processes. Some programs restrict targeting (no hospitals, no CIS countries) while others have fewer restrictions.

**Cryptocurrency Laundering**: Ransomware payments flow through mixing services (Tornado Cash — sanctioned), cross-chain bridges (Ren, THORChain), privacy coins (Monero — increasingly demanded), nested exchanges, and OTC desks. Sanctions against services like Tornado Cash, Sinbad, and ChipMixer have disrupted but not eliminated laundering. Russian-linked exchanges (Garantex — sanctioned) have processed significant ransomware funds.

**Rebranding and Fragmentation**: When groups face law enforcement pressure or internal disputes, they rebrand rather than dissolve. Conti fragmented into Royal/BlackSuit, Black Basta, Akira, and Meow. DarkSide became BlackMatter. This pattern makes attribution challenging but relationship mapping possible through code reuse, affiliate overlap, and operational patterns.

**Victim Negotiation**: Professional negotiation via Tor chat portals is standard. Groups set ransom demands based on victim revenue (often 1-5% of annual revenue). Cyber insurance has both enabled payments and professionalized the negotiation process. Some groups use data publication timers to create urgency.

## Tooling

| Tool | Category | Usage |
|------|----------|-------|
| Cobalt Strike | C2 Framework | Most common post-exploitation framework; cracked versions widespread |
| Brute Ratel C4 | C2 Framework | Growing adoption as CS alternative; better EDR evasion |
| Sliver | C2 Framework | Open-source; increasingly adopted by multiple groups |
| Mimikatz | Credential Theft | Standard for Windows credential dumping |
| BloodHound | AD Enumeration | Maps Active Directory attack paths |
| Rclone | Exfiltration | Cloud storage sync for data theft |
| AnyDesk/ScreenConnect | Remote Access | Legitimate RMM tools used for persistent access |
| Terminator/AuKill | EDR Killer | BYOVD-based EDR/AV disabling tools |
| PsExec/Impacket | Lateral Movement | Remote execution across Windows networks |
| Mega.nz | Exfiltration | Cloud storage for staging stolen data |

## Intelligence Gaps

- **Affiliate identity and overlap**: The extent to which top-tier affiliates operate across multiple RaaS programs simultaneously remains poorly understood. Cross-program affiliate tracking is a critical intelligence need.
- **True payment volumes**: Blockchain analysis captures only a portion of ransomware payments. Monero adoption and evolving laundering techniques create significant blind spots in financial intelligence.
- **Pre-ransom access dwell time**: The typical timeline between initial access purchase from IABs and ransomware deployment is not well-characterized across groups, limiting defensive window estimation.
- **State nexus**: The relationship between Russian ransomware operators and Russian intelligence services remains ambiguous. Some operators appear to have tacit permission rather than direct tasking, but the full extent of state awareness/facilitation is unclear.
- **Victim non-reporting**: A substantial percentage of ransomware incidents go unreported, skewing both volume statistics and sector targeting analysis.

## Sources & References

1. CISA - "#StopRansomware" Advisory Series (ongoing) — https://www.cisa.gov/stopransomware
2. Chainalysis - "2024 Crypto Crime Report: Ransomware" — https://www.chainalysis.com/blog/ransomware-2024/
3. Europol - "Internet Organised Crime Threat Assessment (IOCTA)" — https://www.europol.europa.eu/iocta-report
4. NCA - "Operation Cronos: LockBit Disruption" (February 2024) — https://www.nationalcrimeagency.gov.uk/
5. Mandiant - "Ransomware Rebrand: Tracking Cluster Transformations" — https://www.mandiant.com/resources
6. Recorded Future - "2024 Annual Ransomware Report" — https://www.recordedfuture.com/research
7. Coveware - "Quarterly Ransomware Reports" — https://www.coveware.com/blog
8. Microsoft - "Digital Defense Report 2024" — https://www.microsoft.com/en-us/security/security-insider/microsoft-digital-defense-report-2024

## Change Log

| Date | Change | Source |
|------|--------|--------|
| 2026-04-05 | Initial creation with baseline intelligence through early 2025 | Training knowledge |
