# OpenCTI integration

[OpenCTI](https://filigran.io/solutions/open-cti/) is the open-source threat-intelligence platform by Filigran — a STIX 2.1-native knowledge graph of indicators, observables, actors, malware, reports, and the relationships between them. Like MISP, this integration is **two-way**: you query existing entities AND push new intel back into the platform. Where MISP is the community *exchange* layer, OpenCTI is typically the internal *knowledge base*; many teams run both.

## Getting credentials

1. Log into your OpenCTI instance → **Settings → Security → Users** (admins) or your own profile → **API access**.
2. Every user has an API token (a UUID). For automation, prefer a **dedicated service account** with a role scoped to what the CLI should do:
   - Read-only use: `Access knowledge`
   - Write use: add `Create / Update knowledge`
   - `upload-stix` with the default validation bypass: a role capability that allows importing without workbench review (label varies by version — look for "bypass" under the role's capabilities); without it, imported bundles land in the analyst workbench for human review
   - `delete`: add `Delete knowledge` — grant reluctantly
3. Copy the token and set both env vars:
   - `OPENCTI_URL` — base URL of your instance (e.g. `https://opencti.example.org` or `http://localhost:8080`, **no trailing slash**)
   - `OPENCTI_TOKEN` — the API token (UUID)

Add via `./scripts/setup.sh`, `/cti-setup`, or stash in `.claude/settings.local.json` `env` block. An optional `OPENCTI_PROXY` (or `HTTPS_PROXY`) routes CLI traffic through an HTTP proxy.

## Authentication

Standard Bearer header:

```
Authorization: Bearer <OPENCTI_TOKEN>
Accept: application/json
Content-Type: application/json
```

The CLI sets this for you.

## API surface

Single endpoint — **everything is GraphQL** via `POST {OPENCTI_URL}/graphql`. There are no REST paths. Two consequences worth knowing:

- **Errors come back as HTTP 200** with an `errors` array in the JSON body. The CLI (`tools/clis/opencti.py`) checks it and exits 1 with the first error message. `AUTH_REQUIRED` means a bad/missing token.
- **Filtering uses the FilterGroup format** (OpenCTI ≥ 5.12): `{mode, filters: [{key, values, operator}], filterGroups: []}` — `filterGroups` is required even when empty. The CLI builds this from `--label`, `--created-after/-before`, and `--score-gte` flags. Targets OpenCTI **6.x and later**; older 5.x instances with the legacy filter format are not supported.

### CLI subcommands

| Kind | Subcommand | GraphQL root |
|---|---|---|
| Read | `version` | `about { version }` — connectivity check |
| Read | `search <term>` | `stixCoreObjects(search:)` — global full-text |
| Read | `lookup <value>` | `stixCyberObservables(search:)` + `indicators(search:)` in one query |
| Read | `list <type>` | per-type connection (`indicators`, `reports`, `intrusionSets`, …) with filters + cursor pagination |
| Read | `get <id>` | `stixCoreObject(id:)` + `stixCoreRelationships(fromOrToId:)` |
| Read | `connectors` | `connectors` — registration + active state |
| Write | `create-indicator` | `indicatorAdd` (creates the companion observable by default via `createObservables`) |
| Write | `create-observable` | `stixCyberObservableAdd` |
| Write | `add-label <id> <label>…` | label resolve/create + `stixCoreObjectEdit.relationAdd(object-label)` |
| Write | `add-marking <id> <TLP:…>` | marking-definition resolve + `stixCoreObjectEdit.relationAdd(object-marking)` |
| Write | `update <id> --field --value` | `stixDomainObjectEdit.fieldPatch` / `stixCyberObservableEdit.fieldPatch` |
| Write | `create-relationship` | `stixCoreRelationshipAdd` |
| Write | `upload-stix <bundle>` | multipart `uploadImport` + `askJobImport(bypassValidation:)` |
| Delete | `delete <id>` | `stixDomainObjectEdit.delete` / `stixCyberObservableEdit.delete` — **destructive, confirm with the user first** |

All subcommands accept `--dry-run` (print the GraphQL request, don't send) and `--insecure` (skip TLS verification for self-signed internal deployments — per-invocation by design).

## Indicators vs. observables

OpenCTI models these separately and the write commands respect that:

- `create-observable` — a bare fact ("this IP appeared in our data"), no detection semantics.
- `create-indicator` — a detection assertion with a STIX pattern and `x_opencti_score`. By default it **also creates the underlying observable** (`createObservables: true`); without that, raw value-searches don't find the IOC. Only pass `--no-observable` deliberately.
- `delete` on an indicator does **not** cascade to its observable (and vice versa).

Labels passed via `--labels`/`add-label` are resolved name → internal id, and **auto-created if missing** — check existing label conventions (`list indicators --label <name>`) before inventing new vocabulary.

## STIX 2.1 import semantics

`upload-stix` is a two-step dance the CLI handles: a GraphQL-multipart file upload (`uploadImport`), then `askJobImport` to trigger processing.

- **Default: `bypassValidation: true`** — the bundle imports directly into the knowledge base. Requires the bypass capability on your token; if the mutation fails, the CLI reports that the file is uploaded but **parked in the analyst workbench** (Data → Import) awaiting human validation.
- **`--no-bypass`** — deliberately route the bundle through the workbench for review before it becomes knowledge. The right choice for intel you haven't manually validated.
- Import is **asynchronous** — the mutation returns immediately; poll with `lookup`/`search`. Small bundles land in seconds; `--wait N` sleeps after triggering if you're scripting a follow-up query.

Unlike MISP, OpenCTI is STIX-native: bundles from `/stix-bundle` import as-is, inline TLP marking-definitions included. No marking-definition surgery needed.

## Rate limits

None published — OpenCTI is self-hosted (or SaaS via Filigran) and the bottleneck is the instance's Elasticsearch/Redis backend. Be polite on shared instances: use `list` filters and `--limit` instead of paging everything, and batch writes. Default `--limit` is 25 (max 100 per page); paginate with the returned `end_cursor` via `--after`.

## Admiralty defaults (for `/score-source`)

**Source reliability:** OpenCTI aggregates — rate the *author/feed behind the entity* (the `createdBy` identity), not the platform:

| Entity origin | Reliability |
|---|---|
| Your own analysts (self-hosted instance) | A1 — primary source |
| Vendor connector (Mandiant, CrowdStrike, Recorded Future) | A2 / B2 |
| Open feeds (AlienVault OTX, abuse.ch, MISP feed connectors) | B3–C3 |

**Information credibility:** use the entity's own `confidence` field (0-100, maps onto `/confidence-levels` bands) and `x_opencti_score`; corroborate with the number of independent `createdBy` identities on related entities.

## Testing your credentials

```bash
python3 tools/clis/opencti.py version
```

A JSON response with a `version` string means auth works. `AUTH_REQUIRED` → wrong/missing token. Network error → check `OPENCTI_URL` (scheme, host, no trailing slash).

## Known quirks

- **`connectors` selects minimal fields** — selecting `works { status }` crashes on some 7.x instances (non-nullable `Work.status` bug), so the CLI deliberately doesn't.
- **Labels on 7.x take internal ids, not names** — the CLI resolves (and auto-creates) them before the mutation; you always pass names.
- **TLP names** — `add-marking` accepts `TLP:CLEAR|TLP:WHITE|TLP:GREEN|TLP:AMBER|TLP:AMBER+STRICT|TLP:RED` and resolves against the server's marking-definition catalog; TLP:WHITE only exists on instances that keep the legacy definition.

## See also

- Documentation: https://docs.opencti.io/
- Lookup skill: `skills/lookup-opencti/SKILL.md`
- Python CLI source: `tools/clis/opencti.py`
- Companion: `skills/stix-bundle/SKILL.md` for the STIX 2.1 bundle structure this consumes
- pycti (official Python SDK, when the CLI isn't enough): https://github.com/OpenCTI-Platform/client-python
- MISP counterpart (community exchange vs. internal knowledge base): `tools/integrations/misp.md`
