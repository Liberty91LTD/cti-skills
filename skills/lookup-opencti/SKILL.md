---
name: lookup-opencti
description: Use when you need to query an OpenCTI instance — is this IOC already known, what entities/reports/campaigns exist for an actor — or push new intel into it — creating indicators/observables, labelling, TLP markings, relationships, or importing a STIX 2.1 bundle. Two-way integration. Commonly invoked by /ip-investigation and friends to check whether an indicator is already in your knowledge base, and by analytical skills that want to publish their findings back to OpenCTI. Reads $OPENCTI_URL and $OPENCTI_TOKEN.
metadata:
  version: 1.0.0
  tags: [lookup, write, threat-intel, knowledge-base, stix]
  api: opencti
  default_source_reliability: B
  default_information_credibility: 2
---

# lookup-opencti

Two-way bridge to an [OpenCTI](https://filigran.io/solutions/open-cti/) threat-intelligence platform. OpenCTI is a STIX 2.1-native knowledge base: everything in it — indicators, observables, intrusion sets, malware, reports, campaigns — is a STIX entity connected by relationships. Like `/lookup-misp`, this skill **also writes**: it can create indicators and observables, label and TLP-mark entities, relate them, and import STIX 2.1 bundles. Treat write commands as deliberate actions; don't use them in autonomous enrichment loops. The `delete` command is destructive — **always confirm with the user before invoking it**.

## When to invoke

**Read:**
- An indicator was found by another lookup (VT, OTX, …) — check whether your OpenCTI instance already knows it (`lookup`)
- An analyst wants the entities, reports, or campaigns your platform holds on an actor, malware family, or CVE (`search`, `list`, `get`)
- You need recent high-score indicators, this quarter's incidents, or everything carrying a given label (`list` with filters)
- You want to verify connector health or instance version (`connectors`, `version`)

**Write:**
- A finished investigation produced indicators that belong in your knowledge base
- A STIX 2.1 bundle written via `/stix-bundle` should be imported as entities
- An existing entity needs labels, a TLP marking, a score update, or a relationship to another entity

**Do NOT invoke for:**
- Bulk reputation enrichment (use VT/OTX/RL first; only push the vetted subset into OpenCTI)
- Scanning or pivoting on raw internet infrastructure — OpenCTI is a *curated* dataset, not a scanning service. Use Shodan/Censys for that.
- Community sharing — that's MISP's job (`/lookup-misp`). OpenCTI is your internal knowledge graph; MISP is the exchange layer. Many teams run both, synced by a connector.

## How to invoke

Single Python CLI (stdlib only — no install). Single endpoint: everything is GraphQL against `$OPENCTI_URL/graphql` with `Authorization: Bearer $OPENCTI_TOKEN`.

### Read operations

```bash
# Connectivity + version check
python3 tools/clis/opencti.py version

# Is this IOC known? Checks observables AND indicators in one call
python3 tools/clis/opencti.py lookup 1.2.3.4
python3 tools/clis/opencti.py lookup evil.example.com --limit 10

# Global full-text search across all entity types (actors, malware, reports, ...)
python3 tools/clis/opencti.py search "APT28" --limit 10

# List/filter one entity type. Types: indicators, observables, reports, incidents,
# campaigns, intrusion-sets, malware, attack-patterns, vulnerabilities, sightings
python3 tools/clis/opencti.py list indicators --score-gte 80 --created-after 2026-06-01T00:00:00Z
python3 tools/clis/opencti.py list reports --label apt28 --limit 10
python3 tools/clis/opencti.py list intrusion-sets --order-by modified --order desc

# Full detail + first 25 relationships for one entity (id from lookup/search/list)
python3 tools/clis/opencti.py get <internal-id>

# Connector health (which enrichment/import connectors are registered + active)
python3 tools/clis/opencti.py connectors
```

`list` paginates: when the response has `has_next_page: true`, pass the returned `end_cursor` back via `--after` for the next page.

### Write operations

```bash
# Create an indicator (auto-generates the STIX pattern; creates the underlying
# observable too by default so raw-value lookups will find it)
python3 tools/clis/opencti.py create-indicator \
  --value 185.220.101.45 --type ip \
  --score 85 --description 'C2 observed 2026-07-01' \
  --labels apt28,c2

# Explicit STIX pattern (for anything the --type shorthand doesn't cover)
python3 tools/clis/opencti.py create-indicator \
  --pattern "[file:hashes.'SHA-256' = '<hash>' AND file:name = 'dropper.exe']" \
  --observable-type StixFile --name 'APT28 dropper'

# Create a bare observable (a fact, no detection semantics)
python3 tools/clis/opencti.py create-observable --value 185.220.101.45 --type ip --labels apt28

# Label + TLP-mark an existing entity (labels are auto-created if missing)
python3 tools/clis/opencti.py add-label <id> apt28 c2
python3 tools/clis/opencti.py add-marking <id> TLP:AMBER

# Update a field (name | description | score | confidence)
python3 tools/clis/opencti.py update <id> --field score --value 95

# Relate two entities with a STIX relationship (indicates, uses, targets, ...)
python3 tools/clis/opencti.py create-relationship --from <indicator-id> --to <malware-id> --type indicates

# Import a STIX 2.1 bundle (upload + trigger import job)
python3 tools/clis/opencti.py upload-stix data/stix-bundles/2026-07-01-apt28-c2.json

# Delete an entity — DESTRUCTIVE. Confirm with the user first.
python3 tools/clis/opencti.py delete <id>
```

All commands accept `--dry-run` (preview the GraphQL request without sending) and `--insecure` (skip TLS verification, common on internal deployments).

The CLI exits 2 if `OPENCTI_URL` or `OPENCTI_TOKEN` is unset (when not in dry-run). Report missing credentials; do not fabricate.

## Indicators vs. observables

OpenCTI separates the two, and it matters for both reads and writes:

- **Observable** — a fact: "this IP exists in our data." No detection semantics, no validity window.
- **Indicator** — an assertion: "this pattern is malicious," with a STIX pattern, score, and valid-from/until window.

`lookup` checks both and reports which matched (`known_as`). When writing: use `create-indicator` for anything you'd want detections or blocklists built from, and let it create the companion observable (the default — don't pass `--no-observable` unless you have a reason; without the observable, raw value-searches won't find the IOC). Use `create-observable` for context-only sightings. Deleting an indicator does **not** cascade to its observable, and vice versa.

## STIX 2.1 round-tripping

OpenCTI is STIX-native, so bundles from `/stix-bundle` import without the marking-definition surgery MISP needs:

1. Run an investigation (e.g. `/ip-investigation`)
2. Build a STIX bundle from the findings (`/stix-bundle`)
3. Apply TLP + Admiralty (`/apply-tlp`, `/score-source`)
4. `python3 tools/clis/opencti.py upload-stix <bundle.json>`
5. Review in OpenCTI → add context → connect to actors/campaigns

**Import semantics:** by default the CLI triggers the import with `bypassValidation`, which imports the bundle directly. With `--no-bypass` (or if your token lacks the bypass capability) the bundle lands in the **analyst workbench** (Data → Import) awaiting human validation — uploaded but *not yet* in the knowledge base. The CLI's response `note` tells you which happened; relay it. Import is asynchronous — poll with `lookup`/`search`; small bundles take seconds.

## Response format

All commands return JSON:

```yaml
source: opencti
operation: lookup | search | list | get | create-indicator | upload-stix | ...
query_time: <ISO8601>
# lookup:
known: true|false
known_as: [observable, indicator]
observables: [...]
indicators: [...]
# list:
total_matches: <n>
has_next_page: true|false
end_cursor: <cursor for --after>
results: [...]
# get:
entity: {...}
relationships: [...]
```

## Source reliability (Admiralty default)

Default rating for downstream `/score-source`: **B2** (usually reliable, probably true). OpenCTI is an aggregation platform — the rating belongs to the *feed or author behind the entity*, not the platform. Check `createdBy` and the entity's labels/markings:

- Your own analysts' entities (self-hosted instance) → **A1** — primary source
- Reputable vendor connector (Mandiant, CrowdStrike, Recorded Future) → **A2** / **B2**
- Open feeds (AlienVault, abuse.ch, MISP feed connectors) → **B3** / **C3**
- `confidence` field on the entity (0-100) maps directly onto `/confidence-levels` bands

## Operational notes

- **GraphQL errors arrive as HTTP 200** with an `errors` array — the CLI surfaces the first message and exits 1. `AUTH_REQUIRED` means a bad or missing token.
- **Scores drive automation.** `x_opencti_score` feeds downstream decay and detection-export rules on many deployments. Don't inflate scores on write; 50 is neutral.
- **Labels are shared vocabulary.** `add-label` and `--labels` auto-create missing labels — check `list indicators --label <name>` for the existing convention before inventing a new one.
- **Deletes are silent and permanent.** No recycle bin. Confirm with the user, and remember the indicator/observable non-cascade.
- **pycti exists** — for complex workflows (bulk imports with author identities, custom connectors, streaming) the official [pycti library](https://github.com/OpenCTI-Platform/client-python) is the right tool. This CLI covers the 80% case for query + write, stdlib-only.

## Related skills

- `/stix-bundle` — write STIX 2.1 bundles that this CLI's `upload-stix` consumes (OpenCTI accepts them as-is; no MISP-style TLP workaround needed)
- `/lookup-misp` — the sharing-platform sibling; OpenCTI = internal knowledge graph, MISP = community exchange
- `/lookup-virustotal`, `/lookup-otx` — community reputation lookups; chain before pushing into OpenCTI
- `/score-source` — apply Admiralty rating before publishing
- `/apply-tlp` — decide TLP before `add-marking`
- `/ip-investigation`, `/domain-investigation`, `/hash-investigation`, `/url-investigation` — produce findings that OpenCTI write commands consume
- `/threat-actor-profiling`, `/campaign-tracking` — consume `search`/`list`/`get` output for actor and campaign context

## See also

- Integration setup: `tools/integrations/opencti.md`
- Python CLI source: `tools/clis/opencti.py`
- OpenCTI project: https://filigran.io/solutions/open-cti/
- Documentation: https://docs.opencti.io/
- pycti (full SDK, when this CLI isn't enough): https://github.com/OpenCTI-Platform/client-python
- GraphQL playground: `$OPENCTI_URL/public/graphql` (when enabled by the admin)
