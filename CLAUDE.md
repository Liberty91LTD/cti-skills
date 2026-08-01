# cti-skills — Claude Code orientation

Cyber Threat Intelligence skills pack for Claude Code and other agentic IDEs. See [AGENTS.md](AGENTS.md) for the platform-neutral orientation — this file adds Claude-Code-specific notes.

## What's here

- `skills/` — 74 composable CTI skills flat at the repo root per Agent Skills spec. Each is a directory with a `SKILL.md`. Canonical user-invokable interface. Works in any Agent-Skills-compatible IDE.
- `.claude-plugin/marketplace.json` — plugin manifest, install via `/plugin marketplace add Liberty91LTD/cti-skills`.
- `.claude/agents/` — **optional Claude-Code-specific subagents** (analyst, report-writer, quality-reviewer, osint-researcher, ioc-processor, detection-engineer). These wrap skills with model routing (Opus for deep reasoning, Sonnet for structured work) and tool permissions. The new `cti-orchestrator` lives as a skill now — the old agent was archived.
- `.claude/settings.json` — baseline permissions.
- `tools/` — REGISTRY + per-API integration guides + zero-dep CLIs. Used by `lookup-*` skills.
- `archive/agents/` — the 7 tool-API agents and old `cti-orchestrator` — moved here after being superseded by `lookup-*` skills and the orchestrator skill.
- `data/` — sample IOCs, reports, PIRs for users to model after.
- `mitre-attack/` — bundled MITRE ATT&CK Enterprise dataset.
- `VERSIONS.md` — per-skill semver + changelog.
- `validate-skills.sh` — run before committing.

## How to use the pack

1. **Orchestrator-routed requests** (the default): the user says "investigate 8.8.8.8" or "profile APT28" — route to `/cti-orchestrator`, which picks the right investigation/analysis skill and auto-applies rigor skills (TLP, source rating, confidence, likelihood) on the output.
2. **Direct skill invocations**: when the user types `/ach`, `/iran-cyber-espionage`, `/pir-management` etc., invoke the named skill directly, bypassing the orchestrator.
3. **Composition**: skills can invoke other skills. Investigation skills chain lookups; analytical skills can prioritize IOCs and dispatch further investigation. Composition is documented at the top of each skill body.
4. **Claude-Code subagent specialists** (optional): for deep analytical work, Claude Code can dispatch to `analyst` (Opus), `report-writer` (Opus), `quality-reviewer` (Opus), `osint-researcher` (Sonnet), `ioc-processor` (Sonnet), or `detection-engineer` (Sonnet). These agents load the same skills but offer model routing and tighter tool permissions. They are a Claude-Code-only optimization — skills alone work everywhere.

## Tradecraft vocabularies

Opt-in. Skills with `metadata.tradecraft: true` in frontmatter produce outputs marked with TLP, Admiralty source ratings, MISP confidence, and probability yardstick language. The orchestrator auto-applies these to finished products. See `/apply-tlp`, `/score-source`, `/confidence-language`, `/likelihood-language`.

## Before committing

```bash
./validate-skills.sh
```

If it prints errors, fix them. If it warns about skill body size, move detail into `references/` subdirectories. Update `VERSIONS.md` when you ship changes.

## API keys

Stored in `.claude/settings.local.json` (gitignored), set via `./scripts/setup.sh`, or passed as environment variables. See [README.md](README.md#api-keys).

## See also

- [README.md](README.md) — install, quick start, skill catalog
- [AGENTS.md](AGENTS.md) — platform-neutral orientation
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to propose changes
- [VERSIONS.md](VERSIONS.md) — changelog
