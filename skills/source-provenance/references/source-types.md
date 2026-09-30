# Source types

This table classifies sources by type, access profile and interest. It does not grade sources. The grade is worked out per claim by the skill, from the stated access, corroboration and the source's own confidence language. PRs that add reliability opinions, track-record notes or ratings for a named organisation will not be merged.

`scripts/resolve_provenance.py` reads this file directly. It is a lookup table, not model knowledge, so classification is deterministic and auditable. If a domain is not listed, the script returns `unknown` and the agent must not fill the gap from memory.

## Columns

| Column | Values |
|---|---|
| `domain` | Host, optionally followed by a path prefix (`microsoft.com/en-us/security/blog`). Longest match wins. Subdomains inherit from the parent domain unless they have their own row. |
| `organisation` | Name as the organisation writes it. Alternative names separated by ` / `; the script uses each as a match string when looking for named attributions in article text. |
| `type` | `vendor`, `government`, `victim`, `actor`, `press`, `aggregator`, `social`, `researcher` |
| `access_profile` | How the organisation typically gets its information: `telemetry`, `ir_engagement`, `sample_analysis`, `osint`, `actor_statement`, `victim_statement`, `undisclosed`. A hint for the reader only. The access recorded on an evidence item is read from the primary document's own text. |
| `interest` | `commercial`, `governmental`, `victim`, `actor`, `independent` |
| `notes` | Factual only: sub-paths, what the domain publishes. A note starting with `not a primary` tells the script never to treat a link to this row as an originating source. |

There is no reliability column, by design.

## Built-in rules

These are applied by the script before the table is consulted:

- Any `.onion` host is `actor`, `actor_statement`, interest `actor`. The pack does not list leak-site addresses: they churn, and the table is public.
- A host not matched by any row is `unknown`.

## Contributing

- A new row requires a link, in the PR description, showing what the organisation is (an about page or a published report).
- Edits to another organisation's row must state the reason in the PR.
- Type changes to an existing row need a second reviewer once one exists.
- This file is protected by a `CODEOWNERS` entry and cannot merge without a maintainer.

## Vendors

| domain | organisation | type | access_profile | interest | notes |
|---|---|---|---|---|---|
| cloud.google.com/blog/topics/threat-intelligence | Google Threat Intelligence Group / Mandiant / GTIG | vendor | ir_engagement | commercial | Mandiant and Google Threat Intelligence research blog |
| cloud.google.com | Google Cloud | vendor | undisclosed | commercial | not a primary: product pages and documentation outside the threat intelligence blog |
| mandiant.com | Mandiant | vendor | ir_engagement | commercial | Legacy domain; reports and M-Trends |
| blog.google/threat-analysis-group | Google Threat Analysis Group / Google TAG | vendor | telemetry | commercial | TAG bulletins and campaign reports |
| googleprojectzero.blogspot.com | Google Project Zero / Project Zero | vendor | sample_analysis | commercial | Vulnerability research |
| microsoft.com/en-us/security/blog | Microsoft Threat Intelligence / Microsoft | vendor | telemetry | commercial | Threat intelligence and security research blog |
| msrc.microsoft.com | Microsoft Security Response Center / MSRC | vendor | sample_analysis | commercial | Vulnerability advisories and update guides |
| techcommunity.microsoft.com | Microsoft Tech Community | vendor | undisclosed | commercial | Mixed product and security posts |
| learn.microsoft.com | Microsoft Learn | vendor | undisclosed | commercial | not a primary: documentation |
| unit42.paloaltonetworks.com | Palo Alto Networks Unit 42 / Unit 42 | vendor | telemetry | commercial | Threat research and IR findings |
| paloaltonetworks.com | Palo Alto Networks | vendor | telemetry | commercial | Corporate blog and security advisories |
| crowdstrike.com | CrowdStrike | vendor | telemetry | commercial | Blog, Counter Adversary Operations reporting, annual reports |
| welivesecurity.com | ESET Research / ESET | vendor | telemetry | commercial | ESET research blog |
| eset.com | ESET | vendor | telemetry | commercial | Corporate site, threat reports |
| securelist.com | Kaspersky GReAT / Kaspersky | vendor | telemetry | commercial | Kaspersky research blog |
| kaspersky.com | Kaspersky | vendor | telemetry | commercial | Corporate site and blog |
| news.sophos.com | Sophos X-Ops / Sophos | vendor | telemetry | commercial | Research and IR case reporting |
| sophos.com | Sophos | vendor | telemetry | commercial | Corporate site, advisories |
| sentinelone.com | SentinelOne / SentinelLabs / SentinelLABS | vendor | telemetry | commercial | SentinelLabs research under /labs |
| blog.talosintelligence.com | Cisco Talos / Talos | vendor | telemetry | commercial | Research blog |
| talosintelligence.com | Cisco Talos / Talos | vendor | telemetry | commercial | Reputation lookups and vulnerability reports |
| recordedfuture.com | Recorded Future / Insikt Group | vendor | osint | commercial | Insikt Group research |
| group-ib.com | Group-IB | vendor | ir_engagement | commercial | Research blog and annual reports |
| trendmicro.com | Trend Micro / Trend Micro Research | vendor | telemetry | commercial | Research under /research and /vinfo |
| zerodayinitiative.com | Zero Day Initiative / ZDI | vendor | sample_analysis | commercial | Vulnerability advisories; operated by Trend Micro |
| research.checkpoint.com | Check Point Research | vendor | telemetry | commercial | Research blog |
| checkpoint.com | Check Point | vendor | telemetry | commercial | Corporate blog |
| proofpoint.com | Proofpoint | vendor | telemetry | commercial | Threat insight blog; email telemetry |
| elastic.co/security-labs | Elastic Security Labs | vendor | telemetry | commercial | Research blog |
| elastic.co | Elastic | vendor | undisclosed | commercial | not a primary: product pages and documentation outside Security Labs |
| huntress.com | Huntress | vendor | telemetry | commercial | Blog; managed detection case reporting |
| volexity.com | Volexity | vendor | ir_engagement | commercial | Research blog |
| zscaler.com | Zscaler ThreatLabz / ThreatLabz / Zscaler | vendor | telemetry | commercial | ThreatLabz research |
| security.com | Symantec Threat Hunter Team / Symantec | vendor | telemetry | commercial | Symantec and Carbon Black research; part of Broadcom |
| symantec-enterprise-blogs.security.com | Symantec Threat Hunter Team / Symantec | vendor | telemetry | commercial | Legacy blog domain |
| fortinet.com | Fortinet / FortiGuard Labs | vendor | telemetry | commercial | FortiGuard Labs research under /blog/threat-research |
| fortiguard.com | FortiGuard Labs | vendor | telemetry | commercial | Advisories and encyclopedia |
| bitdefender.com | Bitdefender / Bitdefender Labs | vendor | telemetry | commercial | Labs research |
| malwarebytes.com | Malwarebytes / ThreatDown | vendor | telemetry | commercial | Blog |
| withsecure.com | WithSecure | vendor | ir_engagement | commercial | Research and IR reporting |
| secureworks.com | Secureworks Counter Threat Unit / Secureworks | vendor | ir_engagement | commercial | CTU research; part of Sophos |
| redcanary.com | Red Canary | vendor | telemetry | commercial | Blog and annual detection report |
| rapid7.com | Rapid7 | vendor | telemetry | commercial | Blog; emergent threat response posts |
| tenable.com | Tenable / Tenable Research | vendor | sample_analysis | commercial | Vulnerability research |
| qualys.com | Qualys / Qualys Threat Research Unit | vendor | sample_analysis | commercial | Vulnerability research under blog.qualys.com |
| akamai.com | Akamai / Akamai SIRT | vendor | telemetry | commercial | Security research blog |
| blog.cloudflare.com | Cloudflare / Cloudforce One | vendor | telemetry | commercial | Blog; DDoS and threat reports |
| cloudflare.com | Cloudflare / Cloudforce One | vendor | telemetry | commercial | Threat intelligence under /threat-intelligence |
| netscout.com | NETSCOUT / ASERT | vendor | telemetry | commercial | DDoS reporting |
| blog.lumen.com | Lumen Black Lotus Labs / Black Lotus Labs | vendor | telemetry | commercial | Network telemetry research |
| team-cymru.com | Team Cymru | vendor | telemetry | commercial | Network telemetry research |
| greynoise.io | GreyNoise | vendor | telemetry | commercial | Sensor network observations |
| censys.com | Censys | vendor | telemetry | commercial | Internet-wide scanning research |
| sekoia.io | Sekoia / Sekoia TDR | vendor | telemetry | commercial | Research under blog.sekoia.io |
| harfanglab.io | HarfangLab | vendor | telemetry | commercial | Research blog |
| intezer.com | Intezer | vendor | sample_analysis | commercial | Research blog |
| any.run | ANY.RUN | vendor | sample_analysis | commercial | Sandbox-based malware analyses |
| vmray.com | VMRay | vendor | sample_analysis | commercial | Sandbox-based malware analyses |
| reversinglabs.com | ReversingLabs | vendor | sample_analysis | commercial | Research blog; software supply chain |
| blog.virustotal.com | VirusTotal | vendor | sample_analysis | commercial | Research on submitted samples |
| cybereason.com | Cybereason | vendor | telemetry | commercial | Research blog |
| trellix.com | Trellix / Trellix Advanced Research Center | vendor | telemetry | commercial | Research blog |
| mcafee.com | McAfee / McAfee Labs | vendor | telemetry | commercial | Consumer threat research |
| trustwave.com | Trustwave SpiderLabs / SpiderLabs / Trustwave | vendor | ir_engagement | commercial | SpiderLabs blog |
| nccgroup.com | NCC Group / Fox-IT | vendor | ir_engagement | commercial | Research and monthly threat reporting |
| fox-it.com | Fox-IT | vendor | ir_engagement | commercial | Part of NCC Group |
| eclecticiq.com | EclecticIQ | vendor | osint | commercial | Analyst research blog |
| intel471.com | Intel 471 | vendor | osint | commercial | Underground-source reporting |
| flashpoint.io | Flashpoint | vendor | osint | commercial | Underground-source reporting |
| kelacyber.com | KELA | vendor | osint | commercial | Underground-source reporting |
| cyble.com | Cyble / CRIL | vendor | osint | commercial | Research blog |
| socradar.io | SOCRadar | vendor | osint | commercial | Blog |
| resecurity.com | Resecurity | vendor | osint | commercial | Blog |
| hudsonrock.com | Hudson Rock | vendor | osint | commercial | Infostealer log reporting |
| spycloud.com | SpyCloud | vendor | osint | commercial | Recaptured data reporting |
| dragos.com | Dragos | vendor | ir_engagement | commercial | ICS and OT threat reporting |
| claroty.com | Claroty / Team82 | vendor | sample_analysis | commercial | ICS vulnerability research |
| nozominetworks.com | Nozomi Networks / Nozomi Networks Labs | vendor | telemetry | commercial | OT and IoT research |
| wiz.io | Wiz / Wiz Research | vendor | telemetry | commercial | Cloud threat research |
| sysdig.com | Sysdig / Sysdig Threat Research Team | vendor | telemetry | commercial | Cloud and container research |
| aquasec.com | Aqua Security / Aqua Nautilus | vendor | telemetry | commercial | Honeypot-based cloud research |
| securitylabs.datadoghq.com | Datadog Security Labs | vendor | telemetry | commercial | Cloud threat research |
| sec.okta.com | Okta Security / Okta Threat Intelligence | vendor | telemetry | commercial | Identity threat reporting |
| aws.amazon.com/blogs/security | AWS Security / Amazon Threat Intelligence | vendor | telemetry | commercial | Security blog |
| aws.amazon.com | Amazon Web Services | vendor | undisclosed | commercial | not a primary: product pages and documentation outside the security blog |
| github.blog | GitHub / GitHub Security Lab | vendor | sample_analysis | commercial | Security Lab research and incident notices |
| arcticwolf.com | Arctic Wolf / Arctic Wolf Labs | vendor | telemetry | commercial | Labs blog and security bulletins |
| esentire.com | eSentire / eSentire Threat Response Unit | vendor | telemetry | commercial | TRU advisories |
| binarydefense.com | Binary Defense | vendor | telemetry | commercial | Research blog |
| expel.com | Expel | vendor | telemetry | commercial | Blog and quarterly reports |
| kroll.com | Kroll | vendor | ir_engagement | commercial | Cyber risk publications |
| sygnia.co | Sygnia | vendor | ir_engagement | commercial | IR-based research |
| coveware.com | Coveware | vendor | ir_engagement | commercial | Quarterly ransomware reports from negotiation cases |
| halcyon.ai | Halcyon | vendor | telemetry | commercial | Ransomware reporting |
| asec.ahnlab.com | AhnLab Security Intelligence Center / ASEC / AhnLab | vendor | telemetry | commercial | Research blog |
| ti.qianxin.com | QiAnXin Threat Intelligence Center / QiAnXin | vendor | telemetry | commercial | Research blog |
| lab52.io | Lab52 / S2 Grupo | vendor | sample_analysis | commercial | Research blog |
| cyfirma.com | CYFIRMA | vendor | osint | commercial | Research reports |
| silentpush.com | Silent Push | vendor | osint | commercial | Infrastructure research |
| domaintools.com | DomainTools / DomainTools Investigations | vendor | osint | commercial | Infrastructure research |
| blogs.infoblox.com | Infoblox / Infoblox Threat Intel | vendor | telemetry | commercial | DNS telemetry research |
| labs.watchtowr.com | watchTowr Labs / watchTowr | vendor | sample_analysis | commercial | Vulnerability research |
| horizon3.ai | Horizon3.ai | vendor | sample_analysis | commercial | Vulnerability research |
| vulncheck.com | VulnCheck | vendor | osint | commercial | Exploitation tracking |
| socket.dev | Socket / Socket Threat Research Team | vendor | sample_analysis | commercial | Package ecosystem research |
| checkmarx.com | Checkmarx | vendor | sample_analysis | commercial | Supply chain research |
| sonatype.com | Sonatype | vendor | sample_analysis | commercial | Package ecosystem research |
| jfrog.com | JFrog / JFrog Security Research | vendor | sample_analysis | commercial | Package ecosystem and vulnerability research |
| abnormal.ai | Abnormal AI / Abnormal Security | vendor | telemetry | commercial | Email threat reporting |
| cofense.com | Cofense | vendor | telemetry | commercial | Phishing reporting |
| netskope.com | Netskope / Netskope Threat Labs | vendor | telemetry | commercial | Threat Labs research |
| forescout.com | Forescout / Vedere Labs | vendor | telemetry | commercial | Vedere Labs research |
| chainalysis.com | Chainalysis | vendor | osint | commercial | Blockchain analysis |
| trmlabs.com | TRM Labs | vendor | osint | commercial | Blockchain analysis |
| elliptic.co | Elliptic | vendor | osint | commercial | Blockchain analysis |
| support.citrix.com | Citrix / Cloud Software Group | vendor | sample_analysis | commercial | Security bulletins for Citrix products |
| oracle.com/security-alerts | Oracle | vendor | sample_analysis | commercial | Security alerts and critical patch updates |
| sec.cloudapps.cisco.com | Cisco PSIRT / Cisco | vendor | sample_analysis | commercial | Security advisories for Cisco products |
| support.broadcom.com | Broadcom / VMware | vendor | sample_analysis | commercial | Security advisories for VMware and Broadcom products |
| psirt.global.sonicwall.com | SonicWall PSIRT / SonicWall | vendor | sample_analysis | commercial | Security advisories for SonicWall products |
| sonicwall.com | SonicWall / SonicWall Capture Labs | vendor | telemetry | commercial | Blog and threat reports |
| forums.ivanti.com | Ivanti | vendor | sample_analysis | commercial | Security advisories for Ivanti products |
| ontinue.com | Ontinue | vendor | telemetry | commercial | Managed detection research |
| patchstack.com | Patchstack | vendor | sample_analysis | commercial | WordPress vulnerability research |
| wordfence.com | Wordfence | vendor | telemetry | commercial | WordPress vulnerability and attack reporting |
| sucuri.net | Sucuri | vendor | ir_engagement | commercial | Website compromise research under blog.sucuri.net |
| qrator.net | Qrator Labs | vendor | telemetry | commercial | DDoS and botnet reporting |
| acronis.com | Acronis / Acronis Threat Research Unit | vendor | telemetry | commercial | Threat Research Unit blog |
| imperva.com | Imperva / Imperva Threat Research | vendor | telemetry | commercial | Application attack research |
| f5.com/labs | F5 Labs | vendor | telemetry | commercial | Threat research |
| ibm.com/think/x-force | IBM X-Force / X-Force | vendor | ir_engagement | commercial | X-Force research |
| securityintelligence.com | IBM X-Force / IBM Security Intelligence | vendor | ir_engagement | commercial | Legacy X-Force blog domain |
| blogs.blackberry.com | BlackBerry / BlackBerry Research and Intelligence | vendor | telemetry | commercial | Research blog |
| gendigital.com | Gen / Gen Threat Labs / Avast | vendor | telemetry | commercial | Threat Labs research and quarterly reports |
| decoded.avast.io | Avast Threat Labs / Avast | vendor | telemetry | commercial | Legacy research blog |
| gdatasoftware.com | G DATA | vendor | telemetry | commercial | Research blog |
| drweb.com | Doctor Web / Dr.Web | vendor | telemetry | commercial | Malware research under news.drweb.com |
| threatfabric.com | ThreatFabric | vendor | sample_analysis | commercial | Mobile malware research |
| cleafy.com | Cleafy | vendor | telemetry | commercial | Banking fraud and mobile malware research |
| prodaft.com | PRODAFT | vendor | osint | commercial | Threat actor reporting |
| teamt5.org | TeamT5 | vendor | ir_engagement | commercial | APAC threat research |
| orangecyberdefense.com | Orange Cyberdefense | vendor | ir_engagement | commercial | Research and Security Navigator |
| synacktiv.com | Synacktiv | vendor | sample_analysis | commercial | Vulnerability and reverse engineering research |
| nextron-systems.com | Nextron Systems | vendor | sample_analysis | commercial | Malware and detection research |
| truesec.com | Truesec | vendor | ir_engagement | commercial | IR-based research |
| blog.nviso.eu | NVISO / NVISO Labs | vendor | ir_engagement | commercial | Research blog |
| fieldeffect.com | Field Effect | vendor | telemetry | commercial | Research blog |
| reliaquest.com | ReliaQuest | vendor | telemetry | commercial | Threat research |
| guidepointsecurity.com | GuidePoint Security / GRIT | vendor | ir_engagement | commercial | GRIT ransomware reporting |
| flare.io | Flare | vendor | osint | commercial | Underground-source reporting |
| cloudsek.com | CloudSEK | vendor | osint | commercial | Research blog |
| bitsight.com | Bitsight / Bitsight TRACE | vendor | telemetry | commercial | Internet measurement and sinkhole research |
| securityscorecard.com | SecurityScorecard / STRIKE | vendor | telemetry | commercial | STRIKE team research |
| eclypsium.com | Eclypsium | vendor | sample_analysis | commercial | Firmware and supply chain research |
| binarly.io | Binarly | vendor | sample_analysis | commercial | Firmware vulnerability research |
| orca.security | Orca Security | vendor | telemetry | commercial | Cloud research |
| snyk.io | Snyk | vendor | sample_analysis | commercial | Package ecosystem and vulnerability research |
| aikido.dev | Aikido Security / Aikido | vendor | sample_analysis | commercial | Package ecosystem research |
| stepsecurity.io | StepSecurity | vendor | telemetry | commercial | CI/CD supply chain research |
| lookout.com | Lookout | vendor | telemetry | commercial | Mobile threat research |
| zimperium.com | Zimperium / zLabs | vendor | telemetry | commercial | Mobile threat research |
| iverify.io | iVerify | vendor | telemetry | commercial | Mobile forensics research |
| jamf.com | Jamf / Jamf Threat Labs | vendor | telemetry | commercial | Apple platform threat research |
| permiso.io | Permiso | vendor | telemetry | commercial | Cloud identity threat research |
| mitiga.io | Mitiga | vendor | ir_engagement | commercial | Cloud IR research |
| pushsecurity.com | Push Security | vendor | telemetry | commercial | Identity attack research |
| varonis.com | Varonis / Varonis Threat Labs | vendor | ir_engagement | commercial | Threat Labs research |
| morphisec.com | Morphisec | vendor | telemetry | commercial | Research blog |
| securonix.com | Securonix / Securonix Threat Research | vendor | telemetry | commercial | Threat research |
| hunt.io | Hunt.io | vendor | osint | commercial | Infrastructure research |
| ptsecurity.com | Positive Technologies | vendor | ir_engagement | commercial | Research and IR reporting |
| genians.co.kr | Genians / Genians Security Center | vendor | telemetry | commercial | Korean-peninsula threat research |
| seqrite.com | Seqrite / Quick Heal | vendor | telemetry | commercial | Research blog |
| pwc.com | PwC / PwC Threat Intelligence | vendor | ir_engagement | commercial | Threat intelligence publications |
| openai.com | OpenAI | vendor | telemetry | commercial | Threat disruption reports and notices about incidents affecting its own services |
| anthropic.com | Anthropic | vendor | telemetry | commercial | Threat intelligence reports and notices about incidents affecting its own services |
| prnewswire.com | PR Newswire | vendor | undisclosed | commercial | Press release wire: text is authored by the issuing organisation, which is the source |
| businesswire.com | Business Wire | vendor | undisclosed | commercial | Press release wire: text is authored by the issuing organisation, which is the source |
| globenewswire.com | GlobeNewswire | vendor | undisclosed | commercial | Press release wire: text is authored by the issuing organisation, which is the source |

## Governments and public bodies

| domain | organisation | type | access_profile | interest | notes |
|---|---|---|---|---|---|
| cisa.gov | CISA / Cybersecurity and Infrastructure Security Agency | government | undisclosed | governmental | Advisories, KEV catalogue, joint advisories. Check each advisory for whether it adds evidence or aggregates vendor reporting |
| ic3.gov | FBI Internet Crime Complaint Center / IC3 | government | victim_statement | governmental | FLASH reports, PSAs, annual report built from complaints |
| fbi.gov | FBI / Federal Bureau of Investigation | government | undisclosed | governmental | Press releases, wanted notices |
| nsa.gov | NSA / National Security Agency | government | undisclosed | governmental | Cybersecurity advisories |
| justice.gov | US Department of Justice / Department of Justice / DOJ | government | undisclosed | governmental | Indictments and press releases |
| home.treasury.gov | US Department of the Treasury / OFAC / Treasury | government | undisclosed | governmental | Sanctions designations |
| state.gov | US Department of State | government | undisclosed | governmental | Rewards for Justice notices, statements |
| hhs.gov | US Department of Health and Human Services / HC3 | government | osint | governmental | HC3 sector notes; breach portal |
| nvd.nist.gov | National Vulnerability Database / NVD / NIST | government | osint | governmental | Vulnerability records |
| sec.gov/Archives/edgar | SEC EDGAR filing | victim | victim_statement | victim | Company filings including 8-K Item 1.05. The filer is the source, not the SEC |
| sec.gov | US Securities and Exchange Commission / SEC | government | undisclosed | governmental | Enforcement actions and rules |
| oag.ca.gov | California Attorney General breach notices | victim | victim_statement | victim | Breach notification letters submitted by the affected organisation |
| maine.gov/agviewer | Maine Attorney General breach notices | victim | victim_statement | victim | Breach notifications submitted by the affected organisation |
| ncsc.gov.uk | NCSC-UK / National Cyber Security Centre | government | undisclosed | governmental | Advisories, malware analysis reports |
| nationalcrimeagency.gov.uk | National Crime Agency / NCA | government | undisclosed | governmental | Law enforcement announcements |
| ico.org.uk | Information Commissioner's Office / ICO | government | undisclosed | governmental | Enforcement notices |
| bsi.bund.de | BSI / Bundesamt für Sicherheit in der Informationstechnik | government | undisclosed | governmental | Warnings and annual report |
| verfassungsschutz.de | BfV / Bundesamt für Verfassungsschutz | government | undisclosed | governmental | Cyber-Brief publications |
| cert.ssi.gouv.fr | ANSSI / CERT-FR | government | ir_engagement | governmental | CTI reports and alerts |
| cyber.gouv.fr | ANSSI | government | undisclosed | governmental | Publications |
| cyber.gov.au | ACSC / Australian Cyber Security Centre / Australian Signals Directorate / ASD | government | undisclosed | governmental | Advisories and annual threat report |
| cyber.gc.ca | CCCS / Canadian Centre for Cyber Security | government | undisclosed | governmental | Advisories and assessments |
| ncsc.nl | NCSC-NL / Nationaal Cyber Security Centrum | government | undisclosed | governmental | Advisories |
| aivd.nl | AIVD | government | undisclosed | governmental | Public reports, some joint with MIVD |
| kisa.or.kr | KISA / Korea Internet and Security Agency | government | undisclosed | governmental | Reports and notices |
| krcert.or.kr | KrCERT/CC | government | ir_engagement | governmental | Incident analysis reports |
| jpcert.or.jp | JPCERT/CC / JPCERT | government | ir_engagement | independent | Incident analysis under blogs.jpcert.or.jp. A coordination centre, not a government agency |
| npa.go.jp | National Police Agency of Japan | government | undisclosed | governmental | Attribution statements and alerts |
| cert.gov.ua | CERT-UA | government | ir_engagement | governmental | Incident reports |
| cert.pl | CERT Polska / CERT.PL | government | ir_engagement | governmental | Incident and malware analysis |
| ncsc.govt.nz | NCSC-NZ | government | undisclosed | governmental | Advisories |
| csa.gov.sg | Cyber Security Agency of Singapore / CSA | government | undisclosed | governmental | Advisories |
| enisa.europa.eu | ENISA | government | osint | governmental | Threat landscape reports |
| cert.europa.eu | CERT-EU | government | osint | governmental | Threat briefs and advisories |
| europol.europa.eu | Europol | government | undisclosed | governmental | Operation announcements, IOCTA |
| cert-in.org.in | CERT-In | government | undisclosed | governmental | Advisories |
| ccn-cert.cni.es | CCN-CERT | government | undisclosed | governmental | Reports and alerts |
| ncsc.admin.ch | NCSC-CH / Swiss National Cyber Security Centre | government | undisclosed | governmental | Reports |
| cfcs.dk | Centre for Cyber Security Denmark / CFCS | government | undisclosed | governmental | Threat assessments |
| nsm.no | NSM / Norwegian National Security Authority | government | undisclosed | governmental | Reports |
| nukib.gov.cz | NUKIB | government | undisclosed | governmental | Warnings and reports |
| ncsc.gov.ie | NCSC-IE | government | undisclosed | governmental | Advisories |

## Press

| domain | organisation | type | access_profile | interest | notes |
|---|---|---|---|---|---|
| thehackernews.com | The Hacker News | press | osint | commercial | Usually links the primary in the first three paragraphs |
| bleepingcomputer.com | BleepingComputer | press | osint | commercial | Usually links the primary in the first three paragraphs. Also publishes original reporting from victim and actor contact |
| gbhackers.com | GBHackers / GBHackers on Security | press | osint | commercial | Often links another news article or nothing |
| cybersecuritynews.com | Cyber Security News | press | osint | commercial | Often links another news article or nothing |
| cyberpress.org | Cyber Press | press | osint | commercial | Often links another news article or nothing |
| securityweek.com | SecurityWeek | press | osint | commercial | Usually links the primary |
| therecord.media | The Record / Recorded Future News | press | osint | commercial | Usually links the primary. Owned by Recorded Future |
| darkreading.com | Dark Reading | press | osint | commercial | Frequently quotes vendor researchers directly |
| cyberscoop.com | CyberScoop | press | osint | commercial | Government and policy reporting |
| securityaffairs.com | Security Affairs | press | osint | commercial | |
| helpnetsecurity.com | Help Net Security | press | osint | commercial | |
| infosecurity-magazine.com | Infosecurity Magazine | press | osint | commercial | |
| scworld.com | SC Media / SC World | press | osint | commercial | |
| theregister.com | The Register | press | osint | commercial | |
| arstechnica.com | Ars Technica | press | osint | commercial | |
| wired.com | WIRED | press | osint | commercial | Original reporting with named and unnamed sources |
| techcrunch.com | TechCrunch | press | osint | commercial | Original reporting from victim contact |
| zdnet.com | ZDNET | press | osint | commercial | |
| csoonline.com | CSO Online | press | osint | commercial | |
| hackread.com | Hackread | press | osint | commercial | Reports forum and leak-site postings |
| cybernews.com | Cybernews | press | osint | commercial | Also publishes its own research team's findings |
| databreaches.net | DataBreaches.net | press | osint | independent | Reports from victim and actor contact |
| krebsonsecurity.com | KrebsOnSecurity / Brian Krebs | press | osint | independent | Original investigative reporting |
| 404media.co | 404 Media | press | osint | commercial | Original reporting |
| news.risky.biz | Risky Business News / Risky Bulletin | press | osint | commercial | Newsletter summarising other reporting |
| govinfosecurity.com | GovInfoSecurity / ISMG | press | osint | commercial | |
| bankinfosecurity.com | BankInfoSecurity / ISMG | press | osint | commercial | |
| computerweekly.com | Computer Weekly | press | osint | commercial | |
| thecyberexpress.com | The Cyber Express | press | osint | commercial | Owned by Cyble |
| heise.de | heise online | press | osint | commercial | |
| reuters.com | Reuters | press | osint | commercial | Original reporting with named and unnamed sources |
| bloomberg.com | Bloomberg | press | osint | commercial | Original reporting with named and unnamed sources |
| wsj.com | The Wall Street Journal | press | osint | commercial | Original reporting with named and unnamed sources |
| nytimes.com | The New York Times | press | osint | commercial | Original reporting with named and unnamed sources |
| washingtonpost.com | The Washington Post | press | osint | commercial | Original reporting with named and unnamed sources |
| bbc.com | BBC News / BBC | press | osint | independent | |
| bbc.co.uk | BBC News / BBC | press | osint | independent | |
| theguardian.com | The Guardian | press | osint | commercial | |

## Aggregators and reference sites

| domain | organisation | type | access_profile | interest | notes |
|---|---|---|---|---|---|
| news.ycombinator.com | Hacker News (Y Combinator) | aggregator | osint | independent | Link aggregation and comments. Not The Hacker News |
| reddit.com | Reddit | aggregator | osint | independent | Link aggregation and user posts |
| securityboulevard.com | Security Boulevard | aggregator | osint | commercial | Syndicates vendor and blogger posts; follow through to the original |
| otx.alienvault.com | AlienVault OTX / LevelBlue OTX | aggregator | osint | commercial | Community pulses, usually derived from a published report |
| ransomware.live | Ransomware.live | aggregator | actor_statement | independent | Scrapes leak sites; content is the actor's own claim |
| ransomlook.io | RansomLook | aggregator | actor_statement | independent | Scrapes leak sites; content is the actor's own claim |
| attack.mitre.org | MITRE ATT&CK | aggregator | osint | independent | not a primary: reference knowledge base citing published reports |
| malpedia.caad.fkie.fraunhofer.de | Malpedia | aggregator | osint | independent | not a primary: reference library citing published reports |
| cve.org | CVE Program | aggregator | osint | independent | not a primary: identifier records |
| vx-underground.org | vx-underground | aggregator | osint | independent | Sample and paper collection |
| github.com | GitHub | aggregator | undisclosed | independent | Hosts repositories from many authors; the repository owner is the source |
| en.wikipedia.org | Wikipedia | aggregator | osint | independent | not a primary: encyclopaedia |

## Social platforms

| domain | organisation | type | access_profile | interest | notes |
|---|---|---|---|---|---|
| x.com | X | social | undisclosed | independent | The account holder is the source |
| twitter.com | X (Twitter) | social | undisclosed | independent | The account holder is the source |
| linkedin.com | LinkedIn | social | undisclosed | independent | The account holder is the source |
| bsky.app | Bluesky | social | undisclosed | independent | The account holder is the source |
| infosec.exchange | Infosec Exchange (Mastodon) | social | undisclosed | independent | The account holder is the source |
| t.me | Telegram | social | undisclosed | independent | The channel owner is the source. Actor-run channels are actor statements |
| youtube.com | YouTube | social | undisclosed | independent | The channel owner is the source |
| medium.com | Medium | social | undisclosed | independent | The author is the source |
| substack.com | Substack | social | undisclosed | independent | The author is the source |

## Researchers and non-profits

| domain | organisation | type | access_profile | interest | notes |
|---|---|---|---|---|---|
| citizenlab.ca | Citizen Lab / The Citizen Lab | researcher | sample_analysis | independent | Forensic investigations of targeted surveillance |
| securitylab.amnesty.org | Amnesty International Security Lab / Amnesty Tech | researcher | sample_analysis | independent | Forensic investigations of targeted surveillance |
| accessnow.org | Access Now | researcher | sample_analysis | independent | Digital Security Helpline case reporting |
| bellingcat.com | Bellingcat | researcher | osint | independent | Open source investigations |
| thedfirreport.com | The DFIR Report | researcher | telemetry | independent | Intrusion case reports |
| isc.sans.edu | SANS Internet Storm Center / SANS ISC | researcher | telemetry | independent | Handler diaries, honeypot data |
| shadowserver.org | The Shadowserver Foundation / Shadowserver | researcher | telemetry | independent | Internet-wide scanning and sinkhole data |
| abuse.ch | abuse.ch | researcher | sample_analysis | independent | Community-submitted samples and indicators |
| spamhaus.org | The Spamhaus Project / Spamhaus | researcher | telemetry | independent | Reputation data and botnet reporting |
| malware-traffic-analysis.net | Malware-Traffic-Analysis.net | researcher | sample_analysis | independent | Infection traffic captures |
| doublepulsar.com | Kevin Beaumont / DoublePulsar | researcher | osint | independent | Independent researcher blog |
| objective-see.org | Objective-See / Patrick Wardle | researcher | sample_analysis | independent | macOS malware analysis |
| troyhunt.com | Troy Hunt | researcher | osint | independent | Breach data analysis |
| haveibeenpwned.com | Have I Been Pwned | researcher | osint | independent | Breach corpus records |
| blog.bushidotoken.net | BushidoToken | researcher | osint | independent | Independent researcher blog |
| curatedintel.org | Curated Intelligence | researcher | osint | independent | Community research group |
| eff.org | Electronic Frontier Foundation / EFF | researcher | sample_analysis | independent | Threat Lab research |
