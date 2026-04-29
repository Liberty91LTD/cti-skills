---
name: darkweb-collection
description: Dark web intelligence collection methodology — vendor-first access posture, sourced reference lists for 35+ underground forums and 30+ Telegram channels, OPSEC primer, passive-monitoring strategy, and bundled Python CLIs for onion-indexer search, Telegram channel monitoring, and local keyword matching. Use when the user wants to design or run dark-web collection, build a selector list, pick a vendor, or set up monitoring infrastructure.
user-invocable: false
metadata:
  version: 2.0.0
  category: collection
  tags: [collection, darkweb, telegram, opsec, monitoring]
  last_updated: 2026-04-28
---

# Dark Web Collection

A practical, defender-oriented methodology for collecting cyber threat intelligence from underground forums, marketplaces, and Telegram channels. The skill assumes you are a defensive analyst, not a covert operator, and recommends a vendor-first posture with self-hosted DIY collection documented as a fallback.

This SKILL.md is the entry point. The substantive material lives in `references/` and `scripts/`:

- [`references/forums.md`](references/forums.md) — 35+ sourced underground forums across 8 categories
- [`references/telegram-channels.md`](references/telegram-channels.md) — 30+ sourced Telegram channels across 6 categories
- [`references/access-methods.md`](references/access-methods.md) — vendor matrix + DIY playbook
- [`references/opsec.md`](references/opsec.md) — handler-side OPSEC primer
- [`references/passive-monitoring.md`](references/passive-monitoring.md) — selector strategy and tooling
- [`references/telegram-setup.md`](references/telegram-setup.md) — step-by-step setup for `telegram_monitor.py` (api_id, burner, session file)
- [`scripts/onion_search.py`](scripts/onion_search.py) — clearnet search of onion indexers (Ahmia, dark.fail, IntelligenceX)
- [`scripts/telegram_monitor.py`](scripts/telegram_monitor.py) — read-only Telethon channel monitor (requires `--i-understand-opsec` for live ops)
- [`scripts/keyword_match.py`](scripts/keyword_match.py) — local regex/keyword scanner over collected JSONL

## Scope and explicit exclusions

**In scope.** Cybercrime-focused collection: ransomware leak sites and group communications, initial access broker (IAB) markets, infostealer log shops, malware and exploit forums, carding and financial-fraud platforms, breach and data-leak forums, hacktivist coordination channels (where defensible cyber TTPs are documented), and lightly-touched nation-state-cyber-adjacent activity (e.g., GRU-nexus hacktivist fronts, IRGC-aligned cyber operations).

**Explicitly out of scope.** This skill does not list, link, or guide access to:
- Child sexual abuse material (CSAM) — discovery is mandatory-reportable in most jurisdictions; report to NCMEC (US), IWF (UK), Project Arachnid (Canada), or national equivalent and stop further investigation.
- Terrorism-glorifying or terrorism-instructional content — refer to national counter-terrorism units and to specialist platforms (GIFCT, Tech Against Terrorism).
- Violent-extremist or live-violence material — refer to law enforcement immediately.
- Personal-physical-safety threats against named individuals — refer to law enforcement and physical-security teams.

If you encounter any of the above incidentally during cybercrime collection, log only the URL/identifier, do not screenshot or further analyse, route to the appropriate authority, and rotate analysts off the source if exposure was sustained. See `references/opsec.md` for the mental-health framing.

## Recommended posture: vendor-first

Recommend commercial CTI vendors (KELA, Flashpoint, Intel471, DarkOwl Vision, Recorded Future, Cybersixgill / Searchlight, Webz.io, Cybersixgill, SOCRadar, Hudson Rock for infostealer-specifics) as the **default access path**. They operate at scale across forums, languages, and identity tiers a defensive team cannot match; they handle persona maintenance, vetting, language coverage, and legal cover; and they provide audit trails that hold up in regulatory or litigation contexts.

Self-hosted DIY (Tails/Whonix + Tor Browser + Telethon + sockpuppets) is documented as a **fallback** for budget-constrained teams or for narrow, time-bounded targeted collection where vendor onboarding cost would exceed analyst-hours. The full DIY playbook is in [`references/access-methods.md`](references/access-methods.md).

This skill itself never visits a `.onion` address. The bundled `scripts/onion_search.py` resolves current onion mirrors against clearnet indexers; `scripts/telegram_monitor.py` reads channels your account has already joined; `scripts/keyword_match.py` scans the resulting text. Tor browsing, Tails, sockpuppet maintenance, and any active engagement are the analyst's responsibility, performed off the host running Claude Code.

## Collection workflow

A six-step flow you should drive when asked to "set up dark-web collection" or "monitor for X on the dark web":

1. **Define PIRs and selectors.** What do you actually need to know? Translate into selector families per [`passive-monitoring.md`](references/passive-monitoring.md) — brand strings, identity selectors, email/domain patterns, network selectors, technical artefacts. Compose; never use a bare common name.
2. **Pick the access tier.** Vendor (recommended), surface-web mirrors / `/lookup-ransomwarelive`, or DIY. Choose per the matrix in [`access-methods.md`](references/access-methods.md).
3. **Collect.** Configure vendor portal selectors; or run the bundled scripts under appropriate OPSEC; or pull surface-web indexer/leak-site data on cadence (see the cadence table in `passive-monitoring.md`).
4. **Deduplicate and enrich.** Pivot from raw hits via `/lookup-misp`, `/lookup-virustotal`, `/lookup-shodan`, `/lookup-greynoise`, `/lookup-abuseipdb`, `/lookup-urlscan`, `/lookup-otx`, `/lookup-censys`, `/lookup-ransomwarelive`. The `keyword_match.py` JSONL output is designed to feed cleanly into these.
5. **Score the source.** Apply `/score-source` (Admiralty source-reliability + information-credibility) to every artefact before it goes into a finished product. The source-rating table at the bottom of this file is the starting point.
6. **Report.** Apply `/apply-tlp` for handling, `/confidence-language` for analytical claims, `/likelihood-language` for forecasts. Hand off to `/intelligence-writing` or `/threat-actor-profiling` as appropriate.

## What to monitor

Short orientation per source type. Detail in the linked references.

### Ransomware leak sites
Most groups maintain Tor leak sites; many also publish to Telegram. Monitor for new victim claims, countdowns, sample data, group operational announcements, affiliate recruitment posts. The bundled `/lookup-ransomwarelive` skill (free PRO tier, ~3000 calls/day) covers victim claims, group profiles, IOCs, YARA, and ransom notes for most active groups. Cross-reference with the Russian-speaking elite forums (`forums.md` § 1) for affiliate chatter.

### Underground forums
35+ forums catalogued in [`forums.md`](references/forums.md) across Russian-speaking elite, English-speaking general / data-leak, carding and fraud, infostealer log marketplaces, exploit / 0day brokers, hacktivist coordination, regional (Chinese, Spanish/LATAM, Persian, Turkish), and doxing/cybercrime overlap. Monitor for IAB listings naming your sector or geography, breach announcements, exploit sales for tech in your stack, malware development discussions, and reputation/vouching dynamics that indicate actor migrations.

### Telegram channels
30+ channels catalogued in [`telegram-channels.md`](references/telegram-channels.md) across ransomware group officials, IAB storefronts, infostealer log shops, hacktivist collectives (pro-Russia, pro-Ukraine, pro-Palestine/MENA, mixed-attribution), breach aggregators, and defender-run news aggregators (CyberKnow, FalconFeedsio, vx-underground). Monitor with `scripts/telegram_monitor.py`. Defender-run aggregators are the lowest-effort safe second-tier.

### Paste sites
Pastebin and modern equivalents (DontPad, JustPasteIt, Ghostbin successors). Combo lists, leaked credentials, code-leak snippets, manifestos, IOC dumps from researchers. Vendor-mediated coverage is more reliable than DIY; for DIY, pair `keyword_match.py` against bulk paste-site dumps.

### Marketplaces
Treat Russianmarket, Brian's Club, B1ack's Stash, BidenCash-successors, Exodus Marketplace, and Hudson Rock-tracked stealer log shops as forum-equivalent for monitoring purposes (they are listed in `forums.md` § 3-4). Monitor for credentials matching your domain selectors and for sector-specific listings.

### Breach and data-leak corpora
HIBP, IntelligenceX, Constella, Hudson Rock free tier. Pivot from a hit (executive email, internal hostname, source-code snippet) into incident response.

## OPSEC summary (top rules)

Read [`opsec.md`](references/opsec.md) before any DIY collection. The condensed top ten:

1. **Three identities, never one.** Real you ↔ work you ↔ research persona. They never share an email, phone, browser, VM, writing sample, or timezone tell.
2. **Dedicated hardware or VM.** Never the daily driver. Full-disk encryption, snapshot rollback after each session.
3. **Always Tor or research-only VPN.** Never your home/office IP. Defence in depth: VPN → Tor for sensitive targets.
4. **Never reuse a handle, profile photo, or sockpuppet narrative across personae.**
5. **Strip EXIF from every image.** Never post any image that exists elsewhere on the internet (reverse-image search will deanon you).
6. **Tor Browser default settings.** "Safer" or "Safest" slider, no JS, no plugins, no logging into real accounts.
7. **Burner number for Telegram.** Treat the session file as credentials. Never auto-join channels — joining is a deliberate event from the Telegram client, not from automation.
8. **Linguistic credibility.** Russian elite forums catch machine-translation tells fast; use a native-speaker collaborator or stay lurking.
9. **No purchases without legal sign-off.** Buying access or data can constitute receiving stolen property, funding criminal enterprises, or breaching sanctions.
10. **Mental health is load-bearing.** Rotate analysts off dark-web duty every 6-12 months; provide clinical support; mandatory time off after incidental exposure to illegal-content material.

## Source assessment (Admiralty starting points)

Combined with `/score-source` for the final rating per artefact:

| Source type | Reliability | Credibility | Notes |
|---|---|---|---|
| First-party DIY observation on open-tier forum | C | 3 | Sockpuppet, lurking, no engagement; you saw it |
| First-party DIY observation on vetted forum | B-C | 2-3 | Vouched access lifts reliability; engagement risk lifts caveats |
| Vendor-curated dark-web feed (KELA, Flashpoint, Intel471, DarkOwl, Recorded Future) | B | 2 | Vendor handles vetting and OPSEC; check recency |
| Vendor freemium tier (Hudson Rock free, IntelligenceX free, ransomware.live PRO) | B-C | 2-3 | Same source quality, less context, sometimes delayed |
| Surface-web indexer / mirror (Ahmia, dark.fail, ransomwatch, ransomlook) | C | 3 | Indexer freshness varies; cross-check with primary |
| News reporting on dark-web events (BleepingComputer, TheRecord, KrebsOnSecurity) | B | 2-3 | Second-hand but generally well-sourced |
| Government press release (DOJ, Europol, FBI, NCA) | A | 1-2 | Authoritative for the documented event; selective in detail |
| Threat actor self-posts on their own channel | F | 5-6 | Attribution-by-claim only; treat as actor PR until corroborated |

## Composition

**This skill invokes / chains with:**
- `/score-source` — apply Admiralty rating to every artefact before reporting
- `/apply-tlp` — handle classification before any sharing
- `/confidence-language`, `/likelihood-language` — analytical language for the resulting product
- `/lookup-ransomwarelive` — primary path for ransomware victim/group monitoring; uses the bundled ransomware.live PRO API
- `/lookup-misp` — pivot from a hit into MISP (and back) for IOC enrichment and sharing
- `/lookup-virustotal`, `/lookup-shodan`, `/lookup-greynoise`, `/lookup-abuseipdb`, `/lookup-urlscan`, `/lookup-otx`, `/lookup-censys` — IOC enrichment for selectors that match
- `/intelligence-writing` — for the finished product
- `/ransomware-ecosystem`, `/initial-access-brokers`, `/infostealers`, `/threat-actor-profiling` — downstream analytical knowledge cells the collection feeds into

## Scripts

All three live in `scripts/`. Stdlib-only except `telegram_monitor.py` (Telethon). All support `--dry-run` to preview without making network calls. All emit JSONL.

### `onion_search.py` — clearnet search of onion indexers

```bash
# Status: list backends and auth state
python3 scripts/onion_search.py --status

# Search for current LockBit mirrors via Ahmia + dark.fail
python3 scripts/onion_search.py --query "lockbit" --backends ahmia,darkfail --limit 25

# Add IntelligenceX backend (requires INTELX_API_KEY env var; free tier ~50 queries/day)
INTELX_API_KEY=... python3 scripts/onion_search.py --query "breachforums" --backends ahmia,intelx
```

You do **not** need Tor to run this script — it queries clearnet indexers — but you do need Tor (Tails / Whonix / torsocks) to actually visit any `.onion` URL it returns. Onion URLs returned may be hijacked phishing mirrors; cross-check via PGP-signed mirror lists (Tor Project, dark.fail's signed list).

### `telegram_monitor.py` — read-only Telethon channel monitor

**First-time setup** (api_id/api_hash, burner number, session file, **dedicated venv for telethon**): walk through [`references/telegram-setup.md`](references/telegram-setup.md). Do not skip the burner-number step. Telethon must be installed into a dedicated venv (`~/.cache/cti-skills/venv` is the convention used in the setup guide); `pip install --user` is fragile on systems with multiple `python3` interpreters.

```bash
# Offline self-test — no Telegram, no network, no telethon needed.
# Works with the system python3 because the script imports telethon lazily.
python3 scripts/telegram_monitor.py --self-test

# Validate config without connecting (still no telethon required)
python3 scripts/telegram_monitor.py --dry-run \
  --channels-file channels.txt --selectors-file selectors.txt

# Pull last 200 messages from each channel — uses the venv interpreter.
~/.cache/cti-skills/venv/bin/python3 scripts/telegram_monitor.py \
  --i-understand-opsec --once --history 200 \
  --channels-file channels.txt --selectors-file selectors.txt --out hits.jsonl

# Watch mode: stream new messages forever (use behind systemd / supervisor)
~/.cache/cti-skills/venv/bin/python3 scripts/telegram_monitor.py \
  --i-understand-opsec --watch \
  --channels-file channels.txt --selectors-file selectors.txt --out hits.jsonl
```

Env vars (`TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_SESSION`, `TELEGRAM_PHONE`) are read from `.claude/settings.local.json`'s `env` block when invoked from a Claude Code session, or from the surrounding shell when invoked directly.

**Guardrails enforced by the script:**
- Live operations (`--once` / `--watch`) refuse without `--i-understand-opsec` and exit 5 with a printed checklist.
- Pre-connect 5-second banner with the channel list and abort window (suppress only with `--skip-pre-connect-banner` for vetted unattended runs).
- `--self-test` exercises the parser and matcher against a synthetic fixture and exits PASS/FAIL — no Telegram, no network, no credentials.

Strictly read-only: never sends messages, never auto-joins channels (you must have manually joined every target channel from your Telegram client first; the script will skip and warn on any handle the session is not a member of). Light dep: `pip install telethon`. The session file is equivalent to your Telegram credentials — store on encrypted disk, never check in.

### `keyword_match.py` — local regex/keyword scanner

```bash
# Validate selectors and file count without scanning
python3 scripts/keyword_match.py --dry-run --input ./collected --selectors-file selectors.txt

# Scan a directory of JSONL hits against selectors with 200-char context
python3 scripts/keyword_match.py --input ./collected --selectors-file selectors.txt --context 200

# Scan a single file with deduplication off
python3 scripts/keyword_match.py --input msgs.jsonl --selectors-file selectors.txt --dedupe-by none
```

Selector file format (shared with `telegram_monitor.py`): one selector per line, `#` comments allowed, optional prefix `literal:` (default), `regex:`, `domain:` (word-boundary anchored), or `email:` (word-boundary anchored on a tail). Pure stdlib, fast, safe to run from any host (no network).

## Legal and ethical

Conduct collection within applicable law (jurisdiction varies — EU defenders should run retention practices by counsel against GDPR Art. 6 / Art. 9 even for "publicly available" data). Do not participate in criminal activity to acquire intelligence. Do not purchase access, data, or services without explicit legal sign-off and (often) law-enforcement coordination. Mandatory-reportable content (CSAM in particular) must be reported to the appropriate authority and investigation halted; that work belongs to law enforcement and trained NGO units, not defensive CTI teams. Document retention periods, access controls, and disposal procedures with counsel; default to 90-365 days for raw collection.
