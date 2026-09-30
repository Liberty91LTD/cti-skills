---
name: ransomware-ecosystem
description: Use when the user asks about the ransomware ecosystem, RaaS dynamics, affiliate markets, attribution between groups, leak-site behaviour, or recent group activity (LockBit lineage, ALPHV/BlackCat, RansomHub, Akira, Play, Qilin, Cl0p, Medusa, etc.). Self-updating knowledge cell.
user-invocable: true
metadata:
  category: knowledge-cell
  created: 2026-04-05
  last_updated: 2026-09-29
  update_count: 1
  confidence: moderate
---

# Ransomware Ecosystem

## Executive Summary

The ransomware ecosystem operates predominantly through a Ransomware-as-a-Service (RaaS) model, where operator groups develop and maintain ransomware payloads, negotiate with victims, and manage leak sites, while affiliates — independent contractors — handle the actual intrusion, lateral movement, and deployment. This division of labor has driven the industrialization of ransomware since roughly 2019, enabling groups to scale operations far beyond what a single team could achieve. Revenue sharing typically follows a 70/30 or 80/20 split favoring the affiliate, though elite affiliates can negotiate better terms. The double-extortion model (encrypting data AND threatening to leak it) is now standard, with some groups pursuing triple extortion by adding DDoS threats or contacting victims' customers directly.

Law enforcement pressure has been continuous since 2023: Hive (January 2023), LockBit in Operation Cronos (February 2024), Phobos/8Base (February 2025), BlackSuit in Operation Checkmate (July 2025), and in 2026 a shift toward shared criminal infrastructure, with the First VPN anonymization service (May 2026) and the AudiA6 laundering service (June 2026) taken down [14][16][25][26]. Groups have also collapsed from the inside. ALPHV/BlackCat exit-scammed in March 2024, Black Basta dissolved after its internal chats leaked in February 2025, and RansomHub, the leading brand of 2024, went offline on 1 April 2025 and has not returned [11][12][18]. None of this reduced volume. Displaced affiliates moved to other programs and new brands filled the gaps.

Payments and attack volume have decoupled. Chainalysis tracked about $820 million in on-chain ransomware payments in 2025, down 8% from a revised $892 million in 2024, while claimed incidents rose about 50% to an all-time high [9]. Fewer victims pay: Chainalysis puts the 2025 payment rate at roughly 28%, Coveware reported a record-low rate in Q2 2026, with only 15% of data-exfiltration-only victims paying, and Check Point cites approximately 23% [9][10][22]. Those who do pay are paying more, with the median on-chain payment rising from $12,738 to $59,556 in 2025 [9].

As of September 2026 the ecosystem is more fragmented than at any earlier point. Check Point counted 93 active groups in Q2 2026, a record for its tracking, with the top ten accounting for 57.6% of leak-site victims, down from 71% in Q1 [22]. Qilin has been the most prolific brand for four consecutive quarters, The Gentlemen (emerged mid-2025) is close behind, and Akira, Play, INC Ransom, SafePay and DragonForce remain consistently active [22][24][27]. LockBit returned with version 5.0 in September 2025 [19][20]. Social-engineering-led intrusion (help-desk impersonation, vishing, Teams phishing) has become a leading route to extortion, used by Scattered Spider, Chaos, Silent Ransom and former Black Basta operators [10][17][18][21]. Healthcare, education, manufacturing, and critical infrastructure remain heavily targeted sectors.

## Key Actors

| Group | Status | Notable Characteristics | Peak Activity |
|-------|--------|------------------------|---------------|
| Qilin | Active | Most prolific leak-site brand for four straight quarters to Q2 2026 (279 claimed victims in Q2); absorbed RansomHub affiliates in 2025 | 2025-present |
| The Gentlemen (Storm-2697) | Active | Emerged mid-2025 as a closed group, opened as RaaS in September 2025; 90/10 split; self-propagating Go encryptor; internal data leaked in 2026 | 2025-present |
| Akira | Active | Possible Conti lineage; about $244M in claimed proceeds as of late September 2025; SonicWall and Veeam exploitation; first Nutanix AHV encryption | 2023-present |
| Play | Active | Closed group; about 900 entities affected as of May 2025 per FBI; recompiles its binary per attack; phone-based extortion | 2022-present |
| LockBit | Active (relaunched as LockBit 5.0, Sep 2025) | Disrupted by Operation Cronos (Feb 2024); LockBitSupp identified as Dmitry Khoroshev; 5.0 covers Windows, Linux and ESXi | 2022-2024 |
| DragonForce | Active | Markets itself as a "cartel"; claimed to take over RansomHub in April 2025; deployed by Scattered Spider per CISA | 2025-present |
| Cl0p | Intermittently active | Mass exploitation of enterprise software (MOVEit, GoAnywhere, Cleo, Oracle E-Business Suite in 2025); activity comes in campaign bursts | 2023, 2025-2026 |
| Medusa | Active | RaaS first identified June 2021; over 500 victims as of April 2026 per CISA; pays IABs $100 to $1M; leak-site posting has been sparse since February 2026 | 2023-present |
| INC Ransom | Active | In Rapid7's Q2 2025 and AhnLab's August 2026 top-ten lists; 952 cumulative leak-site claims | 2023-present |
| SafePay | Active | Ranked second alongside Akira in Rapid7's Q2 2025 data | 2025-present |
| Interlock | Active | First observed September 2024; ClickFix and fake-update drive-by access; Windows, Linux and FreeBSD encryptors | 2025-present |
| Chaos | Active | Emerged February 2025; Talos assesses with moderate confidence it was formed by former BlackSuit (Royal) members | 2025-present |
| Scattered Spider | Active (arrests in 2025) | Social-engineering intrusion crew, not a RaaS; uses several ransomware variants, most recently DragonForce | 2023-present |
| RansomHub | Defunct (offline since 1 Apr 2025) | Leading brand of 2024 with a 90/10 split; affiliates moved to Qilin, DragonForce and others | 2024-Mar 2025 |
| Black Basta | Defunct (early 2025) | Conti successor; last leak-site post January 2025; chats leaked February 2025; alleged leader Oleg Nefedov on EU Most Wanted list | 2022-2024 |
| Royal/BlackSuit | Disrupted (Operation Checkmate, Jul 2025) | Conti lineage; infrastructure seized 24 July 2025; members likely continued as Chaos | 2022-2025 |
| BianLian | Inactive (no leak-site posts since Mar 2025) | Shifted to exfiltration-only (no encryption) model | 2022-2024 |
| 8Base / Phobos | Disrupted (Feb 2025) | Two Phobos operators charged by DOJ; over 100 servers taken down; no 8Base posts since | 2023-2024 |
| ALPHV/BlackCat | Defunct (exit scam, Mar 2024) | Rust-based ransomware; $22M Change Healthcare payment; FBI seized leak site Dec 2023, group reclaimed it | 2022-2024 |

Status is based on vendor reporting and ransomware.live leak-site data as of 2026-09-29 [27]. Leak-site counts are actor claims, not confirmed incidents.

## Current Activity

### Qilin and The Gentlemen Lead a Fragmented Field (2025-2026)
Qilin took the top position after RansomHub disappeared and has held it since. Group-IB recorded Qilin's leak-site disclosures roughly doubling from February 2025 [11]. Check Point counted 279 Qilin leak-site victims in Q2 2026 and reported a 62% rise for The Gentlemen over the same quarter [22]. AhnLab's August 2026 data has Qilin at 167 and The Gentlemen at 112 [24]. Microsoft tracks The Gentlemen as Storm-2697 and reports a partnership with BreachForums to recruit penetration testers and initial access brokers [15]. A leak of the group's backend showed a core team of about nine people and a management panel built in about three days with AI coding assistants [22].

### LockBit 5.0 Relaunch
LockBit announced recruitment on underground forums in early September 2025 and released LockBit 5.0 with Windows, Linux and ESXi variants [19][20]. Affiliates pay a deposit of about $500 in Bitcoin for panel access [20]. Check Point identified a dozen victims in September 2025, half of them hit with the 5.0 variant [20]. ransomware.live lists 369 claims under the LockBit 5 leak site, with posts continuing through 28 September 2026 [27].

### Social Engineering as the Primary Entry Route
Coveware ranked phishing and social engineering as the leading initial access vector in Q2 2026, ahead of remote access compromise and stolen credentials, with vulnerability exploitation declining [10]. CISA's July 2025 update on Scattered Spider describes actors impersonating employees to have IT staff reset passwords and transfer MFA tokens [21]. Chaos uses spam flooding followed by voice calls and Microsoft Quick Assist [17]. Former Black Basta operators continued email bombing combined with Microsoft Teams help-desk impersonation after the brand collapsed [18].

### Cl0p Campaign Bursts
A large-scale extortion campaign under the Cl0p brand targeted Oracle E-Business Suite customers. Google Threat Intelligence Group dated zero-day exploitation of CVE-2025-61882 to as early as 9 August 2025, with extortion emails to executives starting 29 September 2025. GTIG made no formal attribution but noted overlaps with FIN11 [13]. Check Point reported that Cl0p dominated Q1 2026 and "nearly vanished" in Q2 [22]. AhnLab reported Cl0p adding 42 organizations in August 2026 after exploiting PTC Windchill and FlexPLM; this rests on a single source [24].

### Shift Toward Exfiltration-Only Operations
A number of groups, BianLian among the first, have abandoned encryption entirely in favor of pure data theft and extortion. This approach reduces operational complexity, avoids triggering endpoint detection that monitors for encryption behavior, and still provides significant leverage over victims. This trend suggests the ecosystem is optimizing for stealth and reliability over maximum disruption. The leverage is weakening, however: Coveware reported that only 15% of exfiltration-only victims paid in Q2 2026. The same quarter's average payment rose to $1.88 million while the median fell to $150,000, a gap Coveware attributes to a few large payments in data-theft cases, including Silent Ransom (Luna Moth) extortion of law firms. ShinyHunters held 12% of Coveware's Q2 2026 caseload [10].

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
| Jan-Feb 2025 | Black Basta collapse | Last leak-site post in January; internal chats leaked in February; leak site gone by end of February [18][27] |
| Feb 2025 | Phobos/8Base disruption | DOJ charged Roman Berezhnoy and Egor Glebov; over 100 servers taken down; more than 1,000 victims and over $16M in payments [16] |
| Mar 2025 | Garantex disrupted | Domains and servers seized, over $26M frozen, two administrators charged; at least $96B processed since 2019 [26] |
| Apr 2025 | RansomHub goes offline | Infrastructure down from 1 April; DragonForce claimed RansomHub had moved to its infrastructure; affiliates dispersed [11][12] |
| Jul 2025 | Arrests over UK retail attacks (M&S, Co-op, Harrods) | NCA arrested four suspects, aged 17 to 20, on 10 July 2025 [23] |
| Jul 2025 | Operation Checkmate (BlackSuit) | Four servers, nine domains and about $1.09M seized; takedown on 24 July [14] |
| Aug-Sep 2025 | Jaguar Land Rover incident | Production halted for about five weeks; Cyber Monitoring Centre estimated a £1.9B UK impact and gave no attribution [28] |
| Aug-Oct 2025 | Oracle E-Business Suite extortion (Cl0p brand) | Zero-day CVE-2025-61882 exploited before patch; emergency patch on 4 October [13] |
| Sep 2025 | LockBit 5.0 released | LockBit resumes operations with a new affiliate program [19][20] |
| Jan 2026 | Black Basta leader named | Oleg Nefedov added to EU Most Wanted and INTERPOL Red Notice lists; searches in Ukraine [29] |
| May 2026 | Operation Saffron (First VPN) | 33 servers dismantled on 19-20 May; details of 506 users shared with partner countries [25] |
| Jun 2026 | AudiA6 laundering service disrupted | Two administrators arrested and charged by DOJ; about €336M laundered since 2021 [30] |

## TTP Evolution

**Initial Access**: Ransomware groups have shifted from relying on phishing and RDP brute-forcing (2019-2021) to purchasing access from Initial Access Brokers (IABs) and exploiting zero-day/one-day vulnerabilities in edge devices (VPNs, firewalls, file transfer appliances). Credential theft via infostealers has become a primary pipeline. Since 2025, social engineering has moved to the front: help-desk impersonation, vishing, email bombing followed by Teams or Quick Assist sessions, and ClickFix prompts [10][17][21][31]. Exploitation continues against SonicWall (CVE-2024-40766), Veeam and SimpleHelp (CVE-2024-57727) [32][33]. Access is cheap: Chainalysis reports the average price of an IAB listing fell from $1,427 in Q1 2023 to $439 in Q1 2026 [9].

**Defense Evasion**: Modern ransomware operations routinely employ EDR killers (Terminator, AuKill, Poortry/Stonestop using signed driver exploits), BYOVD (Bring Your Own Vulnerable Driver) techniques, and living-off-the-land approaches. Safe Mode reboots to disable security tools remain in use.

**Lateral Movement**: Heavy reliance on legitimate tools — Cobalt Strike, Brute Ratel, Sliver for C2; Impacket, PsExec, RDP for movement; Mimikatz, SharpHound/BloodHound for credential harvesting and AD enumeration. Increasingly, groups use RMM tools (AnyDesk, ConnectWise/ScreenConnect, Splashtop) to blend with legitimate admin traffic.

**Exfiltration**: Rclone to cloud storage and custom exfiltration tools remain dominant. WinSCP, FileZilla, and MEGA uploads are common. Some groups use purpose-built exfiltration tools like BlackCat's ExMatter or Black Basta's custom tools.

**Encryption**: Modern ransomware uses intermittent encryption (encrypting portions of files) for speed, multi-threaded encryption, and targets VMware ESXi environments with Linux variants. Akira encrypted Nutanix AHV disk files for the first time in 2025 [32]. Play recompiles its binary for each attack so that hashes are unique [33]. The Gentlemen's encryptor can self-propagate across a network using PsExec, WMI, scheduled tasks, services and PowerShell remoting [15]. Rust and Go-based payloads are increasingly common for cross-platform support.

## Ecosystem & Infrastructure Patterns

**RaaS Economic Model**: The RaaS ecosystem mirrors legitimate SaaS businesses with admin panels, customer support, SLAs for decryptor delivery, and reputation management. Affiliate recruitment occurs on underground forums (Exploit, XSS, RAMP) with vetting processes. Some programs restrict targeting (no hospitals, no CIS countries) while others have fewer restrictions. The 90/10 split that RansomHub used is now offered by The Gentlemen [22]. LockBit 5.0 charges an entry deposit of about $500 [20]. Medusa pays IABs between $100 and $1 million and offers exclusive arrangements [34]. Affiliates work across brands: Microsoft tracks one affiliate, Storm-2570, deploying Qilin, DragonForce, Anubis and BERT since April 2025 with the same post-compromise toolset [35].

**Cryptocurrency Laundering**: Ransomware payments flow through mixing services (Tornado Cash — sanctioned), cross-chain bridges (Ren, THORChain), privacy coins (Monero — increasingly demanded), nested exchanges, and OTC desks. Sanctions against services like Tornado Cash, Sinbad, and ChipMixer have disrupted but not eliminated laundering. Russian-linked exchanges (Garantex — sanctioned in 2022, disrupted in March 2025) have processed significant ransomware funds [26]. The AudiA6 laundering service was taken down in June 2026 [30].

**Rebranding and Fragmentation**: When groups face law enforcement pressure or internal disputes, they rebrand rather than dissolve. Conti fragmented into Royal/BlackSuit, Black Basta, Akira, and Meow. DarkSide became BlackMatter. Since 2025: BlackSuit members likely regrouped as Chaos, Black Basta members are assessed to have moved to Cactus and BlackLock, and RansomHub affiliates moved to Qilin and DragonForce [11][17][18][36]. This pattern makes attribution challenging but relationship mapping possible through code reuse, affiliate overlap, and operational patterns.

**Victim Negotiation**: Professional negotiation via Tor chat portals is standard. Groups set ransom demands based on victim revenue (often 1-5% of annual revenue). Cyber insurance has both enabled payments and professionalized the negotiation process. Some groups use data publication timers to create urgency. Play also telephones victim organizations to threaten data release [33]. Payment rates are at record lows [9][10].

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
| Microsoft Quick Assist / Teams | Initial Access | Abused in help-desk impersonation by Chaos and former Black Basta operators [17][18] |
| MeshAgent / Atera / Splashtop | Remote Access | RMM tools used by the Storm-2570 affiliate across several RaaS brands [35] |
| s5cmd / GoodSync | Exfiltration | Seen alongside Rclone in Storm-2570 and Chaos intrusions [17][35] |

## Intelligence Gaps

- **Affiliate identity and overlap**: The extent to which top-tier affiliates operate across multiple RaaS programs simultaneously remains poorly understood. Cross-program affiliate tracking is a critical intelligence need. Microsoft's Storm-2570 reporting is one documented case; the wider picture is unknown [35].
- **True payment volumes**: Blockchain analysis captures only a portion of ransomware payments. Monero adoption and evolving laundering techniques create significant blind spots in financial intelligence.
- **Pre-ransom access dwell time**: The typical timeline between initial access purchase from IABs and ransomware deployment is not well-characterized across groups, limiting defensive window estimation.
- **State nexus**: The relationship between Russian ransomware operators and Russian intelligence services remains ambiguous. Some operators appear to have tacit permission rather than direct tasking, but the full extent of state awareness/facilitation is unclear. ReliaQuest reports that Black Basta's leader was arrested in 2024 and released through high-level connections; this is not officially confirmed [18].
- **RansomHub's end**: Why RansomHub went offline is unresolved. DragonForce claimed a takeover, Group-IB described the outage as unexplained, and no law-enforcement action has been announced [11][12].
- **Leak-site counts versus incidents**: Vendor rankings rest on actor claims. Counts differ between trackers, and groups can inflate or repost victims.
- **Medusa's current tempo**: CISA updated its advisory in August 2026 citing over 500 victims as of April 2026, while ransomware.live shows no Medusa leak-site post after 13 February 2026 [27][34]. The reason for the gap is not established.
- **Unconfirmed (September 2026)**: A press report that Cl0p's leak-site server was breached by ShinyHunters could not be opened or corroborated in this refresh. Hunters International's reported shutdown and rebrand were not verified either.
- **Jaguar Land Rover attribution**: No authoritative public attribution was found [28].
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
9. Chainalysis - "Crypto Ransomware: 2026 Crypto Crime Report" (26 February 2026) — https://www.chainalysis.com/blog/crypto-ransomware-2026/
10. Coveware by Veeam - "Adverse Cyber Extortion Outcomes Happen More Often Than Victims Are Told" (Q2 2026 report, 29 July 2026) — https://www.veeam.com/blog/cyber-extortion-payment-trends-q2-2026.html
11. Group-IB - "Ransomware debris: an analysis of the RansomHub operation" (30 April 2025) — https://www.group-ib.com/blog/ransomware-debris/
12. The Hacker News - "RansomHub Went Dark April 1; Affiliates Fled to Qilin, DragonForce Claimed Control" (30 April 2025; reports GuidePoint Security findings) — https://thehackernews.com/2025/04/ransomhub-went-dark-april-1-affiliates.html
13. Google Threat Intelligence Group - "Oracle E-Business Suite Zero-Day Exploited in Widespread Extortion Campaign" (10 October 2025) — https://cloud.google.com/blog/topics/threat-intelligence/oracle-ebusiness-suite-zero-day-exploitation
14. US Department of Justice - "Justice Department Announces Coordinated Disruption Actions Against BlackSuit (Royal) Ransomware Operations" (11 August 2025) — https://www.justice.gov/opa/pr/justice-department-announces-coordinated-disruption-actions-against-blacksuit-royal
15. Microsoft Threat Intelligence - "The Gentlemen ransomware: Dissecting a self-propagating Go encryptor" (28 May 2026) — https://www.microsoft.com/en-us/security/blog/2026/05/28/the-gentlemen-ransomware-dissecting-a-self-propagating-go-encryptor/
16. US Department of Justice - "Phobos Ransomware Affiliates Arrested in Coordinated International Disruption" (10 February 2025) — https://www.justice.gov/opa/pr/phobos-ransomware-affiliates-arrested-coordinated-international-disruption
17. Cisco Talos - "Unmasking the new Chaos RaaS group attacks" (24 July 2025) — https://blog.talosintelligence.com/new-chaos-ransomware/
18. ReliaQuest - "Gone But Not Forgotten: Black Basta's Enduring Legacy" (11 June 2025) — https://reliaquest.com/blog/decline-and-legacy-of-black-basta-whats-next-ransomware-phishing/
19. Trend Micro (TrendAI) - "New LockBit 5.0 Targets Windows, Linux, ESXi" (25 September 2025) — https://www.trendaisecurity.com/en-us/resources-insights/trendai-security-blog/lockbit-5-targets-windows-linux-esxi
20. Check Point - "LockBit Returns — and It Already Has Victims" (23 October 2025) — https://blog.checkpoint.com/research/lockbit-returns-and-it-already-has-victims/
21. CISA/FBI - "Scattered Spider" advisory AA23-320A (updated 29 July 2025) — https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-320a
22. Check Point - "Ransomware Didn't Slow Down in Q2 2026. It Just Spread Out." (13 August 2026) — https://blog.checkpoint.com/security/ransomware-didnt-slow-down-in-q2-2026-it-just-spread-out
23. The Register - "NCA arrests four in connection with UK retail ransomware attacks" (10 July 2025) — https://www.theregister.com/2025/07/10/nca_arrests_four_in_connection/
24. AhnLab ASEC - "August 2026 Threat Trend Report on Ransomware" (23 September 2026) — https://asec.ahnlab.com/en/95567/
25. Help Net Security - "Authorities dismantle First VPN, used by ransomware actors" (21 May 2026; reports Europol, Eurojust and Dutch Police statements) — https://www.helpnetsecurity.com/2026/05/21/operation-saffron-first-vpn-takedown/
26. US Department of Justice - "Garantex Cryptocurrency Exchange Disrupted in International Operation" (7 March 2025) — https://www.justice.gov/opa/pr/garantex-cryptocurrency-exchange-disrupted-international-operation
27. ransomware.live - group and victim data, queried 29 September 2026 (leak-site claims) — https://www.ransomware.live/
28. Cyber Monitoring Centre - "Statement on the Jaguar Land Rover Cyber Incident" (22 October 2025) — https://cybermonitoringcentre.com/2025/10/22/cyber-monitoring-centre-statement-on-the-jaguar-land-rovercyber-incident-october-2025/
29. CyberScoop - "Black Basta's alleged ringleader identified as authorities raid homes of other members" (21 January 2026) — https://cyberscoop.com/black-basta-leader-europol-most-wanted-list/
30. The Hacker News - "Europol Disrupts AudiA6 Crypto Laundering Service Used by Ransomware Gangs" (10 June 2026; reports Europol and DOJ statements) — https://thehackernews.com/2026/06/europol-disrupts-audia6-crypto.html
31. CISA/FBI/HHS/MS-ISAC - "#StopRansomware: Interlock" AA25-203A (22 July 2025) — https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-203a
32. CISA/FBI and partners - "#StopRansomware: Akira Ransomware" AA24-109A (updated 13 November 2025) — https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-109a
33. CISA/FBI/ASD - "#StopRansomware: Play Ransomware" AA23-352A (updated 4 June 2025) — https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-352a
34. CISA/FBI/MS-ISAC - "#StopRansomware: Medusa Ransomware" AA25-071A (12 March 2025, updated 18 August 2026) — https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-071a
35. Microsoft Threat Intelligence - "Beyond the ransomware: Tracking Storm-2570's consistent tradecraft across deployments" (24 September 2026) — https://www.microsoft.com/en-us/security/blog/2026/09/24/beyond-ransomware-tracking-storm-2570-consistent-tradecraft-across-deployments/
36. Rapid7 - "Q2 2025 Ransomware Trends Analysis: Boom and Bust" (22 July 2025) — https://www.rapid7.com/blog/post/q2-2025-ransomware-trends-analysis-boom-and-bust/

## Change Log

| Date | Change | Source |
|------|--------|--------|
| 2026-04-05 | Initial creation with baseline intelligence through early 2025 | Training knowledge |
| 2026-09-29 | Refresh covering January 2025 to September 2026: corrected status of RansomHub, Black Basta, BlackSuit and BianLian; added Qilin, The Gentlemen, DragonForce, LockBit 5.0, Chaos, Interlock and others; updated payment data, law-enforcement actions and TTPs; 28 sources added | OSINT refresh |
