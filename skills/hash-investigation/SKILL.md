---
name: hash-investigation
description: Use when a user asks to check, identify, or characterize a file hash (MD5, SHA-1, SHA-256). Chains VirusTotal and OTX, optionally triggers /malware-analysis for deeper behavioral review. Returns detection signals, malware family, behavioral tags, and pivot candidates (communicating IPs, dropped files). Invoked by /cti-orchestrator when the target is a hash.
metadata:
  version: 1.1.0
  tags: [investigation, composition, malware, hash]
  tradecraft: true
---

# hash-investigation

Investigate a file hash end-to-end. Chain lookups, surface malware family attribution, prioritize infrastructure pivots, and decide whether deeper malware analysis is warranted.

**This skill invokes:** `/lookup-virustotal`, `/lookup-otx`, optionally `/lookup-reversinglabs` (vendor-authoritative classification + MITRE ATT&CK + sandbox), optionally `/lookup-crowdstrike` (Falcon Intel verdict + actor/malware attribution), optionally `/lookup-misp` (internal correlation), optionally `/malware-analysis`, then `/source-assessment`, `/tlp-guide`, `/confidence-levels`.

## When to invoke

- User asks to check a hash, identify malware, or enrich a sample
- Another skill surfaces a hash during investigation (e.g., `/ip-investigation` found communicating files)
- User asks "what is this malware" with a hash as input

## Inputs

```yaml
indicator: <MD5 | SHA-1 | SHA-256 hash>
context: <optional — where did this hash come from?>
tlp_ceiling: <optional, default AMBER>
request_malware_analysis: <optional bool — trigger /malware-analysis after lookup>
```

## Procedure

### 1. Validate

- Confirm the hash is a valid length (MD5=32, SHA-1=40, SHA-256=64 hex chars)
- Reject if not; route to correct skill if it looks like a different indicator type

### 2. Parallel lookups

**Always run** (free / commonly available):
```
/lookup-virustotal hash <value>    # detection stats, family, behavior tags
/lookup-otx hash <value>           # community pulses, campaign attribution
```

**Add to the same parallel batch if credentials are configured** — don't demote these to "later, maybe":
```
/lookup-reversinglabs hash <value> --av-scanners --ticloud   # if $REVERSINGLABS_USER is set. Vendor-authoritative verdict + threat name + AV detection ratio. RL is the strongest single-source verdict on a hash; run it whenever available, not just when VT signal is thin.
/lookup-crowdstrike indicator <value>                        # if $CROWDSTRIKE_CLIENT_ID is set. Falcon Intel verdict — malicious confidence + the threat actors and malware families CrowdStrike links to this hash + report refs. One API call.
/lookup-misp search-attributes --value <value>               # if $MISP_URL + $MISP_KEY are set. Internal correlation against your own catalogued events.
```

**Escalation lookup** (run sequentially after the parallel batch only if the call below is warranted):
```
/lookup-reversinglabs report <value> --detailed              # when you need MITRE ATT&CK mapping, sandbox detonation output, or networkthreatintelligence (C2 indicators extracted from the sample). Heavier than `hash` — use when classification alone is not enough.
```

### 3. Check if known-benign

If VirusTotal detection ratio is 0/Y with Y>30, AND OTX has no pulses, AND the file has standard legit characteristics (signed by major vendor, common packaging), treat as likely-benign. Stop and summarize. Don't spend analyst time.

### 4. Consolidate

```yaml
indicator: <hash>
type: hash
hash_type: md5 | sha1 | sha256
consolidated_verdict: malicious | suspicious | clean | unknown
detection_stats:
  vt_ratio: <X/Y>
  first_seen: <date>
  last_analysis: <date>
  names: [<aliases>]
classification:
  malware_family: <popular_threat_classification from VT>
  tags: [<from VT>]
  attributed_actor: <if OTX pulses mention an actor>
file_details:
  type: <PE, ELF, Office, script, etc.>
  size: <bytes>
  packers: [<if detected>]
  signed: <boolean>
  signer: <if signed>
behavior_summary:
  sandbox_verdicts: <from VT>
  notable_behaviors: [<from VT tags>]
  mitre_techniques: [<if inferrable>]
community_context:
  otx_pulse_count: <n>
  campaign_references: [<...>]
pivot_candidates:
  - type: ip
    value: <c2 ip from communicating>
    reason: c2_comm
  - type: domain
    value: <c2 domain>
    reason: c2_comm
  - type: hash
    value: <parent or dropped>
    reason: child_parent
```

### 5. Prioritize pivots

1. **C2 IPs / domains from communicating_files / contacted_domains** — active infrastructure
2. **Parent hashes** (droppers / packers) — same campaign lineage
3. **Dropped hashes** (payloads) — behavioral family
4. **YARA rule matches** (if VT exposes them) — strong family clustering
5. **Command-line strings** — targeting / configuration hints

### 6. Decide on deeper analysis

If detection ratio is high and malware family is known, the lookup may be sufficient. If the hash is novel (low VT detection, recent first_seen, no known family), invoke `/malware-analysis` for a structural and behavioral review.

Also invoke `/malware-analysis` if:
- User explicitly asked for analysis (`request_malware_analysis: true`)
- This is part of a targeted incident response, not routine IOC triage

### 7. Apply rigor

Chain:
- `/source-assessment`
- `/tlp-guide`
- `/confidence-levels`

### 8. Return

```yaml
title: "Hash Investigation: <hash>"
tlp: AMBER
confidence: <0-100>
summary: <2-3 sentences with malware family if known>
verdict: <...>
detection_stats: <...>
classification: <...>
file_details: <...>
behavior_summary: <...>
community_context: <...>
pivot_candidates: <top 3-5>
source_ratings: <...>
investigation_date: <ISO8601>
recommended_next_steps:
  - <e.g., "run /malware-analysis", "pivot on C2 IP via /ip-investigation">
```

## Special cases

- **Hash not found in VT** — doesn't mean clean. Could be very new, rare, or deleted. Check OTX; escalate to `/malware-analysis` if user has the sample.
- **VT detection very low (1-2 engines)** — often false positive or generic heuristic. Downgrade source rating; don't alarm the user without corroboration.
- **Signed by legit vendor but flagged** — possible supply-chain scenario. Flag for special review.

## Related skills

- `/ip-investigation`, `/domain-investigation`, `/url-investigation`
- `/malware-analysis` — for novel or targeted samples
- `/yara-writing` — if the sample should produce a detection rule
- `/indicator-pivoting` — multi-hop IOC graphing
- `/cti-orchestrator`
