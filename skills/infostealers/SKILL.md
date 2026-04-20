---
name: infostealers
description: Knowledge cell for infostealers. Self-updating intelligence knowledge base.
user-invocable: true
metadata:
  category: knowledge-cell
  created: 2026-04-05
  last_updated: 2026-04-05
  update_count: 0
  confidence: moderate
---

# Infostealers

## Executive Summary

Infostealer malware has become one of the most consequential threats in the cybercrime ecosystem, serving as a foundational enabler for ransomware, account takeover, corporate network intrusion, and financial fraud. These malware families operate under a Malware-as-a-Service (MaaS) model, with developers offering subscriptions ($100-$300/month) that include the malware builder, a management panel, and regular updates to evade detection. Upon execution, infostealers harvest browser-stored credentials, session cookies, cryptocurrency wallet data, autofill data, and system information, packaging the results into "logs" that are then sold on dedicated marketplaces or used directly by the operator.

The log marketplace ecosystem is substantial. Russian Market has emerged as the dominant platform for purchasing individual infostealer logs, following the law enforcement takedown of Genesis Market in April 2023 (Operation Cookie Monster). Genesis Market had been unique in selling persistent "bot" access that included browser fingerprints, enabling buyers to impersonate victims' browser sessions. Telegram channels also serve as major distribution points for both bulk and individual log sales. A single high-value corporate log — containing VPN credentials, SSO session cookies, or cloud service tokens — can sell for $10-$500, while bulk residential logs sell for as little as $1-$10 each.

The connection between infostealers and ransomware operations has tightened significantly. Initial Access Brokers (IABs) systematically harvest corporate VPN, RDP, and Citrix credentials from infostealer logs and resell this access to ransomware affiliates. Many ransomware incidents can be traced back to credentials originally stolen by infostealers months earlier. Distribution methods have evolved from traditional email spam to sophisticated SEO poisoning campaigns, malvertising through Google Ads, and trojanized software downloads, making infostealers a pervasive threat that affects both individual consumers and enterprises.

## Key Actors

| Stealer Family | Status | Notable Characteristics | Pricing |
|---------------|--------|------------------------|---------|
| RedLine | Disrupted (Oct 2024) | Was most prolific stealer 2020-2024; Operation Magnus seized infrastructure | $150/month (was) |
| Raccoon Stealer v2 | Disrupted/Uncertain | Developer Mark Sokolovsky arrested (Netherlands); v2 launched after v1 disruption | $200/month (was) |
| Vidar | Active | Derived from Arkei; distributed via malvertising and SEO poisoning; long-running | ~$250/month |
| Lumma Stealer | Active | Rapidly growing market share since 2023; sophisticated anti-analysis; C2 rotation | $250-$1000/tier |
| StealC | Active | Emerged 2023; lightweight; modular; popular on Russian-language forums | $200/month |
| Rhadamanthys | Active | Sophisticated; written in C++; uses AI-based OCR for cryptocurrency seed phrase theft | $250/month |
| Meta Stealer | Active | Targets macOS in addition to Windows; distributed via malvertising | $125-$300/month |
| Mystic Stealer | Active | Emerged mid-2023; polymorphic; targets 40+ browsers and extensions | $150/month |
| RisePro | Active | Growing adoption; distributed via pay-per-install services | $150/month |
| Atomic Stealer (AMOS) | Active | macOS-focused; distributed via malvertising and fake app sites | $1000/month |

## Current Activity

### Lumma Stealer's Market Dominance (2024-2025)
Following the disruption of RedLine in Operation Magnus (October 2024), Lumma Stealer has emerged as arguably the most prevalent infostealer family. Lumma offers tiered subscriptions with advanced features including persistent cookie restoration (attempting to revalidate expired session cookies), corporate log filtering, and sophisticated anti-analysis techniques including C2 domain rotation and encrypted communications. Distribution campaigns leverage Google Ads malvertising, fake CAPTCHA pages, and trojanized software download sites at scale.

### Operation Magnus — RedLine/META Disruption (October 2024)
In October 2024, an international law enforcement operation led by Dutch police disrupted the infrastructure of RedLine Stealer and the related META Stealer. The operation seized servers, domains, and Telegram channels used for distribution and sales. While significant, the infostealer ecosystem quickly adapted, with operators migrating to Lumma, StealC, and other alternatives, demonstrating the resilience of the MaaS model.

### macOS Stealer Proliferation
The emergence and growth of macOS-targeting infostealers (Atomic Stealer/AMOS, Meta Stealer for macOS, Poseidon/RodriguesDecryptor) represents a significant shift. These stealers target Keychain passwords, browser data, cryptocurrency wallets, and files. Distribution primarily occurs through malvertising campaigns impersonating legitimate software downloads (Arc browser, Notion, etc.) and through DMG files distributed via social engineering.

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
| Oct 2024 | Operation Magnus (RedLine/META) | International operation disrupted RedLine infrastructure; multiple arrests |
| Late 2024 | Chrome cookie encryption (App-Bound Encryption) | Google Chrome implemented enhanced cookie protection; stealer developers rapidly developed bypasses |

## TTP Evolution

**Distribution Methods**: The evolution from email spam attachments (2020-2021) to sophisticated distribution via SEO poisoning, Google Ads malvertising, and fake software download sites (2023-present) represents a major shift. Current campaigns create convincing fake websites for popular software (Slack, Zoom, OBS Studio, various gaming tools) that rank in search results or appear in sponsored ad positions. The "fake CAPTCHA" technique emerged in 2024, where malicious sites present a verification challenge that instructs users to open Run dialog (Win+R) and paste a PowerShell command that downloads the stealer.

**Anti-Analysis**: Modern stealers employ VM/sandbox detection, anti-debugging, string encryption, and control flow obfuscation. Lumma and Rhadamanthys use sophisticated techniques including trigonometric calculations for execution delays (evading sandbox timeouts), heavy API call obfuscation, and dynamic C2 resolution via DNS-over-HTTPS or blockchain-based dead drops.

**Data Targeting**: Beyond traditional browser credentials and cookies, modern stealers target: cryptocurrency wallet extensions and desktop wallets, 2FA authenticator app databases, VPN client credentials (corporate targets), email client data, Discord/Telegram session tokens, gaming platform credentials (Steam, Epic), and increasingly files matching patterns (documents, PDFs, private keys).

**Cookie/Session Theft**: Session cookie theft has become as valuable as credential theft, enabling authentication bypass that circumvents MFA entirely. Chrome's App-Bound Encryption (introduced 2024) attempted to protect cookies, but stealer developers developed bypasses within weeks, highlighting the arms race between browser security and stealer development.

**Log Processing and Sale**: Stolen data is processed through automated panels that parse, categorize, and extract high-value items. Logs are tagged by country, affected services (banking, social media, corporate), and data completeness. Automated filtering for corporate VPN credentials (Cisco AnyConnect, Fortinet, Pulse Secure) feeds the IAB pipeline.

## Ecosystem & Infrastructure Patterns

**MaaS Business Model**: Infostealer developers operate subscription-based services with tiered pricing. Higher tiers may include features like log parsing tools, dedicated support, custom builds, and access to private Telegram channels with updates. Developers invest in marketing on cybercrime forums, often providing test builds and comparison demonstrations against competitors.

**Log Market Pipeline**: Stolen logs flow through a multi-stage pipeline: stealer deployment → log collection at C2 panel → automated parsing and categorization → listing on marketplaces (Russian Market, Telegram channels, 2easy) or private buyer arrangements → purchase by IABs, fraudsters, or direct operators → exploitation for account takeover, fraud, or network intrusion.

**Russian Market Dominance**: Following the Genesis Market takedown, Russian Market consolidated its position as the leading log marketplace. It offers search by URL (finding credentials for specific services), geographic filtering, and stealer family filtering. The marketplace maintains automated listing from multiple stealer operators.

**Infostealer-to-Ransomware Pipeline**: The operational chain from infostealer infection to ransomware deployment is well-documented: (1) Employee machine infected with infostealer via malvertising, (2) Corporate VPN/SSO credentials stolen, (3) Credentials appear on log markets, (4) IAB purchases and validates access, (5) IAB sells access on forums (Exploit, XSS, RAMP), (6) Ransomware affiliate purchases access and deploys ransomware. This chain can span weeks to months.

## Tooling

| Tool/Platform | Category | Usage |
|--------------|----------|-------|
| Russian Market | Log Marketplace | Dominant marketplace for purchasing individual infostealer logs |
| 2easy | Log Marketplace | Secondary marketplace for bot/log trading |
| Telegram channels | Distribution/Sales | Bulk log sales, stealer subscriptions, and customer support |
| Google Ads | Distribution Vector | Malvertising campaigns directing to fake download sites |
| Pay-per-install (PPI) services | Distribution | PrivateLoader, SmokeLoader distribute stealers via bundled installs |
| Raccoon/Lumma/Vidar panels | C2 Management | Web-based panels for managing infections and extracting logs |
| CloudFlare Workers | Infrastructure | Used as C2 proxying layer to obscure real infrastructure |
| Discord webhooks | Exfiltration | Used by some stealers to exfiltrate data via Discord |
| Crypters/packers | Evasion | Commercial crypter services used to evade AV detection |
| Fake CAPTCHA kits | Distribution | "Verify you're human" pages that trick users into running malicious commands |

## Intelligence Gaps

- **Corporate impact quantification**: The total number of corporate breaches and ransomware incidents directly attributable to infostealer-harvested credentials is not well-quantified, though anecdotal evidence suggests it is substantial.
- **Log market volumes**: Total volume and revenue of log marketplaces is estimated but not precisely measured; many transactions occur in private channels.
- **Chrome cookie encryption effectiveness**: The ongoing arms race between browser cookie protection and stealer bypass techniques creates rapidly shifting intelligence that is difficult to keep current.
- **macOS stealer prevalence**: The actual infection rates and impact of macOS-targeted stealers are less well-studied compared to Windows stealers due to lower telemetry and research focus.
- **Mobile infostealer convergence**: The overlap between traditional desktop infostealers and mobile banking trojans (which also steal credentials) is not well-mapped as the ecosystems converge.

## Sources & References

1. Dutch National Police - "Operation Magnus: RedLine and META Stealer Disruption" (October 2024) — https://www.politie.nl/
2. FBI/Europol - "Operation Cookie Monster: Genesis Market Takedown" (April 2023) — https://www.fbi.gov/
3. Sekoia - "Infostealer Landscape" threat reports — https://blog.sekoia.io/
4. Recorded Future - "Infostealer Marketplace Intelligence" — https://www.recordedfuture.com/
5. KELA - "Infostealer-to-Ransomware Connection Analysis" — https://www.kelacyber.com/
6. Flare - "Infostealer Log Market Analysis" — https://flare.io/
7. Google Threat Analysis Group - "Malvertising Campaign Disruptions" — https://blog.google/threat-analysis-group/
8. Trend Micro - "Infostealer Family Tracking Reports" — https://www.trendmicro.com/vinfo/us/security/research-and-analysis/

## Change Log

| Date | Change | Source |
|------|--------|--------|
| 2026-04-05 | Initial creation with baseline intelligence through early 2025 | Training knowledge |
