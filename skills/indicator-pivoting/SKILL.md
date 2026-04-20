---
name: indicator-pivoting
description: Indicator pivoting methodology — how to pivot from one indicator to discover related infrastructure. Decision tree by indicator type.
user-invocable: true
metadata:
  version: 1.0.0
---

# Indicator Pivoting

Pivoting is the art of using one known indicator to discover related infrastructure, expanding your understanding of an adversary's operations.

## Pivot Decision Tree

### Starting from an IP Address
```
IP Address
├── Passive DNS → What domains resolved to this IP? (historical)
├── Reverse DNS → What hostname is configured?
├── Certificate → What TLS certificates does it serve?
│   └── Certificate CN/SAN → Other IPs using the same cert?
├── Port/Service fingerprint → Other IPs with identical service banners?
├── JARM fingerprint → Other IPs with same TLS fingerprint? (C2 detection)
├── WHOIS (for IP range) → Who owns this range? Other IPs in same /24?
├── Shared hosting → What other domains are on this IP?
└── Malware connections → What samples communicate with this IP?
```

### Starting from a Domain
```
Domain
├── DNS records → What IPs does/did it resolve to?
│   └── Those IPs → pivot as IP (above)
├── WHOIS → Registrant email, org, name server
│   └── Same registrant → other domains registered?
├── Certificate transparency → What certs exist for this domain?
│   └── Cert SANs → other domains on same cert?
├── Subdomains → Enumerate via CT logs, DNS brute force
├── Name servers → Other domains using same NS?
├── Passive DNS → Historical resolution changes
└── URL patterns → Known phishing kit paths, C2 URI patterns
```

### Starting from a File Hash
```
Hash
├── VirusTotal relations → Communicating IPs, contacted domains, dropped files
├── OSINT → Vendor reports mentioning this hash
├── OTX pulses → Related indicators from community
├── Malware family → Other samples from same family
│   └── Shared code/strings → Related variants
├── Compilation artifacts → PDB paths, compiler fingerprint
│   └── Same PDB path → other samples from same developer
├── C2 configuration → Extracted C2 addresses
│   └── C2 IPs/domains → pivot as IP/domain (above)
└── Infrastructure hosting → Where was this file hosted?
```

## Pivot Quality Assessment

Not all pivots are equally valuable. Assess each:

| Pivot Type | Confidence | Risk of False Connection |
|-----------|-----------|-------------------------|
| Certificate overlap (same cert on multiple IPs) | High | Low |
| Passive DNS (domain → IP historical) | Medium-High | Low-Medium |
| WHOIS registrant match | Medium | Medium (shared hosting, privacy services) |
| Port/service banner match | Low-Medium | High (common configs) |
| Same /24 IP range | Low | High (shared hosting) |
| Name server overlap | Low | High (popular NS providers) |
| Same malware family | Medium-High | Low |
| C2 extracted from sample | High | Low |

## Tool Agent Routing for Pivots

| Pivot Type | Tool Agent(s) |
|-----------|--------------|
| Passive DNS | virustotal-agent, otx-agent |
| Certificate transparency | censys-agent |
| WHOIS | virustotal-agent (domain), shodan-agent |
| Port/service fingerprint | shodan-agent, censys-agent |
| JARM fingerprint | censys-agent |
| Malware relations | virustotal-agent, otx-agent |
| IP reputation | abuseipdb-agent, greynoise-agent |

## Pivot Documentation

Record every pivot and its result:

```markdown
## Pivot Chain: [Starting Indicator]

### Pivot 1: [IP] → Passive DNS
- **Method**: Queried VT for historical DNS
- **Result**: Domain evil.example.com resolved to this IP (2026-01-15 to 2026-03-01)
- **Confidence**: High (direct DNS resolution)

### Pivot 2: evil.example.com → WHOIS
- **Method**: WHOIS lookup
- **Result**: Registered by admin@protonmail.com on 2025-12-01
- **Confidence**: Medium (could be privacy-aware legitimate user)

### Pivot 3: admin@protonmail.com → Reverse WHOIS
- **Method**: Searched for other domains by same registrant
- **Result**: Found 3 additional domains
- **Confidence**: Medium-High (same registrant, similar registration dates)
```

## Common Pitfalls
- **Shared hosting false positives**: Many domains share IPs on CDNs/cloud providers
- **Privacy WHOIS**: Registrant info hidden behind privacy services
- **Historical vs current**: Old DNS resolutions may not reflect current infrastructure
- **Overcounting pivots**: A pivot chain is only as strong as its weakest link
