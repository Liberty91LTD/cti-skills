# AGENTS.md — Orientation for AI agents

You're an agent loading the `cti-skills` pack. This file tells you what's here, how to use it, and what conventions to follow. It's platform-neutral — the same rules apply in Claude Code, Cursor, Codex, Windsurf, and any other agentic IDE that supports the [Agent Skills spec](https://agentskills.io/specification).

## What this pack is

Cyber Threat Intelligence skills: threat actor profiling, IOC investigation, OSINT methodology, detection engineering (SIGMA/YARA/KQL), intelligence writing, and self-updating knowledge cells on nation-state and cybercrime threats.

Not an internal ops tool. A public distribution artifact. Optimize for adoption and clarity over enforced rigor.

## Shape

```
skills/                 # flat — ~52 composable skills (will flatten in Phase C)
.claude/                # Claude Code specific (agents, settings). Other platforms ignore.
.claude-plugin/         # plugin manifest for Claude Code marketplace install
tools/                  # REGISTRY.md + per-API integration guides + zero-dep CLIs
data/                   # sample IOCs, reports, PIRs — example content, not required
mitre-attack/           # local MITRE ATT&CK Enterprise dataset
VERSIONS.md             # per-skill semver + changelog
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
4. Run `./validate-skills.sh`
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
