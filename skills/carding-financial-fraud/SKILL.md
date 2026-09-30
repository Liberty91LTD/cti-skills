---
name: carding-financial-fraud
description: Use when the user asks about carding, BIN attacks, payment-card breach markets, fullz/CVV2 trade, autoshops (BidenCash, Brian's Club, Russianmarket, B1ack's Stash), or financial-fraud TTPs. Self-updating knowledge cell.
user-invocable: true
metadata:
  category: knowledge-cell
  created: 2026-04-05
  last_updated: 2026-09-29
  update_count: 1
  confidence: moderate
---

# Carding & Financial Fraud

## Executive Summary

Carding and financial fraud represent one of the oldest and most mature cybercriminal ecosystems, encompassing the theft, trade, and monetization of payment card data and financial credentials. The ecosystem spans from initial data theft (via digital skimming, phishing, POS malware, and database breaches) through underground marketplace trading to monetization via card-not-present (CNP) fraud, mobile wallet fraud, money mule networks, and reshipping schemes. CNP data still dominates the underground card market, but card-present fraud has returned in a new form: stolen cards provisioned into Apple and Google wallets and used or relayed over NFC [11][13].

The card shop landscape changed materially in 2025. BidenCash, previously the most visible shop, was seized on June 4, 2025 by the US Secret Service and FBI with Dutch police support (about 145 domains; no arrests announced) [9]. In September 2025 the Manhattan District Attorney seized 12 domains belonging to five further vendors, including B1ack's Stash, but Recorded Future assesses that most of those shops kept posting card data on related domains [10][11]. B1ack's Stash took over BidenCash's free-dump marketing tactic and released a further 4.6 million records in May 2026 [12]. Recorded Future counted about 142 million card records posted for sale on dark web marketplaces in 2025, down 19% from 2024, while freely exposed records on Telegram and other sources rose 26% to a comparable volume, and 82% of for-sale CNP records came with victim contact details [11].

The most significant shift in technique is the Chinese-language fraud ecosystem. Smishing kits such as Lighthouse, Darcula and Lucid harvest card data and one-time codes, enroll the cards in mobile wallets on attacker-controlled phones, and cash out in stores or through NFC relay ("ghost tap") tools sold as a service on Telegram [13][14][17]. Google sued the Lighthouse operators in November 2025 and the service reported its servers blocked within days, though researchers expected the activity to continue under other names [15][16]. NFC relay malware has since spread beyond Chinese-speaking vendors to independently developed families in Europe and Latin America [18][20].

Web skimming (Magecart) remains stable at scale rather than declining: Recorded Future tracked more than 10,500 active e-skimmer infections in 2025 despite the PCI DSS 4.0 script-integrity requirements taking effect, with skimmer kits and skimming-as-a-service lowering the barrier to entry [11]. The fraud ecosystem continues to overlap with infostealers, Business Email Compromise (BEC), SIM swapping and Fraud-as-a-Service (FaaS) offerings, and in 2026 researchers documented AI agents being used to automate retailer compromise and skimmer deployment [28].

## Key Actors

| Actor/Entity | Type | Notable Characteristics | Status |
|-------------|------|------------------------|--------|
| BidenCash | Card Shop | Operated from March 2022; marketed via large free card dumps. Per US authorities: 117,000+ customers, 15M+ card numbers trafficked, $17M+ revenue [9] | Seized June 4, 2025; no arrests announced |
| B1ack's Stash | Card Shop | Active since at least 2023; adopted the free-dump marketing tactic (2024, 2025, May 2026); named in Manhattan DA domain seizure of September 2025 [10][11][12] | Active (disrupted, continued operating) |
| SIKTOR, PP24, CVVUNION, VCLUB | Card Shops | Smaller vendors whose domains were seized by the Manhattan DA alongside B1ack's Stash [10] | Disrupted September 2025; current status unconfirmed |
| Joker's Stash | Card Shop | Formerly dominant card shop; voluntarily retired February 2021 | Defunct |
| BriansClub | Card Shop | Major card shop; was itself breached in 2019 exposing 26M card records | Status unclear |
| Genesis Market | Credential/Bot Market | Sold browser fingerprints and credentials; seized in Operation Cookie Monster April 2023 | Seized |
| Russian Market | Log/Credential Shop | Operating since 2020; Rapid7 describes infostealer logs as its main offering (180,000+ logs offered in H1 2025), with card data a secondary line [26] | Active |
| Smishing Triad / Lighthouse, Darcula, Lucid, Xinxin | Chinese-language phishing-as-a-service | SMS/iMessage/RCS phishing kits that harvest card data and one-time codes for mobile wallet provisioning [13][14][15] | Active; Lighthouse disrupted November 2025 |
| TX-NFC, X-NFC, NFU Pay | NFC relay Fraud-as-a-Service | Chinese-language vendors selling "ghost tap" relay apps by subscription on Telegram; tracked by Group-IB [17] | Active |
| Magecart Groups | Digital Skimming Collective | Umbrella term for multiple groups conducting web-based card skimming; increasingly kit- and service-based (Sniffer by Fleras, AcceptCar) [11] | Active (various) |
| FIN7 | Cybercrime Group | Sophisticated group with ties to POS malware (Carbanak/FIN7 campaigns); members arrested but operations continued | Partially disrupted |
| Scattered Spider | Cybercrime Collective | SIM swapping, social engineering, extortion; young Western actors. Multiple members convicted 2025-2026; the NCA said the September 2025 arrests effectively halted the group's activity [27] | Degraded |
| Various BEC Networks | Fraud Operations | West African (Yahoo Boys) and Eastern European networks conducting BEC and romance fraud | Active |
| SIM Swapping Crews | Account Takeover | Loosely organized groups bribing telecom employees or exploiting SS7 | Active |

## Current Activity

### Card Shop Disruption and Free Dump Marketing
With BidenCash seized in June 2025, no single shop holds the position it once did. Recorded Future notes that the seizure followed a steady decline in BidenCash's market share, and that takedowns affecting at least five other marketplaces had limited effect because most resumed posting on related domains [11]. B1ack's Stash continues the free-dump tactic: a release in February 2025 (3.5 million records per Recorded Future; "over 4 million" per SecurityWeek), a second 2025 release of 1.7 million, and 4.6 million in May 2026 [11][12]. SOCRadar assessed about 4.3 million of the May 2026 records as new and roughly 70% as US-issued; the shop presented the release as a penalty against sellers who resold its stock elsewhere [12]. Card records exposed for free on Telegram and other sources now match the dark web shops' for-sale volume [11].

### Smishing-Driven Mobile Wallet Provisioning
China-based phishing-as-a-service groups send toll, parcel and bank lures over SMS, iMessage and RCS. Victims enter card details and then a one-time code, which the operators use to enroll the card in a mobile wallet on a phone they control. Researchers report several wallets loaded per device and a wait of 7-10 days before use or resale of the phone [13][15]. Google's November 2025 complaint says Lighthouse offered over 600 templates imitating more than 400 entities and harmed more than a million victims in 120 countries; its estimate of cards stolen in the US ranges from 12 million to 115 million, so the true figure is uncertain [15][16]. Silent Push observed about 25,000 phishing domains active in any 8-day period [14][15].

### NFC Relay and "Ghost Tap" Fraud
NFC relay fraud passes contactless payment data from a stolen card or provisioned wallet to a mule's device at a point-of-sale terminal or ATM in another location. ThreatFabric documented ghost tap in November 2024 [13][21]. Two variants exist: relay of cards already stolen through phishing, where the victim's device is never infected [17], and Android malware that persuades victims to tap their own card against an infected phone (NGate, SuperCard X, PhantomCard, WindRelay) [18][19][29]. Group-IB identified more than 54 relay app variants and at least $355,000 in illegitimate transactions through one POS vendor between November 2024 and August 2025 [17]. In May 2026 Cleafy reported two independently built families, DevilNFC and NFCMultiPay, attributed to Spanish- and Portuguese-speaking developers and showing signs of AI-assisted development [20]. In August 2026 Group-IB reported WindRelay, delivered with a SpyNote variant during vishing calls against victims in Czechia, Slovakia, Slovenia and Poland [18].

### Magecart/Digital Skimming Evolution
Digital skimming has industrialized. Recorded Future counted more than 10,500 unique e-skimmer infections active in 2025 (7,300 of them new), likely compromising over 23 million transactions, and attributed 26% of infections to a single commercial kit, Sniffer by Fleras [11]. The PCI DSS 4.0 requirement 6.4.3 (client-side script integrity monitoring) took effect in March 2025, but Recorded Future found no corresponding decrease in Magecart impact [11]. Recent campaigns abuse trusted services to evade allowlists: Silent Push exposed a skimming network active since early 2022 (January 2026) [24], and Sansec reported a skimmer hidden in SVG elements on 99 Magento stores (April 2026) and a campaign using Google Tag Manager and a payment processor's API for delivery and exfiltration (June 2026) [22][23]. In September 2026 Gambit reported a Chinese-speaking operator using open-source AI agent frameworks to compromise retailers and deploy skimmers at an estimated cost of about $25 per target; Gambit cautions that its analysis is early-stage [28].

### Card Testing and Purchase Scams
Recorded Future identified more than 1,350 merchants abused for card testing in 2025, 94% of them not seen before, and at least 27 million card records exposed through Telegram-based generation and testing services that can support BIN attacks. It also identified more than 3,600 scam merchant accounts used in purchase scams, where victims authorize the payment themselves [11].

### SIM Swapping and Account Takeover Escalation
SIM swapping attacks have expanded beyond cryptocurrency theft to target traditional financial accounts, corporate accounts, and even government officials. Techniques include bribing or socially engineering telecom employees, exploiting eSIM provisioning vulnerabilities, and using SS7 protocol weaknesses. Several high-profile prosecutions have followed (see Historical Events), but the technique remains prevalent due to the fundamental weakness of SMS-based authentication. One-time password interception more broadly is now a standard component of wallet and relay fraud [11].

## Historical Events

| Date | Event | Impact |
|------|-------|--------|
| 2018 | British Airways Magecart breach | 380,000 card details stolen via injected checkout script; ICO fined BA £20M |
| 2019 | BriansClub breach | 26M stolen card records from the card shop itself were leaked; data shared with banks |
| Feb 2021 | Joker's Stash retirement | Largest card shop voluntarily closed; created market fragmentation |
| Apr 2023 | Operation Cookie Monster (Genesis Market) | FBI-led takedown seized Genesis Market; 119 arrests globally; disrupted bot/fingerprint market |
| 2022-2025 | BidenCash free dumps | Repeated free releases of stolen card data as marketing, including 3.3M cards between October 2022 and February 2023 [9] and 910,000 in April 2025 [11] |
| 2024 | PCI DSS 4.0 transition | New requirements for client-side script monitoring; full enforcement March 2025 |
| 2024-2025 | FIN7 members sentenced | Multiple FIN7 members received significant prison sentences in US courts |
| 2024-2026 | Scattered Spider prosecutions | Noah Urban sentenced to 10 years (August 2025); Tyler Buchanan pleaded guilty in the US (April 2026); Thalha Jubair and Owen Flowers each sentenced in the UK to five years and six months (July 2026) [27] |
| Feb 2025 | B1ack's Stash free dump | Release of 3.5M to 4M+ card records (sources differ) as marketing [11][12] |
| Apr 2025 | SuperCard X disclosed | Cleafy exposed a Chinese-speaking malware-as-a-service for NFC relay fraud, first seen targeting Italy [19] |
| Jun 4, 2025 | BidenCash seizure | US Secret Service and FBI, with Dutch police, Shadowserver and Searchlight Cyber, seized about 145 domains and cryptocurrency; no arrests announced [9] |
| Sep 22, 2025 | Manhattan DA domain seizures | 12 domains of five card vendors (SIKTOR, PP24, CVVUNION, VCLUB, B1ack's Stash) seized; more than 1M cards involved; investigation ongoing [10] |
| Nov 4, 2025 | Operation Chargeback | German-led action coordinated by Europol and Eurojust against three networks accused of misusing card data of 4.3M cardholders (EUR 300M damage, 2016-2021); 18 arrests including payment service provider executives [25] |
| Nov 12, 2025 | Google v. Lighthouse | Civil suit (RICO, Lanham Act, CFAA) against 25 unnamed defendants; Lighthouse reported its servers blocked within days [15][16] |
| Jan 2026 | Ghost Tapped research | Group-IB published its analysis of Chinese tap-to-pay relay vendors [17] |
| May 2026 | B1ack's Stash 4.6M dump | Largest free release by the shop to date, eight months after its domains were seized [12] |

## TTP Evolution

**Data Theft Methods**: The ecosystem has evolved from physical skimming devices and POS RAM scraping malware (2010s) to predominantly web-based digital skimming (Magecart-style JavaScript injection) and mass data theft via infostealer malware. Server-side skimmers that intercept payment data at the application layer are increasingly common, as they evade client-side Content Security Policy (CSP) and script monitoring solutions.

**Mobile Wallet and NFC Abuse**: Since 2024 the main innovation has been converting phished card data into mobile wallet tokens and relaying NFC transactions to mules. This restores card-present fraud without cloning a chip, and wallet transactions tend to be treated as trusted. Recorded Future identifies the card provisioning attempt as the most reliable point for detection; Krebs' sources recommend that issuers require in-app authentication rather than SMS codes for provisioning [11][13].

**Marketplace Infrastructure**: Card shops have moved from forums with manual transactions to automated platforms with APIs, validity checkers (testing cards with small transactions), replacement guarantees (refunds for dead cards), and sophisticated search/filter capabilities. Multi-vendor marketplaces now coexist with single-operator shops. Telegram channels serve as both advertising and direct sales channels.

**Monetization**: CNP fraud techniques include using residential proxies to match cardholder geolocation, anti-fingerprinting browsers (Multilogin, GoLogin) to evade device fingerprinting, and automated checkout bots for rapid purchases. Gift card purchasing remains a primary cashout method. Cryptocurrency purchasing using stolen cards provides another laundering avenue.

**Money Mule Operations**: Recruitment of money mules has shifted from in-person "work from home" scams to social media and messaging app recruitment. Professional mule herders manage networks of mules across countries. Mules receive fraudulent funds and forward them, taking a commission. Some operations use cryptocurrency ATMs for rapid conversion.

**Identity Fraud (Fullz)**: Complete identity packages ("fullz") containing name, SSN, DOB, address, email, phone, and sometimes bank credentials trade for $15-$65 depending on credit score and completeness. Synthetic identity fraud — combining real and fabricated data to create new identities — is a growing trend that is harder to detect than traditional identity theft.

## Ecosystem & Infrastructure Patterns

**Supply Chain**: Card data flows from theft (skimming, breaches, infostealers) → aggregation by data brokers → card shop listings → purchase by carders → monetization via CNP fraud or resale. Each stage has specialized actors, and data may pass through multiple intermediaries before final use.

**Quality Assurance**: Card shops offer "checker" services that validate cards are still active by running small authorization charges. Cards are priced by freshness, bank, type (credit vs. debit), level (Classic, Gold, Platinum, Corporate), and geographic region. Corporate and high-limit cards command premium prices ($20-$100+).

**Fraud-as-a-Service**: Turnkey fraud packages include phishing kits targeting specific banks, fraud tutorials, pre-configured anti-detect browsers with stolen cookies/fingerprints, residential proxy access, and money mule network access. These services democratize fraud, enabling low-skill operators to conduct sophisticated attacks.

**Geographic Patterns**: Major carding actor concentrations include Russia/CIS (card shop operators, malware developers), West Africa (BEC, romance fraud, money mules), Southeast Asia (scam compounds, pig butchering operations), and Western countries (SIM swapping, money mule recruitment). Fraud scam compounds in Myanmar, Cambodia, and Laos have drawn international attention for human trafficking elements.

## Tooling

| Tool | Category | Usage |
|------|----------|-------|
| Magecart skimmers | Data Theft | JavaScript injections into e-commerce checkout pages; sold as kits and services (Sniffer by Fleras, AcceptCar) [11] |
| Smishing kits (Lighthouse, Darcula, Lucid) | Data Theft | Phishing-as-a-service harvesting card data and one-time codes for wallet provisioning [14][15] |
| NFC relay apps (NFCGate derivatives, Z-NFC, TX-NFC, SuperCard X, PhantomCard, WindRelay) | Monetization | Relay contactless transactions to mule devices at POS terminals and ATMs [13][17][18][19] |
| Anti-detect browsers (Multilogin, GoLogin) | Fraud Tooling | Spoof browser fingerprints to evade fraud detection |
| Residential proxies (911.re successors, various) | Infrastructure | Match cardholder geolocation for CNP fraud |
| SMS interceptors / SS7 tools | Account Takeover | Intercept 2FA codes for bank account takeover |
| Card checker services | Validation | Verify card validity before use |
| Infostealer logs | Data Supply | Lumma, Rhadamanthys, Acreed and others feeding card/credential markets [26] |
| POS malware (various) | Data Theft | RAM scraping on point-of-sale terminals (declining) |
| E-commerce bots | Monetization | Automated checkout for rapid fraudulent purchases |
| Telegram bots | Marketplace | Automated card shops and checker services via Telegram |
| Cashout guides/tutorials | Knowledge | Step-by-step fraud methodology documentation |

## Intelligence Gaps

- **Scam compound scale**: The true scale and financial impact of Southeast Asian scam compounds (pig butchering, investment fraud) is poorly quantified, though estimates suggest tens of billions in annual losses.
- **Synthetic identity fraud volume**: The prevalence of synthetic identity fraud is difficult to measure because many losses are misclassified as credit losses rather than fraud losses by financial institutions.
- **Cryptocurrency intersection**: The overlap between traditional carding/fraud operations and cryptocurrency-focused theft (exchange account takeover, DeFi exploitation) is not well-mapped.
- **Real-time card fraud attribution**: Attributing specific card fraud transactions to specific card shop purchases or breach events remains extremely difficult for law enforcement and financial institutions.
- **Fraud-as-a-Service market size**: The total revenue of FaaS platforms and their contribution to overall fraud losses is not well-estimated.

- **BriansClub status**: Unconfirmed. No primary source opened in the September 2026 refresh establishes whether the shop is operating; secondary listings describe repeated disruption and domain churn.
- **FIN7 current activity**: Not re-verified in the September 2026 refresh; the status above is carried over from the baseline.
- **Operators behind seized shops**: No arrests were announced for BidenCash or the vendors named by the Manhattan DA, and the operators remain publicly unidentified [9][10].
- **Lighthouse after the lawsuit**: Whether the service resumed under the same or another name is not confirmed; estimates of cards stolen vary by an order of magnitude [15][16].
- **Ghost tap losses**: Published loss figures cover single vendors or campaigns; no aggregate loss estimate for NFC relay fraud was found.
- **Baseline figures**: The CNP loss estimate in earlier versions of this cell and the Genesis Market arrest count were not re-verified.

## Sources & References

1. Europol - "Internet Organised Crime Threat Assessment (IOCTA) 2024" — https://www.europol.europa.eu/iocta-report
2. Gemini Advisory (Recorded Future) - "Card Fraud Intelligence Reports" — https://www.recordedfuture.com/
3. FBI - "Operation Cookie Monster: Genesis Market Takedown" (April 2023) — https://www.fbi.gov/
4. PCI Security Standards Council - "PCI DSS v4.0" — https://www.pcisecuritystandards.org/
5. APWG - "Phishing Activity Trends Reports" — https://apwg.org/trendsreports/
6. Group-IB - "Hi-Tech Crime Trends" reports — https://www.group-ib.com/resources/research/
7. Flashpoint - "Financial Fraud Intelligence" — https://flashpoint.io/
8. US Secret Service - Financial Crimes Investigations — https://www.secretservice.gov/investigation/financial-crimes
9. US Secret Service - "U.S. Government Seizes Approximately 145 Criminal Marketplace Domains" (June 4, 2025) — https://www.secretservice.gov/newsroom/releases/2025/06/us-government-seizes-approximately-145-criminal-marketplace-domains
10. Manhattan District Attorney's Office - "Manhattan D.A.'s Office Seizes Domains Of Websites Selling More Than 1 Million Stolen Credit Cards" (September 22, 2025) — https://manhattanda.org/manhattan-d-a-s-office-seizes-domains-of-websites-selling-more-than-1-million-stolen-credit-cards/
11. Recorded Future - "Annual Payment Fraud Intelligence Report: 2025" (early 2026) — https://assets.recordedfuture.com/Reports/Annual_Payment_Fraud_Intelligence_Report_2025.pdf
12. SecurityWeek - "B1ack's Stash Marketplace Gives Away 4.6 Million Stolen Credit Cards" (May 19, 2026; reports SOCRadar analysis) — https://www.securityweek.com/b1acks-stash-marketplace-gives-away-4-6-million-stolen-credit-cards/
13. KrebsOnSecurity - "How Phished Data Turns into Apple & Google Wallets" (February 18, 2025) — https://krebsonsecurity.com/2025/02/how-phished-data-turns-into-apple-google-wallets/
14. KrebsOnSecurity - "China-based SMS Phishing Triad Pivots to Banks" (April 10, 2025) — https://krebsonsecurity.com/2025/04/china-based-sms-phishing-triad-pivots-to-banks/
15. KrebsOnSecurity - "Google Sues to Disrupt Chinese SMS Phishing Triad" (November 2025) — https://krebsonsecurity.com/2025/11/google-sues-to-disrupt-chinese-sms-phishing-triad/
16. SecurityWeek - "Google Says Chinese 'Lighthouse' Phishing Kit Disrupted Following Lawsuit" (November 14, 2025) — https://www.securityweek.com/google-says-chinese-lighthouse-phishing-kit-disrupted-following-lawsuit/
17. Group-IB - "Ghost Tapped: Tracking the Rise of Chinese Tap-to-pay Android Malware" (January 7, 2026) — https://www.group-ib.com/blog/ghost-tapped-chinese-malware/
18. Group-IB - "Gone with the WindRelay: A New Malware Combo Behind a Growing Fraud Scheme" (August 12, 2026) — https://www.group-ib.com/blog/windrelay-nfc-spynote-rat-combo-fraud/
19. Cleafy - "SuperCard X: exposing a Chinese-speaker MaaS for NFC Relay fraud operation" (April 18, 2025) — https://www.cleafy.com/cleafy-labs/supercardx-exposing-chinese-speaker-maas-for-nfc-relay-fraud-operation
20. Cleafy - "NFC Relay Goes Local: How AI Is Accelerating a New Wave of Independent Malware Developers" (May 18, 2026) — https://www.cleafy.com/cleafy-labs/nfc-relay-goes-local-how-ai-is-accelerating-a-new-wave-of-independent-malware-developers
21. ThreatFabric - "Fraud Year in Review: What 2025 taught us for 2026" (November 12, 2025) — https://www.threatfabric.com/blogs/fraud-year-in-review-what-2025-taught-us-for-2026
22. Sansec - "SVG Onload Tag Hides Magecart Skimmer on 99 Stores" (April 7, 2026) — https://sansec.io/research/svg-onload-magecart-skimmer
23. Sansec - "Magecart skimmer turns Stripe into a malware command server" (June 4, 2026) — https://sansec.io/research/stripe-api-skimmer-infrastructure
24. Silent Push - "Silent Push Uncovers New Magecart Network: Disrupting Online Shoppers Worldwide" (January 13, 2026) — https://www.silentpush.com/blog/magecart/
25. Europol - "Operation Chargeback: 4.3 million cardholders affected, EUR 300 million in damages" (November 2025) — https://www.europol.europa.eu/media-press/newsroom/news/operation-chargeback-43-million-cardholders-affected-eur-300-million-in-damages ; detail from BleepingComputer (November 4, 2025) — https://www.bleepingcomputer.com/news/security/europol-credit-card-fraud-rings-stole-eur-300-million-from-43-million-cardholders/
26. Rapid7 - "Inside Russian Market: Uncovering the Botnet Empire" (October 7, 2025) — https://www.rapid7.com/blog/post/tr-inside-russian-market-uncovering-the-botnet-empire/
27. KrebsOnSecurity - "Scattered Spider Hackers Plead Guilty on Day 1 of Trial" (June 23, 2026) — https://krebsonsecurity.com/2026/06/scattered-spider-hackers-plead-guilty-on-day-1-of-trial/ ; SecurityWeek - "Two Scattered Spider Hackers Sentenced to Jail in UK" (July 16, 2026) — https://www.securityweek.com/two-scattered-spider-hackers-sentenced-to-jail-in-uk/
28. Gambit - "Autonomous AI Agents are breaking into hundreds of Online Retailers for $25 a target in an ongoing campaign" (September 22, 2026) — https://gambit.security/blog-posts/autonomous-ai-agents-online-retailers-25-a-company
29. The Hacker News - "New Android Malware Wave Hits Banking via NFC Relay Fraud, Call Hijacking, and Root Exploits" (August 2025; reports ThreatFabric's PhantomCard research) — https://thehackernews.com/2025/08/new-android-malware-wave-hits-banking.html

## Change Log

| Date | Change | Source |
|------|--------|--------|
| 2026-04-05 | Initial creation with baseline intelligence through early 2025 | Training knowledge |
| 2026-09-29 | Refresh covering January 2025 to September 2026: BidenCash seizure and Manhattan DA seizures, B1ack's Stash dumps, smishing-driven wallet provisioning and Lighthouse lawsuit, NFC relay/ghost tap families, Magecart statistics and campaigns, Operation Chargeback, Scattered Spider prosecutions; corrected market statuses; 21 sources added | OSINT refresh |
