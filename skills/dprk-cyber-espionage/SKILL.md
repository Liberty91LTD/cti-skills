---
name: dprk-cyber-espionage
description: Use when the user asks about North Korean state-sponsored cyber operations or specific DPRK actors (Lazarus, APT38, BlueNoroff, Andariel, Kimsuky, etc.), revenue-generation campaigns, IT-worker schemes, or DPRK targeting of cryptocurrency / supply chain. Self-updating knowledge cell.
user-invocable: true
metadata:
  category: knowledge-cell
  created: 2026-04-05
  last_updated: 2026-09-29
  update_count: 1
  confidence: moderate
---

# DPRK Cyber Espionage Knowledge Cell

## Executive Summary

North Korea operates a uniquely structured cyber program where revenue generation and intelligence collection are equally prioritized national objectives. Most units sit under the Reconnaissance General Bureau (RGB); Japanese and U.S. authorities assess that the Contagious Interview (WaterPlum) operators and some IT workers instead operate under the 313 General Bureau of the Munitions Industry Department [24]. Chainalysis puts cumulative DPRK cryptocurrency theft at $6.75 billion through the end of 2025 [11]. The Multilateral Sanctions Monitoring Team (MSMT), which replaced the disbanded UN Panel of Experts as the main multilateral reporting body, published its first cyber and IT-worker report in October 2025 [16].

2025 was the largest year on record: Chainalysis attributes $2.02 billion in theft to the DPRK, a 51% increase on 2024 from far fewer known incidents, dominated by the $1.5 billion Bybit theft of February 2025 that the FBI attributed to TraderTraitor [9][11]. 2026 has continued at a lower but still high level. The April 2026 Drift Protocol (about $285 million) and KelpDAO (about $290 million) thefts and the 24 September 2026 Bitget theft ($351.6 million) are all assessed by blockchain analytics firms or the victims as likely DPRK operations, though none has yet been formally attributed by a government. If Bitget is confirmed, 2026 theft exceeds $1 billion [19][20][21][22][23].

Three trends define the period since early 2025. First, developer and open-source targeting has become the main access route: the Contagious Interview fake-interview campaign infected at least 30,000 devices in more than 100 countries between December 2025 and July 2026, and the March 2026 compromise of the axios npm package showed that DPRK operators can hijack packages with more than 100 million weekly downloads [17][18][24]. Second, the IT-worker scheme has drawn sustained enforcement (a coordinated U.S. action in June 2025, sanctions in March 2026, multinational alerts in July and September 2026) while expanding beyond the United States and adopting AI tools for identity fraud [13][14][15][24]. Third, espionage units continue to invest in capability: Lazarus used a Windows zero-day in its 2026 Operation Dream Job wave against defense firms, and Kimsuky compromised South Korean software vendors to reach their customers [26][27].

## Key Actors

Vendor naming overlaps heavily and "Lazarus Group" is often used as an umbrella term for several units. Aliases below are those confirmed in the cited reporting.

| Threat Actor | Aliases | Attribution | Primary Targets | Status |
|---|---|---|---|---|
| Lazarus Group | Diamond Sleet, HIDDEN COBRA, Zinc, Labyrinth Chollima, Nickel Academy | RGB 3rd Bureau | Defense, aerospace, cryptocurrency, banks | Active |
| APT38/BlueNoroff | Sapphire Sleet, Stardust Chollima, UNC1069, CageyChameleon, Alluring Pisces | RGB | Cryptocurrency firms and executives, open-source maintainers, banking | Active |
| Kimsuky | APT43, Emerald Sleet, Velvet Chollima, Thallium, Black Banshee | RGB 5th Bureau | South Korean government and software vendors, think tanks, academics, NK policy experts | Active |
| Andariel | APT45, Onyx Sleet, Stonefly, Silent Chollima, Plutonium, DarkSeoul | RGB 3rd Bureau | Defense, nuclear, aerospace, healthcare (ransomware) | Active |
| TraderTraitor | Jade Sleet, UNC4899 | RGB-linked | Cryptocurrency exchanges, wallet and bridge infrastructure providers | Active |
| Citrine Sleet | UNC4736, AppleJeus, Golden Chollima, Gleaming Pisces, DEV-0139 | RGB-linked | DeFi protocols, cryptocurrency traders, financial technology | Active |
| Contagious Interview | WaterPlum, UNC5342 | 313 General Bureau, Munitions Industry Department (NPA/FBI assessment) | Software developers, freelancers, Web3 and AI job seekers | Active |
| DPRK IT workers | Jasper Sleet (formerly Storm-0287) | Multiple DPRK entities incl. 313 General Bureau | Remote technology roles worldwide | Active |
| ScarCruft | Reaper, Ricochet Chollima, InkySquid, APT37 | MSS (State Security) | South Korean government, defectors, journalists, human rights | Active |

## Active Campaigns

### Cryptocurrency Exchange and DeFi Platform Theft (2023-Present)

DPRK operators remain the largest single source of cryptocurrency theft. Chainalysis attributes $2.02 billion to them in 2025 and notes that they accounted for 76% of all service compromises that year [11]. Confirmed and suspected operations in 2026:

- **Drift Protocol (1 April 2026)**: about $285 million drained in roughly 12 minutes after a social engineering effort that began in autumn 2025, with operators posing as a quantitative trading firm and meeting Drift contributors at conferences. Drift attributed it with medium confidence to UNC4736 (Citrine Sleet). TRM Labs describes DPRK involvement as likely; Elliptic gives the figure as $286 million and calls it suspected DPRK-linked [19][20][21].
- **KelpDAO (18 April 2026)**: about $290 million (Chainalysis: $292 million) taken by poisoning RPC nodes used by the LayerZero verifier and forcing failover with a DDoS attack. LayerZero's preliminary attribution is to TraderTraitor [22].
- **Bitget (24 September 2026)**: $351.6 million taken from hot wallets after attackers compromised a backend system and spoofed transaction data; private keys were not stolen. Bitget's CEO called DPRK involvement very likely. Elliptic assesses it as highly likely DPRK-linked. TRM Labs reports on-chain overlaps with Bybit laundering but has not definitively attributed it [23].

Totals differ by firm. TRM counted about $690 million attributed to the DPRK in 2026 before Bitget; Elliptic counts more than 51 incidents and over $1 billion including Bitget [23]. Laundering relies on rapid splitting into fresh wallets, cross-chain swaps and bridges, mixers, and Chinese-language money movement and guarantee services, with a typical cycle of about 45 days [11].

### Contagious Interview Developer Targeting (2023-Present)

Operators pose as recruiters for AI, cryptocurrency and NFT companies and instruct candidates to run malicious code during a coding test or while "fixing" a video-conferencing error. A joint advisory by Japanese, U.S., Australian and German agencies on 18 September 2026 states that the group infected at least 30,000 devices in more than 100 countries, took funds or credentials from over 7,000 cryptocurrency wallets, and transferred about $10.71 million to the DPRK. Malware is delivered through malicious npm packages and code repositories. The advisory also notes that some operators double as IT workers and that Japan dismantled its first identified laptop farm [24]. Google reported in October 2025 that the group (UNC5342) had used EtherHiding since February 2025, storing payloads in smart contracts on BNB Smart Chain and Ethereum, the first nation-state use of the technique Google had observed [25].

### Open-Source Package Compromise by BlueNoroff (2025-Present)

On 31 March 2026 attackers took over the axios npm maintainer account after a tailored social engineering approach and published two malicious versions that were live for about three hours. They installed a cross-platform backdoor through a fake dependency. Google attributes the compromise to UNC1069 and Microsoft to Sapphire Sleet [17][18]. In July 2026 Amazon attributed the axios compromise, the September 2025 hijack of the debug and chalk packages, and a March 2025 compromise of typo-crypto to the same actor with medium confidence. No other vendor has published an attribution for debug, chalk or typo-crypto [28]. Separately, Arctic Wolf attributed with high confidence a campaign against Web3 executives, first detected in January 2026, that used typo-squatted Zoom and Teams links, fake meetings populated with stolen or AI-generated video, and ClickFix clipboard injection [29].

### IT Worker Fraudulent Employment Scheme (2022-Present)

DPRK IT workers continue to obtain remote employment under false identities. They are mostly located in North Korea, China and Russia, with smaller numbers in Africa and Southeast Asia [13][24]. Revenue estimates vary: earlier UN reporting put it at $250-600 million annually, while the U.S. Treasury stated in March 2026 that the scheme generated nearly $800 million in 2024 [15]. Microsoft reports that the scheme now targets technology roles across industries globally and that workers use AI for document forgery, photo enhancement and voice changing [13]. Enforcement has intensified:

- **June 2025**: DOJ announced searches of 21 laptop farms in 14 states, seizure of 29 financial accounts and 21 websites, and charges in a scheme that placed workers at more than 100 U.S. companies and exposed ITAR-controlled data at a defense contractor. A separate indictment charged four DPRK nationals who stole over $900,000 from an Atlanta blockchain company while employed there [12].
- **July 2025**: Christina Chapman was sentenced to 102 months for running a laptop farm that served 309 U.S. businesses and generated $17 million [14].
- **March 2026**: OFAC designated six individuals and two entities, including Amnokgang Technology Development Company and facilitators in Vietnam and Laos [15].
- **July 2026**: eleven governments issued a joint alert on IT-worker tactics [30].

Chainalysis notes that IT workers embedded in cryptocurrency services are increasingly used to gain privileged access for theft, not only salary revenue [11].

### Lazarus Defense and Nuclear Espionage (2023-Present)

Lazarus Group and Andariel continue espionage against defense, aerospace and nuclear organizations. Check Point documented an Operation Dream Job wave running from early 2026 to July 2026 against defense-sector targets in Western Europe, India and South America, with emphasis on aerospace, drones, sensors and robotics. Fake job offers delivered a trojanized open-source PDF viewer or DLL sideloading chains. The operators used CVE-2026-68820, a Windows AFD.sys use-after-free, as a zero-day for privilege escalation; it was reported on 28 July 2026 and patched on 11 August 2026 [26]. Collected intelligence supports DPRK missile, nuclear, submarine and drone programs.

### Kimsuky Espionage and Vendor Compromise (2025-Present)

Kimsuky compromised South Korean groupware vendors in 2025 and early 2026, through a mail server vulnerability in one case and social engineering in another, then used stolen customer server information to reach the vendors' customers [27]. The FBI warned in January 2026 that Kimsuky uses QR codes in spearphishing against think tanks, academia and government, moving victims to unmanaged mobile devices and stealing session tokens to bypass MFA [31]. Genians documented Kimsuky's adoption of ClickFix lures during 2025 [32].

### Lazarus Overlap with Ransomware Operations (2024-Present)

Symantec reported in February 2026 that Lazarus tooling was used in Medusa ransomware intrusions against U.S. healthcare and Middle East organizations. The activity resembles Andariel (Stonefly) but the sub-group is unconfirmed [33]. In July 2026 South Korean agencies warned that Lazarus tools and infrastructure overlap with ransomware attacks on South Korean organizations; whether this reflects collaboration, shared infrastructure or access brokering is unresolved [34].

## Historical Campaigns

### Bybit Exchange Theft (2025)

On 21 February 2025 about $1.5 billion in Ethereum was taken from Bybit, the largest cryptocurrency theft on record. The FBI attributed it to TraderTraitor on 26 February 2025 [9]. The attackers compromised a Safe{Wallet} developer's macOS workstation on 4 February, used the developer's active AWS sessions to reach Safe{Wallet} infrastructure, and on 19 February modified JavaScript served to the wallet interface so that it altered transactions only when Bybit's cold wallet was the source. The code was removed two minutes after the theft [10].

### 3CX Supply Chain Attack (2023)

In March 2023 a DPRK actor compromised the build pipeline of 3CX, an enterprise VoIP/PBX provider. The intrusion began when a 3CX employee installed a trojanized X_TRADER application from Trading Technologies, itself the product of an earlier supply chain compromise. Mandiant described this as the first time it had seen one software supply chain attack lead to another, and attributed it to UNC4736, which it links with moderate confidence to AppleJeus activity; CrowdStrike attributed it to Labyrinth Chollima [3][8]. Malware included the TAXHAUL loader and COLDCAT downloader on Windows and the POOLRAT backdoor on macOS.

### Bangladesh Bank SWIFT Heist (2016)

APT38 attempted to steal $951 million from the Bangladesh Bank's account at the Federal Reserve Bank of New York by injecting fraudulent SWIFT transfer messages. A spelling error in one transfer request ("fandation" instead of "foundation") triggered scrutiny that limited actual losses to $81 million, which was routed through Philippine casinos. The operation demonstrated DPRK's willingness and ability to target the global financial infrastructure. The attack involved months of reconnaissance, custom SWIFT manipulation malware (NESTEGG, DYEPACK), and knowledge of bank clearing processes. It spurred a global overhaul of SWIFT security controls.

### Ronin Network/Axie Infinity Hack (2022)

In March 2022, Lazarus Group stole approximately $625 million in Ethereum and USDC from the Ronin Network, a blockchain bridge supporting the Axie Infinity game. The attack exploited compromised private keys of validator nodes, obtained through a social engineering campaign involving a fake job offer sent to a senior Sky Mavis engineer via LinkedIn. The FBI attributed the theft to Lazarus Group and Treasury's OFAC sanctioned the associated wallet addresses.

## TTP Evolution

DPRK cyber operations have undergone significant evolution:

- **Cryptocurrency Specialization**: From traditional banking (SWIFT) to exchanges, DeFi protocols, bridges and hot wallets. Since 2025 the largest thefts have targeted off-chain infrastructure around the asset (wallet interface code at Bybit, RPC nodes at KelpDAO, backend signing systems at Bitget) instead of smart contract flaws [10][22][23].
- **Fewer, Larger Thefts**: Chainalysis recorded a record total in 2025 from 74% fewer known attacks [11].
- **Long-Duration Social Engineering**: The Drift operation involved about six months of in-person and online relationship building, including a real deposit of over $1 million to build credibility [21].
- **Social Engineering via Professional Networks**: Fake recruiter and fake interview lures remain the primary initial access vector for both espionage and financial operations [24][26].
- **ClickFix and Fake Meetings**: Kimsuky and BlueNoroff both adopted ClickFix. BlueNoroff pairs it with fake video meetings built from stolen webcam footage and AI-generated imagery [29][32].
- **Supply Chain Attacks**: Progression from cascading vendor compromise (3CX) to hijacking maintainer accounts of widely used open-source packages (axios) and compromising regional software vendors to reach their customers [17][27].
- **Blockchain-Hosted Payloads**: EtherHiding places payloads in smart contracts, which resists takedown [25].
- **Zero-Day Use**: Lazarus exploited a Windows kernel driver zero-day in 2026 to deploy its FudModule rootkit [26].
- **Mobile Pivot for Credential Theft**: Kimsuky's QR-code phishing moves the victim to an unmanaged device and ends in session token replay [31].
- **macOS Targeting**: Continued development of macOS payloads, reflecting their prevalence among cryptocurrency developers. The Bybit chain began on a developer's Mac [10].
- **AI-Assisted Operations**: Documented use of AI for face swapping on identity documents, voice changing, text-to-speech and translation in IT-worker and interview fraud [13][24].
- **Insider Threat Model**: The IT worker scheme obtains legitimate authorized access, and is now also used to enable theft from cryptocurrency firms [11][12].
- **Rapid Laundering**: TRM Labs observed Drift proceeds bridged within hours at a pace exceeding the Bybit laundering [19].

## Infrastructure Patterns

- VPN services and commercial proxy networks for operator anonymity; Astrill VPN recurs in vendor attribution [17]
- Compromised web servers used as C2 relays, including PHP webshells on legitimate sites [26]
- GitHub, Bitbucket and other code repositories for malware delivery via fake projects [24]
- Malicious npm packages and hijacked legitimate packages for supply chain delivery [17][24]
- Public blockchains (BNB Smart Chain, Ethereum) as payload hosting [25]
- Legitimate cloud services as C2, including Microsoft Graph/OneDrive and Google Drive [26][27]
- Typo-squatted Zoom, Teams and npm lookalike domains [28][29]
- Use of legitimate communication platforms (Telegram, Slack, Discord) for victim contact and exfiltration
- Cross-chain swap services, bridges, mixers and Chinese-language guarantee services for laundering [11]
- Laptop farms at facilitators' residences in the United States and, since 2026, Japan, plus facilitator-managed VPS [12][24]
- VoIP numbers and virtual phone services for synthetic identity support

## Tooling

| Tool | Type | Associated Actors | Notes |
|---|---|---|---|
| AppleJeus | Cryptocurrency trojan | Citrine Sleet (UNC4736), Lazarus | Trojanized crypto trading apps targeting macOS and Windows |
| HOPLIGHT | Backdoor | Lazarus | Custom tunneling tool for proxy communications |
| BLINDINGCAN/DTrack | RAT | Lazarus, Andariel | Blindingcan seen again in 2026 Medusa-linked intrusions [33] |
| TAXHAUL / COLDCAT / POOLRAT | Loader, downloader, macOS backdoor | UNC4736 | 3CX compromise; SIMPLESEA was later determined by Mandiant to be POOLRAT [8] |
| BeaverTail | Infostealer | Contagious Interview (WaterPlum) | JavaScript stealer delivered in npm packages and repositories |
| InvisibleFerret | Backdoor | Contagious Interview (WaterPlum) | Python backdoor deployed alongside BeaverTail |
| OtterCookie / OtterCandy | RAT and stealer | Contagious Interview (WaterPlum) | JavaScript-based; OtterCandy combines OtterCookie with RATatouille features [24] |
| StoatWaffle | Modular loader/RAT | Contagious Interview (WaterPlum) | Node.js; abuses VS Code project configuration for auto-run [24] |
| JADESNOW | Downloader | UNC5342 | Fetches payloads from smart contracts (EtherHiding) [25] |
| WAVESHAPER.V2 / SILKBELL | Backdoor and dropper | UNC1069 (Sapphire Sleet) | Delivered through the axios compromise; Windows, macOS, Linux [17] |
| MISTPEN | Downloader | Lazarus | In-memory; retrieves modules via Microsoft Graph API [26] |
| Troy | Backdoor | Lazarus | New modular backdoor seen in 2026 Dream Job wave [26] |
| FudModule | Kernel rootkit | Lazarus | v3.1 exploited CVE-2026-68820; tampers with EDR and Smart App Control [26] |
| Comebacker | Backdoor/loader | Lazarus | Used in Medusa-linked intrusions [33] |
| Gomir | Backdoor | Kimsuky | New variants used against South Korean groupware vendors [27] |
| BabyShark | Script-based malware | Kimsuky | Delivered through ClickFix lures in 2025 [32] |
| FastCash | ATM malware | APT38 | Intercepts ISO 8583 transactions to authorize fraudulent cash withdrawals |
| ELECTRICFISH | Tunneling | Lazarus | Custom tunneling/proxy tool for maintaining covert communications |
| KANDYKORN | macOS backdoor | BlueNoroff | Full-featured macOS RAT targeting crypto developers |
| RandomQuery/FlowerPower | Reconnaissance | Kimsuky | Information collection tools deployed via spear-phishing |

## Intelligence Gaps

- **Attribution of 2026 thefts**: Drift, KelpDAO and Bitget attributions rest on victim, vendor and blockchain-analytics assessments. No government attribution was found for any of them as of 2026-09-29. Some press reporting gives a higher Bitget figure (about $387 million) than the $351.6 million reported by Bitget and TRM Labs; this was not reconciled.
- **MSMT report detail**: The October 2025 MSMT report was confirmed through the joint statement only; the full report could not be retrieved, so its figures are not cited here.
- **npm attribution**: Amazon's medium-confidence attribution of the debug, chalk and typo-crypto compromises to Sapphire Sleet is not corroborated by another vendor [28].
- **Ransomware relationship**: Whether Lazarus-linked activity in Medusa and other ransomware intrusions reflects tasking, moonlighting, tool sharing or access brokering is unknown [33][34].
- **Full IT worker infiltration scope**: The true number of DPRK IT workers employed at foreign companies and the extent of their access is unknown. Revenue estimates range from $250 million to nearly $800 million a year.
- **Cryptocurrency laundering networks**: The network of OTC brokers and conversion services is only partially mapped.
- **Revenue allocation**: How stolen funds flow to weapons programs, leadership and operational reinvestment is poorly characterized.
- **Organizational structure**: The relationship between RGB units and the 313 General Bureau of the Munitions Industry Department, and how vendor cluster names map to either, is not settled in open sources.
- **Zero-day capability**: Lazarus used a Windows zero-day in 2026 [26], but whether such exploits are developed internally or acquired is unclear.
- **AI tool adoption**: Identity fraud uses are documented. Reports of Kimsuky building local LLM environments and of AI-assisted exploit development were seen in secondary reporting but not verified against a primary source in this refresh.
- **Unverified leads**: Reports of a Linux backdoor in trojanized HAProxy builds at South Korean organizations, DPRK-linked malicious Terraform providers and Go modules, and ScarCruft and Andariel activity in 2026 were not reviewed; those actor entries are unchanged from the seed text.

## Live enrichment

When CrowdStrike Falcon Intelligence credentials are configured (`$CROWDSTRIKE_CLIENT_ID`), pull live vendor intelligence to keep this cell current and to answer specific actor questions:

- **Actor profile** — `/lookup-crowdstrike actor "Lazarus"` / `actor "Labyrinth Chollima"` (origins, target countries/industries, motivations, capability, aliases)
- **TTPs** — `/lookup-crowdstrike ttps "Lazarus"` → ATT&CK technique IDs; resolve against `/mitre-attack`
- **Latest reporting** — `/lookup-crowdstrike reports --actor "Stardust Chollima" --latest`
- **Actor population** — `/lookup-crowdstrike actors --origin north-korea` to enumerate DPRK-attributed adversaries CrowdStrike tracks (CrowdStrike uses the "Chollima" cryptonym for DPRK state-nexus actors)

Route through `/threat-actor-profiling` for a full structured profile. CrowdStrike report bodies are typically TLP:AMBER+ — cite report IDs internally, do not redistribute.

## Sources & References

1. FBI/CISA/Treasury Joint Advisory: "TraderTraitor: North Korean State-Sponsored APT Targets Blockchain Companies" (April 2022)
2. Mandiant: "APT43: North Korean Group Uses Cybercrime to Fund Espionage Operations" (28 March 2023; title corrected 2026-09-29) https://cloud.google.com/blog/topics/threat-intelligence/apt43-north-korea-cybercrime-espionage
3. CrowdStrike: "LABYRINTH CHOLLIMA's 3CX Supply Chain Operation" (April 2023)
4. Chainalysis: "2024 Crypto Crime Report: North Korea-Linked Cryptocurrency Theft" (2024)
5. Microsoft Threat Intelligence: "Diamond Sleet supply chain compromise distributes a modified CyberLink installer" (November 2023)
6. UN Panel of Experts Report S/2024/215: DPRK sanctions implementation findings on cyber-enabled theft
7. FBI Public Service Announcement: "North Korean IT Workers Infiltrate U.S. Companies" (October 2023)
8. Mandiant: "3CX Software Supply Chain Compromise Initiated by a Prior Software Supply Chain Compromise; Suspected North Korean Actor Responsible" (20 April 2023; title corrected 2026-09-29) https://cloud.google.com/blog/topics/threat-intelligence/3cx-software-supply-chain-compromise
9. FBI: "North Korea Responsible for $1.5 Billion Bybit Hack" (26 February 2025) https://www.ic3.gov/psa/2025/psa250226
10. Sygnia: "Sygnia's Investigation into the Bybit Hack: What We Know So Far" (2025) https://www.sygnia.co/blog/sygnia-investigation-bybit-hack/
11. Chainalysis: "2025 Crypto Theft Reaches $3.4 Billion" (18 December 2025) https://www.chainalysis.com/blog/crypto-hacking-stolen-funds-2026/
12. U.S. Department of Justice: "Justice Department Announces Coordinated, Nationwide Actions to Combat North Korean Remote Information Technology Workers' Illicit Revenue Generation Schemes" (30 June 2025) https://www.justice.gov/opa/pr/justice-department-announces-coordinated-nationwide-actions-combat-north-korean-remote
13. Microsoft Threat Intelligence: "Jasper Sleet: North Korean remote IT workers' evolving tactics to infiltrate organizations" (30 June 2025) https://www.microsoft.com/en-us/security/blog/2025/06/30/jasper-sleet-north-korean-remote-it-workers-evolving-tactics-to-infiltrate-organizations/
14. The Register: "Laptop farmer behind $17M North Korean IT worker scam locked up for 8.5 years" (24 July 2025) https://www.theregister.com/2025/07/24/laptop_farmer_north_korean_it_scam_sentenced/
15. U.S. Department of the Treasury: "Treasury Sanctions Facilitators of DPRK IT Worker Fraud Targeting U.S. Businesses" (12 March 2026) https://home.treasury.gov/news/press-releases/sb0416
16. U.S. Department of State (mirrored by GlobalSecurity.org): "Joint Statement of the Multilateral Sanctions Monitoring Team (MSMT) on the Report Covering DPRK Cyber and IT Worker Activities" (22 October 2025) https://www.globalsecurity.org/wmd/library/news/dprk/2025/dprk-251022-state01.htm
17. Google Threat Intelligence Group: "North Korea-Nexus Threat Actor Compromises Widely Used Axios NPM Package in Supply Chain Attack" (1 April 2026) https://cloud.google.com/blog/topics/threat-intelligence/north-korea-threat-actor-targets-axios-npm-package
18. Microsoft Threat Intelligence: "Mitigating the Axios npm supply chain compromise" (1 April 2026) https://www.microsoft.com/en-us/security/blog/2026/04/01/mitigating-the-axios-npm-supply-chain-compromise/
19. TRM Labs: "North Korean Hackers Attack Drift Protocol In USD 285 Million Heist" (2 April 2026) https://www.trmlabs.com/resources/blog/north-korean-hackers-attack-drift-protocol-in-285-million-heist
20. Elliptic: "Drift Protocol exploited for $286 million in suspected DPRK-linked attack" (April 2026) https://www.elliptic.co/insights/drift-protocol-exploited-for-286-million-in-suspected-dprk-linked-attack/
21. The Hacker News: "$285 Million Drift Hack Traced to Six-Month DPRK Social Engineering Operation" (5 April 2026, reporting Drift's own disclosure) https://thehackernews.com/2026/04/285-million-drift-hack-traced-to-six.html
22. LayerZero: "KelpDAO Incident Statement" (April 2026) https://layerzero.network/blog/kelpdao-incident-statement ; Chainalysis: "Inside the KelpDAO Bridge Exploit" (23 April 2026) https://www.chainalysis.com/blog/kelpdao-bridge-exploit-april-2026/
23. TRM Labs: "Bitget Loses USD 351.6 Million in Hot Wallet Breach in Likely North Korea Attack" (25 September 2026) https://www.trmlabs.com/resources/blog/bitget-loses-usd-3516-million-in-hot-wallet-breach-in-likely-north-korea-attack ; Elliptic: "Bitget attack pushes suspected North Korea crypto heists over $1 billion in 2026" (25 September 2026) https://www.elliptic.co/insights/bitget-attack-pushes-suspected-north-korea-crypto-heists-over-1-billion-in-2026/
24. NPA, NCO (Japan), FBI, DC3, ASD's ACSC, BND, BfV: "North Korean 'WaterPlum,' commonly referred to as 'Contagious Interview,' Cyber Actor Group Targeting IT Professionals; Activities of North Korean IT Workers in Japan, the United States and Europe" (18 September 2026) https://www.ic3.gov/CSA/2026/260918.pdf
25. Google Threat Intelligence Group: "DPRK Adopts EtherHiding" (17 October 2025) https://cloud.google.com/blog/topics/threat-intelligence/dprk-adopts-etherhiding
26. Check Point Research: "Shattering the Dream: When a Job Offer Becomes a Zero-Day Attack" (11 August 2026) https://research.checkpoint.com/2026/shattering-the-dream-when-a-job-offer-becomes-a-zero-day-attack/
27. ENKI: "Analysis of Kimsuky's Attack on a South Korean Groupware Vendor Using a New Gomir Family Variant" (20 July 2026) https://www.enki.co.kr/en/media-center/blog/analysis-of-kimsuky-s-attack-on-a-south-korean-groupware-vendor-using-a-new-gomir-family-variant ; The Record: "New Kimsuky campaign compromised South Korean software vendors" (22 July 2026) https://therecord.media/kimsuky-north-korea-espionage-groupware-companies
28. Amazon Threat Intelligence: "Amazon identifies North Korean hacker group behind open-source supply chain attacks" (29 July 2026) https://aws.amazon.com/blogs/security/amazon-identifies-north-korean-hacker-group-behind-open-source-supply-chain-attacks/ ; The Hacker News: "Amazon Links Debug and Chalk npm Hijack to North Korea's Sapphire Sleet" (29 July 2026) https://thehackernews.com/2026/07/amazon-links-debug-and-chalk-npm-hijack.html
29. Arctic Wolf Labs: "BlueNoroff Uses ClickFix, Fileless PowerShell, and AI-Generated Fake Zoom Meetings to Target Web3 Sector" (27 April 2026) https://arcticwolf.com/resources/blog/bluenoroff-uses-clickfix-fileless-powershell-and-ai-generated-zoom-meetings-to-target-web3-sector/
30. Baker McKenzie Sanctions and Export Controls Blog: "Multiple Governments Issue Joint Alert on North Korean IT Workers" (2026, summarising the 31 July 2026 alert) https://sanctionsnews.bakermckenzie.com/multiple-governments-issue-joint-alert-on-north-korean-it-workers/
31. FBI FLASH AC-000001-MW: "North Korean Kimsuky Actors Leverage Malicious QR Codes in Spearphishing Campaigns Targeting U.S. Entities" (8 January 2026) https://www.ic3.gov/CSA/2026/260108.pdf
32. Genians Security Center: "Analysis of the threat case of kimsuky group using 'ClickFix' tactic" (1 July 2025) https://www.genians.co.kr/en/blog/threat_intelligence/suky-castle
33. Symantec (Broadcom): "North Korean Lazarus Group Now Working With Medusa Ransomware" (24 February 2026) https://www.security.com/threat-intelligence/lazarus-medusa-ransomware
34. The Record: "North Korea's Lazarus Group sharing tools with ransomware hackers, South Korean agencies warn" (30 July 2026) https://therecord.media/north-korea-hackers-ransomware
35. Mandiant: "APT45: North Korea's Digital Military Machine" (26 July 2024) https://cloud.google.com/blog/topics/threat-intelligence/apt45-north-korea-digital-military-machine
36. MITRE ATT&CK: "Lazarus Group (G0032)" https://attack.mitre.org/groups/G0032/

## Change Log

| Date | Change | Source |
|---|---|---|
| 2026-04-05 | Initial cell creation; seeded with training knowledge through early 2025 | Training data |
| 2026-09-29 | Refresh covering January 2025 to September 2026: rewrote Executive Summary; added Bybit detail (moved to Historical), 2026 thefts (Drift, KelpDAO, Bitget), Contagious Interview/WaterPlum, axios and npm compromises, IT-worker enforcement, Operation Dream Job zero-day, Kimsuky vendor compromise and QR phishing, ransomware overlap; corrected actor aliases, 3CX attribution and malware, BeaverTail/InvisibleFerret association, and two source titles | OSINT refresh |
