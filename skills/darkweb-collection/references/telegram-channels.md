# Cybercrime-Relevant Telegram Channels — Defender Reference

**Verified through:** 2026-04
**Maintained by:** darkweb-collection skill / OSINT researcher

> **Important caveats — read before use.** These lists are transient and rot fast: channels are renamed, banned, and resurrected under new handles constantly; a handle that was active last month may be seized, dormant, or squatted by an unrelated actor today. Handles are listed in `@handle` form without resolved `https://t.me/` hyperlinks to reduce the risk of accidentally directing users to phishing mirrors or hostile pages; defenders should navigate manually and verify channel identity before interaction. The **Status** column is the authoritative field — treat any channel marked `banned`, `seized`, or `dormant` as potentially resurrected under a new handle and validate before collecting against it.

---

## 1. Ransomware Group Official Channels

Channels operated by or directly attributed to named RaaS groups for victim shaming, affiliate recruitment, and leak publication. Most groups prefer Tor-hosted leak sites; Telegram channels are supplementary and more volatile.

| Channel name | @handle | Status | Affiliation | Type | Language | Notable | Source |
|---|---|---|---|---|---|---|---|
| LockBit 3.0 | @lockbitchannels | seized | LockBit lineage | leak-announcement | EN/multi | Launched Mar 2024 by LockBitSupp404; displayed FBI seizure notice Jun 9 2024; LockBit 5.0 launched Sep 2025 | [x.com/intel_anastasia](https://x.com/intel_anastasia/status/1799842165746467204) |
| LockBit APT | @LockBit_APT | banned | LockBit lineage | leak-announcement | EN | Listed in deepdarkCTI as ONLINE prior to ban | [github.com/fastfire](https://github.com/fastfire/deepdarkCTI/blob/main/telegram_threat_actors.md) |
| 8Base | @eightbase | seized | 8Base / Phobos variant | RaaS-comms | EN | Leak site and channel seized Feb 2025, Operation Phobos Aetor; 4 members arrested | [thehackernews.com](https://thehackernews.com/2025/02/8base-ransomware-data-leak-sites-seized.html) |
| Medusa "information support" | @OSINT_without_borders | active | Medusa ransomware | leak-announcement | EN | Clearnet Telegram channel created Jul 2021; Medusa partnered Nov 2022; branded "OSINT Without Borders"; clearnet-accessible; over 700 shared files | [unit42.paloaltonetworks.com](https://unit42.paloaltonetworks.com/medusa-ransomware-escalation-new-leak-site/) |
| Snatch info | @snatch_info | active | Snatch Team | leak-announcement | EN/RU | Listed in CISA/FBI advisory; operates alongside Tor site; claimed Tyson Foods breach | [therecord.media](https://therecord.media/snatch-ransomware-group-alert-fbi-cisa) |
| Bl00dy Ransomware Gang | @bl00dy_Ransomware_Gang | active | Bl00dy (independent) | RaaS-comms | EN | Created Jul 2022; left Telegram Sep 2024 after policy change; relaunched Oct 2024 under same name; exploited PaperCut CVE-2023-27350 | [bleepingcomputer.com](https://www.bleepingcomputer.com/news/security/leaked-lockbit-30-builder-used-by-bl00dy-ransomware-gang-in-attacks/) |
| Kill Security | @k1llsec | active | KillSec (Kill Security) | RaaS-comms | EN/RU | Transitioned from hacktivist to RaaS Jun 2024; $250 entry fee; 276 documented victims; avoids CIS nations | [halcyon.ai](https://www.halcyon.ai/threat-group/killsec) |

**Intelligence gaps — ransomware:** Public Telegram handles for ALPHV/BlackCat (exited Mar 2024), RansomHub (went silent Apr 2025), Akira, Play, Qilin (channel blocked post-Synnovis injunction), BianLian, Hunters International, Cactus, and Money Message were not confirmed in Tier-1 public sources at collection time. These groups operate primarily via Tor-hosted DLS; any Telegram presence is either private, unconfirmed, or rapidly rotated.

---

## 2. Initial Access Broker / Access-Listing Storefront Channels

IABs primarily operate on Russian-language forums (Exploit, XSS, RAMP) and private Telegram channels. Publicly documented storefronts are rare; most confirmed handles come from brief researcher exposure before takedown.

| Channel name | @handle | Status | Affiliation | Type | Language | Notable | Source |
|---|---|---|---|---|---|---|---|
| BreachForums announcements | @breachforums | seized | ShinyHunters / Baphomet lineage | IAB-storefront | EN | 18K+ members; seized by FBI May 15 2024 and again 2025; ShinyHunters recovered domain briefly; now declared honeypot risk | [therecord.media](https://therecord.media/breachforums-platform-seized-by-fbi-doj) |
| Jacuzzi / Baphchat | @jacuzzidf | replaced-by-@DarkForumsHub | BreachForums / DarkForums lineage | IAB-storefront | EN | Former official BreachForums chat; taken over by DarkForums Jun 2025 following ShinyHunters exit | [redhotcyber.com](https://www.redhotcyber.com/en/post/darkforums-takes-over-breachforums-telegram-channel-the-jacuzzi/) |
| DarkForums Hub | @DarkForumsHub | active | DarkForums / DarkArmy | IAB-storefront | EN | BreachForums successor; admin "Knox" took over from "Lucifer" Aug 2024; aggregates content rather than originating breaches | [kelacyber.com](https://www.kelacyber.com/blog/darkforums-chronicles/) |

**Intelligence gaps — IABs:** Most confirmed IAB Telegram activity occurs in private invite-only channels not amenable to open-source confirmation. The list above reflects only publicly documented channels from Tier-1 sources.

---

## 3. Infostealer Log Shops

Channels distributing stolen credential logs, combo lists, and stealer output. Handles in this category are highly volatile — Telegram has accelerated takedowns since Aug 2024 following Pavel Durov's arrest.

| Channel name | @handle | Status | Affiliation | Type | Language | Notable | Source |
|---|---|---|---|---|---|---|---|
| Moon Cloud | not confirmed | active | Unattributed (LummaC2/RedLine aggregator) | infostealer-shop | EN/RU | 20K+ members; described as "central aggregation hub" for LummaC2 and RedLine logs; daily updates | [nordstellar.com](https://nordstellar.com/blog/top-dark-web-telegram-groups-and-channels/) |
| Observer Cloud | not confirmed | active | Unattributed | infostealer-shop | EN/RU | 15K+ members; operational since Apr 2022; presents as "educational"; long-standing credential dump channel | [webz.io](https://webz.io/dwp/top-dark-web-telegram-chat-groups-and-channels/) |
| Daisy Cloud | not confirmed | active | Unattributed | infostealer-shop | EN/RU | 14K+ members; daily free and premium log uploads; active credential distribution | [webz.io](https://webz.io/dwp/top-dark-web-telegram-chat-groups-and-channels/) |
| Omega Cloud | not confirmed | active | Unattributed (RedLine-focused) | infostealer-shop | EN/RU | 6K+ members; subscription-based; distributes RedLine-harvested credentials | [nordstellar.com](https://nordstellar.com/blog/top-dark-web-telegram-groups-and-channels/) |
| LummaC2 Stealer | @LummaC2Stealer | seized | LummaC2 (Shamel) | infostealer-shop | EN/RU | Official promo/update channel; 1,800+ members at peak; Microsoft DCU + Bitsight seized 1,000+ domains and 90+ channels including this; infrastructure dismantled 2025 | [infosecurity-magazine.com](https://www.infosecurity-magazine.com/news/lumma-stealer-proliferation-fueled/) |
| BidenCash CVV Discussion | not confirmed | seized | BidenCash carding marketplace | infostealer-shop | EN/RU | Discussed stolen payment card data; 4.6K+ members documented; marketplace seized Jun 2025 (145 domains); $17M revenue; Telegram channel status unconfirmed post-seizure | [cyberscoop.com](https://cyberscoop.com/bidencash-marketplace-domains-seized/) |

**Note on "not confirmed" handles:** Moon Cloud, Observer Cloud, Daisy Cloud, and Omega Cloud are named in multiple Tier-1 CTI vendor reports but without a confirmed `@handle` in the same source documents. Defenders should treat channel-name-only references as directional, not definitive. Handles for these channels are confirmed to rotate frequently.

---

## 4. Hacktivist Collectives

Channels used to coordinate, claim, and publicize DDoS attacks, defacements, and data leaks. Operationally relevant channels are those where researchers have corroborated a documented cyber operation — not pure propaganda. Attribution language below reflects what the cited source stated.

### Pro-Russian / Russia-Ukraine war-aligned

| Channel name | @handle | Status | Affiliation | Type | Language | Notable | Source |
|---|---|---|---|---|---|---|---|
| NoName057(16) RU | @noname05716 | active | NoName057(16) | hacktivist-ops | RU | Primary RU channel; 45K+ subscribers; avg 6 posts/day; DDoSia project coordination; targets NATO members | [sentinelone.com](https://www.sentinelone.com/labs/noname05716-the-pro-russian-hacktivist-group-targeting-nato/) |
| NoName057(16) EN | @noname05716eng | active | NoName057(16) | hacktivist-ops | EN | English-language mirror of main channel | [tgstat.com](https://tgstat.com/channel/@noname05716eng) |
| NoName057(16) EN ver | @noname05716engver | active | NoName057(16) | hacktivist-ops | EN | Second English version; documented by SentinelOne | [sentinelone.com](https://www.sentinelone.com/labs/noname05716-the-pro-russian-hacktivist-group-targeting-nato/) |
| CyberArmyofRussia_Reborn (CARR) | @CyberArmyofRussia_Reborn | active | CARR / GRU-nexus | hacktivist-ops | RU | GRU-founded per DOJ indictment; 75K+ followers; claimed ICS/OT intrusions; water utility disruptions US and EU 2023-2024; also operates as Z-Pentest | [justice.gov](https://www.justice.gov/opa/pr/justice-department-announces-actions-combat-two-russian-state-backed-cyber-criminal-hacking) |
| Z-Pentest / Z-Alliance | @ZAllianceRU | active | CARR / Z-Pentest | hacktivist-ops | RU | CARR sub-brand focused on SCADA/OT intrusions; formed Sep 2024 by CARR + NoName057 admins; documented in CISA advisory AA25-343A | [cisa.gov](https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-343a) |
| WE ARE KILLNET | @killnet_reservs | dormant | Killnet (post-sale) | hacktivist-ops | RU | One of the documented Killnet channels; sold to new owner late 2023; activity declined sharply; Killnet2.0 emerged Jan 2024 | [kelacyber.com](https://www.kelacyber.com/blog/russia-ukraine-war-pro-russian-hacktivist-activity-two-years-on/) |
| Killnet official | @Killneto | active | Killnet (commercial phase) | hacktivist-ops | RU/EN | Documented in breachsense.com CTI channel list as ONLINE; group shifted to cybercrime-for-hire post-2023 sale | [breachsense.com](https://www.breachsense.com/threat-actor-channels/) |
| IT Army of Russia | @itarmyofrussianews | active | IT Army of Russia (GRU-adjacent) | hacktivist-ops | RU | 800+ members; recruitment-focused; DDoS coordination; documented by Intel 471 alongside TwoNet | [intel471.com](https://www.intel471.com/blog/pro-russian-hacktivism-shifting-alliances-new-groups-and-risks) |

### Pro-Ukraine

| Channel name | @handle | Status | Affiliation | Type | Language | Notable | Source |
|---|---|---|---|---|---|---|---|
| IT Army of Ukraine | @itarmyofukraine2022 | active | IT Army of Ukraine (volunteer) | hacktivist-ops | EN/UK | 240K+ followers Feb 2024; crowdsourced DDoS against Russian infrastructure; most active group targeting Russia per F6 2024; 94 operations documented | [en.wikipedia.org/wiki/IT_Army_of_Ukraine](https://en.wikipedia.org/wiki/IT_Army_of_Ukraine) |

### Pro-Palestinian / MENA-aligned

| Channel name | @handle | Status | Affiliation | Type | Language | Notable | Source |
|---|---|---|---|---|---|---|---|
| Dark Storm Team | @DarkStormTeams | active | Dark Storm Team | hacktivist-ops | AR/EN | Claimed DDoS on X (Twitter) Mar 2025; claimed Zoom disruption Apr 2025; offers DDoS-for-hire; documented by Check Point and Orange Cyberdefense | [blog.checkpoint.com](https://blog.checkpoint.com/security/dark-storm-team-claims-responsibility-for-cyber-attack-on-x-platform-what-it-means-for-the-future-of-digital-security/) |
| RipperSec | @RipperSec | active | RipperSec (Malaysia, pro-Palestinian) | hacktivist-ops | multi | Founded Jun 2023; 2K+ members; 196 DDoS incidents Jan-Aug 2024; MegaMedusa DDoS tool; targets Israel-aligned orgs | [cyble.com](https://cyble.com/threat-actor-profiles/rippersec-hacktivist-group/) |
| DragonForce Malaysia | @dragonforceio | active | DragonForce Malaysia | hacktivist-ops | multi | Pro-Palestinian; launched OpPatuk against India Jun 2022; claimed ransomware aspirations 2023; distinct from DragonForce RaaS | [radware.com](https://www.radware.com/security/ddos-knowledge-center/ddospedia/dragonforce-malaysia/) |
| Handala Channel | @Handala_hack | active | Handala Hack Team (MOIS-linked) | hacktivist-ops | FA/EN | FBI attributed to Iranian MOIS "Justice Homeland" unit; Dec 2023 origin; multiple channels (primary + @Handala_backup); primary went silent Feb 2025, resumed Jul 2025 | [infosecwriteups.com](https://infosecwriteups.com/cti-research-handala-hack-group-aka-handala-hack-team-ddbdd294cfb8) |
| Anonymous Sudan | not confirmed | seized | Anonymous Sudan (disrupted) | hacktivist-ops | AR/EN/RU | First surfaced Jan 2023; 80K subscribers at peak; DOJ indictment Oct 2024; two Sudanese brothers charged; DDoS tools seized; channel status post-seizure unconfirmed | [therecord.media](https://therecord.media/anonymous-sudan-brothers-charged-ddos-attacks-hospital-critical-infrastructure) |
| DieNet | banned | banned | DieNet | hacktivist-ops | EN/AR | Announced Mar 7 2025 in a now-banned channel; promoted by Mr.Hamza, Sylhet Gang-SG, LazaGrad Hack; 60+ claimed DDoS attacks in first 2 months; targets US CNI | [netscout.com](https://www.netscout.com/blog/asert/profiling-dienet-new-hacktivist-threat) |

### Other hacktivist / mixed attribution

| Channel name | @handle | Status | Affiliation | Type | Language | Notable | Source |
|---|---|---|---|---|---|---|---|
| Indian Cyber Force | @TeamIndianCyberForce | active | Indian Cyber Force | hacktivist-ops | EN | Named one of 5 most active hacktivist groups 2024 by Webz.io; collaborates with TeamUCC, Team-Network-Nine | [webz.io](https://webz.io/dwp/the-5-most-active-hacktivist-groups-of-2024/) |

---

## 5. Breach Announcement / Data-Leak Aggregator Channels

Channels that publish victim data, aggregate leaks from multiple actors, or serve as cross-group announcement boards.

| Channel name | @handle | Status | Affiliation | Type | Language | Notable | Source |
|---|---|---|---|---|---|---|---|
| Handala backup leaks | @Handala_backup | active | Handala Hack Team (MOIS-linked) | breach-aggregator | FA/EN | Backup/overflow channel for Handala; used when primary channel is banned; also aggregates Israel-related breach material | [infosecwriteups.com](https://infosecwriteups.com/cti-research-handala-hack-group-aka-handala-hack-team-ddbdd294cfb8) |
| Snatch news | @snatch_news | active | Snatch Team | breach-aggregator | EN | Secondary Snatch channel; mirrors victim announcements from @snatch_info; listed in deepdarkCTI | [github.com/fastfire](https://github.com/fastfire/deepdarkCTI/blob/main/telegram_threat_actors.md) |
| BreachForums News | @BreachForumsNews | seized | ShinyHunters / BreachForums | breach-aggregator | EN | Secondary news channel for BreachForums; seized alongside main channel May 2024 | [therecord.media](https://therecord.media/breachforums-platform-seized-by-fbi-doj) |
| TEAM UNDERGROUND | @UndergroundDataLeaks | active | Team Underground | breach-aggregator | EN/RU | Multi-actor data leak aggregation; listed in deepdarkCTI ransomware/leak section | [github.com/fastfire](https://github.com/fastfire/deepdarkCTI/blob/main/ransomware_gang.md) |

---

## 6. Defender-Run Cyber-News Aggregators

These channels are operated by defenders, researchers, or CTI vendors. They are explicitly **safe-to-follow** and useful as second-tier collection for monitoring underground chatter without direct exposure to criminal infrastructure. Listed here to aid newer analysts in distinguishing safe research resources from hostile channels.

| Channel name | @handle | Status | Affiliation | Type | Language | Notable | Source |
|---|---|---|---|---|---|---|---|
| vx-underground | @vxunderground | active | vx-underground (independent research) | news-aggregator | EN | 48K+ subscribers; largest public malware sample and paper archive; covers threat actor activity and TTPs; not a threat actor channel | [tgstat.com](https://tgstat.com/channel/@vxunderground) |
| FalconFeeds | @falconfeeds | active | FalconFeeds.io / Technisanct (vendor) | news-aggregator | EN | Real-time dark web and ransomware tracker; monitors 3000+ threat actors; mirrors significant underground announcements | [t.me/falconfeeds](https://t.me/falconfeeds/) |
| Cyber Threat Intelligence | @ctinow | active | Independent (community-run) | news-aggregator | EN | Aggregates CTI news and threat actor announcements; documented across multiple defender resource lists | [t.me/ctinow](https://t.me/ctinow) |

**Note — CyberKnow (@Cyberknow20):** CyberKnow is a widely-cited hacktivist tracker but operates primarily via X/Twitter (@Cyberknow20) and Substack, not a standalone Telegram channel. Referenced here as a research resource rather than a channel entry.

---

## Sources (deduplicated)

- [x.com/intel_anastasia — LockBit Telegram seizure claim Jun 2024](https://x.com/intel_anastasia/status/1799842165746467204)
- [github.com/fastfire/deepdarkCTI — telegram_threat_actors.md](https://github.com/fastfire/deepdarkCTI/blob/main/telegram_threat_actors.md)
- [github.com/fastfire/deepdarkCTI — ransomware_gang.md](https://github.com/fastfire/deepdarkCTI/blob/main/ransomware_gang.md)
- [thehackernews.com — 8Base ransomware sites seized Feb 2025](https://thehackernews.com/2025/02/8base-ransomware-data-leak-sites-seized.html)
- [unit42.paloaltonetworks.com — Medusa ransomware "information support" channel](https://unit42.paloaltonetworks.com/medusa-ransomware-escalation-new-leak-site/)
- [therecord.media — Snatch ransomware group FBI/CISA advisory](https://therecord.media/snatch-ransomware-group-alert-fbi-cisa)
- [bleepingcomputer.com — Bl00dy gang uses leaked LockBit 3.0 builder](https://www.bleepingcomputer.com/news/security/leaked-lockbit-30-builder-used-by-bl00dy-ransomware-gang-in-attacks/)
- [halcyon.ai — KillSec threat group profile](https://www.halcyon.ai/threat-group/killsec)
- [therecord.media — BreachForums platform seized by FBI/DOJ](https://therecord.media/breachforums-platform-seized-by-fbi-doj)
- [redhotcyber.com — DarkForums takes over BreachForums' Jacuzzi channel](https://www.redhotcyber.com/en/post/darkforums-takes-over-breachforums-telegram-channel-the-jacuzzi/)
- [kelacyber.com — DarkForums Chronicles leadership analysis](https://www.kelacyber.com/blog/darkforums-chronicles/)
- [nordstellar.com — Top hazardous Telegram channels (Moon Cloud, Omega Cloud)](https://nordstellar.com/blog/top-dark-web-telegram-groups-and-channels/)
- [webz.io — Top dark web Telegram channels (Observer Cloud, Daisy Cloud)](https://webz.io/dwp/top-dark-web-telegram-chat-groups-and-channels/)
- [infosecurity-magazine.com — LummaC2 stealer Telegram proliferation](https://www.infosecurity-magazine.com/news/lumma-stealer-proliferation-fueled/)
- [cyberscoop.com — BidenCash 145 domains seized Jun 2025](https://cyberscoop.com/bidencash-marketplace-domains-seized/)
- [sentinelone.com — NoName057(16) Telegram channel documentation](https://www.sentinelone.com/labs/noname05716-the-pro-russian-hacktivist-group-targeting-nato/)
- [tgstat.com — @noname05716eng channel statistics](https://tgstat.com/channel/@noname05716eng)
- [justice.gov — DOJ actions against CARR and GRU-sponsored hacking groups](https://www.justice.gov/opa/pr/justice-department-announces-actions-combat-two-russian-state-backed-cyber-criminal-hacking)
- [cisa.gov — AA25-343A: Pro-Russia Hacktivists Conduct Opportunistic Attacks](https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-343a)
- [kelacyber.com — Russia-Ukraine pro-Russian hacktivist activity two years on](https://www.kelacyber.com/blog/russia-ukraine-war-pro-russian-hacktivist-activity-two-years-on/)
- [breachsense.com — Telegram CTI threat actor channels list](https://www.breachsense.com/threat-actor-channels/)
- [intel471.com — Pro-Russian hacktivism: IT Army of Russia, TwoNet](https://www.intel471.com/blog/pro-russian-hacktivism-shifting-alliances-new-groups-and-risks)
- [en.wikipedia.org/wiki/IT_Army_of_Ukraine](https://en.wikipedia.org/wiki/IT_Army_of_Ukraine)
- [blog.checkpoint.com — Dark Storm Team X platform attack Mar 2025](https://blog.checkpoint.com/security/dark-storm-team-claims-responsibility-for-cyber-attack-on-x-platform-what-it-means-for-the-future-of-digital-security/)
- [cyble.com — RipperSec hacktivist group profile](https://cyble.com/threat-actor-profiles/rippersec-hacktivist-group/)
- [radware.com — DragonForce Malaysia DDOSpedia](https://www.radware.com/security/ddos-knowledge-center/ddospedia/dragonforce-malaysia/)
- [infosecwriteups.com — CTI Research: Handala Hack Group Mar 2026](https://infosecwriteups.com/cti-research-handala-hack-group-aka-handala-hack-team-ddbdd294cfb8)
- [therecord.media — Anonymous Sudan brothers charged Oct 2024](https://therecord.media/anonymous-sudan-brothers-charged-ddos-attacks-hospital-critical-infrastructure)
- [netscout.com — Profiling DieNet: A new hacktivist threat](https://www.netscout.com/blog/asert/profiling-dienet-new-hacktivist-threat)
- [webz.io — 5 most active hacktivist groups of 2024](https://webz.io/dwp/the-5-most-active-hacktivist-groups-of-2024/)
- [tgstat.com — @vxunderground channel statistics](https://tgstat.com/channel/@vxunderground)
- [t.me/falconfeeds — FalconFeeds Telegram channel](https://t.me/falconfeeds/)
- [t.me/ctinow — Cyber Threat Intelligence channel](https://t.me/ctinow)
