---
name: url-investigation
description: Use when a user asks to scan, investigate, or characterize a URL. Submits to URLScan (unlisted by default), cross-references with VirusTotal and OTX, extracts the parent domain and resolved IP for follow-up investigation. Returns verdict, redirect chain, contacted infrastructure, and screenshot. Invoked by /cti-orchestrator when the target is a URL.
metadata:
  version: 1.1.0
  tags: [investigation, composition, url]
  tradecraft: true
---

# url-investigation

Investigate a URL end-to-end. Scan it live (URLScan), cross-reference reputation (VT, OTX), extract parent domain + resolved IP for sibling investigations.

**This skill invokes:** `/lookup-urlscan`, `/lookup-virustotal`, `/lookup-otx`, optionally `/lookup-reversinglabs` (network threat-intel from RL malware corpus), optionally `/lookup-crowdstrike` (IOC reputation + actor/malware links), optionally `/lookup-misp` and/or `/lookup-opencti` (internal correlation), optionally `/domain-investigation` and/or `/ip-investigation` for the parent/resolved infrastructure, then `/source-assessment`, `/tlp-guide`, `/confidence-levels`.

## When to invoke

- User asks to scan, check, or investigate a URL
- User pastes a suspicious link from a phishing email
- `/domain-investigation` or another skill hands off a specific URL for live-scan evidence

## Inputs

```yaml
indicator: <URL>
context: <optional — phishing email? user report? hunt result?>
tlp_ceiling: <optional, default AMBER — phishing-kit URLs often warrant AMBER+STRICT>
visibility: <unlisted | public — default unlisted for operational safety>
```

## Procedure

### 1. Validate

- Confirm it's a valid URL (scheme + host minimum)
- Extract parent domain — useful for later pivots
- Extract path + query params (but DON'T include in URL if it contains credentials or user-identifying tokens)

### 2. Primary scan

```
/lookup-urlscan url <value> --visibility unlisted
```

This takes 45-90 seconds on first submission. While waiting, run the other lookups in parallel.

**Visibility default is `unlisted`** — public submissions expose the IOC on URLScan's global feed and can tip off threat actors. Only use `public` if the user explicitly requests it or the URL is already publicly known.

### 3. Parallel reputation lookups

```
/lookup-virustotal url <value>   # aggregate reputation
/lookup-otx url <value>          # community pulses referencing this URL
```

**Add to the same parallel batch if credentials are configured**:
```
/lookup-reversinglabs url <value>                # if $REVERSINGLABS_USER is set. Network reputation from RL's malware-analysis corpus — files seen requesting this URL, RL classification. One API call.
/lookup-crowdstrike indicator <value>            # if $CROWDSTRIKE_CLIENT_ID is set. Falcon Intel view — malicious confidence, linked actors + malware families, report refs. One API call.
/lookup-misp search-attributes --value <value>   # if $MISP_URL + $MISP_KEY are set. Internal correlation against your own catalogued events.
/lookup-opencti lookup <value>                   # if $OPENCTI_URL + $OPENCTI_TOKEN are set. Internal correlation against your OpenCTI knowledge base (observables + indicators in one call).
```

Optionally (escalation):
```
/lookup-reversinglabs submit-url <value> --crawler local --wait
# only when you need a fresh RL crawl + sandbox detonation of the URL — slower and consumes submission budget
```

### 4. Consolidate

```yaml
indicator: <url>
type: url
parent_domain: <extracted>
consolidated_verdict: malicious | suspicious | phishing | clean | unknown
live_scan:
  final_url: <after redirects>
  redirect_chain: [<urls>]
  resolved_ip: <from urlscan>
  server: <from urlscan>
  screenshot_url: <...>
  scan_url: <urlscan.io result page>
  behaviors_observed:
    - <e.g., "credential form", "JS obfuscation", "drive-by download attempt">
reputation:
  vt_detection_ratio: <X/Y>
  vt_categories: [<list>]
  otx_pulse_count: <n>
contacted_infrastructure:
  domains: [<top 10>]
  ips: [<top 10>]
community_context:
  attributed_campaigns: [<from OTX>]
  malware_family: <if URL serves known malware>
pivot_candidates:
  - type: domain
    value: <parent domain>
    reason: parent
  - type: ip
    value: <resolved ip>
    reason: hosts_url
  - type: domain
    value: <contacted domain>
    reason: contacted_by_url
  - type: hash
    value: <dropped file>
    reason: url_delivers
```

### 5. Automatic follow-up (when warranted)

If the URL is malicious / phishing / suspicious AND the user's request was open-ended ("investigate this URL"), automatically invoke:
- `/domain-investigation` on the parent domain
- `/ip-investigation` on the resolved IP

Do NOT auto-chain if the verdict is clean/benign or the user's request was narrow ("just scan this URL").

### 6. Apply rigor

Chain:
- `/source-assessment`
- `/tlp-guide` (consider AMBER+STRICT for active phishing kits to avoid tipping off actors)
- `/confidence-levels`

### 7. Return

```yaml
title: "URL Investigation: <url>"
tlp: AMBER | AMBER+STRICT
confidence: <0-100>
summary: <2-3 sentences>
verdict: <...>
live_scan: <...>
reputation: <...>
contacted_infrastructure: <...>
community_context: <...>
pivot_candidates: <top 3-5>
related_investigations:
  - parent_domain_investigation: <ref or inline summary>
  - resolved_ip_investigation: <ref or inline summary>
source_ratings: <...>
investigation_date: <ISO8601>
recommended_next_steps: <...>
```

## Special cases

- **Phishing kit URLs** — often target a specific brand; note the brand in `behaviors_observed`. Consider `/sigma-writing` to build a detection.
- **Redirector chains** — the final URL matters most. Also capture intermediate domains; they're sometimes attacker-controlled infrastructure reused across campaigns.
- **URL with auth tokens / sensitive query params** — scrub before submitting anywhere public. If you cannot scrub, don't scan — note limitation instead.
- **Already-dead URL** — URLScan may report no response; check archive.org / urlscan history; don't assume benign.

## Related skills

- `/ip-investigation`, `/domain-investigation`, `/hash-investigation`
- `/malware-analysis` — if the URL delivers a file, follow up on the hash
- `/phishing-social-engineering` — knowledge cell for phishing TTPs
- `/sigma-writing` — for detection
- `/cti-orchestrator`
