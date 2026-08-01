---
name: indicator-pivoting
description: Indicator pivoting methodology — how to use one known indicator to discover related infrastructure across the IOC graph. Decision tree by indicator type with concrete `/lookup-*` commands per pivot, a worked multi-hop example, pivot-quality scoring, and routing into the rigor pipeline. Use when the user asks "what else is connected to this IP / domain / hash / cert / actor?", needs to expand a single seed IOC into a campaign cluster, or wants the canonical reference for graph-walking IOCs.
user-invocable: true
metadata:
  version: 2.0.0
  tags: [investigation, pivoting, composition, tradecraft]
  tradecraft: true
---

# Indicator Pivoting

Pivoting is the art of using one known indicator to discover related infrastructure, expanding a single seed into an understanding of an adversary's wider operations. Each pivot is a directed-graph walk: the node is an indicator (typed), the edge is a relation derived from a lookup, and the cost is one or more API calls plus the analyst time to interpret the result.

This skill is the canonical "how to walk the IOC graph" reference. The four investigation skills (`/ip-investigation`, `/domain-investigation`, `/hash-investigation`, `/url-investigation`) chain a fixed set of lookups for a known seed type; this skill takes over when you need to keep walking past their first-hop output.

**This skill invokes:** `/lookup-liberty91`, `/lookup-virustotal`, `/lookup-otx`, `/lookup-shodan`, `/lookup-censys`, `/lookup-urlscan`, `/lookup-abuseipdb`, `/lookup-greynoise`, `/lookup-misp`, `/lookup-opencti`, `/lookup-ransomwarelive`, `/lookup-crowdstrike`, `/lookup-reversinglabs`; then `/score-source`, `/apply-tlp`, `/confidence-language`. May hand off to `/threat-actor-profiling`, `/campaign-tracking`, `/malware-analysis`, `/yara-writing`, `/sigma-writing`, `/darkweb-collection`.

## When to invoke

- The user has a single seed IOC and asks "what else is related to this?"
- An investigation skill returned `pivot_candidates` and you need to walk further than its routing did
- You suspect a campaign cluster (multiple indicators in incident telemetry) and want to confirm common infrastructure
- A threat-actor profile mentions an indicator and you want to see the wider footprint
- You need to clearly document a pivot chain so a reviewer can trace your reasoning end-to-end

## Pivot decision trees, with the commands to run

For each starting indicator type: a tree of pivots, then the concrete commands. The `/lookup-*` form is the skill-invocation; the `python3 tools/clis/...` form is the underlying CLI. Both are equivalent — pick whichever the surrounding context demands.

### Starting from an IP address

```
IP address
├── Reputation (cheap, parallel first)
│   ├── /lookup-virustotal ip <ip>
│   ├── /lookup-abuseipdb (abuse + categories)
│   └── /lookup-greynoise (noise/scanner classification — filters out internet-wide scanners)
├── Service fingerprint
│   ├── /lookup-shodan host <ip>          → ports, banners, products, vulns, hostnames
│   └── /lookup-censys host <ip>          → richer service detail, certificate chain, CPE
├── DNS pivots
│   ├── /lookup-shodan dns reverse <ip>   → reverse-DNS hostname(s)
│   ├── /lookup-virustotal ip <ip> --relationships resolutions  → passive-DNS history
│   └── /lookup-otx ip <ip>               → community-reported domains for this IP
├── Cert pivots
│   ├── /lookup-shodan host <ip>          → cert SHA1 in the banner blob
│   └── /lookup-censys host <ip>          → cert fingerprint(s) → pivot to other hosts
├── JARM / TLS-fingerprint pivots
│   └── /lookup-shodan search 'ssl.jarm:"<jarm>"'   → other hosts with same JARM (often C2 family)
├── Range pivots (use sparingly — high false-positive risk)
│   └── /lookup-shodan search 'net:<cidr>'          → neighbours in same /24
└── Malware pivots
    └── /lookup-virustotal ip <ip> --relationships communicating_files,downloaded_files
```

**Concrete commands:**

```bash
# Reputation triple
python3 tools/clis/virustotal.py ip 185.220.101.45
python3 tools/clis/abuseipdb.py check 185.220.101.45 --verbose
python3 tools/clis/greynoise.py ip 185.220.101.45

# Service fingerprint
python3 tools/clis/shodan.py host 185.220.101.45 --history
python3 tools/clis/censys.py host 185.220.101.45 --at-time 2026-04-01T00:00:00Z

# Passive DNS + community
python3 tools/clis/virustotal.py ip 185.220.101.45 --relationships resolutions,communicating_files
python3 tools/clis/otx.py ip 185.220.101.45

# JARM-pivot to find C2 siblings
python3 tools/clis/shodan.py search 'ssl.jarm:"3fd21b20d00000021c43d21b21b43d41226ab2434c2cd1a5e1b3c2bc5f4f4e7"'
```

### Starting from a domain

```
Domain
├── Reputation (parallel)
│   ├── /lookup-virustotal domain <d>           → detection ratio + categories + WHOIS-ish
│   ├── /lookup-otx domain <d>                  → pulses + passive DNS
│   └── /lookup-urlscan domain <d>              → existing scans (don't re-submit by default)
├── DNS resolution (always)
│   ├── /lookup-shodan dns resolve <d>          → current A/AAAA records
│   └── /lookup-virustotal domain <d> --relationships resolutions  → historical
│       └── pivot the resolved IPs as IPs (above)
├── Subdomain enumeration
│   ├── /lookup-shodan dns domain <d>           → subdomains Shodan knows about
│   └── /lookup-censys search 'names: <d>'      → CT-derived names (paid plan only)
├── Certificate transparency
│   ├── /lookup-censys search 'services.tls.certificates.leaf_data.subject.common_name:<d>'
│   │   → other hosts presenting a cert for this name
│   └── /lookup-virustotal domain <d>           → cert SAN list in the response
│       └── cert SAN siblings → pivot each as a domain
├── WHOIS / registrant
│   └── /lookup-virustotal domain <d>           → registrar, creation_date, registrant_email if not redacted
│       └── registrant email → /lookup-virustotal search …  (paid VT Intel only)
│       └── reverse-WHOIS via vendor (DomainTools, WhoisXMLAPI) — outside the bundled lookups
├── Ransomware-claim sweep
│   └── /lookup-ransomwarelive search --q <org-candidate>
│       → derive org-candidate by stripping public suffix and `www.`; see /domain-investigation §3
└── Content
    └── /lookup-urlscan domain <d>              → screenshots, DOM, page tech
```

**Concrete commands:**

```bash
# Reputation + content
python3 tools/clis/virustotal.py domain evil.example.com
python3 tools/clis/otx.py domain evil.example.com
python3 tools/clis/urlscan.py search "domain:evil.example.com"

# DNS now + historical
python3 tools/clis/shodan.py dns resolve evil.example.com
python3 tools/clis/virustotal.py domain evil.example.com --relationships resolutions

# Cert-CN pivot (paid Censys plan)
python3 tools/clis/censys.py search 'services.tls.certificates.leaf_data.subject.common_name:"evil.example.com"'

# Ransomware-claim sweep
python3 tools/clis/ransomwarelive.py search --q "example"
```

### Starting from a URL

```
URL
├── Live scan (when a fresh capture is wanted)
│   └── /lookup-urlscan submit <url>            → DOM, network log, screenshot, verdict
├── Existing scans
│   └── /lookup-urlscan search 'page.url:<url>' → past captures (faster, no re-submit)
├── Reputation
│   └── /lookup-virustotal url <url>            → detection ratio + redirect chain
├── Hostname pivot
│   └── extract hostname → pivot as a domain (above)
└── Path/kit fingerprint
    └── /lookup-urlscan search 'page.url:"<distinctive-path>"'  → other URLs with same kit path
```

**Concrete commands:**

```bash
python3 tools/clis/urlscan.py submit "https://login-acme[.]net/secure/portal" --tags phishing
python3 tools/clis/urlscan.py search 'page.url:"/secure/portal/"'
python3 tools/clis/virustotal.py url "https://login-acme[.]net/secure/portal"
```

### Starting from a file hash

```
Hash (md5 / sha1 / sha256)
├── Reputation + family
│   ├── /lookup-virustotal file <hash>          → detection stats, family tags, sandbox verdicts
│   └── /lookup-otx file <hash>                 → community pulses, campaign attribution
├── C2 extraction (highest-value pivot)
│   └── /lookup-virustotal file <hash> --relationships contacted_ips,contacted_domains,contacted_urls
│       → pivot each contacted indicator
├── Family lineage
│   └── /lookup-virustotal file <hash> --relationships dropped_files,parent_files,similar_files
│       → walk dropper/payload chain
├── Submitter/source
│   └── /lookup-virustotal file <hash> --relationships submissions   (premium)
├── Compilation artefacts
│   └── /lookup-virustotal file <hash>          → response includes pdb_path, compiler, packers
│       → distinctive PDB path → /lookup-virustotal search …  (premium)
└── Internal correlation
    ├── /lookup-misp search-attributes --value <hash>   → events that already include this hash
    └── /lookup-opencti lookup <hash>                   → observables/indicators already in your knowledge base
```

**Concrete commands:**

```bash
# Detection + family
python3 tools/clis/virustotal.py file 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8

# C2 extraction (highest-value)
python3 tools/clis/virustotal.py file 5e884898... \
  --relationships contacted_ips,contacted_domains,contacted_urls --limit 25

# Family lineage
python3 tools/clis/virustotal.py file 5e884898... \
  --relationships dropped_files,parent_files,similar_files --limit 10

# OTX community attribution
python3 tools/clis/otx.py file 5e884898...

# Internal correlation via MISP / OpenCTI
python3 tools/clis/misp.py search-attributes --value 5e884898...
python3 tools/clis/opencti.py lookup 5e884898...
```

### Starting from a TLS certificate (SHA-256 or CN)

```
Certificate
├── Hosts presenting this cert
│   ├── /lookup-shodan search 'ssl.cert.fingerprint:<sha256>'    → IPs serving the cert
│   └── /lookup-censys search 'services.tls.certificates.leaf_data.fingerprint_sha256:<sha256>'
└── Other certs by same Subject
    └── /lookup-censys certs view <cert_id>     → issuer, validity, sibling SANs
```

**Concrete commands:**

```bash
python3 tools/clis/shodan.py search 'ssl.cert.fingerprint:"5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"'
python3 tools/clis/censys.py certs view 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
```

### Starting from a registrant email or org name

```
Registrant identity
├── Reverse-WHOIS (premium / outside the bundled lookups — DomainTools, WhoisXMLAPI, Constella)
├── Internal MISP correlation
│   └── /lookup-misp search-attributes --type whois-registrant-email --value <email>
└── Domains attributed to the same actor in OTX pulses
    └── /lookup-otx pulse-search "<registrant-email-or-org>"
```

### Starting from an actor name, malware family, or campaign label

```
Actor / family / campaign string
├── Ransomware group (if applicable)
│   ├── /lookup-ransomwarelive group <name>            → group profile, victims, IOCs
│   ├── /lookup-ransomwarelive iocs <name>             → IOC dump for this group
│   └── /lookup-ransomwarelive yara <name>             → YARA rules attributed to the group
├── Community pulses
│   └── /lookup-otx pulse-search "<actor-or-family>"   → IOCs from public pulses
├── MISP events
│   └── /lookup-misp search-events --tag "actor=<name>" → previously catalogued IOCs
├── OpenCTI knowledge base
│   └── /lookup-opencti search "<actor-or-family>"      → intrusion sets, malware, reports, campaigns; then `get <id>` for relationships
└── Surface-web mentions (forums + Telegram)
    └── /darkweb-collection (with selectors built from the actor's known aliases)
```

### Starting from a Telegram channel handle or onion mirror

```
Channel handle / .onion address
├── Telegram channel handle
│   └── scripts/telegram_monitor.py --once --channels @<handle>  --selectors-file <selectors>
│       → match channel content against your IOC selectors
└── .onion address
    └── scripts/onion_search.py --query "<distinctive substring>"
        → resolve other clearnet/onion mirrors that mention the same string
```

(See `/darkweb-collection` for OPSEC and access posture before running these.)

## Pivot quality scoring

Not all pivots are equal. Score each before reporting:

| Pivot | Confidence | False-positive risk | Why |
|---|---|---|---|
| C2 IP/domain extracted from a reverse-engineered sample | High | Low | Direct, sample-grounded |
| TLS cert SHA-256 reused across hosts | High | Low | Cert reuse is intentional; the actor pinned it |
| Cert subject CN reused across hosts | Medium-High | Low-Medium | CN can be reused legitimately on shared certs |
| JARM fingerprint match | Medium-High | Medium | Strong for unusual JARMs; weak for default-config tools |
| Passive DNS (domain → IP, current) | Medium-High | Low-Medium | Direct; check the dates |
| Passive DNS (domain → IP, historical only) | Medium | Medium | Stale; could pre-date the campaign |
| Same WHOIS registrant email | Medium | Medium | Many real users share an email across domains |
| Same name server | Low | High | Popular NS providers host millions of unrelated domains |
| Same /24 IP range | Low | High | Cloud and CDN sharing |
| Same registrar | Very low | Very high | Registrars are infrastructure; near-meaningless alone |
| Same JA3/JA3S TLS client fingerprint | Medium | Medium | Strong for custom clients; weak for OS-default stacks |
| Same MITRE technique | Very low | Very high | Technique-level overlap is not infrastructure overlap |

**Rule of thumb**: a pivot chain is only as strong as its weakest link. Three High pivots in series ≈ High overall. One High + two Mediums ≈ Medium. Anything with a Low link ≈ Low overall, regardless of length.

## Pivot routing — by goal

| Goal | First-choice lookup | Second |
|---|---|---|
| IP reputation | `/lookup-virustotal` | `/lookup-abuseipdb`, `/lookup-greynoise` |
| Filter out internet-wide scanners | `/lookup-greynoise` | — |
| Service banner / vuln view | `/lookup-shodan` | `/lookup-censys` (richer, slower) |
| Cert fingerprint pivot | `/lookup-censys` | `/lookup-shodan` |
| JARM pivot | `/lookup-shodan` | `/lookup-censys` |
| Passive DNS | `/lookup-virustotal` `--relationships resolutions` | `/lookup-otx` |
| Subdomain enumeration | `/lookup-shodan dns domain` | `/lookup-censys` (paid) |
| Live URL analysis | `/lookup-urlscan submit` | `/lookup-virustotal url` |
| Existing URL captures | `/lookup-urlscan search` | — |
| File reputation | `/lookup-virustotal` | `/lookup-otx`, `/lookup-reversinglabs hash` |
| Authoritative classification + MITRE ATT&CK mapping | `/lookup-reversinglabs report --detailed` | `/malware-analysis` |
| Pivot to siblings by malware family / threat name | `/lookup-reversinglabs search 'threatname:<name>'` | `/lookup-otx pulse-search` |
| Parent container / extracted children | `/lookup-reversinglabs containers` / `extracted` | — |
| C2 extraction from a hash | `/lookup-virustotal` `--relationships contacted_ips,contacted_domains,contacted_urls` | `/lookup-reversinglabs report --fields networkthreatintelligence` |
| Community/actor attribution | `/lookup-otx` | `/lookup-misp search-events --tag`, `/lookup-crowdstrike indicator` (actors + malware families linked to the IOC) |
| Actor → TTPs / reports / related infrastructure | `/lookup-crowdstrike actor "<name>"` then `ttps` / `reports --actor` | `/threat-actor-profiling` |
| Internal correlation against own catalogued IOCs | `/lookup-misp` | `/lookup-opencti lookup` (observables + indicators, then `get` for relationships) |
| First-party check before spending third-party quota | `/lookup-liberty91 ioc-lookup` | `/lookup-liberty91 threat-events --q <value>` for the occurrences the indicator appears in, then `threat-event <id> --section iocs` for its co-reported indicators |
| Actor or malware family → its wider footprint | `/lookup-liberty91 library <type> --name\|--alias` | then `entity <type> <id> --section related\|threat-events\|iocs` — `related` ranks co-occurring entities by shared occurrences |
| Ransomware-group profile / IOCs / YARA | `/lookup-ransomwarelive` | — |
| Ransomware-victim sweep on org name | `/lookup-ransomwarelive search --q` | — |
| Underground-forum / Telegram chatter | `/darkweb-collection` | — |

## Worked example — phish URL → APT cluster

A walkthrough of a realistic four-hop chain. Source rating in brackets.

**Seed.** `https://login-acme[.]net/secure/portal/login.html` reported by an internal user as a suspicious password-reset email. Source: internal phishing inbox (B2).

**Hop 1 — characterise the URL.**

```bash
python3 tools/clis/urlscan.py search 'page.url:"login-acme.net"'
python3 tools/clis/virustotal.py url "https://login-acme.net/secure/portal/login.html"
```

Result: URLScan shows two prior submissions in the last 14 days (both flagged phishing), screenshot is an Acme-cloned login page, JS posts credentials to `https://api.login-acme[.]net/auth`. VT detection ratio 12/89 — phishing. Pivot candidate: domain `login-acme.net` (B2).

**Hop 2 — domain → resolved IP and cert.**

```bash
python3 tools/clis/shodan.py dns resolve login-acme.net api.login-acme.net
python3 tools/clis/virustotal.py domain login-acme.net --relationships resolutions
```

Result: both names currently resolve to `198.51.100.42`; passive DNS shows the names appeared together on 2026-04-12 (10 days ago — newly weaponised). Pivot candidates: IP `198.51.100.42` (B2), creation cluster of `*.login-acme.net` subdomains.

**Hop 3 — IP → service fingerprint and cert SHA-256.**

```bash
python3 tools/clis/shodan.py host 198.51.100.42 --history
python3 tools/clis/censys.py host 198.51.100.42
python3 tools/clis/greynoise.py ip 198.51.100.42
```

Result: nginx on 443; TLS cert SHA-256 `8f3c…b22a` issued by Let's Encrypt for `login-acme.net`, `api.login-acme.net`, and **`accounts-globex[.]net`** (a separate brand). GreyNoise: not a known scanner — quiet host, consistent with phishing infra. Pivot candidate: domain `accounts-globex.net` (B2).

**Hop 4 — cert pivot: who else serves this cert?**

```bash
python3 tools/clis/censys.py search 'services.tls.certificates.leaf_data.fingerprint_sha256:"8f3c...b22a"'
python3 tools/clis/shodan.py search 'ssl.cert.fingerprint:"8f3c...b22a"'
```

Result: three more IPs in the same hosting AS serving the same cert, each with a Let's Encrypt cert covering a different `*-cloud[.]net` look-alike domain. Pattern: brand-impersonation phishing infrastructure templated by the same operator. Pivot candidate: cluster of 5 domains, 4 IPs, 1 cert (B2 — high-confidence cluster).

**Hop 5 — community/family attribution.**

```bash
python3 tools/clis/otx.py domain login-acme.net
python3 tools/clis/otx.py domain accounts-globex.net
python3 tools/clis/misp.py search-attributes --value 198.51.100.42
```

Result: both domains appear in a single OTX pulse from a vendor researcher dated 2026-04-15, attributed to a known credential-phishing kit ("BabyShark-Mailer-v3"). MISP returns one event with the IP from a sibling intrusion two weeks prior.

**Synthesis.** Five domains and four IPs sharing a single cert, all newly created in a 14-day window, served from one AS, attributed to a documented kit. Confidence: **High** (multiple High-rated pivots in series). Recommended action: block the cluster, hand off to `/threat-actor-profiling` for kit attribution and to `/lookup-misp create-event` to publish the cluster to your sharing community.

```yaml
seed: https://login-acme[.]net/secure/portal/login.html
investigation_date: 2026-04-28
chain:
  - hop: 1; type: url;    method: urlscan+vt;          confidence: High
  - hop: 2; type: domain; method: dns+passivedns;      confidence: High
  - hop: 3; type: ip;     method: shodan+censys+gn;    confidence: High
  - hop: 4; type: cert;   method: censys cert pivot;   confidence: High
  - hop: 5; type: actor;  method: otx+misp attribution; confidence: Medium-High
overall_confidence: High
cluster:
  domains: [login-acme.net, api.login-acme.net, accounts-globex.net, ...]
  ips:     [198.51.100.42, ...]
  certs:   [sha256:8f3c...b22a]
  family:  BabyShark-Mailer-v3
recommended_next:
  - /threat-actor-profiling for the kit operator
  - /lookup-misp create-event to publish
  - /sigma-writing for a detection rule on the kit's distinctive POST path
```

## Pivot documentation template

Record every hop. Future readers (and future-you) need the chain.

```markdown
## Pivot Chain: <seed indicator>

### Hop 1 — <indicator type> → <pivot type>
- **Method**: <tool/skill + subcommand>
- **Command**: `python3 tools/clis/<cli>.py <args>` (or `/lookup-… <args>`)
- **Result**: <one-line summary; numbers matter>
- **Pivot candidates produced**: [<list>]
- **Source rating**: <Admiralty A1-F6, see /score-source>
- **Confidence**: <High/Medium/Low — see scoring table>

### Hop 2 — …
…

### Synthesis
- **Cluster**: <indicators that hang together>
- **Overall confidence**: <weakest-link>
- **Recommended next**: <skill handoffs>
```

Apply `/score-source`, `/apply-tlp`, and `/confidence-language` before publishing the pivot chain as a finished product.

## Common pitfalls

- **Shared hosting / CDN false positives.** Many domains share IPs on Cloudflare, Fastly, AWS CloudFront. Same-IP pivots from a CDN range are nearly meaningless — check `/lookup-shodan host` for the org/ASN before treating same-IP as a relationship.
- **Privacy WHOIS.** Most public WHOIS is now redacted. The bundled `/lookup-virustotal domain` returns what's available; for unredacted reverse-WHOIS you need a paid vendor (DomainTools, WhoisXMLAPI, Constella).
- **Historical vs. current resolution.** A passive-DNS edge from 2022 is not evidence of the same operator's involvement in 2026. Check `passive_dns` dates and prefer recent edges.
- **Overcounting pivots.** A chain with one Low-confidence link is a Low-confidence chain regardless of length. Five Low pivots stacked do not become a High pivot.
- **Stopping too early.** The Hop-1 lookup almost never gives you the cluster — it gives you Hop-2 candidates. Budget for at least 3-4 hops on any non-trivial seed.
- **Letting cost decide direction.** Censys `search` and VT `--relationships submissions` cost credits/quota. Plan the pivot before paying the call; don't blow your budget enumerating noise.
- **Not recording rejected pivots.** A pivot you tried and discarded is just as important as one you kept. Record both.
- **Confusing infrastructure overlap with intent overlap.** Two campaigns can share infrastructure without being the same actor (rented hosting, leaked toolkit). Two campaigns can share TTPs without sharing infrastructure (commodity malware). Pivoting addresses infrastructure; attribution needs more.

## Related skills

- `/ip-investigation`, `/domain-investigation`, `/hash-investigation`, `/url-investigation` — first-hop chains; this skill takes over for deeper traversal
- `/lookup-liberty91`, `/lookup-virustotal`, `/lookup-shodan`, `/lookup-censys`, `/lookup-urlscan`, `/lookup-otx`, `/lookup-abuseipdb`, `/lookup-greynoise`, `/lookup-misp`, `/lookup-opencti`, `/lookup-ransomwarelive`, `/lookup-reversinglabs`, `/lookup-crowdstrike` — the underlying lookups
- `/darkweb-collection` — when the pivot leads off-network into forum / Telegram chatter
- `/threat-actor-profiling`, `/campaign-tracking` — what to do with the cluster once you have it
- `/malware-analysis`, `/yara-writing`, `/sigma-writing` — sample-grounded follow-ups to a hash pivot
- `/score-source`, `/apply-tlp`, `/confidence-language`, `/likelihood-language` — apply rigor to the finished pivot chain
- `/cti-orchestrator` — the default entry point that routes to investigation skills, which then hand off to this one
