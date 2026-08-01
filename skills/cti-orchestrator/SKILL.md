---
name: cti-orchestrator
description: Use as the default entry point for any CTI request that doesn't name a specific skill. Activates when a user asks to investigate an indicator, profile a threat actor, write an assessment, enrich IOCs, or build detection rules. Routes to the right investigation or analysis skill, then auto-applies rigor skills (source rating, TLP, confidence, likelihood) on the output.
metadata:
  version: 1.0.0
  tags: [orchestrator, entry-point]
  tradecraft: true
---

# cti-orchestrator

You are the default entry point for the `cti-skills` pack. When a user's request doesn't name a specific skill, activate here. Your job is to:

1. Classify the request
2. Invoke the right downstream skill(s)
3. Auto-apply rigor skills on the result
4. Return a source-rated, confidence-marked product

You do NOT query external APIs directly. Compose other skills — especially the `lookup-*` skills — to do the work.

## When to activate

Activate on any of these user intents:

| User says something like... | Route to |
|---|---|
| "Investigate 8.8.8.8" / "check this IP" | `/ip-investigation` |
| "What's this domain doing" / "investigate example.com" | `/domain-investigation` |
| "Check this hash" / "is d41d8cd98f... malicious" | `/hash-investigation` |
| "Scan this URL" / "what does this link do" | `/url-investigation` |
| "Profile APT28" / "tell me about this actor" | `/threat-actor-profiling` |
| "Track this campaign" | `/campaign-tracking` |
| "Analyze this malware sample" | `/malware-analysis` |
| "Write a threat assessment on X" | `/threat-assessment` + `/writing-assessments` + `/intelligence-writing` |
| "Enrich this IOC list" | `/ioc-enrichment-workflow` → appropriate `lookup-*` skills → `/ioc-export` |
| "Write detection rules for X" | `/sigma-writing` / `/yara-writing` / `/kql-writing` |
| "What's the current X landscape" | relevant knowledge cell (e.g., `/ransomware-ecosystem`) + `/horizon-scanning` |
| "Run ACH" / "hypothesis analysis" | `/ach` |
| Direct invocation `/skill-name` | bypass this orchestrator, invoke directly |

If the request is ambiguous, ask one clarifying question. Don't guess.

## Routing logic

For investigation-shaped requests:
```
user request
  ↓ classify indicator type (IP / domain / hash / URL / actor / campaign / sample / topic)
  ↓
invoke the matching investigation or analysis skill
  ↓
that skill may chain multiple /lookup-<api> skills in parallel
  ↓
on completion → auto-apply rigor (see next section)
  ↓
return to user
```

For analytical or production-shaped requests:
```
user request
  ↓ check active PIRs (if present under data/pirs/active/) for priority alignment
  ↓
invoke the relevant analytical skill(s): /threat-assessment, /ach, /structured-analytic-techniques, /red-team-analysis, /key-assumptions-check, /horizon-scanning
  ↓
if writing a product: /intelligence-writing, /writing-assessments
  ↓
apply /quality-control before presenting
  ↓
auto-apply rigor
  ↓
return to user
```

## Auto-rigor pipeline

After the primary skill(s) complete, apply these rigor skills to the output **without asking the user**. They're non-negotiable for any intelligence product.

1. **`/source-assessment`** — assign Admiralty Scale ratings (source reliability A-F, information credibility 1-6) to each piece of collected intelligence. Use the `default_source_reliability` + `default_information_credibility` declared in each lookup skill's frontmatter as starting points; adjust based on content.
2. **`/tlp-guide`** — mark every output with a TLP designation (CLEAR / GREEN / AMBER / AMBER+STRICT / RED). Default to AMBER for investigative findings unless the user specifies otherwise or content is inherently public (OSINT aggregations → CLEAR).
3. **`/confidence-levels`** — attach a MISP confidence score (0-100) to every analytical judgment. Justify based on source ratings and corroboration.
4. **`/likelihood-language`** — use probability-yardstick language for any forward-looking statement ("Remote" / "Unlikely" / "Even Chance" / "Likely" / "Almost Certain" with numeric bands).

If the user explicitly says "skip rigor" or "just give me the raw data," honor that.

## PIR awareness

If `data/pirs/active/` exists and contains files, read them first. When the request aligns with an active PIR, note the PIR ID in the output header. When the product satisfies a PIR, update the PIR's `last_satisfied` field and suggest refreshing the PIR list.

## Knowledge cell updates

After significant new intelligence is collected, consider whether a knowledge cell should be updated:

- IP/domain attributed to a known actor → update that actor's cell
- New campaign observed → update the relevant regional or malware-family cell
- TTP observed in the wild → update the matching threat area (e.g., `/ransomware-ecosystem`)

Use `/feedback-loops` to log the update if non-trivial.

## Lookup catalog

Authoritative list of `/lookup-*` skills available in this pack. **Keep this list in sync** when a new lookup is added (a hook reminds when `skills/lookup-*/SKILL.md` is touched). When routing an investigation, ensure the downstream skill chains every applicable lookup from this list — don't trust that downstream skill bodies are current.

| Skill | Indicator types | Default Admiralty | Notes |
|---|---|---|---|
| `/lookup-liberty91` | ip, domain, hash, url, actor, malware, CVE, occurrence | **native Admiralty** | **First-party — check before spending third-party quota.** Deduplicated Threat Events (occurrences with every source, each source's reliability grade, the occurrence's credibility band and verification stage), canonical threat library with ATT&CK TTPs, IOC lookup, alert matches, per-organization relevance. Two-way: also ingests reports and generates intelligence packages (writes need user confirmation). Use the platform's own reliability/credibility rather than a default rating. |
| `/lookup-virustotal` | ip, domain, hash, url | B2 | Crowd-sourced AV aggregate; default first call |
| `/lookup-otx` | ip, domain, hash, url | C3 | AlienVault community pulses; cheap and unconstrained |
| `/lookup-abuseipdb` | ip | B2 | Abuse-report history; IP-only |
| `/lookup-greynoise` | ip | B2 | Internet-noise classifier; use to short-circuit on benign scanners |
| `/lookup-shodan` | ip, domain | B2 | Host fingerprint, ports, services, vulns |
| `/lookup-censys` | ip, cert search | B2 | Deep host + certificate recon; **250/month free quota** — use sparingly |
| `/lookup-urlscan` | url, domain | B2 | Live scan + existing-scan search |
| `/lookup-reversinglabs` | ip, domain, url, hash | **A2** | Spectra Analyze (A1000) — vendor-authoritative classification, MITRE ATT&CK, sandbox, sample fan-out. **Use whenever credentials are configured** — independent of VT and stronger than crowd AV. |
| `/lookup-crowdstrike` | ip, domain, hash, url, actor, report | **A2** | Falcon Intelligence — IOC reputation (malicious confidence, linked actors/malware) AND finished intel: threat-actor profiles, actor search by origin/target, MITRE ATT&CK TTPs, intel reports. **Use whenever credentials are configured** — the primary vendor feed for actor/report/TTP questions, not just IOC lookups. |
| `/lookup-misp` | any | B2 | Internal correlation against your own MISP catalogue |
| `/lookup-opencti` | any | B2 | Two-way: correlation against your OpenCTI knowledge base (indicators, observables, actors, reports) + write-back of vetted findings |
| `/lookup-ransomwarelive` | org-name, group | B2 (group/dates), B3 (descriptions) | Ransomware leak-site claims; treat criminal-written descriptions cautiously |

When a downstream investigation skill (e.g. `/hash-investigation`) is invoked but its SKILL.md doesn't reference a lookup that obviously applies (e.g. RL for a hash), **chain it explicitly anyway** and flag the omission for skill-body update. Better to over-chain once than miss high-value signal.

## What you do NOT do

- **Do not call external APIs directly.** Always invoke a `/lookup-*` skill.
- **Do not perform deep analysis in this skill.** Delegate to `/analyst` equivalents (`/threat-actor-profiling`, `/ach`, `/threat-assessment`, etc.).
- **Do not write finished reports in this skill.** Delegate to `/intelligence-writing` or `/writing-assessments`.
- **Do not skip the rigor pipeline** unless the user explicitly opts out.

## Composition contract

When you invoke a downstream skill, include in your message to the skill:
- The user's original request (verbatim)
- Any context already gathered (e.g., IOC type, indicator, known aliases)
- The expected output format
- Any constraints (TLP ceiling, PIR alignment, rate-limit concerns)

Downstream skills follow the same contract when they chain further skills.

## See also

- `AGENTS.md` — platform-neutral orientation
- `VERSIONS.md` — what's shipped
- `tools/REGISTRY.md` — external API catalog
- Investigation skills: `/ip-investigation`, `/domain-investigation`, `/hash-investigation`, `/url-investigation`
- Analytical skills: `/threat-actor-profiling`, `/ach`, `/threat-assessment`, `/campaign-tracking`, `/malware-analysis`
- Rigor skills: `/source-assessment`, `/tlp-guide`, `/confidence-levels`, `/likelihood-language`
- Production skills: `/intelligence-writing`, `/writing-assessments`, `/quality-control`
