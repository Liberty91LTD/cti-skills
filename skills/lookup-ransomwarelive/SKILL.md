---
name: lookup-ransomwarelive
description: Use when you need to check whether an organisation/domain has been claimed by a ransomware group, profile a specific ransomware group (TTPs, leak-site infra, IOCs, YARA), or aggregate ransomware victim claims by country/sector/timeframe. Backed by ransomware.live's leak-site scrapes — 27k+ victims across 330+ groups. Commonly invoked by /domain-investigation, /ransomware-ecosystem, /threat-actor-profiling, and detection-engineering workflows. Reads $RANSOMWARE_LIVE.
metadata:
  version: 1.0.0
  tags: [lookup, threat-intel, ransomware, leak-sites, ttps, iocs, yara]
  api: ransomwarelive
  default_source_reliability: B
  default_information_credibility: 2
---

# lookup-ransomwarelive

Queries ransomware.live's PRO API for victim claims, group profiles, IOCs, YARA rules, ransom notes, negotiation chats, and CSIRT contacts. Retrieval only — the invoking skill or agent reasons about the result. Note that **leak-site claims are claims, not confirmed breaches** (see Source reliability below).

## When to invoke

- An investigated domain or organisation should be checked against ransomware leak-site claims
- Profiling a ransomware group — pull description, TTPs, tools, vulnerabilities, leak-site `.onion` infrastructure
- Sector- or country-level ransomware briefing (e.g., "all NL victims claimed in 2026")
- Detection engineering for a specific group — fetch its public YARA rules + IOC dump
- Updating the `/ransomware-ecosystem` knowledge cell with the current top-N groups by victim count
- Incident response: looking up a country's CSIRT/CERT contact list

**Do NOT invoke for:**
- General malware classification — use `/lookup-virustotal`
- Confirming whether a specific incident actually occurred — leak-site claims are unverified by default
- Initial-access vector intelligence — that's not on leak sites; chain `/initial-access-brokers` instead

## How to invoke

Single Python CLI (stdlib only — no install).

### Sanity checks

```bash
python3 tools/clis/ransomwarelive.py validate     # check the API key
python3 tools/clis/ransomwarelive.py stats        # global totals
```

### Victim lookups

```bash
# Free-text search across victim names + descriptions
python3 tools/clis/ransomwarelive.py search --q "acme corp"

# Targeted filters (combine freely)
python3 tools/clis/ransomwarelive.py search --country NL --limit 10
python3 tools/clis/ransomwarelive.py search --sector Healthcare --country US
python3 tools/clis/ransomwarelive.py search --group lockbit3 --limit 5

# Last 100 claims globally (newest first)
python3 tools/clis/ransomwarelive.py recent --limit 20

# Single victim detail by ransomware.live id
python3 tools/clis/ransomwarelive.py victim "QksgR3JvdXBAYWtpcmE="
```

### Group intelligence

```bash
# All 330+ groups, sorted by victim count
python3 tools/clis/ransomwarelive.py groups --limit 20

# Profile of a specific group — description, TTPs, tools, leak-site URLs, etc.
python3 tools/clis/ransomwarelive.py group-profile lockbit3

# Lighter group detail
python3 tools/clis/ransomwarelive.py group lockbit3
```

### Defensive intel

```bash
# IOC dump (md5, ip, etc.) — all groups
python3 tools/clis/ransomwarelive.py iocs
# Per-group IOCs
python3 tools/clis/ransomwarelive.py iocs lockbit3

# YARA rules — all groups, or per group
python3 tools/clis/ransomwarelive.py yara
python3 tools/clis/ransomwarelive.py yara lockbit3        # full rule content

# Ransom note samples
python3 tools/clis/ransomwarelive.py ransomnotes lockbit3

# Negotiation chat logs (if available for that group)
python3 tools/clis/ransomwarelive.py negotiations lockbit3
```

### Context

```bash
python3 tools/clis/ransomwarelive.py press              # recent press mentions
python3 tools/clis/ransomwarelive.py press --all        # full archive
python3 tools/clis/ransomwarelive.py sectors            # valid sector filter values
python3 tools/clis/ransomwarelive.py csirt NL           # CSIRT contacts for a country
```

All commands accept `--dry-run` (preview the request without spending quota) and `--insecure` (TLS bypass — rarely needed). The CLI exits 2 if `RANSOMWARE_LIVE` is unset (not in dry-run); report missing key, do not fabricate.

## Quota

PRO tier: **3,000 calls/day** with burst allowed. Each subcommand is one HTTP call. Use `--dry-run` if scoping a batch.

## Pivots

- **From `/domain-investigation` or `/ip-investigation`** → `search --q <orgname>` to check if the domain's owner has been claimed
- **From `/ransomware-ecosystem` knowledge cell** → `groups --limit 30` for current top-N + `group-profile` for each
- **From `/threat-actor-profiling` (ransomware group target)** → `group-profile <name>` is the primary feed; chain `iocs`, `yara`, `negotiations` for depth
- **From `/sigma-writing` / `/yara-writing`** → `yara <group>` returns existing community rules to start from
- **Country-scoped briefing** → `search --country <CC>`, then `csirt <CC>` for IR contact list

## Response format

Read commands return:

```yaml
source: ransomware.live
operation: search | recent | victim | groups | group-profile | iocs | yara | ...
query_time: <ISO8601>
data:
  <distilled response>
```

For `search` and `recent`, `data.victims[]` is normalised to:

```yaml
id: <ransomware.live id>
title: <victim name>
group: <ransomware group, e.g. lockbit3, akira>
country: <ISO-3166 alpha-2>
sector: <activity / sector>
discovered: <when ransomware.live scraped the post>
published: <when leak-site authored the post>
description: <criminal-written breach summary — treat as low credibility>
website: <victim website>
post_url: <leak-site post URL, often .onion>
permalink: <ransomware.live record URL>
screenshot: <leak-site screenshot, if archived>
```

## Source reliability (Admiralty default)

Default for `/score-source`: **B2** (usually reliable, probably true).

**Important credibility nuance:**

| Field | Credibility | Why |
|---|---|---|
| Victim name, country, sector, dates, group attribution | 2 (probably true) | Corroborated by the leak-site post itself |
| Breach `description` | 3–4 (possibly true → doubtful) | Written by criminals to coerce payment; routinely overstates volume/sensitivity/ongoing access |
| YARA rules, IOC lists | 2 (probably true) | Sourced from public researchers; cross-check before deploying |

A leak-site claim is a **claim**, not a confirmed breach. Many victims dispute or never publicly acknowledge. Some posts repackage older breaches under a new brand. Always frame downstream products with this caveat.

## Operational notes

- **Server returns full result sets, not pages.** `search --country US` hits the API once and returns ~8k victims. `--limit N` trims locally — narrow with filters (`--group`, `--sector`, `--country`) to keep responses small.
- **`group_name` is sometimes null** in `/victims/recent` responses — known API quirk; the value populates correctly in `search` and `victim` detail.
- **The `description` field can contain victim PII or stolen credentials** — quote selectively in finished products; don't paste full responses into shared docs.
- **PRO endpoint** is `api-pro.ransomware.live`. The free unauthenticated endpoint (`api.ransomware.live`, 1 req/min) is not supported by this CLI.

## Related skills

- `/ransomware-ecosystem` — knowledge cell consuming `groups` + `group-profile` data
- `/threat-actor-profiling` — for ransomware-group profiles, the `group-profile` endpoint is the primary feed
- `/yara-writing`, `/sigma-writing` — start from `yara <group>` output
- `/lookup-virustotal`, `/lookup-otx` — chain after pulling group IOCs to verify hashes
- `/domain-investigation` — pivots into `search --q <orgname>` for victim-status check
- `/initial-access-brokers` — complementary; ransomware.live doesn't track IAB activity
- `/score-source`, `/apply-tlp`, `/confidence-language` — apply rigor before publishing

## See also

- Integration setup: `tools/integrations/ransomwarelive.md`
- Python CLI source: `tools/clis/ransomwarelive.py`
- API docs: https://api-pro.ransomware.live/docs
- Project: https://www.ransomware.live/
