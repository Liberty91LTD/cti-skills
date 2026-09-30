---
name: russia-cyber-espionage
description: Use when the user asks about Russian state-sponsored cyber operations or specific actors (APT28/Fancy Bear, Sandworm, Cozy Bear/APT29, Turla, GRU-affiliated hacktivist fronts like CARR/NoName057), wartime ICS/OT campaigns, or pro-RU information operations. Self-updating knowledge cell.
user-invocable: true
metadata:
  category: knowledge-cell
  created: 2026-04-05
  last_updated: 2026-09-29
  update_count: 1
  confidence: moderate
---

# Russia Cyber Espionage Knowledge Cell

## Executive Summary

Russia maintains one of the most capable and aggressive state-sponsored cyber operations programs globally, distributed across three primary intelligence services: the GRU (military intelligence), SVR (foreign intelligence), and FSB (federal security service). GRU units run the most disruptive and destructive operations and the largest credential-theft campaigns. The SVR conducts long-term espionage against governments, diplomats and cloud identity systems. The FSB runs both high-volume operations against Ukraine (Gamaredon) and selective, long-lived espionage (Turla, Center 16 network-device intrusions, Star Blizzard).

The war in Ukraine remains the center of gravity. ESET reporting covering October 2024 to March 2026 describes Sandworm deploying a succession of new wipers (ZEROLOT, Sting and others) against Ukrainian energy, government, logistics and grain-sector targets, and Gamaredon as the most active group targeting Ukraine [10][11][12]. APT28 has spent more than two years targeting Western logistics and technology companies that move aid to Ukraine [9], and Ukrainian drone manufacturers are now a recurring target for both GRU and SVR-linked operators [12][25].

Three developments since early 2025 change the picture. First, destructive activity reached a NATO member: on 29 December 2025 wipers and attacks on industrial devices hit more than 30 wind and solar farms, a combined heat and power plant and a manufacturer in Poland [14]. Attribution is contested. ESET attributes the DynoWiper malware to Sandworm with medium confidence [13], CERT Polska reports infrastructure overlap with the FSB-linked cluster known as Static Tundra or Berserk Bear [14], and in July 2026 the UK and EU member states formally attributed the attack to FSB Center 16 [15][16]. Second, Russian services are increasingly working from the network path rather than the endpoint: Turla uses an ISP-level adversary-in-the-middle position inside Russia against embassies [26], APT28 hijacked DNS on compromised home and small-office routers [35], and a Midnight Blizzard sub-cluster manipulated hotel and conference Wi-Fi captive portals [24]. Third, Western governments have moved against the ecosystem around the services: Operation Eastwood against NoName057(16) in July 2025 [39], US indictments and a joint advisory on GRU-supported hacktivist fronts in December 2025 [37][38], a US disruption of the APT28 router network in April 2026 [35], and coordinated UK and EU sanctions in July 2026 [15][17].

Cooperation between units is now documented rather than assumed. ESET assesses with high confidence that Gamaredon provided access to Turla on machines in Ukraine in 2025 [27]. A previously unknown actor, Void Blizzard (Laundry Bear), was exposed in May 2025 and was the subject of a 24-agency advisory in July 2026 [32][33].

## Key Actors

| Threat Actor | Aliases | Attribution | Primary Targets | Status |
|---|---|---|---|---|
| APT28 | Fancy Bear, Forest Blizzard, Sofacy, Sednit, Pawn Storm, BlueDelta, Strontium | GRU 85th GTsSS, Unit 26165 | Government, defense, logistics and transport, IT services (NATO states, Ukraine) | Active; router DNS-hijacking network disrupted April 2026 [35] |
| APT29 | Cozy Bear, Midnight Blizzard, The Dukes, Nobelium | SVR | Government, diplomats, technology, cloud identity, defense and drone industry | Active; Microsoft tracks sub-clusters Storm-2372 and Storm-2945 [24] |
| Sandworm | APT44, Seashell Blizzard, Iridium, Voodoo Bear, Iron Viking, Electrum | GRU GTsST, Unit 74455 | Ukrainian energy, government, logistics, grain sector; Western energy and edge infrastructure | Active |
| Turla | Secret Blizzard, Venomous Bear, Snake, Krypton, Summit | FSB (Center 16) | Government, military, diplomatic (Ukraine, Europe, embassies in Moscow) | Active; EU attributed Turla to the FSB 16th Center in July 2026 [16] |
| Static Tundra | Berserk Bear, Energetic Bear, Dragonfly, Crouching Yeti, Ghost Blizzard | FSB (Center 16) | Network devices in telecoms, higher education, manufacturing, energy; Ukraine | Active; Talos assesses Static Tundra as a likely sub-cluster of Energetic Bear [34] |
| Gamaredon | Armageddon, Primitive Bear, Aqua Blizzard, Shuckworm | FSB (Crimea) | Ukrainian government and military | Active; collaborating with Turla [27] |
| Star Blizzard | Callisto, ColdRiver, Seaborgium, UNC4057 | FSB (Center 18) | Advisors to Western governments and militaries, think tanks, journalists, NGOs | Active; shifted from credential phishing to malware in 2025 [30][31] |
| Cadet Blizzard / Ember Bear | DEV-0586, UNC2589, Frozenvista, UAC-0056 | GRU 161st Specialist Training Center, Unit 29155 | Ukrainian government and IT sector; NATO states | Active; one actor under several vendor names [42] |
| Void Blizzard | Laundry Bear, CL-STA-1114, TA488 | Russian state-supported; service not publicly named | Government, defense industry, law enforcement, transport, NGOs (NATO states, Ukraine) | Active since at least April 2024 [32][33] |
| CARR, Z-Pentest, Sector16, NoName057(16) | CyberArmyofRussia_Reborn | Hacktivist fronts with GRU or Kremlin-linked support | Water, food and agriculture, energy OT; DDoS against NATO states | Active; subject to indictments, takedowns and sanctions [37][38][39] |

## Active Campaigns

### APT29 Cloud and Identity Infrastructure Targeting (2023-Present)

APT29 continues to target diplomats, governments and cloud identity systems, and abuses OAuth applications, device code authentication and federated identity trusts. From January 2025 Check Point tracked phishing that impersonated a European foreign ministry with wine-tasting invitations, delivering a new loader, GRAPELOADER, and a new WINELOADER variant to European diplomatic entities [23].

On 31 July 2026 Microsoft reported the CaptiveCrunch campaign by Storm-2945, which it assesses to be an operational sub-cluster of Midnight Blizzard. Since early May 2026 the actor manipulated DNS and HTTP traffic on hotel and conference Wi-Fi networks that use captive portals, redirecting travelers to adversary-in-the-middle phishing, device code abuse and fake updates that install the CornFlake remote access trojan and the ChocoShell stealer. How the captive portal networks were compromised is still under investigation. The same post describes Storm-2372, the device code phishing cluster, as a Midnight Blizzard initial access sub-cluster [24].

In September 2026 Anthropic reported disrupting a Russian-speaking actor (GTG-20006) that used its Claude model from December 2025 to August 2026 across reconnaissance, phishing infrastructure, command execution, data handling and modification of malware to evade detection. Targets included Ukrainian government, military and diplomatic personnel, European defense organizations and drone manufacturers. Anthropic states its attribution is consistent with public reporting linking the actor to Midnight Blizzard; it does not make an independent attribution to the SVR [25].

### Sandworm Ukraine Conflict Operations (2022-Present)

Sandworm remains the primary Russian destructive operator in Ukraine. ESET reports the ZEROLOT wiper against Ukrainian energy companies between October 2024 and March 2025, deployed through Active Directory Group Policy [10], then ZEROLOT and Sting against government, energy, logistics and grain-sector organizations between April and September 2025, with the likely aim of weakening the Ukrainian economy [11]. ESET reports several further new wipers over the winter of 2025-2026 [12].

Initial access is increasingly handled by dedicated sub-groups. Microsoft's BadPilot research describes a Seashell Blizzard subgroup that has exploited internet-facing systems since at least 2021, expanded to the US, UK, Canada and Australia in 2024, and has likely enabled at least three destructive attacks in Ukraine since 2023 [20]. CERT-UA tracks UAC-0145, reported as a Sandworm sub-cluster, which in 2026 used fake CAPTCHA (ClickFix) prompts on compromised websites [41] and posed as recruiters to persuade Ukrainian system administrators to install a trojanized WireGuard client during mock interviews [40]. Google reports that APT44 helps forward-deployed Russian forces link Signal accounts from captured devices to actor-controlled infrastructure, and that several Russia-aligned clusters abuse Signal's linked devices feature through malicious QR codes [22].

### GRU Targeting of Western Edge Devices and Energy (2021-Present)

Amazon Threat Intelligence assesses with high confidence that a GRU-associated cluster, with infrastructure overlaps to Sandworm, has targeted Western energy organizations and critical infrastructure providers since 2021. Initial access moved from exploitation of WatchGuard, Confluence and Veeam vulnerabilities to sustained targeting of misconfigured customer network edge devices in 2025, followed by credential harvesting from intercepted traffic and replay against victims' online services [21].

In September 2026 Cisco Talos reported exploitation of two Cisco Secure Firewall Management Center vulnerabilities (CVE-2026-20079 and CVE-2026-20316) by three clusters. One, UAT-11823, overlaps in tooling with Sandworm and deployed a variant of Cyclops Blink [18]. Sophos assesses with high confidence that the activity has a Russian nexus and with moderate confidence that it is associated with Sandworm (Iron Viking), noting the absence of conclusive evidence directly linking the group to the 2026 deployments [19].

### APT28 Logistics, Webmail and Router Operations (2022-Present)

A May 2025 joint advisory attributes to GRU Unit 26165 a campaign since 2022 against logistics, transport, defense and IT service companies involved in delivering aid to Ukraine, across at least 13 countries. Techniques include password spraying, spearphishing, exploitation of Outlook, Roundcube and WinRAR vulnerabilities, and manipulation of mailbox permissions. The actors also targeted internet-connected IP cameras, mostly in Ukraine and neighboring countries; in a sample of over 10,000 cameras, 81% were in Ukraine [9]. ESET's Operation RoundPress describes the same group exploiting cross-site scripting flaws in Roundcube, Horde, MDaemon and Zimbra webmail, including an MDaemon zero-day [10].

In January 2026 Zscaler observed APT28 exploiting CVE-2026-21509 through crafted RTF files within days of the out-of-band patch, targeting Ukraine, Slovakia and Romania and delivering MiniDoor, an Outlook email stealer, and a Covenant Grunt implant [36]. ESET reports Covenant and BeardShell used against Ukrainian military personnel and drone manufacturers between October 2025 and March 2026 [12].

Since at least 2024 APT28 compromised TP-Link routers (CVE-2023-50224) and changed their DHCP and DNS settings so that connected devices used actor-controlled resolvers, enabling interception of credentials and tokens for services such as Outlook Web Access. The FBI and the US Department of Justice disrupted the router network in April 2026 [35]. Whether the actor has rebuilt this capability is not known.

### FSB Center 16 Network Device Intrusions (2015-Present)

Cisco Talos and the FBI reported in August 2025 that Static Tundra exploits CVE-2018-0171 in Cisco Smart Install on unpatched and end-of-life devices to collect configurations and maintain long-term access, and that the group has used the SYNful Knock firmware implant [34]. On 13 July 2026 the UK NCSC and partners from 12 countries published an advisory on FSB Center 16 scanning for weak SNMP credentials and exploiting Cisco devices across communications, defense, energy, financial services, government and healthcare [15].

### Turla Espionage Against Diplomats and Ukraine (2024-Present)

Microsoft reported in July 2025 that Secret Blizzard holds an adversary-in-the-middle position at ISP level inside Russia, likely through domestic intercept systems such as SORM, and uses it against foreign embassies in Moscow. Targets are redirected through a captive portal to install ApolloShadow, which adds a trusted root certificate. The campaign has run since at least 2024 [26].

In Ukraine, ESET found Gamaredon tools (PteroGraphin, PteroOdd, PteroPaste) restarting or deploying Turla's Kazuar backdoor between February and June 2025, and assesses with high confidence that Gamaredon is providing access to Turla [27]. In June 2026 Google described STOCKSTAY, a multi-component .NET backdoor in development since at least December 2022, used against Ukrainian government and military organizations and entities with an interest in Italian foreign policy. Delivery included malicious RDP files and WinRAR CVE-2025-8088. Google attributes it to clusters with high-confidence links to Turla [28].

### Gamaredon High-Volume Operations Against Ukraine (2013-Present)

ESET recorded 35 distinct spearphishing campaigns in 2025, mostly in the second half of the year, targeting only Ukrainian government and military institutions. The group introduced six new PowerShell tools, moved exfiltration to S3-compatible cloud storage, and exploited WinRAR CVE-2025-8088 from 26 September 2025 [29].

### Star Blizzard Malware and Credential Campaigns (2023-Present)

Star Blizzard (also tracked as Callisto and ColdRiver) targets current and former advisors to Western governments and militaries, journalists, think tanks, NGOs and people connected to Ukraine. The DOJ and Microsoft seized over 100 of its domains in October 2024. In 2025 the group added malware delivery through ClickFix fake CAPTCHA lures. Google disclosed the LOSTKEYS file stealer in May 2025 [30]; within five days the group replaced it with a new chain (NOROBOT, YESROBOT, MAYBEROBOT), and Google has not seen LOSTKEYS since. Google describes the development tempo as rapidly increased [31].

### Void Blizzard Cloud and Webmail Espionage (2024-Present)

Void Blizzard uses credentials likely bought from infostealer markets, and from April 2025 adversary-in-the-middle phishing, to collect email and files in bulk through Exchange Online and Microsoft Graph [32]. A July 2026 advisory by 24 agencies describes the same actor exploiting a Zimbra cross-site scripting flaw (CVE-2025-66376) as a zero-day from July 2025, triggered when the victim views an email, with extensive Ukrainian targeting before use against the US and NATO allies [33].

### GRU-Linked Hacktivist Fronts Targeting OT (2022-Present)

A December 2025 joint advisory states that GRU Unit 74455 is likely responsible for supporting the creation of CARR in 2022, that NoName057(16) was created as a covert project by CISM, an organization established on behalf of the Kremlin, and that Z-Pentest (September 2024) and Sector16 (January 2025) emerged from these groups. They gain access to water, food and energy OT through internet-exposed VNC with weak credentials. Impact is usually a temporary loss of view, but the advisory notes disregard for human safety [37]. The DOJ states CARR was founded, funded and directed by the GRU and describes Z-Pentest as another name for CARR, which differs from the advisory's account [38]. The EU sanctioned Z-Pentest and two of its members in July 2026 [17].

## Historical Campaigns

### Poland Energy Sector Destructive Attack (December 2025)

On 29 December 2025 attackers struck more than 30 wind and photovoltaic farms, a combined heat and power plant serving about 500,000 customers, and a manufacturing company. At the grid connection points they damaged remote terminal units, controller firmware, HMIs and protection relays. Electricity and heat supply were not interrupted [14]. ESET attributes the DynoWiper malware to Sandworm with medium confidence, citing similarity to the ZOV wiper, and notes that preparatory stages may have been carried out by another group [13]. CERT Polska found a high degree of infrastructure overlap with Static Tundra / Berserk Bear and called it the first publicly described destructive activity from that cluster [14]. The UK and EU member states attributed the attack to FSB Center 16 on 13 July 2026 [15][16].

### Midnight Blizzard Microsoft Corporate Email Compromise (2023-2024)

APT29 compromised Microsoft's corporate environment in late 2023 through a password spray against a legacy test tenant without MFA, then used that access to read email from senior executives and reach source code repositories. The campaign extended to other technology companies and US government agencies using Microsoft 365.

### SolarWinds Supply Chain Compromise (2020-2021)

APT29 executed one of the most sophisticated supply chain attacks in history by compromising the build system of SolarWinds Orion, a widely deployed network management platform. The trojanized SUNBURST backdoor was distributed via legitimate software updates to approximately 18,000 organizations, with the SVR selectively exploiting access in approximately 100 high-value targets including U.S. Treasury, Commerce, State Department, DHS, and major technology firms. The operation demonstrated exceptional operational security, including dormancy periods, traffic blending with legitimate Orion communications, and anti-analysis checks. Post-compromise activity used TEARDROP and Raindrop loaders to deploy Cobalt Strike beacons.

### Sandworm Invasion-Phase Operations (2022)

At the outset of the invasion Sandworm deployed multiple wiper families against Ukrainian government, energy, telecommunications and financial targets. The AcidRain attack disabled Viasat KA-SAT modems, and the April 2022 Industroyer2 attack targeted Ukrainian electrical substations.

### NotPetya (2017)

Sandworm deployed the NotPetya destructive malware via a compromised update to M.E.Doc, a Ukrainian tax accounting software. While disguised as ransomware, NotPetya was a wiper designed to cause maximum disruption. The malware spread laterally using EternalBlue and Mimikatz-based credential harvesting, escaping Ukraine's borders to cause an estimated $10+ billion in global damages. Maersk, Merck, FedEx/TNT Express, and Mondelez were among the most severely impacted. NotPetya remains the most destructive cyberattack in history and led to U.S., U.K., and EU attribution statements identifying the GRU.

### Ukraine Power Grid Attacks (2015-2016)

Sandworm conducted two pioneering attacks against Ukraine's power grid. The December 2015 attack on Kyivoblenergo and two other distribution companies used BlackEnergy malware for initial access and the KillDisk wiper, causing power outages for approximately 225,000 customers. The December 2016 attack deployed Industroyer/CrashOverride, the first known malware specifically designed to attack electrical grid control systems (ICS/SCADA), targeting the Pivnichna substation in Kyiv. These attacks demonstrated the real-world potential of cyber operations to disrupt critical infrastructure.

## TTP Evolution

Russian cyber operations have evolved significantly across several dimensions:

- **Wiper Proliferation**: The Ukraine conflict produced at least 10 distinct wiper malware families in 2022 alone. The pattern continues with ZEROLOT, Sting, ZOV and DynoWiper, and targeting has widened to economic sectors such as grain and logistics [11][13].
- **Destructive Activity Beyond Ukraine**: The December 2025 attack in Poland combined wipers with direct damage to industrial devices in a NATO member state [14].
- **Network-Path Interception**: ISP-level interception (Turla), router DNS hijacking (APT28) and captive portal manipulation (Storm-2945) move collection onto infrastructure the victim does not control [26][35][24].
- **Edge Devices and Misconfiguration**: GRU and FSB operators favor unpatched or misconfigured routers, VPN gateways and management appliances over zero-day exploitation [21][34][15].
- **Cloud Pivot**: APT29 and Void Blizzard focus on cloud identity abuse, OAuth and device code flows, and bulk collection through cloud APIs [24][32].
- **ClickFix Social Engineering**: Star Blizzard, a Sandworm sub-cluster and Storm-2945 all use fake CAPTCHA or verification prompts that make the victim run the payload [30][41][24].
- **Webmail and Messaging Exploitation**: View-triggered cross-site scripting in Roundcube, MDaemon and Zimbra, and abuse of Signal's linked devices feature [10][33][22].
- **Rapid Retooling and N-day Speed**: Star Blizzard replaced burned malware in five days; APT28 was seen exploiting CVE-2026-21509 three days after the patch [31][36].
- **Inter-Service Cooperation**: Gamaredon providing access to Turla is the first documented case of collaboration between the two [27].
- **AI-Assisted Operations**: One actor linked in public reporting to Midnight Blizzard used a commercial AI model across the intrusion lifecycle, including automated modification of detected tooling [25].
- **Hack-and-Leak Operations**: Integration of cyber operations with information warfare, using stolen data for strategic leaks (e.g., DNC 2016, Star Blizzard operations).
- **Proxies and Fronts**: State-supported hacktivist groups conduct low-sophistication OT intrusions and DDoS that provide deniability and publicity [37].

## Infrastructure Patterns

- Compromised SOHO routers reconfigured to use actor-controlled DNS resolvers hosted on virtual private servers [35]
- Compromised network edge devices used for packet capture and credential replay [21]
- ISP-level and captive-portal positions used for redirection and malware delivery [26][24]
- Legitimate cloud services for C2 and exfiltration, including file-sharing APIs, S3-compatible storage, tunneling services and dead drops [29][36]
- Extensive use of compromised legitimate websites for C2, fake CAPTCHA lures and watering hole attacks
- In-country compromised infrastructure, including government services, used to deliver payloads [28]
- Tor hidden services for persistent covert access (ShadowLink) [20]
- Domain typosquatting and homoglyph domains for credential harvesting
- Compromised email accounts for spear-phishing delivery
- VPN services and residential proxy networks to geolocate traffic near targets
- Legitimate remote management tools for persistence after exploitation [20]

## Tooling

| Tool | Type | Associated Actors | Notes |
|---|---|---|---|
| ZEROLOT | Wiper | Sandworm | Used against Ukrainian energy companies from late 2024; deployed via Group Policy [10] |
| Sting | Wiper | Sandworm | Used with ZEROLOT in Ukraine in 2025 [11] |
| DynoWiper | Wiper | Sandworm (ESET, medium confidence); attack attributed to FSB Center 16 by UK and EU | Poland, December 2025; similar to the ZOV wiper [13][15] |
| Cyclops Blink (2026 variant) | Modular Linux implant | Sandworm (moderate confidence) | x86-64 build found on Cisco FMC devices; adds network scanning and packet capture [18][19] |
| WAVESIGN | Batch script | Sandworm | Exfiltrates Signal Desktop messages using Rclone [22] |
| HEADLACE, MASEPIE, OCEANMAP, STEELHOOK | Backdoors and stealers | APT28 | Named in the May 2025 logistics advisory [9] |
| MiniDoor / NotDoor | Outlook VBA email stealer | APT28 | MiniDoor is a reduced variant of NotDoor [36] |
| Covenant, BeardShell | Implants | APT28 | Used against Ukrainian military and drone sector [12] |
| GRAPELOADER, WINELOADER | Loader, backdoor | APT29 | Diplomatic phishing in 2025 [23] |
| CornFlake, ChocoShell | Go RAT, PowerShell stealer | Storm-2945 (APT29 sub-cluster) | Delivered through manipulated captive portals [24] |
| GraphicalProton | Backdoor | APT29 | Deployed after TeamCity exploitation in 2023 [43] |
| Brute Ratel C4 | C2 framework | APT29 | Commercial red team tool adopted for operations |
| SUNBURST | Supply chain backdoor | APT29 | Deployed via trojanized SolarWinds Orion updates |
| Kazuar | Backdoor | Turla | Versions 2 and 3 active in Ukraine in 2025 [27] |
| STOCKSTAY | Multi-component .NET backdoor | Turla | WebSocket C2; code overlaps with Kazuar [28] |
| ApolloShadow | Root certificate installer | Turla | Delivered through ISP-level interception in Moscow [26] |
| Snake | Implant/P2P network | Turla | Disrupted by FBI in May 2023; historical |
| SYNful Knock | Cisco IOS firmware implant | Static Tundra | Persists through reboots [34] |
| Pterodo/Pteranodon family | Downloaders, stealers | Gamaredon | Six new PowerShell tools in 2025, including PteroPaste and PteroOdd [29] |
| LOSTKEYS | File stealer | Star Blizzard | Abandoned after disclosure in May 2025 [30][31] |
| NOROBOT, YESROBOT, MAYBEROBOT | Downloader, backdoors | Star Blizzard | Replaced LOSTKEYS; YESROBOT was a short-lived stopgap [31] |
| WhisperGate | Wiper (MBR/file) | Cadet Blizzard / Ember Bear (Unit 29155) | Disguised as ransomware; deployed against Ukraine Jan 2022 [42] |
| HermeticWiper, CaddyWiper | Wipers | Sandworm | 2022 invasion-phase tools; historical |
| Industroyer2 | ICS malware | Sandworm | Targets IEC-104 protocol; April 2022; historical |
| AcidRain | Wiper | Sandworm | Targeted Viasat KA-SAT satellite modems; historical |

## Intelligence Gaps

- **Poland attack attribution**: Vendor and government attributions differ between Sandworm (GRU) and FSB Center 16. Whether this reflects shared tooling, cooperation between services, or an attribution error is unresolved in public reporting [13][14][15].
- **Captive portal compromise vector**: How Storm-2945 gained control of hospitality Wi-Fi networks is not yet established [24].
- **Cyclops Blink operator**: The link between the 2026 Cisco FMC activity and Sandworm rests on tooling overlap and is assessed at moderate confidence [18][19].
- **Void Blizzard sponsor**: The service behind Void Blizzard has not been named in the sources reviewed [32][33].
- **Effect of disruptions**: The lasting effect of Operation Eastwood, the April 2026 router disruption and the July 2026 sanctions on actor operations is not measured in the sources reviewed. The outcome of the US prosecutions announced in December 2025 was not confirmed for this update [38].
- **Star Blizzard in 2026**: No primary reporting on the group's activity after October 2025 was confirmed for this update.
- **Reported but not verified at the primary source**: UAC-0145 tool names and outcomes (CERT-UA pages could not be opened; details here are from press coverage) [40][41].
- **GRU-ransomware nexus**: The precise relationship between Russian intelligence services and ransomware groups (safe harbor, tacit approval, active direction, or recruitment) remains poorly defined.
- **Pre-positioned access in Western infrastructure**: The extent of Russian pre-positioning in NATO member critical infrastructure outside Ukraine and Poland is largely unknown.
- **Coordination across agencies**: Gamaredon and Turla cooperate inside the FSB [27]; the degree of coordination between GRU, SVR and FSB units remains unclear.

## Live enrichment

When CrowdStrike Falcon Intelligence credentials are configured (`$CROWDSTRIKE_CLIENT_ID`), pull live vendor intelligence to keep this cell current and to answer specific actor questions:

- **Actor profile** — `/lookup-crowdstrike actor "Cozy Bear"` / `actor "Fancy Bear"` (origins, target countries/industries, motivations, capability, aliases)
- **TTPs** — `/lookup-crowdstrike ttps "Fancy Bear"` → ATT&CK technique IDs; resolve against `/mitre-attack`
- **Latest reporting** — `/lookup-crowdstrike reports --actor "Voodoo Bear" --latest`
- **Actor population** — `/lookup-crowdstrike actors --origin russia` to enumerate Russia-attributed adversaries CrowdStrike tracks (CrowdStrike uses the "Bear" cryptonym for Russian state-nexus actors)

Route through `/threat-actor-profiling` for a full structured profile. CrowdStrike report bodies are typically TLP:AMBER+ — cite report IDs internally, do not redistribute.

## Sources & References

1. Microsoft Threat Intelligence: "Midnight Blizzard: Guidance for responders on nation-state attack" (January 2024)
2. CISA Advisory AA22-110A: "Russian State-Sponsored and Criminal Cyber Threats to Critical Infrastructure" (April 2022)
3. Mandiant: "APT29 Targets Microsoft 365 Environments" (2024)
4. ESET Research: "Industroyer2: Sandworm's Cyberwarfare Targets Ukraine's Power Grid Again" (April 2022)
5. SentinelLabs: "AcidRain: A Modem Wiper Rains Down on Europe" (March 2022)
6. DOJ Press Release: "Justice Department Announces Court-Authorized Disruption of Snake Malware Network" (May 2023)
7. CrowdStrike 2025 Global Threat Report: Russia-nexus adversary activity analysis
8. NSA/CISA/FBI Joint Advisory: "Russian GRU Conducting Global Brute Force Campaign" (2021)
9. CISA and partners, Advisory AA25-141A: "Russian GRU Targeting Western Logistics Entities and Technology Companies" (21 May 2025). https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-141a
10. ESET: "ESET Research APT Report: Russian cyberattacks in Ukraine intensify; Sandworm unleashes new destructive wiper" (19 May 2025). https://www.eset.com/us/about/newsroom/research/eset-research-apt-report-russian-cyberattacks-in-ukraine-intensify-sandworm-unleashes-new-destructive-wiper/
11. ESET Research: "ESET APT Activity Report Q2 2025–Q3 2025" (6 November 2025). https://www.welivesecurity.com/en/eset-research/eset-apt-activity-report-q2-2025-q3-2025/
12. ESET Research: "ESET APT Activity Report Q4 2025–Q1 2026" (28 May 2026). https://www.welivesecurity.com/en/eset-research/eset-apt-activity-report-q4-2025-q1-2026/
13. ESET Research: "DynoWiper update: Technical analysis and attribution" (30 January 2026). https://www.welivesecurity.com/en/eset-research/dynowiper-update-technical-analysis-attribution/
14. CERT Polska: "Energy Sector Incident Report - 29 December 2025" (30 January 2026). https://cert.pl/en/posts/2026/01/incident-report-energy-sector-2025/
15. UK NCSC: "UK and Allies urge critical sectors to improve defences against Russian intelligence targeting" (13 July 2026). https://www.ncsc.gov.uk/news/uk-and-allies-urge-critical-sectors-to-improve-defences-against-russian-intelligence-targeting
16. Council of the EU: "Cyber / Russia: Statement by the High Representative on behalf of the European Union denouncing Russia's malicious cyber ecosystem" (13 July 2026), read as mirrored at https://www.globalsecurity.org/security/library/news/2026/07/sec-260713-ec02.htm
17. Council of the EU: "Russian cyber-attacks and destabilising activities: Council sanctions nine individuals and four entities" (13 July 2026), read as mirrored at https://www.globalsecurity.org/security/library/news/2026/07/sec-260713-ec01.htm
18. Cisco Talos: "Active exploitation of Cisco Secure Firewall Management Center vulnerabilities" (9 September 2026). https://blog.talosintelligence.com/fmc-ongoing-exploitation/
19. Sophos Counter Threat Unit: "'Eye' spy: Cyclops Blink returns with extended capabilities" (September 2026). https://www.sophos.com/en-us/blog/-eye-spy-cyclops-blink-returns-with-extended-capabilities
20. Microsoft Threat Intelligence: "The BadPilot campaign: Seashell Blizzard subgroup conducts multiyear global access operation" (12 February 2025). https://www.microsoft.com/en-us/security/blog/2025/02/12/the-badpilot-campaign-seashell-blizzard-subgroup-conducts-multiyear-global-access-operation/
21. Amazon Threat Intelligence: "Amazon Threat Intelligence identifies Russian cyber threat group targeting Western critical infrastructure" (15 December 2025). https://aws.amazon.com/blogs/security/amazon-threat-intelligence-identifies-russian-cyber-threat-group-targeting-western-critical-infrastructure
22. Google Threat Intelligence Group: "Signals of Trouble: Multiple Russia-Aligned Threat Actors Actively Targeting Signal Messenger" (February 2025). https://cloud.google.com/blog/topics/threat-intelligence/russia-targeting-signal-messenger
23. Check Point Research: "Renewed APT29 Phishing Campaign Against European Diplomats" (15 April 2025). https://research.checkpoint.com/2025/apt29-phishing-campaign/
24. Microsoft Threat Intelligence: "CaptiveCrunch: Midnight Blizzard targets travelers worldwide for malware delivery and credential theft" (31 July 2026). https://www.microsoft.com/en-us/security/blog/2026/07/31/captivecrunch-midnight-blizzard-targets-travelers-worldwide-for-malware-delivery-and-credential-theft/
25. Anthropic: "Threat Intelligence Report" (September 2026). https://www.anthropic.com/threat-intelligence-report-september-2026
26. Microsoft Threat Intelligence: "Frozen in transit: Secret Blizzard's AiTM campaign against diplomats" (31 July 2025). https://www.microsoft.com/en-us/security/blog/2025/07/31/frozen-in-transit-secret-blizzards-aitm-campaign-against-diplomats/
27. ESET Research: "Gamaredon X Turla collab" (19 September 2025). https://www.welivesecurity.com/en/eset-research/gamaredon-x-turla-collab/
28. Google Threat Intelligence Group: "STOCKSTAY Another Day: The Latest Addition to Turla's Intelligence Gathering Apparatus" (June 2026). https://cloud.google.com/blog/topics/threat-intelligence/stockstay-turla-intelligence-gathering/
29. ESET Research: "Gamaredon in 2025: Leveraging tunnels, workers, dead drops, and new alliances" (25 June 2026). https://www.welivesecurity.com/en/eset-research/gamaredon-2025-leveraging-tunnels-workers-dead-drops-new-alliances/
30. Google Threat Intelligence Group: "COLDRIVER Using New Malware To Steal Documents From Western Targets and NGOs" (8 May 2025). https://cloud.google.com/blog/topics/threat-intelligence/coldriver-steal-documents-western-targets-ngos
31. Google Threat Intelligence Group: report on COLDRIVER's NOROBOT, YESROBOT and MAYBEROBOT malware (21 October 2025). https://cloud.google.com/blog/topics/threat-intelligence/new-malware-russia-coldriver/
32. Microsoft Threat Intelligence: "New Russia-affiliated actor Void Blizzard targets critical sectors for espionage" (27 May 2025). https://www.microsoft.com/en-us/security/blog/2025/05/27/new-russia-affiliated-actor-void-blizzard-targets-critical-sectors-for-espionage/
33. CISA and partners, Advisory AA26-204A: "Russian State-Supported Cyber Actors Conduct Phishing Campaign Targeting Users of Zimbra Collaboration Suite" (23 July 2026). https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-204a
34. Cisco Talos: "Russian state-sponsored espionage group Static Tundra compromises unpatched end-of-life network devices" (20 August 2025). https://blog.talosintelligence.com/static-tundra/
35. FBI IC3 Public Service Announcement PSA260407: "Russian GRU Exploiting Vulnerable Routers to Steal Sensitive Information" (7 April 2026). https://www.ic3.gov/PSA/2026/PSA260407
36. Zscaler ThreatLabz: "APT28 Leverages CVE-2026-21509 in Operation Neusploit" (2 February 2026). https://www.zscaler.com/blogs/security-research/apt28-leverages-cve-2026-21509-operation-neusploit
37. CISA and partners, Advisory AA25-343A: "Pro-Russia Hacktivists Conduct Opportunistic Attacks Against US and Global Critical Infrastructure" (9 December 2025). https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-343a
38. US Department of Justice: "Justice Department Announces Actions to Combat Two Russian State-Sponsored Cyber Criminal Hacking Groups" (9 December 2025). https://www.justice.gov/opa/pr/justice-department-announces-actions-combat-two-russian-state-sponsored-cyber-criminal
39. Infosecurity Magazine, reporting Europol: "Pro-Russian Cybercrime Network Demolished in Operation Eastwood" (16 July 2025). https://www.infosecurity-magazine.com/news/prorussian-cybercrime-network/
40. The Record, reporting CERT-UA: "Russian military hackers pose as recruiters to target Ukrainian IT workers" (10 August 2026). https://therecord.media/russian-military-hackers-pose-as-recruiters-ukraine-it-workers
41. The Record, reporting CERT-UA: "Sandworm hackers have a CAPTCHA trick for Ukrainians" (16 July 2026). https://therecord.media/ukraine-sandworm-hacks-captcha-powershell
42. CISA and partners, Advisory AA24-249A on GRU Unit 29155 cyber actors (5 September 2024). https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-249a
43. CISA and partners, Advisory AA23-347A on SVR exploitation of JetBrains TeamCity (13 December 2023). https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-347a

## Change Log

| Date | Change | Source |
|---|---|---|
| 2026-04-05 | Initial cell creation; seeded with training knowledge through early 2025 | Training data |
| 2026-09-29 | Refresh covering January 2025 to September 2026. Rewrote Executive Summary; added Poland energy attack with contested attribution, APT28 logistics and router campaigns, CaptiveCrunch, Turla ISP-level interception and STOCKSTAY, Gamaredon-Turla collaboration, Void Blizzard, FSB Center 16 device intrusions, hacktivist fronts and law enforcement actions. Corrected GraphicalProton attribution (APT29, not APT28) and merged Cadet Blizzard and Ember Bear as one Unit 29155 actor. Moved the 2023-2024 Microsoft compromise and 2022 invasion-phase operations to Historical. Added sources 9-43. | OSINT refresh |
