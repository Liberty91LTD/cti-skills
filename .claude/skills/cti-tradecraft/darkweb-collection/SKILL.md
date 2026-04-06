---
name: darkweb-collection
description: Dark web intelligence collection methodology. Surface-web accessible dark web monitoring, marketplace analysis, and forum intelligence.
user-invocable: false
metadata:
  version: 1.0.0
---

# Dark Web Collection

## Limitations
This platform CANNOT access .onion sites directly. This skill covers:
- Surface-web mirrors of dark web content
- Publicly available dark web intelligence
- Monitoring methodology for when direct access tools are available
- Interpreting dark web intelligence from vendor reports

## What to Monitor

### Ransomware Leak Sites
Most ransomware groups maintain leak sites (sometimes on clearnet mirrors):
- New victims listed (sector, geography, data volume)
- Countdown timers (negotiation status)
- Published data samples
- Group announcements and operational changes

### Underground Forums
Key forums (often mirrored or reported on by vendors):
- **Exploit.in** — Russian-language, IAB marketplace, malware sales
- **XSS.is** — Russian-language, similar to Exploit
- **RAMP** — Ransomware-focused forum
- **BreachForums** (successor to RaidForums) — English-language, data leaks, tools
- **Nulled.to** — Cracking, leaks, tools

### Telegram Channels
Many threat actors have moved to Telegram:
- Hacktivist group channels (claims, DDoS targets)
- Ransomware group communications
- Data leak announcements
- Tool and exploit sales

### Paste Sites
- Pastebin and alternatives
- Leaked credentials, code snippets, manifestos
- IOC dumps from researchers

### Marketplaces (via vendor intelligence)
- **Russian Market** — Infostealer logs, RDP access, credentials
- **Genesis Market** (disrupted 2023, successors active) — Browser fingerprints, cookies
- **2easy** — Infostealer logs
- **Card shops** — Stolen payment card data

## Collection Approach

### Using Vendor Intelligence
Most CTI vendors provide dark web monitoring:
- Recorded Future, Flashpoint, KELA, Searchlight Cyber
- These provide curated, contextualised dark web intelligence
- Source reliability: B (usually reliable vendor with dark web collection capability)

### Using Surface-Web Mirrors
Some dark web content is mirrored or indexed on the clearnet:
- Ransomware leak site trackers (e.g., ransomwatch, ransomlook)
- Dark web search engine caches
- Academic/research databases
- News articles quoting dark web sources

### Using OSINT to Find Dark Web Indicators
- Search for threat actor usernames across platforms
- Monitor for leaked dark web content on paste sites
- Track cryptocurrency wallets associated with threat actors
- Monitor court documents and law enforcement press releases

## Intelligence Requirements from Dark Web

| Requirement | What to Look For |
|------------|-----------------|
| Targeting us? | Organisation name, domain, employee names on leak sites or forums |
| Credential exposure | Corporate email addresses in infostealer logs or breach dumps |
| Supply chain risk | Vendor/partner names on leak or compromise sites |
| Threat actor capability | New tools, exploits, or services being advertised |
| Threat landscape trends | Pricing changes, new services, market dynamics |

## Source Assessment
- Direct dark web observation (if available): Source reliability C-D (depending on forum reputation), Information credibility 3-4
- Vendor dark web intelligence: Source reliability B, Information credibility 2
- Surface-web mirrors: Source reliability C, Information credibility 3 (mirror may be incomplete or delayed)
- News/blog reporting on dark web: Source reliability C, Information credibility 3-4 (second-hand reporting)
