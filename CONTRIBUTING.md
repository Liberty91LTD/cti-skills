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

## Tradecraft conventions (opt-in)

If your skill produces intelligence products, opt into the tradecraft conventions by adding `metadata.tradecraft: true`:

- **TLP** — mark every output (CLEAR/GREEN/AMBER/AMBER+STRICT/RED)
- **Admiralty Scale** — rate sources (A-F for reliability, 1-6 for credibility)
- **MISP confidence** — score judgments 0-100
- **Probability yardstick** — use standard likelihood language for forward-looking statements

The orchestrator auto-applies these when active. If your skill is likely to be invoked standalone, include the conventions in the skill body directly. See `skills/apply-tlp/`, `skills/score-source/`, `skills/confidence-language/`, `skills/likelihood-language/` for the vocabulary.

## Pull request checklist

- [ ] `./validate-skills.sh` passes
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
