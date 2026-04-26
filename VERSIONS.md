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
| `darkweb-collection` | 1.0.0 | 2026-04-20 |
| `indicator-pivoting` | 1.0.0 | 2026-04-20 |
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
| `ioc-enrichment-workflow` | 1.0.0 | 2026-04-20 |
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
| `shodan-api` | 1.0.0 | 2026-04-20 | superseded by `lookup-shodan` |
| `urlscan-api` | 1.0.0 | 2026-04-20 | superseded by `lookup-urlscan` |
| `virustotal-api` | 1.0.0 | 2026-04-20 | superseded by `lookup-virustotal` |

## Changelog

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
