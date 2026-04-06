---
name: osint-methodology
description: Structured OSINT collection methodology. Planning, collection techniques, search operators, and documentation. Loaded by the osint-researcher agent.
user-invocable: false
metadata:
  version: 1.0.0
---

# OSINT Collection Methodology

## Collection Planning

Before collecting, define:
1. **Objective**: What specific intelligence do we need?
2. **Scope**: What sources are relevant? What's out of scope?
3. **Keywords**: Search terms, aliases, IOCs to look for
4. **Time constraints**: How recent must the intelligence be?
5. **Documentation**: How will findings be recorded?

## Source Categories

| Category | Sources | Best For |
|----------|---------|----------|
| **Government advisories** | CISA, NCSC, CERT-EU, national CERTs | Authoritative threat alerts, vulnerability warnings |
| **Vendor reports** | Mandiant, CrowdStrike, Microsoft, Recorded Future, Talos | Campaign analysis, actor profiles, malware analysis |
| **Security research** | Blogs, conference talks, academic papers | Novel techniques, deep dives, vulnerability research |
| **Underground** | Forum mirrors, paste sites, Telegram (public), leak aggregators | Threat actor communications, credential dumps, tools |
| **Code repositories** | GitHub, GitLab | Malware source, PoC exploits, attacker tools, leaked configs |
| **Certificate transparency** | crt.sh, Censys | Domain enumeration, infrastructure mapping |
| **DNS/WHOIS** | SecurityTrails, DomainTools, RiskIQ (via web search) | Infrastructure relationships, historical records |
| **News/media** | Tech press, infosec news sites | Incident reports, geopolitical context |
| **Social media** | X/Twitter, LinkedIn, Reddit (public) | OPSEC failures, community intelligence, actor claims |

## Search Operator Cheat Sheet

### Google Dorks
```
site:example.com filetype:pdf         # PDFs on a specific site
"threat actor" AND "APT28" -site:reddit.com  # Exclude noise
inurl:"/wp-content/uploads/" filetype:exe    # Exposed uploads
"index of" "/backup"                   # Directory listings
intitle:"login" site:*.example.com     # Login pages on subdomains
```

### GitHub Search
```
org:target-org password                # Leaked credentials
filename:.env DB_PASSWORD              # Exposed environment files
"api_key" language:python              # Hardcoded API keys
"BEGIN RSA PRIVATE KEY"                # Exposed private keys
```

### Certificate Transparency (crt.sh)
```
https://crt.sh/?q=%.example.com        # All certs for subdomains
https://crt.sh/?q=example.com&output=json  # JSON output
```

### Shodan Dorks (via web)
```
ssl.cert.subject.cn:"example.com"      # Certificates for domain
http.title:"Dashboard" org:"Target"    # Web dashboards
product:"Cobalt Strike"                # C2 servers
```

## Collection Process

### 1. Broad Sweep
Start with broad searches to understand what's available:
- Search for the topic/actor/indicator across major sources
- Note the quantity and quality of available information
- Identify the most promising sources for deeper collection

### 2. Targeted Collection
Narrow down to specific sources and extract detailed intelligence:
- Read full reports, not just headlines
- Extract specific IOCs, TTPs, dates, and attribution claims
- Note each source's perspective and potential biases

### 3. Source Assessment
Apply Admiralty Scale to every finding (per source-assessment skill):
- Rate source reliability (A-F)
- Rate information credibility (1-6)
- Note whether information is corroborated across sources

### 4. Documentation
Record every finding with full attribution:
```markdown
#### Finding: [Title]
- **Source**: [URL or description]
- **Source rating**: [Admiralty code, e.g., B2]
- **Date collected**: YYYY-MM-DD
- **Date of information**: YYYY-MM-DD (when was this information produced?)
- **Summary**: [Key intelligence extracted]
- **Relevance**: [How this relates to the collection objective]
```

## Ethical and Legal Boundaries
- Only access publicly available information
- Do not create fake accounts or impersonate anyone
- Do not attempt to access restricted systems
- Respect robots.txt and terms of service
- Be aware of data protection regulations (GDPR)
- Do not engage with threat actors or participate in illegal activity
