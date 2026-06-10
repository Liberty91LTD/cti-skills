---
name: crowdstrike-api
description: CrowdStrike Falcon Intelligence (Intel API) reference. OAuth2 auth, Falcon Query Language, indicator (IOC) lookups, threat-actor entities, intel reports, MITRE ATT&CK mappings, malware families, vulnerabilities, rule sets.
user-invocable: false
metadata:
  version: 1.0.0
---

# CrowdStrike Falcon Intelligence (Intel) API

This is reference documentation. The agent-invokable lookup skill is `/lookup-crowdstrike`; the runtime CLI is `tools/clis/crowdstrike.py`. Read this file when the lookup skill's options are not enough and you need to know which raw endpoint to hit, what fields a response carries, or how to construct an FQL query the CLI does not expose directly.

Source of truth: https://developer.crowdstrike.com/api-reference/collections/intel/

## Base URL

OAuth2 base differs by cloud region. The Intel path prefix is `/intel/`.

| Cloud | Base URL |
|---|---|
| US-1 (default) | `https://api.crowdstrike.com` |
| US-2 | `https://api.us-2.crowdstrike.com` |
| EU-1 | `https://api.eu-1.crowdstrike.com` |
| US-GovCloud | `https://api.laggar.gcw.crowdstrike.com` |

Override with `CROWDSTRIKE_BASE_URL` (or `--base-url`). FalconPy also accepts the short names `us-1`, `us-2`, `eu-1`, `usgov1`.

## Authentication

OAuth2 **client-credentials** flow:

1. `POST /oauth2/token` with form-encoded `client_id` and `client_secret`.
2. Response: `{"access_token": "<jwt>", "expires_in": 1799, "token_type": "bearer"}`.
3. All subsequent requests carry `Authorization: Bearer <access_token>`.

FalconPy performs this exchange and refresh automatically when given `client_id=` / `client_secret=`.

```bash
# Manual token exchange
TOKEN=$(curl -s -X POST "https://api.crowdstrike.com/oauth2/token" \
  -d "client_id=$CROWDSTRIKE_CLIENT_ID&client_secret=$CROWDSTRIKE_CLIENT_SECRET" | jq -r .access_token)

# Subsequent call
curl -s "https://api.crowdstrike.com/intel/combined/actors/v1?filter=origins.slug%3A%27ru%27&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

The API client needs the **Intel** scopes: `Indicators (Falcon Intelligence): Read`, `Actors (Falcon Intelligence): Read`, `Reports (Falcon Intelligence): Read`, and `Rules (Falcon Intelligence): Read` for rule-set endpoints. Create it in the Falcon console → **Support and resources → API clients and keys**. If the env vars are unset, inform the user to run `/cti-setup` or `./scripts/setup.sh`.

## Rate limits

Per-tenant token bucket. Responses carry `X-RateLimit-Limit` and `X-RateLimit-Remaining`. On exhaustion the API returns **HTTP 429** with a `Retry-After: <seconds>` header — back off and retry. `429` is also returned briefly if you call before the OAuth token is minted.

## Falcon Query Language (FQL)

Query/`combined` endpoints accept a `filter` parameter in FQL:

- Equality: `malicious_confidence:'high'`, `name:'FANCY BEAR'` (actor name; exact match)
- Country slugs are **ISO 3166-1 alpha-2 codes**, not names: `origins.slug:'ru'` (Russia), `'cn'` (China), `'ir'` (Iran), `'kp'` (North Korea), `target_countries.slug:'us'`
- Other nested arrays use word slugs: `target_industries.slug:'financial-services'`, `motivations.slug:'state-sponsored'`, `actors.slug:'mustang-panda'`
- Comparisons / dates: `created_date:>'2025-01-01'`, `last_updated:>=1704067200`
- Boolean combine: `+` = AND, `,` = OR. e.g. `origins.slug:'cn'+target_industries.slug:'government'`
- Free-text: the separate `q` parameter does a fuzzy text match across the entity (used by `actor`/`reports --search`)
- Sort: `sort=created_date|desc`, `sort=last_activity_date|desc`. **`name` is not a sortable field on the actors endpoint** — sorting by it silently returns zero results
- Page: `limit` (max 5000 for most, 10000 for indicators) + `offset`

## Capability map

| Group | Operation | Method + endpoint | FalconPy method |
|---|---|---|---|
| Actors | QueryIntelActorEntities | GET `/intel/combined/actors/v1` | `query_actor_entities` |
| Actors | QueryIntelActorIds | GET `/intel/queries/actors/v1` | `query_actor_ids` |
| Actors | GetIntelActorEntities | GET `/intel/entities/actors/v1` | `get_actor_entities` |
| Indicators | QueryIntelIndicatorEntities | GET `/intel/combined/indicators/v1` | `query_indicator_entities` |
| Indicators | QueryIntelIndicatorIds | GET `/intel/queries/indicators/v1` | `query_indicator_ids` |
| Indicators | GetIntelIndicatorEntities | POST `/intel/entities/indicators/GET/v1` | `get_indicator_entities` |
| Reports | QueryIntelReportEntities | GET `/intel/combined/reports/v1` | `query_report_entities` |
| Reports | QueryIntelReportIds | GET `/intel/queries/reports/v1` | `query_report_ids` |
| Reports | GetIntelReportEntities | GET `/intel/entities/reports/v1` | `get_report_entities` |
| Reports | GetIntelReportPDF | GET `/intel/entities/report-files/v1` | `get_report_pdf` |
| MITRE | QueryMitreAttacks | GET `/intel/combined/mitre-attacks/v1` | `query_mitre_attacks` |
| MITRE | QueryMitreAttacksForMalware | GET `/intel/combined/mitre-attacks-for-malware/v1` | `query_mitre_attacks_for_malware` |
| MITRE | GetMitreReport | GET `/intel/entities/mitre-reports/v1` | `get_mitre_report` |
| MITRE | GetMalwareMitreReport | GET `/intel/entities/malware-mitre-reports/v1` | `get_malware_mitre_report` |
| MITRE | PostMitreAttacks | POST `/intel/entities/mitre/v1` | `post_mitre_attacks` |
| Malware | QueryIntelMalwareEntities | GET `/intel/combined/malware/v1` | `query_malware` / `query_malware_entities` |
| Malware | GetIntelMalwareEntities | GET `/intel/entities/malware/v1` | `get_malware_entities` |
| Vulnerabilities | QueryVulnerabilities | GET `/intel/queries/vulnerabilities/v1` | `query_vulnerabilities` |
| Vulnerabilities | GetVulnerabilities | GET `/intel/entities/vulnerabilities/GET/v1` | `get_vulnerabilities` |
| Rule sets | QueryIntelRuleIds | GET `/intel/queries/rules/v1` | `query_rule_ids` |
| Rule sets | GetIntelRuleEntities | GET `/intel/entities/rules/v1` | `get_rule_entities` |
| Rule sets | GetIntelRuleFile | GET `/intel/entities/rules-files/v1` | `get_rule_file` |
| Rule sets | GetLatestIntelRuleFile | GET `/intel/entities/rules-latest-files/v1` | `get_latest_intel_rule_file` |

The CLI wraps the bold-path subset (actors, indicators, reports, mitre-attacks, mitre-reports). The rest are reachable directly via FalconPy if a skill needs them.

## Key endpoints — examples

### Indicator (IOC) lookup

```bash
# Single-value lookup (CLI: `indicator <value>`)
curl -s "https://api.crowdstrike.com/intel/combined/indicators/v1?filter=indicator%3A%271.1.1.1%27&limit=50" \
  -H "Authorization: Bearer $TOKEN"

# Browse/sweep the feed — latest high-confidence malicious IOCs (CLI: `indicators --malicious`)
curl -s "https://api.crowdstrike.com/intel/combined/indicators/v1?filter=malicious_confidence%3A%27high%27&sort=published_date%7Cdesc&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

`type` values are: `ip_address`, `domain`, `url`, `hash_md5`, `hash_sha1`, `hash_sha256`, `email_address`, `file_name`, `mutex_name`, `registry`, `service_name`, `username`, `persona_name`, `x509_serial`, `x509_subject` (and more). Combine confidence + type + `actors:'<slug>'` + `malware_families:'<fam>'` + `published_date:>EPOCH` with `+`. **Requires the Indicators (Falcon Intelligence): Read scope** — without it the endpoint returns HTTP 403 "scope not permitted" even though Actors/Reports work.

Response `resources[]` highlights: `indicator`, `type` (`ip_address`/`domain`/`hash_sha256`/`url`/…), `malicious_confidence` (high/medium/low/unverified), `actors[]` (slugs), `malware_families[]`, `kill_chains[]`, `threat_types[]`, `reports[]` (report IDs), `labels[]`, `relations[]`, `published_date`, `last_updated`.

### Actor entities

```bash
# Search by origin (ISO country-code slug; sort by activity, NOT name)
curl -s "https://api.crowdstrike.com/intel/combined/actors/v1?filter=origins.slug%3A%27ru%27&sort=last_activity_date%7Cdesc&limit=30" \
  -H "Authorization: Bearer $TOKEN"

# Free-text profile lookup
curl -s "https://api.crowdstrike.com/intel/combined/actors/v1?q=Charming%20Kitten&limit=1" \
  -H "Authorization: Bearer $TOKEN"
```

Actor `resources[]` fields: `id`, `name`, `slug`, `short_description`, `description`, `known_as`, `origins[]`, `target_countries[]`, `target_industries[]`, `motivations[]`, `capability`, `group`, `actor_type`, `first_activity_date`, `last_activity_date`, `url`. Each `origins`/`target_*` element is `{id, value, slug}`.

### Reports

```bash
# Latest reports for an actor
curl -s "https://api.crowdstrike.com/intel/combined/reports/v1?filter=actors.slug%3A%27mustang-panda%27&sort=created_date%7Cdesc&limit=5" \
  -H "Authorization: Bearer $TOKEN"

# Download a report PDF (binary)
curl -s "https://api.crowdstrike.com/intel/entities/report-files/v1?ids=CSA-250123" \
  -H "Authorization: Bearer $TOKEN" -o report.pdf
```

Report `resources[]` fields: `id`, `name`, `title`, `slug`, `short_description`, `description`, `created_date`, `last_modified_date`, `actors[]`, `target_countries[]`, `target_industries[]`, `motivations[]`, `tags[]`, `report_type`, `sub_type`, `url`, `attachments[]`.

### MITRE ATT&CK for an actor

```bash
# Technique IDs mapped to an actor (by slug or id)
curl -s "https://api.crowdstrike.com/intel/combined/mitre-attacks/v1?id=charming-kitten" \
  -H "Authorization: Bearer $TOKEN"

# Full ATT&CK report — csv | json | json_navigator
curl -s "https://api.crowdstrike.com/intel/entities/mitre-reports/v1?actor_id=charming-kitten&format=json_navigator" \
  -H "Authorization: Bearer $TOKEN"
```

`QueryMitreAttacks` returns a flat list of ATT&CK technique IDs in `resources[]`. `GetMitreReport` returns the full mapping; `json_navigator` is an ATT&CK Navigator layer JSON you can load directly into the Navigator UI. Resolve technique IDs against the bundled dataset with `/mitre-attack`.

## Response shape

FalconPy returns `{status_code, headers, body}` where `body = {meta, resources, errors}`. The CLI unwraps `body.resources` and emits a normalised envelope. See `skills/lookup-crowdstrike/SKILL.md` § Response format.
