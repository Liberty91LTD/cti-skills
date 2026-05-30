---
name: ip-investigation
description: Use when a user asks to investigate, check, enrich, or characterize an IP address (IPv4 or IPv6). Chains VirusTotal, Shodan, AbuseIPDB, GreyNoise, OTX, and optionally Censys in parallel, then consolidates findings and prioritizes follow-up IOCs. Invoked by /cti-orchestrator when the target is an IP.
metadata:
  version: 1.1.0
  tags: [investigation, composition, ip]
  tradecraft: true
---

# ip-investigation

Investigate an IP address end-to-end. Chain multiple `lookup-*` skills, consolidate results, prioritize follow-up IOCs, and return a rated investigation summary. You invoke skills — you don't call APIs directly.

**This skill invokes:** `/lookup-virustotal`, `/lookup-shodan`, `/lookup-abuseipdb`, `/lookup-greynoise`, `/lookup-otx`, optionally `/lookup-censys`, optionally `/lookup-reversinglabs` (network threat-intel + sample fan-out), optionally `/lookup-crowdstrike` (IOC reputation + actor/malware links), optionally `/lookup-misp` (internal correlation), then `/source-assessment`, `/tlp-guide`, `/confidence-levels`.

## When to invoke

- User asks to investigate, check, or enrich an IP
- User pastes an IP and asks "what is this?" / "is this malicious?"
- Another skill hands off an IP indicator for follow-up
- IOC triage pipeline

## Inputs

```yaml
indicator: <IPv4 or IPv6 address>
context: <optional — why is the user asking? where did this come from?>
tlp_ceiling: <optional — CLEAR/GREEN/AMBER/AMBER+STRICT/RED, default AMBER>
```

## Procedure

### 1. Validate + triage (before spending API quota)

- Reject RFC 1918 / loopback / link-local / documentation-range (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24) unless the user specifically asks — these are not public infrastructure and enrichment is wasted
- Check if the IP is already in `data/iocs/` — if yes, load existing enrichment and note age
- Decide whether to include Censys (skip by default due to 250/month quota)

### 2. Parallel lookups

Invoke in parallel (agents should batch these calls):

```
/lookup-greynoise ip <value>    # FAST — filter out noise early
/lookup-virustotal ip <value>   # reputation aggregate
/lookup-abuseipdb ip <value>    # abuse reports
/lookup-shodan ip <value>       # infrastructure fingerprint
/lookup-otx ip <value>          # community pulses
```

**Add to the same parallel batch if credentials are configured**:
```
/lookup-reversinglabs ip <value>                 # if $REVERSINGLABS_USER is set. Network reputation from RL's malware-analysis corpus — files seen contacting this IP, RL classification. One API call, no pivot fan-out.
/lookup-crowdstrike indicator <value>            # if $CROWDSTRIKE_CLIENT_ID is set. Falcon Intel view — malicious confidence, linked actors + malware families, report refs. One API call.
/lookup-misp search-attributes --value <value>   # if $MISP_URL + $MISP_KEY are set. Internal correlation against your own catalogued events.
```

Optionally add (escalation — separate API budget):
```
/lookup-censys ip <value>                                                # ONLY if Shodan insufficient + quota available
/lookup-reversinglabs ip <value> --pivot files,domains,urls --max-results 25
# only when you want sample fan-out from the IP — each --pivot entry is a separate API call
```

### 3. Short-circuit on noise

If GreyNoise returns `noise: true` and `classification: benign`, AND AbuseIPDB confidence <10, this is likely mass-scanning background noise. Summarize briefly and stop — no need to burn full analysis on it. Note: `noise: true` with `classification: malicious` is still interesting (opportunistic attacker infrastructure).

### 4. Consolidate

Build a unified view:

```yaml
indicator: <ip>
type: ipv4 | ipv6
consolidated_verdict: malicious | suspicious | clean | benign-noise | unknown
detection_signals:
  - source: virustotal
    detection_ratio: <X/Y>
    verdict: <...>
  - source: abuseipdb
    abuse_confidence: <0-100>
    recent_reports: <count>
  - source: greynoise
    noise: <bool>
    riot: <bool>
    classification: <...>
infrastructure:
  asn: <...>
  org: <...>
  country: <...>
  open_ports: <[...] from shodan>
  services: <top 5 from shodan>
  vulnerabilities: <CVE list>
  certificates: <present/absent>
community_context:
  pulse_count: <from otx>
  key_actors_attributed: <any pulse authors or malware families?>
pivot_candidates:
  - type: domain
    value: <hostname from shodan/vt>
    reason: <"resolves to this IP", "shares cert", etc.>
  - type: hash
    value: <communicating_files from vt>
    reason: <...>
```

### 5. Prioritize follow-up IOCs

Rank pivot candidates by investigative value:

1. **Certificate matches** (highest — strong infrastructure link)
2. **Communicating files** (medium-high — active C2 signal)
3. **Passive DNS resolutions** (medium — historical association)
4. **Recent WHOIS/registration overlaps** (medium)
5. **Generic ASN/org neighbors** (low)

Return the top 3-5 candidates to the invoking skill or orchestrator for optional deep-dive via `/domain-investigation`, `/hash-investigation`, or `/indicator-pivoting`.

### 6. Apply rigor

Before returning, chain:
- `/source-assessment` — rate each lookup result (defaults in each lookup skill's frontmatter)
- `/tlp-guide` — mark the investigation output (default AMBER)
- `/confidence-levels` — score the consolidated verdict (MISP 0-100)

### 7. Return

```yaml
title: "IP Investigation: <ip>"
tlp: AMBER
confidence: <0-100>
summary: <2-3 sentences>
verdict: <...>
detection_signals: <...>
infrastructure: <...>
community_context: <...>
pivot_candidates: <top 3-5>
source_ratings:
  virustotal: B2
  shodan: B2
  ...
investigation_date: <ISO8601>
recommended_next_steps:
  - <e.g., "pivot on domain X via /domain-investigation">
```

## When to stop

- GreyNoise benign-noise short-circuit (step 3)
- All lookups returned "not found" → report no signal; don't escalate
- Clear malicious verdict with high confidence → return; leave deeper pivots to the user

## Rate-limit awareness

Respect the lookup skills' own rate limits. Parallelizing 5 lookups on one IP = 5 API calls total, well within all free tiers. Don't loop over a list without throttling — use `/ioc-enrichment-workflow` for bulk.

## Related skills

- `/domain-investigation`, `/hash-investigation`, `/url-investigation` — sibling investigation skills
- `/indicator-pivoting` — deeper graph traversal from a starting IOC
- `/ioc-enrichment-workflow` — bulk IOC list enrichment
- `/threat-actor-profiling` — if the IP is attributed to a known actor, consider profiling
- `/cti-orchestrator` — typically the caller
