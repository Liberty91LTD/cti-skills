# CrowdStrike Falcon Intelligence integration

[CrowdStrike Falcon Intelligence](https://www.crowdstrike.com/platform/threat-intelligence/) is CrowdStrike's threat-intelligence subscription. The **Intel API** exposes finished intelligence produced by CrowdStrike's analyst teams: IOC reputation, threat-actor (adversary) profiles, MITRE ATT&CK technique mappings, intel reports, malware-family and vulnerability records. It is a licensed product — credentials are issued to customer tenants, not signed up for online, and the relevant API scopes require a Falcon Intelligence (or Intelligence Premium / Elite) subscription.

## Getting credentials

1. In the Falcon console, go to **Support and resources → Resources and tools → API clients and keys**.
2. **Create API client**. Give it a name (e.g. `cti-skills-intel`) and assign the **Read** scopes:
   - `Indicators (Falcon Intelligence)` — Read
   - `Actors (Falcon Intelligence)` — Read
   - `Reports (Falcon Intelligence)` — Read
   - `Rules (Falcon Intelligence)` — Read (only if you use the rule-set endpoints)
3. Copy the **Client ID** and **Client Secret** (the secret is shown once).
4. Note your cloud region (US-1 is the default; US-2 / EU-1 / GovCloud have different base URLs — see below).
5. Set the env vars (or run `./scripts/setup.sh`):
   ```bash
   export CROWDSTRIKE_CLIENT_ID="<client id>"
   export CROWDSTRIKE_CLIENT_SECRET="<client secret>"
   export CROWDSTRIKE_BASE_URL="https://api.crowdstrike.com"   # optional; default shown (US-1)
   ```

The CLI's first invocation bootstraps a private Python venv at `tools/clis/.venv-crowdstrike/` and installs `crowdstrike-falconpy`. No global pip install.

## Cloud regions

| Cloud | `CROWDSTRIKE_BASE_URL` |
|---|---|
| US-1 (default) | `https://api.crowdstrike.com` |
| US-2 | `https://api.us-2.crowdstrike.com` |
| EU-1 | `https://api.eu-1.crowdstrike.com` |
| US-GovCloud | `https://api.laggar.gcw.crowdstrike.com` |

Pick the one matching your Falcon tenant; an API client only works against its own cloud.

## Authentication flow

OAuth2 client-credentials, with auto-refresh:

1. FalconPy sends `POST /oauth2/token` with form-encoded `client_id` + `client_secret`.
2. Server returns `{"access_token": "<jwt>", "expires_in": 1799, "token_type": "bearer"}`.
3. FalconPy puts `Authorization: Bearer <access_token>` on every request and refreshes before expiry.

## Rate limits

Per-tenant token bucket. Responses carry `X-RateLimit-Limit` / `X-RateLimit-Remaining`. On exhaustion the API returns **HTTP 429** with `Retry-After: <seconds>` — back off and retry. Each CLI subcommand is one API call, except `ttps` (2 calls, 3 with `--detailed`).

## Supported indicators

| Type | CLI subcommand | Notes |
|---|---|---|
| IP / domain / file hash / URL | `indicator` | FQL `indicator:'<value>'`; returns malicious confidence, linked actors, malware families, report refs |
| Threat actor (name) | `actor`, `ttps`, `reports --actor` | free-text `q` resolves the adversary; `ttps` maps ATT&CK techniques |
| Actor population (origin/target) | `actors` | FQL search by `origins.slug`, `target_countries.slug`, `target_industries.slug`, `motivations.slug` |
| Intel report (free-text / ID) | `reports` | `--search` for text, `--filter` for FQL, `--pdf <id>` to download |

## Endpoints used

| CLI subcommand | REST endpoint | FalconPy method |
|---|---|---|
| `indicator` | `GET /intel/combined/indicators/v1` | `query_indicator_entities` |
| `actor` | `GET /intel/combined/actors/v1` (q) | `query_actor_entities` |
| `actors` | `GET /intel/combined/actors/v1` (filter) | `query_actor_entities` |
| `reports` | `GET /intel/combined/reports/v1` | `query_report_entities` |
| `reports --pdf` | `GET /intel/entities/report-files/v1` | `get_report_pdf` |
| `ttps` | `GET /intel/combined/actors/v1` + `GET /intel/combined/mitre-attacks/v1` | `query_actor_entities` + `query_mitre_attacks` |
| `ttps --detailed` | `GET /intel/entities/mitre-reports/v1` | `get_mitre_report` |

Authentication header on every call: `Authorization: Bearer <token>` (handled by the SDK). Full operation catalogue (rule sets, malware, vulnerabilities, malware MITRE) is in `skills/crowdstrike-api/SKILL.md`.

## Admiralty defaults (for `/score-source`)

**Source reliability:** A (completely reliable) — vendor-authoritative finished intelligence from a dedicated analyst team.
**Information credibility:** 2 (probably true) — well validated, but low-confidence indicators and sparse/provisional actor records warrant analyst verification.

**Downgrades:**
- Indicator `malicious_confidence` is `low` or `unverified` → **B3**
- Actor record sparse (no `origins` / `capability`) or judgement rests on a single hedged report → **B3**

**Upgrades:**
- Indicator `malicious_confidence == high` AND linked to a named actor or malware family, corroborated by ≥1 finished report → **A1**

## Privacy notes

- Finished intelligence is licensed and proprietary — CrowdStrike report content is typically **TLP:AMBER or stricter** under the subscription agreement. Do not redistribute report bodies outside your organisation; cite report IDs internally.
- Queries do not submit your IOCs to a shared pool — the Intel API is read-only retrieval against CrowdStrike's catalogue.
- Treat the client secret as a long-lived credential; rotate it from the API clients page if exposed.

## Testing your credentials

```bash
# Token round-trip
curl -s -X POST "$CROWDSTRIKE_BASE_URL/oauth2/token" \
  -d "client_id=$CROWDSTRIKE_CLIENT_ID&client_secret=$CROWDSTRIKE_CLIENT_SECRET" | head -c 200

# Or use the CLI's dry-run path (no network call):
python3 tools/clis/crowdstrike.py indicator 1.1.1.1 --dry-run

# Real round-trip (uses one API call):
python3 tools/clis/crowdstrike.py actor "Cozy Bear"
```

## See also

- API reference (companion skill): `skills/crowdstrike-api/SKILL.md`
- Lookup skill: `skills/lookup-crowdstrike/SKILL.md`
- Python CLI source: `tools/clis/crowdstrike.py`
- Official API docs: https://developer.crowdstrike.com/api-reference/collections/intel/
- SDK source: https://github.com/CrowdStrike/falconpy
