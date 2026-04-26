---
name: lookup-misp
description: Use when you need to query a MISP instance for existing events/attributes/objects, or push new intel into MISP — adding attributes to an event, creating an event, or uploading a STIX 2 bundle as one or more events. Two-way integration. Commonly invoked by /ip-investigation and friends to check whether an indicator is already known to your CTI sharing community, and by analytical skills that want to publish their findings back to MISP. Reads $MISP_URL and $MISP_API_KEY.
metadata:
  version: 1.0.0
  tags: [lookup, write, threat-intel, sharing, stix]
  api: misp
  default_source_reliability: B
  default_information_credibility: 2
---

# lookup-misp

Two-way bridge to a MISP threat-intelligence platform. Unlike the other `lookup-*` skills, this one **also writes** — it can create events, add attributes, tag events, and import STIX 2 bundles. Treat write commands as deliberate actions; don't use them in autonomous enrichment loops.

## When to invoke

**Read:**
- An indicator was found by another lookup (VT, OTX, …) — check whether MISP already has it
- An analyst wants the most recent published events for a threat actor or campaign
- You need to export a slice of MISP as a STIX 2 bundle for sharing

**Write:**
- A finished investigation produced indicators that should be shared with the community
- An existing event needs to be enriched with newly observed attributes
- A STIX 2 bundle written via `/stix-bundle` should be pushed into MISP as event(s)

**Do NOT invoke for:**
- Bulk enrichment (use VT/OTX first; only push the high-confidence subset to MISP)
- Pivoting on raw indicators — MISP is a *curated* dataset, not a scanning service. Use Shodan/Censys for that.

## How to invoke

Single Python CLI (stdlib only — no install).

### Read operations

```bash
# Search published events containing a value, optionally filtered by tag/date/published
python3 tools/clis/misp.py search-events --value 1.2.3.4 --tag tlp:white --limit 20
python3 tools/clis/misp.py search-events --tag misp-galaxy:threat-actor=\"APT28\" --from 2026-01-01

# Search attributes (the most common indicator lookup)
python3 tools/clis/misp.py search-attributes --type ip-dst --value 1.2.3.4
python3 tools/clis/misp.py search-attributes --type sha256 --value <hash> --limit 5

# Inspect a single event (full attribute + object detail)
python3 tools/clis/misp.py get-event 12345

# Search objects within an event
python3 tools/clis/misp.py search-objects --event-id 12345 --name file

# Resolve tag names → ids (needed before applying tags)
python3 tools/clis/misp.py list-tags --search tlp

# Export a search result as a STIX 2 bundle (cross-platform sharing)
python3 tools/clis/misp.py search-events --tag malware-family:lockbit --returnFormat stix2 > out.json
```

### Write operations

```bash
# Add one attribute to an existing event
python3 tools/clis/misp.py add-attribute 12345 \
  --type ip-dst --value 185.220.101.45 \
  --category 'Network activity' \
  --comment 'C2 observed 2026-04-25' \
  --to-ids true \
  --distribution 1 \
  --tags 'tlp:amber,kill-chain:command-and-control'

# Create a new event (skeleton — add attributes/objects after)
python3 tools/clis/misp.py create-event \
  --info 'APT28 C2 cluster — April 2026' \
  --threat-level 2 --analysis 1 \
  --distribution 1 \
  --tags 'tlp:amber,misp-galaxy:threat-actor="APT28"'

# Upload a STIX 2 bundle as one or more events (the canonical bulk-import path)
python3 tools/clis/misp.py upload-stix data/stix-bundles/2026-04-26-apt28-c2.json \
  --publish --galaxies-as-tags --force-contextual-data

# Tag an existing event (resolves tag name → id automatically)
python3 tools/clis/misp.py tag-event 12345 'tlp:amber'

# Publish an event (makes it visible to other orgs at the chosen distribution)
python3 tools/clis/misp.py publish-event 12345
```

All commands accept `--dry-run` (preview the HTTP call without sending) and `--insecure` (skip TLS verification, common on internal MISP deployments).

The CLI exits 2 if `MISP_URL` or `MISP_API_KEY` is unset (when not in dry-run). Report missing credentials; do not fabricate.

## Distribution levels

`--distribution N` on `add-attribute` and `create-event`:

| N | Meaning | Use when |
|---|---|---|
| 0 | Your org only | Drafting, unverified, sensitive sources |
| 1 | This community | Published intel for your MISP server's users |
| 2 | Connected communities | Trusted federated sharing |
| 3 | All communities | Open community sharing |
| 4 | Sharing group | Named-partner sharing (needs sharing-group id) |
| 5 | Inherit event | Attributes that should track their parent event |

Default to **0** while drafting. Bump to **1+** only after review and TLP alignment.

## STIX 2 round-tripping

This is the killer feature. The pack already writes STIX 2.1 bundles via `/stix-bundle`; `upload-stix` pushes them into MISP intact:

1. Run an investigation (e.g. `/ip-investigation`)
2. Build a STIX bundle from the findings (`/stix-bundle`)
3. Apply TLP + Admiralty (`/apply-tlp`, `/score-source`)
4. `python3 tools/clis/misp.py upload-stix <bundle.json> --galaxies-as-tags`
5. Review in MISP → add context → publish

For exporting MISP → STIX, set `--returnFormat stix2` on `search-events`.

**Gotcha:** MISP's STIX 2 importer rejects inline TLP marking-definition objects (the STIX 2.0 `definition_type: "tlp"` shape that `/stix-bundle` produces). Either drop the marking-definition from the bundle and apply TLP via `tag-event` after import, or trim the bundle to references only. See `tools/integrations/misp.md` for details.

## Response format

Read commands return:

```yaml
source: misp
operation: search-events | search-attributes | get-event | ...
query_time: <ISO8601>
filters: <echoed filters>
count: <n>
events|attributes|objects: [<distilled summaries>]
raw: <full response on get-event for completeness>
```

Write commands return:

```yaml
source: misp
operation: add-attribute | create-event | upload-stix | ...
query_time: <ISO8601>
event_id|event|attribute: <created/updated object summary>
result|raw: <MISP response envelope>
```

## Source reliability (Admiralty default)

Default rating for downstream `/score-source`: **B2** (usually reliable, probably true). MISP is a sharing platform — the *underlying* org's reliability matters more than MISP itself. Adjust based on the event's `Org`/`Orgc`:

- Sector CSIRT or national CERT (CIRCL, FIRST, ISAC) → **A1**
- Reputable vendor (Mandiant, CrowdStrike, ESET) → **A2** / **B2**
- Anonymous community contributor → **C3**
- Your own org (self-hosted) → **A1** — primary source

Read the event tags too: `admiralty-scale:source-reliability="b"` and `admiralty-scale:information-credibility="2"` are common.

## Operational notes

- **Distribution is sticky.** Once a published event syncs to other servers, it can't be recalled. Default to draft (`0`) and review before publishing.
- **Tagging matters.** TLP, kill-chain, and galaxy tags drive how MISP routes events to subscribers. Don't skip them.
- **PyMISP exists** — for complex workflows (sightings, warninglists, feed management) the [PyMISP library](https://github.com/MISP/PyMISP) is the right tool. This CLI covers the 80% case for query + write, stdlib-only.
- **Don't autopublish.** `--publish` on `upload-stix` is convenient but bypasses the human review step. Skip it for intel you haven't manually validated.

## Related skills

- `/stix-bundle` — write STIX 2.1 bundles that this CLI's `upload-stix` consumes
- `/lookup-virustotal`, `/lookup-otx` — community reputation lookups; chain before pushing to MISP
- `/score-source` — apply Admiralty rating before publishing
- `/apply-tlp` — set TLP markings before publishing
- `/intelligence-sharing` — broader sharing-model context (TAXII, ISACs, MISP communities)
- `/ip-investigation`, `/domain-investigation`, `/hash-investigation`, `/url-investigation` — produce findings that MISP write commands consume

## See also

- Integration setup: `tools/integrations/misp.md`
- Python CLI source: `tools/clis/misp.py`
- MISP project: https://www.misp-project.org/
- OpenAPI reference: https://www.misp-project.org/openapi/
- PyMISP (full SDK, when this CLI isn't enough): https://github.com/MISP/PyMISP
- Tag taxonomies: https://github.com/MISP/misp-taxonomies
- Galaxy clusters: https://github.com/MISP/misp-galaxy
