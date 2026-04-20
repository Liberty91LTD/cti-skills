---
name: domain-investigation
description: Use when a user asks to investigate, check, or characterize a domain or hostname. Chains VirusTotal, URLScan (search existing scans), Shodan (DNS resolve + host), OTX, and optionally Censys. Returns reputation, resolution, hosting fingerprint, and pivot candidates. Invoked by /cti-orchestrator when the target is a domain.
metadata:
  version: 1.0.0
  tags: [investigation, composition, domain]
  tradecraft: true
---

# domain-investigation

Investigate a domain or hostname end-to-end. Chain `lookup-*` skills, consolidate, prioritize follow-up IOCs, and return a rated investigation summary.

**This skill invokes:** `/lookup-virustotal`, `/lookup-urlscan`, `/lookup-shodan`, `/lookup-otx`, optionally `/lookup-censys`, then `/source-assessment`, `/tlp-guide`, `/confidence-levels`.

## When to invoke

- User asks to investigate, check, or enrich a domain / hostname
- User pastes a suspicious domain and asks "what is this?"
- `/url-investigation` hands off the parent domain for deeper context
- `/ip-investigation` surfaced a hostname worth investigating

## Inputs

```yaml
indicator: <domain or hostname>
context: <optional>
tlp_ceiling: <optional, default AMBER>
```

## Procedure

### 1. Validate + triage

- Confirm it parses as a valid domain (reject IPs, URLs — route those to the right skill)
- Check for obvious false positives (top 1M domains, your own infrastructure)
- Check `data/iocs/` for prior enrichment

### 2. Parallel lookups

```
/lookup-virustotal domain <value>    # reputation + WHOIS-ish
/lookup-urlscan domain <value>       # existing scans (search, not submit)
/lookup-shodan domain <value>        # DNS resolve + host fingerprint of the resolved IP
/lookup-otx domain <value>           # community pulses + passive DNS
```

Optionally:
```
/lookup-censys search "services.tls.certificates.leaf_data.subject.common_name: <domain>"
# ONLY if certificate pivoting is valuable; costs a query credit
```

### 3. Consolidate

```yaml
indicator: <domain>
type: domain
consolidated_verdict: malicious | suspicious | clean | unknown
reputation:
  vt_detection_ratio: <X/Y>
  vt_categories: [<list>]
  otx_pulse_count: <n>
registration:
  registrar: <...>
  creation_date: <...>
  age_days: <calc>
dns:
  resolved_ip: <...>
  passive_dns: [<historical resolutions>]
  ns: [<name servers>]
hosting:
  asn: <from shodan on resolved ip>
  org: <...>
  country: <...>
  certificates: <present/absent, recent renewal?>
content:
  urlscan_verdict: <from existing scans>
  urlscan_screenshot: <URL if available>
community_context:
  pulse_count: <...>
  malware_families: [<...>]
  attributed_actors: [<...>]
pivot_candidates:
  - type: ip
    value: <resolved_ip>
    reason: resolves_to
  - type: domain
    value: <cert_sibling>
    reason: shares_tls_cert
  - type: hash
    value: <communicating_file>
    reason: downloaded_from
```

### 4. Prioritize pivots

1. **Resolved IP** (always — then `/ip-investigation` on it if suspicious)
2. **TLS certificate siblings** (strong infrastructure link)
3. **Newly-registered-domain clusters** (if created_date <30 days + similar TLD/pattern)
4. **Communicating files from VT** (medium)
5. **Passive DNS neighbors** (low-medium)

### 5. Apply rigor

Chain:
- `/source-assessment`
- `/tlp-guide`
- `/confidence-levels`

### 6. Return

```yaml
title: "Domain Investigation: <domain>"
tlp: AMBER
confidence: <0-100>
summary: <2-3 sentences>
verdict: <...>
reputation: <...>
registration: <...>
dns: <...>
hosting: <...>
content: <...>
community_context: <...>
pivot_candidates: <top 3-5>
source_ratings: <...>
investigation_date: <ISO8601>
recommended_next_steps: <...>
```

## Special cases

- **Newly-registered domains (<7 days)** — very common in phishing campaigns; flag even if low reputation score yet. Pivot aggressively to find sibling domains.
- **Parked/sinkhole domains** — URLScan will show a parking page; don't treat as malicious automatically.
- **Subdomain of a known CDN** (e.g., `xyz.cloudfront.net`) — the interesting data is the hostname pattern + what it fronts, not the CDN itself.

## Related skills

- `/ip-investigation`, `/url-investigation`, `/hash-investigation`
- `/indicator-pivoting` — deeper graph pivoting
- `/threat-actor-profiling` — if domain attributes to a known actor
- `/cti-orchestrator`
