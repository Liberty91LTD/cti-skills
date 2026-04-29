---
name: phishing-social-engineering
description: Use when the user asks about phishing campaigns, social-engineering techniques, BEC (business email compromise), pretexting, AiTM (adversary-in-the-middle) kits, or specific phishing-kit families. Self-updating knowledge cell.
user-invocable: true
metadata:
  category: knowledge-cell
  created: 2026-04-05
  last_updated: 2026-04-05
  update_count: 0
  confidence: moderate
---

# Phishing & Social Engineering

## Executive Summary

Phishing and social engineering remain the most common initial access vectors across both cybercriminal and state-sponsored operations. The landscape has undergone significant evolution beyond traditional email-based credential harvesting. Adversary-in-the-Middle (AitM) phishing platforms — notably EvilProxy and Evilginx — now enable real-time interception of credentials AND session tokens, effectively bypassing most forms of multi-factor authentication (MFA). This development has fundamentally altered the threat model for organizations relying on MFA as a primary defense, shifting the security boundary toward phishing-resistant MFA methods such as FIDO2/WebAuthn hardware keys.

The Phishing-as-a-Service (PhaaS) market has matured substantially, with platforms like EvilProxy, Greatness, Tycoon 2FA, and others offering turnkey AitM phishing kits with subscription models, customer support, and real-time dashboards. These services target Microsoft 365 accounts disproportionately, reflecting the platform's dominance in enterprise environments. Pricing ranges from $200-$1,000+ per month depending on features and target capabilities. Meanwhile, Business Email Compromise (BEC) continues to generate the highest financial losses of any cybercrime category according to FBI IC3 data — over $2.9 billion in reported losses in 2023 alone — despite being less technically sophisticated than other threats.

Emerging vectors include QR code phishing ("quishing"), which evades email security gateways by embedding malicious URLs in images; vishing and callback phishing campaigns that move victims to phone conversations to bypass email controls; AI-generated deepfake voice and video for executive impersonation; and consent phishing that abuses OAuth application permissions to gain persistent access to cloud mailboxes. The combination of AI-enhanced content generation (eliminating grammatical tells), sophisticated infrastructure (legitimate cloud hosting, CAPTCHA protection, geofencing), and AitM session hijacking has made modern phishing significantly harder to detect and defend against.

## Key Actors

| Actor/Platform | Type | Notable Characteristics | Status |
|---------------|------|------------------------|--------|
| EvilProxy | PhaaS Platform | Leading AitM phishing service; targets M365, Google, etc.; subscription-based | Active |
| Tycoon 2FA | PhaaS Platform | AitM kit; heavy use of CAPTCHAs and anti-analysis to evade detection | Active |
| Greatness | PhaaS Platform | M365-focused; easy setup; gained popularity 2023-2024 | Active |
| Evilginx | Open-Source Tool | Open-source AitM framework by Kuba Gretzky; basis for many PhaaS platforms | Active (tool) |
| Storm-1167/Star Blizzard | State-Sponsored (Russia) | Sophisticated spearphishing targeting government, academia, think tanks | Active |
| Scattered Spider | Cybercrime Collective | Expert social engineering; vishing help desk staff; SIM swapping; young Western actors | Active |
| Midnight Blizzard (APT29) | State-Sponsored (Russia) | Teams phishing, token theft; targeted Microsoft itself | Active |
| Various BEC Networks | Organized Fraud | West African and Eastern European BEC operations; increasingly use deepfakes | Active |
| Kimsuky (APT43) | State-Sponsored (DPRK) | Prolific credential harvesting targeting Korea experts, think tanks, journalists | Active |
| Muddled Libra | Cybercrime | Overlaps with Scattered Spider; targets BPO/telecom for downstream access | Active |

## Current Activity

### AitM Phishing at Scale (2024-2025)
AitM phishing kits have become the dominant method for compromising enterprise accounts protected by traditional MFA (push notifications, SMS codes, TOTP). Platforms like EvilProxy and Tycoon 2FA operate as reverse proxies, relaying victim interactions to legitimate login pages in real time while capturing both credentials and session cookies. Campaigns routinely target thousands of organizations simultaneously, with phishing emails delivered from compromised legitimate accounts to bypass reputation-based filtering. Session cookies captured via AitM enable immediate account takeover without triggering new-device MFA prompts.

### QR Code Phishing ("Quishing") Surge
Starting in late 2023 and accelerating through 2024-2025, QR code-based phishing has surged. Attackers embed malicious QR codes in phishing emails, PDFs, or even physical media, directing victims to credential harvesting sites on their mobile devices — which typically lack the email security gateway protections and DNS filtering present on corporate laptops. Microsoft, SharePoint, and DocuSign impersonation campaigns using QR codes have been particularly prevalent. The technique exploits the gap between desktop email security and mobile device protection.

### AI-Enhanced Social Engineering
The use of AI-generated content for phishing and social engineering has moved from theoretical to practical. AI voice cloning has been used in vishing attacks impersonating executives to authorize wire transfers (multiple confirmed incidents with losses in the millions). Large language models generate grammatically flawless phishing emails in any language, eliminating traditional detection signals. While large-scale AI-generated phishing campaigns are difficult to distinguish from human-authored ones, the most impactful use has been in targeted BEC and vishing operations.

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
| 2024-2025 | Callback phishing (BazarCall variants) | Phone-based social engineering directing victims to install remote access tools |

## TTP Evolution

**Email Delivery**: Attackers have shifted from bulk commodity spam to abusing compromised legitimate accounts, legitimate email marketing platforms (SendGrid, Mailchimp), and trusted cloud services (SharePoint file shares, OneNote pages, Google Forms) as delivery mechanisms. This approach exploits trust relationships and bypasses domain reputation filtering. HTML smuggling (embedding encoded payloads in HTML attachments) is used to evade gateway scanning.

**MFA Bypass**: The progression from simple credential theft (pre-MFA era) → MFA fatigue/push bombing → AitM session hijacking → device code phishing (OAuth) represents a continuous arms race. AitM phishing currently poses the most scalable threat to non-phishing-resistant MFA. Device code/OAuth phishing targets Azure AD device authorization flows, making the victim authorize a device the attacker controls.

**Landing Page Sophistication**: Modern phishing pages employ CAPTCHA challenges (Cloudflare Turnstile), fingerprint checks, geofencing to block security researchers, user-agent validation, and IP reputation checks. Some pages serve benign content to scanners while displaying phishing content to real victims. Anti-analysis measures include time-delayed page activation and single-use URLs.

**Brand Impersonation**: Microsoft remains the most impersonated brand, followed by Google, Apple, Amazon, and financial institutions. Phishing kits include pixel-perfect reproductions of login pages with dynamic branding (pulling the target organization's logo via Microsoft's brand API). DocuSign, SharePoint, and voicemail notification lures are consistently effective.

**Vishing and Hybrid Attacks**: Callback phishing (initially pioneered by BazarCall/BazaCall) has spawned numerous variants where phishing emails direct victims to call a phone number, where operators social-engineer them into installing remote access software (AnyDesk, ScreenConnect, Quick Assist). Scattered Spider demonstrated the effectiveness of direct vishing to IT help desks to reset MFA and gain corporate access.

## Ecosystem & Infrastructure Patterns

**PhaaS Market Structure**: The PhaaS market mirrors other -as-a-service models with subscription tiers, admin panels, real-time credential viewers, and API integrations. Some platforms offer geo-targeting, A/B testing of lures, and automated session token extraction. Customer support via Telegram is standard. The low barrier to entry (no technical skill required) has expanded the pool of actors conducting sophisticated phishing.

**Infrastructure**: Phishing campaigns increasingly use legitimate cloud hosting (Azure, AWS, Cloudflare Workers, Firebase) to benefit from trusted domains and SSL certificates. Domains often use typosquatting, homograph attacks (using Unicode characters that visually resemble legitimate domains), or long subdomains that push the actual domain off-screen in mobile browsers. URL shorteners and redirectors (including open redirects on legitimate sites) obscure final destination URLs.

**Post-Compromise Actions**: After capturing credentials and session tokens, automated systems immediately begin data harvesting: downloading emails (especially those containing financial data, credentials, or confidential attachments), setting up mail forwarding rules for persistence, and registering new MFA devices. For BEC operations, actors monitor mailboxes for financial transaction threads to insert themselves via reply-chain hijacking.

**BEC Ecosystem**: BEC operations involve role specialization: phishers who compromise accounts, operators who monitor email for financial opportunities, money mule managers who control laundering networks, and sometimes document forgers who create fake invoices. The FBI estimates BEC has caused over $50 billion in global losses since 2013.

## Tooling

| Tool/Platform | Category | Usage |
|--------------|----------|-------|
| Evilginx | AitM Framework | Open-source reverse proxy for AitM phishing; foundation for many PhaaS |
| EvilProxy | PhaaS Service | Commercial AitM platform targeting M365, Google Workspace, etc. |
| Tycoon 2FA | PhaaS Service | AitM kit with advanced anti-detection |
| GoPhish | Phishing Framework | Open-source phishing simulation (used by both red teams and criminals) |
| Modlishka | AitM Tool | Open-source AitM reverse proxy |
| SET (Social-Engineer Toolkit) | Framework | Credential harvesting and social engineering automation |
| Cloudflare Turnstile | Anti-Analysis | CAPTCHA service used on phishing pages to block automated scanning |
| HTML Smuggling techniques | Delivery | Embedding encoded payloads in HTML to bypass email gateways |
| Voice cloning AI (ElevenLabs, etc.) | Vishing | AI-generated voice for executive impersonation calls |
| Residential proxies | Infrastructure | Used to access compromised accounts from victim's geographic region |

## Intelligence Gaps

- **AI phishing detection**: The ability to reliably distinguish AI-generated phishing from human-authored content remains limited, and the detection challenge will grow as models improve.
- **Quishing scale and impact**: The true volume and success rate of QR code phishing campaigns is poorly measured since QR scans on personal mobile devices bypass most corporate telemetry.
- **Voice deepfake prevalence**: Confirmed cases of AI voice clone attacks are likely the tip of the iceberg; most successful vishing attacks are never forensically analyzed for AI use.
- **AitM session token longevity**: How long stolen session tokens remain valid across different platforms and configurations, and the effectiveness of token revocation policies, is inconsistently documented.
- **PhaaS platform revenue**: The total revenue and customer base of major PhaaS platforms is not publicly known; estimates vary widely.

## Sources & References

1. FBI Internet Crime Complaint Center (IC3) - "2023 Internet Crime Report" — https://www.ic3.gov/
2. Microsoft - "Digital Defense Report 2024" — https://www.microsoft.com/en-us/security/security-insider/
3. Proofpoint - "State of the Phish 2024" — https://www.proofpoint.com/us/resources/threat-reports/state-of-phish
4. Kuba Gretzky - "Evilginx" project and research — https://breakdev.org/evilginx/
5. Mandiant - "Phishing and AitM Campaign Analysis" — https://www.mandiant.com/resources
6. Cisco Talos - "Phishing Trends and Techniques Research" — https://blog.talosintelligence.com/
7. KnowBe4 - "Phishing Benchmarking Reports" — https://www.knowbe4.com/
8. Sekoia - "Tycoon 2FA and PhaaS Landscape Analysis" — https://blog.sekoia.io/

## Change Log

| Date | Change | Source |
|------|--------|--------|
| 2026-04-05 | Initial creation with baseline intelligence through early 2025 | Training knowledge |
