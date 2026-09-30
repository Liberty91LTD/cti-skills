---
name: hacktivism
description: Use when the user asks about hacktivist activity (Killnet, NoName057(16), IT Army of Ukraine, Anonymous Sudan, RipperSec, CARR, etc.), DDoS-claiming groups, politically-motivated cyber operations, or wartime cyber-ops chatter. Self-updating knowledge cell.
user-invocable: true
metadata:
  category: knowledge-cell
  created: 2026-04-05
  last_updated: 2026-09-29
  update_count: 1
  confidence: moderate
---

# Hacktivism

## Executive Summary

Hacktivism in 2025-2026 is driven by two conflicts: Russia's war against Ukraine and the confrontation between Iran, Israel and the United States. Activity tracks military and political events closely. Radware recorded a peak in public DDoS claims in Q2 2025, a contraction afterwards, and a 103% month-over-month jump in March 2026 following the US and Israeli strikes on Iran that began on 28 February 2026 [19][20]. Europe receives roughly half of all claimed hacktivist DDoS attacks, and government is the most targeted sector [19][20].

The question of whether the main pro-Russian brands are grassroots or state-run has largely been answered by governments. In December 2025 the US Department of Justice and a joint advisory from CISA, FBI, NSA and international partners stated that Cyber Army of Russia Reborn (CARR) was created and funded by the GRU, and that NoName057(16) was created by CISM, an organization established on behalf of the Kremlin [11][12]. Denmark's Defence Intelligence Service assessed that Z-Pentest and NoName057(16) both have links to the Russian state and are used as instruments of hybrid war [13]. On the Iranian side, vendors describe Handala as linked to the Ministry of Intelligence and Security (MOIS) and Cyber Av3ngers as affiliated with the IRGC [17][23].

Law-enforcement pressure increased but has not stopped the activity. Europol's Operation Eastwood (July 2025) took more than 100 NoName057(16) servers offline and produced two arrests and seven arrest warrants; Imperva measured a few days of silence followed by a higher attack tempo [9][10]. NoName057(16) remained the most active DDoS-claiming group through the first half of 2026 [19]. The United States extradited and indicted one alleged CARR and NoName057(16) participant, Spain arrested an alleged supporter, and Dutch investigators seized 800 servers from hosting companies linked to the group's infrastructure [11][14][15].

Most hacktivist operations still have limited effect, and the groups routinely exaggerate. The joint advisory says pro-Russian groups have limited capabilities and regularly make false or exaggerated claims [12]. The exception is tampering with internet-exposed operational technology (OT). Confirmed cases now include burst water pipes in Denmark, a dam valve opened in Norway, and manipulated water pressure in Canada, all achieved through weak or default credentials rather than sophisticated tooling [13][21][22]. Anonymous Sudan remains disrupted following the October 2024 US indictment; no later activity was found in this refresh.

## Key Actors

| Group | Alignment | Primary TTPs | Status |
|-------|-----------|-------------|--------|
| NoName057(16) | Pro-Russia; created by Kremlin-linked CISM per US government [11][12] | Crowdsourced DDoS via DDoSia; joint OT claims with CARR and Z-Pentest | Active; most active DDoS claimant in 2025 and H1 2026 despite Operation Eastwood [19][20] |
| Cyber Army of Russia Reborn (CARR); also People's Cyber Army of Russia, Russian CyberTeam [12] | Pro-Russia; created and funded by GRU unit 74455 per US government [11][12] | DDoS; HMI tampering via exposed VNC at water, food and energy sites | Named in Dec 2025 advisory; two members sanctioned (Jul 2024), one alleged member indicted (Dec 2025); current tempo unconfirmed |
| Z-Pentest | Pro-Russia; formed Sep 2024 by CARR and NoName057(16) administrators [12] | OT intrusion, hack-and-leak, defacement; largely avoids DDoS | Active; claimed Israeli water systems in Mar 2026 [16] |
| Sector16 | Pro-Russia; formed Jan 2025 with Z-Pentest [12] | OT intrusion claims | Active as of Dec 2025 advisory; described as novice |
| TwoNet | Pro-Russia | DDoS, then OT claims | Announced it was ceasing operations on 30 Sep 2025 [24] |
| KillNet | Formerly pro-Russia; now assessed as mercenary | Hack-for-hire; unverified claims against Ukraine | Rebranded under new ownership; reappeared May 2025 [25] |
| Anonymous Sudan (Storm-1359) | Claimed pro-Sudan | Layer 7 DDoS; targeted Microsoft, Cloudflare, US hospitals | Disrupted (Oct 2024 indictment); case outcome not confirmed |
| IT Army of Ukraine | Pro-Ukraine | Crowdsourced DDoS against Russian telecoms, media, payment systems | Active as of Mar 2025 reporting [26] |
| Hacking Cat, Ukrainian Cyber Alliance, Cyber Anarchy Squad | Pro-Ukraine | Data leaks, defacement, and since mid-2025 encryption and wiping (per Kaspersky) | Active (Sep 2026) [27] |
| Handala | Pro-Iran; linked to MOIS per Unit 42 [17] | Hack-and-leak, destructive claims, intimidation | Active; claimed the Mar 2026 Stryker incident [17][18] |
| Cyber Av3ngers (Shahid Kaveh Group) | Pro-Iran; IRGC Cyber Electronic Command [23] | PLC and HMI exploitation | Active per vendors; see note on 2026 PLC campaign below |
| Keymous+, DieNet, Dark Storm Team, RipperSec, 313 Team, Cyber Islamic Resistance | Pro-Palestine / pro-Iran | DDoS, defacement, hack-and-leak claims | Active in Mar 2026 surge [16][17] |
| Predatory Sparrow (Gonjeshke Darande) | Anti-Iran; widely believed linked to Israeli military intelligence [28] | Destructive attacks on Iranian infrastructure | Active; claimed Bank Sepah attack Jun 2025 |
| SiegedSec | Hacktivist (anti-government) | Data leaks | Disbanded (claimed); not re-verified in this refresh |
| GhostSec | Unclear alignment | Varied; cooperated with ransomware groups | Not re-verified in this refresh |

## Current Activity

### NoName057(16) After Operation Eastwood (2025-2026)
NoName057(16) claimed 4,693 attacks in 2025 according to Radware, and generated 40.5% of all recorded hacktivist DDoS claims in the first half of 2026 [19][20]. Operation Eastwood in mid-July 2025 disrupted its infrastructure, but Imperva recorded a rise from about 10 to about 18 targeted sites per day once the group resumed on 23 July, with nearly half of the subsequent attacks aimed at German websites [10]. The group continued to time campaigns to political events. It carried out DDoS attacks on Danish political party websites ahead of the November 2025 municipal and regional elections, which Denmark attributed to it [13]. It claimed attacks on about 120 Italian targets, including foreign ministry sites and hotels in Cortina d'Ampezzo, before the February 2026 Winter Olympics; Italy's foreign minister said the attacks were thwarted and reporting indicated no significant disruption [29]. On 2 March 2026 the group declared solidarity with Iran and began claiming Israeli targets [16].

### Pro-Russian OT Tampering
The joint advisory AA25-343A (9 December 2025) describes CARR, NoName057(16), Z-Pentest and Sector16 scanning for internet-facing VNC services, brute-forcing weak or default passwords, and then changing settings on human-machine interfaces. Targets are mainly water and wastewater, food and agriculture, and energy. The most common effect is a temporary loss of view that forces manual operation; the advisory states that attacks have not yet caused injury [12]. Confirmed or officially attributed cases:

- **Denmark**: the Defence Intelligence Service attributed a destructive 2024 attack on a water utility to Z-Pentest [13]. Press reporting describes manipulated pressure and households left without water for several hours [30].
- **Norway**: on 7 April 2025 an attacker opened a valve at the Bremanger dam for about four hours through a web-accessible control panel protected by a weak password. No damage resulted. The head of the Police Security Service attributed it to pro-Russian cyber actors in August 2025 [21].
- **Canada**: alert AL25-016 (29 October 2025) reported tampering with water pressure at a water facility, a manipulated tank gauge at an oil and gas company, and altered temperature and humidity in a grain silo. It named no group [22]. Separately, the Communications Security Establishment reported that NoName057(16) claimed control of a Quebec municipal water treatment plant in October 2025; the claim is unconfirmed [31].
- **United States**: the Department of Justice alleges CARR attacks on drinking water systems in several states and on a Los Angeles meat processing facility in November 2024 that spoiled thousands of pounds of meat and triggered an ammonia leak [11].

Forescout showed how unreliable claims can be: TwoNet publicly claimed an attack on a water utility that was in fact a Forescout honeypot, entered with default credentials [24].

### Middle East: June 2025 and the 2026 Iran Conflict
During the June 2025 Israel-Iran exchange, Predatory Sparrow claimed to have destroyed data at Iran's Bank Sepah. IRGC-linked Iranian media reported disrupted account access, withdrawals and card payments [28].

After the US and Israeli strikes of 28 February 2026, Radware counted 149 hacktivist DDoS claims against 110 organizations in 16 countries in the first three days, with Keymous+, DieNet and NoName057(16) responsible for about three quarters of them and Kuwait, Israel and Jordan the most targeted [32]. Unit 42 counted about 60 active groups by 2 March and described an "Electronic Operations Room" set up on 28 February to coordinate Iran-aligned personas [17]. Pro-Russian groups joined in: Z-Pentest claimed control of Israeli water and pump systems, and Cardinal and Russian Legion claimed breaches of Iron Dome systems [16][17]. None of these claims was independently verified. Intel 471 assessed that the surge was real but that the groups frequently exaggerate impact [16].

The most consequential incident associated with a hacktivist persona in this period is Stryker. The company disclosed on 12 March 2026 that an incident identified on 11 March caused a global disruption to its Microsoft environment and disrupted order processing, manufacturing and shipping [18]. Handala claimed responsibility, including device wiping and data theft. Stryker did not attribute the incident, and the method and the data theft claim remain unverified [33].

### Pro-Ukrainian Operations
Russian vendor F6 reported in March 2025 that IT Army of Ukraine DDoS activity had risen sharply over the previous year, with a focus on regional telecom operators in Kursk and Belgorod [26]. Kaspersky reported in September 2026 that Hacking Cat had moved from leaks and defacement to encryption and data destruction, working alongside Ukrainian Cyber Alliance and Cyber Anarchy Squad. Hacking Cat disputed part of that attribution [27].

## Historical Events

| Date | Event | Impact |
|------|-------|--------|
| Feb 2022 | Ukraine invasion sparks hacktivist surge | Dozens of new groups formed on both sides; IT Army of Ukraine launched via Telegram |
| 2022 | KillNet DDoS campaigns against NATO | Targeted government sites in US, Europe; caused brief disruptions; high media profile |
| 2022-2023 | Anonymous Sudan emerges | Launched major DDoS attacks on Microsoft, Cloudflare, X; disrupted US hospital services |
| Jun 2023 | SiegedSec leaks NATO data | Claimed theft of unclassified NATO documents; later targeted US state governments |
| Oct 2023 | Israel-Hamas conflict triggers cyber operations | Wave of hacktivist activity from pro-Palestinian, pro-Israeli, and aligned groups |
| Nov 2023 | Cyber Av3ngers target US water Unitronics PLCs | IRGC-linked group exploited default passwords on internet-exposed PLCs |
| Jan 2024 | CyberArmyofRussia_Reborn claims US water attacks | Claimed manipulation of water system controls in Texas; partially confirmed |
| Mar 2024 | Anonymous Sudan DDoS impacts multiple sectors | Major DDoS campaigns disrupted government and healthcare services |
| Jul 2024 | OFAC sanctions two CARR members | Yuliya Pankratova and Denis Degtyarenko designated [11] |
| Sep 2024 | Z-Pentest formed | Created by CARR and NoName057(16) administrators, per AA25-343A [12] |
| Oct 2024 | Anonymous Sudan members indicted | US DOJ charged two Sudanese nationals; infrastructure seized |
| 2024 | Danish water utility attack | Attributed to Z-Pentest by Danish intelligence in Dec 2025 [13] |
| Mar 2025 | DDoS attack on X | Dark Storm Team claimed it; Bitsight confirmed an IoT-botnet DDoS but doubted the attribution [34] |
| Apr 2025 | Bremanger dam valve opened (Norway) | About four hours of water release, no damage; attributed to pro-Russian actors [21] |
| May 2025 | KillNet reappears | Unverified claim against Ukraine's drone-tracking system; brand now under new ownership [25] |
| Jun 2025 | Predatory Sparrow claims Bank Sepah attack | Customer services disrupted per Iranian media [28] |
| Jul 2025 | Operation Eastwood against NoName057(16) | More than 100 servers disrupted, 2 arrests, 7 warrants; group resumed within days [9][10] |
| Sep 2025 | TwoNet claims honeypot as a real utility, then shuts down | Forescout documented the fabricated claim [24] |
| Oct 2025 | Canada alert AL25-016 | Three ICS tampering incidents at water, oil and gas, and agricultural sites [22] |
| Nov 2025 | NoName057(16) DDoS on Danish party websites before elections | Sites temporarily offline; attributed by Danish intelligence [13][30] |
| Dec 2025 | DOJ indictments and joint advisory AA25-343A | Dubranova charged; CARR and NoName057(16) publicly tied to the Russian state [11][12] |
| Feb 2026 | NoName057(16) campaign before Winter Olympics | About 120 Italian targets claimed; no significant disruption reported [29] |
| Feb-Mar 2026 | Hacktivist surge after strikes on Iran | 149 DDoS claims in three days; about 60 groups active [17][32] |
| Mar 2026 | Stryker incident | Global disruption to operations; claimed by Handala, not attributed by the company [18][33] |
| Mar 2026 | Spain arrests alleged CARR and Z-Pentest supporter | Arrest in Palencia following FBI information; announced Jul 2026 [14] |
| May 2026 | Dutch FIOD seizes 800 servers | Two arrests at hosting companies tied to sanctioned Stark Industries; infrastructure linked to NoName057(16) attacks [15] |

## TTP Evolution

**DDoS Capabilities**: Hacktivist DDoS has evolved from basic volumetric attacks using off-the-shelf tools (LOIC, HOIC) to sophisticated Layer 7 application-layer attacks using commercial stresser services, botnets, and custom tools. Anonymous Sudan utilized cloud infrastructure and SaaS DDoS platforms to generate attacks exceeding 1 Tbps. NoName057(16)'s DDoSia represents a gamified crowdsourcing model. Some groups rent or operate botnets for sustained campaigns. The March 2025 attack on X was carried mostly by compromised IP cameras and video recorders, whoever directed it [34].

**From DDoS to Data**: More capable groups have moved beyond DDoS to data exfiltration and publication. SiegedSec specialized in data leaks targeting organizations based on political stance. Some pro-Russian groups have leaked data from Ukrainian organizations. Z-Pentest favors hack-and-leak and defacement over DDoS [12]. The transition from "disruption" to "exposure" hacktivism increases potential impact and intelligence value.

**ICS/OT Targeting**: OT tampering has moved from occasional claims to a recurring, government-documented pattern. The method remains simple: scan for exposed VNC or web panels, brute-force weak or default credentials, and change values through the operator interface. The joint advisory calls the approach unsophisticated, inexpensive and easy to replicate, and notes that the actors often misunderstand the processes they alter, which makes outcomes unpredictable [12]. Cyber Av3ngers specifically targeted Unitronics Vision PLC devices in 2023. A joint US advisory of April 2026 (updated July 2026) describes Iranian-affiliated actors manipulating Rockwell Automation, and later Schneider Electric and Siemens, PLCs with operational disruption and financial loss in some cases [23].

**State-Aligned Operations**: The most significant TTP evolution is the use of hacktivist branding as a facade for state-directed operations. This provides plausible deniability, enables more aggressive operations without direct attribution to intelligence services, and leverages volunteer participants as unwitting proxies. US authorities allege that a moniker associated with at least one GRU officer instructed CARR leadership on target selection, and that CISM staff built DDoSia, paid for infrastructure and picked targets for NoName057(16) [11][12].

**Ransomware Crossover**: Some hacktivist groups have adopted ransomware or wiper tactics. GhostSec partnered with Stormous ransomware. Groups have deployed wipers against Ukrainian targets under hacktivist banners. Kaspersky reports pro-Ukrainian groups using ransomware and wipers against Russian organizations, and notes shared custom tooling across several groups [27]. This convergence of hacktivist motivation with criminal tooling blurs traditional categorization.

**Mercenary Drift**: KillNet's brand was sold after its founder was exposed, and analysts now describe it as a hack-for-hire operation driven by money rather than ideology [25].

## Ecosystem & Infrastructure Patterns

**Telegram as Command-and-Control**: Telegram is the primary coordination platform for modern hacktivism. Groups use channels for target announcements, attack coordination, proof-of-impact screenshots, and recruiting. During Operation Eastwood, authorities used the same channel in reverse, messaging 1,100 participants and 17 administrators to warn them of criminal liability [9].

**Geopolitical Alignment Clustering**: The hacktivist landscape clusters along geopolitical lines: Pro-Russia (NoName057(16), CARR, Z-Pentest, Sector16) + Pro-Iran (Handala, Cyber Av3ngers, Homeland Justice) + some pro-Palestine groups form one axis. Pro-Ukraine (IT Army of Ukraine, Ukrainian Cyber Alliance, various) + anti-Iran groups form another. The March 2026 surge showed the first axis acting together, with pro-Russian groups claiming Israeli targets within days of the strikes on Iran [16][17].

**Brand Churn**: Groups splinter, rebrand and revive old names. Z-Pentest grew out of CARR and NoName057(16); Sector16 grew out of Z-Pentest; TwoNet appeared, closed, returned and closed again within a year [12][24]. Track people and infrastructure rather than names.

**Crowdsourcing Models**: NoName057(16)'s DDoSia and Ukraine's IT Army both use crowdsourcing — distributing target lists and tools to volunteers via Telegram, enabling large-scale operations without centralized infrastructure. DDoSia incentivizes participation with cryptocurrency payments, creating a paid volunteer model.

**Hosting Dependencies**: Pro-Russian operations depend on commercial hosting. The EU sanctioned Stark Industries in May 2025, and in May 2026 Dutch investigators seized 800 servers from companies alleged to have continued its business [15].

**Attribution Challenges**: Distinguishing genuine grassroots hacktivism from state-directed operations is extremely difficult. Indicators of state alignment include: operational sophistication exceeding stated capability, targeting aligned precisely with state foreign policy objectives, infrastructure overlapping with known state actors, and operational security inconsistent with volunteer groups.

## Tooling

| Tool | Category | Usage |
|------|----------|-------|
| DDoSia | Crowdsourced DDoS | NoName057(16)'s custom volunteer DDoS tool with crypto incentives |
| IT Army tools | Crowdsourced DDoS | Various tools distributed by Ukraine's IT Army for volunteer attacks |
| MHDDoS | DDoS Tool | Multi-vector DDoS tool popular in hacktivist communities |
| MegaMedusa | DDoS Tool | Used by TwoNet before its move to OT claims [24] |
| Stresser/Booter services | DDoS-for-hire | Commercial DDoS services used by less technical groups |
| IoT botnets | DDoS infrastructure | Compromised cameras and recorders; seen in the Mar 2025 X attack [34] |
| Nmap, OpenVAS | Reconnaissance | Used to find exposed VNC services on OT devices [12] |
| Password brute-force tools | Initial access | Used against HMIs with default or weak credentials [12] |
| Telegram | C2/Coordination | Primary platform for coordination, targeting, and proof-of-attack |
| Web vulnerability scanners | Reconnaissance | Automated scanning for defacement and data exfiltration targets |
| SQLMap | Data Theft | SQL injection tool for database exfiltration |
| Gorilla RAT, Monkey ransomware, Nemo wiper | Intrusion / Destruction | Attributed by Kaspersky to Hacking Cat; partly disputed by the group [27] |
| Wiper malware (various) | Destruction | Used by state-aligned groups under hacktivist cover |
| Leaked credentials | Account Takeover | Used for accessing and defacing websites or leaking data |

## Intelligence Gaps

- **State direction vs. alignment**: Governments have now stated the origin of CARR and NoName057(16), but the degree of day-to-day tasking is unclear, as is the position of smaller brands. The advisory says only that Sector16 members may have received indirect support from the Russian government [12].
- **CARR and Z-Pentest relationship**: Sources disagree. The Department of Justice describes CARR as "also known as Z-Pentest"; the joint advisory describes Z-Pentest as a separate group formed by CARR and NoName057(16) administrators in September 2024 [11][12].
- **Dubranova case outcome**: Trials were scheduled for 3 February 2026 (NoName057(16)) and 7 April 2026 (CARR). No verdict, plea or sentence was found in this refresh [11].
- **Anonymous Sudan case outcome**: No trial, plea or sentencing information was found, and no renewed activity under the name.
- **Stryker attribution**: Handala's claim, the intrusion method and the alleged data theft are unverified by the company [18][33].
- **2026 PLC campaign actor**: The joint advisory attributes the activity to Iranian-affiliated APT actors and mentions Cyber Av3ngers only as the source of similar earlier activity. Unit 42 tracks the Rockwell targeting as a cluster it associates with Cyber Av3ngers [17][23].
- **SiegedSec, GhostSec, RipperSec**: Status was not independently re-verified. RipperSec appears in vendor reporting on the March 2026 surge as part of a wider collective [17].
- **IT Army of Ukraine tempo in 2026**: The latest sourced assessment dates from March 2025 and comes from a Russian vendor [26].
- **Actual DDoS impact**: Most hacktivist groups self-report their impact through screenshots of error pages or downtime monitors. Vendor counts of "claimed attacks" measure claims, not outages.
- **ICS/OT claims verification**: Many hacktivist ICS claims are exaggerated or fabricated, as the TwoNet honeypot case shows. Verifying which claims represent genuine compromises remains essential but difficult.
- **Financial flows**: US authorities allege GRU funding of CARR tools through at least September 2024 and that dissatisfaction with that funding led to Z-Pentest [12]. Funding of other groups is not well understood.

## Sources & References

1. US DOJ - "Two Sudanese Nationals Indicted for Anonymous Sudan DDoS Attacks" (October 2024) — https://www.justice.gov/
2. CISA - "IRGC-Affiliated Cyber Actors Exploit PLCs" Advisory (December 2023) — https://www.cisa.gov/
3. Mandiant - "Hacktivism and State-Aligned Operations Analysis" — https://www.mandiant.com/resources
4. CrowdStrike - "Hacktivist Landscape Reports" — https://www.crowdstrike.com/
5. Radware - "Hacktivism Unveiled" reports — https://www.radware.com/
6. Flashpoint - "Pro-Russian and Pro-Ukrainian Hacktivist Tracking" — https://flashpoint.io/
7. Microsoft - "Storm-1359 (Anonymous Sudan) Analysis" — https://www.microsoft.com/en-us/security/blog/
8. Orange Cyberdefense - "Cy-Xplorer Reports on Hacktivism" — https://www.orangecyberdefense.com/
9. BleepingComputer - "Europol disrupts pro-Russian NoName057(16) DDoS hacktivist group" (16 July 2025), reporting the Europol announcement — https://www.bleepingcomputer.com/news/security/europol-disrupts-pro-russian-noname05716-ddos-hacktivist-group/
10. Imperva - "Operation Eastwood: Measuring the Real Impact on NoName057(16)" (September 2025) — https://www.imperva.com/blog/operation-eastwood-measuring-the-real-impact-on-noname05716/
11. US DOJ - "Justice Department Announces Actions to Combat Two Russian State-Sponsored Cyber Criminal Hacking Groups" (9 December 2025) — https://www.justice.gov/opa/pr/justice-department-announces-actions-combat-two-russian-state-sponsored-cyber-criminal
12. CISA, FBI, NSA and partners - "Pro-Russia Hacktivists Conduct Opportunistic Attacks Against US and Global Critical Infrastructure", AA25-343A (9 December 2025, revised 18 December 2025) — https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-343a
13. Danish Defence Intelligence Service - "Russia is responsible for destructive and disruptive cyber-attacks against Denmark" (18 December 2025) — https://www.fe-ddis.dk/globalassets/fe/dokumenter/2025/-russia-responsible-for-cyber-attacks-.pdf
14. The Record - "Spain arrests alleged supporter of pro-Russian hacktivist groups after FBI tip" (8 July 2026) — https://therecord.media/spain-arrest-alleged-supporter-noname-carr-zpentest
15. BleepingComputer - "Netherlands seizes 800 servers of hosting firm enabling cyberattacks" (22 May 2026) — https://www.bleepingcomputer.com/news/security/netherlands-seizes-800-servers-of-hosting-firm-enabling-cyberattacks/
16. Intel 471 - "Israeli, US strikes against Iran triggers a surge in hacktivist activity" (9 March 2026) — https://www.intel471.com/blog/israeli-us-strikes-against-iran-triggers-a-surge-in-hacktivist-activity
17. Palo Alto Networks Unit 42 - "Threat Brief: Escalation of Cyber Risk Related to Iran" (updated 17 April 2026) — https://unit42.paloaltonetworks.com/iranian-cyberattacks-2026/
18. Stryker Corporation - Form 8-K (filed 12 March 2026) — https://www.sec.gov/Archives/edgar/data/310764/000119312526104431/d101097d8k.htm
19. Radware - "H1 2026 Global Threat Report" press release (9 September 2026) — https://www.globenewswire.com/news-release/2026/09/09/3358409/8980/en/radware-h1-2026-global-threat-report-shows-web-ddos-attacks-jump-more-than-110-as-cyber-threats-accelerate.html
20. Radware - "2026 Global Threat Report" press release (19 February 2026) — https://www.globenewswire.com/news-release/2026/02/19/3240861/8980/en/radware-2026-global-threat-report-shows-ddos-attacks-jump-168-as-cyber-threats-escalate-across-networks-and-applications.html
21. NATO CCDCOE Cyber Law Toolkit - "Cyber incident against the Bremanger dam in Norway (2025)" — https://cyberlaw.ccdcoe.org/wiki/Cyber_incident_against_the_Bremanger_dam_in_Norway_(2025)
22. Canadian Centre for Cyber Security - "AL25-016 Internet-accessible industrial control systems (ICS) abused by hacktivists" (29 October 2025) — https://www.cyber.gc.ca/en/alerts-advisories/al25-016-internet-accessible-industrial-control-systems-ics-abused-hacktivists
23. CISA, FBI, NSA and partners - "Iranian-Affiliated Cyber Actors Exploit Programmable Logic Controllers Across US Critical Infrastructure", AA26-097A (7 April 2026, updated 22 July 2026) — https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-097a
24. Forescout - "Anatomy of a Hacktivist Attack: Russia-Aligned Group Targets OT/ICS" (9 October 2025) — https://www.forescout.com/blog/anatomy-of-a-hacktivist-attack-russian-aligned-group-targets-otics/
25. The Record - "Russian hacker group Killnet returns with new identity" (22 May 2025) — https://therecord.media/russian-hacker-group-killnet-returns-with-new-identity
26. The Record - "Ukraine's IT Army keeps up attacks on Russia despite waning media hype" (19 March 2025) — https://therecord.media/it-army-keeps-up-attacks-on-russia-ukraine
27. The Record - report on Kaspersky research into Hacking Cat (14 September 2026) — https://therecord.media/ukraine-malware-russia-ransomware
28. The Record - "Pro-Israel hackers claim breach of Iranian bank amid military escalation" (17 June 2025) — https://therecord.media/pro-israel-hackers-claim-attack-on-iranian-bank
29. The Record - "Italy blames Russia-linked hackers for cyberattacks ahead of Winter Olympics" (5 February 2026) — https://therecord.media/italy-blames-russia-linked-hackers-winter-games-cyberattack
30. The Record - "Denmark summons Russian ambassador over alleged cyberattacks on water utility, elections" (19 December 2025) — https://therecord.media/denmark-summons-russian-ambassador-cyberattack-elections
31. GovInfoSecurity - "Russian Water System Hack Attempted to Turn Canada Dry" (30 June 2026), reporting the CSE annual report 2025-2026 — https://www.govinfosecurity.com/russian-water-system-hack-attempted-to-turn-canada-dry-a-32122
32. The Hacker News - "149 Hacktivist DDoS Attacks Hit 110 Organizations in 16 Countries After Middle East Conflict" (March 2026), reporting Radware data — https://thehackernews.com/2026/03/149-hacktivist-ddos-attacks-hit-110.html
33. Arctic Wolf - "Stryker Systems Disrupted in Cyber Attack; Handala Group Claims Responsibility" (13 March 2026) — https://arcticwolf.com/resources/blog/stryker-systems-disrupted-cyber-attack-handala-group-claims-responsibility/
34. Bitsight - "Massive DDoS on X: Dark Storm or Cyber Fog?" (14 March 2025) — https://www.bitsight.com/blog/massive-ddos-x-dark-storm-or-cyber-fog

## Change Log

| Date | Change | Source |
|------|--------|--------|
| 2026-04-05 | Initial creation with baseline intelligence through early 2025 | Training knowledge |
| 2026-09-29 | Refresh covering Jan 2025 to Sep 2026: Operation Eastwood, DOJ indictments and AA25-343A, state attribution of CARR, NoName057(16) and Z-Pentest, confirmed OT tampering cases, 2026 Iran conflict surge, Stryker incident, KillNet and TwoNet status; People's Cyber Army merged into CARR as an alias; 26 sources added | OSINT refresh |
