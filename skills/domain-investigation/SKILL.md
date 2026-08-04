---
name: domain-investigation
description: Use when a user asks to investigate, check, or characterize a domain or hostname. Chains VirusTotal, URLScan (search existing scans), Shodan (DNS resolve + host), OTX, ransomware.live (victim-status sweep), and optionally Censys. Returns reputation, resolution, hosting fingerprint, ransomware-claim status, and pivot candidates. Invoked by /cti-orchestrator when the target is a domain.
metadata:
  version: 1.2.0
  tags: [investigation, composition, domain]
  tradecraft: true
---

# domain-investigation

Investigate a domain or hostname end-to-end. Chain `lookup-*` skills, consolidate, prioritize follow-up IOCs, and return a rated investigation summary.

**This skill invokes:** `/lookup-liberty91` (first-party — run first), `/lookup-virustotal`, `/lookup-urlscan`, `/lookup-shodan`, `/lookup-otx`, `/lookup-ransomwarelive`, optionally `/lookup-censys`, optionally `/lookup-reversinglabs` (network threat-intel from RL malware corpus), optionally `/lookup-crowdstrike` (IOC reputation + actor/malware links), optionally `/lookup-misp` and/or `/lookup-opencti` (internal correlation), optionally `/lookup-sentinel` (exposure check in your own telemetry), then `/source-assessment`, `/tlp-guide`, `/confidence-levels`.

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
/lookup-ransomwarelive search --q <org-candidate>   # victim-status sweep
```

For the ransomware.live sweep, derive an `org-candidate` from the domain by stripping the public suffix and any common subdomains (`www.acme-corp.com` → `acme-corp` or `acme corp`). If the apex contains a hyphen or dot, also try the first label alone. The PRO tier returns the full match set in one call (no pagination), so two candidate queries cost at most two of the 3000-call daily budget.

**Add to the same parallel batch if credentials are configured**:
```
/lookup-reversinglabs domain <domain>            # if $REVERSINGLABS_USER is set. Network reputation from RL's malware-analysis corpus — files seen resolving / contacting this domain, RL classification. One API call.
/lookup-crowdstrike indicator <domain>           # if $CROWDSTRIKE_CLIENT_ID is set. Falcon Intel view — malicious confidence, linked actors + malware families, report refs. One API call.
/lookup-liberty91 ioc-lookup <domain>            # if $LIBERTY91_API_KEY is set. First-party — run first: does your own platform already hold this domain, with what verdict, confidence and TLP?
/lookup-misp search-attributes --value <domain>  # if $MISP_URL + $MISP_KEY are set. Internal correlation against your own catalogued events.
/lookup-opencti lookup <domain>                  # if $OPENCTI_URL + $OPENCTI_TOKEN are set. Internal correlation against your OpenCTI knowledge base (observables + indicators in one call).
```

Optionally (escalation):
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
ransomware_status:
  matched_total: <n>             # total leak-site claims matching org-candidate
  high_confidence_matches:       # only entries where website OR title clearly maps to the domain
    - victim_id: <...>
      title: <...>
      group: <ransomware group>
      country: <CC>
      sector: <...>
      published: <ISO date>
      website: <victim website if present>
      description_excerpt: <first 200 chars — quote sparingly, criminal-written>
      permalink: <ransomware.live record URL>
  notes: <attribution caveat — name collisions are common, e.g. "Acme" is many companies>
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

### 4b. Exposure check — was it seen in OUR environment? (if Sentinel is configured)

If `$SENTINEL_WORKSPACE_ID` + app credentials are set and the verdict is malicious or suspicious, chain `/lookup-sentinel` to sweep the domain across the workspace's *available* tables (`DeviceNetworkEvents` RemoteUrl, `DnsEvents`, `CommonSecurityLog`, `EmailUrlInfo`, … — that skill discovers what exists before querying). Report hits with first/last seen and affected devices/accounts; report a miss as "not observed in collected telemetry over <window>", never "not compromised".

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

### Ransomware-claim hits — handle with care

A match in `ransomware_status` does **not** prove the queried domain's owner has been breached. Validate before reporting:

1. **Cross-check the `website` field on the victim record.** If it contains the queried domain (or its apex), confidence is high. If it's blank or a different domain, treat as a possible name collision.
2. **Common-name collisions.** Generic apex strings (`acme`, `apple`, `delta`, `chase`) match many unrelated organisations. Always inspect 2–3 top results manually rather than trusting `matched_total` alone.
3. **Credibility split.** Per `/lookup-ransomwarelive`, group attribution + dates are B2 (probably true), but the criminal-written `description` field is B3–B4 (often inflated). Quote selectively and never present a leak-site claim as a confirmed breach without independent corroboration.
4. **No-hit doesn't mean clean.** Ransomware.live only tracks public *leak-site* claims. Quietly-paid victims and intrusions that didn't escalate to extortion never appear.

## Related skills

- `/ip-investigation`, `/url-investigation`, `/hash-investigation`
- `/indicator-pivoting` — deeper graph pivoting
- `/threat-actor-profiling` — if domain attributes to a known actor (use `/lookup-ransomwarelive group-profile` for ransomware groups)
- `/ransomware-ecosystem` — knowledge cell to consult when a victim hit lands
- `/cti-orchestrator`
