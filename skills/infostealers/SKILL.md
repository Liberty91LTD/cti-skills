---
name: infostealers
description: Use when the user asks about infostealer families (LummaC2, RedLine, Vidar, Stealc, Raccoon, Rhadamanthys, etc.), log marketplaces (Russian Market, Genesis successors, BidenCash, Hudson Rock corpus), or stealer-driven incidents and credential exposure. Self-updating knowledge cell.
user-invocable: true
metadata:
  category: knowledge-cell
  created: 2026-04-05
  last_updated: 2026-09-29
  update_count: 1
  confidence: moderate
---

# Infostealers

## Executive Summary

Infostealer malware remains a foundational enabler for ransomware, account takeover, corporate network intrusion, and financial fraud. The families operate under a Malware-as-a-Service (MaaS) model: developers sell subscriptions that include a builder, a management panel, and regular updates to evade detection. Upon execution, infostealers harvest browser-stored credentials, session cookies, cryptocurrency wallet data, autofill data, and system information, packaging the results into "logs" that are sold on marketplaces, traded on Telegram, or used directly by the operator.

Between May 2025 and June 2026 the three families that led the market after RedLine's 2024 disruption were each hit by coordinated action: Lumma (May 2025, Microsoft, US DOJ, Europol and JC3), Rhadamanthys (November 2025, Operation Endgame), and StealC together with the Amadey loader (June 2026, Operation Endgame) [9][10][17][21][22]. None of these actions announced an arrest of a stealer developer. The results differ by family. Lumma rebuilt after the May 2025 seizures, then lost customers after rivals doxxed its alleged core members between late August and October 2025; it remains in circulation at reduced standing [13][14][28]. Rhadamanthys' developer attempted a revival about three weeks after the takedown, without new releases [19]. The post-takedown state of StealC is not yet established in the sources reviewed.

The market is now fragmented. Vidar, relaunched as version 2.0 in October 2025, absorbed much of the displaced demand [13][15][19]. Acreed rose on Russian Market during 2025 [11][12]. Newer names, including Remus, RevStealer and a set of macOS stealers (MacSync, Shub Stealer, DigitStealer), appear in 2026 vendor reporting [25][26][27][29]. Russian Market continues to operate, but Flare reports that more than 90% of the stealer logs it sees are now found on Telegram [28]. BidenCash was seized by US authorities in June 2025 [31].

Delivery has shifted towards ClickFix: fake verification or troubleshooting pages that persuade the user to paste and run a command. Microsoft describes campaigns hitting thousands of devices daily and, in 2026, macOS variants that fingerprint visitors before showing the lure [23][24][25]. The infostealer-to-ransomware link through Initial Access Brokers (IABs) is unchanged, while the value of a log has widened: Flare found enterprise SSO or identity-provider credentials in 2.05 million of 18.7 million logs analysed for 2025, and in 2026 stolen sessions for AI services became a reported monetisation path [28][32][33].

## Key Actors

| Stealer Family | Status | Notable Characteristics | Pricing |
|---------------|--------|------------------------|---------|
| RedLine | Disrupted (Oct 2024) | Was most prolific stealer 2020-2024; Operation Magnus seized infrastructure; still named among families in 2026 session-theft reporting [32] | $150/month (was) |
| Raccoon Stealer v2 | Disrupted; operator sentenced | Mark Sokolovsky arrested in the Netherlands (Mar 2022), extradited Feb 2024, sentenced to 60 months in Dec 2024 [30] | $200/month (was) |
| Vidar | Active | Derived from Arkei; version 2.0 released 6 Oct 2025 by "Loadbaks": rewritten in C, multithreaded, polymorphic builder, App-Bound Encryption bypass by memory injection [15]; gained users from Lumma and Rhadamanthys [13][19] | $300 per Trend Micro [15] |
| Lumma Stealer (LummaC2) | Disrupted (May 2025); active at reduced standing | About 2,300 domains seized; rebuilt; declined after doxxing (Aug-Oct 2025); uptick from the week of 20 Oct 2025 with browser fingerprinting added [9][13][14]; second by detections in AhnLab's August 2026 data [29] | $250-$1,000/tier; source $20,000 [9] |
| StealC | Disrupted (Jun 2026); current status unconfirmed | Emerged 2023; V2 released Mar 2025 with JSON-based C2 protocol, RC4, MSI and PowerShell payload support, embedded builder [16]; deployed with Amadey [16][21] | $200/month (pre-2025 figure) |
| Rhadamanthys | Disrupted (Nov 2025); revival attempted | Developer "kingcrete2022"; AI-based OCR for seed phrases; 0.9.x series in 2025; used by TA571, TA866, TA2541, TA547, TA585 [17]; no release since May 2025 [19] | $300-$500/month [17] |
| Acreed | Active | First identified in 2025; second to Lumma on Russian Market in Q1 2025 and prominent after Lumma's disruption [11][12][20] | Not confirmed |
| Remus | Active | Most frequently detected stealer in AhnLab's August 2026 statistics [29] | Not confirmed |
| RevStealer | Active (emerging) | Tracked by Elastic as REF2859; spread through game-cheat lures on hijacked YouTube channels; Polygon smart-contract fallback C2; no evidence of a MaaS offering in the analysis [27] | Not confirmed |
| Atomic Stealer (AMOS) | Active | macOS-focused; delivered through ClickFix and fake utility pages in 2025-2026 [23][25][26] | $1000/month (pre-2025 figure) |
| MacSync, Shub Stealer, DigitStealer | Active | macOS stealers named in Microsoft reporting, 2026 [24][25][26] | Not confirmed |
| Meta Stealer | Not verified in this refresh | Disrupted with RedLine in Operation Magnus (Oct 2024) | $125-$300/month (pre-2025 figure) |
| Mystic Stealer | Not verified in this refresh | Emerged mid-2023; polymorphic; targets 40+ browsers and extensions | $150/month (pre-2025 figure) |
| RisePro | Not verified in this refresh | Distributed via pay-per-install services | $150/month (pre-2025 figure) |

## Current Activity

### Fragmented Market After Three Disruptions (2025-2026)
No single family holds the position Lumma held in late 2024, when ReliaQuest attributed nearly 92% of its Russian Market credential-log alerts to it [11]. Trend Micro and SpyCloud both observed Vidar gaining activity as Lumma and Rhadamanthys customers moved [13][19]. AhnLab's August 2026 statistics rank Remus first by detections, followed by LummaC2, Vidar and ACRStealer [29]. Flare reports total infections fell about 20% year over year in 2025 while the share of logs exposing enterprise identity credentials rose [28].

### Operation Endgame: StealC and Amadey (June 2026)
On 24 June 2026 Microsoft's Digital Crimes Unit, Europol and partners announced action against StealC and the Amadey loader, which Microsoft describes as a delivery-to-theft chain. Microsoft reports over 200 command-and-control domains and IPs identified and shut down [21]. Published figures differ: Dutch police cite more than 100 servers and domains and more than 24 million credentials from 384,000 systems [22]; press coverage of the Europol announcement cites 27 million credentials, more than 140,000 infected computers in the first half of May 2026, and EUR 41 million in cryptocurrency frozen [34]. No arrests were reported in these sources.

### Lumma After Disruption and Doxxing
Lumma's operators restored infrastructure after May 2025. A campaign on a site called "Lumma Rats" then published personal details of five alleged core members, and the operation's Telegram accounts were compromised on 17 September 2025. Trend Micro recorded a steady decline from early September and a parallel drop in Amadey activity [13]. Flare attributes Lumma's decline to the doxxing rather than the law enforcement action [28]. Trend Micro reported renewed activity from the week of 20 October 2025 [14].

### ClickFix and macOS Stealers
Microsoft names Lumma as the most prolific ClickFix final payload and documents a June 2025 campaign delivering AMOS to macOS users [23]. Between February and April 2026, lures posing as macOS utility guides were hosted on Squarespace, Craft and Medium pages and delivered MacSync, Shub Stealer and AMOS through Terminal commands [26]. By August 2026 a cluster of more than 250 domains was using server-side browser fingerprinting to show the lure only to genuine macOS browsers [25].

### AI Service Sessions as a Target
BleepingComputer reported on 30 August 2026 that Anthropic notified users whose Claude sessions had been taken from stealer-infected machines and used to consume paid usage; families named were Vidar, LummaC2, StealC, RedLine and Acreed, with a small number of AMOS cases [32]. A vendor-sponsored SOCRadar report in September 2026 claims stealer-log exposure of AI service logins across more than 80,000 corporate domains [33].

## Historical Events

| Date | Event | Impact |
|------|-------|--------|
| 2020 | RedLine Stealer emerges | Rapidly became dominant infostealer; sold via Telegram and forums |
| Mar 2022 | Raccoon Stealer v1 disruption | Developer arrested; operations temporarily ceased before v2 launch |
| Oct 2022 | Raccoon Stealer v2 launched | Rebuilt from scratch after developer arrest; resumed operations |
| 2023 | Lumma Stealer rapid growth | Gained significant market share with advanced features and aggressive marketing |
| Apr 2023 | Genesis Market seized (Operation Cookie Monster) | Major log/bot marketplace taken down; 119 arrests; Russian Market absorbed demand |
| Mid-2023 | Rhadamanthys adds OCR capabilities | AI-powered recognition of cryptocurrency seed phrases from images |
| Early 2024 | Fake CAPTCHA distribution campaigns | Novel technique: fake "verify you are human" pages trick users into running PowerShell commands to install stealers |
| Oct 2024 | Operation Magnus (RedLine/META) | International operation led by Dutch police disrupted RedLine and META infrastructure; operators migrated to Lumma, StealC and others |
| Late 2024 | Chrome cookie encryption (App-Bound Encryption) | Google Chrome implemented enhanced cookie protection; stealer developers rapidly developed bypasses |
| Q4 2024 | Lumma dominance on Russian Market | Nearly 92% of ReliaQuest's Russian Market credential-log alerts [11] |
| Dec 2024 | Raccoon operator sentenced | Mark Sokolovsky sentenced to 60 months; restitution over $910,000 [30] |
| Jan-Apr 2025 | INTERPOL Operation Secure | 26 countries; over 20,000 malicious IPs and domains taken down, 41 servers seized, 32 arrests, 216,000+ victims notified [18] |
| Mar 2025 | StealC V2 released | New C2 protocol and payload formats [16] |
| May 2025 | Lumma disruption | Microsoft seized or blocked about 2,300 domains; DOJ seized five control-panel domains (19-21 May); 394,000+ infected Windows machines identified 16 Mar-16 May 2025; FBI counted at least 1.7 million theft instances [9][10] |
| Jun 2025 | BidenCash seized | About 145 domains and cryptocurrency seized; market had 117,000+ customers and over $17 million revenue since Mar 2022 [31] |
| Aug-Oct 2025 | Lumma doxxing campaign | Five alleged core members exposed; customers moved to Vidar and StealC [13] |
| Oct 2025 | Vidar 2.0 released | Full rewrite announced on underground forums [15] |
| Nov 2025 | Operation Endgame: Rhadamanthys, VenomRAT, Elysium | 1,025 servers taken down, 20 domains seized, 11 searches; Shadowserver's enhanced dataset lists 567,215 unique IPs and 91.9 million stealing events (14 Mar-11 Nov 2025) [17][19][35] |
| Jun 2026 | Operation Endgame: StealC and Amadey | Infrastructure seized; 24-27 million credentials recovered depending on source [21][22][34] |

## TTP Evolution

**Distribution Methods**: The evolution from email spam attachments (2020-2021) to SEO poisoning, Google Ads malvertising, and fake software download sites (2023-present) represents a major shift. The "fake CAPTCHA" technique of 2024 matured into ClickFix, now delivered through phishing emails, malvertising and compromised websites, and sold as kits [23]. On macOS the equivalent is a pasted Terminal command, which Microsoft notes does not undergo the same evaluation as an application bundle [26]. Other 2025-2026 vectors in vendor reporting include hijacked YouTube channels with AI-generated videos promoting game cheats [27], WhatsApp-based propagation (Eternidade Stealer) and fake PDF tools [24], and abuse of the Renpy game engine inside ZIP archives [29].

**Anti-Analysis**: Modern stealers employ VM/sandbox detection, anti-debugging, string encryption, and control flow obfuscation. Lumma and Rhadamanthys use techniques including trigonometric calculations for execution delays, heavy API call obfuscation, and dynamic C2 resolution via DNS-over-HTTPS or blockchain-based dead drops. Recent additions: Lumma's browser fingerprinting of victims through a dedicated C2 endpoint [14], Vidar 2.0's per-build polymorphism [15], RevStealer's sandbox scoring and Polygon smart-contract fallback [27], and server-side cloaking of lure pages [25]. StealC V2 removed its anti-VM checks [16].

**Data Targeting**: Beyond traditional browser credentials and cookies, modern stealers target: cryptocurrency wallet extensions and desktop wallets, 2FA authenticator app databases, VPN client credentials (corporate targets), email client data, Discord/Telegram session tokens, gaming platform credentials (Steam, Epic), and increasingly files matching patterns (documents, PDFs, private keys). macOS stealers take Keychain entries, iCloud data, SSH keys and notes [25][26]. Sessions and API keys for AI services are now extracted from logs and resold or used directly [32][33].

**Cookie/Session Theft**: Session cookie theft has become as valuable as credential theft, enabling authentication bypass that circumvents MFA entirely. Chrome's App-Bound Encryption (introduced 2024) was bypassed within weeks. Bypasses are now standard features: Vidar 2.0 extracts keys from live browser processes by memory injection [15], and RevStealer uses a debugger-based method [27]. Flare counted more than 1.17 million logs in 2025 that held both credentials and active session cookies [28].

**Log Processing and Sale**: Stolen data is processed through automated panels that parse, categorize, and extract high-value items. Logs are tagged by country, affected services (banking, social media, corporate), and data completeness. Automated filtering for corporate VPN credentials (Cisco AnyConnect, Fortinet, Pulse Secure) feeds the IAB pipeline.

## Ecosystem & Infrastructure Patterns

**MaaS Business Model**: Infostealer developers operate subscription-based services with tiered pricing. Higher tiers may include features like log parsing tools, dedicated support, custom builds, and access to private Telegram channels with updates. Lumma's developer, known as "Shamel" and based in Russia, reported about 400 active clients in November 2023 [9]. Supporting services are sold the same way: Microsoft found ClickFix builders offered at $200 to $1,500 per month [23].

**Log Market Pipeline**: Stolen logs flow through a multi-stage pipeline: stealer deployment, log collection at the C2 panel, automated parsing and categorization, listing on marketplaces or Telegram channels or private sale, purchase by IABs, fraudsters, or direct operators, then exploitation for account takeover, fraud, or network intrusion.

**Russian Market**: Still operating as of the 2025-2026 sources reviewed [20][28]. Rapid7 counted over 180,000 logs offered in the first half of 2025, about 30,000 per month, with three sellers accounting for 81% of listings and a typical price near $10 [20]. ReliaQuest noted recycled and fake credentials in listings and the absence of a seller review system [11]. Telegram has overtaken centralised markets as the main venue for logs by volume [28].

**Disruption Effects**: Infrastructure seizures without arrests have produced temporary effects. Lumma returned within weeks of May 2025; the larger loss of customers followed exposure by rivals [13][28]. Law enforcement access to panels also damages trust: a Rhadamanthys customer reported that the panel had been accessed before servers were destroyed [19]. Proofpoint measured email campaigns from Endgame-targeted families falling from 17% of campaigns in March 2023 to 1% in September 2025 [17].

**Infostealer-to-Ransomware Pipeline**: The operational chain from infostealer infection to ransomware deployment is well-documented: (1) Employee machine infected with infostealer via malvertising, (2) Corporate VPN/SSO credentials stolen, (3) Credentials appear on log markets, (4) IAB purchases and validates access, (5) IAB sells access on forums (Exploit, XSS, RAMP), (6) Ransomware affiliate purchases access and deploys ransomware. This chain can span weeks to months. Microsoft names Octo Tempest among Lumma's users [9].

## Tooling

| Tool/Platform | Category | Usage |
|--------------|----------|-------|
| Russian Market | Log Marketplace | Largest centralised marketplace for individual infostealer logs; operating [20][28] |
| 2easy | Log Marketplace | Secondary marketplace for bot/log trading; status not verified in this refresh |
| BidenCash | Carding/Credential Marketplace | Seized June 2025 [31] |
| Telegram channels | Distribution/Sales | Main venue for logs by volume; stealer subscriptions and customer support [28] |
| Google Ads | Distribution Vector | Malvertising campaigns directing to fake download sites |
| Pay-per-install (PPI) services | Distribution | PrivateLoader, SmokeLoader, Amadey distribute stealers; Amadey disrupted June 2026 [21] |
| Raccoon/Lumma/Vidar panels | C2 Management | Web-based panels for managing infections and extracting logs |
| CloudFlare Workers | Infrastructure | Used as C2 proxying layer to obscure real infrastructure |
| Discord webhooks | Exfiltration | Used by some stealers to exfiltrate data via Discord |
| Crypters/packers | Evasion | Commercial crypter services used to evade AV detection; Themida seen on StealC V2 [16] |
| ClickFix / fake CAPTCHA kits | Distribution | Pages that trick users into running malicious commands; sold as builders [23] |
| Blockchain dead drops | Infrastructure | Backup C2 addresses stored in smart contracts (RevStealer on Polygon) [27] |

## Intelligence Gaps

- **StealC and Amadey after June 2026**: No source reviewed establishes whether either service has resumed. Published figures for the operation differ between agencies and press [21][22][34].
- **Status of Meta Stealer, Mystic Stealer, RisePro and 2easy**: Listed as active in the April 2026 seed text; not confirmed either way in this refresh.
- **Acreed and ACRStealer**: Whether ReliaQuest's "Acreed" and AhnLab's "ACRStealer" are the same family was not confirmed. Acreed's developer, pricing and sales model are not public in the sources reviewed.
- **Remus**: AhnLab ranks it first for August 2026 but the summary reviewed gives no lineage or operator detail [29].
- **Developer accountability**: No arrests of Lumma, Rhadamanthys or StealC developers were found. The doxxed Lumma identities are allegations by rivals and are unverified.
- **Corporate impact quantification**: The number of breaches and ransomware incidents directly attributable to stealer-harvested credentials is not well-quantified.
- **Log market volumes**: With most logs moving through Telegram and private channels, marketplace counts understate total volume [28].
- **Browser session protection**: The effect of newer browser session-binding measures on stealer yield was not researched in this refresh.
- **AI service exposure**: The scale of the Claude session thefts was not quantified [32]; the SOCRadar figures come from sponsored content and are not independently corroborated [33].
- **Mobile infostealer convergence**: The overlap between desktop infostealers and mobile banking trojans is not well-mapped.

## Sources & References

1. Dutch National Police - "Operation Magnus: RedLine and META Stealer Disruption" (October 2024) — https://www.politie.nl/
2. FBI/Europol - "Operation Cookie Monster: Genesis Market Takedown" (April 2023) — https://www.fbi.gov/
3. Sekoia - "Infostealer Landscape" threat reports — https://blog.sekoia.io/
4. Recorded Future - "Infostealer Marketplace Intelligence" — https://www.recordedfuture.com/
5. KELA - "Infostealer-to-Ransomware Connection Analysis" — https://www.kelacyber.com/
6. Flare - "Infostealer Log Market Analysis" — https://flare.io/
7. Google Threat Analysis Group - "Malvertising Campaign Disruptions" — https://blog.google/threat-analysis-group/
8. Trend Micro - "Infostealer Family Tracking Reports" — https://www.trendmicro.com/vinfo/us/security/research-and-analysis/
9. Microsoft - "Disrupting Lumma Stealer: Microsoft leads global action against favored cybercrime tool" (21 May 2025) — https://blogs.microsoft.com/on-the-issues/2025/05/21/microsoft-leads-global-action-against-favored-cybercrime-tool/
10. US Department of Justice - "Justice Department Seizes Domains Behind Major Information-Stealing Malware Operation" (21 May 2025) — https://www.justice.gov/opa/pr/justice-department-seizes-domains-behind-major-information-stealing-malware-operation
11. ReliaQuest - "The Infostealer Pipeline: How Russian Market Fuels Credential-Based Attacks" (2 June 2025) — https://reliaquest.com/blog/infostealer-pipeline-stolen-credential-attacks-russian-marketplace/
12. The Record - "Acreed infostealer poised to replace Lumma after global crackdown" (4 June 2025) — https://therecord.media/acreed-infostealer-arises-after-lumma-takedown
13. Trend Micro - "Shifts in the Underground: The Impact of Water Kurita's (Lumma Stealer) Doxxing" (16 October 2025) — https://www.trendmicro.com/en_us/research/25/j/the-impact-of-water-kurita-lumma-stealer-doxxing.html
14. Trend Micro - "Increase in Lumma Stealer Activity Coincides with Use of Adaptive Browser Fingerprinting Tactics" (13 November 2025) — https://www.trendmicro.com/en_us/research/25/k/lumma-stealer-browser-fingerprinting.html
15. Trend Micro - "Fast, Broad, and Elusive: How Vidar Stealer 2.0 Upgrades Infostealer Capabilities" (21 October 2025) — https://www.trendmicro.com/en_us/research/25/j/how-vidar-stealer-2-upgrades-infostealer-capabilities.html
16. Zscaler ThreatLabz - "I StealC You: Tracking the Rapid Changes To StealC" (1 May 2025) — https://www.zscaler.com/blogs/security-research/i-stealc-you-tracking-rapid-changes-stealc
17. Proofpoint - "Operation Endgame Quakes Rhadamanthys" (13 November 2025) — https://www.proofpoint.com/us/blog/threat-insight/operation-endgame-quakes-rhadamanthys
18. INTERPOL - "20,000 malicious IPs and domains taken down in INTERPOL infostealer crackdown" (11 June 2025) — https://www.interpol.int/en/News-and-Events/News/2025/20-000-malicious-IPs-and-domains-taken-down-in-INTERPOL-infostealer-crackdown
19. SpyCloud - "Analyzing the Impact of the Operation Endgame Takedown on Rhadamanthys & the MaaS Ecosystem" (10 December 2025) — https://spycloud.com/blog/impact-operation-endgame-takedown-on-rhadamanthys-stealer/
20. Rapid7 Labs - "Inside Russian Market: Uncovering the Botnet Empire" (7 October 2025) — https://www.rapid7.com/blog/post/tr-inside-russian-market-uncovering-the-botnet-empire/
21. Microsoft - "StealC and Amadey: Breaking down infostealers and the cybercrime services that deliver them" (24 June 2026) — https://www.microsoft.com/en-us/security/blog/2026/06/24/stealc-and-amadey-breaking-down-infostealers-and-the-cybercrime-services-that-deliver-them/
22. Dutch National Police - "Operation Endgame: two infostealers taken down again" (24 June 2026) — https://www.politie.nl/en/news/2026/june/24/11-operation-endgame-two-infostealers-taken-down-again.html
23. Microsoft - "Think before you Click(Fix): Analyzing the ClickFix social engineering technique" (21 August 2025) — https://www.microsoft.com/en-us/security/blog/2025/08/21/think-before-you-clickfix-analyzing-the-clickfix-social-engineering-technique/
24. Microsoft - "Infostealers without borders: macOS, Python stealers, and platform abuse" (2 February 2026) — https://www.microsoft.com/en-us/security/blog/2026/02/02/infostealers-without-borders-macos-python-stealers-and-platform-abuse/
25. Microsoft - "From open lures to cloaked gates: How a macOS ClickFix campaign learned to hide" (5 August 2026) — https://www.microsoft.com/en-us/security/blog/2026/08/05/macos-clickfix-campaign-learned-hide/
26. Microsoft - "ClickFix campaign uses fake macOS utilities lures to deliver infostealers" (6 May 2026) — https://www.microsoft.com/en-us/security/blog/2026/05/06/clickfix-campaign-uses-fake-macos-utilities-lures-deliver-infostealers/
27. Elastic Security Labs - "REVSTEALER ramps up: analysis of up-and-coming infostealer" (2 September 2026) — https://www.elastic.co/security-labs/threat-command/revstealer-credential-harvesting-infostealer
28. Flare - "State of the Dark Web in 2026" (9 April 2026) — https://flare.io/learn/resources/blog/state-of-the-dark-web-2026
29. AhnLab ASEC - "August 2026 Infostealer Trend Report" (22 September 2026) — https://asec.ahnlab.com/en/95519/
30. SecurityWeek - "Ukrainian Raccoon Infostealer Operator Sentenced to Prison in US" (19 December 2024) — https://www.securityweek.com/ukrainian-raccoon-infostealer-operator-sentenced-to-prison-in-us/
31. CyberScoop - "Feds seize 145 domains associated with BidenCash cybercrime platform" (4 June 2025) — https://cyberscoop.com/bidencash-marketplace-domains-seized/
32. BleepingComputer - "Anthropic warns infostealer malware is hijacking Claude sessions to drain usage" (30 August 2026) — https://www.bleepingcomputer.com/news/artificial-intelligence/anthropic-warns-infostealer-malware-is-hijacking-claude-sessions-to-drain-usage/
33. BleepingComputer (sponsored by SOCRadar) - "80,000+ Organizations Had AI Logins Stolen: From Shadow AI to LLMjacking" (28 September 2026) — https://www.bleepingcomputer.com/news/security/80-000-plus-organizations-had-ai-logins-stolen-from-shadow-ai-to-llmjacking/
34. Infosecurity Magazine - "Europol-Led Operation Endgame Takes Down StealC and Amadey Infostealers" (24 June 2026) — https://www.infosecurity-magazine.com/news/operation-endgame-stealc-amadey/
35. Shadowserver Foundation - "Rhadamanthys Historical Bot Infections Special Report" (13 November 2025, updated 15 December 2025) — https://www.shadowserver.org/news/rhadamanthys-historical-bot-infections-special-report/

## Change Log

| Date | Change | Source |
|------|--------|--------|
| 2026-04-05 | Initial creation with baseline intelligence through early 2025 | Training knowledge |
| 2026-09-29 | Refresh covering Jan 2025-Sep 2026: Lumma, Rhadamanthys and StealC/Amadey disruptions; Lumma doxxing; Vidar 2.0; Acreed, Remus, RevStealer and macOS families added; BidenCash seizure; ClickFix and AI-session theft; family and marketplace status corrected; unverified entries flagged | OSINT refresh |
