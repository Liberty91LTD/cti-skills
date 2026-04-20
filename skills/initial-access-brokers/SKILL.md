---
name: initial-access-brokers
description: Knowledge cell for initial access brokers. Self-updating intelligence knowledge base.
user-invocable: true
metadata:
  category: knowledge-cell
  created: 2026-04-05
  last_updated: 2026-04-05
  update_count: 0
  confidence: moderate
---

# Initial Access Brokers

## Executive Summary

Initial Access Brokers (IABs) are specialized cybercriminal actors who focus exclusively on gaining unauthorized access to corporate networks and then selling that access to other threat actors — most commonly ransomware affiliates. IABs represent a critical node in the cybercrime supply chain, effectively decoupling the intrusion phase from the monetization phase and enabling a division of labor that increases overall ecosystem efficiency. By purchasing pre-validated network access, ransomware operators and affiliates can skip the time-consuming and technically demanding initial intrusion phase, reducing their time-to-impact from weeks to hours.

The IAB marketplace operates primarily on Russian-language cybercrime forums, with Exploit, XSS, and RAMP being the most active venues. Access listings typically specify the victim's country, industry sector, revenue (a key pricing factor), access type (RDP, VPN, web shell, Active Directory credentials), and level of privilege. Pricing varies dramatically: basic RDP access to a small company might sell for $500-$2,000, while domain admin access to a Fortune 500 company can command $20,000-$50,000 or more. The median price for IAB listings is approximately $1,500-$3,000. Some IABs operate through private channels and maintain exclusive relationships with specific ransomware operations rather than selling on open forums.

The infostealer-to-IAB pipeline has become the dominant supply mechanism for access inventory. IABs systematically purchase or harvest infostealer logs from marketplaces (Russian Market, Telegram channels), filter for corporate VPN credentials (Cisco AnyConnect, Fortinet, Palo Alto GlobalProtect, Pulse Secure/Ivanti), validate access, escalate privileges where possible, and list the access for sale. This pipeline means that an employee's malware infection on a personal device — often via malvertising or a trojanized software download — can directly lead to a ransomware attack on their employer weeks or months later. Separately, IABs exploit vulnerabilities in internet-facing infrastructure (VPN appliances, Citrix, Exchange, firewalls) to harvest access at scale.

## Key Actors

| Actor/Handle | Forum Presence | Notable Characteristics | Status |
|-------------|---------------|------------------------|--------|
| Zebra2104 | Multiple forums | Prolific broker; sold access used by multiple ransomware groups | Active (intermittent) |
| Sang_real (Frapochka) | Exploit, XSS | High-volume listings across sectors; established reputation | Active |
| JETKITTEN | Exploit | Targets education and healthcare | Active |
| Roblette | Exploit, XSS | Specializes in European targets | Active |
| montns | RAMP, Exploit | Significant listing volume; medium-enterprise focus | Active |
| Bostaurus | Exploit | Specializes in access via VPN exploitation | Active |
| Various Telegram-based brokers | Telegram channels | Lower-tier access; often direct from infostealer operators | Active |
| Multiple unattributed IABs | Private channels | Operate exclusively through private deals with ransomware groups | Unknown |

Note: IAB handles change frequently. Actors rebrand, retire, and new actors enter the market regularly. The above represents observed active handles but is not exhaustive.

## Current Activity

### Infostealer Log-to-Access Pipeline Acceleration (2024-2025)
The volume of corporate credentials available via infostealer logs has grown substantially, driven by the proliferation of Lumma, StealC, and other stealer families. IABs have industrialized the process of filtering corporate VPN/SSO credentials from bulk log purchases, validating access, and listing it for sale. Some have developed automated tools to test credentials at scale across VPN endpoints. The time from employee infostealer infection to corporate access listing has compressed, with some operations completing the cycle within days. KELA and Flare research indicates IAB listings have grown year-over-year, with several hundred active listings at any given time.

### Vulnerability Exploitation for Mass Access Harvesting
IABs increasingly exploit critical vulnerabilities in edge devices to build access inventory at scale. Exploited products in 2023-2025 include Citrix NetScaler/ADC (CVE-2023-4966 "Citrix Bleed"), Fortinet FortiOS (multiple CVEs), Ivanti Connect Secure (CVE-2024-21887/CVE-2023-46805), Cisco ASA/FTD, ConnectWise ScreenConnect (CVE-2024-1709), and Palo Alto PAN-OS (CVE-2024-3400). Actors exploit these vulnerabilities to deploy webshells or create accounts across hundreds of organizations, then sell individual accesses as listings. This approach provides inventory at near-zero marginal cost per victim.

### Ransomware-IAB Relationship Tightening
Evidence from ransomware chat leaks (Conti leaks 2022, Black Basta chat leak early 2025) confirms that ransomware operations maintain regular purchasing relationships with IABs, sometimes with standing arrangements for specific types of access (particular sectors, revenue thresholds, geographic regions). Some ransomware programs have dedicated budget lines for access purchases. Premium ransomware affiliates may negotiate exclusive first-look arrangements with top-tier IABs.

## Historical Events

| Date | Event | Impact |
|------|-------|--------|
| 2019-2020 | IAB market formalization | Dedicated access trading sections established on major forums (Exploit, XSS) |
| 2020 | RDP access sales surge during COVID | Remote work expansion massively increased available RDP/VPN attack surface |
| Feb 2022 | Conti leaks expose IAB purchases | Internal chat logs showed Conti's systematic purchase of access from IABs |
| 2022-2023 | RAMP forum gains prominence | Became significant IAB marketplace after its launch, attracting new sellers |
| Late 2023 | Citrix Bleed mass exploitation | CVE-2023-4966 exploited at scale; access to affected orgs appeared on forums within weeks |
| Jan 2024 | Ivanti Connect Secure mass exploitation | Multiple zero-days in VPN appliance exploited for broad access harvesting |
| Early 2025 | Black Basta chat leaks | Confirmed IAB purchasing patterns and pricing for major ransomware operation |
| 2024-2025 | IAB listing volumes increase | Research from KELA, Flashpoint, and Group-IB shows sustained growth in access listings |

## TTP Evolution

**Access Acquisition Methods**:
- *2019-2021*: Predominantly RDP brute-forcing, VPN credential stuffing from data breaches, and exploitation of common vulnerabilities (BlueKeep, Exchange ProxyLogon/ProxyShell).
- *2022-2023*: Shift toward infostealer log harvesting as primary credential source; increasing exploitation of VPN/edge device vulnerabilities.
- *2024-present*: Mature pipeline combining automated infostealer log processing with rapid exploitation of newly disclosed vulnerabilities in edge infrastructure. Some IABs specialize in one method or the other.

**Access Types Sold**:
- *RDP/VPN credentials*: Most common; buyer needs to do their own reconnaissance and privilege escalation.
- *Web shells*: Pre-deployed persistent access; common from vulnerability exploitation campaigns.
- *Domain admin/enterprise admin*: Premium access where IAB has already escalated privileges; commands highest prices.
- *Citrix/Remote Desktop Gateway*: Provides access to virtualized environments with broader reach.
- *Cloud/SaaS access*: Emerging category; M365 Global Admin, AWS root credentials from infostealer logs.
- *MSP/RMM access*: High value due to downstream access to MSP clients; treated as premium listings.

**Pricing Factors**: Access pricing correlates with: victim revenue (strongest factor), access type and privilege level, country (US/EU commands premium), sector (finance/insurance/healthcare premium), network size, and whether security tools were observed. Forum reputation and seller track record also affect willingness to pay. Auction formats are sometimes used for high-value access.

**Operational Security**: Established IABs use forum escrow services to protect both parties. Listings avoid naming victims directly, instead providing country, sector, revenue, number of hosts, and access type. Some use "check" services where potential buyers can verify the access is still valid before completing purchase. Communication for sensitive details moves to encrypted messengers (Tox, Jabber/XMPP).

## Ecosystem & Infrastructure Patterns

**Forum Marketplace Structure**: Major forums (Exploit, XSS, RAMP) have dedicated sections for access trading with established rules, escrow services, and reputation systems. Sellers build reputations through consistent delivery and positive buyer reviews. Some forums require initial deposits or vetting to participate. Listings follow semi-standardized formats specifying access parameters.

**Supply Chain Position**: IABs sit at the critical junction between initial compromise and monetization. Their upstream suppliers include: infostealer operators (providing raw credential logs), vulnerability researchers (providing exploits), and botnet operators (providing infected machine access). Their downstream customers include: ransomware affiliates (primary buyers), corporate espionage operators, data theft groups, and occasionally state-sponsored actors using criminal infrastructure.

**Seasonal and Event-Driven Patterns**: Access listings spike following major vulnerability disclosures in edge devices, as IABs race to exploit and list access before victims patch. Listing volumes also correlate with infostealer campaign waves. New ransomware programs entering the market can create demand spikes as affiliates stock up on access.

**Quality Assurance**: Sophisticated IABs provide "freshness" guarantees — confirming that access is validated within a recent timeframe. Some offer brief replacement guarantees if access becomes invalid shortly after sale. The most professional operations provide detailed information about the victim environment (domain structure, security tools observed, number of hosts) to help buyers assess the opportunity.

**Pricing Benchmarks** (approximate, based on public research):

| Access Type | Typical Price Range | Notes |
|------------|-------------------|-------|
| Basic RDP (single host, SMB) | $500-$2,000 | Most commoditized |
| VPN credentials (enterprise) | $1,000-$5,000 | Varies by company size |
| Domain Admin access | $5,000-$30,000 | Premium; ready for deployment |
| Citrix/RDS Gateway | $2,000-$10,000 | Broader network reach |
| MSP/RMM access | $5,000-$50,000+ | Multiplier effect on downstream clients |
| Fortune 500 / high revenue | $10,000-$50,000+ | Revenue-dependent premium |
| Web shell (large org) | $1,000-$5,000 | Requires further escalation |
| Cloud admin (M365/AWS) | $1,000-$10,000 | Emerging category |

## Tooling

| Tool | Category | Usage |
|------|----------|-------|
| Russian Market / 2easy | Log Sourcing | Purchasing infostealer logs to extract corporate credentials |
| Shodan/Censys | Reconnaissance | Identifying internet-exposed VPN/RDP/Citrix infrastructure |
| Exploit frameworks (Metasploit, custom) | Exploitation | Exploiting vulnerabilities in edge devices |
| Credential testing tools | Validation | Automated testing of harvested credentials against VPN endpoints |
| Brute-force tools (Hydra, custom) | Access | RDP/SSH brute-forcing (declining but still used) |
| Forum escrow services | Transaction | Protected payment for access trades |
| Tox/Jabber/XMPP | Communication | Encrypted messaging for transaction details |
| Cobalt Strike/Sliver | Post-Exploitation | Used by some IABs for privilege escalation before sale |
| BloodHound | AD Enumeration | Mapping Active Directory to assess access value |
| Cryptocurrency (BTC, XMR) | Payment | Primary payment methods for access purchases |

## Intelligence Gaps

- **Private deal volume**: A significant portion of IAB activity occurs through private channels and direct relationships rather than public forum listings. The ratio of public to private access trading is unknown but likely skews heavily toward private, meaning forum monitoring captures only a fraction of activity.
- **Time-to-exploitation**: The average elapsed time from an access listing appearing on forums to a ransomware affiliate purchasing and deploying ransomware is not well-characterized. Faster timelines reduce the defensive window.
- **IAB-ransomware attribution**: Connecting specific ransomware incidents to specific IAB listings/sellers is extremely difficult without insider access, law enforcement data, or ransomware group chat leaks. This limits disruption targeting.
- **Cloud access pricing and volume**: As corporate environments shift to cloud/SaaS, the IAB market for cloud admin access is emerging but not well-studied compared to traditional network access.
- **IAB operator demographics**: Beyond a few arrested individuals, the demographics, geographic distribution, and organizational structure of IAB operators remain largely unknown.
- **Infostealer log to access conversion rate**: What percentage of corporate credentials in infostealer logs are actually viable for network access (not expired, not MFA-blocked, etc.) is poorly quantified.

## Sources & References

1. KELA - "IAB Landscape Reports" and access listing tracking — https://www.kelacyber.com/
2. Flashpoint - "Initial Access Broker Intelligence" — https://flashpoint.io/
3. Group-IB - "Hi-Tech Crime Trends: Initial Access Brokers" — https://www.group-ib.com/
4. CrowdStrike - "Access Broker Tracking and ECrime Index" — https://www.crowdstrike.com/
5. Mandiant - "FIN12 and Access Broker Relationships" — https://www.mandiant.com/resources
6. Secureworks - "Initial Access Broker Marketplace Analysis" — https://www.secureworks.com/
7. Digital Shadows (now ReliaQuest) - "IAB Marketplace Monitoring" — https://www.reliaquest.com/
8. CISA - Known Exploited Vulnerabilities Catalog (edge device CVEs) — https://www.cisa.gov/known-exploited-vulnerabilities-catalog

## Change Log

| Date | Change | Source |
|------|--------|--------|
| 2026-04-05 | Initial creation with baseline intelligence through early 2025 | Training knowledge |
