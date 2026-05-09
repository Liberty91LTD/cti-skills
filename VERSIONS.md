# Versions

Per-skill semantic version and changelog. Update this file when you ship changes to a skill. Skills follow [semver](https://semver.org/): MAJOR.MINOR.PATCH.

- **MAJOR** — breaking change to skill behavior or required inputs
- **MINOR** — new capability, backward-compatible
- **PATCH** — clarifications, typo fixes, small improvements

Agents should check this file on session start and warn the user if 2+ skills have minor-or-greater updates since last seen.

## Pack version

**cti-skills:** 1.0.0 (2026-04-20)

## Skills

### Analytical techniques
| Skill | Version | Last updated |
|---|---|---|
| `ach` | 1.0.0 | 2026-04-20 |
| `horizon-scanning` | 1.0.0 | 2026-04-20 |
| `key-assumptions-check` | 1.0.0 | 2026-04-20 |
| `red-team-analysis` | 1.0.0 | 2026-04-20 |
| `source-assessment` | 1.0.0 | 2026-04-20 |
| `structured-analytic-techniques` | 1.0.0 | 2026-04-20 |
| `threat-assessment` | 1.0.0 | 2026-04-20 |

### CTI tradecraft
| Skill | Version | Last updated |
|---|---|---|
| `campaign-tracking` | 1.0.0 | 2026-04-20 |
| `darkweb-collection` | 2.0.0 | 2026-04-28 |
| `indicator-pivoting` | 2.0.0 | 2026-04-28 |
| `malware-analysis` | 1.0.0 | 2026-04-20 |
| `osint-methodology` | 1.0.0 | 2026-04-20 |
| `threat-actor-profiling` | 1.0.0 | 2026-04-20 |
| `vulnerability-intelligence` | 1.0.0 | 2026-04-20 |

### Hyperloop
| Skill | Version | Last updated |
|---|---|---|
| `cti-hyperloop` | 1.0.0 | 2026-04-20 |

### Knowledge cells
Knowledge cells decay faster than other skills — update the `Last updated` column whenever you refresh intel. Agents should warn if a knowledge cell is >90 days stale.

| Skill | Version | Last updated |
|---|---|---|
| `carding-financial-fraud` | 1.0.0 | 2026-04-20 |
| `china-cyber-espionage` | 1.0.0 | 2026-04-20 |
| `dprk-cyber-espionage` | 1.0.0 | 2026-04-20 |
| `hacktivism` | 1.0.0 | 2026-04-20 |
| `infostealers` | 1.0.0 | 2026-04-20 |
| `initial-access-brokers` | 1.0.0 | 2026-04-20 |
| `iran-cyber-espionage` | 1.0.0 | 2026-04-20 |
| `phishing-social-engineering` | 1.0.0 | 2026-04-20 |
| `ransomware-ecosystem` | 1.0.0 | 2026-04-20 |
| `russia-cyber-espionage` | 1.0.0 | 2026-04-20 |
| `supply-chain-threats` | 1.0.0 | 2026-04-20 |

### Management
| Skill | Version | Last updated |
|---|---|---|
| `feedback-loops` | 1.0.0 | 2026-04-20 |
| `intelligence-sharing` | 1.0.0 | 2026-04-20 |
| `maturity-assessment` | 1.0.0 | 2026-04-20 |
| `pir-management` | 1.0.0 | 2026-04-20 |
| `quality-control` | 1.0.0 | 2026-04-20 |
| `sops` | 1.0.0 | 2026-04-20 |
| `stakeholder-management` | 1.0.0 | 2026-04-20 |

### Production
| Skill | Version | Last updated |
|---|---|---|
| `confidence-levels` | 1.0.0 | 2026-04-20 |
| `intelligence-writing` | 1.0.0 | 2026-04-20 |
| `ioc-enrichment-workflow` | 2.0.0 | 2026-04-28 |
| `ioc-export` | 1.0.0 | 2026-04-20 |
| `kql-writing` | 1.0.0 | 2026-04-20 |
| `likelihood-language` | 1.0.0 | 2026-04-20 |
| `sigma-writing` | 1.0.0 | 2026-04-20 |
| `stix-bundle` | 1.0.0 | 2026-04-20 |
| `tlp-guide` | 1.0.0 | 2026-04-20 |
| `writing-assessments` | 1.0.0 | 2026-04-20 |
| `yara-writing` | 1.0.0 | 2026-04-20 |

### Orchestrator + investigation skills (new in Phase C)
| Skill | Version | Last updated |
|---|---|---|
| `cti-orchestrator` | 1.0.0 | 2026-04-20 |
| `ip-investigation` | 1.0.0 | 2026-04-20 |
| `domain-investigation` | 1.1.0 | 2026-04-26 |
| `hash-investigation` | 1.0.0 | 2026-04-20 |
| `url-investigation` | 1.0.0 | 2026-04-20 |

### Lookup skills (external API wrappers)
| Skill | Version | Last updated |
|---|---|---|
| `lookup-abuseipdb` | 1.0.0 | 2026-04-20 |
| `lookup-censys` | 1.0.0 | 2026-04-20 |
| `lookup-greynoise` | 1.0.0 | 2026-04-20 |
| `lookup-otx` | 1.0.0 | 2026-04-20 |
| `lookup-shodan` | 1.0.0 | 2026-04-20 |
| `lookup-misp` | 1.0.0 | 2026-04-26 |
| `lookup-ransomwarelive` | 1.0.0 | 2026-04-26 |
| `lookup-reversinglabs` | 1.0.0 | 2026-05-08 |
| `lookup-urlscan` | 1.0.0 | 2026-04-20 |
| `lookup-virustotal` | 1.0.0 | 2026-04-20 |
| `mitre-attack` | 1.0.0 | 2026-04-20 |

### Legacy tool-API reference skills (superseded by `lookup-*` in Phase B)
These remain for reference but agents should prefer the `lookup-*` skills above. Will be removed in a future cleanup.

| Skill | Version | Last updated | Status |
|---|---|---|---|
| `abuseipdb-api` | 1.0.0 | 2026-04-20 | superseded by `lookup-abuseipdb` |
| `censys-api` | 1.0.0 | 2026-04-20 | superseded by `lookup-censys` |
| `greynoise-api` | 1.0.0 | 2026-04-20 | superseded by `lookup-greynoise` |
| `otx-api` | 1.0.0 | 2026-04-20 | superseded by `lookup-otx` |
| `reversinglabs-api` | 1.0.0 | 2026-05-08 | reference companion to `lookup-reversinglabs` |
| `shodan-api` | 1.0.0 | 2026-04-20 | superseded by `lookup-shodan` |
| `urlscan-api` | 1.0.0 | 2026-04-20 | superseded by `lookup-urlscan` |
| `virustotal-api` | 1.0.0 | 2026-04-20 | superseded by `lookup-virustotal` |

## Changelog

### 1.7.0 — 2026-05-08
- Added `lookup-reversinglabs` skill wrapping the ReversingLabs Spectra Analyze (A1000) API. Covers hash classification, detailed reports (incl. MITRE ATT&CK mapping, TitaniumCore static analysis, sandbox results), file/URL submission with optional polling, network threat intelligence for URLs/domains/IPs, advanced search for pivoting by threatname/AV-signature/family, parent-container and extracted-file relationships, and read-only YARA-ruleset matches. SDK-backed Python CLI at `tools/clis/reversinglabs.py` with self-bootstrapping venv. Reads `$REVERSINGLABS_USER` + `$REVERSINGLABS_PASSWORD` (+ optional `$REVERSINGLABS_HOST`); SDK auto-exchanges credentials for a token via `/api-token-auth/`. Source reliability defaults to A2 with B3 downgrade rules for `unknown`/`suspicious` verdicts and very fresh samples. Added companion `reversinglabs-api` reference skill (non-invokable). Cross-referenced from `/ip-investigation`, `/domain-investigation`, `/hash-investigation`, `/url-investigation`, and `/indicator-pivoting`. No Node CLI — RL has no upstream Node SDK and auth requires the token exchange.

### 1.6.0 — 2026-04-29
- Backfilled trigger phrases in 34 user-invocable skill descriptions that pre-dated the [`CONTRIBUTING.md`](CONTRIBUTING.md) line-44 convention. Affected: `campaign-tracking`, `carding-financial-fraud`, `china-cyber-espionage`, `confidence-levels`, `cti-hyperloop`, `dprk-cyber-espionage`, `hacktivism`, `horizon-scanning`, `infostealers`, `initial-access-brokers`, `intelligence-sharing`, `intelligence-writing`, `iran-cyber-espionage`, `key-assumptions-check`, `kql-writing`, `likelihood-language`, `malware-analysis`, `maturity-assessment`, `phishing-social-engineering`, `pir-management`, `ransomware-ecosystem`, `red-team-analysis`, `russia-cyber-espionage`, `sigma-writing`, `sops`, `source-assessment`, `stakeholder-management`, `structured-analytic-techniques`, `supply-chain-threats`, `threat-actor-profiling`, `tlp-guide`, `vulnerability-intelligence`, `writing-assessments`, `yara-writing`. Each description now starts with "Use when…" or contains "when the user…" so an orchestrator can match user intent against the frontmatter. No version bump per skill (description-only edit), but adds an 11th check to the auditor — `description-trigger` — that warns on user-invocable skills missing a trigger phrase. Skips `user-invocable: false` (library / pipeline skills loaded by other skills, not surfaced to user routing). Auditor reports 0 FAIL / 0 WARN at end of release.

### 1.5.0 — 2026-04-28
- Added `tools/audit-integrations.py` — stdlib auditor that parses `tools/REGISTRY.md` as the source of truth and runs ten checks across the codebase (registry/disk consistency, integration-guide presence, CLI presence, `VERSIONS.md` coverage, dead `*-agent` references, unknown `/lookup-*` references, `cti-setup` env-var coverage, `scripts/setup.sh` env-var coverage, composite-skill cross-reference coverage, and "the N services" cardinality drift). Wired into `validate-skills.sh` as a non-fatal step. Documented the add/update/remove integration workflow in `CONTRIBUTING.md`. Sweep-cleanup driven by the auditor in this same release: `ioc-enrichment-workflow` 2.0.0 (18 retired `*-agent` references replaced with `/lookup-*` skill names; expanded routing tables; added `lookup-misp` and `lookup-ransomwarelive` correlation steps); `ip-investigation` / `domain-investigation` / `hash-investigation` / `url-investigation` now cross-reference `/lookup-misp` for internal-correlation; `osint-methodology`, `campaign-tracking`, `vulnerability-intelligence`, `threat-actor-profiling`, and `malware-analysis` gained "Related skills" sections that route into the current `/lookup-*` set, `/indicator-pivoting`, and `/darkweb-collection`. Auditor reports 0 FAIL / 0 WARN at end of release.

### 1.4.0 — 2026-04-28
- `indicator-pivoting` 2.0.0 — overhauled to use the current `/lookup-*` skills (the prior version routed to the retired `*-agent` agents) and to include concrete CLI invocations per pivot type. Added decision trees + commands for four new starting indicator types: URL, TLS certificate (SHA-256/CN), registrant email/org, and actor/family/campaign label. Added a Telegram-handle / .onion starting point that hands off to `/darkweb-collection`. New "Pivot routing — by goal" table maps every common pivot to its first-/second-choice lookup. Added a five-hop worked example (phish URL → APT cluster) with real CLI commands and per-hop confidence scoring. Refreshed pivot-quality table (added JARM, JA3, MITRE-technique-overlap caveats) and pivot-documentation template. MAJOR bump because the routing table and frontmatter description changed in ways that prior callers should re-read.

### 1.3.0 — 2026-04-28
- `darkweb-collection` 2.0.0 — substantial expansion. Restructured into `SKILL.md` + `references/` + `scripts/` (first skill in the pack to use the subdir layout). New material: 37 sourced underground forums across 8 categories (`references/forums.md`), 34 sourced Telegram channels across 6 categories (`references/telegram-channels.md`), vendor-first access matrix covering 13 commercial CTI vendors plus a DIY Tails/Whonix/Tor/Telethon playbook (`references/access-methods.md`), handler-side OPSEC primer including persona separation, stylometry, mental-health framing, and explicit out-of-scope statement for CSAM/terrorism/violent-extremist content (`references/opsec.md`), and passive-monitoring strategy with selector taxonomy + cadence table + storage schema (`references/passive-monitoring.md`). Three new stdlib-only Python CLIs under `scripts/`: `onion_search.py` (clearnet search of Ahmia + dark.fail + IntelligenceX onion indexers), `telegram_monitor.py` (read-only Telethon channel monitor; light dep), `keyword_match.py` (local regex/keyword scanner over collected JSONL). Reads `INTELX_API_KEY` (optional, freemium) and `TELEGRAM_API_ID`/`TELEGRAM_API_HASH`/`TELEGRAM_SESSION` (for Telegram monitor). MAJOR bump because the skill's frontmatter description, file layout, and recommended posture all changed; prior callers relying on the v1 single-file shape need to re-read.

### 1.2.0 — 2026-04-26
- `domain-investigation` 1.1.0 — chains `/lookup-ransomwarelive search` against an org-candidate derived from the domain's apex, surfaces `ransomware_status` in the consolidated output, and adds a "Ransomware-claim hits" handling section covering name-collision risk and the metadata-vs-description credibility split.
- Added `lookup-ransomwarelive` skill wrapping ransomware.live's PRO API. Covers victim search/recent/detail (27k+ leak-site claims across 330+ groups), group listings + rich `group-profile` (description, TTPs, tools, leak-site `.onion` infra, vulnerabilities), per-group IOC dumps, YARA rules with full content, ransom-note samples, negotiation chats, press archive, sector reference, and country CSIRT contacts. Stdlib-only Python CLI at `tools/clis/ransomwarelive.py`. Reads `$RANSOMWARE_LIVE`. Source reliability defaults to B2 with credibility nuance: metadata is B2, criminal-written `description` field is B3–B4 (often inflated). Total skill count: 67 (66 active + `stix-bundle` reference).

### 1.1.0 — 2026-04-26
- Added `lookup-misp` skill with two-way MISP integration (the first write-capable lookup skill in the pack). Covers query (`search-events`, `search-attributes`, `search-objects`, `get-event`, `list-tags`) and write (`add-attribute`, `create-event`, `upload-stix`, `tag-event`, `publish-event`). Supports STIX 2 round-tripping — `upload-stix` consumes bundles produced by `/stix-bundle`, and `search-events --returnFormat stix2` exports MISP events as STIX. Stdlib-only Python CLI at `tools/clis/misp.py`. Reads `$MISP_URL` and `$MISP_API_KEY`. Self-signed-cert support via `--insecure`. Total skill count: 65 active + 1 reference (`stix-bundle`).

### 1.0.0 — 2026-04-20
- Initial versioned release
- 52 skills across analytical techniques, CTI tradecraft, knowledge cells, production, management, and tool APIs
- Phase B: 7 new `lookup-*` skills wrap each external threat-intel API (VirusTotal, OTX, URLScan, Shodan, AbuseIPDB, GreyNoise, Censys). Paired with zero-dep Node CLIs under `tools/clis/` and integration docs under `tools/integrations/`. The 7 legacy tool-API agents (`.claude/agents/*-agent.md`) moved to `archive/agents/`.
- Phase C: new `cti-orchestrator` skill as the default entry point. Four investigation skills (`ip-investigation`, `domain-investigation`, `hash-investigation`, `url-investigation`) compose lookups, auto-apply rigor pipeline (source-assessment, tlp-guide, confidence-levels, likelihood-language), and prioritize follow-up IOCs. All 64 skills flattened from `.claude/skills/<category>/<name>/` to top-level `skills/<name>/` (Agent Skills spec layout). Old `cti-orchestrator` agent archived; 6 remaining agents (analyst, report-writer, quality-reviewer, osint-researcher, ioc-processor, detection-engineer) kept in `.claude/agents/` as optional Claude-Code-specific specialist subagents.
- Phase D (partial): added `package.json` + `bin/cti-skills.js` so `npx github:Liberty91LTD/cti-skills` installs the pack into any directory. Subcommands: `install` (default), `add <skill>`, `list`, `update`, `help`. Accepts `--target <dir>`.
- Repo transferred from `renzejongman/cti-agentic-skills` to `Liberty91LTD/cti-skills`
- Added MIT LICENSE, plugin manifest, skill validator, cross-agent AGENTS.md
