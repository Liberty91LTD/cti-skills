# cti-skills

Cyber Threat Intelligence skills for Claude Code and AI agents. Threat actor profiling, IOC investigation, OSINT methodology, detection engineering (SIGMA/YARA/KQL), intelligence writing, and self-updating knowledge cells on nation-state and cybercrime threats.

Built by [Liberty91 Ltd](https://liberty91.com). MIT-licensed. Works in Claude Code, Cursor, Codex, Windsurf — any agentic IDE that supports [Agent Skills](https://agentskills.io/specification).

## What's in the pack

- **52 skills** covering analytical tradecraft, CTI methodology, detection engineering, intelligence production, and living knowledge cells on China, Russia, Iran, DPRK cyber espionage, ransomware, infostealers, initial access brokers, and more.
- **7 threat-intel integrations** — VirusTotal, URLScan.io, Shodan, AbuseIPDB, GreyNoise, AlienVault OTX, Censys. Each exposed as a lookup skill any other skill can chain.
- **Local MITRE ATT&CK dataset** — TTP mapping without network calls.
- **Tradecraft vocabularies** — TLP, NATO Admiralty Scale, MISP confidence, probability yardstick. Auto-applied by the orchestrator; also invokable directly.
- **A single orchestrator skill** that routes requests and auto-applies rigor to every output.

## Install

Pick whichever works for your stack.

### Claude Code plugin (recommended)

```bash
/plugin marketplace add Liberty91LTD/cti-skills
/plugin install cti-skills
```

### Git clone

```bash
git clone git@github.com:Liberty91LTD/cti-skills.git
cd cti-skills
./scripts/setup.sh      # prompts for optional API keys + downloads MITRE data
claude
```

### Git submodule (for embedding in an existing repo)

```bash
git submodule add https://github.com/Liberty91LTD/cti-skills.git skills/cti
```

### Fork

Hit "Fork" on GitHub, then install via plugin or clone from your fork.

### Direct copy

Copy the `skills/` directory into your own project. Each skill is self-contained.

### Cursor, Codex, Windsurf, other Agent Skills-compatible IDEs

Clone the repo into your agent skills directory per your IDE's documentation. The orchestrator is itself a skill — no Claude-specific subagent required.

## Try it

Once installed:

```
Investigate 203.0.113.42
```
The orchestrator routes this to `/ip-investigation`, which chains `/lookup-virustotal` + `/lookup-otx` + `/lookup-shodan` + `/lookup-abuseipdb` + `/lookup-greynoise`, scores sources, applies TLP, and returns a rated investigation report.

```
Profile APT28
```
Routes to `/threat-actor-profile` — produces an actor card with aliases, targeting, TTPs, attribution confidence.

```
/ach
```
Direct-invoke Analysis of Competing Hypotheses.

```
/iran-cyber-espionage
```
Load the Iran knowledge cell.

```
/pir-management
```
Set up Priority Intelligence Requirements.

## Pick a skill

Skills are organized flat (in Phase C) but currently grouped. Browse:

- **Investigation** — `/ip-investigation`, `/domain-investigation`, `/hash-investigation`, `/url-investigation` *(coming in Phase C)*
- **Analysis** — `/threat-actor-profile`, `/ach`, `/indicator-pivoting`, `/campaign-tracking`, `/malware-analysis`, `/threat-assessment`, `/horizon-scanning`, `/key-assumptions-check`, `/red-team-analysis`, `/structured-analytic-techniques`
- **Tradecraft rigor** — `/apply-tlp`, `/score-source`, `/confidence-language` *(currently `confidence-levels`)*, `/likelihood-language`
- **Production** — `/intelligence-writing`, `/writing-assessments`, `/quality-control`, `/ioc-export`, `/stix-bundle`, `/ioc-enrichment-workflow`
- **Detection engineering** — `/sigma-writing`, `/yara-writing`, `/kql-writing`
- **Knowledge cells** — `/china-cyber-espionage`, `/russia-cyber-espionage`, `/iran-cyber-espionage`, `/dprk-cyber-espionage`, `/ransomware-ecosystem`, `/infostealers`, `/initial-access-brokers`, `/phishing-social-engineering`, `/supply-chain-threats`, `/carding-financial-fraud`, `/hacktivism`
- **OSINT + collection** — `/osint-methodology`, `/darkweb-collection`, `/vulnerability-intelligence`
- **Lookups** — `/lookup-virustotal`, `/lookup-otx`, `/lookup-urlscan`, `/lookup-shodan`, `/lookup-abuseipdb`, `/lookup-greynoise`, `/lookup-censys`, `/mitre-attack` *(coming in Phase B)*
- **Management** — `/pir-management`, `/stakeholder-management`, `/feedback-loops`, `/sops`, `/maturity-assessment`, `/intelligence-sharing`, `/quality-control`
- **Methodology** — `/cti-hyperloop` (optional operating doctrine)

## API keys

Optional. The pack degrades gracefully — skills skip enrichments for which no key is configured.

| Service | Env variable | Free tier |
|---|---|---|
| VirusTotal | `VIRUSTOTAL_API_KEY` | 4 req/min, 500/day |
| URLScan.io | `URLSCAN_API_KEY` | 100 scans/day |
| Shodan | `SHODAN_API_KEY` | 1 req/sec |
| AbuseIPDB | `ABUSEIPDB_API_KEY` | 1000 checks/day |
| GreyNoise | `GREYNOISE_API_KEY` | 50 req/day |
| AlienVault OTX | `OTX_API_KEY` | 10,000 req/hour |
| Censys | `CENSYS_API_ID` + `CENSYS_API_SECRET` | 250 queries/month |

`./scripts/setup.sh` walks you through configuration. Keys land in `.claude/settings.local.json` (gitignored). Environment variables work too.

## Contributing

Forks and PRs welcome from anyone. Merges reserved to Liberty91 Ltd maintainers. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Status

Version 1.0.0 — see [VERSIONS.md](VERSIONS.md) for per-skill versions and changelog.

Active restructure: this repo is transitioning from a 14-agent hierarchical architecture to a flat-skill + single-orchestrator model. Some invocations listed above (the `lookup-*` skills, investigation skills) ship in Phase B/C.

## License

MIT — see [LICENSE](LICENSE).

## About Liberty91

[Liberty91 Ltd](https://liberty91.com) builds AI-native threat intelligence tooling. Contact: contact@liberty91.com.
