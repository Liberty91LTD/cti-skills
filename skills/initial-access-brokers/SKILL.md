---
name: initial-access-brokers
description: Use when the user asks about initial access brokers (IABs), the access-listing market, ransomware-feeding-IAB pipelines, specific broker handles, or how access is priced and packaged. Self-updating knowledge cell.
user-invocable: true
metadata:
  category: knowledge-cell
  created: 2026-04-05
  last_updated: 2026-09-29
  update_count: 1
  confidence: moderate
---

# Initial Access Brokers

## Executive Summary

Initial Access Brokers (IABs) are specialized cybercriminal actors who gain unauthorized access to corporate networks and sell or hand that access to other threat actors, most commonly ransomware and data-extortion crews. They decouple the intrusion phase from the monetization phase, which lets buyers skip the slowest part of an attack. The model is unchanged; the venues, the prices and the way vendors track brokers all changed materially between 2025 and 2026.

The forum landscape the market relied on has been broken up. The alleged administrator of XSS was arrested in Kyiv on 22 July 2025 and the forum's clear-web domains were seized; a site under the XSS name returned under a new administrator, but former moderators left to found DamageLib and trust in XSS has not recovered [9][10][11]. BreachForums lost its domains to an FBI seizure in October 2025 and has since split into competing successors [12]. RAMP, the one major forum that openly permitted ransomware advertising, was seized by the FBI on 28 January 2026 and its administrator said he would not rebuild it [13][14]. Of the three forums this cell previously named as the core venues, only Exploit is still operating without a known disruption. Ransomware actors have dispersed to newer forums such as Rehub and T1erOne rather than consolidating on one successor, and both XSS and Exploit have restated their bans on ransomware activity [13].

Pricing data is vendor-specific and the two most recent Rapid7 datasets are not directly comparable. For the second half of 2024 Rapid7 reported an average base price of just over $2,700 across Exploit, XSS and BreachForums, with nearly 40% of offers priced between $500 and $1,000 [15][16]. For 2025, with DarkForums and RAMP added to the dataset, Rapid7 reported an average base price of $113,275, which it attributes largely to very high-value listings on DarkForums [17]. Most listings bundle a privilege level with the access vector: 71.4% in the 2024 data, and domain admin in roughly a third of 2025 listings that stated a privilege [16][17].

Vendor reporting increasingly describes brokers that never post a public listing. Cisco Talos proposed splitting "initial access groups" into financially motivated, state-sponsored and opportunistic categories [18]. Reporting in 2026 describes access operations tied directly to specific extortion programs: the FortiBleed credential-harvesting operation linked to INC Ransom and Lynx [22], a broker affiliated with Payouts King [23], and Microsoft-tracked Storm-3121, whose voice-phishing access leads to ShinyHunters and Falcon extortion [24]. The infostealer log pipeline and exploitation of internet-facing appliances remain the two main supply mechanisms, with social engineering of identity and SaaS access now a third.

## Key Actors

| Actor/Handle | Forum Presence | Notable Characteristics | Status |
|-------------|---------------|------------------------|--------|
| ToyMaker (UNC961) | None reported (direct handoff) | Financially motivated; exploits internet-facing servers, deploys custom LAGTOY backdoor; handed access to Cactus about three weeks after compromise in a 2023 intrusion [18][19] | Tracked by Cisco Talos (2025 reporting) |
| UNC5174 | Not stated | Talos example of an "opportunistic" access group that sells access to state-sponsored actors [18] | Tracked (2025 reporting) |
| ShroudedSnooper (UNC1860) | None (state-sponsored) | Talos example of state-sponsored initial access; hands off to other Iranian-aligned groups [18] | Tracked (2025 reporting) |
| FortiBleed operation | Not stated | Russian-speaking; SSH brute force and FortigateSniffer credential interception on FortiGate firewalls; about 20 people; operator seen working INC Ransom and Lynx panels (SOCRadar, via SecurityWeek) [22] | Active (reported July 2026) |
| Payouts King-affiliated broker | Not stated | Microsoft Teams IT-impersonation lures; malicious Edge extension "Edgecution" with Python backdoor (Zscaler) [23] | Active (reported June 2026) |
| Storm-3121 | Not stated | Helpdesk-themed voice and text lures to personal phones, AiTM and device-code phishing; access leads to ShinyHunters and Falcon extortion (Microsoft) [24] | Active since May 2026 |
| Storm-3032 | Not stated | Splintered from BlackFile; same access technique, now extorts under the Helix name rather than brokering (Microsoft) [24] | Active since May 2026 |
| Unnamed Russian-speaking operator | Not stated | Exposed server showed exploitation of at least 12 CVEs in edge products; victims later claimed by RansomHouse and Tengu; also collected against Ukrainian defense and aerospace targets (CloudSEK) [21] | Reported August 2026 |
| ALP-001 | Not stated | ReliaQuest assesses it may be a broker moving to monetize intrusions directly [25] | Reported April 2026 |
| BigBro / Big-Bro, lacrim | Forums in Rapid7 dataset | Named by Rapid7 as prominent sellers in its 2025 data [17] | Active in 2025 |
| Aleksei Volkov ("chubaka.kor", "nets") | — | Broker for Yanluowang, paid a share of ransoms; sentenced to 81 months [26][27] | Imprisoned (March 2026) |
| Feras Albashiti ("r1z") | XSS, Exploit and others per KELA [29] | Sold access to at least 50 networks to an undercover officer; pleaded guilty [28] | In US custody; pleaded guilty January 2026 |
| IntelBroker (Kai West) | BreachForums | Described by Rapid7 as a formerly dominant seller; apprehended and charged in the US [17] | Arrested |
| Zebra2104, Sang_real (Frapochka), JETKITTEN, Roblette, montns, Bostaurus | Exploit, XSS, RAMP (as seeded) | Handles from the April 2026 seed; no 2025-2026 source found for any of them | Unverified; do not treat as active |
| Various Telegram-based brokers | Telegram channels | Lower-tier access; often direct from infostealer operators | Unverified in this refresh |
| Multiple unattributed IABs | Private channels | Operate through private deals with ransomware groups | Unknown |

Note: IAB handles change frequently. Actors rebrand, retire, and new actors enter the market regularly. Vendor cluster names (Storm-, UNC, ToyMaker) describe tracked activity, not forum handles, and the two rarely map onto each other in public reporting.

## Current Activity

### Forum Disruption and Dispersal (July 2025-2026)
Three of the main access-trading venues were disrupted within six months. After the XSS administrator's arrest, a new administrator moved the forum to new infrastructure in early August 2025; eight moderators publicly stated their distrust and launched DamageLib, which KELA counted at 33,487 registered users by 27 August 2025 (about 66% of XSS's membership) but with far lower posting activity than XSS before the arrest [10][11]. Intel 471 noted that most of the forum's escrow cryptocurrency was no longer accessible and assessed a broader shift toward decentralized, invite-only venues [10]. After the RAMP seizure, Rapid7 observed ransomware actors spreading across Rehub (active since August 2025, low entry barrier) and T1erOne (launched February 2026, vetted or paid entry) [13]. BreachForums successors PwnForums and Breached were competing for the English-language user base as of mid-2026 [12]. In Rapid7's 2025 dataset of 530 access threads, DarkForums (221) and RAMP (208) carried most of the volume, against Exploit (53), BreachForums (30) and XSS (18) [17]. Where RAMP's share went after January 2026 has not been measured publicly.

### Brokers Tied to Specific Extortion Programs
Several 2026 reports describe access operations with a direct operational link to a ransomware or extortion brand rather than open-market sales. SOCRadar found an operator with access to FortiBleed infrastructure working negotiation panels for both INC Ransom and Lynx; the operation had scanned 11,250 FortiGate portals, gained administrative access to 409 and recorded 12 ransomware deployments [22]. Zscaler linked the Edgecution campaign to a broker affiliated with Payouts King [23]. Microsoft reported that the helpdesk-impersonation activity it has tracked since May 2026 is used by Storm-3121, Storm-3032 and others; Microsoft describes this as initial access activity and does not itself use the term "broker" [24].

### Social Engineering for Identity and Cloud Access
Voice and chat-based impersonation of IT staff is now a documented access-acquisition method alongside credential theft and exploitation. The Microsoft-reported campaign calls employees on personal phones with a passkey-reset pretext, then uses adversary-in-the-middle or device-code phishing to obtain sessions and registers attacker MFA methods [24]. The Payouts King-affiliated broker starts with Microsoft Teams messages [23]. The product sold or handed over in these cases is an authenticated cloud identity, not a network foothold.

### Vulnerability Exploitation for Mass Access Harvesting
Exploitation of edge devices continues to supply access at scale. CloudSEK's analysis of an exposed broker server found staged exploits for at least 12 vulnerabilities across Fortinet, F5, Citrix, SonicWall, Sophos, SAP and other products, mostly unmodified public proof-of-concept code, with victims appearing on ransomware leak sites weeks after they appeared in the operator's records [21]. FortiBleed shows a variant that needs no vulnerability: brute-forced administrative access followed by passive credential interception on the firewall itself [22]. Earlier exploited products (Citrix Bleed, Ivanti Connect Secure, ScreenConnect, PAN-OS) are covered under Historical Events.

### Crime and State Overlap
Talos argues that the "broker" label hides different motivations and that handoffs between a financially motivated access group and a ransomware crew can be mistaken for one actor [18]. CloudSEK's exposed-server case is a concrete example: the same operator prepared access for ransomware buyers and ran Sliver-based collection against Ukrainian defense and aerospace organizations [21].

### Infostealer Log-to-Access Pipeline
Brokers continue to filter corporate VPN and SSO credentials from infostealer logs, validate them and list the resulting access. Analysis of the Black Basta leak found the group drew credentials from infostealer logs as well as buying access from brokers on underground forums [20]. Stealer families and log markets are tracked in the infostealers cell; this refresh did not find a current, vendor-attributed measurement of how much IAB inventory originates from logs.

## Historical Events

| Date | Event | Impact |
|------|-------|--------|
| 2019-2020 | IAB market formalization | Dedicated access trading sections established on major forums (Exploit, XSS) |
| 2020 | RDP access sales surge during COVID | Remote work expansion massively increased available RDP/VPN attack surface |
| Feb 2022 | Conti leaks expose IAB purchases | Internal chat logs showed Conti's systematic purchase of access from IABs |
| 2022-2023 | RAMP forum gains prominence | Became significant IAB marketplace after its 2021 launch, attracting new sellers |
| Late 2023 | Citrix Bleed mass exploitation | CVE-2023-4966 exploited at scale; access to affected orgs appeared on forums within weeks |
| Jan 2024 | Ivanti Connect Secure mass exploitation | Multiple zero-days in VPN appliance exploited for broad access harvesting |
| Jan 2024 | Volkov arrested in Italy | Yanluowang broker later extradited to the US [27] |
| Jul 2024 | Albashiti ("r1z") extradited from Georgia | Identified after selling access to an undercover officer in May 2023 [28] |
| Feb 2025 | Black Basta chat logs leaked | About 197,000 messages covering 2023-2024; confirmed purchases from IABs on forums [20] |
| Apr-May 2025 | Talos publishes ToyMaker and IAB taxonomy | Documented a broker-to-Cactus handoff and proposed FIA/SIA/OIA categories [18][19] |
| Jun 2025 | French arrests of ShinyHunters members tied to BreachForums | Four arrests; preceded the forum's later seizure [30] |
| 22 Jul 2025 | Alleged XSS administrator arrested in Kyiv | French-led investigation with Ukraine and Europol; clear-web domains seized; suspect allegedly earned over EUR 7 million [9][10] |
| Aug 2025 | XSS relaunch and DamageLib split | Moderators left XSS over fears of law-enforcement control [10][11] |
| Oct 2025 | FBI seizes BreachForums domains | Led to competing successor forums in 2026 [12] |
| Late 2025 | Volkov pleads guilty | DOJ gives the plea date as 25 November 2025 [26] |
| Jan 2026 | Albashiti pleads guilty | Sentencing was scheduled for 11 May 2026; outcome not confirmed [28] |
| 28 Jan 2026 | FBI seizes RAMP | Tor and clear-web sites replaced by seizure notice; no DOJ statement at the time of reporting; administrator "Stallman" confirmed the seizure [13][14] |
| 23 Mar 2026 | Volkov sentenced to 81 months | Ordered to pay $9,167,198.19 in restitution [26] |
| Mid-Jun 2026 | FortiBleed operation uncovered | Exposed by an operator OPSEC error; active since at least February 2026 [22] |

## TTP Evolution

**Access Acquisition Methods**:
- *2019-2021*: Predominantly RDP brute-forcing, VPN credential stuffing from data breaches, and exploitation of common vulnerabilities (BlueKeep, Exchange ProxyLogon/ProxyShell).
- *2022-2023*: Shift toward infostealer log harvesting as primary credential source; increasing exploitation of VPN/edge device vulnerabilities.
- *2024-2025*: Pipeline combining automated infostealer log processing with rapid exploitation of newly disclosed vulnerabilities in edge infrastructure. Some IABs specialize in one method or the other.
- *2026*: Helpdesk impersonation by voice, text and Microsoft Teams used to obtain cloud sessions and endpoint footholds [23][24]; credential interception on compromised firewalls [22]; continued reliance on public exploit code for edge devices [21].

**Access Types Sold**:
- *RDP/VPN credentials*: Most common. RDP was 21.2% and VPN 12.8% of offers in Rapid7's 2025 data; VPN led at 23.5% in its 2024 data [15][17].
- *RDWeb*: 11.2% of offers in Rapid7's 2025 data [17].
- *Web shells*: Pre-deployed persistent access; common from vulnerability exploitation campaigns.
- *Domain user / domain admin*: In Rapid7's 2025 data, domain user was 42.9% and domain admin 32.1% of stated privilege levels [17].
- *Citrix/Remote Desktop Gateway*: Provides access to virtualized environments with broader reach.
- *Cloud/SaaS access*: Authenticated Microsoft 365 sessions obtained by social engineering are now handed to extortion groups [24].
- *MSP/RMM access*: High value due to downstream access to MSP clients; treated as premium listings.

**Pricing Factors**: Access pricing correlates with: victim revenue (strongest factor), access type and privilege level, country (the US was 30.9% of listings in Rapid7's 2025 data [17]), sector, network size, and whether security tools were observed. Forum reputation and seller track record also affect willingness to pay. Auction formats are sometimes used for high-value access. Not all brokers sell at a fixed price: Volkov was paid a percentage of ransoms collected [27].

**Operational Security**: Established IABs use forum escrow services to protect both parties. Listings avoid naming victims directly, instead providing country, sector, revenue, number of hosts, and access type. Communication for sensitive details moves to encrypted messengers (Tox, Jabber/XMPP). The XSS case showed the exposure this creates: the arrested administrator is also suspected of running a private messaging service used by forum members, and forum-held deposits were largely lost [9][10]. Both prosecuted brokers were identified through reuse of personal accounts and identifiers [27][28].

## Ecosystem & Infrastructure Patterns

**Forum Marketplace Structure**: Access trading has historically run through dedicated forum sections with escrow and reputation systems. As of September 2026: Exploit is operating; XSS is operating under a new administrator with reduced trust; DamageLib is operating as an XSS splinter; RAMP is seized; BreachForums is seized and succeeded by rival forums; DarkForums carried the largest share of access threads in Rapid7's 2025 data [10][11][12][13][17]. Seller reputation no longer transfers cleanly between venues, and forum administrators have themselves become a point of failure.

**Supply Chain Position**: IABs sit between initial compromise and monetization. Upstream suppliers include infostealer operators, exploit developers and botnet operators. Downstream customers include ransomware affiliates (primary buyers), data theft and extortion groups, and in some cases state-sponsored actors [18]. ReliaQuest notes that some brokers may be moving to extort victims directly because selling access alone yields lower returns [25].

**Seasonal and Event-Driven Patterns**: Access listings spike following major vulnerability disclosures in edge devices, as IABs race to exploit and list access before victims patch. Listing volumes also correlate with infostealer campaign waves. Forum seizures cause short-term displacement rather than a lasting drop in supply [13].

**Quality Assurance**: Sophisticated IABs confirm that access was validated recently, and some offer replacement if access becomes invalid shortly after sale. Detailed victim environment information (domain structure, security tools observed, number of hosts) helps buyers assess the opportunity.

**Pricing Benchmarks**: The ranges below are the April 2026 seed estimates and are not tied to a single dataset. Treat them as indicative. For sourced figures use Rapid7: average base price just over $2,700 with nearly 40% of offers at $500-$1,000 (H2 2024; Exploit, XSS, BreachForums) [15][16], and average base price $113,275 (2025; five forums including DarkForums and RAMP) [17]. The second figure is an average pulled up by high-value listings and a changed forum set, not evidence that typical access became forty times more expensive.

| Access Type | Typical Price Range | Notes |
|------------|-------------------|-------|
| Basic RDP (single host, SMB) | $500-$2,000 | Most commoditized |
| VPN credentials (enterprise) | $1,000-$5,000 | Varies by company size |
| Domain Admin access | $5,000-$30,000 | Premium; ready for deployment |
| Citrix/RDS Gateway | $2,000-$10,000 | Broader network reach |
| MSP/RMM access | $5,000-$50,000+ | Multiplier effect on downstream clients |
| Fortune 500 / high revenue | $10,000-$50,000+ | Revenue-dependent premium |
| Web shell (large org) | $1,000-$5,000 | Requires further escalation |
| Cloud admin (M365/AWS) | $1,000-$10,000 | No current sourced benchmark |

## Tooling

| Tool | Category | Usage |
|------|----------|-------|
| Russian Market / 2easy | Log Sourcing | Purchasing infostealer logs to extract corporate credentials (status tracked in the infostealers cell) |
| Shodan/Censys | Reconnaissance | Identifying internet-exposed VPN/RDP/Citrix infrastructure |
| Public proof-of-concept exploits | Exploitation | Exploiting vulnerabilities in edge devices, usually with little modification [21] |
| FortigateSniffer | Credential Interception | Custom Golang tool abusing the FortiOS packet sniffer on compromised firewalls [22] |
| LAGTOY | Backdoor | Custom implant used by ToyMaker [19] |
| Edgecution | Backdoor | Malicious Edge extension plus Python backdoor using native messaging [23] |
| AiTM and device-code phishing | Identity Access | Capturing authenticated cloud sessions [24] |
| Credential testing tools | Validation | Automated testing of harvested credentials against VPN endpoints |
| Brute-force tools (Hydra, custom) | Access | RDP/SSH brute-forcing; SSH brute force was FortiBleed's entry method [22] |
| Forum escrow services | Transaction | Protected payment for access trades |
| Tox/Jabber/XMPP | Communication | Encrypted messaging for transaction details |
| Cobalt Strike/Sliver | Post-Exploitation | Used by some IABs for privilege escalation before sale [21] |
| BloodHound | AD Enumeration | Mapping Active Directory to assess access value |
| Cryptocurrency (BTC, XMR) | Payment | Primary payment methods for access purchases |

## Intelligence Gaps

- **Private deal volume**: A significant portion of IAB activity occurs through private channels and direct relationships rather than public forum listings. The cases reported in 2026 suggest this share is growing, but no public measurement exists.
- **Post-RAMP market share**: RAMP carried 208 of 530 access threads in Rapid7's 2025 data [17]. Where that volume moved after January 2026 is not yet quantified.
- **Status of seeded handles**: No source from 2025 or 2026 was found for Zebra2104, Sang_real, JETKITTEN, Roblette, montns or Bostaurus. Their current status is unconfirmed.
- **Albashiti sentencing**: Scheduled for 11 May 2026 [28]; the outcome was not confirmed in this refresh.
- **RAMP seizure details**: No DOJ statement had been issued when the seizure was reported [14]. Claims that the forum database leaked or was offered for sale are unverified and were denied by the administrator [13].
- **Control of XSS**: Former moderators allege the relaunched forum is under law-enforcement control; this has not been confirmed by any authority [10][11].
- **Price comparability**: Vendor averages differ by forum set, period and method. No public median for 2025-2026 listings was found.
- **Time-to-exploitation**: Public data points are single cases (about three weeks for ToyMaker to Cactus [19]; "weeks" in the CloudSEK case [21]). No representative measurement was found.
- **IAB-ransomware attribution**: Connecting specific incidents to specific sellers still depends on operator mistakes, leaks or law enforcement data.
- **Infostealer log to access conversion rate**: What percentage of corporate credentials in infostealer logs are viable for network access is poorly quantified.

## Sources & References

1. KELA - "IAB Landscape Reports" and access listing tracking — https://www.kelacyber.com/
2. Flashpoint - "Initial Access Broker Intelligence" — https://flashpoint.io/
3. Group-IB - "Hi-Tech Crime Trends: Initial Access Brokers" — https://www.group-ib.com/
4. CrowdStrike - "Access Broker Tracking and ECrime Index" — https://www.crowdstrike.com/
5. Mandiant - "FIN12 and Access Broker Relationships" — https://www.mandiant.com/resources
6. Secureworks - "Initial Access Broker Marketplace Analysis" — https://www.secureworks.com/
7. Digital Shadows (now ReliaQuest) - "IAB Marketplace Monitoring" — https://www.reliaquest.com/
8. CISA - Known Exploited Vulnerabilities Catalog (edge device CVEs) — https://www.cisa.gov/known-exploited-vulnerabilities-catalog
9. Help Net Security - "Mastermind behind Russian-speaking cybercrime hub arrested in Ukraine" (reporting the Europol announcement), 2025-07-23 — https://www.helpnetsecurity.com/2025/07/23/europol-cybercrime-operation-xss-is-admin-arrest/
10. Intel 471 - "After disruption, XSS cybercrime forum faces loss of trust", 2025-08-21 — https://www.intel471.com/blog/after-disruption-xss-cybercrime-forum-faces-loss-of-trust
11. KELA - "XSS Forum After Takedown: DamageLib Emerges", 2025-09-04 — https://www.kelacyber.com/blog/xss-forum-after-takedown-damagelib-emerges/
12. KELA - "BreachForums Successors in 2026: PWN vs Breached", 2026 — https://www.kelacyber.com/blog/breachforums-succession-wars-2026/
13. Rapid7 - "The Post-RAMP Era: Allegations, Fragmentation, and the Rebuilding of the Ransomware Underground", 2026-02-25 — https://www.rapid7.com/blog/post/tr-post-ramp-allegations-fragmentation-ransomware-underground-rebuild/
14. The Record - "Notorious Russia-based RAMP cybercrime forum apparently seized by FBI", 2026-01-29 — https://therecord.media/notorious-russia-based-ramp-forum-seized
15. Rapid7 - "Compromise for Sale: Inside the Rapid7 2025 Access Brokers Report", 2025-08-11 — https://www.rapid7.com/blog/post/compromise-for-sale-inside-the-rapid7-2025-access-brokers-report/
16. Rapid7 - "Rapid7 Access Brokers Report: New Research Reveals Depth of Compromise in Access Broker Deals, with 71% Offering Privileged Access", 2025-08-12 — https://investors.rapid7.com/news/news-details/2025/Rapid7-Access-Brokers-Report-New-Research-Reveals-Depth-of-Compromise-in-Access-Broker-Deals-with-71-Offering-Privileged-Access/default.aspx
17. Rapid7 - "Initial Access Brokers have Shifted to High-Value Targets and Premium Pricing", 2026-03-31 — https://www.rapid7.com/blog/post/tr-initial-access-broker-shift-high-value-targets-premium-pricing/
18. Cisco Talos - "Redefining IABs: Impacts of compartmentalization on threat tracking and modeling", 2025-05-13 — https://blog.talosintelligence.com/redefining-initial-access-brokers/
19. Cisco Talos - "Introducing ToyMaker, an initial access broker working in cahoots with double extortion gangs", 2025-04-23 — https://blog.talosintelligence.com/introducing-toymaker-an-initial-access-broker/
20. Intel 471 - "An in-depth look at Black Basta's TTPs", 2025-04-02 — https://www.intel471.com/blog/an-in-depth-look-at-black-bastas-ttps
21. CloudSEK - "Access For Sale: Inside a Russian-Speaking Access Broker's Dual Operation", 2026-08-03 — https://www.cloudsek.com/blog/access-for-sale-inside-a-russian-speaking-access-brokers-dual-operation
22. SecurityWeek - "FortiBleed Campaign Linked to INC, Lynx Ransomware Attacks" (reporting SOCRadar research), 2026-07-02 — https://www.securityweek.com/fortibleed-campaign-linked-to-inc-lynx-ransomware-attacks/
23. Zscaler ThreatLabz - "Payouts King Ransomware Initial Access Broker Deploys New Edgecution Malware", 2026-06-23 — https://www.zscaler.com/blogs/security-research/payouts-king-ransomware-initial-access-broker-deploys-new-edgecution
24. Microsoft Security Blog - "Passkey-themed social engineering leads to identity and cloud compromise", 2026-09-09 — https://www.microsoft.com/en-us/security/blog/2026/09/09/passkey-themed-social-engineering-leads-identity-cloud-compromise/
25. ReliaQuest - "Ransomware and Cyber Extortion in Q1 2026", 2026-04-27 — https://reliaquest.com/blog/threat-spotlight-ransomware-and-cyber-extortion-in-q1-2026/
26. US Department of Justice - "Russian Citizen Sentenced to Prison for Hacking into U.S. Companies and Enabling Major Cybercrime Groups to Extort Tens of Millions of Dollars", 2026-03-23 — https://www.justice.gov/opa/pr/russian-citizen-sentenced-prison-hacking-us-companies-and-enabling-major-cybercrime-groups
27. BleepingComputer - "Yanluowang ransomware access broker gets 81 months in prison", 2026-03-24 — https://www.bleepingcomputer.com/news/security/yanluowang-ransomware-access-broker-gets-81-months-in-prison/
28. The Record - "Jordanian initial access broker pleads guilty to helping target 50 companies", 2026-01-16 — https://therecord.media/guilty-plea-initial-access-broker-r1z
29. KELA - "Inside the r1z Initial Access Broker Case", 2026-01-21 — https://www.kelacyber.com/blog/the-high-price-of-poor-opsec-inside-the-r1z-initial-access-broker-case-/
30. Sophos - "Taking the shine off BreachForums", 2025-06 — https://www.sophos.com/en-us/blog/taking-the-shine-off-breachforums

## Change Log

| Date | Change | Source |
|------|--------|--------|
| 2026-04-05 | Initial creation with baseline intelligence through early 2025 | Training knowledge |
| 2026-09-29 | Rewrote summary and forum status (XSS arrest and split, BreachForums and RAMP seizures); added vendor-tracked brokers, Volkov and Albashiti prosecutions, Rapid7 pricing data; marked seeded handles and price ranges as unverified | OSINT refresh |
