# MISP integration

[MISP](https://www.misp-project.org/) is the open-source threat-intelligence platform used by ISACs, CSIRTs, and many private CTI teams to share structured indicators, events, and context. Unlike the other integrations in this pack, MISP is **two-way**: you query existing events/attributes AND push new intel back into the platform.

## Getting credentials

1. Log into your MISP instance → top-right user menu → **My Profile** → **Auth keys** → **Add authentication key**.
2. Set:
   - **Comment:** `cti-skills CLI`
   - **Allowed IPs:** restrict to your egress IP if possible
   - **Expiration:** set a date — MISP supports keyed rotation
   - **Permissions:** match the role; for write operations the role needs `perm_add`, `perm_modify`, `perm_tag`, `perm_publish`
3. Copy the key (shown once).
4. Set both env vars:
   - `MISP_URL` — the base URL of your MISP instance (e.g. `https://misp.example.org`, **no trailing slash**)
   - `MISP_API_KEY` — the auth key from step 3

Add via `./scripts/setup.sh` or stash in `.claude/settings.local.json` `env` block.

## Authentication

MISP uses a non-standard auth header — the raw key, not `Bearer <key>`:

```
Authorization: <MISP_API_KEY>
Accept: application/json
Content-Type: application/json
```

The CLI sets this for you.

## Self-signed certs

Many MISP deployments are internal and use self-signed TLS certificates. Pass `--insecure` to skip verification on a per-call basis:

```bash
python3 tools/clis/misp.py search-events --value 1.2.3.4 --insecure
```

Don't disable verification globally — it's per-invocation by design.

## Endpoints used

The CLI (`tools/clis/misp.py`) covers query and write surfaces:

### Read

| Verb | Path | CLI subcommand |
|---|---|---|
| POST | `/events/restSearch` | `search-events` |
| POST | `/attributes/restSearch` | `search-attributes` |
| POST | `/objects/restsearch` | `search-objects` |
| GET  | `/events/view/{event_id}` | `get-event` |
| GET  | `/tags` / `/tags/search/{term}` | `list-tags` |

`restSearch` accepts a JSON body of filters: `value`, `type`, `category`, `tags`, `from`, `to`, `published`, `eventid`, `limit`, `page`, plus `returnFormat`. Setting `returnFormat: stix2` on a search-events call exports the result as a STIX 2 bundle — useful for cross-platform sharing.

### Write

| Verb | Path | CLI subcommand |
|---|---|---|
| POST | `/events/add` | `create-event` |
| POST | `/attributes/add/{event_id}` | `add-attribute` |
| POST | `/events/upload_stix/2[/publish:1][/galaxies_as_tags:1][/force_contextual_data:1]` | `upload-stix` |
| POST | `/events/addTag/{event_id}/{tag_id}/local:{0\|1}` | `tag-event` |
| POST | `/events/publish/{event_id}` | `publish-event` |

The STIX 2 import endpoint takes a STIX 2.x JSON bundle in the request body and creates one or more MISP events from it. The bundle should contain at minimum a `report` SDO (becomes the event title) plus the indicators/observables/relationships. See `skills/stix-bundle/SKILL.md` for the bundle structure used by this pack.

## Distribution levels

MISP's distribution model controls who sees what. Pass `--distribution N` on `add-attribute` and `create-event`:

| N | Meaning |
|---|---|
| 0 | Your organisation only |
| 1 | This community only (your MISP server's users) |
| 2 | Connected communities |
| 3 | All communities (full sharing) |
| 4 | Sharing group (requires a sharing-group ID) |
| 5 | Inherit event (attributes only) |

Default to `0` for unverified intel and `1` for community-shared work.

## Threat level + analysis fields

`create-event` accepts:

- `--threat-level 1..4` — 1=High, 2=Medium, 3=Low, 4=Undefined
- `--analysis 0..2` — 0=Initial, 1=Ongoing, 2=Completed

Map these from the threat assessment skill output if you want consistency across products.

## Rate limits

MISP itself has no public rate limits — the bottleneck is the host's CPU and DB. On shared community servers, be polite: batch your work, don't poll, and prefer `restSearch` filters over fetching+filtering client-side.

## Admiralty defaults (for `/score-source`)

**Source reliability:** depends on the MISP instance and the org that authored the event. Common defaults:

| Instance type | Reliability |
|---|---|
| Sector/national CSIRT MISP (CIRCL, FIRST, sector ISAC) | A (completely reliable) |
| Vendor-shared MISP (CrowdStrike, Mandiant, etc.) | B (usually reliable) |
| Community open MISP (e.g. CIRCL Public) | B-C (varies by Org) |
| Self-hosted internal | A1 (your own team's work, treat as primary) |

**Information credibility:** read off the event's `tags` and `Galaxy` clusters. Events tagged `admiralty-scale:source-reliability="a"` etc. carry an explicit rating; otherwise apply judgement based on:
- Is the event published and have other orgs tagged it?
- Are the attributes corroborated (`to_ids` flag set, sightings present)?
- Does it cite a primary report?

## STIX 2 round-tripping

This pack writes STIX 2.1 bundles per `skills/stix-bundle/SKILL.md`. To push them into MISP:

```bash
python3 tools/clis/misp.py upload-stix data/stix-bundles/2026-04-26-apt28-c2.json --publish --galaxies-as-tags
```

Flags worth knowing:
- `--publish` — auto-publish the imported event(s); skip if you want to review before sharing
- `--galaxies-as-tags` — map STIX SDOs (threat-actor, malware) to MISP galaxy tags rather than separate objects
- `--force-contextual-data` — preserve identity, marking-definition, and other STIX context objects that MISP would otherwise drop

### Gotcha: TLP marking-definitions in STIX 2 import

MISP's STIX 2 importer is strict about `marking-definition` objects. If your bundle uses the inline STIX 2.0 shape (`"definition_type": "tlp", "definition": {"tlp": "clear"}`), MISP returns:

```
Invalid value for Bundle 'objects': Marking marking-definition--... does not match spec marking
Does not match any TLP Marking definition!
```

Workarounds:
- **Drop the marking-definition object entirely** from the bundle and apply TLP via a `tag-event` call after import (cleanest path).
- Use only the canonical TLP-2.0 marking-definition UUIDs *by reference* — no inline `definition_type`/`definition` block — letting MISP resolve them from its built-in catalog.
- For non-MISP STIX consumers, the inline format from `/stix-bundle` is fine. The mismatch is MISP-specific.

## Testing your credentials

```bash
curl -sk -H "Authorization: $MISP_API_KEY" -H "Accept: application/json" "$MISP_URL/users/view/me" | head -c 300
```

A 200 with a JSON body that includes your user record means auth works. A 403 means the key is valid but lacks permission. A 401 means the key is wrong.

## Privacy + sharing semantics

- **Distribution is sticky** — once an event is published with distribution ≥ 1, it propagates to connected MISP servers and cannot be recalled. Default to `0` while drafting.
- **Sharing groups** are the granular control — use them when you need to share with named partners but not the whole community.
- **TLP markings as tags** — apply `tlp:red`, `tlp:amber+strict`, `tlp:green`, `tlp:clear` tags via `--tags` or `tag-event`. MISP will warn on conflicting TLP + distribution combinations.

## See also

- API docs: [MISP OpenAPI](https://www.misp-project.org/openapi/) and [PyMISP](https://github.com/MISP/PyMISP)
- Lookup skill: `skills/lookup-misp/SKILL.md`
- Python CLI source: `tools/clis/misp.py`
- Companion: `skills/stix-bundle/SKILL.md` for the STIX 2 bundle structure
- Tag taxonomies (TLP, admiralty, kill chain, etc.): https://github.com/MISP/misp-taxonomies
- Galaxy clusters (threat-actor, malware, etc.): https://github.com/MISP/misp-galaxy
