---
name: supply-chain-threats
description: Use when the user asks about supply-chain attacks, third-party / vendor compromise (SolarWinds, Kaseya, 3CX, MOVEit, XZ-utils-style), software-bill-of-materials risks, or library / dependency-injection attacks. Self-updating knowledge cell.
user-invocable: true
metadata:
  category: knowledge-cell
  created: 2026-04-05
  last_updated: 2026-09-29
  update_count: 1
  confidence: moderate
---

# Supply Chain Threats

## Executive Summary

Software supply chain attacks target the trust relationships between organizations and their software vendors, open-source dependencies, SaaS integrations, and managed service providers. Rather than attacking a target directly, adversaries compromise an upstream component — a package maintainer account, a CI/CD workflow, an update channel, an OAuth integration, or an MSP's remote management tooling — to reach many downstream victims at once. The defining incidents of 2020 to 2024 (SolarWinds, Kaseya, 3CX, MOVEit, XZ Utils) remain the reference cases, but the threat picture as of September 2026 is dominated by a different pattern: high-tempo, credential-stealing attacks on the developer ecosystem itself.

Three shifts stand out since early 2025. First, self-propagating package worms became routine. Shai-Hulud (September 2025) was described by Wiz as the first successful self-propagating attack in the npm ecosystem; it was followed by Shai-Hulud 2.0 (November 2025), the "Mini Shai-Hulud" waves attributed to TeamPCP (April to June 2026), and ChainDrop (August 2026), which infected hundreds of packages within hours. The Mini Shai-Hulud source code was published in May 2026, and Red Hat now describes the derived "Miasma" payload as an open-source malware kit, so later waves cannot be assumed to be the work of one group. Second, CI/CD became the primary entry point: the tj-actions/changed-files compromise (March 2025), the Nx "s1ngularity" incident (August 2025), the Trivy compromise (March 2026) and the TanStack compromise (May 2026) all abused GitHub Actions, and the TanStack wave produced malicious packages carrying valid SLSA Build Level 3 provenance. Third, North Korean actors moved to social engineering of maintainers of very widely used packages: Google, Microsoft and Amazon attribute the axios compromise (March 2026) to a DPRK actor tracked as UNC1069 or Sapphire Sleet.

Outside the package registries, SaaS-to-SaaS OAuth token theft emerged as a supply-chain class of its own (Salesloft Drift in August 2025, Gainsight in November 2025, Klue in June 2026), Cl0p continued its mass-exploitation model against enterprise applications (Oracle E-Business Suite in 2025, PTC Windchill in 2026), and update channels were hijacked at the infrastructure layer (Notepad++ in 2025, Virtualizor and Coder's module registry in August 2026). Registry operators have responded with time-based defenses: Dependabot now waits three days before proposing non-security version updates, and PyPI rejects new files on releases older than 14 days.

## Key Actors

| Actor | Attribution | Notable Operations | Motivation |
|-------|-----------|-------------------|------------|
| APT29/Midnight Blizzard (Cozy Bear) | Russia (SVR) | SolarWinds (2020); Microsoft email compromise (2024) | Espionage |
| Lazarus Group / TraderTraitor (UNC4899) | North Korea (RGB) | 3CX supply chain attack (2023); Bybit theft via compromised Safe{Wallet} developer workstation and injected JavaScript (Feb 2025, ~$1.5B per FBI) | Financial/Espionage |
| Sapphire Sleet / UNC1069 (BlueNoroff, Stardust Chollima) | North Korea | axios (Mar 2026); Mastra npm scope (Jun 2026, Microsoft high confidence); Amazon also links typo-crypto (Mar 2025) and chalk/debug (Sep 2025) with medium confidence | Financial |
| TeamPCP | Cybercriminal collective; two alleged members arrested in Australia (Aug 2026) | Trivy, Checkmarx KICS, LiteLLM, Telnyx (Mar 2026); Bitwarden CLI, SAP CAP packages (Apr 2026); TanStack and @antv waves (May 2026) | Credential theft, extortion |
| GlassWorm operators | Unknown; researchers note Russian-language indicators but consider them insufficient for attribution | Malicious VS Code / Open VSX extensions from Oct 2025; 433 components across GitHub, npm and extension marketplaces (Mar 2026); C2 disrupted May 2026 | Credential and cryptocurrency theft |
| UNC6395 and ShinyHunters-linked clusters (Storm-3138, Icarus) | Cybercriminal; group names overlap and are claimed opportunistically | Salesloft Drift OAuth token abuse (Aug 2025); Gainsight (Nov 2025); Klue (Jun 2026) | Data theft, extortion |
| Cl0p Ransomware (FIN11 overlap) | Cybercriminal | MOVEit (2023); GoAnywhere (2023); Cleo (2024); Accellion (2020); Oracle E-Business Suite (2025); PTC Windchill/FlexPLM (2026) | Financial |
| Lotus Blossom (Billbug) | China-nexus (Rapid7, moderate confidence) | Notepad++ update traffic hijack delivering Chrysalis backdoor (Jun-Nov 2025) | Espionage |
| Storm-1175 | China-based, financially motivated (Microsoft) | N-able N-central zero-day exploitation followed by StormEncryptor ransomware (Aug 2026) | Financial |
| "Jia Tan" (XZ Utils) | Unknown (suspected state) | XZ Utils backdoor (2024); multi-year social engineering of maintainer | Suspected espionage |
| UNC2452 (SolarWinds cluster) | Russia | SolarWinds Orion supply chain compromise | Espionage |
| Various npm/PyPI attackers | Multiple actors | GitHub's advisory database catalogued about 18 newly identified malicious npm packages per day in the year to May 2026 | Cryptomining, data theft, access |
| APT41/Barium | China (MSS-linked) | CCleaner (2017); ASUS Live Update (2019); multiple software vendor compromises | Espionage/Financial |
| REvil | Cybercriminal (defunct) | Kaseya VSA attack (2021) targeting MSPs | Financial |
| Various IABs | Cybercriminal | MSP compromises sold for downstream access | Financial |

## Current Activity

### Self-Propagating Package Worms (Ongoing)
The most recent large wave is ChainDrop. On 4 August 2026 an attacker used a compromised maintainer identity to push malicious commits to the keyv repository and publish keyv 6.0.0, followed by cacheable, flat-cache, cache-manager and related packages. The payload runs from a preinstall hook, downloads the Bun runtime, harvests cloud, CI/CD, developer and AI-tool credentials, and republishes itself into every package the stolen npm tokens can reach. It also plants persistence in VS Code tasks and Claude Code hooks, and retrieves C2 details from an Ethereum smart contract. Counts differ by vendor and time of writing: Wiz reported over 400 packages, Aikido at least 444 packages across 1,381 versions, and BleepingComputer later cited Aikido for at least 868. Wiz describes the payload as a descendant of the Mini Shai-Hulud family; Datadog names no actor.

Because the Mini Shai-Hulud source code was briefly published on GitHub on 12 May 2026, and Unit 42 found attribution of the July 2026 AsyncAPI compromise ambiguous despite infrastructure overlaps with TeamPCP, each new wave needs its own attribution assessment.

### DPRK Social Engineering of Package Maintainers (Ongoing)
On 31 March 2026 two malicious axios releases (1.14.1 and 0.30.4) were live for about three hours. They added the dependency plain-crypto-js, which delivered the WAVESHAPER.V2 backdoor on Windows, macOS and Linux. Google attributes the attack to UNC1069; Microsoft attributes it to Sapphire Sleet. On 17 June 2026 the same actor, per Microsoft with high confidence, used a compromised maintainer account to add a typosquatted dependency to more than 140 packages in the Mastra scopes. In July 2026 Amazon linked axios, chalk/debug (September 2025) and typo-crypto (March 2025) to Sapphire Sleet with medium confidence. A Rust crate compromise on 20 August 2026 (arrayref 0.3.10 and two other crates) showed what Wiz called significant overlap with these campaigns; no formal attribution has been published.

### CI/CD Pipeline Targeting (Ongoing)
GitHub Actions is now the most common entry point for large package compromises. Recurring weaknesses are the `pull_request_target` trigger, mutable action tags, cache poisoning and long-lived publishing tokens. In the May 2026 TanStack compromise the attackers chained three GitHub Actions weaknesses without any stolen credentials, extracted an OIDC token from runner memory, and published packages with valid SLSA provenance. In the June 2026 Red Hat incident a developer's GitHub account, compromised through a malicious VS Code extension, was used to trigger publishing workflows for 32 @redhat-cloud-services packages. In July 2026 attackers pushed to unprotected release branches in four AsyncAPI repositories.

### SaaS Integration OAuth Token Abuse (Ongoing)
Attackers compromise a SaaS vendor that holds OAuth tokens for its customers' Salesforce or Google Workspace tenants, then use those tokens to query many customer environments, bypassing MFA. On 12 June 2026 tokens held by the market-intelligence platform Klue were used to steal Salesforce data from customers including LastPass; the Icarus extortion group claimed responsibility. Microsoft's July 2026 review places Klue in a year-long series with Salesloft Drift and Gainsight and ties the activity to ShinyHunters-linked actors.

### Enterprise Application Mass Exploitation (Cl0p Pattern)
Cl0p continues to exploit widely deployed enterprise applications and extort victims weeks later. Following Accellion FTA (2020), GoAnywhere MFT (2023), MOVEit Transfer (2023) and Cleo (late 2024), the group's brand was used in an extortion campaign against Oracle E-Business Suite customers: Google observed exploitation of CVE-2025-61882 from 9 August 2025 and extortion emails from 29 September 2025. In mid-2026 CVE-2026-12569 in PTC Windchill and FlexPLM was exploited to plant JSP webshells and steal product lifecycle data. PTC began patching on 17 June 2026 and CISA added the flaw to its Known Exploited Vulnerabilities catalog on 25 June. ReliaQuest states the actor is unconfirmed but the tradecraft matches earlier Cl0p campaigns.

### Update and Distribution Infrastructure Hijacking (Ongoing)
Attackers are intercepting software delivery without touching source code or build systems. Between 28 and 30 August 2026 an unauthorized BGP announcement diverted traffic for Softaculous infrastructure; the attacker obtained valid TLS certificates and served a malicious Virtualizor update to what the vendor calls a small number of installations. On 31 August 2026 an attacker with access to Coder's Cloudflare account added rogue servers to the registry.coder.com pool for about 14 hours, serving Terraform modules with credential-stealing scripts. On 14 September 2026 a hardcoded Cloudflare API key let attackers inject ClickFix scripts into Brevo scripts embedded on customer websites. None of the three has been attributed.

### MSP and RMM Tooling (Ongoing)
Storm-1175 exploited CVE-2026-18577, an authentication bypass in N-able N-central, as a zero-day from 31 July 2026 and began deploying a new ransomware strain, StormEncryptor, on 2 August. A compromised N-central server gives access to every endpoint it manages, including the clients of an MSP. N-able said it contacted a limited number of affected customers; no downstream victim count has been published.

## Historical Events

| Date | Event | Impact |
|------|-------|--------|
| Aug-Sep 2017 | CCleaner supply chain compromise (APT41) | Backdoored version 5.33 distributed 15 Aug to 12 Sep 2017 to 2.3M users; targeted subset of tech companies |
| Dec 2020 | SolarWinds Orion backdoor discovered | 18,000 orgs received trojanized update; ~100 selectively targeted for follow-on espionage |
| Apr 2021 | Codecov bash uploader compromise | Malicious modification exfiltrated CI/CD secrets from thousands of repos |
| Jul 2021 | Kaseya VSA attack (REvil) | MSP management tool exploited to deploy ransomware to 1,500+ downstream businesses |
| Oct 2021 | ua-parser-js npm compromise | Popular package (8M weekly downloads) hijacked via maintainer account compromise |
| Nov 2021 | Log4Shell (CVE-2021-44228) | Not a supply chain attack per se, but highlighted systemic risk of ubiquitous open-source dependencies |
| Jan 2023 | CircleCI security incident | Employee credential theft led to customer secrets exposure |
| Feb 2023 | GoAnywhere MFT zero-day (Cl0p) | 130+ organizations breached via CVE-2023-0669 |
| Mar 2023 | 3CX supply chain attack (Lazarus) | Desktop client trojanized; traced back to prior Trading Technologies supply chain compromise |
| May 2023 | MOVEit Transfer mass exploitation (Cl0p) | CVE-2023-34362; 2,500+ orgs and 60M+ individuals affected |
| Mar 2024 | XZ Utils backdoor discovered (CVE-2024-3094) | Multi-year social engineering campaign to backdoor foundational Linux library; caught before widespread deployment |
| Late 2024 | Cleo file transfer exploitation (Cl0p) | Continuation of Cl0p's pattern targeting file transfer appliances |
| Feb 2025 | Bybit theft via Safe{Wallet} (TraderTraitor) | Developer workstation infected through a malicious Docker project; JavaScript served from Safe{Wallet}'s S3 bucket altered to target Bybit; ~$1.5B stolen |
| Mar 2025 | tj-actions/changed-files and reviewdog/action-setup (CVE-2025-30066, CVE-2025-30154) | Chain began with a SpotBugs maintainer token leaked in late 2024; initial target was Coinbase's agentkit; 23,000+ repositories used the action |
| Aug 2025 | Nx "s1ngularity" npm compromise | Workflow injection via pull request title; malware invoked installed AI CLI tools to search for secrets; 1,000+ GitHub tokens stolen, 5,500+ private repos made public |
| Aug 2025 | Salesloft Drift OAuth token abuse (UNC6395) | Salesforce data exported 8-18 Aug 2025; Drift Email tokens also affected; 700+ organizations per later reporting |
| Aug-Oct 2025 | Oracle E-Business Suite exploitation (Cl0p brand) | CVE-2025-61882 exploited as zero-day; mass extortion emails to executives |
| Sep 2025 | chalk/debug npm compromise | 18 packages with 2B+ combined weekly downloads; maintainer phished; cryptocurrency address-swapping payload live ~2.5 hours |
| Sep 2025 | Shai-Hulud npm worm | First wave from 15 Sep 2025; counts grew from 100+ (Wiz) to over 500 packages (CISA) |
| Jun-Dec 2025 | Notepad++ update hijack (Lotus Blossom) | Hosting provider compromise used to redirect update traffic for selected users; disclosed Feb 2026; verification added in v8.8.9 |
| Nov 2025 | Shai-Hulud 2.0 | 796 packages (Datadog); preinstall execution; home-directory wipe fallback; exfiltration repo counts range from 14,000+ (Datadog) to 25,000+ (Unit 42) |
| Nov 2025 | Gainsight OAuth token abuse | 200+ Salesforce instances per Microsoft, as reported by The Hacker News |
| Mar 2026 | TeamPCP campaign: Trivy, Checkmarx KICS, LiteLLM, Telnyx | Trivy release v0.69.4 and action tags replaced; stolen CI secrets used to publish litellm 1.82.7/1.82.8 and telnyx 4.87.1/4.87.2 |
| Mar 2026 | axios npm compromise (UNC1069 / Sapphire Sleet) | Versions 1.14.1 and 0.30.4 live ~3 hours on 31 Mar; cross-platform backdoor |
| Apr 2026 | Bitwarden CLI and SAP CAP npm packages (TeamPCP / Mini Shai-Hulud) | @bitwarden/cli 2026.4.0 (22 Apr); four SAP packages (29 Apr) |
| May 2026 | TanStack and @antv waves (TeamPCP) | 373 malicious versions across 169 npm packages and 2 PyPI packages (11 May); 639 versions across 323 packages (19 May); token-revocation-triggered home-directory wipe |
| May 2026 | GlassWorm C2 disruption | CrowdStrike, Google and Shadowserver disrupted all four C2 channels on 26 May 2026 |
| Jun 2026 | Red Hat @redhat-cloud-services npm compromise | 32 packages; Red Hat reports no product release affected and closed its investigation on 17 Jun |
| Jun 2026 | Mastra npm compromise (Sapphire Sleet) | 140+ packages given a malicious typosquatted dependency |
| Aug 2026 | Alleged TeamPCP members arrested | Two men arrested in Western Australia on 26 Aug 2026 by the AFP with FBI and state police |

## TTP Evolution

**Software Build Compromise**: The SolarWinds model — injecting malicious code into a vendor's build pipeline so that signed, legitimate-looking updates contain backdoors — remains the most sophisticated supply chain vector. Defenders responded with build provenance verification, reproducible builds, and the SLSA framework. Attackers have adapted by targeting earlier stages (source code repositories, developer workstations, code review processes) and, since 2025, the CI workflow itself. The TanStack compromise showed that provenance attests where a package was built, not that the build was uncompromised.

**Self-Propagating Worms**: The payload steals npm and GitHub tokens, enumerates packages the victim can publish, injects itself and republishes. Execution moved from postinstall (Shai-Hulud) to preinstall (Shai-Hulud 2.0 onward), and the Bun runtime is used to avoid Node.js-focused monitoring. Destructive behavior has been added as a deterrent to response: Shai-Hulud 2.0 attempts to wipe the home directory when it cannot exfiltrate or propagate, and the TanStack payload installs a daemon that does so if the stolen GitHub token is revoked.

**Decentralized C2**: GlassWorm resolves C2 through Solana transaction memos, BitTorrent DHT and Google Calendar event titles. The Miasma variant seen in July 2026 used Ethereum smart contracts, Nostr relays and BitTorrent DHT as fallbacks.

**Developer Tooling as Target and Instrument**: The Nx malware ran installed AI command-line assistants with permission-bypass flags to search the filesystem. Unit 42 assesses with moderate confidence that an LLM generated part of the first Shai-Hulud payload. ChainDrop and the Red Hat incident both planted persistence in IDE and AI coding tool configuration files so that opening a repository re-infects the next developer.

**Dependency Attacks**: Dependency confusion (Alex Birsan's research, 2021) showed that internal package names could be hijacked by publishing identically named public packages with higher version numbers, causing build systems to pull the malicious public version. While mitigations exist (registry scoping, pinning), the technique continues to be exploited. A common 2026 variant adds a new malicious dependency to a legitimate package rather than altering its code (plain-crypto-js in axios, easy-day-js in Mastra, proc-macro1 in arrayref).

**MSP/MSSP Compromise**: Targeting Managed Service Providers provides a multiplier effect, as a single MSP compromise grants access to dozens or hundreds of client organizations. The Kaseya VSA attack demonstrated this at scale, and the N-central exploitation of August 2026 repeated the model. RMM (Remote Monitoring and Management) tools used by MSPs represent attractive targets.

**Social Engineering of Maintainers**: The XZ Utils case demonstrated a patient approach: building trust with an open-source maintainer over years before introducing a concealed backdoor. The 2025-2026 cases are faster: phishing from a lookalike npm support domain (chalk/debug) and targeted social engineering of individual maintainers (axios).

**Watering Hole via Popular Libraries**: Rather than creating new malicious packages, attackers increasingly target the accounts of popular library maintainers (via credential theft, SIM swapping, or session hijacking from infostealer logs) to inject malicious code into libraries with millions of weekly downloads. GitHub's review of 21 incidents found malicious versions were consistently pulled within hours, which is the basis for cooldown defenses.

## Ecosystem & Infrastructure Patterns

**Attack Surface Mapping**: The average enterprise application has hundreds of direct and transitive dependencies, creating a vast attack surface. Tools like Dependabot, Snyk, and Renovate automate dependency monitoring but struggle with novel attack techniques and social engineering vectors. Automated updating also shortens the time between a malicious publish and its installation.

**Registry and Platform Hardening**: In July 2026 GitHub gave Dependabot a default three-day cooldown before proposing non-security version updates, and PyPI began rejecting new files uploaded to releases older than 14 days, citing the LiteLLM and Telnyx incidents. CISA's guidance after Shai-Hulud and axios recommends pinning versions, phishing-resistant MFA for developer accounts, credential rotation and disabling install scripts where possible.

**SLSA Framework**: Supply-chain Levels for Software Artifacts (SLSA, pronounced "salsa") defines a Build track with levels from L0 (no guarantees) to L3 (hardened builds with strong tamper protection). Version 1.0 removed the earlier four-level scheme, and version 1.2 is current. Adoption is growing but remains partial, and valid provenance has now been observed on malicious packages.

**SBOM Adoption**: Software Bills of Materials (SBOMs), mandated for US government software by Executive Order 14028, provide transparency into software components. Formats include SPDX and CycloneDX. While SBOMs improve visibility, they are only as useful as the vulnerability intelligence matched against them.

**SaaS Integration Sprawl**: OAuth tokens granted to third-party integrations are long-lived, bypass MFA and are stored by the vendor. One vendor compromise exposes every customer tenant that authorized the integration.

**Sector Impact**: Supply chain attacks disproportionately affect government (espionage targeting via software vendors), financial services and cryptocurrency (high-value data and transaction capability), and technology companies (access to downstream customers and source code). Healthcare, education, and critical infrastructure are affected as consumers of compromised software. Manufacturing, aerospace and defense were exposed through the 2026 PTC Windchill exploitation.

## Tooling

| Tool/Framework | Category | Usage |
|---------------|----------|-------|
| SLSA Framework | Defense/Standards | Supply chain integrity levels for build provenance |
| Sigstore/Cosign | Code Signing | Keyless signing and verification for software artifacts |
| SBOM (SPDX, CycloneDX) | Transparency | Software composition documentation |
| Dependabot/Snyk/Renovate | Dependency Management | Automated dependency monitoring and updates; Dependabot applies a default three-day cooldown since July 2026 |
| Socket.dev | Package Analysis | Detects supply chain attacks in open-source packages |
| in-toto | Build Verification | Framework for securing build pipeline integrity |
| GUAC (Graph for Understanding Artifact Composition) | Analysis | Aggregates software security metadata |
| npm audit / pip-audit | Vulnerability Scanning | Package-level vulnerability detection |
| Scorecard (OpenSSF) | Risk Assessment | Automated security assessment of open-source projects |
| Reproducible Builds | Verification | Techniques to verify build output matches source |
| Shai-Hulud / Mini Shai-Hulud / Miasma | Attacker malware family | Self-propagating npm credential stealer; source code public since May 2026 |
| WAVESHAPER.V2 | Attacker malware | Cross-platform backdoor delivered through the axios compromise |
| GlassWorm | Attacker malware | Extension- and package-borne stealer with blockchain-based C2 |
| TruffleHog | Dual-use | Legitimate secret scanner run by the first Shai-Hulud payload to find credentials |

## Intelligence Gaps

- **Pre-positioning detection**: Organizations compromised via supply chain but not yet exploited (like SolarWinds victims who received the trojanized update but were not selected for follow-on activity) represent an unknown risk. Detection of dormant implants in legitimate software remains extremely challenging.
- **Downstream use of stolen credentials**: The worms of 2025-2026 harvested very large numbers of cloud, CI/CD and registry credentials. How many were used for follow-on intrusions, and by whom, is largely unreported.
- **Worm attribution after the source leak**: With the Mini Shai-Hulud code public, it is unconfirmed which waves after May 2026 belong to TeamPCP. ChainDrop has no published attribution. Whether related activity has continued since the August 2026 arrests was not confirmed in this refresh.
- **TeamPCP impact figures**: Figures reported at the time of the arrests (over 1,000 organizations, 500,000+ credentials) come from press coverage of the police announcement and have not been independently verified here. Vendors also disagree on the start date of the Trivy compromise (19 March per Datadog, 23 March per ReversingLabs).
- **Salesloft Drift initial access**: Google's advisory does not state how the Drift OAuth tokens were obtained, and the vendor's own account could not be retrieved for this refresh. Victim counts for Drift and Gainsight rest on secondary reporting.
- **Relationship between OAuth-abuse clusters**: How UNC6395, Storm-3138, Icarus and ShinyHunters relate is unsettled; reporting notes that the names overlap and are claimed opportunistically.
- **Update-channel hijacks**: The actors behind the Virtualizor BGP hijack, the Coder registry compromise and the Brevo script injection are unidentified, as is the method of access to Coder's Cloudflare account.
- **Open-source maintainer compromise scale**: The true number of legitimate packages whose maintainer accounts have been compromised (beyond publicly disclosed cases) is unknown. Many compromises may go undetected.
- **Nation-state involvement in open-source attacks**: DPRK activity is now well documented, but beyond XZ Utils the extent of other state-sponsored operations targeting open-source infrastructure is poorly understood.
- **Transitive dependency risk**: Most organizations do not have full visibility into their transitive (indirect) dependency chains, creating blind spots for deeply nested compromises.
- **MSP compromise frequency**: Smaller MSP compromises that do not generate headlines but provide access to dozens of downstream organizations are likely undercounted. No downstream victim count exists for the N-central exploitation.

## Sources & References

1. CISA - "Defending Against Software Supply Chain Attacks" — https://www.cisa.gov/sites/default/files/publications/defending_against_software_supply_chain_attacks.pdf
2. Mandiant - "SolarWinds/UNC2452 Investigation Reports" — https://www.mandiant.com/resources
3. SLSA Framework — https://slsa.dev/
4. OpenSSF (Open Source Security Foundation) - Supply Chain Security Initiatives — https://openssf.org/
5. Microsoft Threat Intelligence - "3CX Supply Chain Attack Analysis" — https://www.microsoft.com/en-us/security/blog/
6. Progress Software / Huntress / Rapid7 - "MOVEit Vulnerability Analysis" — various
7. NVD - "CVE-2024-3094 (XZ Utils Backdoor)" — https://nvd.nist.gov/vuln/detail/CVE-2024-3094
8. Sonatype - "State of the Software Supply Chain Report" — https://www.sonatype.com/state-of-the-software-supply-chain
9. Cisco Talos - "CCleanup: A Vast Number of Machines at Risk" (2017-09-18) — https://blog.talosintelligence.com/avast-distributes-malware/
10. SLSA - "Security levels" specification page (v1.0, notes v1.2 as current; accessed 2026-09-29) — https://slsa.dev/spec/v1.0/levels
11. FBI IC3 - "North Korea Responsible for $1.5 Billion Bybit Hack" (2025-02-26) — https://www.ic3.gov/PSA/2025/PSA250226
12. Sygnia - "Sygnia's Investigation into the Bybit Hack: What We Know So Far" (2025-03-16) — https://www.sygnia.co/blog/sygnia-investigation-bybit-hack/
13. CISA - "Supply Chain Compromise of Third-Party tj-actions/changed-files (CVE-2025-30066) and reviewdog/action-setup@v1 (CVE-2025-30154)" (2025-03-18, updated 2025-03-26) — https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction
14. Palo Alto Networks Unit 42 - "GitHub Actions Supply Chain Attack: A Targeted Attack on Coinbase Expanded to the Widespread tj-actions/changed-files Incident" (2025-03-20, updated 2025-04-02) — https://unit42.paloaltonetworks.com/github-actions-supply-chain-attack/
15. Wiz - "s1ngularity: supply chain attack leaks secrets on GitHub" (2025-08-27) — https://www.wiz.io/blog/s1ngularity-supply-chain-attack
16. Google Threat Intelligence Group - "Widespread Data Theft Targets Salesforce Instances via Salesloft Drift" (2025-08-27, updated 2025-08-28) — https://cloud.google.com/blog/topics/threat-intelligence/data-theft-salesforce-instances-via-salesloft-drift
17. Aikido - "npm debug and chalk packages compromised" (2025-09-08) — https://www.aikido.dev/blog/npm-debug-and-chalk-packages-compromised
18. Wiz - "Shai-Hulud: Ongoing Package Supply Chain Worm Delivering Data-Stealing Malware" (2025-09-16) — https://www.wiz.io/blog/shai-hulud-npm-supply-chain-attack
19. CISA - "Widespread Supply Chain Compromise Impacting npm Ecosystem" (2025-09-23) — https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem
20. Google Threat Intelligence Group - "Oracle E-Business Suite Zero-Day Exploited in Widespread Extortion Campaign" (2025-10-10) — https://cloud.google.com/blog/topics/threat-intelligence/oracle-ebusiness-suite-zero-day-exploitation
21. Palo Alto Networks Unit 42 - "'Shai-Hulud' Worm Compromises npm Ecosystem in Supply Chain Attack" (2025-11-25 update) — https://unit42.paloaltonetworks.com/npm-supply-chain-attack/
22. Datadog Security Labs - "The Shai-Hulud 2.0 npm worm: analysis, and what you need to know" (2025-11-25) — https://securitylabs.datadoghq.com/articles/shai-hulud-2.0-npm-worm/
23. Notepad++ - "Notepad++ Hijacked by State-Sponsored Hackers" (2026-02-02) — https://notepad-plus-plus.org/news/hijacked-incident-info-update/
24. Rapid7 - "The Chrysalis Backdoor: A Deep Dive into Lotus Blossom's toolkit" (2026-02-02) — https://www.rapid7.com/blog/post/tr-chrysalis-backdoor-dive-into-lotus-blossoms-toolkit/
25. BleepingComputer - "GlassWorm malware hits 400+ code repos on GitHub, npm, VSCode, OpenVSX" (2026-03-17) — https://www.bleepingcomputer.com/news/security/glassworm-malware-hits-400-plus-code-repos-on-github-npm-vscode-openvsx/
26. Datadog Security Labs - "LiteLLM and Telnyx compromised on PyPI: Tracing the TeamPCP supply chain campaign" (2026-03-24) — https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-teampcp-supply-chain-campaign/
27. ReversingLabs - "The TeamPCP supply chain attack evolves" (2026-03-27) — https://www.reversinglabs.com/blog/teampcp-supply-chain-attack-spreads
28. Google Threat Intelligence Group - "North Korea-Nexus Threat Actor Compromises Widely Used Axios NPM Package in Supply Chain Attack" (2026-04-01) — https://cloud.google.com/blog/topics/threat-intelligence/north-korea-threat-actor-targets-axios-npm-package
29. Microsoft - "Mitigating the Axios npm supply chain compromise" (2026-04-01) — https://www.microsoft.com/en-us/security/blog/2026/04/01/mitigating-the-axios-npm-supply-chain-compromise/
30. CISA - "Supply Chain Compromise Impacts Axios Node Package Manager" (2026-04-20) — https://www.cisa.gov/news-events/alerts/2026/04/20/supply-chain-compromise-impacts-axios-node-package-manager
31. Orca Security - "TanStack and 160+ npm/PyPI Packages Compromised in Supply Chain Worm Attack" (2026-05-12) — https://orca.security/resources/blog/tanstack-npm-supply-chain-worm/
32. BleepingComputer - "Glassworm botnet disrupted after resilient C2 infrastructure takedown" (2026-05-27) — https://www.bleepingcomputer.com/news/security/glassworm-botnet-disrupted-after-resilient-c2-infrastructure-takedown/
33. Red Hat - "RHSB-2026-006 Supply chain compromise of @redhat-cloud-services npm packages" (2026-06-01) — https://access.redhat.com/security/vulnerabilities/RHSB-2026-006
34. Microsoft - "From package to postinstall payload: Inside the Mastra npm supply chain compromise by Sapphire Sleet" (2026-06-17) — https://www.microsoft.com/en-us/security/blog/2026/06/17/postinstall-payload-inside-mastra-npm-supply-chain-compromise/
35. BleepingComputer - "LastPass confirms data breach in Klue supply chain attack" (2026-06-23) — https://www.bleepingcomputer.com/news/security/lastpass-confirms-data-breach-in-klue-supply-chain-attack/
36. The Hacker News - "Microsoft Maps Year-Long ShinyHunters-Linked Salesforce Data Theft Across Three Paths" (2026-07-14) — https://thehackernews.com/2026/07/microsoft-maps-year-long-shinyhunters.html
37. Palo Alto Networks Unit 42 - "The npm Threat Landscape: Attack Surface and Mitigations" (updated 2026-07-15) — https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/
38. PyPI - "Releases now reject new files after 14 days" (2026-07-22) — https://blog.pypi.org/posts/2026-07-22-releases-now-reject-new-files-after-14-days/
39. GitHub - "The case for a cooldown: Why Dependabot now waits before issuing version updates" (2026-07-23) — https://github.blog/security/supply-chain-security/the-case-for-a-cooldown-why-dependabot-now-waits-before-issuing-version-updates/
40. BleepingComputer - "Clop ransomware targets Windchill, FlexPLM in data theft attacks" (2026-07-24) — https://www.bleepingcomputer.com/news/security/clop-ransomware-targets-windchill-flexplm-in-data-theft-attacks/
41. Amazon - "Amazon identifies North Korean hacker group behind open-source supply chain attacks" (2026-07-29) — https://aws.amazon.com/blogs/security/amazon-identifies-north-korean-hacker-group-behind-open-source-supply-chain-attacks/
42. Datadog Security Labs - "'ChainDrop' worm compromises hundreds of popular npm packages" (2026-08-04) — https://securitylabs.datadoghq.com/articles/npm-worm-compromises-popular-npm-packages/
43. Wiz - "keyv and cacheable npm Package Hijacked in Supply Chain Attack" (2026-08-04) — https://www.wiz.io/blog/keyv-and-cacheable-npm-supply-chain-attack
44. Aikido - "Keyv and friends compromised in active Shai-Hulud supply chain attack" (2026-08-04, updated 2026-08-05) — https://www.aikido.dev/blog/keyv-and-friends-compromised-in-npm-supply-chain-attack
45. BleepingComputer - "Massive ChainDrop npm supply-chain attack infects hundreds of packages" (2026-08-04) — https://www.bleepingcomputer.com/news/security/massive-chaindrop-npm-supply-chain-attack-infects-hundreds-of-packages/
46. The Record - "China-linked hackers turning popular cybersecurity tool into ransomware launchpad, Microsoft warns" (2026-08-10) — https://therecord.media/china-hackers-ransomware-microsoft
47. BleepingComputer - "New StormEncryptor ransomware used by former Medusa affiliate" (2026-08-10) — https://www.bleepingcomputer.com/news/security/new-stormencryptor-ransomware-used-by-former-medusa-affiliate/
48. BleepingComputer - "Hackers poison arrayref Rust crate to push infostealer malware" (2026-08-20) — https://www.bleepingcomputer.com/news/security/hackers-poison-arrayref-rust-crate-to-push-infostealer-malware/
49. BleepingComputer - "Australia arrests alleged TeamPCP hackers behind supply-chain attacks" (2026-08-27) — https://www.bleepingcomputer.com/news/security/australia-arrests-alleged-teampcp-hackers-behind-supply-chain-attacks/
50. Softaculous / Virtualizor - "Security Incident – BGP Hijacking" (2026-08-31) — https://www.virtualizor.com/blog/security-incident-bgp-hijacking/
51. Coder - "Malicious Packages Served from Unauthorized Registry Server" (GHSA-vx42-ghc9-gw65, 2026-09-01) — https://github.com/coder/coder/security/advisories/GHSA-vx42-ghc9-gw65
52. BleepingComputer - "Brevo supply-chain attack injected ClickFix scripts on customer sites" (2026-09-17) — https://www.bleepingcomputer.com/news/security/brevo-supply-chain-attack-injected-clickfix-scripts-on-customer-sites/

## Change Log

| Date | Change | Source |
|------|--------|--------|
| 2026-04-05 | Initial creation with baseline intelligence through early 2025 | Training knowledge |
| 2026-09-29 | First refresh covering Jan 2025 to Sep 2026: rewrote Executive Summary and Current Activity; added package worms (Shai-Hulud to ChainDrop), TeamPCP, DPRK maintainer targeting, GitHub Actions compromises, SaaS OAuth token abuse, Cl0p Oracle EBS and Windchill, update-channel hijacks, N-central; added 18 Historical Events rows and 44 sources; corrected CCleaner date and SLSA level description | OSINT refresh |
