---
name: china-cyber-espionage
description: Use when the user asks about Chinese state-sponsored cyber operations or specific PRC-aligned actors (APT41, Volt Typhoon, Mustang Panda, APT10, APT31, Salt Typhoon, etc.), MSS/PLA-attributed campaigns, or PRC sector targeting. Self-updating knowledge cell.
user-invocable: true
metadata:
  category: knowledge-cell
  created: 2026-04-05
  last_updated: 2026-09-29
  update_count: 1
  confidence: moderate
---

# China Cyber Espionage Knowledge Cell

## Executive Summary

China operates the most extensive state-sponsored cyber espionage apparatus globally. Operations are tasked primarily by the Ministry of State Security (MSS) and the People's Liberation Army (PLA), with the Ministry of Public Security (MPS) also named as a customer in U.S. indictments. Since 2025 the public record has shifted from describing discrete "APT groups" to describing an ecosystem: government advisories, sanctions and indictments now name the private companies that build tooling, run infrastructure and sell stolen data to the state. Named firms include i-Soon, Integrity Technology Group, Shanghai Heiying, Sichuan Juxinhe, Beijing Huanyu Tianqiong and Sichuan Zhixin Ruijie [9][10][11][12][22]. One consequence is that vendor cluster names no longer map cleanly onto organisations, and sources disagree on several mappings (see Key Actors).

Two strategic lines of effort remain active. The first is espionage against communications infrastructure: the activity tracked as Salt Typhoon was described in August 2025 by agencies from 13 countries as a global campaign running since at least 2021 against telecommunications, government, transportation, lodging and military networks [9]. European governments continued to disclose compromises into 2026 [26][27]. The second is pre-positioning in critical infrastructure, associated with Volt Typhoon. U.S. advisories attribute Volt Typhoon to PRC state-sponsored actors without naming a service [1]. The Wall Street Journal reported in April 2025 that Chinese officials indirectly acknowledged the activity in a December 2024 meeting in Geneva, in remarks U.S. officials read as linked to U.S. support for Taiwan [30].

Tradecraft has converged on the network edge and on systems that cannot run endpoint detection. The 2025-2026 record is dominated by exploitation of VPN, firewall, router and email appliances, by backdoors placed on VMware vCenter and ESXi hosts with dwell times averaging over a year [17][18], by abuse of stolen credentials, API keys and OAuth applications to reach downstream customers of IT providers [13], and by covert networks of compromised SOHO and IoT devices that a 15-agency advisory in April 2026 said the majority of China-nexus actors now use [22]. CrowdStrike reported a 38% rise in China-nexus activity in 2025 [32]. In November 2025 Anthropic reported the first documented espionage campaign in which an AI model carried out most of the intrusion work, attributed with high confidence to a Chinese state-sponsored group [20].

Traditional espionage against governments continues alongside this. Mustang Panda clusters remained active across Asia and returned to European diplomatic targeting from mid-2025, extending to the Middle East in March 2026 [23][24]. APT41 continued government targeting using cloud services for command and control [19].

## Key Actors

| Threat Actor | Aliases | Attribution | Primary Targets | Status |
|---|---|---|---|---|
| APT41 | Winnti, Wicked Panda, Barium, Double Dragon, HOODOO | MSS (Chengdu) | Government, shipping and logistics, media, technology, automotive | Active; TOUGHPROGRESS campaign disclosed May 2025 [19] |
| APT10 | Stone Panda, MenuPass, Red Apollo | MSS (Tianjin) | MSPs, technology, aerospace, defense | No new reporting confirmed in the 2026-09 refresh |
| APT31 | Zirconium, Judgment Panda, Violet Typhoon | MSS (Wuhan) | Government, political entities, NGOs, think tanks | Active; Microsoft named Violet Typhoon in SharePoint exploitation, July 2025 [16] |
| Volt Typhoon | Bronze Silhouette, Vanguard Panda, DEV-0391 | PRC state-sponsored; U.S. advisories do not name a service [1] | U.S. critical infrastructure (energy, water, comms, transport) | Active |
| Salt Typhoon | GhostEmperor, FamousSparrow, OPERATOR PANDA, RedMike, UNC5807 | Contractor-enabled; three named companies supply the MSS and PLA [9] | Telecommunications, government, transportation, lodging, military | Active |
| Mustang Panda | Bronze President, Earth Preta, Stately Taurus, HoneyMyte; TA416 / RedDelta is tracked by Proofpoint as a distinct cluster [23] | MSS-linked | Government and diplomatic entities (Asia, Europe, Middle East) | Active |
| APT27 | Emissary Panda, Lucky Mouse, Iron Tiger, Bronze Union, Budworm | MSS and MPS contractors per DOJ [12] | Defense, technology, government | Active; two alleged members indicted March 2025 |
| Silk Typhoon | Hafnium | MSS-linked (Shanghai State Security Bureau contractors per DOJ) [31] | IT providers, government, healthcare, legal, education, defense | Active; one alleged member in U.S. custody since April 2026 |
| UNC5221 | None agreed (see note) | Suspected China-nexus | Legal services, SaaS, BPO, technology | Active |
| Flax Typhoon | None confirmed in this refresh | Operated via Integrity Technology Group [11][22] | Critical infrastructure; operated the Raptor Train botnet | Company sanctioned January 2025 |
| Linen Typhoon | None confirmed in this refresh | PRC state-sponsored per Microsoft [16] | Government, defense; intellectual property theft | Active (since 2012 per Microsoft) |
| Storm-2603 | None | China-based, moderate confidence; motive unclear [16] | SharePoint servers; deployed Warlock and LockBit ransomware | Active as of July 2025 |
| UAT-9686 | None | China-nexus, moderate confidence (Cisco Talos) [21] | Cisco email security appliances | Active as of December 2025 |
| APT3 | Gothic Panda, Buckeye, UPS Team | MSS (Guangdong) | Defense, aerospace, technology | Reduced activity |

**Naming conflicts.** The March 2025 DOJ release lists "Silk Typhoon" and "UNC 5221" among the aliases of APT27 [12]. Microsoft tracks Silk Typhoon as the actor formerly called HAFNIUM [13]. Google states that it does not consider UNC5221 and Silk Typhoon to be the same cluster [17]. This cell keeps the three as separate rows and treats the overlap as unresolved.

## Active Campaigns

### Volt Typhoon Critical Infrastructure Pre-Positioning (2023-Present)

Volt Typhoon has maintained persistent access to U.S. critical infrastructure networks in the communications, energy, transportation and water sectors. The group relies on LOTL techniques, using built-in Windows tools such as `wmic`, `ntdsutil`, `netsh`, and `PowerShell` to move laterally and maintain persistence. Initial access is typically achieved through internet-facing network appliances from Fortinet (FortiGate), Ivanti (Connect Secure), NETGEAR, Citrix and Cisco [1]. The campaign is assessed as pre-positioning for disruptive or destructive operations in a crisis or conflict.

In March 2025 Dragos disclosed that the actor had been inside the Littleton Electric Light and Water Departments in Massachusetts from February to November 2023, collecting operating procedures, geographic information system data and network diagrams; no customer data was taken [29]. The KV botnet used by the group was largely defunct after the 2023-2024 takedown, but Lumen reported in June 2026 that its JDY cluster survived and has grown to more than 1,500 SOHO and IoT devices used for scanning, with U.S. military networks the most prominent target. Lumen links JDY to Chinese state-backed actors including Volt Typhoon rather than to Volt Typhoon alone [25].

### Salt Typhoon Global Telecommunications Compromise (2021-Present)

What was first reported in 2024 as a breach of U.S. carriers is now documented as a global campaign. Advisory AA25-239A (27 August 2025, revised 3 September 2025), co-signed by agencies from the United States, Australia, Canada, New Zealand, the United Kingdom, the Czech Republic, Finland, Germany, Italy, Japan, the Netherlands, Poland and Spain, dates the activity to at least 2021 and names three Chinese companies as suppliers of the capability [9]. Treasury had sanctioned one of them, Sichuan Juxinhe, in January 2025 [10].

The actors modify router access control lists, open SSH on non-standard ports, run tooling in Cisco Guest Shell containers, and capture TACACS+ and RADIUS traffic to harvest credentials [9]. Sources differ on initial access. The advisory lists exploitation of known CVEs in Ivanti, Palo Alto Networks and Cisco products and states that no zero-day use has been observed [9]. Recorded Future observed attempts against more than 1,000 Cisco devices in December 2024 and January 2025 using CVE-2023-20198 and CVE-2023-20273 [15]. Cisco Talos, reporting on the U.S. carrier intrusions, found that access was gained mainly with legitimate stolen credentials, confirmed only one case of CVE-2018-0171 exploitation, and saw access held for over three years in one environment [14].

Disclosed victims now extend well beyond the original carriers. A June 2025 DHS memo reported that one U.S. state's Army National Guard network was compromised from March to December 2024 [28]. Norway's Police Security Service confirmed compromised network devices in Norwegian organisations in February 2026 [26]. Press compilations list further confirmed or reported victims in Canada, the Netherlands, the United Kingdom, Italy and elsewhere, and cite an FBI figure of at least 200 affected companies [27].

### Mustang Panda Government and Diplomatic Targeting (2024-Present)

Targeting is no longer confined to Southeast Asia. Proofpoint reports that TA416 resumed campaigns against European diplomatic missions to the EU and NATO from mid-2025 after a two-year lull, and expanded to Middle Eastern government entities in March 2026. Delivery chains rotated between fake Cloudflare Turnstile pages, Microsoft Entra ID OAuth redirect abuse and renamed MSBuild executables, ending in a customised PlugX loaded by DLL sideloading [23]. Proofpoint separates this cluster from a second Mustang Panda cluster that uses TONESHELL and PUBLOAD [23].

Kaspersky reported in August 2026 that the cluster it tracks as HoneyMyte deployed PlugX and then a CoolClient backdoor protected by a signed kernel-mode driver against government entities in Myanmar, Mongolia, Pakistan and Russia [24]. USB propagation and themed lures tied to regional politics remain in use.

### Silk Typhoon IT Supply Chain Targeting (2024-Present)

Microsoft reported in March 2025 that Silk Typhoon has moved from direct exploitation toward the IT supply chain. The actor steals API keys and credentials from privileged access management, cloud application and data management providers, then uses them to enter downstream customer environments, where it abuses OAuth applications and service principals to collect email and SharePoint data through Microsoft Graph. It also used a zero-day in Ivanti Pulse Connect VPN (CVE-2025-0282) in January 2025 [13].

### UNC5221 BRICKSTORM Intrusions (2024-Present)

Google reported in September 2025 that UNC5221 and related clusters had held access to U.S. legal services, SaaS, business process outsourcing and technology companies with an average dwell time of 393 days. The BRICKSTORM backdoor is placed on VMware vCenter and ESXi hosts and on Linux and BSD appliances that do not support endpoint detection [17]. CISA, the NSA and the Canadian Centre for Cyber Security attributed BRICKSTORM to PRC state-sponsored actors in December 2025, describing one victim where access ran from April 2024 to at least September 2025, and updated the report through February 2026 with Rust and .NET variants [18].

## Historical Campaigns

### APT10 Cloud Hopper (2016-2019)

APT10's "Cloud Hopper" campaign targeted managed service providers (MSPs) to gain indirect access to the networks of hundreds of organizations across at least 12 countries. By compromising MSP infrastructure, the group accessed client networks in aerospace, defense, healthcare, and technology sectors. The campaign demonstrated the strategic value of supply chain compromise and led to the 2018 DoJ indictment of two Chinese nationals associated with MSS operations in Tianjin. Tools included QuasarRAT, PlugX, and custom Scorpion and Haymaker implants.

### APT41 Supply Chain and Dual-Purpose Operations (2019-2022)

APT41 conducted multiple supply chain compromises including the ASUS Live Update and CCleaner attacks, alongside targeted intrusions into at least 14 countries. The group uniquely combined state-sponsored espionage with financially motivated operations including video game virtual currency theft and ransomware deployment. The 2020 DoJ indictment of five Chinese nationals revealed the group's connection to Chengdu 404 Network Technology, a front company linked to the MSS. APT41 also exploited Log4Shell, ProxyLogon, and other zero-days at speed.

### Hafnium/Silk Typhoon Exchange Server Exploitation (2021)

In early 2021, Hafnium conducted mass exploitation of four zero-day vulnerabilities in Microsoft Exchange Server (ProxyLogon, CVE-2021-26855 and related CVEs), compromising an estimated 250,000+ servers globally. The operation began as targeted espionage but rapidly escalated to mass exploitation once the vulnerabilities became public. The campaign prompted an emergency CISA directive and an unusual FBI operation to remotely remove web shells from compromised U.S. servers. Xu Zewei, an alleged contractor for the Shanghai State Security Bureau charged over this period of activity, was arrested in Milan in July 2025 and extradited to the United States in April 2026; a co-defendant remains at large [31].

### U.S. Treasury Compromise (2024)

Treasury's Departmental Offices network was compromised in 2024. OFAC sanctioned Yin Kecheng, described as an MSS-affiliated actor based in Shanghai, in January 2025 for his involvement [10], and sanctioned his associate Zhou Shuai and the company Shanghai Heiying in March 2025 [11]. DOJ unsealed indictments against both men the same day, describing them as APT27 members who sold stolen data to MSS and MPS customers [12].

### SharePoint "ToolShell" Exploitation (July 2025)

Microsoft observed exploitation attempts against on-premises SharePoint servers from 7 July 2025 using CVE-2025-49706 and CVE-2025-49704, followed by the bypasses CVE-2025-53770 and CVE-2025-53771. It attributed activity to Linen Typhoon, Violet Typhoon and Storm-2603. Attackers deployed a web shell to steal ASP.NET machine keys. Storm-2603 deployed Warlock and LockBit ransomware from 18 July, an example of a China-based actor whose motive Microsoft could not determine [16].

### AI-Orchestrated Espionage Campaign (September 2025)

Anthropic detected in mid-September 2025, and disclosed on 13 November 2025, a campaign in which a group it assesses with high confidence to be Chinese state-sponsored manipulated its Claude Code tool into attempting intrusions against roughly thirty organisations in technology, finance, chemical manufacturing and government. A small number succeeded. The AI performed an estimated 80-90% of the work, with human input at a handful of decision points. Anthropic noted that the model at times hallucinated credentials or overstated findings [20].

## TTP Evolution

Chinese cyber operations have undergone significant tactical evolution over the past five years:

- **LOTL Dominance**: Volt Typhoon pioneered the near-exclusive use of built-in operating system tools, avoiding custom malware entirely. This approach has spread to other Chinese groups, dramatically complicating detection.
- **Edge Device Targeting**: Systematic exploitation of network perimeter devices (VPN appliances, firewalls, routers, email gateways) has become a hallmark. Ivanti, Fortinet, Citrix, Palo Alto Networks and Cisco devices are consistently targeted, with both zero-days [13][21] and long-patched flaws such as CVE-2018-0171 [9][14]. CrowdStrike reports that 40% of the vulnerabilities China-nexus actors exploited in 2025 were in internet-facing edge devices [32].
- **Virtualisation and Appliance Persistence**: Backdoors are placed on vCenter, ESXi and network appliances where endpoint detection is absent, producing dwell times of a year or more [17][18].
- **Operational Relay Boxes (ORBs)**: Covert networks of compromised SOHO routers, IoT devices, firewalls and NAS units are now used by most China-nexus actors for every phase of an intrusion. They are built and maintained by Chinese information security companies and shared between actors [22].
- **Identity and Cloud Abuse**: Stolen API keys, credentials found in public code repositories, and compromised OAuth applications are used to move from IT providers into customer tenants [13]. OAuth redirect abuse also appears in phishing delivery [23].
- **Supply Chain Focus**: From Cloud Hopper to the targeting of SaaS, PAM and MSP providers, Chinese actors continue to target upstream providers for downstream access [13][17].
- **Speed of Exploitation**: Reconnaissance against newly disclosed flaws begins within hours. Lumen observed JDY scanning rise hours after disclosure of CVE-2026-35616 [25].
- **Contractor Model**: Indictments describe contractors paid per compromised mailbox (i-Soon charged roughly $10,000 to $75,000 each) and freelancers selling the same access to multiple state customers [12].
- **AI Use**: Agentic AI has been used to automate reconnaissance, exploitation and exfiltration, with reliability limits [20]. Separately, a September 2026 U.S. advisory describes model distillation campaigns against U.S. AI firms; it attributes these to China-based AI companies, not to state intrusion sets [33].
- **Kernel-Level Concealment**: Some espionage clusters are adding signed kernel drivers to hide implants [24], a counter-trend to the general reduction in custom malware.

## Infrastructure Patterns

- Compromised SOHO routers and IoT devices used as operational relay boxes, mostly end-of-life equipment; brands named in recent reporting include Cisco, NETGEAR, Araknis, DrayTek, Hikvision, Linksys, Zyxel, QNAP and Cyberoam [13][22][25]
- Covert networks operated by contractors, for example Raptor Train (over 200,000 devices in 2024) managed by Integrity Technology Group [22]
- Leased infrastructure from U.S.-based hosting providers and cloud services to blend with legitimate traffic
- Legitimate cloud services for C2 and staging, including Google Calendar, Cloudflare Workers and Azure Blob Storage [19][23]
- GRE tunnels and non-standard-port SSH on compromised routers for persistence and exfiltration [9][15]
- Re-registered formerly legitimate domains fronted by Cloudflare [23]
- Fast-flux DNS and dynamic DNS services for rapid infrastructure rotation
- VPN appliance implants that survive firmware updates and reboots
- Tor and multi-hop proxy chains for operator access to C2 infrastructure [25]
- Use of code-signing certificates (often stolen or expired) to sign malware and drivers [24]

## Tooling

| Tool | Type | Associated Actors | Notes |
|---|---|---|---|
| ShadowPad | Modular backdoor | APT41, APT10, multiple MSS groups | Successor to PlugX; shared among MSS contractors |
| PlugX | RAT/backdoor | Mustang Panda, TA416, APT10, APT27, APT41 | Still actively developed; customised, heavily obfuscated variant used by TA416 in 2025-2026 [23] |
| Cobalt Strike | C2 framework | APT41, APT27, multiple groups | Widely used legitimate red team tool; cracked copies prevalent |
| TONESHELL | Backdoor | Mustang Panda | Custom shellcode loader with multiple C2 protocols |
| DOPLUGS | Backdoor loader | Mustang Panda | Enhanced PlugX variant with additional evasion |
| CoolClient | Backdoor | Mustang Panda (HoneyMyte) | 2025-2026 variant installs signed kernel driver msagent.sys [24] |
| BRICKSTORM | Backdoor | UNC5221 and related clusters | Go, Rust and .NET variants; SOCKS proxy; targets vCenter, ESXi and appliances [17][18] |
| BRICKSTEAL / SLAYSTYLE | Credential stealer / web shell | UNC5221 | Java Servlet filter and JSP web shell on vCenter [17] |
| TOUGHPROGRESS | Backdoor | APT41 | Google Calendar C2; delivered by PLUSDROP and PLUSINJECT; infrastructure taken down by Google [19] |
| JumbledPath | Packet capture utility | Salt Typhoon | Go tool for remote capture on Cisco devices through a jump host [14] |
| AquaShell / AquaTunnel / AquaPurge | Backdoor, tunnel, log cleaner | UAT-9686 | Deployed on Cisco Secure Email appliances [21] |
| Winnti | Backdoor/rootkit | APT41 | Kernel-level rootkit for long-term persistence |
| China Chopper | Web shell | Multiple groups | Lightweight (~4KB) web shell; widely deployed post-exploitation |
| Deadeye/LOWKEY | Backdoor | APT41 | Passive backdoor activated by magic packet |
| KV Botnet | Botnet/proxy | Volt Typhoon | Main cluster largely defunct since 2024 takedown; JDY cluster persists [22][25] |
| JDY | Scanning botnet | China-nexus actors including Volt Typhoon | 1,500+ SOHO and IoT devices as of June 2026 [25] |
| Raptor Train | Botnet/proxy | Flax Typhoon (Integrity Technology Group) | Over 200,000 devices in 2024 [22] |
| KEYPLUG | Backdoor | APT41 | Cross-platform (Windows/Linux) modular backdoor |

## Intelligence Gaps

- **Full scope of Volt Typhoon pre-positioning**: The true extent of compromised critical infrastructure remains unknown; confirmed cases likely represent a fraction of actual access. Which service directs Volt Typhoon has not been stated in the U.S. advisories reviewed.
- **Salt Typhoon eviction status**: Whether the actors have been removed from U.S. carrier networks is not established in any primary source opened for this refresh. August 2026 press reporting that officials consider the actors contained but not eradicated could not be verified and is unconfirmed.
- **Salt Typhoon data access**: The complete scope of data taken from telecom providers has not been publicly disclosed.
- **Cluster-to-organisation mapping**: The relationship between APT27, Silk Typhoon and UNC5221 is contested between DOJ, Microsoft and Google [12][13][17]. The relationship between TA416 and other Mustang Panda clusters is likewise a vendor judgement [23].
- **Contractor ecosystem**: More companies are now named, but how tasking, tooling and access are shared between them and between MSS, PLA and MPS customers remains poorly understood.
- **Zero-day acquisition pipeline**: The mechanisms by which Chinese groups acquire zero-day exploits remain partially opaque.
- **APT10 and APT3 current activity**: No reporting from 2025-2026 on either group was confirmed during this refresh; their status entries are carried forward from the original cell.
- **Not confirmed in this refresh**: The 2026 ODNI Annual Threat Assessment wording on China, the Czech attribution of a foreign ministry intrusion to APT31, and the reported DOJ operation to remove PlugX from U.S. hosts were not checked against primary sources and are not relied on here.
- **AI integration**: One campaign is documented [20]. How widely Chinese operators use AI models for vulnerability research and operations is unknown.

## Live enrichment

When CrowdStrike Falcon Intelligence credentials are configured (`$CROWDSTRIKE_CLIENT_ID`), pull live vendor intelligence to keep this cell current and to answer specific actor questions:

- **Actor profile** — `/lookup-crowdstrike actor "Mustang Panda"` (origins, target countries/industries, motivations, capability, aliases)
- **TTPs** — `/lookup-crowdstrike ttps "Mustang Panda"` → ATT&CK technique IDs; resolve against `/mitre-attack`
- **Latest reporting** — `/lookup-crowdstrike reports --actor "Mustang Panda" --latest`
- **Actor population** — `/lookup-crowdstrike actors --origin china` to enumerate China-attributed adversaries CrowdStrike tracks (CrowdStrike uses the "Panda" cryptonym for PRC state-nexus actors)

Route through `/threat-actor-profiling` for a full structured profile. CrowdStrike report bodies are typically TLP:AMBER+ — cite report IDs internally, do not redistribute.

## Sources & References

1. CISA Advisory AA24-038A: "PRC State-Sponsored Actors Compromise and Maintain Persistent Access to U.S. Critical Infrastructure" (February 2024)
2. Microsoft Threat Intelligence: "Volt Typhoon targets US critical infrastructure with living-off-the-land techniques" (May 2023)
3. Mandiant APT41 Report: "Double Dragon: APT41, a Dual Espionage and Cyber Crime Operation" (2022)
4. CISA/FBI Joint Advisory: "People's Republic of China-Linked Actors Compromise Telecom Networks" (December 2024)
5. CrowdStrike 2025 Global Threat Report: China-nexus adversary activity analysis
6. Recorded Future Insikt Group: "Chinese State-Sponsored Cyber Espionage: Trends and Outlook" (2024)
7. DOJ Indictment: United States v. Zhang Haoran et al., APT41 members (September 2020)
8. Secureworks Counter Threat Unit: "Bronze Silhouette Targets U.S. Government and Defense Organizations" (2023)
9. CISA, NSA, FBI and partners, Advisory AA25-239A: "Countering Chinese State-Sponsored Actors Compromise of Networks Worldwide to Feed Global Espionage System" (27 August 2025, revised 3 September 2025). https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-239a
10. U.S. Department of the Treasury: "Treasury Sanctions Company Associated with Salt Typhoon and Hacker Associated with Treasury Compromise" (17 January 2025). https://home.treasury.gov/news/press-releases/jy2792
11. U.S. Department of the Treasury: "Treasury Sanctions China-based Hacker Involved in the Compromise of Sensitive U.S. Victim Networks" (5 March 2025). https://home.treasury.gov/news/press-releases/sb0042
12. U.S. Department of Justice: "Justice Department Charges 12 Chinese Contract Hackers and Law Enforcement Officers in Global Computer Intrusion Campaigns" (5 March 2025), read via the GlobalSecurity.org mirror. https://www.globalsecurity.org/security/library/news/2025/03/sec-250305-doj02.htm
13. Microsoft Threat Intelligence: "Silk Typhoon targeting IT supply chain" (5 March 2025). https://www.microsoft.com/en-us/security/blog/2025/03/05/silk-typhoon-targeting-it-supply-chain/
14. Cisco Talos: "Weathering the storm: In the midst of a Typhoon" (20 February 2025). https://blog.talosintelligence.com/salt-typhoon-analysis/
15. Recorded Future Insikt Group: "RedMike (Salt Typhoon) Exploits Vulnerable Cisco Devices of Global Telecommunications Providers" (2025). https://www.recordedfuture.com/research/redmike-salt-typhoon-exploits-vulnerable-devices
16. Microsoft Threat Intelligence: "Disrupting active exploitation of on-premises SharePoint vulnerabilities" (22 July 2025, updated 23 July 2025). https://www.microsoft.com/en-us/security/blog/2025/07/22/disrupting-active-exploitation-of-on-premises-sharepoint-vulnerabilities/
17. Google Threat Intelligence Group / Mandiant: BRICKSTORM espionage campaign report (September 2025). https://cloud.google.com/blog/topics/threat-intelligence/brickstorm-espionage-campaign
18. CISA, NSA and Canadian Centre for Cyber Security, Malware Analysis Report AR25-338A: "BRICKSTORM Backdoor" (4 December 2025, updated to 11 February 2026). https://www.cisa.gov/news-events/analysis-reports/ar25-338a
19. Google Threat Intelligence Group: "Mark Your Calendar: APT41 Innovative Tactics" (May 2025). https://cloud.google.com/blog/topics/threat-intelligence/apt41-innovative-tactics
20. Anthropic: "Disrupting the first reported AI-orchestrated cyber espionage campaign" (13 November 2025). https://www.anthropic.com/news/disrupting-AI-espionage
21. Cisco Talos: UAT-9686 campaign against Cisco Secure Email Gateway and Secure Email and Web Manager (17 December 2025). https://blog.talosintelligence.com/uat-9686/
22. CISA, NCSC-UK and partners, Advisory AA26-113A: "Defending Against China-Nexus Covert Networks of Compromised Devices" (23 April 2026). https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-113a
23. Proofpoint: "I'd come running back to EU again: TA416 resumes European government espionage campaigns" (1 April 2026). https://www.proofpoint.com/us/blog/threat-insight/id-come-running-back-eu-again-ta416-resumes-european-government-espionage
24. Kaspersky Securelist: "CoolClient backdoor goes deeper: HoneyMyte adds Windows kernel rootkit" (14 August 2026). https://securelist.com/honeymyte-coolclient-driver-rootkit/121028/
25. Lumen Black Lotus Labs: "Expanded JDY IoT and SOHO botnet enables rapid vulnerability exploitation" (10 June 2026). https://www.lumen.com/blog/en-us/expanded-jdy-iot-and-soho-botnet-enables-rapid-vulnerability-exploitation
26. The Record: "Norwegian intelligence discloses country hit by Salt Typhoon campaign" (6 February 2026). https://therecord.media/norawy-intelligence-discloses-salt-typhoon-attacks
27. TechCrunch: compilation of organisations and countries hit by Salt Typhoon (9 March 2026). https://techcrunch.com/2026/03/09/salt-typhoon-china-who-has-been-hacked-global-telecom-giants/
28. BleepingComputer: "Chinese hackers breached National Guard to steal network configurations" (17 July 2025), reporting a DHS memo of 11 June 2025. https://www.bleepingcomputer.com/news/security/chinese-hackers-breached-national-guard-to-steal-network-configurations/
29. The Record: "Volt Typhoon hackers were in Massachusetts utility's systems for 10 months" (12 March 2025), reporting a Dragos case study. https://therecord.media/volt-typhoon-hackers-utility-months
30. SecurityWeek: "China Admitted to Volt Typhoon Cyberattacks on US Critical Infrastructure: Report" (11 April 2025), reporting The Wall Street Journal. https://www.securityweek.com/china-admitted-to-us-that-it-conducted-volt-typhoon-attacks-report/
31. CyberScoop: "Chinese national extradited to US for pandemic-era Silk Typhoon attacks" (27 April 2026). https://cyberscoop.com/xu-zewei-extradited-china-national-silk-typhoon-hafnium/
32. CrowdStrike: 2026 Global Threat Report press release (24 February 2026). https://www.crowdstrike.com/en-us/press-releases/2026-crowdstrike-global-threat-report/
33. NSA, CISA and FBI, Advisory AA26-251A: "China-Based Artificial Intelligence Companies Conducting Industrial-Scale Distillation Campaigns Against U.S. AI Companies" (8 September 2026). https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-251a

## Change Log

| Date | Change | Source |
|---|---|---|
| 2026-04-05 | Initial cell creation; seeded with training knowledge through early 2025 | Training data |
| 2026-09-29 | First refresh covering January 2025 to September 2026. Rewrote Executive Summary; reframed Salt Typhoon as a global campaign per AA25-239A; added Silk Typhoon supply chain and UNC5221 BRICKSTORM campaigns; added Treasury compromise, ToolShell and AI-orchestrated campaign to Historical; added sanctions, indictments and the Xu Zewei extradition; added six actors and nine tooling rows; corrected Volt Typhoon attribution and the Fortinet product name; documented the APT27 / Silk Typhoon / UNC5221 naming conflict; added sources 9-33 | OSINT refresh |
