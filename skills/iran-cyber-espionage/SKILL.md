---
name: iran-cyber-espionage
description: Use when the user asks about Iranian state-sponsored cyber operations or specific IRGC/MOIS-aligned actors (APT35/Charming Kitten, APT34/OilRig, MuddyWater, Imperial Kitten, etc.), wiper campaigns, front-group hacktivist personas (Handala, Cyber Av3ngers), or anti-Iran operations such as Predatory Sparrow. Self-updating knowledge cell.
user-invocable: true
metadata:
  category: knowledge-cell
  created: 2026-04-05
  last_updated: 2026-09-29
  update_count: 1
  confidence: moderate
---

# Iran Cyber Espionage Knowledge Cell

## Executive Summary

Iran's state-sponsored cyber operations are conducted primarily by two organizations: the Islamic Revolutionary Guard Corps (IRGC) and the Ministry of Intelligence and Security (MOIS). IRGC-affiliated groups (APT33, APT35/APT42, Nimbus Manticore/UNC1549, Imperial Kitten, CyberAv3ngers) cover espionage against defense, aerospace and policy targets and attacks on operational technology. MOIS-affiliated groups (APT34/OilRig, MuddyWater, Scarred Manticore, Void Manticore, Cavern Manticore) run sustained espionage against government, telecom and IT providers in the Middle East, and, through Void Manticore's Handala Hack persona, destructive and hack-and-leak operations.

Since this cell was seeded, Iranian cyber activity has been shaped by two wars. During the June 2025 Israel-Iran conflict, US agencies warned of possible Iranian activity against US networks but stated they had not seen a coordinated campaign [10]. Iran itself was the victim of destructive attacks claimed by Predatory Sparrow against Bank Sepah and the Nobitex exchange [11][12]. On 28 February 2026 the United States and Israel began a joint offensive against Iran (Operation Epic Fury / Operation Roaring Lion) [13][14]. A ceasefire announced on 7 April 2026 was declared over on 9 July 2026 [14]. This second conflict brought highly disruptive Iranian-linked activity against US organizations: the 11 March 2026 wipe of Stryker Corporation's managed devices, claimed by Handala [15][16][17], and exploitation of internet-exposed PLCs in US water, energy and government facilities [18][19].

Three shifts stand out. First, destructive operations no longer depend on wiper malware: the Stryker incident used the built-in wipe function of a cloud endpoint management platform [17], and Void Manticore also wipes by hand over RDP or with legitimate disk-encryption software [15]. Second, MOIS actors have retooled. MuddyWater moved from broad abuse of remote management tools to a series of custom backdoors, including Rust implants with Telegram command and control [20][21][22][23]. Third, vendors report AI-assisted malware development by MuddyWater, Void Manticore and Nimbus Manticore [15][23][25]. Long-running social engineering by APT35/APT42 and fake-recruiter operations against aerospace and defense continue [24][25][26][27][28]. US law enforcement and sanctions action against Iranian operators resumed in August 2026 [29][30].

## Key Actors

Status reflects public reporting opened for the 2026-09-29 refresh. "Not confirmed" means no 2025-2026 primary reporting was reviewed, not that the actor is inactive.

| Threat Actor | Aliases | Attribution | Primary Targets | Status |
|---|---|---|---|---|
| APT33 | Elfin, Peach Sandstorm, Refined Kitten, Holmium | IRGC | Satellite, communications, oil and gas, government, defense (U.S., UAE) | Not confirmed; last primary reporting reviewed is August 2024 [9] |
| APT34 | OilRig, Hazel Sandstorm, Helix Kitten, Crambus; Check Point describes Lyceum as an OilRig subgroup [34] | MOIS | Government, financial, telecom (Gulf states, Middle East, Israel) | Active; joint sub-campaign with MuddyWater in January-February 2025 [22] |
| APT35 / APT42 | Charming Kitten, Mint Sandstorm, Phosphorus, TA453, Educated Manticore | IRGC Intelligence Organization | Academics, journalists, security researchers, officials, dissidents | Active; internal documents leaked from 30 September 2025 [24][31] |
| MuddyWater | Mercury, Mango Sandstorm, Static Kitten, Seedworm | MOIS | Government, telecom, energy, critical infrastructure (MENA, Israel, Europe, U.S.) | Active; heavily retooled 2025-2026 [20][21][22][23] |
| Void Manticore | Handala Hack, Karma, Homeland Justice, Banished Kitten, Red Sandstorm, Storm-0842, COBALT MYSTIQUE | MOIS | Israel, Albania, U.S. enterprises, Iranian dissidents | Active; most visible destructive actor of 2026 [15][32][33] |
| Scarred Manticore | DEV-0861 | MOIS | Telecom, government (Middle East) | Active; linked to initial access preceding Void Manticore operations [15][33] |
| Cavern Manticore | Links to MuddyWater and Lyceum | MOIS-linked | Israeli government and IT providers | Active; tracked by Check Point since early 2026 [34] |
| Nimbus Manticore | UNC1549, Smoke Sandstorm, Screening Serpens, "Iranian Dream Job" | IRGC-affiliated | Aerospace, defense, aviation, telecom (Middle East, Europe, U.S.) | Active [25][26][27][28] |
| UNC6446 | None confirmed | Iran-nexus | Aerospace and defense (U.S., Middle East) | Active per Google, February 2026 [28] |
| Imperial Kitten | Tortoiseshell, Crimson Sandstorm | IRGC | Maritime, defense, technology, logistics | Active; linked by Amazon to reconnaissance preceding a missile strike [35] |
| CyberAv3ngers | Shahid Kaveh Group | IRGC Cyber Electronic Command | Internet-exposed PLCs and HMIs in water, energy, government facilities | Active; named in AA26-097A in connection with earlier PLC activity [18] |
| Mabna Institute | Silent Librarian, Cobalt Dickens, TA407 | IRGC (per reported DOJ charges) | Universities, companies, government agencies | 17 people reported charged 18 August 2026 [29] |
| Fox Kitten / Pay2Key.I2P | Pay2Key | Iran-nexus; linked by Morphisec | Israel, U.S. and other Western organizations (ransomware) | Ransomware-as-a-service re-emerged February 2025 [36] |
| Moses Staff | Marigold Sandstorm | IRGC-linked | Israeli organizations | Not confirmed |
| Agrius | Pink Sandstorm, DEV-0227 | MOIS-linked | Israel | Not confirmed |
| Cotton Sandstorm | Neptunium, Emennet Pasargad | IRGC-linked | Election infrastructure, media, influence operations | Not confirmed |

Predatory Sparrow (Gonjeshke Darande) is not an Iranian actor. It attacks Iranian targets and is widely reported as linked to Israel [11][12]. It is covered here because its operations shape Iranian retaliation.

## Active Campaigns

### Void Manticore / Handala Destructive and Hack-and-Leak Operations (2023-Present)

Check Point attributes the Handala Hack persona to Void Manticore, an actor it links to the MOIS, alongside the Karma persona (likely replaced by Handala) and Homeland Justice (used against Albania since mid-2022) [15]. Initial access relies on compromised VPN accounts, brute forcing of VPN infrastructure, and compromise of IT and service providers to reach their customers. Operators move laterally by hand over RDP and tunnel with NetBird. Destruction uses a custom MBR-based wiper, a PowerShell wiper that Check Point describes as AI-assisted, VeraCrypt, and manual deletion [15]. After Iran's internet shutdown in January 2026, Check Point saw the actor connect from Starlink IP ranges and directly from Iranian IP addresses, a decline in operational security [15].

On 11 March 2026 Stryker Corporation, a US medical technology company, suffered an attack on its Microsoft environment [16]. Press reporting states that the attackers compromised an administrator account, created a new Global Administrator account, and used the Microsoft Intune wipe command against nearly 80,000 devices, with no malware deployed [17]. Handala claimed responsibility and claimed the theft of 50 terabytes of data [17]. Check Point lists Stryker among Handala's targets [15]. CISA's alert of 18 March 2026 names Stryker but does not name an actor [16].

Separately, Group-IB attributes with moderate confidence a surveillance campaign against Iranian dissidents, journalists and government opponents to the same actor. It uses the HEAVYGRAM backdoor, controlled through Telegram bots, and the CRUDEEXCLUDE utility, with samples dating back to September 2023 [32].

### PLC Exploitation in US Critical Infrastructure (2026-Present)

On 7 April 2026 the FBI, CISA, NSA, EPA, DOE, US Cyber Command's Cyber National Mission Force and Treasury published advisory AA26-097A on Iranian-affiliated actors exploiting internet-exposed PLCs in the government services, water and wastewater, and energy sectors. Affected devices include Rockwell Automation/Allen-Bradley, Schneider Electric and Siemens controllers. The actors modified PLC project files and manipulated data shown on HMI and SCADA displays, causing operational disruption and financial loss. The advisory was updated on 22 July 2026 with guidance on detecting malicious changes to reusable code modules [18]. The advisory attributes the activity to an Iranian-affiliated APT group and links previously reported activity to CyberAv3ngers [18].

On 26-27 July 2026, more than 30 community water systems in Minnesota were attacked, with further incidents in Georgia, New Jersey and other states; press reporting counts at least 12 states. Effects included temporary disruption, loss of water pressure and a brief boil-water advisory in Georgia. Authorities suspect Iran-nexus groups but attribution is not settled: Minnesota officials said it was not clear that one actor carried out all the attacks, and a persona called APT Iran claimed credit and said it worked with CyberAv3ngers [19].

### MuddyWater Custom Tooling Campaigns (2025-Present)

Group-IB reported in September 2025 that MuddyWater had significantly reduced its broad RMM-based intrusions in favor of targeted operations with custom backdoors (BugSleep, StealthCache, Phoenix) and the Fooder loader [20]. A campaign that began on 19 August 2025 used a compromised mailbox, accessed through a commercial VPN, to send macro-enabled documents to more than 100 government entities across the Middle East and North Africa, delivering Phoenix version 4, a browser credential stealer, and the PDQ and Action1 RMM tools [21]. ESET documented a campaign from 30 September 2024 to 18 March 2025 against Israeli organizations and one Egyptian target using the MuddyViper backdoor, and a joint sub-campaign with OilRig in January-February 2025. ESET suggests MuddyWater may act as an initial access broker for other Iran-aligned groups [22]. Operation Olalampo, first observed on 26 January 2026, targeted the MENA region with the Rust-based CHAR backdoor (controlled by a Telegram bot), GhostFetch, GhostBackDoor and HTTP_VIP, and included attempts to exploit recently disclosed vulnerabilities on public-facing servers [23].

### Nimbus Manticore / UNC1549 Aerospace and Defense Targeting (2025-Present)

Check Point reported in September 2025 that this actor, which overlaps with UNC1549 and Smoke Sandstorm, had extended fake-recruiter operations to Western Europe, particularly Denmark, Sweden and Portugal, using fake career portals, multi-stage DLL side-loading, and the MiniJunk backdoor and MiniBrowse stealer [26]. In 2026 Check Point recorded three waves (February, the February-March war period, and April after the ceasefire) with wider targeting that included US aviation companies, a new backdoor named MiniFast, AppDomain hijacking, a trojanized Zoom installer and SEO poisoning [25]. Unit 42 tracks the same actor as Screening Serpens and documented MiniJunk V2 and MiniUpdate between mid-February and April 2026 [27]. Google reports that UNC1549 also reaches defense targets through third-party suppliers and legitimate remote access services, and uses the CRASHPAD credential theft tool [28].

### APT35/Charming Kitten Academic, Policy and Security Researcher Targeting (2023-Present)

APT35 maintains persistent social engineering campaigns against academics, think tank researchers, journalists, and current and former officials in the U.S., U.K., and Israel, building trust over weeks through email, LinkedIn and WhatsApp before delivering a credential harvesting link or malware. In 2024, the group compromised email accounts associated with the Trump campaign. Check Point reported that from mid-June 2025 the group (tracked as Educated Manticore) targeted Israeli journalists, cyber security experts and computer science professors, posing as assistants to technology executives. The supporting phishing kit, in use since January 2025, is a React single-page application that relays passwords and two-factor codes in real time and logs keystrokes [24].

### Cavern Manticore Targeting of Israeli IT Providers and Government (2026-Present)

Check Point has tracked this MOIS-linked cluster since early 2026. It uses Cavern, a modular .NET command-and-control framework whose components are compiled in three different formats to hinder analysis. In multiple intrusions the initial foothold came through RMM software already deployed at the victim; one recovered chain began with a SysAid software update feature [34].

## Historical Campaigns

### Shamoon/Disttrack Attacks (2012, 2016-2017)

The original Shamoon attack in 2012, attributed to Iran, destroyed approximately 35,000 workstations at Saudi Aramco by overwriting the master boot record. Follow-on Shamoon 2 attacks in 2016-2017 targeted additional Saudi and Gulf state organizations in the energy and government sectors. The attacks established wiper malware as a core element of Iranian cyber strategy.

### APT34 Tool Leaks and Operational Exposure (2019)

In 2019, an entity calling itself "Lab Dookhtegan" publicly leaked APT34's hacking tools, infrastructure details, and victim data on Telegram, and exposed the identities of alleged MOIS officers. APT34 continued operations with retooled capabilities.

### MuddyWater Telecommunications Targeting in the Middle East (2020-2023)

MuddyWater conducted sustained campaigns against telecommunications providers and government organizations across the Middle East, Turkey, and South Asia, using spear-phishing, legitimate remote management tools (Atera, SimpleHelp), and PowerShell-based implants such as PowGoop and MuddyC2Go. The group has since reduced its reliance on RMM tools (see Active Campaigns) [20].

### Peach Sandstorm/APT33 Password Spray and Tickler Operations (2023-2024)

Microsoft reported password spray attacks against thousands of organizations from February 2023 and, between April and July 2024, deployment of the custom Tickler backdoor against satellite, communications equipment, oil and gas, and government targets in the U.S. and UAE, with command and control hosted in attacker-created Azure tenants [1][9]. No 2025-2026 primary reporting on this actor was reviewed in the latest refresh, so the campaign is listed here without a confirmed end date.

### Post-October 2023 Destructive Operations Against Israel (2023-2024)

Multiple Iranian groups intensified destructive operations against Israeli targets after October 2023, using wipers and ransomware as destructive tools and amplifying results through Telegram channels and hacktivist personas. MITRE ATT&CK attributes use of the BiBi wiper to Void Manticore [33]. The Void Manticore part of this activity continues under the Handala persona (see Active Campaigns).

### June 2025 Israel-Iran Conflict (June 2025)

Predatory Sparrow claimed a destructive attack on Bank Sepah, reported on 17 June 2025, which disrupted account access, withdrawals and card payments [11]. It then claimed an attack on the Nobitex cryptocurrency exchange in which more than $90 million in assets was sent to wallets with no accessible keys and source code was exposed [12]. On 30 June 2025 CISA, FBI, DC3 and NSA warned that Iranian actors may target US networks, with defense industrial base companies linked to Israeli firms at increased risk [10]. Amazon later reported that MuddyWater accessed a server holding live CCTV streams from Jerusalem on 17 June 2025, days before missile attacks on the city on 23 June [35].

### Charming Kitten Internal Document Leak (September-October 2025)

On 30 September 2025 a large cache of internal documents attributed to Charming Kitten surfaced on a public platform. Secondary reporting, not verified in this refresh, names the publishing account as KittenBusters. Gatewatcher's review describes attack playbooks, campaign management records and timesheets, network diagrams, target lists and vulnerability scan reports [31]. The identity of the leaker is not established.

## TTP Evolution

Iranian cyber operations have evolved across multiple dimensions:

- **Social Engineering Sophistication**: APT35 invests weeks in building trust with targets. Nimbus Manticore and UNC6446 use fake recruiters, career portals and resume-builder applications against aerospace and defense staff [26][28].
- **Real-Time MFA Relay**: APT35's phishing kit captures passwords and one-time codes and relays them to the legitimate service during the session [24].
- **Destruction Without Malware**: Abuse of cloud endpoint management (the Intune wipe at Stryker), legitimate disk encryption, and manual deletion over RDP replace or supplement custom wipers [15][17].
- **Ransomware as Destruction and Proxy**: Iranian groups deploy ransomware as a destructive tool. Pay2Key.I2P offers affiliates an 80 percent share for attacks on Iran's adversaries [36].
- **Hacktivist Personas**: State actors operate named personas (Handala, Karma, Homeland Justice) to claim attacks and leak data [15]. Unit 42 also recorded many self-declared hacktivist groups, including pro-Russian ones, active during the 2026 conflict [13].
- **OT Targeting**: Exploitation of internet-exposed PLCs moved from defacement-style activity to modification of project files and manipulation of HMI data [18].
- **Custom Tooling Over RMM**: MuddyWater reduced broad RMM abuse in favor of custom backdoors, then Rust implants [20][23]. RMM abuse persists as an access vector: Cavern Manticore entered through RMM software already present at victims [34].
- **AI-Assisted Development**: Check Point and Group-IB report signs of AI-generated code in Void Manticore, Nimbus Manticore and MuddyWater tooling [15][23][25].
- **Third-Party and Supply Chain Access**: Void Manticore and UNC1549 pivot from IT providers and suppliers to their customers [15][28].
- **Inter-Group Handoffs**: Scarred Manticore access preceding Void Manticore destruction, and the MuddyWater-OilRig joint sub-campaign, indicate cooperation among MOIS actors [22][33].
- **Cyber-Enabled Kinetic Targeting**: Amazon documented Imperial Kitten's searches of ship AIS data days before a Houthi missile strike on the same vessel (February 2024) and MuddyWater's access to Jerusalem CCTV before missile attacks (June 2025) [35].
- **Cloud Targeting**: APT33 built expertise in cloud identity attacks and hosted command and control in attacker-created Azure tenants [9].

## Infrastructure Patterns

- Adversary-controlled domains mimicking webmail and meeting services (Gmail, Google Meet) for credential harvesting; Check Point counted more than 130 domains in one APT35 cluster [24]
- Fake career portals and spoofed company sites for malware delivery; command and control routed through Azure-hosted domains [26][27]
- MuddyWater hosting spread across AWS, Cloudflare, M247, OVH and bulletproof providers, with Namecheap registration and Let's Encrypt or Google Trust Services certificates [20]
- Telegram bots, users and groups for command and control and exfiltration (MuddyWater CHAR, Void Manticore HEAVYGRAM) [23][32]
- Commercial VPN services for operator access; compromised mailboxes used to send phishing [21]
- Starlink ranges and direct Iranian IP addresses used by Void Manticore after the January 2026 internet shutdown [15]
- Commercial tunneling and mesh tools (NetBird) inside victim networks [15]
- Cloud storage services for data exfiltration and dynamic DNS for rapid infrastructure rotation

## Tooling

| Tool | Type | Associated Actors | Notes |
|---|---|---|---|
| Shamoon/Disttrack | Wiper | APT33 | MBR wiper; used in destructive attacks on Gulf energy sector |
| BiBi Wiper | Wiper (Linux/Windows) | Void Manticore | Deployed against Israeli targets after October 2023 [33] |
| Handala Wiper / PowerShell Wiper | Wiper | Void Manticore | MBR-based executable and a script Check Point describes as AI-assisted [15] |
| Microsoft Intune, VeraCrypt | Legitimate software abused for destruction | Handala (claimed), Void Manticore | Remote wipe at Stryker; disk encryption as a wiper [15][17] |
| HEAVYGRAM / CRUDEEXCLUDE | Backdoor / Defender-exclusion utility | Void Manticore (moderate confidence) | Telegram-controlled surveillance of dissidents [32] |
| Apostle/Fantasy | Ransomware/wiper | Agrius | Ransomware facade concealing destructive intent |
| POWERSTAR | Backdoor | APT35 | PowerShell-based backdoor with modular capabilities |
| BellaCiao | Backdoor | APT35 | .NET implant; tailored per victim |
| Sponsor | Backdoor | APT35 | Stores configuration in Windows registry |
| MuddyC2Go | C2 framework | MuddyWater | Go-based C2 replacing older PowGoop framework |
| BugSleep, StealthCache, Phoenix | Backdoors | MuddyWater | Custom implants of 2024-2025; Phoenix v4 used against 100+ government entities [20][21] |
| MuddyViper / Fooder | Backdoor / loader | MuddyWater | C/C++ backdoor; loader masquerades as a Snake game [22] |
| CHAR, GhostFetch, GhostBackDoor, HTTP_VIP | Rust backdoor, downloaders, implant | MuddyWater | Operation Olalampo, January 2026 [23] |
| Atera, SimpleHelp, PDQ, Action1, Syncro | RMM (legitimate) | MuddyWater | Still used, but less broadly than before 2025 [20][21][22] |
| Cavern | Modular .NET C2 framework | Cavern Manticore | Agent plus file, SQL, LDAP, network and tunnel modules [34] |
| LIONTAIL | Backdoor | Scarred Manticore | Passive implant using Windows HTTP stack driver |
| MiniJunk, MiniBrowse, MiniFast, MiniUpdate | Backdoors / stealer | Nimbus Manticore (UNC1549) | Successors to Minibike; delivered by side-loading and AppDomain hijacking [25][26][27] |
| CRASHPAD | Credential theft tool | UNC1549 | Reported by Google [28] |
| Tickler | Backdoor | APT33 | Multi-stage backdoor reported by Microsoft in August 2024 [9] |
| FalseFont | Backdoor | APT33 | Targets defense industrial base; carried over from the original cell, not re-verified |
| Pay2Key.I2P | Ransomware-as-a-service | Fox Kitten-linked | Hosted on I2P; tied to Mimic ransomware; Linux build added June 2025 [36] |

## Intelligence Gaps

- **Attribution of the July 2026 water system attacks**: Authorities suspect Iran-nexus actors, but whether one group or several was responsible, and the role of the APT Iran persona, is not settled [19].
- **Stryker intrusion details**: The initial access vector and device count rest on press reporting and the actor's own claims. No government attribution was found in the sources reviewed [16][17].
- **Mabna Institute charges**: The reported August 2026 charges against 17 people were confirmed through press only; the DOJ release could not be retrieved. The reported victim figures match those of the 2018 Mabna indictment, so whether this is a new or superseding case is unconfirmed [29]. Treasury's designations of 24 August 2026 describe a group working for the MOIS, while the reported DOJ case cites the IRGC; the relationship between the two actions is unclear [29][30].
- **Charming Kitten leak**: Who published the leak and whether all leaked material is authentic are not established [31].
- **Unverified leads**: Platform and press leads seen but not verified against a primary source in this refresh include a Handala claim against California Water Service (June 2026), a vendor attribution of a March 2026 LA Metro intrusion to an Iranian persona, and reports of Iranian exploitation of a VPN vulnerability. Treat as unconfirmed.
- **Status of APT33, Agrius, Moses Staff and Cotton Sandstorm**: No 2025-2026 primary reporting was reviewed.
- **IRGC-MOIS coordination**: Cooperation among MOIS groups is now documented [22][33]; coordination between the IRGC and MOIS remains poorly understood.
- **Contractor ecosystem**: Iran's use of private companies and front organizations (e.g., Emennet Pasargad, Najee Technology, Afkar System) requires further mapping.
- **Effect of the conflict on capability**: How strikes, leadership losses and internet shutdowns inside Iran have affected operator capacity is unclear. Check Point observed reduced operational security in one actor [15].
- **Posture after the ceasefire collapse**: Whether the operational tempo seen in March-July 2026 is sustained after 9 July 2026 is not yet documented in the sources reviewed.

## Live enrichment

When CrowdStrike Falcon Intelligence credentials are configured (`$CROWDSTRIKE_CLIENT_ID`), pull live vendor intelligence to keep this cell current and to answer specific actor questions:

- **Actor profile** — `/lookup-crowdstrike actor "Charming Kitten"` (origins, target countries/industries, motivations, capability, aliases)
- **TTPs** — `/lookup-crowdstrike ttps "Charming Kitten"` → ATT&CK technique IDs; resolve against `/mitre-attack`
- **Latest reporting** — `/lookup-crowdstrike reports --actor "Imperial Kitten" --latest`
- **Actor population** — `/lookup-crowdstrike actors --origin iran` to enumerate Iran-attributed adversaries CrowdStrike tracks

Route through `/threat-actor-profiling` for a full structured profile. CrowdStrike report bodies are typically TLP:AMBER+ — cite report IDs internally, do not redistribute.

## Sources & References

1. Microsoft Threat Intelligence: "Peach Sandstorm password spray campaigns enable intelligence collection at high-value targets" (September 2023)
2. Mandiant: "APT42: Crooked Charms, Cons, and Compromises" (September 2022)
3. CISA Advisory AA22-055A: "Iranian Government-Sponsored Actors Conduct Cyber Operations Against Global Government and Commercial Networks" (2022)
4. CrowdStrike: "Imperial Kitten Deploys Novel Malware Families in Middle East-Focused Operations" (2023)
5. Check Point Research: "Scarred Manticore's LIONTAIL: A New Passive Implant Framework" (2023)
6. FBI Flash Alert: "Iranian Cyber Group Emennet Pasargad Conducting Hack-and-Leak Operations" (2024)
7. Proofpoint: "TA453 Uses LNK Files and Mac Malware in Social Engineering Operations" (2023)
8. Recorded Future Insikt Group: "Iran's Cyber Threat Activities: Trends and Outlook" (2024)
9. Microsoft Threat Intelligence: "Peach Sandstorm deploys new custom Tickler malware in long-running intelligence gathering operations" (28 August 2024) https://www.microsoft.com/en-us/security/blog/2024/08/28/peach-sandstorm-deploys-new-custom-tickler-malware-in-long-running-intelligence-gathering-operations/
10. CISA, FBI, DC3, NSA: "Iranian Cyber Actors May Target Vulnerable US Networks and Entities of Interest" (30 June 2025) https://www.cisa.gov/resources-tools/resources/iranian-cyber-actors-may-target-vulnerable-us-networks-and-entities-interest
11. The Record: "Pro-Israel hackers claim breach of Iranian bank amid military escalation" (17 June 2025) https://therecord.media/pro-israel-hackers-claim-attack-on-iranian-bank
12. SecurityWeek: "Predatory Sparrow Burns $90 Million on Iranian Crypto Exchange in Cyber Shadow War" (19 June 2025) https://www.securityweek.com/predatory-sparrow-burns-90-million-on-iranian-crypto-exchange-in-cyber-shadow-war/
13. Palo Alto Networks Unit 42: "Threat Brief: Escalation of Cyber Risk Related to Iran" (updated 17 April 2026) https://unit42.paloaltonetworks.com/iranian-cyberattacks-2026/
14. ABC News: "How the US-Iran ceasefire and MOU broke down -- a timeline" (9 July 2026) https://abcnews.com/Politics/us-iran-ceasefire-mou-broke-timeline/story?id=134622392
15. Check Point Research: "'Handala Hack' - Unveiling Group's Modus Operandi" (12 March 2026) https://research.checkpoint.com/2026/handala-hack-unveiling-groups-modus-operandi/
16. CISA: "CISA Urges Endpoint Management System Hardening After Cyberattack Against US Organization" (18 March 2026) https://www.cisa.gov/news-events/alerts/2026/03/18/cisa-urges-endpoint-management-system-hardening-after-cyberattack-against-us-organization
17. BleepingComputer: "CISA urges US orgs to secure Microsoft Intune systems after Stryker breach" (19 March 2026) https://www.bleepingcomputer.com/news/security/cisa-warns-businesses-to-secure-microsoft-intune-systems-after-stryker-breach/
18. CISA, FBI, NSA, EPA, DOE, CNMF, Treasury: Advisory AA26-097A, "Iranian-Affiliated Cyber Actors Exploit Programmable Logic Controllers Across US Critical Infrastructure" (7 April 2026, updated 22 July 2026) https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-097a
19. Cybersecurity Dive: "What we know so far about the hacking campaign against US water systems" (20 August 2026) https://www.cybersecuritydive.com/news/what-we-know-so-far-about-the-hacking-campaign-against-us-water-systems/828374/
20. Group-IB: "Tracking MuddyWater in Action: Infrastructure, Malware and Operations during 2025" (17 September 2025) https://www.group-ib.com/blog/muddywater-infrastructure-malware/
21. Group-IB: "Unmasking MuddyWater's New Malware Toolkit Driving International Espionage" (22 October 2025) https://www.group-ib.com/blog/muddywater-espionage/
22. ESET Research: "MuddyWater: Snakes by the riverbank" (2 December 2025) https://www.welivesecurity.com/en/eset-research/muddywater-snakes-riverbank/
23. Group-IB: "Operation Olalampo: Inside MuddyWater's Latest Campaign" (20 February 2026) https://www.group-ib.com/blog/muddywater-operation-olalampo/
24. Check Point Research: "Iranian Educated Manticore Targets Leading Tech Academics" (25 June 2025) https://research.checkpoint.com/2025/iranian-educated-manticore-targets-leading-tech-academics/
25. Check Point Research: "Fast and Furious - Nimbus Manticore Operations During the Iranian Conflict" (22 May 2026) https://research.checkpoint.com/2026/fast-and-furious-nimbus-manticore-operations-during-the-iranian-conflict/
26. Check Point Research: "Nimbus Manticore Deploys New Malware Targeting Europe" (22 September 2025) https://research.checkpoint.com/2025/nimbus-manticore-deploys-new-malware-targeting-europe/
27. Palo Alto Networks Unit 42: "Tracking Iranian APT Screening Serpens' 2026 Espionage Campaigns" (22 May 2026) https://unit42.paloaltonetworks.com/tracking-iran-apt-screening-serpens/
28. Google Threat Intelligence Group: "Threats to the Defense Industrial Base" (11 February 2026) https://cloud.google.com/blog/topics/threat-intelligence/threats-to-defense-industrial-base
29. Cybersecurity Dive: "DOJ charges 17 people in Iran-backed hacking campaign against US" (18 August 2026) https://www.cybersecuritydive.com/news/doj-charges-17-iran-hacking-campaign-us-university/828212/
30. US Department of the Treasury: "Treasury Launches Unprecedented Campaign Against Iranian Regime on Economic D-Day" (24 August 2026) https://home.treasury.gov/news/press-releases/sb0613/
31. Gatewatcher: "Data breach: the operations of 'Charming Kitten' revealed" (9 October 2025) https://www.gatewatcher.com/en/lab/data-breach-the-operations-of-charming-kitten-revealed/
32. Group-IB: "HEAVYGRAM: A Telegram-based Surveillance Backdoor Linked to Handala Hack" (17 September 2026) https://www.group-ib.com/blog/heavygram-handala-hack-telegram-c2/
33. MITRE ATT&CK: "VOID MANTICORE, Group G1055" (last modified 31 July 2026) https://attack.mitre.org/groups/G1055/
34. Check Point Research: "Cavern Manticore: Exposing Iran-Linked Modular C2 Framework" (6 July 2026) https://research.checkpoint.com/2026/cavern-manticore-exposing-iran-linked-modular-c2-framework/
35. Amazon Threat Intelligence: "New Amazon Threat Intelligence findings: Nation-state actors bridging cyber and kinetic warfare" (19 November 2025) https://aws.amazon.com/blogs/security/new-amazon-threat-intelligence-findings-nation-state-actors-bridging-cyber-and-kinetic-warfare/
36. Morphisec: "Pay2Key's Resurgence: Iranian Cyber Warfare Targets the West" (8 July 2025) https://www.morphisec.com/blog/pay2key-resurgence-iranian-cyber-warfare/

## Change Log

| Date | Change | Source |
|---|---|---|
| 2026-04-05 | Initial cell creation; seeded with training knowledge through early 2025 | Training data |
| 2026-09-29 | Refresh covering January 2025 to September 2026: June 2025 and 2026 conflicts, Stryker wipe, PLC advisory AA26-097A and water system attacks, MuddyWater retooling, Nimbus Manticore, Cavern Manticore, Charming Kitten leak, August 2026 charges and sanctions. Corrected BiBi wiper attribution, replaced unverified EagleSpy reference with Tickler, moved two campaigns to Historical. Sources 9-36 added. | OSINT refresh |
