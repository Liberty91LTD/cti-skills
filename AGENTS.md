# AGENTS.md — Orientation for AI agents

You're an agent loading the `cti-skills` pack. This file tells you what's here, how to use it, and what conventions to follow. It's platform-neutral — the same rules apply in Claude Code, Cursor, Codex, Windsurf, and any other agentic IDE that supports the [Agent Skills spec](https://agentskills.io/specification).

## What this pack is

Cyber Threat Intelligence skills: threat actor profiling, IOC investigation, OSINT methodology, detection engineering (SIGMA/YARA/KQL), intelligence writing, and self-updating knowledge cells on nation-state and cybercrime threats.

Not an internal ops tool. A public distribution artifact. Optimize for adoption and clarity over enforced rigor.

## Shape

```
skills/                 # flat — 78 composable skills
.claude/                # Claude Code specific (agents, settings). Other platforms ignore.
.claude-plugin/         # plugin manifest for Claude Code marketplace install
tools/                  # REGISTRY.md + per-API integration guides + zero-dep CLIs
data/                   # sample IOCs, reports, PIRs — example content, not required
mitre-attack/           # local MITRE ATT&CK Enterprise dataset
VERSIONS.md             # per-skill semver + changelog
tests/                  # offline tests for provenance resolution and grading caps
validate-skills.sh      # frontmatter linter — run before committing
```

## Finding and invoking skills

Skills are self-describing via YAML frontmatter. The `description` field includes trigger phrases — match user intent against descriptions to decide which skill to use.

```yaml
---
name: threat-actor-profile
description: Use when the user asks to profile a threat actor, build an actor card, or characterize an adversary group. Produces an actor profile with aliases, TTPs, targeting, attribution confidence, and observed infrastructure.
---
```

Skills can invoke other skills. An investigation skill like `/ip-investigation` will chain `/lookup-virustotal`, `/lookup-otx`, `/lookup-shodan`, and then apply rigor skills like `/score-source` and `/apply-tlp`. When you're a skill composing others, state the composition explicitly at the top of the skill body: "This skill invokes: X, Y, Z."

## The orchestrator pattern

When the user's request doesn't name a specific skill, route it through `/cti-orchestrator`. That skill:
1. Parses the request
2. Routes to the right investigation/analysis skill
3. Auto-applies rigor skills on the output (`/score-source`, `/apply-tlp`, `/confidence-language`, `/likelihood-language`)
4. Returns a formatted, source-rated, confidence-marked product

Direct user invocations like `/ach` or `/iran-cyber-espionage` bypass the orchestrator — that's fine.

## Conventions — opt-in, not gates

This pack *offers* tradecraft vocabularies. It does not enforce them. Skills that declare `metadata.tradecraft: true` in frontmatter will be validated against these conventions by `validate-skills.sh`; others are free-form.

- **TLP** (Traffic Light Protocol) — CLEAR / GREEN / AMBER / AMBER+STRICT / RED. Applied to intelligence products.
- **Admiralty Scale** — source reliability A-F + information credibility 1-6. Applied to collected intelligence.
- **MISP confidence** — 0-100. Applied to analytical judgments.
- **Probability yardstick** — Remote / Unlikely / Even Chance / Likely / Almost Certain with percentage bands. Applied to forward-looking statements.

Each has a dedicated skill (`/apply-tlp`, `/score-source`, `/confidence-language`, `/likelihood-language`) that the orchestrator auto-invokes.

### The one default: graded evidence

Since 2.0, `/ach`, `/threat-assessment` and `/writing-assessments` prefer graded evidence items and run `/quality-of-information-check` first when handed raw URLs or text. The user can skip it. A run on ungraded evidence is labelled `Evidence basis: ungraded`, carries no invented grades, and is capped at Moderate confidence, so the reader always knows which kind of product they are holding.

The principle behind it: confidence in a judgment is bounded above by the weakest load-bearing claim, and first-party observation is the top of the scale, not outside it.

When you work with sources:

- **Resolve provenance from data.** Use `/source-provenance`. Do not state where a report originated from memory.
- **Grade claims, not events, and not outlets.** Use `/quality-of-information-check` and its fixed rubric.
- **Do not assert what was not established.** No primary the script or platform did not resolve, no corroboration without data, no access type inferred from reputation, no invented confidence language.
- **Carry `provenance_basis` through** (`platform-resolved`, `script-resolved`, `model-judged`) into every product built on the evidence.
- **Enter hits in the user's own telemetry as observations graded direct and established.** CVSS and EPSS are reference data, not evidence.
- **Write the evidence grade in words.** Access level and claim support, for example "direct, firm". It is not an Admiralty rating: never write it as a letter and a number, and never convert one into the other. Admiralty ratings apply to lookup results and single items through `/source-assessment`.
- **Never add ratings of organisations to `source-types.md`.** It records what an organisation is, not how much to trust it.

## External APIs

Each external threat-intel API has three artifacts:

1. `skills/lookup-<api>/SKILL.md` — the invokable skill (what an agent calls)
2. `tools/integrations/<api>.md` — auth setup, rate limits, default source-reliability rating
3. `tools/clis/<api>.js` — zero-dependency Node CLI that the skill shells out to

This separation means: skills are platform-neutral (just SKILL.md), integration docs are for humans setting up keys, CLIs do the actual HTTP work. No MCP server required.

## When you update a skill

1. Edit the skill body
2. Bump version in its frontmatter `metadata.version`
3. Update the row in `VERSIONS.md`
4. Run `./validate-skills.sh` and `python3 tests/provenance/run_tests.py`
5. Open a PR (see `CONTRIBUTING.md`)

## What not to do

- Don't invent new skills without adding them to `VERSIONS.md` and passing the validator
- Don't hardcode API keys — always read from environment variables (see `tools/integrations/<api>.md` for names)
- Don't write content that depends on Claude-Code-specific subagent syntax if the skill could be useful cross-agent. Keep skill bodies neutral; use `.claude/` for platform-specific extensions only.
- Don't drop TLP / source-rating / confidence from intelligence outputs if the orchestrator is active — it's auto-applied for a reason.

## Where to read next

- `README.md` — install methods and quick-start examples
- `CLAUDE.md` — Claude Code-specific orientation
- `CONTRIBUTING.md` — how to propose changes
- `tools/REGISTRY.md` — catalog of external APIs the pack integrates with
- `VERSIONS.md` — what's shipped and what changed
