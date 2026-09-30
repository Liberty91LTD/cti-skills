# cti-skills

Cyber Threat Intelligence skills for Claude Code and AI agents. Threat actor profiling, IOC investigation, OSINT methodology, detection engineering (SIGMA/YARA/KQL), intelligence writing, and self-updating knowledge cells on nation-state and cybercrime threats.

Built by [Liberty91 Ltd](https://liberty91.com). MIT-licensed. Works in Claude Code, Cursor, Codex, Windsurf — any agentic IDE that supports [Agent Skills](https://agentskills.io/specification).

## What is this? (the simple version)

Imagine you're investigating something suspicious on the internet — a weird link in an email, an IP address that keeps trying to log into your server, or a hacking group you read about in the news. Normally you'd open ten different websites, copy-paste between them, write up notes, and try to remember the right way to score what you found.

This pack teaches Claude Code (an AI coding assistant) how to do all of that for you. You type a question in plain English, and Claude:

1. **Looks the thing up** in fourteen trusted threat-intel sources (Liberty91, VirusTotal, Shodan, AbuseIPDB, and others) — and, if you connect your Microsoft Sentinel, in your own logs too.
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

- **78 skills** covering analytical tradecraft, CTI methodology, detection engineering, intelligence production, and living knowledge cells on China, Russia, Iran, DPRK cyber espionage, ransomware, infostealers, initial access brokers, and more.
- **14 threat-intel integrations** — Liberty91, VirusTotal, URLScan.io, Shodan, AbuseIPDB, GreyNoise, AlienVault OTX, Censys, MISP, OpenCTI, Ransomware.live, ReversingLabs, CrowdStrike Falcon Intelligence, Microsoft Sentinel. Each exposed as a lookup skill any other skill can chain.
- **Local MITRE ATT&CK dataset** — TTP mapping without network calls.
- **Tradecraft vocabularies** — TLP, NATO Admiralty Scale, MISP confidence, probability yardstick. Auto-applied by the orchestrator; also invokable directly.
- **Evidence grading by default** — provenance resolved by script or platform, claims anchored to source sentences, grades from a published rubric with hard caps. Hypothesis testing and assessments grade their evidence first, and label the result when you skip it.
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
Copies all 78 skills + tool integrations + plugin manifest into the current directory. Use `--target <dir>` to install elsewhere, or `npx github:Liberty91LTD/cti-skills list` to browse skills first.

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

## Harnesses

The pack is plain Agent Skills files. Any harness that loads skills, can run a shell command and read files, and calls tools reliably will run it.

| Harness | Notes |
|---|---|
| Claude Code | Plugin install, above. Optional subagents in `.claude/agents/`. |
| Codex, Cursor, Windsurf, OpenCode, Goose | Clone into the agent's skills directory. The orchestrator is itself a skill. |
| Hermes Agent and other self-improving harnesses | Loads the pack. Enable write approval, or disable skill self-modification, for the `cti-skills` directory, so the tradecraft skills stay stable and reviewable. |
| Local models | Claude Code with `ANTHROPIC_BASE_URL` pointed at Ollama, Codex with `--oss`, and similar. See the FAQ for what to expect. |
| Headless | `claude -p` with an allowlist of tools, for scheduled or triggered runs. |

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
How reliable is this? https://example-news-site.com/2026/09/some-article
```
Routes to `/quality-of-information-check` — traces the article to its originating source, splits the report into claims, and grades each claim in words, on how the source knows and what backs the statement, with a rationale.

```
/ach
```
Direct-invoke Analysis of Competing Hypotheses. Hand it URLs or text and it grades the evidence first.

```
/iran-cyber-espionage
```
Load the Iran knowledge cell.

```
/pir-management
```
Set up Priority Intelligence Requirements.

## What's new in 2.0

### Quality of Information Check — `/quality-of-information-check`

**Grade the evidence before you reason about it.** `/quality-of-information-check` resolves any article back to its originating source, splits the report into individual claims, and grades each claim with a stated rationale. The grade has two elements, written in words: access level (how the source knows) and claim support (what backs the statement). It is not an Admiralty rating: it rests on what the document says about how the finding was made, not on the source's track record. Five outlets citing one vendor report count as one source. Caveats the press dropped in transmission are restored. Anything that cannot be traced to a primary is capped, not guessed. `/ach` and `/threat-assessment` now grade their evidence first by default.

Works on any URL, with no API key: the skill resolves the chain for the article you gave it and tells you exactly what it could not verify. Platform-resolved provenance, where a Liberty91 key returns the chain and the count of independent sources across the whole deduplicated event, is built into the skills and switches on when the platform serves those fields.

Cross-vendor name matching (APT28 to Sednit, UNC to named group) uses your own alias file, or the Liberty91 Threat Library with an API key.

New to this? [How evidence grading works, in plain English](docs/how-evidence-grading-works.md) explains it without the jargon.

**Three skills, usable separately:**

- **`/source-provenance`** — where did this actually come from? A script follows the article's links and named attributions to the originating document and returns the chain, the primary's own access and confidence language, and every hop it could not resolve.
- **`/claim-extraction`** — what does this report actually claim? Five to twelve atomic claims, typed as observation, attribution, assessment, actor claim or victim disclosure, each anchored to the exact source sentence.
- **`/quality-of-information-check`** — the two above, plus transmission fidelity, corroboration counted by independent primaries, a fixed grading rubric, a deception screen, and machine-readable output.

**What changed for existing users.** `/ach`, `/threat-assessment` and `/writing-assessments` prefer graded evidence. Hand them a URL and they run the check first. Ask them to skip it and they still run: the output is labelled ungraded and capped at Moderate confidence. On graded evidence, an assessment's confidence can no longer exceed what its weakest load-bearing claim supports, and a hit in your own telemetry counts as the strongest evidence there is. `/red-team-analysis` is now `/devils-advocacy`, which is what it always did. STIX and MISP exports carry grades per claim. Details in [VERSIONS.md](VERSIONS.md).

Every output is labelled `platform-resolved`, `script-resolved` or `model-judged`, and the label travels into whatever is built on it.

## Earlier additions

Three additions along one arc: knowing what is coming at you, knowing whether you can stop it — and now, knowing whether it already reached you.

### 0. Microsoft Sentinel hunting — `/lookup-sentinel`

**What it is.** Every other integration in this pack asks the world about an indicator. This one asks **your own telemetry**: has this IOC been seen in our environment? Is this ATT&CK technique's behaviour in our logs? It connects to your Microsoft Sentinel workspace (read-only) and turns intelligence findings into exposure answers.

**The idea that makes it different.** No two Sentinel environments have the same tables — availability follows the connectors you've deployed. So the skill **discovers before it hunts**: it inventories which tables your workspace actually ingests, probes the candidates, and only then generates KQL, restricted to tables that verifiably exist. No queries that fail on missing tables; no hunts that silently "succeed" against telemetry you don't collect. When your environment *can't* observe a technique, it tells you that — a telemetry-gap finding is often the most valuable line in the report.

**What you get:**

- **IOC exposure sweeps** — hand it the malicious subset from an investigation or `/ioc-enrichment-workflow` and it sweeps IPs, domains, hashes, URLs, and accounts across every relevant table your workspace has, with fallback ladders when the preferred table is absent.
- **Behavioural TTP hunts** — from a MITRE ATT&CK technique to table-adapted KQL, composed with `/kql-writing`'s per-technique patterns and `/mitre-attack`'s local dataset.
- **Honest misses** — a clean sweep is reported as "not observed in collected telemetry over this window", never "not compromised", with retention and connector coverage stated.

Setup: four values from the Azure portal (app registration + a read-only role on the workspace) — the walkthrough is in [`tools/integrations/sentinel.md`](tools/integrations/sentinel.md).

### 1. Liberty91 platform integration — `/lookup-liberty91`

**What it is.** The pack's only **first-party** integration. Where VirusTotal tells you whether an indicator is bad, Liberty91 tells you *what happened, who reported it, how well corroborated it is, and which of your organizations it touches*.

**The idea that makes it different.** Everything else in the pack works on indicators. This works on **occurrences**. One breach covered by a vendor write-up, three news articles and a leak-site post is **one Threat Event and five Events**. You read the occurrence once, with the disagreement between sources still visible, instead of deduplicating five reports by hand.

**What you get:**

- **Deduplicated occurrences** with every source you are entitled to, each carrying NATO Admiralty source reliability, occurrence credibility, a verification stage, and a per-report stance (claims / corroborates / disputes). When sources disagree, the skill reports the dispute rather than averaging it away.
- **ATT&CK techniques per occurrence, with a note on how each was actually used** in that specific event, not a generic definition. This is the single most useful field for turning "an actor targets aviation" into "here is what they did".
- **Named actors, malware, vulnerabilities and victims** on every list row, keyed to a canonical cross-tenant catalog, so you can pivot straight from a result to the full entity record.
- **Two-way**: push your own finished reports back in with `ingest`, and they are enriched, entity-extracted and matched into an occurrence, private to your account.

**Why it matters for the pack.** It supplies the *Threat Capability* evidence that `/control-coverage-mapping` below needs, and it is the only source here that can say what is happening to **your** sector and region rather than the world in general.

Setup: one key, `LIBERTY91_API_KEY`. Full reference in [`tools/integrations/liberty91.md`](tools/integrations/liberty91.md).

### 2. Control coverage mapping — `/control-coverage-mapping`

**What it is.** Answers "which attacker techniques do our controls actually stop, and how well?" by joining your control baseline to **9,545 control-to-technique mappings** drawn from six public sources: MITRE ATT&CK's own mitigations, and independent CTID assessments of NIST 800-53, AWS, Azure, GCP and Microsoft 365.

**The problem it solves.** Control gap analysis is normally a negotiation. Someone asserts a coverage percentage, someone else disputes it, and neither can show their working. This replaces the negotiation with a table both sides can read, where every row cites its source and its score. A disagreement becomes a disagreement about a published assessment rather than about someone's confidence.

**What you get.** Four lists, not three:

| | |
|---|---|
| **Addressed strongly** | a control scored `significant` against the technique |
| **Addressed weakly** | reached only at `partial`, `minimal`, or relevance-asserted-without-strength |
| **Real gaps** | controls for it exist in the evidence base, yours reach none of them |
| **Nobody's controls address this** | no control anywhere maps, or ATT&CK itself says it cannot be mitigated |

That fourth list is the point. Merging it into "gaps" is the standard mistake: it pads the gap list with things no security programme could ever close, and it costs you credibility with the first competent reader.

**Honesty is enforced, not encouraged.** Effectiveness scores are never synthesized. Where no source rates a control's strength, the output says "relevance asserted, no strength claim" rather than inventing a number. A vendor-specific score is never presented as a control-class score. Controls that do not map cleanly get their own section instead of being forced to the nearest-looking identifier.

**Where it fits.** It supplies the **Resistance Strength** half of Vulnerability in a FAIR risk assessment. Pair it with `/lookup-liberty91` for Threat Capability and you have both halves: a technique list without controls tells you what is coming, a control list without techniques tells you what you bought. Joined, they tell you what to do next.

Runs offline, stdlib only, no API key. Evidence base bundled in [`data/attack-control-mapping/`](data/attack-control-mapping/).

## Pick a skill

All skills live flat under `skills/` and are user-invocable as `/<skill-name>`. Grouped here for browsing:

- **Entry point** — `/cti-orchestrator` (default routing), `/cti-setup` (configure API keys)
- **Investigation** — `/ip-investigation`, `/domain-investigation`, `/hash-investigation`, `/url-investigation`
- **Analysis** — `/threat-actor-profiling`, `/ach`, `/indicator-pivoting`, `/campaign-tracking`, `/malware-analysis`, `/threat-assessment`, `/control-coverage-mapping` (which techniques your controls actually stop, and how well), `/horizon-scanning`, `/key-assumptions-check`, `/devils-advocacy`, `/structured-analytic-techniques`
- **Tradecraft rigor** — `/quality-of-information-check` (grade every claim before you reason from it), `/source-provenance` (trace an article to its originating source), `/claim-extraction` (split a report into typed, anchored claims), `/tlp-guide`, `/source-assessment`, `/confidence-levels`, `/likelihood-language`
- **Production** — `/intelligence-writing`, `/writing-assessments`, `/quality-control`, `/ioc-export`, `/stix-bundle`, `/ioc-enrichment-workflow`
- **Detection engineering** — `/sigma-writing`, `/yara-writing`, `/kql-writing`
- **Knowledge cells** — `/china-cyber-espionage`, `/russia-cyber-espionage`, `/iran-cyber-espionage`, `/dprk-cyber-espionage`, `/ransomware-ecosystem`, `/infostealers`, `/initial-access-brokers`, `/phishing-social-engineering`, `/supply-chain-threats`, `/carding-financial-fraud`, `/hacktivism`
- **OSINT + collection** — `/osint-methodology`, `/darkweb-collection`, `/vulnerability-intelligence`
- **Lookups** — `/lookup-liberty91` (first-party: deduplicated occurrences, threat library, IOCs — query + write), `/lookup-virustotal`, `/lookup-otx`, `/lookup-urlscan`, `/lookup-shodan`, `/lookup-abuseipdb`, `/lookup-greynoise`, `/lookup-censys`, `/lookup-misp` (two-way: query + write), `/lookup-opencti` (two-way: knowledge-base query + write), `/lookup-ransomwarelive`, `/lookup-reversinglabs`, `/lookup-crowdstrike` (IOC reputation + threat-actor / TTP / report intelligence), `/lookup-sentinel` (hunt your own Sentinel workspace: IOC exposure sweeps + ATT&CK TTP hunts, table-adaptive KQL), `/mitre-attack`
- **Management** — `/pir-management`, `/stakeholder-management`, `/feedback-loops`, `/sops`, `/maturity-assessment`, `/intelligence-sharing`
- **Methodology** — `/cti-hyperloop` (optional operating doctrine)

## API keys

Optional. The pack degrades gracefully — skills skip enrichments for which no key is configured.

| Service | Env variable | Free tier |
|---|---|---|
| Liberty91 | `LIBERTY91_API_KEY` | per-key rate limit + monthly credits (your plan) |
| VirusTotal | `VIRUSTOTAL_API_KEY` | 4 req/min, 500/day |
| URLScan.io | `URLSCAN_API_KEY` | 100 scans/day |
| Shodan | `SHODAN_API_KEY` | 1 req/sec |
| AbuseIPDB | `ABUSEIPDB_API_KEY` | 1000 checks/day |
| GreyNoise | `GREYNOISE_API_KEY` | 50 req/day |
| AlienVault OTX | `OTX_API_KEY` | 10,000 req/hour |
| Censys | `CENSYS_PAT` (legacy: `CENSYS_API_ID` + `CENSYS_API_SECRET`) | 250 queries/month |
| MISP | `MISP_URL` + `MISP_API_KEY` | host-bound (your instance) |
| OpenCTI | `OPENCTI_URL` + `OPENCTI_TOKEN` | host-bound (your instance) |
| Ransomware.live | `RANSOMWARE_LIVE` | 3,000/day (PRO) |
| ReversingLabs A1000 | `REVERSINGLABS_USER` + `REVERSINGLABS_PASSWORD` | licensed (Spectra Analyze) |
| CrowdStrike Falcon Intelligence | `CROWDSTRIKE_CLIENT_ID` + `CROWDSTRIKE_CLIENT_SECRET` | licensed (Falcon Intelligence) |
| Microsoft Sentinel | `SENTINEL_TENANT_ID` + `SENTINEL_CLIENT_ID` + `SENTINEL_CLIENT_SECRET` + `SENTINEL_WORKSPACE_ID` | your Azure tenancy (read-only app registration) |

Three ways to configure:

1. **Inside Claude Code** (works for all install paths): type `/cti-setup` and Claude walks you through it.
2. **Shell script** (clone install only): `./scripts/setup.sh` — interactive prompts, or use `--non-interactive --virustotal=KEY` flags for scripted setup.
3. **Environment variables**: export the variable in your shell rc; the CLIs read them at runtime. Copy [`.env.example`](.env.example) to `.env` (gitignored) as a starting point listing every supported variable, or pass them inline (`VIRUSTOTAL_API_KEY=… ./scripts/setup.sh --non-interactive`).

Keys are merged into `.claude/settings.local.json` (gitignored). The pack degrades gracefully — skills skip enrichments for which no key is configured.

To verify keys are wired up: `./scripts/setup.sh --verify` (or ask Claude to verify after `/cti-setup`).

## FAQ

**How do you keep the LLM from doing the analysis?**
Three ways. Provenance resolution is deterministic: a script (or the Liberty91 pipeline) follows the links and classifies sources from a maintained table, so the chain is data, not a model's recollection. Claims are extracted with a fixed schema and anchored to the exact source sentence, so every extraction is checkable. Grading follows a published rubric with hard caps, and `/quality-control` rejects outputs that violate the schema. What remains model judgement (fidelity, rationale, deception screen) is labelled as such in every output. ACH and threat assessments grade their evidence first by default, and a run where you skipped grading says so in its header and cannot claim High confidence.

**How do you know the skill works?**
`tests/provenance/` holds the resolver's expected chains and twenty-two rubric violations the validator must reject. They run offline in CI. The same directory records a live run on 30 URLs and what resolved. It also records a claim extraction run on five real vendor reports: 60 claims, all 60 anchors verbatim, 53 passing every review point, and what the review found missing.

**Does the source-types table rate vendors?**
No. It records what an organisation is (vendor, government, press, actor) and how it typically gets its information (telemetry, incident response, sample analysis). Reliability is computed per claim from access, corroboration and the source's own confidence language, never from a stored opinion about the organisation. PRs adding ratings are not merged.

**Does this work with local models?**
Yes. The skills are plain Agent Skills files and the harness matters more than the model. Claude Code pointed at Ollama (`ANTHROPIC_BASE_URL`), Codex with `--oss`, OpenCode, Goose and similar all load the pack. Practical floor is a 20 to 30B class model; the analytical skills degrade first as models get smaller, the lookup wrappers and knowledge cells degrade least. Note that a local model does not mean local data: the lookup skills still call external APIs. The fully offline subset is the knowledge cells, control coverage mapping, detection writing, intelligence production, and now provenance resolution and QoI on documents you already have. We have not benchmarked local models ourselves; results as issues are welcome.

**Can I use this in Hermes Agent or another self-improving harness?**
Yes, the pack loads in any Agent Skills-compatible harness. We recommend enabling write approval or disabling skill self-modification for the `cti-skills` directory. The tradecraft skills are meant to be stable and reviewable, and self-improvement loops are typically not gated on whether a run was actually correct.

## Acknowledgements

This pack codifies established Cyber Threat Intelligence tradecraft into composable agent skills. It rests on decades of public scholarship, open standards, free training material from CTI educators, and vendor research that the community publishes openly. The full per-skill credits live in **[`CREDITS.md`](CREDITS.md)**.

**If we missed you.** We've tried to credit sources where we could find them. If you've contributed to work this pack draws on and feel you haven't been properly credited, please reach out at **Contact@liberty91.com** and we'll update the credits.

## Contributing

Forks and PRs welcome from anyone. Merges reserved to Liberty91 Ltd maintainers. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Status

Version 2.0.0 — see [VERSIONS.md](VERSIONS.md) for per-skill versions and changelog.

## License

MIT — see [LICENSE](LICENSE).

## About Liberty91

[Liberty91 Ltd](https://liberty91.com) builds AI-native threat intelligence tooling. Contact: contact@liberty91.com.
