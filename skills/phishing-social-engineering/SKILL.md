---
name: phishing-social-engineering
description: Use when the user asks about phishing campaigns, social-engineering techniques, BEC (business email compromise), pretexting, AiTM (adversary-in-the-middle) kits, or specific phishing-kit families. Self-updating knowledge cell.
user-invocable: true
metadata:
  category: knowledge-cell
  created: 2026-04-05
  last_updated: 2026-09-29
  update_count: 1
  confidence: moderate
---

# Phishing & Social Engineering

## Executive Summary

Phishing and social engineering remain among the most common initial access vectors across both cybercriminal and state-sponsored operations. Microsoft's 2025 Digital Defense Report attributes 28% of the breaches its incident responders investigated to phishing or social engineering [39]. The defining change since 2024 is that attackers increasingly avoid stealing a password at all. Three techniques now sit alongside Adversary-in-the-Middle (AitM) session theft: device code phishing, where the victim authorizes an attacker's device on the genuine Microsoft sign-in page; ClickFix, where a fake CAPTCHA or error page talks the victim into pasting and running a command; and voice phishing, where a caller posing as the IT help desk walks an employee through handing over access. All three defeat non-phishing-resistant MFA, and the consistent vendor recommendation is FIDO2/passkey authentication, restriction of the device code flow, and managed-device requirements.

The Phishing-as-a-Service (PhaaS) market was the target of four major disruptions in twelve months: RaccoonO365 (September 2025), Tycoon 2FA (March 2026), the China-based Outsider kit (June 2026) and EvilTokens (September 2026) [10][17][19][34]. Results were mixed. Tycoon 2FA, which Microsoft says accounted for about 62% of the phishing attempts it blocked by mid-2025, lost 330 domains but was back at pre-disruption volume within days according to CrowdStrike, and by late April 2026 had added device code phishing [10][11][13]. Outsider affiliates stood up more than 700 new phishing pages in the month after the takedown [33]. EvilTokens, launched in February 2026, turned device code phishing into a commodity and bundled an AI assistant that triaged stolen mailboxes for payment fraud; its disruption was accompanied by two arrests in the UK, and it is too early to judge whether it holds [18][19]. Subscription prices observed in 2025-2026 range from $289 per month (Greatness) to a $1,500 entry fee plus $500 per month (EvilTokens) [19][23].

Business Email Compromise (BEC) remains the second most costly crime type reported to the FBI IC3, behind investment fraud: $3.05 billion in reported losses from 24,768 complaints in 2025, up from $2.77 billion in 2024 [9]. Voice-led extortion crews (UNC6040, UNC6671 and clusters using the ShinyHunters name) have made help-desk impersonation a routine route into Salesforce, Microsoft 365 and Okta tenants [28][29][30]. Law enforcement pressure on Scattered Spider has been substantial, with two members sentenced in the UK in July 2026 [36]. AI use is now documented in kit features and lure production, but measured losses attributed to AI remain a small share of the total [9].

## Key Actors

| Actor/Platform | Type | Notable Characteristics | Status |
|---------------|------|------------------------|--------|
| Tycoon 2FA | PhaaS Platform | AitM kit first seen August 2023; about 2,000 users at takedown (TrendAI); targets Microsoft 365 and Google Workspace; added device code phishing April 2026 | Active. Disrupted 4 March 2026 (330 domains seized), rebuilt within weeks [10][11][12][13][16] |
| EvilTokens (Storm-2992) | PhaaS Platform | Device code phishing kit sold on Telegram from February 2026; AI assistant for mailbox triage and BEC targeting; linked by Microsoft to 12,000+ inboxes in 10,000+ organizations | Disrupted 22 September 2026; two arrests in UK on 11 September; durability unknown [18][19] |
| Greatness | PhaaS Platform | Now supports AitM, device code phishing and OAuth consent abuse; targets M365, iCloud, Yahoo, Google Workspace; $289/month | Active as of August 2026 [23] |
| Kali365 | PhaaS Platform | Device code phishing kit distributed via Telegram, first seen April 2026; AI-generated lures; subject of an FBI PSA | Active as of May 2026 [22] |
| RaccoonO365 (Storm-2246) | PhaaS Platform | Microsoft 365 credential kit; 850+ Telegram members; at least 5,000 credentials stolen across 94 countries | Disrupted September 2025 (338 domains seized); current status not confirmed [17] |
| Outsider Phishing Kit | PhaaS Platform | China-based smishing kit with AitM capability; 267+ templates; 230+ affiliates before takedown (Group-IB) | Disrupted June 2026 (Operation Ghost Hook); affiliates still active [33][34] |
| EvilProxy | PhaaS Platform | AitM phishing service targeting M365, Google and others | Reported by Barracuda as gaining share after the Tycoon 2FA disruption; not independently re-verified [15] |
| Evilginx | Open-Source Tool | Open-source AitM framework by Kuba Gretzky | Active (tool) |
| UNC6040 / UNC6240 | Cybercrime (extortion) | Vishing as IT support to get a malicious connected app authorized in Salesforce; extortion follows months later under the ShinyHunters name | Active [28] |
| UNC6671 (BlackFile; Storm-3032) | Cybercrime (extortion) | Vishing to personal mobiles with passkey or MFA enrollment pretext, then AitM against M365 and Okta; rebranded as REDACT, FALCON, HELIX, PINK | Active [29][30][31] |
| Scattered Spider | Cybercrime Collective | Help-desk vishing, SIM swapping, SMS phishing; young Western actors | Degraded. Two members jailed in UK July 2026; NCA says the action "effectively halted" the group, though others may reuse the name [35][36] |
| Muddled Libra | Cybercrime | Overlaps with Scattered Spider; targets BPO/telecom for downstream access | Not re-verified in this refresh |
| Storm-1167 | Cybercrime (AitM/BEC) | Developed and operated an AitM kit used in a multi-stage AitM and BEC campaign documented by Microsoft in 2023 | Not re-verified in this refresh [37] |
| Star Blizzard (formerly SEABORGIUM) | State-Sponsored (Russia) | Spearphishing of government, diplomatic, policy and Ukraine-support targets; shifted to WhatsApp QR-code account linking | See russia-cyber-espionage cell [38] |
| Storm-2372 | Suspected State-Aligned (Russia) | Device code phishing via WhatsApp, Signal and fake Teams invites since August 2024; Microsoft attribution at moderate confidence | See russia-cyber-espionage cell [24] |
| Midnight Blizzard (APT29) | State-Sponsored (Russia) | Teams phishing, token theft; targeted Microsoft itself | See russia-cyber-espionage cell |
| Kimsuky (APT43) | State-Sponsored (DPRK) | Credential harvesting targeting Korea experts, think tanks, journalists | See dprk-cyber-espionage cell |
| Various BEC Networks | Organized Fraud | West African and Eastern European BEC operations | Active |

## Current Activity

### Device Code Phishing Goes Mainstream (2026)
Device code phishing abuses the OAuth device authorization flow: the victim enters an attacker-generated code on the legitimate Microsoft sign-in page and completes their own MFA, and the attacker receives access and refresh tokens. No password is captured and no fake login page is needed. The technique was used by the suspected Russia-aligned actor Storm-2372 from August 2024 [24], then commoditized when EvilTokens launched on Telegram in mid-February 2026. Huntress tied a campaign against 344 organizations between 2 and 19 March 2026 to EvilTokens [20]. Push Security reported a 37.5x increase in device code phishing pages detected during 2026 and tracked more than a dozen kits, with EvilTokens the most prevalent [21]. The FBI issued a PSA on the Kali365 kit on 21 May 2026 [22]. Tycoon 2FA and Greatness have both added the technique [13][23]. After access, operators register a device to obtain a Primary Refresh Token, create inbox rules to hide their activity, and enumerate the tenant through Microsoft Graph [18]. Elastic notes that device-bound tokens survive ordinary session revocation, so registered devices must be removed during containment [14].

### PhaaS Disruption and Rapid Recovery
Microsoft's Digital Crimes Unit, with Europol and industry partners, seized 330 Tycoon 2FA domains on 4 March 2026 under a US court order, with law enforcement measures in Latvia, Lithuania, Portugal, Poland, Spain and the UK [10]. CrowdStrike observed volume fall to 25% of pre-disruption levels on 4 and 5 March, then return to early-2026 levels, with "no material decline" in cloud account compromises [11]. Abnormal documented a rebuilt deployment on new infrastructure within weeks [12]. Barracuda's assessment is that the Tycoon 2FA brand declined while its techniques spread across other kits, including Mamba 2FA, EvilProxy, Sneaky 2FA and Whisper 2FA [15]. The Outsider takedown in June 2026 followed the same pattern [33]. The EvilTokens action differs in that it was accompanied by arrests: two men aged 32 and 38 were arrested by the Metropolitan Police on 11 September 2026 and released on bail [19].

### ClickFix and Fake-CAPTCHA Lures
ClickFix pages present a fake human-verification check, browser error or meeting fault, and instruct the visitor to paste a command into the Windows Run dialog, PowerShell or the macOS Terminal. Microsoft reported in August 2025 that campaigns target thousands of enterprise and consumer devices daily, delivered through phishing email, malvertising and compromised websites, with Lumma Stealer the most prolific payload alongside remote access tools and loaders [25]. ClickFix builders are sold on criminal forums; Microsoft cited $200 to $1,500 per month, ReversingLabs $250 per month to $1,800 for a lifetime license [25][27]. Variants named by ReversingLabs include FileFix (File Explorer address bar), CrashFix, PromptFix and ConsentFix (OAuth consent) [27]. A macOS campaign documented by Microsoft in August 2026 delivered MacSync and Atomic Stealer through more than 250 front-end domains and used server-side fingerprinting to hide lures from researchers [26].

### Help-Desk and Voice Social Engineering
Google's Threat Intelligence Group (GTIG) reported in June 2025 that UNC6040 operators phone employees posing as IT support and guide them to authorize a modified Salesforce Data Loader as a connected app, giving API access for bulk data theft; extortion follows, sometimes months later, from a cluster tracked as UNC6240 that claims to be ShinyHunters. Google disclosed that one of its own Salesforce instances was affected [28]. UNC6671, first operating as BlackFile in early 2026, calls employees on personal mobiles with a passkey or MFA enrollment pretext, directs them to a victim-specific subdomain on an AitM page, registers its own MFA device, and exfiltrates SharePoint, OneDrive and Salesforce data with scripts [29]. GTIG traced 141.65 BTC (about $10.7 million) to BlackFile wallets between January and May 2026, and the group has since narrowed its targeting to financial and legal firms [30]. Microsoft tracks related activity as Storm-3121 and Storm-3032 and notes the use of both AitM and device code flows [31].

### AI-Enhanced Social Engineering
AI is now a marketed kit feature. EvilTokens offered preset prompts to summarize and translate stolen mail, find wire-transfer threads and identify who controls payments; Microsoft called it its first action against an end-to-end AI-enabled cybercrime service [19]. Kali365 advertises AI-generated lures [22]. Microsoft reported a BEC campaign of more than one million emails on 3-5 August 2026 impersonating executives with fabricated ServiceNow invoices, noting indicators consistent with AI-assisted template development but stating these do not establish how much content was AI-generated [32]. IC3 recorded 22,364 complaints with an AI element in 2025 and $893 million in losses, of which $632 million was investment fraud and $30 million was BEC [9].

### QR Code Phishing ("Quishing")
QR codes in emails and PDFs continue to move victims onto mobile devices that lack corporate filtering. Star Blizzard used a QR code in early 2025 to trick targets into linking the attacker's device to their WhatsApp account, which Microsoft described as the first observed change to that actor's long-standing tradecraft [38].

## Historical Events

| Date | Event | Impact |
|------|-------|--------|
| 2020 | SolarWinds campaign included spearphishing | State-sponsored phishing as one vector in major supply chain operation |
| 2021 | Microsoft warns of consent phishing campaigns | OAuth app abuse for persistent mailbox access without credentials |
| Sep 2022 | Uber breach via MFA fatigue | Scattered Spider-linked actor bombarded employee with MFA pushes; gained access |
| Jan 2023 | Reddit employee phished | Sophisticated targeted phishing led to internal system access |
| Aug 2023 | Microsoft Storm-0558 token theft | Stolen MSA signing key enabled forging Azure AD tokens for government email |
| Late 2023 | QR code phishing surge begins | Major increase in quishing campaigns targeting corporate users |
| Jan 2024 | Midnight Blizzard phishes Microsoft | Russian APT compromised Microsoft corporate email via password spray then OAuth abuse |
| 2024 | $25M deepfake video call BEC (Hong Kong) | Finance employee tricked by deepfake video call impersonating CFO and colleagues |
| 2024 | EvilProxy campaigns hit thousands of orgs | Mass AitM phishing campaigns compromise M365 accounts at scale |
| Aug 2024 | Transport for London intrusion | Scattered Spider members later convicted; about £29 million in costs [35][36] |
| 2024-2025 | Callback phishing (BazarCall variants) | Phone-based social engineering directing victims to install remote access tools |
| Feb 2025 | Microsoft exposes Storm-2372 | First large documented device code phishing campaign, active since August 2024 [24] |
| Jun 2025 | GTIG exposes UNC6040 | Vishing-led Salesforce data theft and extortion; Google itself affected (disclosed August 2025) [28] |
| Aug 2025 | Noah Urban sentenced (US) | Scattered Spider member sentenced to 10 years, $13 million restitution [35] |
| Sep 2025 | RaccoonO365 disrupted | Microsoft and Cloudflare seize 338 domains; Microsoft names alleged leader and makes criminal referral [17] |
| Feb 2026 | EvilTokens launches | First criminal PhaaS kit for device code phishing [18][21] |
| 4 Mar 2026 | Tycoon 2FA disrupted | 330 domains seized; activity back to prior levels within days [10][11] |
| Jun 2026 | Operation Ghost Hook | FBI, Google and Lumen act against Outsider kit; $1.9 billion estimated losses; no arrests reported [34] |
| Jul 2026 | Scattered Spider sentencing (UK) | Thalha Jubair and Owen Flowers each sentenced to five and a half years [36] |
| Sep 2026 | EvilTokens disrupted | 50 websites seized, 150+ domains disabled, two arrests in UK [19] |

## TTP Evolution

**Email Delivery**: Attackers have shifted from bulk commodity spam to abusing compromised legitimate accounts, legitimate email marketing platforms (SendGrid, Mailchimp), and trusted cloud services (SharePoint file shares, OneNote pages, Google Forms) as delivery mechanisms. In 2026 campaigns, links were wrapped in email security vendors' own URL rewriters and click-tracking services, and landing pages were hosted on Cloudflare Workers, Vercel and similar platforms [13][20]. HTML smuggling is used to evade gateway scanning.

**MFA Bypass**: The progression runs from credential theft → MFA fatigue/push bombing → AitM session hijacking → device code and OAuth consent phishing. AitM and device code phishing now coexist inside the same kits [13][23]. Device code phishing has the advantage for the attacker that the victim only ever interacts with genuine Microsoft pages, and the resulting sign-in resembles normal application activity [13]. Attackers then register their own MFA method or device for persistence [18][29].

**User-Executed Commands**: ClickFix moves the execution step to the user, bypassing attachment and download controls. Variants target File Explorer, the macOS Terminal and OAuth consent screens [25][26][27]. Apple added a paste warning in macOS 26.4 [26].

**Landing Page Sophistication**: Modern phishing pages employ CAPTCHA challenges (Cloudflare Turnstile), fingerprint checks, geofencing, user-agent validation and IP reputation checks. eSentire found a Tycoon 2FA variant blocking more than 230 security vendors and analysis tools [13]. Server-side visitor qualification before the lure is shown is now seen in ClickFix infrastructure as well [26].

**Brand Impersonation**: Microsoft is the most heavily targeted platform for device code and AitM phishing, with Google, Salesforce, GitHub and AWS also targeted [21]. DocuSign, SharePoint, voicemail notification, construction bid and payroll lures are recurring themes [20].

**Vishing and Hybrid Attacks**: Callback phishing (BazarCall variants) directs victims to call a number and install remote access software. The 2025-2026 pattern is outbound calling: operators phone employees, often on personal mobiles, impersonate the help desk, and direct them to an AitM page or a connected-app authorization. Passkey and MFA enrollment is the current pretext of choice [29][30][31].

## Ecosystem & Infrastructure Patterns

**PhaaS Market Structure**: The PhaaS market mirrors other -as-a-service models with subscription tiers, admin panels, real-time credential viewers and add-on products. Telegram is the standard sales and support channel [17][19][22][23]. Market share figures depend on the vantage point: Microsoft put Tycoon 2FA at about 62% of the phishing it blocked by mid-2025, while Barracuda put it at 89% of the PhaaS activity it observed a year before April 2026 [10][15]. These measure different things and should not be compared directly.

**Takedown Resilience**: Domain seizures without arrests have produced short interruptions. Kits carry stable code fingerprints across rebuilds, which vendors recommend as a more durable detection basis than domains [12][13]. Barracuda advises building detection around techniques because kit-specific detection ages quickly [15].

**Infrastructure**: Phishing campaigns increasingly use legitimate cloud and platform-as-a-service hosting to benefit from trusted domains and certificates [20]. Vishing crews register generic root domains and reuse them with victim-named subdomains [29][30]. Domains also use typosquatting, homograph attacks and long subdomains. URL shorteners and open redirects obscure final destinations.

**Post-Compromise Actions**: After obtaining tokens, operators register devices or MFA methods, create inbox rules, enumerate the tenant via Microsoft Graph, and harvest mail and files [18][31]. Extortion crews exfiltrate SharePoint and OneDrive content with scripts, sometimes streaming files so that logs show access events rather than downloads [29]. For BEC, actors look for live payment threads and vendor invoices to alter; EvilTokens automated that search [19].

**BEC Ecosystem**: BEC operations involve role specialization: phishers who compromise accounts, operators who monitor email for financial opportunities, money mule managers, and sometimes document forgers. IC3 reports that 86% of BEC losses in 2025 moved by wire transfer or ACH [9]. The FBI estimates BEC has caused over $50 billion in global losses since 2013.

## Tooling

| Tool/Platform | Category | Usage |
|--------------|----------|-------|
| Evilginx | AitM Framework | Open-source reverse proxy for AitM phishing |
| EvilProxy | PhaaS Service | Commercial AitM platform targeting M365, Google Workspace, etc. |
| Tycoon 2FA | PhaaS Service | AitM kit with anti-analysis; device code phishing added April 2026 [13] |
| EvilTokens | PhaaS Service | Device code phishing kit with AI mailbox analysis; disrupted September 2026 [19] |
| Kali365 | PhaaS Service | Device code phishing kit with AI-generated lures [22] |
| Greatness | PhaaS Service | AitM, device code and OAuth consent phishing [23] |
| Outsider Phishing Kit | PhaaS Service | Smishing kit with AitM capture of SMS, PIN, email and app verification [33][34] |
| ClickFix builders | Lure Kit | Configurable fake CAPTCHA and error pages sold on forums [25][27] |
| Modified Salesforce Data Loader | Connected App Abuse | Authorized by victim during vishing call to enable bulk data export [28] |
| GoPhish | Phishing Framework | Open-source phishing simulation (used by both red teams and criminals) |
| Modlishka | AitM Tool | Open-source AitM reverse proxy |
| SET (Social-Engineer Toolkit) | Framework | Credential harvesting and social engineering automation |
| Cloudflare Turnstile | Anti-Analysis | CAPTCHA service used on phishing pages to block automated scanning |
| HTML Smuggling techniques | Delivery | Embedding encoded payloads in HTML to bypass email gateways |
| Voice cloning AI | Vishing | AI-generated voice for impersonation calls |
| Residential and datacenter proxies | Infrastructure | Used to access compromised accounts from plausible locations [14] |

## Intelligence Gaps

- **Durability of the EvilTokens disruption**: The action is one week old at the time of writing. Whether the service or a successor returns is unknown.
- **Tycoon 2FA operators**: Microsoft named an alleged developer believed to be in Pakistan [10]. No arrest of Tycoon 2FA operators was confirmed in the sources reviewed.
- **EvilProxy, Mamba 2FA, Sneaky 2FA, Whisper 2FA**: Named by Barracuda as gaining share in 2026 [15], but no dedicated primary reporting on their current scale was reviewed in this refresh.
- **RaccoonO365 after September 2025**: Whether the service resumed, and the outcome of Microsoft's criminal referral, were not confirmed.
- **Scattered Spider residual activity**: The NCA states its action halted the group [36]. Attribution of 2025 UK retail intrusions and any continuing activity under the name were not confirmed in this refresh.
- **Unconfirmed statistics**: Widely repeated figures that ClickFix accounted for 47% of initial access in Microsoft Defender Experts notifications, and that AI-written phishing achieved a 54% click-through rate, could not be located in the primary material opened for this refresh and are not relied on here.
- **AI share of phishing**: IC3's AI-related figures rest on complainants recognizing and reporting AI use, and IC3 itself notes that many victims do not realize AI was involved [9].
- **Voice deepfake prevalence**: Most successful vishing attacks are never forensically analyzed for AI use.
- **Quishing scale and impact**: QR scans on personal mobile devices bypass most corporate telemetry.
- **PhaaS platform revenue**: Disclosed figures are partial (for example at least $100,000 for RaccoonO365 [17]); total market revenue is not publicly known.

## Sources & References

1. FBI Internet Crime Complaint Center (IC3) - "2023 Internet Crime Report" — https://www.ic3.gov/
2. Microsoft - "Digital Defense Report 2024" — https://www.microsoft.com/en-us/security/security-insider/
3. Proofpoint - "State of the Phish 2024" — https://www.proofpoint.com/us/resources/threat-reports/state-of-phish
4. Kuba Gretzky - "Evilginx" project and research — https://breakdev.org/evilginx/
5. Mandiant - "Phishing and AitM Campaign Analysis" — https://www.mandiant.com/resources
6. Cisco Talos - "Phishing Trends and Techniques Research" — https://blog.talosintelligence.com/
7. KnowBe4 - "Phishing Benchmarking Reports" — https://www.knowbe4.com/
8. Sekoia - "Tycoon 2FA and PhaaS Landscape Analysis" — https://blog.sekoia.io/
9. FBI Internet Crime Complaint Center (IC3) - "Internet Crime Report 2025" (2026) — https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf
10. Microsoft On the Issues - "Defending the gates: How a global coalition disrupted Tycoon 2FA" (2026-03-04) — https://blogs.microsoft.com/on-the-issues/2026/03/04/how-a-global-coalition-disrupted-tycoon/
11. CrowdStrike - "Tycoon2FA Phishing-as-a-Service Platform Persists After Takedown" (2026-03-20) — https://www.crowdstrike.com/en-us/blog/tycoon2fa-phishing-as-a-service-platform-persists-following-takedown/
12. Abnormal AI - "Tycoon2FA Rebounds Post-Takedown with 6 Layers of Obfuscation" (2026-05-06) — https://abnormal.ai/blog/tycoon2fa-post-takedown-rebuild
13. eSentire - "Tycoon 2FA Operators Adopt OAuth Device Code Phishing" (2026-05-12) — https://www.esentire.com/blog/tycoon-2fa-operators-adopt-oauth-device-code-phishing
14. Elastic Security Labs - "Detecting Tycoon 2FA AiTM attacks across Entra ID and Google Workspace" (2026-05-26) — https://www.elastic.co/security-labs/tycoon-2fa-aitm-detection-engineering
15. Barracuda - "Threat Spotlight: Tycoon 2FA didn't die — it's scattered everywhere" (2026-04-16, updated 2026-09-03) — https://blog.barracuda.com/2026/04/16/threat-spotlight-tycoon-2fa-scattered-everywhere
16. TrendAI - "Europol, Microsoft, TrendAI, and Collaborators Halt Tycoon 2FA Operations" (March 2026) — https://www.trendaisecurity.com/en-us/resources-insights/trendai-security-blog/tycoon2fa-takedown
17. Microsoft On the Issues - "Microsoft seizes 338 websites to disrupt rapidly growing 'RaccoonO365' phishing service" (2025-09-16) — https://blogs.microsoft.com/on-the-issues/2025/09/16/microsoft-seizes-338-websites-to-disrupt-rapidly-growing-raccoono365-phishing-service/
18. Microsoft Security Blog - "Unmasking EvilTokens: Getting to the root of device code phishing" (2026-09-22) — https://www.microsoft.com/en-us/security/blog/2026/09/22/unmasking-eviltokens-getting-to-the-root-of-device-code-phishing/
19. Microsoft On the Issues - "Disrupting EvilTokens: The AI Chatbot Built for Cybercrime" (2026-09-22) — https://blogs.microsoft.com/on-the-issues/2026/09/22/disrupting-eviltokens-the-ai-chatbot-built-for-cybercrime/
20. Huntress - "Railway PaaS M365 token replay campaign" (2026-03-20, updated 2026-03-23) — https://www.huntress.com/blog/railway-paas-m365-token-replay-campaign
21. Push Security - "Analyzing the rise in device code phishing attacks in 2026" (2026-04-04, updated 2026-05-15) — https://pushsecurity.com/blog/device-code-phishing
22. FBI IC3 - "Kali365 Phishing-as-a-Service Kit Hijacks Microsoft 365 Access Tokens" PSA (2026-05-21) — https://www.ic3.gov/PSA/2026/PSA260521
23. ZeroBEC - "Greatness PhaaS: AiTM and device code phishing" (2026-08-04) — https://zerobec.com/blog/greatness-phaas-aitm-and-device-code-phishing
24. Microsoft Security Blog - "Storm-2372 conducts device code phishing campaign" (2025-02-13) — https://www.microsoft.com/en-us/security/blog/2025/02/13/storm-2372-conducts-device-code-phishing-campaign/
25. Microsoft Security Blog - "Think before you Click(Fix): Analyzing the ClickFix social engineering technique" (2025-08-21) — https://www.microsoft.com/en-us/security/blog/2025/08/21/think-before-you-clickfix-analyzing-the-clickfix-social-engineering-technique/
26. Microsoft Security Blog - "From open lures to cloaked gates: How a macOS ClickFix campaign learned to hide" (2026-08-05) — https://www.microsoft.com/en-us/security/blog/2026/08/05/macos-clickfix-campaign-learned-hide/
27. Help Net Security - "ClickFix is changing the economics of social engineering" (reporting ReversingLabs research) (2026-07-15) — https://www.helpnetsecurity.com/2026/07/15/clickfix-social-engineering-attacks-report/
28. Google Threat Intelligence Group - "The Cost of a Call: From Voice Phishing to Data Extortion" (2025-06-05, updated 2025-08-08) — https://cloud.google.com/blog/topics/threat-intelligence/voice-phishing-data-extortion
29. Google Threat Intelligence Group - "Welcome to BlackFile: Inside a Vishing Extortion Operation" (May 2026) — https://cloud.google.com/blog/topics/threat-intelligence/blackfile-vishing-extortion-operation/
30. Google Threat Intelligence Group - "UNC6671 Rebrands: Multi-Brand Vishing Extortion Targets Financial Services and Enterprise Cloud Environments" (August 2026) — https://cloud.google.com/blog/topics/threat-intelligence/unc6671-targets-financial-services-and-enterprise-cloud-environments/
31. Microsoft Security Blog - "Passkey-themed social engineering leads to identity and cloud compromise" (2026-09-09) — https://www.microsoft.com/en-us/security/blog/2026/09/09/passkey-themed-social-engineering-leads-identity-cloud-compromise/
32. Microsoft Security Blog - "Protecting organizations from AI-assisted executive impersonation and invoice fraud" (2026-09-10) — https://www.microsoft.com/en-us/security/blog/2026/09/10/protecting-organizations-ai-assisted-executive-impersonation-invoice-fraud/
33. Group-IB - "The Outsider Phishing Kit: A Resilient Threat in the Face of Law Enforcement Action" (2026-09-03) — https://www.group-ib.com/blog/chenlun-outsider-phaas-kit/
34. CyberScoop - "FBI takes down massive China-based cybercrime network that caused $1.9B in losses" (June 2026) — https://cyberscoop.com/outsider-cybercrime-network-takedown-china-fbi-google-lumen/
35. Krebs on Security - "Scattered Spider Hackers Plead Guilty on Day 1 of Trial" (June 2026) — https://krebsonsecurity.com/2026/06/scattered-spider-hackers-plead-guilty-on-day-1-of-trial/
36. SecurityWeek - "Two Scattered Spider Hackers Sentenced to Jail in UK" (July 2026) — https://www.securityweek.com/two-scattered-spider-hackers-sentenced-to-jail-in-uk/
37. Microsoft Security Blog - "Detecting and mitigating a multi-stage AiTM phishing and BEC campaign" (2023-06-08) — https://www.microsoft.com/en-us/security/blog/2023/06/08/detecting-and-mitigating-a-multi-stage-aitm-phishing-and-bec-campaign/
38. Microsoft Security Blog - "New Star Blizzard spear-phishing campaign targets WhatsApp accounts" (2025-01-16) — https://www.microsoft.com/en-us/security/blog/2025/01/16/new-star-blizzard-spear-phishing-campaign-targets-whatsapp-accounts/
39. Microsoft - "Microsoft Digital Defense Report 2025" — https://www.microsoft.com/en-us/security/security-insider/threat-landscape/microsoft-digital-defense-report-2025

## Change Log

| Date | Change | Source |
|------|--------|--------|
| 2026-04-05 | Initial creation with baseline intelligence through early 2025 | Training knowledge |
| 2026-09-29 | Rewrote Executive Summary and Current Activity for 2025-2026: device code phishing, ClickFix, vishing-led extortion, PhaaS takedowns (RaccoonO365, Tycoon 2FA, Outsider, EvilTokens). Corrected kit status, BEC ranking and IC3 figures, and the Storm-1167/Star Blizzard conflation. Added 31 sources. | OSINT refresh |
