# Passive monitoring strategy

> Companion to `access-methods.md` (where the data comes from) and `opsec.md` (how to handle yourself while collecting).

Passive monitoring is the bulk of defensive dark-web work: you build a list of selectors that matter to your org, point them at every collection source you can reach, and route hits into your triage queue. The trap is making the list either too narrow (miss everything) or too noisy (drown your analysts). This page is the field guide.

## Selector taxonomy

Six families. Always combine selectors from at least two families to enrich precision.

| Family | Examples | Use for |
|---|---|---|
| **Brand strings** | `"Acme Corp"`, `"Acme Cloud"`, internal product codenames | Brand mentions on leak sites, marketplace listings, hacktivist target lists |
| **Identity selectors** | Executive names, key engineers' aliases, board members | Doxing prep, executive-protection alerts, IAB targeting |
| **Email patterns** | `email:@brand.com`, `email:@subsidiary.com`, role-based addresses (`security@`, `legal@`) | Credential leaks, infostealer logs, breach corpora |
| **Domain patterns** | `domain:brand\.com`, `domain:[a-z]+-brand\.com`, sub-brands | Phishing kit chatter, typosquats listed for sale, exposed-credential dumps |
| **Network selectors** | IP ranges, CIDR blocks, ASN, BGP prefixes, hostname patterns | IAB access listings ("RDP access to ASNxxx"), CDN-fronted infrastructure mentions |
| **Technical artefacts** | Internal hostnames, project codenames, internal API URLs, certificate CNs, hash prefixes | Source-code leaks, build-pipeline exposure, supply-chain compromise indicators |

## Selector hygiene

Bad selectors create noise. Noise creates analyst fatigue. Analyst fatigue creates missed real signals.

**Rules:**

1. **Never use a bare common name.** "John Smith" matches everything. Pair with at least one other family: `regex:John Smith.{0,200}Acme` or `regex:Acme.{0,200}CFO`.
2. **Anchor domain selectors.** Use the `domain:` prefix in `keyword_match.py` — it word-boundary-anchors so `acme.com` does not match `notacme.com`.
3. **Anchor email selectors.** Use the `email:` prefix — `email:@acme\.com` matches `alice@acme.com` but not `something@notacme.com`.
4. **Compose, don't broaden.** If "Acme" is too noisy, *add* a context word (`Acme.*?(breach|leak|access|rdp|database)`) rather than removing the brand.
5. **Localise.** "Acme" in Russian is "Акме"; in Chinese, transliterations vary. If your org operates internationally, maintain selectors per locale.
6. **Refresh quarterly.** Codenames retire; products rebrand; executives change. Stale selectors miss real hits.
7. **Negative selectors.** When you cannot tighten a selector enough, add a post-match filter that drops hits matching common false-positive context (e.g., a press-release boilerplate that triggers your selector but is just journalism).

## Tool stack

Layered, vendor-first.

### Layer 1 — Vendor APIs (recommended)

Configure your selectors in vendor portals. Each vendor returns ranked alerts with context, source, and (sometimes) actor attribution.

- **Selectors first**: write the selector list once, then translate it into each vendor's UI. Vendors differ in regex support, field-targeting, and de-duplication; budget time for tuning per vendor.
- **Cadence**: most vendor portals deliver daily / weekly digests by default. For ransomware leak sites, set hourly or near-real-time.
- **Triage routing**: webhook hits into your SOAR / case management; do not let alerts pile up in vendor portals.

### Layer 2 — Bundled scripts (DIY)

For sources vendors do not cover or for budget-constrained teams.

- **`scripts/onion_search.py`** — keyword search across Ahmia + dark.fail (+ optional IntelligenceX). Run nightly per high-priority brand selector to catch new onion mirrors. Pipe into a daily review queue.
- **`scripts/telegram_monitor.py`** — read-only Telethon listener over channels your sockpuppet account joined. Use `--watch` mode behind a process supervisor (systemd, supervisord, tmux); use `--once --history N` for ad-hoc back-fills.
- **`scripts/keyword_match.py`** — local scanner over the JSONL output of the above two (and over any other text dump: leak archives, breach corpora, vendor-exported alert dumps). The selector file format is shared with `telegram_monitor.py` so you can maintain one canonical selector list.

Suggested pipeline:

```
selectors.txt ──┬──> telegram_monitor.py --watch --selectors-file selectors.txt --out telegram-hits.jsonl
                ├──> onion_search.py --query "$brand" >> onion-results/$(date +%F).jsonl
                └──> keyword_match.py --input ./collected --selectors-file selectors.txt > keyword-hits.jsonl
```

### Layer 3 — Bundled lookups (cross-skill)

Already in this pack:

- **`/lookup-ransomwarelive`** — poll for victim claims matching your org / sector / country. Free PRO tier supports ~3000 calls/day, plenty for selector-based polling.
- **`/lookup-misp`** — pivot from a hit to your MISP instance (and back) for IOC enrichment, sharing, and timeline correlation.
- **`/lookup-greynoise`, `/lookup-shodan`, `/lookup-censys`** — for the network-selector family.

## Cadence

| Source type | Polling cadence | Why |
|---|---|---|
| Ransomware leak sites (via `/lookup-ransomwarelive`) | Hourly | Claims posted in waves; first 12-24h matter most for victim notification |
| Telegram (RaaS comms, hacktivist ops) | 5-15 min (use `--watch`) | Breaking claims appear here first; ops chatter is high-tempo |
| Surface-web onion indexers (`onion_search.py`) | Daily | Indexers themselves crawl slowly; sub-daily polling wastes calls |
| Forum scrapes (vendor-mediated) | Daily or vendor's near-real-time | Most forums are low-tempo; depth of context matters more than freshness |
| Paste sites + breach announcement channels | Hourly | Credential dumps appear without warning |
| Infostealer log marketplaces | Daily | Log shops update in batches; per-domain credential exposure summary is the unit of interest |

## Storage schema

All bundled scripts emit JSONL with these common fields:

- `source` — the originating script name
- `captured_at` / `query_time` — ISO 8601 UTC
- `selector` / `selector_kind` — what matched and how
- `match` — the literal string matched
- `context_before` / `context_after` — surrounding text for triage

Suggested directory layout:

```
collected/
├── telegram/
│   └── 2026-04-28.jsonl
├── onion/
│   └── 2026-04-28.jsonl
├── leaksites/
│   └── 2026-04-28.jsonl   # /lookup-ransomwarelive recent dumps
└── triage/
    └── 2026-04-28.jsonl   # keyword_match.py output
```

One file per source per day. Append-only. Encrypted at rest. Daily rollover so file size stays under 100MB for routine grep.

## Triage workflow

1. **Daily sweep**: read the day's `triage/*.jsonl`. For each hit:
   - True-positive operational: open a case, route to SOC / IR / legal as appropriate.
   - True-positive informational: append to weekly intel report; no immediate action.
   - False positive: tune the selector. *Always* tune; never just close-without-action.
2. **Weekly review**: rotation analyst checks selector tune-ups, retires dead selectors, adds new ones from PIRs.
3. **Monthly** retro: vendor coverage gaps, DIY pipeline reliability, mean-time-to-detect by source.
4. **Quarterly**: full selector list refresh; rotate sockpuppets if approaching burn-risk thresholds; revisit vendor mix.

## Retention and legal

- **Raw collection** retention is jurisdiction-dependent. EU defenders should run retention by counsel against GDPR Art. 6 / Art. 9 considerations even for "publicly available" data — courts have not been universally permissive.
- **Typical defender practice**: 90-365 days for raw collection, longer for finished intelligence products that have been through `/apply-tlp`.
- **Special handling**: any hit that includes verified victim PII (e.g., infostealer log content with employee credentials) escalates to incident handling and to a separate, restricted-access store.
- **Sharing**: TLP-tag every artefact before it leaves the analyst. Use `/apply-tlp`. Use `/score-source` to qualify the source.

## Anti-patterns

- **One mega-selector list applied everywhere.** Different sources have different signal density; what is a useful selector on a Russian forum is noise on a defender-run news channel.
- **Polling vendor APIs faster than they update.** Wastes API budget; some vendors flag aggressive polling as abuse.
- **Letting the alert queue grow.** If 2 weeks of hits sit untriaged, you may already have missed an active intrusion or victim-notification window.
- **No feedback loop from triage to selector tuning.** Selectors should evolve every week.
- **Treating hit count as a metric.** Count of *triaged-true-positive* hits matters; raw count rewards noise.

## See also

- `access-methods.md` — vendor matrix + DIY playbook (where to point selectors).
- `opsec.md` — analyst safety while operating the collection.
- `forums.md`, `telegram-channels.md` — the source landscape.
- `/lookup-ransomwarelive`, `/lookup-misp` — bundled cross-skill lookups.
- `/score-source`, `/apply-tlp`, `/confidence-language`, `/likelihood-language` — tradecraft skills applied to every product derived from this collection.
