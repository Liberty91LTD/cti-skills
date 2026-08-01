---
name: lookup-liberty91
description: Use when you need Liberty91 platform intelligence — what actually happened (deduplicated Threat Events with every source, Admiralty reliability/credibility and verification stage), whether an IOC is already known to your account, the canonical threat library (actors, malware, vulnerabilities, clusters, ATT&CK TTPs), alert matches, or which of your customer organizations an occurrence affects — or when you need to push intelligence back: ingesting your own report, generating an intelligence package, or uploading an organization document. Two-way, first-party integration. Commonly invoked by /ip-investigation and friends, /ioc-enrichment-workflow, /threat-actor-profiling, /campaign-tracking and /vulnerability-intelligence. Reads $LIBERTY91_API_KEY.
metadata:
  version: 1.1.0
  tags: [lookup, write, threat-intel, knowledge-base, first-party, stix]
  api: liberty91
  default_source_reliability: B
  default_information_credibility: 2
---

# lookup-liberty91

Two-way bridge to the [Liberty91](https://liberty91.com) platform — the pack's only **first-party** integration. Where VirusTotal or Shodan answer *"what is known about this indicator"*, Liberty91 answers *"what happened, who reported it, how well corroborated is it, and which of my organizations does it touch"*.

Like `/lookup-misp` and `/lookup-opencti`, this skill **also writes**: it ingests your own reports, queues intelligence packages, and manages organization profiles. Writes publish into your Liberty91 account and are metered — **confirm with the user before invoking any write command**, and never run one inside an autonomous enrichment loop.

## The two-layer model — read this first

Everything else follows from it.

- A **Threat Event** is a real-world occurrence: one breach, one exploitation campaign, one leak. Deduplicated, with every source you are entitled to attached.
- An **Event** is one *report about* an occurrence. A breach covered by a vendor write-up, three news articles and a leak-site post is **five Events and one Threat Event**.

| You want | Command |
|---|---|
| What happened, deduplicated, with all its sources | `threat-events` |
| The individual documents — who published what | `events` |

**Default to `threat-events`.** Drop to `events` only when the question is genuinely about documents ("what did vendor X publish this week", "poll my ingested report until enrichment completes"). Every Event carries `threat_event_id` so you can move between layers.

## When to invoke

**Read:**
- The user asks what has happened — to a sector, a country, an organization, in a date window (`threat-events`)
- An indicator surfaced elsewhere and you want to know whether the platform already holds it (`ioc-lookup`)
- An actor / malware family / CVE needs its canonical record, aliases, ATT&CK TTPs, linked occurrences or co-occurring entities (`library`, `entity`)
- A vendor's name for an actor needs resolving to the canonical entry (`library threat-actors --alias "…"`)
- The user wants their alert rules' matches, or a saved search re-run (`alert-matches`, `run-search`)
- A TIP (MISP, OpenCTI) needs parented STIX for an occurrence (`threat-event <id> --section iocs-export`)
- The user asks which of their customer organizations is affected, or about an org's assets/suppliers (`threat-event --section detail`, `orgs`, `org`)

**Write — confirm with the user first:**
- A finished investigation or an external report should live in the platform (`ingest`)
- The user wants an intelligence package generated (`report-generate` — 50 credits *per report*)
- An organization profile needs a document ingested or extracted entities confirmed (`upload-document`, `confirm-entities`, `refresh-description`)

**Do NOT invoke for:**
- Raw internet reconnaissance — Liberty91 is curated intelligence, not a scanner. Use Shodan/Censys.
- Bulk third-party reputation sweeps — run VT/OTX/RL first, then check the vetted subset here.
- Community sharing — that is MISP's job (`/lookup-misp`). Liberty91 is your intelligence source and customer-facing production platform.

## How to invoke

Single Python CLI, stdlib only — no install, no venv.

### Occurrences

```bash
# Connectivity, quota, and which API surface this host serves
python3 tools/clis/liberty91.py quota

# Triage feed: occurrences at least two independent sources agree on, mapped to your account
python3 tools/clis/liberty91.py threat-events --relevant --verification corroborated --min-credibility 2

# Scope by sector / country / technique / time
python3 tools/clis/liberty91.py threat-events --target-sector energy --target-country AE --last-reported-after 2026-07-01
python3 tools/clis/liberty91.py threat-events --technique T1566.001 --event-class security-incident
python3 tools/clis/liberty91.py threat-events --organization <org-uuid> --all --max-pages 5

# One occurrence: the evidence — sources with stance + reliability, entities, ATT&CK, org relevance
python3 tools/clis/liberty91.py threat-event <id>
python3 tools/clis/liberty91.py threat-event <id> --section iocs
python3 tools/clis/liberty91.py threat-event <id> --section sources     # every report behind it, paginated
python3 tools/clis/liberty91.py threat-event <id> --section iocs-export --out bundle.json   # parented STIX for a TIP
```

**The list row now carries the entities.** From API v2.1, `threat-events` rows include `actors`, `malware`, `vulnerabilities`, `techniques`, `victims` and `source_countries` alongside the `sectors` and `regions` they always had. Actor/malware/vulnerability entries are `{id, name, from_private_source}` where `id` is the **canonical** catalog id, so you can go straight from a list row to `entity <type> <id>` without paying for a detail call first, which matters more now that pages are a quarter the size. Three caveats that change what you may conclude:

- **List rows show publicly-linked entities only.** An entity named *only* in a report private to your account appears on the detail response but not on the list row. Absence from a row is not absence from the occurrence.
- **`source_countries` counts only publicly-sourced, non-disputing reports.** Private and user-uploaded reports never contribute one, by design.
- **Only `threat-events` rows gained these.** `search` and `alert-matches` still return the **base** Threat Event shape without them, so do not write a pipeline that expects `actors` on every occurrence row regardless of where it came from.

**`--section sources` vs the sources in `detail`.** The detail response embeds a `sources[]` block that is **capped**: for a heavily corroborated occurrence it is a sample, not the record. `--section sources` paginates the full set, newest first, and is the one to use when you are counting or citing reporting. Both are masked to what your account is entitled to, so neither reveals reporting you do not hold. It costs an extra scope: `threat-events.read` **plus** `events.read`.

### Threat library (canonical catalog)

```bash
# Resolve a name — or a vendor's alias — to a canonical id, then track the id, not the string
python3 tools/clis/liberty91.py library threat-actors --name "APT28"
python3 tools/clis/liberty91.py library threat-actors --alias "Fancy Bear"
python3 tools/clis/liberty91.py library vulnerabilities --q "CVE-2026-2" --tracked

# The record and its sub-resources (entity types: threat-actors | malware | vulnerabilities | clusters)
python3 tools/clis/liberty91.py entity threat-actors <id>
python3 tools/clis/liberty91.py entity threat-actors <id> --section techniques      # dated ATT&CK observations
python3 tools/clis/liberty91.py entity threat-actors <id> --section threat-events   # occurrences it was named in
python3 tools/clis/liberty91.py entity threat-actors <id> --section related         # co-occurring entities
python3 tools/clis/liberty91.py entity malware <id> --section iocs
```

### Search, events, IOCs, alerts, organizations

```bash
# Search returns Threat Events, not reports (POST, but a read — a default-scoped key can use it)
python3 tools/clis/liberty91.py search --free-text "wiper" --target-sector energy --date-from 2026-06-01T00:00:00Z
python3 tools/clis/liberty91.py search --query-tree-file tree.json    # the full grammar
python3 tools/clis/liberty91.py saved-searches
python3 tools/clis/liberty91.py run-search <id>

# Individual reports
python3 tools/clis/liberty91.py events --since 2026-07-01 --threat-event <uuid>
python3 tools/clis/liberty91.py event <id>

# IOCs
python3 tools/clis/liberty91.py ioc-lookup 185.220.101.45
python3 tools/clis/liberty91.py iocs --kind domain --verdict MALICIOUS --since 2026-07-01
python3 tools/clis/liberty91.py ioc-export --format csv --out iocs.csv     # blocklist, not TIP context

# Alerts, packages, organizations
python3 tools/clis/liberty91.py alerts
python3 tools/clis/liberty91.py alert-matches <id>                # Threat Events; --results reports for documents
python3 tools/clis/liberty91.py reports --status DRAFT
python3 tools/clis/liberty91.py report-download <id> --type md --out report.md
python3 tools/clis/liberty91.py orgs
python3 tools/clis/liberty91.py org <org-id> --section suppliers
```

**Canonical entity filters (v2.1).** Six new `query_tree` leaf fields, usable in `search` and in saved searches:

| Leaf | Values | Matches |
|---|---|---|
| `canonical_actor` | UUID[] | threat actor from the deduplicated cross-tenant catalog |
| `canonical_malware` | UUID[] | malware, same catalog |
| `canonical_vulnerability` | UUID[] | vulnerability, same catalog |
| `incident_technique` | `T1566`, `T1566.001` | ATT&CK techniques derived for the **occurrence** |
| `affected_organization` | UUID[] | one of **your own** customer organizations |
| `relevant_to_me` | one of `true`/`false`/`1`/`0`/`yes`/`no` | occurrence intersects any of your organizations' profiles |

**Prefer the canonical leaves.** The legacy leaves (`threat_actor`, `malware`, `vulnerability`, `threat_cluster`) still work and are not being removed, but they match your *account-local* entities while the canonical ones match the deduplicated catalog. Resolve a name with `library threat-actors --name`/`--alias`, then filter on the canonical id.

`technique` and `incident_technique` answer **different questions**, and both are kept: `technique` matches what a single *report* named, `incident_technique` matches the set derived for the *occurrence*, which merges every source and can therefore carry an assertion no individual report made. Tree grammar and caps are unchanged: depth 3, 50 nodes, 50 values per leaf, 3 free-text leaves.

**The caveat that will look like missing data.** An entity filter returns strictly **fewer** results than a free-text search for the same name. A report not yet matched into an occurrence has no canonical links, so no entity filter can reach it, even when its text plainly names the actor. This is correct behaviour, not a gap. When someone asks why filtering APT28 by id returns less than searching the string, that is the answer. For a completeness sweep run the free-text search as well, and say which one the finding came from.

### Write operations — confirm with the user first

```bash
# Push a report in. Private to your account; extracted IOCs are TLP:RED. 10 credits.
python3 tools/clis/liberty91.py ingest --title "Phishing wave against UAE energy" \
  --text-file findings.md --source "Internal CTI" --actor APT34 --vulnerability CVE-2026-1234

# Then poll until enrichment completes, and read threat_event_id for the occurrence it matched
python3 tools/clis/liberty91.py event <event_id>

# Intelligence package — 50 credits PER REPORT generated
python3 tools/clis/liberty91.py report-generate --organization-id <org-id> --intelligence-requirement <ir-id>

# Organization profile (orgs.write)
python3 tools/clis/liberty91.py upload-document <org-id> supplier-list.xlsx --description "2026 vendor register"
python3 tools/clis/liberty91.py confirm-entities <org-id> <doc-id> --id <entity-id> --id <entity-id>
python3 tools/clis/liberty91.py refresh-description supplier <entity-id>
```

Every command accepts `--dry-run` (preview the request, send nothing) and `--insecure` (skip TLS verification — non-production hosts only). Lists accept `--page-size`, `--all`, `--max-pages` and `--cursor`; `next` is an opaque complete URL, never build cursor params. The CLI exits 2 if `LIBERTY91_API_KEY` is unset. Report a missing key; never fabricate results.

**Page size shrank in v2.1, and it costs you.** The server default drops **100 → 25** and the maximum **500 → 100**, on every paginated endpoint. Credits are charged per request and the rate limit is a fixed window per key, so **the same walk now costs up to 4x the credits and 4x the rate-limit budget**. The CLI omits `page_size` unless you pass `--page-size`, so it follows whichever contract the host serves and needs no change. What does need your attention is `--max-pages` (default 10): the same `--all --max-pages 10` that returned up to 5,000 rows returns 250 against a v2.1 host. Check `truncated` before reporting a count as complete, and raise `--max-pages` deliberately rather than assuming the default still covers the set.

## Reading the trust signals

Three separate judgements travel with every occurrence. **Do not collapse them into one number** — and do not re-derive them, they are already Admiralty.

- **Source reliability** (`A`–`F`, per source) — *who said it*. Government sources start at A, vendors at B, news at C, and move on evidence.
- **Credibility** (`1`–`6`, per occurrence, **lower is better**) — *how well-supported the claim is*. 1 Confirmed · 2 Probably True · 3 Possibly True · 4 Doubtful · 5 Improbable · 6 Cannot be judged. Syndicated re-publications collapse to one source, so they cannot inflate it. `null` means unscored, not average.
- **Verification** — *where the occurrence stands*: `auto`, `corroborated`, `verified`, `disputed`, `rejected`, `merged` (see `merged_into`). Analyst judgements are never overwritten by the pipeline.
- **Stance** — a property of each *report*: `claims`, `corroborates`, `updates`, `mentions`, `disputes`. When sources disagree, **say so** — report the dispute, don't average it away.

`--verification corroborated --min-credibility 2` is the triage filter for "actionable now".

## Response format

All commands return JSON on stdout:

```yaml
source: liberty91
operation: threat-events | threat-event | library | entity | search | ioc-lookup | ingest | ...
query_time: <ISO8601>
# lists:
count: <n>
pages_walked: <n>
next: <complete URL or null>
truncated: true            # only when --max-pages stopped the walk
results: [...]
unlinked_report_count: <n> # search and alert-matches only
# ioc-lookup:
found: true|false
results: [...]
# _meta on every successful call:
_meta:
  rate_limit_remaining: <n>
  credits_remaining: <n>
```

Watch `_meta.credits_remaining` and surface it when it gets low. Reads cost 1 credit (2 for detail/search, 5 for STIX and downloads, 10 for IOC export and ingest, 25 for document upload, 50 per generated report). Failed requests are never charged.

## Source reliability (Admiralty default)

Liberty91 emits Admiralty ratings natively — **use the platform's own numbers rather than a default**:

- Occurrence carries per-source `reliability` and an occurrence `credibility` → pass both to `/source-assessment` verbatim
- Occurrence unscored (`credibility: null`) → **B6** — reliability from the source class, credibility cannot be judged
- Nothing else available → **B2** (the frontmatter default)
- A report your own analysts ingested → **A1**; a report you ingested from a third party → rate the original author

When an occurrence rests on a single `D`/`E`-graded publisher, downgrade to that worst contributing source no matter how confident the summary reads.

## Operational notes

- **A bad filter value is a `400`, not an empty page.** If a sector or country filter errors, it is a typo in your query — not absence of data. Read `detail`; it names the field.
- **`404` is also "not in your account".** Tenancy is enforced by returning `404` rather than `403`, so never report a `404` as "deleted" or "does not exist" — say "not visible to this account".
- **Visibility is per-report.** You see an occurrence when you hold at least one of its reports, and `report_count` / `source_count` count only those. Never present them as the total volume of reporting in the world.
- **Your ingested reports are private** and their IOCs are `TLP:RED` — check `/tlp-guide` before including them in anything shared.
- **Flat vs parented STIX.** `ioc-export --format stix` is a context-free indicator list (blocklist). For a TIP, use `--section iocs-export` on an occurrence or entity — it carries the occurrence plus relationships to each indicator.
- **Clusters are account-local**: the `techniques`, `threat-events` and `related` sections return `400` for them. The CLI refuses those combinations locally.
- **Enrichment and generation are asynchronous.** `ingest` returns 202 — poll `event <id>` until `enrichment_status` is `complete`. `report-generate` queues — poll `report <id>` until `status` leaves `GENERATING`.
- **An empty `alert-matches` has historically meant nothing.** Alert rules carrying a **sector** condition have never fired: the rule stored two-letter sector codes while events store display names, and the matcher compared them directly, so the condition was always false. The auto-created rule every new account receives is *country AND sector*, so **that rule has never produced a single alert**. v2.1 fixes the matcher. Until a host is on v2.1, never read "no alert matches" as "no matching activity", and after the upgrade expect a first-activation surge that reflects the backlog rather than a spike in threat activity. No customer needs to reconfigure anything: the rules were always right, the matcher was not.
- **Three scopes now gate the flagship detail call.** `threat-event <id>` needs `threat-events.read` **+** `orgs.read` **+** `events.read` from v2.1, because the detail is a join across three resources: the occurrence, your organizations' relevance, and the reporting behind it. `events.read` is the new one, added because the embedded `sources[]` is the report layer, so withholding it previously bought nothing and only changed which URL the caller used. If you need the occurrence alone, use `threat-events` (the list), which still needs `threat-events.read` by itself.
- **`alerts` needs four scopes from v2.1**: `alerts.read` **+** `orgs.read` **+** `search.read` **+** `threats.read`. The rule's `criteria` block returns suppliers and asset technologies (org resources), the effective `query_tree` (a search resource) and threat clusters (a threat-library resource), so the endpoint now requires the scope of everything it actually returns. A narrowly scoped key that worked before will get a `403` naming what is missing. Also from v2.1, `criteria.query_tree` always reflects what the rule really evaluates: for a rule configured only through the flat criteria fields it returns the tree those compile to, where it previously returned `null`. **Treat `query_tree` as the authoritative statement of what a rule fires on.**
- **The occurrence layer may not be deployed yet.** API v2.0 introduced `/threat-events/`, `/search/` and `/threat-library/` (renaming the pre-2.0 `/threats/`); as of 31 July 2026 the production host still serves the pre-2.0 surface and those return `404`. `quota` reports `occurrence_layer_available: false` when that is the case — fall back to `events` + `iocs` and say plainly that deduplication is unavailable rather than presenting report counts as occurrence counts.
- **v2.1 is documented here but is not live anywhere yet.** Everything marked v2.1 above (25/100 page sizes, entity-bearing list rows, `--section sources`, the canonical search leaves, the widened scopes, the alert-matcher fix) sits on an unmerged branch, not yet on staging, and the production host is still behind even v2.0. Check `/api/v1/schema/` for what a host actually serves before promising any of it to a user. The v1 contract only grows: no field has been renamed or removed, so ignore fields you do not recognise rather than treating them as errors.

## Related skills

- `/ip-investigation`, `/domain-investigation`, `/hash-investigation`, `/url-investigation` — chain `ioc-lookup` for first-party correlation
- `/ioc-enrichment-workflow` — first-party check before third-party enrichment, and the write-back path afterwards
- `/threat-actor-profiling`, `/campaign-tracking` — `library` + `entity --section techniques|threat-events|related` before rebuilding a profile from scratch
- `/vulnerability-intelligence` — `library vulnerabilities` for CVE records with exploitation context
- `/lookup-misp`, `/lookup-opencti` — the other two-way integrations; Liberty91 is the source, MISP the exchange layer, OpenCTI the internal graph
- `/stix-bundle` — the bundle structure `--section stix` produces
- `/source-assessment`, `/confidence-levels`, `/tlp-guide` — consume the platform's native ratings rather than inventing new ones
- `/intelligence-writing`, `/writing-assessments` — turn occurrences into finished products

## See also

- Integration setup: `tools/integrations/liberty91.md`
- Python CLI source: `tools/clis/liberty91.py`
- Interactive API reference: https://api.liberty91.com/api/v1/docs/ (public, no key)
- OpenAPI schema: https://api.liberty91.com/api/v1/schema/ (public — check which surface a host actually serves)
