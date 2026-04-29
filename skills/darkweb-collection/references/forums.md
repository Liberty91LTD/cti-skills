# Cybercrime Forums Reference

**Verified through: 2026-04**

Forum lists are transient and rot fast: seizures, voluntary shutdowns, rebrands, and domain changes mean any snapshot is partially stale within weeks. Surface-web mirror domains listed below are the *canonical* clearnet reference points known at verification date; do not treat them as live operational indicators without checking current status. The **Status** column is the single source of truth for currency — always verify against the cited source URL and supplement with runtime lookups where needed. Live .onion v3 addresses are deliberately excluded from this file; resolve those at runtime using the bundled `onion_search.py` script.

---

## 1. Russian-Speaking Elite Forums

Forums in this tier require established reputation, vouching, or both. They are the primary venues for initial access broker (IAB) listings, high-tier malware sales, and RaaS recruitment. Defenders monitor these for early indicators of enterprise compromises.

| Forum | Status | Language | Surface mirror | Onion? | Access | Primary content | Notable | Source |
|-------|--------|----------|----------------|--------|--------|-----------------|---------|--------|
| Exploit (Hack-All) | active | RU | exploit.in | yes | register+vouch | IAB listings, exploit sales, malware-as-a-service, vulnerability research | Founded 2005 as Hack-All; one of the longest-running RU forums; admin "toha" transferred control ~2018; breached (proxy) Mar 2021 | [flare.io](https://flare.io/learn/resources/blog/exploit-forum) |
| XSS (DaMaGeLaB) | active — post-seizure, new admin "Stallman"; trust disrupted | RU | xss.pro | yes | register | Credentials, malware, IAB listings, spam; historically linked to REvil, LockBit, Conti | Founded 2013 as DaMaGeLaB; rebranded XSS.is 2018; admin "Toha" arrested by Ukrainian/French/Europol operation Jul 22 2025; new clearweb xss.pro launched Aug 3 2025; predecessor of DamageLib | [kelacyber.com](https://www.kelacyber.com/blog/xss-forum-after-takedown-damagelib-emerges/) |
| DamageLib | active — low engagement | RU | (onion only — resolve via onion_search.py) | yes | register | Hacking tutorials, malware dev, exploit discussion, IAB listings | Launched Aug 2025 by XSS ex-moderator team (cryptocat, fenix, sizeof, zen) after loss of trust in post-seizure XSS admin; ~33,487 users as of Aug 27 2025 | [kelacyber.com](https://www.kelacyber.com/blog/xss-forum-after-takedown-damagelib-emerges/) |
| Verified (Verifed.ru) | dormant — hacked Jan 2021, effectively destroyed | RU | (onion only — resolve via onion_search.py) | yes | register+vouch | Carding, stolen PII, fraud tutorials | Dates to early-mid 2000s; domain registrar hijacked Jan 20 2021; 3.8 M IP records of members exposed; never fully recovered | [krebsonsecurity.com](https://krebsonsecurity.com/2021/03/three-top-russian-cybercrime-forums-hacked/) |
| Maza (Mazafaka / MFclub) | dormant — breached Mar 2021, ceased operations | RU | (onion only — resolve via onion_search.py) | yes | invite | Elite carding, financial fraud, cash-out services | Founded ~2003; one of the oldest RU elite forums; breached Mar 3 2021 by unknown actor; 3,000-row member dump including ICQ/Skype IDs published | [flashpoint.io](https://flashpoint.io/blog/breelite-cybercrime-forum-maza-breached-by-unknown-attacker/) |
| Crdclub | active (current status uncertain; admin account compromised Feb 2021) | RU | (onion only — resolve via onion_search.py) | yes | register+vouch | Carding, stolen payment card data, fraud services | Admin account hijacked Feb 2021 to divert user funds; forum promised reimbursement; continues to operate per 2024 reporting | [krebsonsecurity.com](https://krebsonsecurity.com/2021/03/three-top-russian-cybercrime-forums-hacked/) |
| RAMP (Russian Anonymous Marketplace) | seized Jan 28 2026 | RU | (onion only — resolve via onion_search.py) | yes | register | RaaS recruitment, ransomware affiliate ads, IAB listings, malware sharing | Launched Jul 2021 by "Orange" / Wazawaka (Mikhail Matveev, indicted 2023) after Exploit/XSS banned ransomware promotion post-Colonial Pipeline; hosted LockBit, ALPHV, RansomHub, Qilin; FBI/SDFL/DOJ CCIPS seizure Jan 28 2026 | [bleepingcomputer.com](https://www.bleepingcomputer.com/news/security/fbi-seizes-ramp-cybercrime-forum-used-by-ransomware-gangs/) |
| WWH-Club | active — administrators indicted; forum distancing from arrested admins | RU | (onion only — resolve via onion_search.py) | yes | pay-to-vouch | Stolen PII, carding, fraud tutorials and "courses", money laundering | Founded ~2012; 353,000+ registered accounts by 2023; offered 6-week fraud courses for ~$975; admins Pavel Kublitskii (RU) and Alex Khodyrev (KZ) arrested Miami, charged Sep 2024 | [flashpoint.io](https://flashpoint.io/blog/wwh-club-russian-cybercrime/) |
| Lolzteam (Zelenka.guru) | active | RU | zelenka.guru | no | open | Gaming/social-media account sales, infostealer ads, traffer team recruitment | Founded ~2013 by Grisha Sutchkov; ~250,000 daily visitors; 65% Russian members, 20% Ukrainian; ~283,000 accounts for sale Feb 2024; minority of members engaged in serious fraud | [flare.io](https://flare.io/learn/resources/blog/top-russian-cybercrime-forums) |
| Best Hack Forum (BHF) | active | RU | bestblackhatforum.com | yes | register | Credential sales, spam tools, combolists, stealer logs, social engineering | Founded 2012; built-in escrow service; Telegram integrations; one of the more stable mid-tier RU forums; active 10+ years | [flare.io](https://flare.io/learn/resources/blog/top-russian-cybercrime-forums) |

---

## 2. English-Speaking General / Data-Leak Forums

Forums primarily serving English-speaking audiences, focused on data leak publication, credential dumps, combo lists, and hacking tools. Access tiers vary widely.

| Forum | Status | Language | Surface mirror | Onion? | Access | Primary content | Notable | Source |
|-------|--------|----------|----------------|--------|--------|-----------------|---------|--------|
| BreachForums v1 (pompompurin) | seized Mar–Jun 2023 | EN | — | yes | register | Stolen data leaks, hacked databases, credential dumps | Founded Mar 4 2022 by Conor Fitzpatrick ("pompompurin", 19); FBI seized Jun 23 2023; pompompurin arrested Mar 15 2023, resentenced 3 yrs prison Sep 2025; successor-of RaidForums | [wikipedia.org](https://en.wikipedia.org/wiki/BreachForums) |
| BreachForums v2 (Baphomet/ShinyHunters) | seized May 15 2024 | EN | — | yes | register | Stolen data leaks, extortion listings | Reopened 2023 under Baphomet + ShinyHunters; seized again May 15 2024 after Europol portal breach listing | [sophos.com](https://www.sophos.com/en-us/blog/taking-the-shine-off-breachforums) |
| BreachForums v3–v4 (IntelBroker / ShinyHunters) | seized/offline Aug 2025; user DB leaked Jan 2026 | EN | — | yes | register | Stolen data leaks, malware trade | IntelBroker (Kai West) assumed ownership 2024; arrested Feb 2025; ShinyHunters, Hollow, Noct, Depressed arrested France Jun 25 2025; 325,000 user records leaked by "James" Jan 2026 | [wikipedia.org](https://en.wikipedia.org/wiki/BreachForums) |
| RaidForums | seized Apr 12 2022 (Operation Tourniquet) | EN | — | no | register | Hacked database sales, credential leaks, hacking tools | Founded 2015 by Diogo Santos Coelho ("Omnipotent"); 530,000+ users; seized Feb 25/Apr 12 2022 by FBI/Europol/USSS; Coelho arrested UK Jan 31 2022; direct predecessor of BreachForums | [secretservice.gov](https://www.secretservice.gov/newsroom/releases/2022/04/us-leads-seizure-one-worlds-largest-hacker-forums-and-arrests) |
| Cracked.io | seized Jan 29 2025 (Operation Talent) | EN | — | no | register | Cracked software, credential stuffing configs, combo lists, hacking tools | Joint operation: FBI, Germany, Italy, Spain, France, Greece, Australia, Romania; 2 arrests, 17 servers seized, €300,000+ cash/crypto; staff confirmed seizure via Telegram | [bleepingcomputer.com](https://www.bleepingcomputer.com/news/security/fbi-seizes-crackedio-nulledto-hacking-forums-in-operation-talent/) |
| Nulled.to | seized Jan 29 2025 (Operation Talent) | EN | — | no | register | Credential leaks, cracked tools, marketplace for stolen data | Seized simultaneously with Cracked.io in same operation; 10M+ combined users across both forums | [bleepingcomputer.com](https://www.bleepingcomputer.com/news/security/fbi-seizes-crackedio-nulledto-hacking-forums-in-operation-talent/) |
| LeakBase | seized Mar 3–4 2026 (Operation Leak) | EN | — | no | register | Stolen database sales, stealer logs, credential combo lists | Founded 2021 as ARES threat group project; 142,000+ members; 215,000+ messages; seized by FBI/Europol 14-country operation Mar 2026; admin arrested by Russian authorities; resurfaced briefly on leakbase.bz | [thehackernews.com](https://thehackernews.com/2026/03/fbi-and-europol-seize-leakbase-forum.html) |
| Exposed.vc | active (as of 2024; status uncertain 2025–2026) | EN | exposed.vc | no | register | Stolen data leaks, breach announcements | Emerged Mar 2023 as a RaidForums/BreachForums successor; attracted displaced users after Breached shutdown; was briefly offered for sale | [cyberint.com](https://cyberint.com/blog/research/breachforums/) |
| DarkForums (DARK4RMY) | active — absorbed BreachForums user base 2025 | EN | darkforums.st | no | register | Data leaks, malware distribution, hacking tools (largely reposted content) | Founded Mar 2022 as DARK4RMY; 600% activity surge Apr–Jun 2025 after BreachForums shutdown; admins AnonOne, Knox; low opsec; founder Lucifer (India) transferred control Aug 2024 | [kelacyber.com](https://www.kelacyber.com/blog/darkforums-chronicles/) |
| HackForums | active | EN | hackforums.net | no | open | Script-kiddie tools, RATs, DDoS services, credential cracking, tutorials | Founded 2007 by "Omniscient"; described by Krebs as overrun with "wannabe hackers"; historically associated with malware distribution; open registration; still operational as of 2025 | [wikipedia.org](https://en.wikipedia.org/wiki/Hack_Forums) |
| Dread | active | EN | (onion only — resolve via onion_search.py) | yes | open | Darknet market discussion, data leaks, ransomware victim announcements, privacy | Launched Feb 15 2018 by "HugBunter"; Reddit-style subdread structure; 372,578 /d/Dread subscribers Sep 2024; 1,700+ active communities; used by ransomware groups for victim comms | [wikipedia.org](https://en.wikipedia.org/wiki/Dread_(forum)) |
| Sinister.ly | active | EN | sinister.ly | no | register | Social engineering, cracking tools, leaked credentials, tutorials | Founded 2016; ~62,000 users; lower tier, skews toward social engineering and cracked tools | [flare.io](https://flare.io/learn/resources/blog/dark-web-forums) |

---

## 3. Carding and Financial Fraud Forums / Shops

Platforms focused on payment card fraud, stolen card data (dumps/CVV2), fullz (complete identity packages), and financial fraud services. Several have shifted from forum to autoshop model.

| Forum | Status | Language | Surface mirror | Onion? | Access | Primary content | Notable | Source |
|-------|--------|----------|----------------|--------|--------|-----------------|---------|--------|
| Joker's Stash | shutdown Feb 15 2021 (voluntary, post-infrastructure seizure) | RU/EN | — | yes | register | Stolen payment card dumps (CP/CNP), CVV2, fullz | Active Oct 2014–Feb 2021; admin alias "JokerStash" / "Vega" (Timur Shakhmametov); DOJ charges filed years post-shutdown; estimated $280M–$1B revenue; 40M+ card records | [flashpoint.io](https://flashpoint.io/blog/jokers-stash-shutting-down-for-good-this-time/) |
| UniCC | shutdown Jan 22 2022 (voluntary + Russian MVD seizure) | RU/EN | — | yes | register | Stolen payment card data (CP/CNP) | Active 2013–2022; controlled ~30% of stolen card market; ~$358M estimated revenue; Russian MVD seized alongside Trump's Dumps, Ferum, Sky-Fraud, UAS RDP Jan 22 2022 | [malwarebytes.com](https://www.malwarebytes.com/blog/news/2022/01/infamous-dark-net-carding-site-unicc-to-close) |
| BriansClub | active (as of mid-2025 reporting) | RU/EN | (onion only — resolve via onion_search.py) | yes | register | Stolen payment card dumps (CP), CVV2, fullz | Active since ~2014–2015; ~26M cards' worth of data hacked from it 2019 (ironic breach); $126M+ in sales; one of oldest surviving card autoshops | [krebsonsecurity.com](https://krebsonsecurity.com/tag/briansclub/) |
| BidenCash | seized Jun 4 2025 | EN | — | yes | open (dumps released for free as marketing) | Stolen payment card data, CVV2, PII bundles | Active Mar 2022–Jun 2025; 117,000+ customers; 15M+ card records trafficked; $17M+ revenue; 145 domains seized by USSS/FBI/DOJ Eastern District of Virginia; Dutch NHTCU, Shadowserver assisted | [secretservice.gov](https://www.secretservice.gov/newsroom/releases/2025/06/us-government-seizes-approximately-145-criminal-marketplace-domains) |
| Russianmarket.to | active | RU/EN | russianmarket.to | yes | register | RDP access (until Jan 2024), then pivot to stealer logs, CVV2, dumps | Active since ~2019; post-Genesis Market vacuum drove rapid growth; 180,000+ logs for sale H1 2025; avg $10/bot; pivoted from RDP to stealer logs Jan 2024; continuous operations with no takedown | [rapid7.com](https://www.rapid7.com/blog/post/tr-inside-russian-market-uncovering-the-botnet-empire/) |
| B1ack's Stash | active | EN | (onion only — resolve via onion_search.py) | yes | register | Stolen payment card data | Emerged 2024; gained attention Feb 2025 with 4M free card dump promoted on XSS and Exploit as marketing | [darkowl.com](https://www.darkowl.com/blog-content/darknet-market-place-spotlight-b1acks-stash/) |
| WWH-Club (carding angle) | active — see Russian Elite section; carding is primary purpose | RU | — | yes | pay-to-vouch | See Russian Elite table; PII, cards, fraud tutorials | Cross-listed; primary purpose is carding and fraud education; 353,000+ accounts | [flashpoint.io](https://flashpoint.io/blog/wwh-club-russian-cybercrime/) |

---

## 4. Infostealer Log Marketplaces

Closer to autoshops than traditional forums, but defenders monitor them as forums because threat actors use them to advertise tools, recruit traffers, and discuss tactics. Logs contain browser credentials, session cookies, crypto wallets, and system fingerprints harvested by infostealer malware.

| Forum / Shop | Status | Language | Surface mirror | Onion? | Access | Primary content | Notable | Source |
|--------------|--------|----------|----------------|--------|--------|-----------------|---------|--------|
| Genesis Market | seized Apr 4 2023 (Operation Cookie Monster) | EN | — | yes | invite | Packaged infostealer logs with browser-plugin "bot" format for plug-and-play identity fraud | FBI Milwaukee + 44 field offices + Europol 17-country operation; 119 arrested; 1.5M compromised computers; 80M+ account credentials; unique browser-extension model set it apart from competitors | [eurojust.europa.eu](https://www.eurojust.europa.eu/news/takedown-online-market-sold-stolen-account-credentials-Operation-Cookie-Monster) |
| Russian Market | active | RU/EN | russianmarket.to (shared with fraud shop) | yes | register | Raw infostealer logs (Lumma, RedLine, Vidar, Raccoon, Stealc, Rhadamanthys), RDP access (ceased Jan 2024) | Active since ~2019; 150% listing growth in nine months post-Genesis seizure; 1.6M posts analyzed by Rapid7; 61% of logs contain SaaS credentials; dominant marketplace for raw logs 2023–2026 | [bleepingcomputer.com](https://www.bleepingcomputer.com/news/security/russian-market-emerges-as-a-go-to-shop-for-stolen-credentials/) |
| 2easy Shop | active (credibility concerns; scam allegations 2022–2023) | EN | (onion only — resolve via onion_search.py) | yes | register | Raw infostealer logs (primarily RedLine in early years; multi-stealer by 2024) | Launched Jan 2020; grew to 600,000 bots by late 2021; allegations of reposting stale/invalid data from Russian Market from late 2022; users alleged registration fee theft; resilient but trust-impaired | [kelacyber.com](https://www.kelacyber.com/blog/2easy-logs-marketplace-on-the-rise/) |
| Exodus Marketplace | active | EN | (onion only — resolve via onion_search.py) | yes | register | Infostealer logs (Genesis Market-style; 7,000+ bots across 192 countries) | Launched Jan 2024; announced on Cracked.io Feb 10 2024; positioned as Genesis replacement; domain changed twice 2024; prices $3–$10/bot; BTC/Monero/LTC payments | [cyble.com](https://cyble.com/blog/exodus-marketplace-a-haven-for-exiled-criminals/) |

---

## 5. Exploit and Zero-Day Broker Forums

Forums with dedicated exploit/zero-day sales or brokering sections. These are largely clearnet or semi-clearnet and cater to both criminal and gray-market buyers.

| Forum | Status | Language | Surface mirror | Onion? | Access | Primary content | Notable | Source |
|-------|--------|----------|----------------|--------|--------|-----------------|---------|--------|
| 0day.today | active | EN/RU | 0day.today | no | register / pay-per-exploit | N-day and some 0-day exploit listings, PoC code, vulnerability disclosure database | Public-facing exploit aggregator; prices 10–100x legitimate bug bounty rates for black-market listings; cited in Trend Micro N-day market research; accessible via standard browser | [trendmicro.com](https://www.trendmicro.com/vinfo/us/security/news/vulnerabilities-and-exploits/trends-and-shifts-in-the-underground-n-day-exploit-market) |
| Exploit.in (exploit broker sections) | active | RU | exploit.in | yes | register+vouch | IAB listings; dedicated exploit auction and sales sections; malware-as-a-service | Also in Russian Elite table; exploit brokering is a core sub-function; has auction system for high-value exploits; preferred by IABs seeking enterprise targets | [flare.io](https://flare.io/learn/resources/blog/exploit-forum) |

---

## 6. Hacktivist Coordination Boards

Operationally relevant hacktivist communities that have demonstrably coordinated DDoS or leak operations. Included where CTI reporting confirms defender relevance. Violent-extremist forums excluded entirely.

| Forum / Channel | Status | Language | Surface mirror | Onion? | Access | Primary content | Notable | Source |
|-----------------|--------|----------|----------------|--------|--------|-----------------|---------|--------|
| KillNet (Telegram-primary) | active — reduced tempo post-2024 | RU/EN | (Telegram channel; no onion) | no | open (Telegram) | DDoS coordination against NATO/Western targets, hacktivist claims, attack target lists | Pro-Russia hacktivist collective; active since 2022 Ukraine invasion; Mandiant confirmed new capabilities 2023; CISA advisories issued; operates primarily via Telegram | [cloud.google.com](https://cloud.google.com/blog/topics/threat-intelligence/killnet-new-capabilities-older-tactics) |
| Anonymous Sudan (KillNet affiliate) | disrupted — founders indicted Oct 2024 | EN/AR | (Telegram channel) | no | open (Telegram) | DDoS-for-hire services, anti-Western/pro-Islamic hacktivist claims | Emerged Jan 2023; declared KillNet allegiance; responsible for Jun 2023 Microsoft DDoS outages; Ahmed Salah Yusuuf Omer and Alaa Salah Yusuuf Omer (brothers) indicted California Oct 2024; suspected Russian direction | [darkreading.com](https://www.darkreading.com/cyberattacks-data-breaches/pro-islam-anonymous-sudan-hacktivists-front-russia-killnet-operation) |

---

## 7. Regional Forums

At least one entry per region where reliable CTI sourcing exists. Regions without verifiable public sourcing are omitted rather than fabricated.

### Chinese-Language

| Forum | Status | Language | Surface mirror | Onion? | Access | Primary content | Notable | Source |
|-------|--------|----------|----------------|--------|--------|-----------------|---------|--------|
| 52pojie (I Love Cracking) | active | ZH | 52pojie.cn | no | open | Software cracking, malware analysis, reverse engineering, Android cracking, virus analysis | Founded Mar 2008; 10+ years continuous operation; primarily clearnet (Great Firewall shapes Chinese DDW toward clearnet); high-quality technical posts; community-driven | [webz.io](https://webz.io/dwp/the-top-5-chinese-platforms-on-the-deep-and-dark-web-in-2023/) |
| Exchange Market (DeepMix) | active | ZH | (onion only — resolve via onion_search.py) | yes | register | Stolen PII, carding, hacking services; Chinese-user-focused | Founded 2013 as Chinese Darknet Forum; pivoted to marketplace 2015; prioritizes user anonymity; face DDoS disruptions historically; predominantly Chinese membership | [webz.io](https://webz.io/dwp/the-top-5-chinese-platforms-on-the-deep-and-dark-web-in-2023/) |
| FREECITY | active | ZH/EN/KO | (onion only — resolve via onion_search.py) | yes | register | Stolen data, WeChat account theft, credit cards, developer tools | Founded 2016; multi-language (Chinese, English, Korean); forum + marketplace structure; diverse goods and services | [webz.io](https://webz.io/dwp/the-top-5-chinese-platforms-on-the-deep-and-dark-web-in-2023/) |

### Spanish / Latin American

| Forum | Status | Language | Surface mirror | Onion? | Access | Primary content | Notable | Source |
|-------|--------|----------|----------------|--------|--------|-----------------|---------|--------|
| Indetectables | active (declining prominence; members migrating to RU/EN forums) | ES | indetectables.net | no | register | Crypters, botnets, RATs, ransomware discussion; historically Spain/LATAM focused | One of the oldest Spanish-language cybercrime communities; prominent Spanish/LATAM actors increasingly use Exploit, Nulled, Hackforums instead; Trend Micro documented transition | [trendmicro.com](https://www.trendmicro.com/vinfo/us/security/news/cybercrime-and-digital-threats/across-the-span-of-the-spanish-cybercriminal-underground-current-activities-and-trends) |

### Persian / Iranian

| Forum | Status | Language | Surface mirror | Onion? | Access | Primary content | Notable | Source |
|-------|--------|----------|----------------|--------|--------|-----------------|---------|--------|
| Ashiyane Forum | shutdown Aug 5 2018 | FA | — | no | register | Security research, defacement, APT actor coordination; IRGC-adjacent | Founded 2003 by Behrooz Kamalian; ~20,000 users; IRGC-linked via Ashiyane Digital Security Team; APT33 members present; shut down following gambling activity exposure; members split between VBIran.ir and Persian Tools Forum | [recordedfuture.com](https://www.recordedfuture.com/research/ashiyane-forum-history) |

### Turkish

| Forum | Status | Language | Surface mirror | Onion? | Access | Primary content | Notable | Source |
|-------|--------|----------|----------------|--------|--------|-----------------|---------|--------|
| Warriors.to | active | TR/EN | warriors.to | no | register | Patriotic hacktivism, DDoS coordination, credential leaks, warez | Founded 2022 with stated aim of uniting Turkish hackers; Recorded Future Insikt Group analysis Jan 2023; Turkish law enforcement pressure keeps Turkish-targeting content off-platform; activity mirrors geopolitical events | [recordedfuture.com](https://www.recordedfuture.com/research/current-trends-in-the-turkish-language-dark-web) |

---

## 8. Doxing / Harassment-Cybercrime Overlap

Included because these platforms are widely cited in CTI reporting as enablers of SIM-swapping, account takeover, swatting, and extortion chains — all of which feed financially motivated cybercrime. Note: pure harassment platforms that do not overlap with financially motivated cybercrime are out of scope.

| Forum | Status | Language | Surface mirror | Onion? | Access | Primary content | Notable | Source |
|-------|--------|----------|----------------|--------|--------|-----------------|---------|--------|
| Doxbin | active (suffered data breach Feb 2025) | EN | doxbin.com | yes | register | Personal information (dox) listings, SIM-swap facilitation, swatting support | Onion-original; widely cited in LAPSUS$ coverage (15 LATAM/Portugal victims); KrebsOnSecurity extensively documented; operator linked to Com/harm group ecosystem; 41,544 user credentials exposed by TOoDA group Feb 2025 | [flashpoint.io](https://flashpoint.io/blog/doxbin-leak/) |

---

## Sources

All URLs cited inline above. Deduplicated canonical source list:

- [bleepingcomputer.com — Cracked.io / Nulled.to Operation Talent seizure](https://www.bleepingcomputer.com/news/security/fbi-seizes-crackedio-nulledto-hacking-forums-in-operation-talent/)
- [bleepingcomputer.com — RAMP cybercrime forum seizure Jan 2026](https://www.bleepingcomputer.com/news/security/fbi-seizes-ramp-cybercrime-forum-used-by-ransomware-gangs/)
- [bleepingcomputer.com — Russian Market emerges post-Genesis](https://www.bleepingcomputer.com/news/security/russian-market-emerges-as-a-go-to-shop-for-stolen-credentials/)
- [cloud.google.com — Mandiant: KillNet new capabilities](https://cloud.google.com/blog/topics/threat-intelligence/killnet-new-capabilities-older-tactics)
- [cyberint.com — BreachForums tracker](https://cyberint.com/blog/research/breachforums/)
- [cyble.com — Exodus Marketplace](https://cyble.com/blog/exodus-marketplace-a-haven-for-exiled-criminals/)
- [darkreading.com — Anonymous Sudan / KillNet analysis](https://www.darkreading.com/cyberattacks-data-breaches/pro-islam-anonymous-sudan-hacktivists-front-russia-killnet-operation)
- [darkowl.com — B1ack's Stash](https://www.darkowl.com/blog-content/darknet-market-place-spotlight-b1acks-stash/)
- [eurojust.europa.eu — Operation Cookie Monster (Genesis Market)](https://www.eurojust.europa.eu/news/takedown-online-market-sold-stolen-account-credentials-Operation-Cookie-Monster)
- [flashpoint.io — Maza breach](https://flashpoint.io/blog/breelite-cybercrime-forum-maza-breached-by-unknown-attacker/)
- [flashpoint.io — WWH-Club disruption](https://flashpoint.io/blog/wwh-club-russian-cybercrime/)
- [flashpoint.io — Joker's Stash shutdown](https://flashpoint.io/blog/jokers-stash-shutting-down-for-good-this-time/)
- [flashpoint.io — Doxbin leak](https://flashpoint.io/blog/doxbin-leak/)
- [flare.io — Exploit forum IAB analysis](https://flare.io/learn/resources/blog/exploit-forum)
- [flare.io — Top Russian cybercrime forums](https://flare.io/learn/resources/blog/top-russian-cybercrime-forums)
- [flare.io — Dark web forums overview](https://flare.io/learn/resources/blog/dark-web-forums)
- [kelacyber.com — XSS takedown, DamageLib emergence](https://www.kelacyber.com/blog/xss-forum-after-takedown-damagelib-emerges/)
- [kelacyber.com — DarkForums chronicles](https://www.kelacyber.com/blog/darkforums-chronicles/)
- [kelacyber.com — 2easy logs marketplace](https://www.kelacyber.com/blog/2easy-logs-marketplace-on-the-rise/)
- [krebsonsecurity.com — Three top Russian forums hacked 2021](https://krebsonsecurity.com/2021/03/three-top-russian-cybercrime-forums-hacked/)
- [malwarebytes.com — UniCC shutdown](https://www.malwarebytes.com/blog/news/2022/01/infamous-dark-net-carding-site-unicc-to-close)
- [rapid7.com — Inside Russian Market](https://www.rapid7.com/blog/post/tr-inside-russian-market-uncovering-the-botnet-empire/)
- [recordedfuture.com — Ashiyane forum history](https://www.recordedfuture.com/research/ashiyane-forum-history)
- [recordedfuture.com — Turkish dark web trends](https://www.recordedfuture.com/research/current-trends-in-the-turkish-language-dark-web)
- [secretservice.gov — BidenCash 145 domains seized Jun 2025](https://www.secretservice.gov/newsroom/releases/2025/06/us-government-seizes-approximately-145-criminal-marketplace-domains)
- [secretservice.gov — RaidForums seizure Apr 2022](https://www.secretservice.gov/newsroom/releases/2022/04/us-leads-seizure-one-worlds-largest-hacker-forums-and-arrests)
- [sophos.com — Taking the shine off BreachForums](https://www.sophos.com/en-us/blog/taking-the-shine-off-breachforums)
- [thehackernews.com — LeakBase seizure Mar 2026](https://thehackernews.com/2026/03/fbi-and-europol-seize-leakbase-forum.html)
- [trendmicro.com — Spanish cybercriminal underground](https://www.trendmicro.com/vinfo/us/security/news/cybercrime-and-digital-threats/across-the-span-of-the-spanish-cybercriminal-underground-current-activities-and-trends)
- [trendmicro.com — Underground N-day exploit market](https://www.trendmicro.com/vinfo/us/security/news/vulnerabilities-and-exploits/trends-and-shifts-in-the-underground-n-day-exploit-market)
- [webz.io — Top 5 Chinese deep/dark web platforms 2023](https://webz.io/dwp/the-top-5-chinese-platforms-on-the-deep-and-dark-web-in-2023/)
- [wikipedia.org — BreachForums](https://en.wikipedia.org/wiki/BreachForums)
- [wikipedia.org — RaidForums](https://en.wikipedia.org/wiki/RaidForums)
- [wikipedia.org — Dread forum](https://en.wikipedia.org/wiki/Dread_(forum))
- [wikipedia.org — Hack Forums](https://en.wikipedia.org/wiki/Hack_Forums)
