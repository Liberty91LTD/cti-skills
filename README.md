# cti-skills

Cyber Threat Intelligence skills for Claude Code and AI agents. Threat actor profiling, IOC investigation, OSINT methodology, detection engineering (SIGMA/YARA/KQL), intelligence writing, and self-updating knowledge cells on nation-state and cybercrime threats.

Built by [Liberty91 Ltd](https://liberty91.com). MIT-licensed. Works in Claude Code, Cursor, Codex, Windsurf — any agentic IDE that supports [Agent Skills](https://agentskills.io/specification).

## What is this? (the simple version)

Imagine you're investigating something suspicious on the internet — a weird link in an email, an IP address that keeps trying to log into your server, or a hacking group you read about in the news. Normally you'd open ten different websites, copy-paste between them, write up notes, and try to remember the right way to score what you found.

This pack teaches Claude Code (an AI coding assistant) how to do all of that for you. You type a question in plain English, and Claude:

1. **Looks the thing up** in seven trusted threat-intel databases (VirusTotal, Shodan, AbuseIPDB, and others).
2. **Pulls together** what they all say about it.
3. **Writes you a report** in the format real threat analysts use — with confidence ratings, sources, and a clear bottom line.

You don't need to know which database to use. You don't need to know how to score a source. The pack handles the boring parts so you can focus on the thinking.

## How to use it (5 steps)

1. **Install Claude Code** if you don't have it: https://claude.com/claude-code
2. **Install this pack** in Claude Code:
   ```
   /plugin marketplace add Liberty91LTD/cti-skills
   /plugin install cti-skills
   ```
3. **Add your API keys** (free signups, all optional). Inside Claude Code, type:
   ```
   /cti-setup
   ```
   Claude will walk you through it. Or skip this and the pack still works — it just won't be able to do live lookups.
4. **Ask a question.** Examples:
   ```
   investigate 8.8.8.8
   profile the threat actor APT28
   write a flash report on this URL: http://example.com/login
   what do we know about Lazarus Group?
   ```
5. **Read the report.** Claude returns a structured analysis with confidence levels, sources, and recommended next steps.

That's it. If you get stuck, type `/cti-setup` to fix keys, or `npx github:Liberty91LTD/cti-skills list` to see every skill the pack has.

## What's in the pack

- **65 skills** covering analytical tradecraft, CTI methodology, detection engineering, intelligence production, and living knowledge cells on China, Russia, Iran, DPRK cyber espionage, ransomware, infostealers, initial access brokers, and more.
- **7 threat-intel integrations** — VirusTotal, URLScan.io, Shodan, AbuseIPDB, GreyNoise, AlienVault OTX, Censys. Each exposed as a lookup skill any other skill can chain.
- **Local MITRE ATT&CK dataset** — TTP mapping without network calls.
- **Tradecraft vocabularies** — TLP, NATO Admiralty Scale, MISP confidence, probability yardstick. Auto-applied by the orchestrator; also invokable directly.
- **A single orchestrator skill** that routes requests and auto-applies rigor to every output.

## Install

The recommended path for Claude Code users is the plugin. Other paths are listed below for non-Claude-Code IDEs and embedding scenarios.

### Claude Code plugin (recommended)

```bash
/plugin marketplace add Liberty91LTD/cti-skills
/plugin install cti-skills
```

Then run `/cti-setup` inside Claude Code to add API keys.

### npx (one-shot install into any project)

```bash
npx github:Liberty91LTD/cti-skills
```
Copies all 65 skills + tool integrations + plugin manifest into the current directory. Use `--target <dir>` to install elsewhere, or `npx github:Liberty91LTD/cti-skills list` to browse skills first.

### Git clone (for development or contribution)

```bash
git clone git@github.com:Liberty91LTD/cti-skills.git
cd cti-skills
./scripts/setup.sh      # prompts for optional API keys + downloads MITRE data
claude
```

`setup.sh` supports non-interactive use too:

```bash
# Pass keys as flags
./scripts/setup.sh --non-interactive --virustotal=KEY --shodan=KEY

# Pass keys as env vars
VIRUSTOTAL_API_KEY=KEY SHODAN_API_KEY=KEY ./scripts/setup.sh --non-interactive

# Verify configured keys (dry-run, no API calls)
./scripts/setup.sh --verify
```

The script merges keys into `.claude/settings.local.json` non-destructively — existing fields like `permissions` are preserved. Re-run anytime to add more keys.

### Other install paths

- **Git submodule** (embed in another repo): `git submodule add https://github.com/Liberty91LTD/cti-skills.git skills/cti`
- **Fork**: hit "Fork" on GitHub, then install via plugin or clone from your fork.
- **Direct copy**: copy the `skills/` directory into your project. Each skill is self-contained.
- **Cursor, Codex, Windsurf, other Agent-Skills-compatible IDEs**: clone the repo into your agent skills directory per your IDE's documentation. The orchestrator is itself a skill — no Claude-specific subagent required.

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

All skills live flat under `skills/` and are user-invocable as `/<skill-name>`. Grouped here for browsing:

- **Entry point** — `/cti-orchestrator` (default routing), `/cti-setup` (configure API keys)
- **Investigation** — `/ip-investigation`, `/domain-investigation`, `/hash-investigation`, `/url-investigation`
- **Analysis** — `/threat-actor-profiling`, `/ach`, `/indicator-pivoting`, `/campaign-tracking`, `/malware-analysis`, `/threat-assessment`, `/horizon-scanning`, `/key-assumptions-check`, `/red-team-analysis`, `/structured-analytic-techniques`
- **Tradecraft rigor** — `/tlp-guide`, `/source-assessment`, `/confidence-levels`, `/likelihood-language`
- **Production** — `/intelligence-writing`, `/writing-assessments`, `/quality-control`, `/ioc-export`, `/stix-bundle`, `/ioc-enrichment-workflow`
- **Detection engineering** — `/sigma-writing`, `/yara-writing`, `/kql-writing`
- **Knowledge cells** — `/china-cyber-espionage`, `/russia-cyber-espionage`, `/iran-cyber-espionage`, `/dprk-cyber-espionage`, `/ransomware-ecosystem`, `/infostealers`, `/initial-access-brokers`, `/phishing-social-engineering`, `/supply-chain-threats`, `/carding-financial-fraud`, `/hacktivism`
- **OSINT + collection** — `/osint-methodology`, `/darkweb-collection`, `/vulnerability-intelligence`
- **Lookups** — `/lookup-virustotal`, `/lookup-otx`, `/lookup-urlscan`, `/lookup-shodan`, `/lookup-abuseipdb`, `/lookup-greynoise`, `/lookup-censys`, `/lookup-misp` (two-way: query + write), `/lookup-ransomwarelive`, `/mitre-attack`
- **Management** — `/pir-management`, `/stakeholder-management`, `/feedback-loops`, `/sops`, `/maturity-assessment`, `/intelligence-sharing`
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
| MISP | `MISP_URL` + `MISP_API_KEY` | host-bound (your instance) |
| Ransomware.live | `RANSOMWARE_LIVE` | 3,000/day (PRO) |

Three ways to configure:

1. **Inside Claude Code** (works for all install paths): type `/cti-setup` and Claude walks you through it.
2. **Shell script** (clone install only): `./scripts/setup.sh` — interactive prompts, or use `--non-interactive --virustotal=KEY` flags for scripted setup.
3. **Environment variables**: export the variable in your shell rc; the CLIs read them at runtime.

Keys are merged into `.claude/settings.local.json` (gitignored). The pack degrades gracefully — skills skip enrichments for which no key is configured.

To verify keys are wired up: `./scripts/setup.sh --verify` (or ask Claude to verify after `/cti-setup`).

## Contributing

Forks and PRs welcome from anyone. Merges reserved to Liberty91 Ltd maintainers. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Status

Version 1.0.0 — see [VERSIONS.md](VERSIONS.md) for per-skill versions and changelog.

## License

MIT — see [LICENSE](LICENSE).

## About Liberty91

[Liberty91 Ltd](https://liberty91.com) builds AI-native threat intelligence tooling. Contact: contact@liberty91.com.
