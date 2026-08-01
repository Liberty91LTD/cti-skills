# Liberty91 integration

[Liberty91](https://liberty91.com) is the threat-intelligence platform this skills pack comes from. Its API is the pack's only **first-party** integration: where VirusTotal or Shodan answer "what is known about this indicator", Liberty91 answers "what happened, who reported it, how well corroborated is it, and which of my organizations does it touch".

The integration is **two-way**: read the occurrence layer, the canonical threat catalog, IOCs, alerts and organization profiles; write your own reports in (`ingest`), queue intelligence packages, and manage organization documents.

## The two-layer model — read this first

Everything else follows from it.

- A **Threat Event** is a real-world occurrence: one breach, one exploitation campaign, one leak. Deduplicated, with every source you are entitled to attached.
- An **Event** is one *report about* an occurrence. A single breach covered by a vendor write-up, three news articles and a leak-site post is **five Events and one Threat Event**.

| You want | Endpoint | CLI |
|---|---|---|
| What happened, deduplicated, with all its sources | `GET /threat-events/` | `threat-events` |
| The individual documents — who published what | `GET /events/` | `events` |

Consume `/threat-events/` and you read each occurrence once, with disagreement between sources visible. Consume `/events/` and you get five rows to dedupe yourself. Every Event carries `threat_event_id`, so you can move between layers.

**Default to `threat-events`.** Drop to `events` only when the question is genuinely about documents ("what did vendor X publish this week", "poll my own ingested report until enrichment completes").

### What a Threat Event row carries (v2.1)

List rows gain six fields, each identical in shape to the corresponding block on the detail response: `actors`, `malware`, `vulnerabilities` (all `{id, name, from_private_source}`, where `id` is the **canonical** catalog id), `techniques` (ATT&CK, derived for the occurrence), `victims` (`{name, role}`) and `source_countries` (uppercase ISO codes). `sectors` and `regions` were already there and are unchanged; `regions` covers target regions and countries. The detail response gains `source_countries` too.

Because the canonical ids are on the row, a list result feeds `entity <type> <id>` directly, with no detail call in between — a real credit saving now that pages are a quarter the size.

Two semantics worth stating rather than discovering:

- **The list shows publicly-linked entities only.** An entity named *only* in a report private to your account appears on the detail but **not** on the list row. This is deliberate: the list matches what the new entity filters match on, so filtering and display agree. Absence from a row is not absence from the occurrence.
- **`source_countries` counts only publicly-sourced, non-disputing reports.** Private and user-uploaded reports never contribute one.

`/search/` and `/alerts/{id}/matches/` still return the **base** Threat Event shape and did **not** gain these six fields.

### The full source list (v2.1)

`GET /threat-events/{id}/sources/` is a paginated, masked list of every report behind an occurrence, newest first, with rows of `report_id`, `title`, `url`, `source_name`, `module`, `published_at`, `stance`, `reliability`, `reliability_label`, `event_id`.

**Use it over the detail when the reporting itself is the question.** The detail's embedded `sources[]` is **capped** and is unchanged, so for a heavily corroborated occurrence that block is a sample while this endpoint is the complete record. You still only see reports your account is entitled to, and the counts on the Threat Event are computed the same way, so nothing here reveals reporting you do not hold. Scopes: `threat-events.read` + `events.read`.

## Getting credentials

1. Log into the Liberty91 platform → user menu → **API Access**. Keys are created by an account **Owner** or **Admin**.
2. Choose a key type: `l91_live_` for production, `l91_test_` for development.
3. The full secret is shown **once**, at creation — afterwards only a prefix and last four characters are stored. Lost keys are rotated, not recovered.
4. Set `LIBERTY91_API_KEY`. Add via `./scripts/setup.sh`, `/cti-setup`, or the `env` block of `.claude/settings.local.json`.

Optional env vars: `LIBERTY91_API_URL` (defaults to `https://api.liberty91.com/api/v1` — override for a staging host), `LIBERTY91_PROXY` (or `HTTPS_PROXY`).

Give each integration its own key with only the scopes it needs — that also gives clean per-integration usage and rate-limit visibility. Revocation takes effect within ~30 seconds.

## Authentication

Either header form works; the CLI sends the first:

```
X-API-Key: l91_live_xxxxxxxxxxxxxxxxxxxxxxxx
Authorization: Bearer l91_live_xxxxxxxxxxxxxxxxxxxxxxxx
```

Never put the key in a query parameter, and never let it reach a browser — this is a server-to-server API.

## Scopes

A key carries a set of scopes. **An empty scope list grants all read scopes**; write scopes are always explicit. Scopes are ANDed where an endpoint lists more than one, and calling without one returns `403` naming what is missing.

| Scope | Grants | CLI commands |
|---|---|---|
| `threat-events.read` | Threat Events, their sources, IOCs, STIX | `threat-events`, `threat-event` |
| `events.read` **+ the two above** | *(v2.1)* `GET /threat-events/{id}/` and `…/sources/` — see the note below | `threat-event --section detail\|sources` |
| `threats.read` | Threat library (actors, malware, vulnerabilities, clusters) | `library`, `entity` |
| `search.read` | Search + saved searches | `search`, `saved-searches`, `run-search` |
| `events.read` | Individual reports | `events`, `event` |
| `iocs.read` | IOC lookup/list/export — **also required** for every per-entity and per-occurrence IOC and STIX sub-resource | `iocs`, `ioc-lookup`, `ioc-export`, `--section iocs\|iocs-export` |
| `reports.read` | Intelligence packages | `reports`, `report`, `report-download` |
| `alerts.read` | Alert rules and matches — *(v2.1)* `alerts` additionally needs `orgs.read` + `search.read` + `threats.read` | `alerts`, `alert-matches` |
| `orgs.read` | Organizations, assets, suppliers, documents | `orgs`, `org`, `org-document` |
| `events.write` | Ingest your own reports | `ingest` |
| `reports.generate` | Generate intelligence packages | `report-generate` |
| `orgs.write` | Upload documents, confirm entities, refresh descriptions | `upload-document`, `confirm-entities`, `refresh-description` |

A read-only key with no scopes set is the right default for enrichment work.

**Two endpoints widen their scope requirements in v2.1, and both are breaking for narrowly-scoped keys.** The rule behind both is the same, and it is worth internalising: *an endpoint requires the scope of every resource it actually returns.*

- **`GET /threat-events/{id}/`** goes from `threat-events.read` + `orgs.read` to those **plus `events.read`**. The detail embeds `sources[]`, which is the report layer — the same projection `…/sources/` serves behind `events.read`. Without this, withholding `events.read` bought nothing; it only changed which URL the caller used. Three scopes on the flagship detail endpoint is a lot, and the honest framing is that it is a join across three resources: the occurrence, your organizations' relevance, and the reporting behind it. A caller who wants only the occurrence should use the list, which still needs `threat-events.read` alone.
- **`GET /alerts/`** goes from `alerts.read` to **`alerts.read` + `orgs.read` + `search.read` + `threats.read`**, because the rule's `criteria` block returns suppliers and asset technologies (`orgs.read`), the effective `query_tree` (`search.read`) and threat clusters (`threats.read`). Previously a key holding only `alerts.read` was refused all of those endpoints and could still read the same data here.

Audited on production 2026-07-31: **zero** issued keys currently carry `alerts.read` at all, so the alerts tightening breaks no existing key. Re-run that audit at deploy time if keys have been issued since.

## What your account can see

Threat Events are shared records, so the visibility rule matters:

**You see a Threat Event when you are entitled to at least one of the reports behind it, and you see only those reports.** `report_count` and `source_count` are computed over only the reports you can see — a count including sources you are not entitled to would tell you they exist.

- **Titles.** If you are entitled to an occurrence only through a report you uploaded or licensed privately, the `title` is your own report's title. Once public reporting names the occurrence, the public headline becomes the shared title.
- **Your uploads.** A report you `ingest` is private to your account. It corroborates an occurrence you can already see, or creates one only you can see, and is masked out of every other account. IOCs extracted from it are marked `TLP:RED` — respect that on export.
- **Tenancy.** Objects belonging to another account return `404`, not `403` — a `403` would confirm the object exists. Don't read a `404` as "deleted".

## API surface

Base `https://api.liberty91.com/api/v1`. A machine-readable schema (`/schema/`) and interactive reference (`/docs/`) are public and need no key.

| Kind | CLI subcommand | Endpoint |
|---|---|---|
| Read | `quota` | probes `/threat-events/`, falls back to `/iocs/` — reports `X-RateLimit-*` / `X-Credits-*` |
| Read | `threat-events` | `GET /threat-events/` — 17 filters, cursor-paginated |
| Read | `threat-event <id> [--section detail\|iocs\|sources\|stix\|iocs-export]` | `GET /threat-events/{id}/[iocs/\|sources/\|stix/\|iocs/export/]` |
| Read | `library <entity_type>` | `GET /threat-library/{type}/` — `--name`/`--alias` resolve a name to an id |
| Read | `entity <entity_type> <id> [--section …]` | `GET /threat-library/{type}/{id}/[iocs/\|related/\|techniques/\|threat-events/\|stix/\|iocs/export/]` |
| Read | `search` | `POST /search/` — flat criteria or a `query_tree` |
| Read | `saved-searches`, `saved-search <id>`, `run-search <id>` | `GET /searches/`, `GET /searches/{id}/`, `POST /searches/{id}/run/` |
| Read | `events`, `event <id>` | `GET /events/`, `GET /events/{id}/` |
| Read | `ioc-lookup <value>`, `iocs`, `ioc-export` | `GET /iocs/lookup/`, `GET /iocs/`, `GET /iocs/export/` |
| Read | `reports`, `report <id>`, `report-download <id>` | `GET /reports/…` |
| Read | `alerts`, `alert-matches <id>` | `GET /alerts/`, `GET /alerts/{id}/matches/` |
| Read | `orgs`, `org <id> --section …`, `org-document` | `GET /organizations/…` |
| Write | `ingest` | `POST /events/ingest/` — 202, then poll `event <id>` |
| Write | `report-generate` | `POST /reports/generate/` — 50 credits **per report** |
| Write | `upload-document`, `confirm-entities`, `refresh-description` | `POST /organizations/{org}/documents/`, `…/entities/confirm/`, `POST /entities/{type}/{id}/update-description/` |

`search` and `run-search` are `POST` but are **reads** — a default-scoped key can use them.

Every subcommand accepts `--dry-run` (print the request, don't send) and `--insecure` (skip TLS verification — non-production hosts only).

## Search and alert criteria (v2.1)

Six new `query_tree` leaf fields on `POST /search/` and on saved searches:

| Leaf | Values | Matches |
|---|---|---|
| `canonical_actor` | UUID[] | threat actor from the deduplicated cross-tenant catalog |
| `canonical_malware` | UUID[] | malware, same catalog |
| `canonical_vulnerability` | UUID[] | vulnerability, same catalog |
| `incident_technique` | ATT&CK codes, e.g. `T1566`, `T1566.001` | techniques derived for the **occurrence** |
| `affected_organization` | UUID[] | one of **your own** customer organizations |
| `relevant_to_me` | exactly one of `true`/`false`/`1`/`0`/`yes`/`no` | occurrence intersects any of your organizations' profiles |

The legacy leaves (`threat_actor`, `malware`, `vulnerability`, `threat_cluster`) still work and are **not** removed, but they match your account-local entities while the canonical ones match the deduplicated catalog — **document and default to the canonical ones.** `technique` and `incident_technique` are different questions and both are kept: `technique` matches what a single *report* named; `incident_technique` matches the set derived for the *occurrence*, which merges every source and can carry an assertion no individual report made. Tree grammar and caps are unchanged: depth 3, 50 nodes, 50 values per leaf, 3 free-text leaves.

**The caveat that generates support tickets if left undocumented:** an entity filter returns strictly **fewer** results than a free-text search for the same name. A report not yet matched into an occurrence has no canonical links, so no entity filter can return it even when its text plainly names the actor. That is correct behaviour — the two are different questions — but users read it as missing data unless it is stated right next to the entity filters.

**Alert rules take a `query_tree` on create and update**, so an alert can now use any search filter including all six above; previously a rule could only carry a tree by being created from a saved search. Precedence when more than one source of criteria is present: **linked saved search → the rule's own `query_tree` → the flat criteria fields.** A malformed tree is rejected at write time rather than stored, and `query_tree` round-trips (it is returned on read, inside `criteria` on the public API). `criteria.query_tree` now always reflects what the rule actually evaluates: for a rule configured only through the flat criteria fields it returns the tree those compile to, where it previously returned `null`. Treat it as the authoritative statement of what a rule fires on.

## Pagination

Every list endpoint uses cursor pagination with one envelope: `{next, previous, results}` (search and alert matches add `unlinked_report_count`). Page size is set with `--page-size`.

| | Pre-v2.1 | **v2.1** |
|---|---|---|
| default `page_size` | 100 | **25** |
| maximum `page_size` | 500 | **100** |

This applies to **every paginated endpoint**, not just Threat Events, and it is a breaking change for anyone who paginates. **A full walk of a large result set now takes 4x as many requests.** Credits are charged per request and the rate limit is a fixed window per key, so the same data costs up to 4x the credits and 4x the rate-limit budget. Tell any integrator with a paginating job before they upgrade.

The CLI omits `page_size` unless you pass `--page-size`, so it inherits whichever default the host serves and needs no change. The thing to watch is `--max-pages` (default 10): the same `--all --max-pages 10` that walked up to 5,000 rows walks 250 against a v2.1 host. Check `truncated` before treating a count as complete.

`next` is a complete URL — **never build cursor parameters yourself**, and don't store cursors beyond the current walk. The CLI follows `next` when you pass `--all`, capped by `--max-pages` (default 10) so a walk can't quietly burn the credit pool; when it stops early the response carries `truncated: true` and the `next` URL to resume from via `--cursor`.

## Rate limits and credits

Every response carries `X-RateLimit-Limit` / `-Remaining` / `-Reset` and `X-Credits-Limit` / `-Remaining`. The CLI echoes them in a `_meta` block on every successful response — watch `credits_remaining`.

| Cost | Operations |
|---|---|
| 1 | Most reads: lists, details, lookups, sub-resources |
| 2 | Threat Event detail, report detail, search, running a saved search |
| 5 | STIX bundle export, report download |
| 10 | IOC export, ingesting a report |
| 25 | Document upload |
| 50 | Report generation *(per report generated)* |

Failed requests (4xx and 5xx) never consume credits. A `429` is either rate limiting **or** exhausted monthly credits — check `X-Credits-Remaining` to tell them apart; the CLI does this for you and says which in the error.

## Errors

| Status | Meaning | CLI behaviour |
|---|---|---|
| `400` | Unknown filter value, malformed date, invalid body | surfaces `detail`, which names the field |
| `401` | Missing / malformed / revoked / expired key | tells you to check `$LIBERTY91_API_KEY` |
| `403` | Key lacks a scope | names the missing scope from `detail` |
| `404` | Not found, or not in your account — indistinguishable by design | flags the possibility of a pre-v2.0 host |
| `409` | The user who created the key is no longer active | rotate the key |
| `429` | Rate limited **or** credits exhausted | distinguishes the two via `X-Credits-Remaining` |
| `503` | Upstream dependency unavailable | retry with backoff; **writes are not retried server-side — resubmit** |

**An unrecognised filter value is a `400`, not an empty result set.** A mistyped sector silently returning zero rows would read as "nothing matches", which is the opposite of the truth — so treat a `400` as a typo in your query, not as absence of data.

## Reading the trust signals

Three separate judgements travel with every occurrence. They map onto the pack's tradecraft skills almost exactly — which is why `/lookup-liberty91` output needs less re-rating than any other lookup.

**Source reliability** — a property of the *publisher*, on each source, NATO Admiralty `A`–`F` (A completely reliable … F cannot be judged). Grades start from the source class — government at A, vendors at B, news at C — and move on evidence. Feed straight into `/source-assessment`.

**Credibility** — a property of the *occurrence*, Admiralty information-credibility `1`–`6`, **lower is better**. Only public, attributable reporting counts, and re-published copies of one story collapse to a single source, so syndication cannot inflate it.

| Band | Label | Read it as |
|---|---|---|
| 1 | Confirmed | Several reliable independent sources — actionable |
| 2 | Probably True | Independently corroborated — actionable |
| 3 | Possibly True | A single moderate source — corroborate before acting |
| 4 | Doubtful | Weak or passing sourcing only |
| 5 | Improbable | Only unreliable-grade sourcing |
| 6 | Cannot be judged | No attributable sources |

`credibility` (number) and `credibility_label` (word) are both `null`/empty when the occurrence has not been scored.

**Verification** — where the occurrence stands overall: `auto` (machine-created, single source), `corroborated` (2+ independent sources), `verified` (analyst confirmed), `disputed` (a source disputes it), `rejected` (judged not real), `merged` (folded into another — see `merged_into`). Analyst judgements are never overwritten by the automatic pipeline.

**Stance** — a property of each *report*, not the occurrence: `claims`, `corroborates`, `updates`, `mentions`, `disputes`. Disagreement stays visible rather than being averaged away; surface it rather than reporting a consensus that doesn't exist.

Suggested triage filter: `--verification corroborated --min-credibility 2`.

## Admiralty defaults (for `/score-source`)

Liberty91 emits Admiralty ratings natively, so **use the platform's own numbers rather than a fixed default**:

| Situation | Rating |
|---|---|
| Occurrence with per-source `reliability` + occurrence `credibility` | use them verbatim — that is the whole point |
| Occurrence not yet scored (`credibility: null`) | **B6** — reliability from the source class, credibility cannot be judged |
| Platform-level default when nothing else is available | **B2** |
| A report *you* ingested | **A1** if your own analysts wrote it; otherwise rate the original author |

Downgrade to the *worst* contributing source when an occurrence rests on one `D`/`E`-graded publisher, regardless of how confident the summary sounds.

## Testing your credentials

```bash
python3 tools/clis/liberty91.py quota
```

A JSON response with `authenticated: true` and a `_meta` block means the key works. `401` → wrong or revoked key. `409` → the creating user is no longer active on the account.

## Known quirks and deployment state

- **v2.1 is documented here but is live nowhere yet.** Everything tagged *(v2.1)* in this file — the 25/100 page sizes, the six new list fields, `…/sources/`, the canonical search leaves, the widened scopes on `/threat-events/{id}/` and `/alerts/`, the writable alert `query_tree` and the sector-matcher fix — sits on an unmerged feature branch. It is not on staging, and production is still behind even v2.0. Verified against the branch head's served schema on 2026-07-31, but **check `/api/v1/schema/` for what a given host actually serves before relying on any of it.**
- **Alert rules with a sector condition have never fired.** `AlertRule.target_sectors` stores two-letter sector codes while events store sector display names, and the matcher compared the two directly, so the condition was always false. The auto-created rule every new account receives is *country AND sector*, which means **that rule has never produced a single alert**. v2.1 fixes the matcher and those rules begin firing for the first time. Consequences worth communicating before it ships: accounts that read "no alerts" as "no matching activity" were wrong, first-activation volume may be substantial, and **nobody needs to change any configuration** — the rules were always correct, the matcher was not. A proactive note beats letting inboxes explain it.
- **The occurrence layer may not be deployed on your host.** API v2.0 (29 July 2026) introduced `/threat-events/`, `/search/`, `/searches/` and renamed `/threats/` → `/threat-library/`. As of 31 July 2026 `https://api.liberty91.com` still serves the pre-2.0 surface: those four paths return `404` while `/events/`, `/iocs/`, `/reports/`, `/alerts/` and `/organizations/` work normally, and the old `/threats/{type}/` path still answers. `quota` detects this and reports `occurrence_layer_available: false`. Until v2.0 lands, work from `events` and dedupe by hand, or check `/api/v1/schema/` for what is actually deployed. The CLI targets the documented v2.0/v2.1 contract and needs no change when it ships.
- **`threat_event_id` on `/events/` rows** arrived with v2.0. On a pre-2.0 host the field is simply absent — treat its absence as "unknown", never as "unlinked".
- **IOC `confidence` is derived at read time**, not a stored column, and is `null` (empty in CSV) when there is genuinely no signal — *not* a misleading middling 50. Before the 2026-07-29 fix, JSON and CSV returned a stored value while STIX returned the derived one; all three now agree. If a pre-fix host returns a suspiciously uniform `50`, that is the stored default, not a judgement.
- **`/events/ingest/` now accepts `text`.** The field name was documented but never read, so a request following the old documentation created a report with an empty body. Both `text` and `description` are accepted; the CLI sends `text`.
- **`enrichment_status` is validated** — an unrecognised value is a `400`, where it previously returned an empty page with a `200`.
- **Clusters are account-local** groupings with no canonical record: the `techniques`, `threat-events` and `related` sub-resources return `400` for them. The CLI refuses those combinations locally rather than spending a request.
- **Flat vs parented STIX.** `ioc-export --format stix` is an indicator list with no context — right for a blocklist, wrong for a TIP. For TIP sync use `threat-event <id> --section iocs-export` (or the entity equivalent), which carries the occurrence plus relationships to each indicator.
- **Document upload is multipart.** The published schema types the `file` field as `uri`, which is how DRF renders a `FileField`; the CLI posts `multipart/form-data`. If a deployment rejects that, fall back to the platform UI.
- **The v1 contract only grows.** Fields and endpoints are added, never renamed or removed — so ignore fields you don't recognise, and don't depend on key order or on a field's absence.

## See also

- Documentation: https://api.liberty91.com/api/v1/docs/ · schema: https://api.liberty91.com/api/v1/schema/
- Lookup skill: `skills/lookup-liberty91/SKILL.md`
- Python CLI source: `tools/clis/liberty91.py`
- Knowledge-base siblings (same read-then-write shape): `tools/integrations/opencti.md`, `tools/integrations/misp.md`
- `skills/stix-bundle/SKILL.md` — the bundle structure `--section stix` produces
