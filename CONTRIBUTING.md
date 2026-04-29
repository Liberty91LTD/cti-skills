# Contributing to cti-skills

Thanks for taking a look. This pack is open to community contributions. Forks and PRs from anyone are welcome. Merges are reserved to Liberty91 Ltd maintainers.

## Quick rules

1. One skill or one fix per PR. Smaller PRs review faster.
2. Run `./validate-skills.sh` before opening a PR — it must pass.
3. Bump the skill's version in `VERSIONS.md` using [semver](https://semver.org/).
4. Don't commit API keys or secrets. The `.gitignore` already excludes `.claude/settings.local.json`; don't add anything else sensitive.

## What we accept

- **New skills** — threat actor profiles, new knowledge cells, additional analytical techniques, new detection-rule writing skills, new lookup skills for additional threat-intel APIs.
- **Skill updates** — fresher intelligence in knowledge cells, clarifications, bug fixes, new frameworks.
- **Integration improvements** — CLI tools, new API integrations, better error handling in `tools/clis/`.
- **Documentation** — README improvements, fix broken links, clarify install instructions.
- **Tooling** — improvements to `validate-skills.sh`, new validation rules, CI workflows.

## What we don't merge

- Skills that duplicate existing ones without clear improvement
- Changes that hardcode credentials or exfiltrate data to external services
- Skills that require paid tools without free-tier alternatives (exception: if the skill is optional and clearly marked)
- Skills with prompts designed to extract outputs that violate Claude's usage policies

## Skill anatomy

A skill lives in its own directory with a `SKILL.md` entrypoint.

```
skills/<skill-name>/
├── SKILL.md           # required — the skill itself
├── references/        # optional — details referenced by SKILL.md (templates, framework deep-dives, examples)
├── scripts/           # optional — helper scripts the skill may execute
└── assets/            # optional — static files (checklists, templates)
```

### Required frontmatter

```yaml
---
name: skill-name-kebab-case
description: One or two sentences describing what this skill does and when to use it. Include trigger phrases agents can match user intent against. 1-1024 chars.
---
```

### Recommended frontmatter

```yaml
---
name: skill-name
description: ...
metadata:
  version: 1.0.0
  tags: [analysis, actor-profiling]
  author: Your Name
  tradecraft: true       # opt-in to TLP/Admiralty/MISP validator checks
  updated: 2026-04-20    # keep this current for knowledge cells
---
```

### Skill body guidelines

- Keep under 500 lines. Move long examples, templates, or framework deep-dives into `references/`.
- State up front which skills this one invokes, if any. Example: "This skill invokes: `/lookup-virustotal`, `/score-source`."
- Write in second person addressing the agent ("You are conducting..."), not first or third person.
- Include concrete examples ("weak" vs "strong" outputs) where possible.
- Cross-reference sibling skills by their slug: "For source rating, use `/score-source`."

## Adding, updating, or removing an integration

External threat-intel integrations (VirusTotal, Shodan, MISP, ransomware.live, …) appear in many places at once: a `lookup-*` skill, an integration guide, one or more CLIs, env-var references in `cti-setup` and `scripts/setup.sh`, a row in `VERSIONS.md`, and cross-references from the four investigation skills, `indicator-pivoting`, `ioc-enrichment-workflow`, and the older tradecraft skills. The auditor at `tools/audit-integrations.py` keeps that surface honest.

### Source of truth

The catalog table at the top of [`tools/REGISTRY.md`](tools/REGISTRY.md) is canonical. Every external integration lives there with its skill name, indicator types, and required environment variables. The auditor parses that table and checks the rest of the codebase against it.

### When you ADD an integration

1. Create `skills/lookup-<name>/SKILL.md` (Agent Skills frontmatter + trigger phrases).
2. Create `tools/integrations/<name>.md` (auth setup, rate limits, Admiralty defaults).
3. Create at least one CLI under `tools/clis/<name>.{py,js}`.
4. **Add a row to the catalog table in `tools/REGISTRY.md`.**
5. Register the env vars in `skills/cti-setup/SKILL.md` (services table) and in `scripts/setup.sh` (interactive prompt + flag).
6. Add the skill to `VERSIONS.md` and to the changelog at the bottom.
7. Run `python3 tools/audit-integrations.py`. Fix anything it surfaces.
8. If the integration is relevant to a composite skill (`ip-investigation`, `domain-investigation`, `hash-investigation`, `url-investigation`, `indicator-pivoting`), add a cross-reference there. The auditor's `composite-coverage` check will tell you exactly which.
9. Run `./validate-skills.sh` (which now also runs the auditor as a non-fatal step).

### When you UPDATE an integration (e.g. env-var rename)

1. Update the row in `tools/REGISTRY.md`.
2. Update `skills/cti-setup/SKILL.md`, `scripts/setup.sh`, and the integration guide.
3. Update the lookup skill's frontmatter / body if the variable surfaces there.
4. Run the auditor — it surfaces every place the old name still appears.
5. Bump the lookup skill's version in `VERSIONS.md` and add a changelog entry.

The Censys migration (legacy `CENSYS_API_ID`/`CENSYS_API_SECRET` → `CENSYS_PAT`) is a worked example of this flow — see commit history.

### When you REMOVE an integration

1. Delete `skills/lookup-<name>/`, `tools/clis/<name>.{py,js}`, `tools/integrations/<name>.md`.
2. Remove the row from `tools/REGISTRY.md`.
3. Remove the env vars from `skills/cti-setup/SKILL.md` and `scripts/setup.sh`.
4. Move the row in `VERSIONS.md` to the "Archived" section with the retirement date.
5. Run the auditor — it will surface every dangling `/lookup-<name>` reference. Fix them by either replacing with a current skill, or noting the historical reference if appropriate.
6. The auditor's `unknown-lookup-ref` check is the safety net here.

### Auditor checks at a glance

| Check | Level | What it catches |
|---|---|---|
| `registry-disk-match` | FAIL | `skills/lookup-X/` exists but no catalog row, or vice versa |
| `integration-guide-exists` | FAIL | catalog row missing `tools/integrations/<name>.md` |
| `cli-exists` | FAIL | catalog row missing `tools/clis/<name>.{py,js}` |
| `versions-md` | FAIL | catalog skill not listed in `VERSIONS.md` |
| `dead-agent-refs` | FAIL | `<name>-agent` token appears in `skills/` (retired naming) |
| `unknown-lookup-ref` | FAIL | `/lookup-X` reference but no such skill exists (catches removals) |
| `cti-setup` | WARN | env var not mentioned in `skills/cti-setup/SKILL.md` |
| `setup-sh` | WARN | env var not handled by `scripts/setup.sh` |
| `composite-coverage` | WARN | composite skill missing a `/lookup-X` it should reference |
| `description-trigger` | WARN | user-invocable skill's frontmatter description has no trigger phrase (`Use when…` / `when the user…` / `invoked by…` etc.) — orchestrator routing depends on it (see line 44 of this file) |
| `cardinality` | WARN | hardcoded `the seven services` / `the nine integrations` out of sync with the current catalog count |

Run `python3 tools/audit-integrations.py --strict` to make warnings fail. Run `--json` for CI consumption.

## Tradecraft conventions (opt-in)

If your skill produces intelligence products, opt into the tradecraft conventions by adding `metadata.tradecraft: true`:

- **TLP** — mark every output (CLEAR/GREEN/AMBER/AMBER+STRICT/RED)
- **Admiralty Scale** — rate sources (A-F for reliability, 1-6 for credibility)
- **MISP confidence** — score judgments 0-100
- **Probability yardstick** — use standard likelihood language for forward-looking statements

The orchestrator auto-applies these when active. If your skill is likely to be invoked standalone, include the conventions in the skill body directly. See `skills/apply-tlp/`, `skills/score-source/`, `skills/confidence-language/`, `skills/likelihood-language/` for the vocabulary.

## Pull request checklist

- [ ] `./validate-skills.sh` passes (also runs `tools/audit-integrations.py` non-fatally)
- [ ] If touching an integration: `python3 tools/audit-integrations.py` reports zero FAILs
- [ ] `VERSIONS.md` updated with new/bumped version + date
- [ ] Skill frontmatter has `name`, `description`, and `metadata.version`
- [ ] Skill invokes listed at top of body (if applicable)
- [ ] No secrets committed
- [ ] Description includes trigger phrases for agent discovery

## Opening a PR

1. Fork the repo
2. Branch from `main`
3. Make your change
4. Run the validator
5. Open a PR against `Liberty91LTD/cti-skills` `main`

A maintainer from Liberty91 Ltd will review. Merges are reserved to maintainers.

## Questions

Open a GitHub issue or email contact@liberty91.com.
