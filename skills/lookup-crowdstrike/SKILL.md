---
name: lookup-crowdstrike
description: Use when you need CrowdStrike Falcon Intelligence on an indicator (IOC reputation for an IP, domain, hash, or URL — malicious confidence, linked actors, malware families, reports) OR on an adversary (threat-actor profile, origin/target search, MITRE ATT&CK TTPs, finished intel reports). Answers questions like "look up 1.1.1.1", "what TTPs does Charming Kitten use?", "which threat actors operate from Russia?", and "latest report on Mustang Panda". Commonly invoked by the four /*-investigation skills, /ioc-enrichment-workflow, /threat-actor-profiling, and the regional espionage cells. Other agents/skills can chain this for vendor-authoritative actor and finished-intel context. Requires a Falcon Intelligence subscription.
metadata:
  version: 1.0.0
  tags: [lookup, threat-intel, actor-intel, finished-intel]
  api: crowdstrike
  default_source_reliability: A
  default_information_credibility: 2
---

# lookup-crowdstrike

Queries the CrowdStrike Falcon Intelligence (Intel) API for indicator (IOC) reputation, threat-actor (adversary) profiles, actor search by origin/target, MITRE ATT&CK technique coverage, and finished intelligence reports. Retrieval only — do not interpret, assess, or conclude. The invoking skill or agent reasons about the result.

## When to invoke

- User asks to look up an IP / domain / hash / URL and CrowdStrike credentials are configured — return CrowdStrike's malicious-confidence, linked actors, malware families, and report references alongside the other lookups
- User asks for the latest / recent malicious IOCs, a CrowdStrike indicator feed, or "what's CrowdStrike seeing lately" → `indicators --malicious` (browse/sweep, newest-first; filter by type/actor/malware/recency)
- User asks "what TTPs / techniques does <actor> use?" → `ttps <actor>` (MITRE ATT&CK mapping)
- User asks "which threat actors operate from <country>?" / "who targets <sector>?" → `actors --origin <c>` / `--target-industry <i>`
- User asks to profile a named adversary (Charming Kitten, Mustang Panda, Cozy Bear, …) → `actor <name>`
- User wants the latest finished reporting on an actor or topic → `reports --actor <name> --latest` or `reports --search "<topic>"`
- `/threat-actor-profiling` or a regional espionage cell wants vendor-authoritative attribution, origins, motivations, and capability
- Need to download a specific intel report PDF by ID → `reports --pdf <id>`

## How to invoke

One CLI: a Python wrapper around the official `crowdstrike-falconpy` SDK. Self-bootstraps a private venv at `tools/clis/.venv-crowdstrike/` on first run; no global install. The SDK exchanges your client id + secret for an OAuth2 bearer token at `/oauth2/token` automatically.

```bash
# IOC reputation — ip / domain / hash / url (auto-detected by CrowdStrike via FQL indicator: match)
python3 tools/clis/crowdstrike.py indicator <value> [--limit N] [--include-deleted]

# Browse / sweep the indicator feed — latest malicious IOCs, by type / actor / recency
python3 tools/clis/crowdstrike.py indicators [--malicious] [--type ip|domain|url|hash|md5|sha1|sha256|email] \
  [--actor "<name>"] [--malware <family>] [--since 7d] [--filter "<FQL>"] [--limit N]

# Profile a single named threat actor (adversary)
python3 tools/clis/crowdstrike.py actor "<name>" [--limit N] [--fields F1,F2,...]

# Search actors by origin / target / motivation / raw FQL
python3 tools/clis/crowdstrike.py actors [--origin russia] [--target-country united-states] \
  [--target-industry financial-services] [--motivation state-sponsored] [--filter "<FQL>"] [--limit N]

# Finished intel reports — by actor, free-text, latest-first, or PDF download
python3 tools/clis/crowdstrike.py reports [--actor "<name>"] [--search "<q>"] [--filter "<FQL>"] \
  [--latest] [--limit N] [--pdf <report_id> --out <path>]

# MITRE ATT&CK techniques mapped to an actor (add --detailed for the full Navigator/CSV/JSON report)
python3 tools/clis/crowdstrike.py ttps "<actor>" [--detailed] [--format csv|json|json_navigator]
```

All subcommands accept `--dry-run` to preview the request plan without spending an API call, and `--base-url` to override the cloud region for one call. All exit code 2 if `$CROWDSTRIKE_CLIENT_ID` or `$CROWDSTRIKE_CLIENT_SECRET` is unset (when not in dry-run). Report missing credentials; do not fabricate.

### Examples

```bash
# 0) "What are the latest 10 malicious IOCs from CrowdStrike?"
python3 tools/clis/crowdstrike.py indicators --malicious --limit 10
#    e.g. latest malicious domains from the past week tied to an actor:
python3 tools/clis/crowdstrike.py indicators --malicious --type domain --since 7d --actor "Fancy Bear"

# 1) "Look up IP 1.1.1.1" — CrowdStrike's view of the indicator
python3 tools/clis/crowdstrike.py indicator 1.1.1.1

# 2) "What TTPs does Charming Kitten use?"
python3 tools/clis/crowdstrike.py ttps "Charming Kitten" --detailed --format json_navigator

# 3) "Which threat actors operate from Russia?"
python3 tools/clis/crowdstrike.py actors --origin russia --limit 30

# 4) "Give me the latest report on Mustang Panda"
python3 tools/clis/crowdstrike.py reports --actor "Mustang Panda" --latest --limit 5

# 5) Profile an actor, then pull its newest report PDF
python3 tools/clis/crowdstrike.py actor "Cozy Bear"
python3 tools/clis/crowdstrike.py reports --pdf CSA-250123 --out cozy-bear-latest.pdf
```

### Quota awareness

The Intel API is governed by CrowdStrike's per-tenant rate limit (token-bucket; the response carries `X-RateLimit-Limit` / `X-RateLimit-Remaining` headers). On exhaustion the API returns **HTTP 429** with a `Retry-After` header — back off and retry. Each subcommand is a single API call, except `ttps` (resolves the actor slug, then queries MITRE — 2 calls, 3 with `--detailed`) and `reports --pdf` (1 call returning binary). Use `--dry-run` to confirm the call plan before fan-out across many actors.

## Response format

The CLI emits JSON to stdout. Skills consuming it should treat it as:

```yaml
source: crowdstrike
operation: indicator_lookup | indicator_search | actor_profile | actor_search | report_search | report_pdf | actor_ttps
indicator: <queried value or FQL>
type: indicator | indicator_query | actor | actor_query | report_query | report_id
base_url: https://api.crowdstrike.com
query_time: <ISO8601>
count: <n>                       # number of resources returned
# operation-specific payload — the SDK's deserialised resources array
indicators: [ ... ]              # for `indicator`
actors: [ ... ]                  # for `actor`, `actors`
reports: [ ... ]                 # for `reports`
technique_ids: [ ... ]           # for `ttps`; + mitre_report when --detailed
saved_to: <path>                 # for `reports --pdf`
```

Common fields inside each resource type:

| Resource | Key fields |
|---|---|
| indicator | `indicator`, `type`, `malicious_confidence` (high/medium/low/unverified), `actors`, `malware_families`, `kill_chains`, `threat_types`, `reports`, `labels`, `published_date`, `last_updated` |
| actor | `name`, `slug`, `short_description`, `description`, `known_as`, `origins[]`, `target_countries[]`, `target_industries[]`, `motivations[]`, `capability`, `group`, `actor_type`, `first_activity_date`, `last_activity_date` |
| report | `name`, `title`, `slug`, `short_description`, `created_date`, `last_modified_date`, `actors[]`, `target_countries[]`, `target_industries[]`, `tags[]`, `report_type`, `url`, `attachments[]` |
| ttps | `technique_ids[]` (ATT&CK technique IDs); `mitre_report` (CSV / JSON / Navigator layer when `--detailed`) |

## Rate limits

Per-tenant token bucket; `429` + `Retry-After` on exhaustion. `indicator`/`actor`/`actors`/`reports` = 1 call each; `ttps` = 2–3 calls. Back off on 429.

## Source reliability (Admiralty default)

Default rating for downstream `/score-source`: **A2** (completely reliable, probably true). CrowdStrike Falcon Intelligence is vendor-authoritative finished intelligence produced by a dedicated analyst team; attribution, origins, and TTP mappings are well validated.

**Downgrade to B3** if:
- An indicator's `malicious_confidence` is `low` or `unverified`
- An actor record is sparse (no `origins` / `capability`) or flagged provisional
- The judgement rests on a single report with hedged language — read the report body, don't infer from the tag alone

**Stay at A2 / consider A1** if:
- `malicious_confidence` is `high` AND the indicator is linked to a named actor or malware family
- Multiple finished reports corroborate the actor attribution and TTP set

## Related skills

- `/lookup-virustotal` — community-aggregated detection; complements CrowdStrike's vendor view on the same IOC
- `/lookup-reversinglabs` — vendor-authoritative malware classification + sandbox for a hash
- `/lookup-otx` — community pulse context for the same indicator
- `/threat-actor-profiling` — chains `actor` / `ttps` / `reports` into a full adversary profile
- `/ip-investigation`, `/domain-investigation`, `/hash-investigation`, `/url-investigation` — chain the `indicator` lookup
- `/mitre-attack` — resolve the `technique_ids` from `ttps` against the local ATT&CK dataset
- `/score-source` — apply the Admiralty rating to the result

## See also

- Integration setup: `tools/integrations/crowdstrike.md`
- Python CLI source: `tools/clis/crowdstrike.py`
- Companion API reference (non-invokable): `skills/crowdstrike-api/SKILL.md`
- Official API docs: https://developer.crowdstrike.com/api-reference/collections/intel/
- SDK source: https://github.com/CrowdStrike/falconpy
