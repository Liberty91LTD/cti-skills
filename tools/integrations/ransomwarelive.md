# ransomware.live integration

[Ransomware.live](https://www.ransomware.live/) tracks ransomware victim claims by scraping leak sites (DLS — data leak sites) of named ransomware groups. The dataset answers: who has been claimed, by which group, when, in which sector and country. The PRO API also exposes group profiles (TTPs, tools, leak-site infrastructure), per-group IOCs, YARA rules, ransom-note samples, and negotiation chats — making it a one-stop CTI feed for the criminal-extortion ecosystem.

This pack targets the **PRO** tier (`api-pro.ransomware.live`). The free unauthenticated tier (`api.ransomware.live`, 1 req/min/endpoint) is not supported by the CLI.

## Getting a key

1. Sign up at https://my.ransomware.live (free PRO account)
2. Generate an API key in the dashboard
3. Set `RANSOMWARE_LIVE` in your environment or stash it in `.claude/settings.local.json` via `./scripts/setup.sh`

## Authentication

```
X-API-KEY: <RANSOMWARE_LIVE>
Accept: application/json
```

Test:

```bash
curl -s -H "X-API-KEY: $RANSOMWARE_LIVE" https://api-pro.ransomware.live/validate
# → {"status": "valid", "client": "<your-email>"}
```

## Rate limits

| Tier | Calls/day | Auth | Notes |
|---|---|---|---|
| Free (api.ransomware.live) | — | none | 1 req/min/endpoint, no IPv6 |
| PRO (api-pro.ransomware.live) | 3,000 | `X-API-KEY` | Burst allowed, fair-use policy |
| PRO+ | TBD | TBD | Coming soon — enhanced analytics |

The CLI surfaces `429` cleanly and exits 1.

## Endpoints used

The Python CLI (`tools/clis/ransomwarelive.py`) covers:

| Subcommand | Path | Returns |
|---|---|---|
| `validate` | `GET /validate` | key status |
| `stats` | `GET /stats` | global victim/group/press counts |
| `search` | `GET /victims/search?q=&group=&sector=&country=&order=` | filtered victim list |
| `recent` | `GET /victims/recent` | last 100 claims |
| `victim` | `GET /victim/{id}` | single victim detail |
| `groups` | `GET /groups` | full group list with victim counts |
| `group` | `GET /groups/{name}` | group detail |
| `group-profile` | `GET /group/{name}` | rich profile: description, TTPs, tools, leak-site infra |
| `iocs` | `GET /iocs[/{group}]` | indicator dump (md5, ip, etc.) |
| `yara` | `GET /yara[/{group}]` | YARA rules per group |
| `ransomnotes` | `GET /ransomnotes[/{group}[/{note}]]` | ransom note samples |
| `negotiations` | `GET /negotiations[/{group}[/{chat_id}]]` | negotiation chat logs |
| `press` | `GET /press/recent` (default) or `/press/all` | press mentions |
| `sectors` | `GET /listsectors` | valid sector filter values |
| `csirt` | `GET /csirt/{country}` | CSIRT/CERT contacts for a country |

### Search filter notes

- `--q` is the only free-text param. Other filters (`--group`, `--sector`, `--country`) are exact-match against indexed fields.
- `--country` uses ISO-3166 alpha-2 (`US`, `NL`, `DE`).
- `--sector` must match a value from `/listsectors` (run `ransomwarelive.py sectors` to get the list).
- `--order` accepts `discovered` (default — when ransomware.live first scraped the post) or `published` (when the leak-site post was authored).
- The server returns `count` (total matching) and `victims` (full result set, no server-side pagination). `--limit N` on the CLI just trims locally — every search call hits the API once and returns everything matched, so use `--country`/`--sector`/`--group` to narrow before the round-trip.

### Group-profile is the killer endpoint

`group-profile lockbit3` returns:

- `description` — analyst-written summary
- `ttps` — list of MITRE ATT&CK technique IDs
- `tools` — known tools used
- `vulnerabilities` — CVEs the group is known to exploit
- `locations` — leak-site `.onion` URLs with availability + last-scrape timestamps
- `has_negotiations` / `has_ransomnote` flags + counts
- `firstseen` / `lastseen` activity dates

This feeds directly into `/threat-actor-profiling` and `/ransomware-ecosystem` knowledge-cell updates.

## Admiralty defaults (for `/score-source`)

**Source reliability:** B (usually reliable) — ransomware.live aggregates leak-site scrapes performed continuously; data hygiene is good and the team publishes corrections.

**Information credibility:**
- For *metadata* (victim name, country, sector, dates, group attribution): **2** (probably true) — corroborated by the leak-site post itself
- For *breach descriptions* (the `description` field): **3-4** (possibly true / doubtful) — these are written by criminals to coerce payment and routinely overstate volume, sensitivity, or ongoing access
- For *YARA rules / IOCs*: **2** (probably true) — sourced from public researchers like rivitna; cross-check before deploying

Always treat a leak-site claim as a *claim*, not a confirmed breach. Many victims dispute, downscale, or never publicly acknowledge; some claims are repostings of older breaches under a new brand.

## When to invoke

- Domain or organisation comes up in an investigation — check whether they've been claimed by a ransomware group
- Threat-actor profiling on a ransomware group — pull `group-profile`, IOCs, YARA, negotiations
- Sector or country threat-landscape briefing — aggregate via `search --sector` / `--country`
- Detection-engineering for a specific group — pull `yara` rules and `iocs` to seed signatures
- Updating `/ransomware-ecosystem` knowledge cell — `groups` + `group-profile` for the top families

## What the API doesn't tell you

- Whether the leak-site post is *true* (the data may not exist, may be stale, may be from a third-party breach the group is reposting)
- Whether the victim paid (ransomware.live infers this only loosely from post status changes)
- Anything about the *initial-access* vector for a specific victim — that's not on the leak site
- TTPs at incident granularity — `group-profile.ttps` is the group's general repertoire, not a per-victim chain

For initial-access intelligence, chain `/initial-access-brokers` knowledge cell. For per-victim TTP detail, you need vendor IR reports.

## Privacy

- The CLI hits a public API. There is no data submission, no callback URL, no exposure of investigated indicators.
- Be careful with the response data downstream: leak-site descriptions occasionally contain victim PII or stolen credentials. Don't cache the full response into shared documentation; quote selectively.

## See also

- API docs: https://api-pro.ransomware.live/docs (Swagger UI; `swagger.json` available at the same host)
- Project: https://www.ransomware.live/
- Lookup skill: `skills/lookup-ransomwarelive/SKILL.md`
- Python CLI source: `tools/clis/ransomwarelive.py`
- Related: `skills/ransomware-ecosystem/SKILL.md` (knowledge cell), `skills/threat-actor-profiling/SKILL.md`
