# Versions

Per-skill semantic version and changelog. Update this file when you ship changes to a skill. Skills follow [semver](https://semver.org/): MAJOR.MINOR.PATCH.

- **MAJOR** — breaking change to skill behavior or required inputs
- **MINOR** — new capability, backward-compatible
- **PATCH** — clarifications, typo fixes, small improvements

Agents should check this file on session start and warn the user if 2+ skills have minor-or-greater updates since last seen.

## Pack version

**cti-skills:** 1.13.0 (2026-08-01)

## Skills

### Analytical techniques
| Skill | Version | Last updated |
|---|---|---|
| `ach` | 1.0.0 | 2026-04-20 |
| `horizon-scanning` | 1.0.0 | 2026-04-20 |
| `key-assumptions-check` | 1.0.0 | 2026-04-20 |
| `red-team-analysis` | 1.0.0 | 2026-04-20 |
| `source-assessment` | 1.0.0 | 2026-04-20 |
| `structured-analytic-techniques` | 1.0.0 | 2026-04-20 |
| `threat-assessment` | 1.0.0 | 2026-04-20 |

### CTI tradecraft
| Skill | Version | Last updated |
|---|---|---|
| `campaign-tracking` | 1.0.0 | 2026-04-20 |
| `control-coverage-mapping` | 1.0.0 | 2026-08-01 |
| `darkweb-collection` | 2.0.0 | 2026-04-28 |
| `indicator-pivoting` | 2.0.0 | 2026-04-28 |
| `malware-analysis` | 1.1.0 | 2026-05-14 |
| `osint-methodology` | 1.0.0 | 2026-04-20 |
| `threat-actor-profiling` | 1.0.0 | 2026-04-20 |
| `vulnerability-intelligence` | 1.0.0 | 2026-04-20 |

### Hyperloop
| Skill | Version | Last updated |
|---|---|---|
| `cti-hyperloop` | 1.0.0 | 2026-04-20 |

### Knowledge cells
Knowledge cells decay faster than other skills — update the `Last updated` column whenever you refresh intel. Agents should warn if a knowledge cell is >90 days stale.

| Skill | Version | Last updated |
|---|---|---|
| `carding-financial-fraud` | 1.0.0 | 2026-04-20 |
| `china-cyber-espionage` | 1.0.0 | 2026-04-20 |
| `dprk-cyber-espionage` | 1.0.0 | 2026-04-20 |
| `hacktivism` | 1.0.0 | 2026-04-20 |
| `infostealers` | 1.0.0 | 2026-04-20 |
| `initial-access-brokers` | 1.0.0 | 2026-04-20 |
| `iran-cyber-espionage` | 1.0.0 | 2026-04-20 |
| `phishing-social-engineering` | 1.0.0 | 2026-04-20 |
| `ransomware-ecosystem` | 1.0.0 | 2026-04-20 |
| `russia-cyber-espionage` | 1.0.0 | 2026-04-20 |
| `supply-chain-threats` | 1.0.0 | 2026-04-20 |

### Management
| Skill | Version | Last updated |
|---|---|---|
| `feedback-loops` | 1.0.0 | 2026-04-20 |
| `intelligence-sharing` | 1.0.0 | 2026-04-20 |
| `maturity-assessment` | 1.0.0 | 2026-04-20 |
| `pir-management` | 1.0.0 | 2026-04-20 |
| `quality-control` | 1.0.0 | 2026-04-20 |
| `sops` | 1.0.0 | 2026-04-20 |
| `stakeholder-management` | 1.0.0 | 2026-04-20 |

### Production
| Skill | Version | Last updated |
|---|---|---|
| `confidence-levels` | 1.0.0 | 2026-04-20 |
| `intelligence-writing` | 1.0.0 | 2026-04-20 |
| `ioc-enrichment-workflow` | 2.1.0 | 2026-05-14 |
| `ioc-export` | 1.0.0 | 2026-04-20 |
| `kql-writing` | 1.0.0 | 2026-04-20 |
| `likelihood-language` | 1.0.0 | 2026-04-20 |
| `sigma-writing` | 1.0.0 | 2026-04-20 |
| `stix-bundle` | 1.0.0 | 2026-04-20 |
| `tlp-guide` | 1.0.0 | 2026-04-20 |
| `writing-assessments` | 1.0.0 | 2026-04-20 |
| `yara-writing` | 1.1.0 | 2026-05-14 |

### Orchestrator + investigation skills (new in Phase C)
| Skill | Version | Last updated |
|---|---|---|
| `cti-orchestrator` | 1.0.0 | 2026-04-20 |
| `ip-investigation` | 1.1.0 | 2026-05-14 |
| `domain-investigation` | 1.2.0 | 2026-05-14 |
| `hash-investigation` | 1.1.0 | 2026-05-14 |
| `url-investigation` | 1.1.0 | 2026-05-14 |

### Lookup skills (external API wrappers)
| Skill | Version | Last updated |
|---|---|---|
| `lookup-liberty91` | 1.1.0 | 2026-07-31 |
| `lookup-abuseipdb` | 1.0.0 | 2026-04-20 |
| `lookup-censys` | 1.0.0 | 2026-04-20 |
| `lookup-greynoise` | 1.0.0 | 2026-04-20 |
| `lookup-otx` | 1.0.0 | 2026-04-20 |
| `lookup-shodan` | 1.0.0 | 2026-04-20 |
| `lookup-misp` | 1.0.0 | 2026-04-26 |
| `lookup-opencti` | 1.0.0 | 2026-07-02 |
| `lookup-ransomwarelive` | 1.0.0 | 2026-04-26 |
| `lookup-reversinglabs` | 1.0.0 | 2026-05-08 |
| `lookup-crowdstrike` | 1.0.0 | 2026-05-30 |
| `lookup-urlscan` | 1.0.0 | 2026-04-20 |
| `lookup-virustotal` | 1.0.0 | 2026-04-20 |
| `mitre-attack` | 1.0.0 | 2026-04-20 |

### Legacy tool-API reference skills (superseded by `lookup-*` in Phase B)
These remain for reference but agents should prefer the `lookup-*` skills above. Will be removed in a future cleanup.

| Skill | Version | Last updated | Status |
|---|---|---|---|
| `abuseipdb-api` | 1.0.0 | 2026-04-20 | superseded by `lookup-abuseipdb` |
| `censys-api` | 1.0.0 | 2026-04-20 | superseded by `lookup-censys` |
| `greynoise-api` | 1.0.0 | 2026-04-20 | superseded by `lookup-greynoise` |
| `otx-api` | 1.0.0 | 2026-04-20 | superseded by `lookup-otx` |
| `reversinglabs-api` | 1.0.0 | 2026-05-08 | reference companion to `lookup-reversinglabs` |
| `crowdstrike-api` | 1.0.0 | 2026-05-30 | reference companion to `lookup-crowdstrike` |
| `shodan-api` | 1.0.0 | 2026-04-20 | superseded by `lookup-shodan` |
| `urlscan-api` | 1.0.0 | 2026-04-20 | superseded by `lookup-urlscan` |
| `virustotal-api` | 1.0.0 | 2026-04-20 | superseded by `lookup-virustotal` |

## Changelog

### 1.13.0 — 2026-08-01
- **New skill `control-coverage-mapping` (1.0.0)** — joins a control baseline to ATT&CK techniques against a bundled evidence base of 9,545 control-to-technique rows from six public sources (ATT&CK v19.1 native mitigations; CTID Mappings Explorer for NIST 800-53 rev5, AWS, Azure, GCP, M365). Supplies the **Resistance Strength** node of FAIR Vulnerability, pairing with `/lookup-liberty91` for Threat Capability. Ships `tools/clis/map_controls.py` (stdlib only, no API key) and `data/attack-control-mapping/` (JSON export so nothing needs Excel, plus the source workbook and METHODOLOGY for provenance).
- **Four CLI modes.** Beyond coverage (`--controls`) and recommend (omit it), two modes answer the question NIST cannot: `--mitigations` returns ATT&CK M-codes with MITRE's own published definitions, and `--telemetry` resolves "monitoring" into named log sources and detection logic down to channel level (`WinEventLog:Sysmon EventCode=1`, `auditd:SYSCALL execve`, `Security 4688`). Driven by a real limitation: **the NIST half of the workbook carries a control id and a name and nothing else**, so `SI-04 System Monitoring` stands in for 52 techniques with no text to expand it from. Both new modes read pre-extracted files (`attack_mitigations.json`, `attack_telemetry.json`, ~1 MB) rather than the 45 MB ATT&CK bundle, which is gitignored and absent on a fresh clone; regenerate with `data/attack-control-mapping/build_attack_extract.py`.
- **Distinctive vs baseline, so the output reads like an analyst brief.** A breadth ranking surfaces basic hygiene every time for any input, because that is what breadth measures: `M1018 User Account Management` covers 20% of all ATT&CK techniques and `SI-04 System Monitoring` most of the NIST-mapped universe, so they top every list and say nothing about the threat just analysed. Both `--mitigations` and recommend mode now split on **lift** (share of *your* techniques covered over share of *all* techniques covered): ~1.0 is baseline hygiene, >=1.5 is distinctive. On the US-financial run this moved `SI-04` to baseline at 1.26x and surfaced `M1013 Application Developer Guidance` and `M1033 Limit Software Installation` at 2.6x, which are precisely the npm supply-chain compromises in that data and were previously buried. `--min-support` (default 3) holds thin controls in a `low_support` bucket so a 1-of-2 control cannot claim 20x, `--lift-threshold` tunes the cut, and a technique set too small to rank says so in the summary rather than returning an empty-looking result. Documented with the warning that distinctive does not mean more important.
- **Recommend mode splits its output by evidence type.** Only the four CTID cloud stacks carry effectiveness scores, so ranking on strength alone returned nothing but vendor products (zero NIST controls in the top 60) and read as a product pitch. Scored capabilities and control classes are now ranked and presented separately, with the second labelled "controls nobody has scored" rather than implied to be weaker.
- **Four output buckets, not three.** Beyond the usual significant / weak / gap lists, techniques that **no** source maps a control to are held separately, including those whose only mapping is ATT&CK's `M1056 Pre-compromise` placeholder. Merging them into the gap list pads it with items no control programme could close; on real data this moved 6 of 39 techniques out of "gap".
- **Correctness traps handled in the CLI, each found empirically**: five revoked ATT&CK IDs (`T1081`, `T1192`, `T1188`, `T1488`, `T1022`) remapped to MITRE successors so a stale identifier does not read as a security gap; the technique universe is built from `Master_Mapping` rather than `Technique_Summary`, because the two sheets disagree on 18 IDs including the entire `T1562` Impair Defenses family (40 mapped rows would otherwise be reported as unmapped).
- **Mapping boundaries documented rather than papered over**: CTID's 800-53 mapping contains **no PL, AT or IR family**, so policy, awareness and incident-response controls score zero regardless of quality; its M365 sheet has **no Defender for Endpoint**, so EDR cannot be scored from that source. Controls that do not map cleanly get their own reported section instead of being forced to the nearest identifier.
- **`scripts/setup.sh` interactive mode fixed.** `read_secret` tested `[ -t 1 ]`, but it is always called inside `$( )`, where stdout is a pipe, so the condition was **never true in a real terminal**: no prompt was ever printed and the script appeared to hang. Now tests stdin only and writes the prompt to stderr, which command substitution does not capture. Verified under a real pty.
- Setup also: URLs, usernames and client ids now echo while typing (`plain` vs `secret` per service) so typos are visible; `--verify` reports Censys instead of silently printing nothing; and `--verify` honours the `MISP_KEY` alias that `misp.py` already accepted, so a working MISP setup no longer reports as "not configured". `read` failures are tolerated so `set -e` cannot abort the run at the first skipped service.
- **`.env.example` completed**: added `TELEGRAM_API_ID`/`_API_HASH`/`_PHONE`/`_SESSION` and `INTELX_API_KEY` (used by `/darkweb-collection` but previously undocumented), `MISP_PROXY`, `LIBERTY91_PROXY`, and a note that `MISP_API_KEY` is canonical with `MISP_KEY` accepted as an alias. All 30 values verified empty. README's Censys row corrected to `CENSYS_PAT`, which is what the CLI actually reads.
- README gains a **What's new** section with plain-language write-ups of the Liberty91 integration and the control mapping, and `/control-coverage-mapping` is listed under Analysis.

### 1.12.0 — 2026-07-31
- `lookup-liberty91` → **1.1.0**. Documents the Liberty91 API **v2.1** contract, from the upstream documentation brief for branch `feature/search-canonical-alignment` (verified against the branch head's served schema, 2026-07-31). **None of it is live**: the branch is unmerged, not on staging, and production still serves the pre-2.0 surface. Every v2.1 item is tagged as such in the skill and the integration doc, with the instruction to check `/api/v1/schema/` before relying on it.
- **BREAKING, pagination** — default page size 100 → **25**, max 500 → **100**, on *every* paginated endpoint. Because credits are charged per request and the rate limit is a fixed window per key, the same walk costs up to **4x** the credits and rate-limit budget. The CLI omits `page_size` unless `--page-size` is passed, so it inherits the host's default and needs no change; the documented trap is `--max-pages` (default 10), where the same `--all` walk drops from ~5,000 rows to 250. Skill and integration doc both tell the agent to check `truncated` before calling a count complete.
- **BREAKING, scopes** — `GET /threat-events/{id}/` now also needs `events.read` (three scopes total: it is a join across the occurrence, org relevance, and the reporting behind it); `GET /alerts/` now also needs `orgs.read` + `search.read` + `threats.read` (its `criteria` block returns suppliers, asset technologies, the effective `query_tree` and threat clusters). Recorded with the upstream production audit finding that **zero** issued keys currently carry `alerts.read`, so the alerts tightening breaks nothing today.
- **New CLI section** — `threat-event <id> --section sources` → `GET /threat-events/{id}/sources/`, the paginated full report list behind an occurrence. Implemented as a paginating branch (the only section that pages), so `threat-event` gained `--page-size`/`--cursor`/`--all`/`--max-pages`. Documented against the detail's embedded `sources[]`, which is **capped** and therefore a sample, not the record.
- **Threat Event list rows gained six fields** — `actors`, `malware`, `vulnerabilities` (canonical `{id, name, from_private_source}`), `techniques`, `victims`, `source_countries`. Because the canonical id is on the row, a list result now feeds `entity <type> <id>` with no detail call in between, which matters more with quarter-size pages. Two semantics documented rather than left to discovery: list rows show **publicly-linked entities only** (an entity named only in a private report shows on detail but not on the row, so absence from a row is not absence from the occurrence), and `source_countries` counts only publicly-sourced, non-disputing reports. `search` and `alert-matches` still return the **base** shape and did not gain these.
- **Six new canonical `query_tree` leaves** — `canonical_actor`, `canonical_malware`, `canonical_vulnerability`, `incident_technique`, `affected_organization`, `relevant_to_me`. Legacy leaves are kept (they match account-local entities; the canonical ones match the deduplicated catalog) with the canonical ones documented as the default choice. `technique` vs `incident_technique` is called out as two different questions: what one *report* named, vs the set derived for the *occurrence*. Carries the support-ticket caveat prominently: **an entity filter returns strictly fewer results than free-text for the same name**, because an unmatched report has no canonical links — correct behaviour that reads as missing data.
- **Alert `query_tree` is writable** on create/update, with precedence linked saved search → own `query_tree` → flat criteria fields, malformed trees rejected at write time, and `criteria.query_tree` now always returning what the rule actually evaluates instead of `null` for flat-criteria rules.
- **Operational caveat with teeth** — alert rules carrying a **sector** condition have *never fired* (rules store two-letter sector codes, events store display names, the matcher compared them directly), and since the auto-created rule every account receives is *country AND sector*, that rule has never produced an alert. The skill now instructs agents never to read an empty `alert-matches` as "no matching activity" on a pre-v2.1 host, and to expect a backlog-driven surge on first activation rather than reporting it as a spike in threat activity.

### 1.11.0 — 2026-07-30
- Added `lookup-liberty91` — the pack's **first-party** integration, wrapping the Liberty91 platform API v1 (documentation v2.0, 29 July 2026). The third write-capable lookup, after `lookup-misp` and `lookup-opencti`. Its distinguishing feature is the **two-layer model**: a *Threat Event* is a deduplicated real-world occurrence carrying every source you are entitled to, while an *Event* is one report about it — five write-ups of one breach are five Events and one Threat Event. Skill and CLI default to the occurrence layer.
- **Read surface** — `quota` (connectivity + `X-RateLimit-*`/`X-Credits-*`, and which API surface the host serves); `threat-events` (17 filters: relevance, verification stage, credibility floor, taxonomy class/type, ATT&CK technique, target/source country, sector, source count, organization, intelligence requirement, occurrence and reporting date windows); `threat-event --section detail|iocs|stix|iocs-export`; `library <threat-actors|malware|vulnerabilities|clusters>` with `--name`/`--alias` name resolution; `entity --section detail|iocs|related|techniques|threat-events|stix|iocs-export`; `search` (flat criteria or a `query_tree`) plus `saved-searches`/`run-search`; `events`/`event`; `ioc-lookup`/`iocs`/`ioc-export`; `reports`/`report`/`report-download`; `alerts`/`alert-matches`; `orgs`/`org`/`org-document`.
- **Write surface** (all require user confirmation — they publish into the account and are metered) — `ingest` a report (enriched, entity- and IOC-extracted, matched into a Threat Event, private to your account, extracted IOCs `TLP:RED`); `report-generate` (50 credits per report); `upload-document`, `confirm-entities`, `refresh-description` for organization profiles.
- Stdlib-only Python CLI at `tools/clis/liberty91.py`. Reads `$LIBERTY91_API_KEY` (+ optional `$LIBERTY91_API_URL`, `$LIBERTY91_PROXY`). Cursor pagination follows the server's `next` URL, capped by `--max-pages` (default 10) so an `--all` walk cannot quietly drain the credit pool — a capped walk reports `truncated: true` plus the resume cursor. Every response echoes rate-limit and credit headers in `_meta`; a `429` is disambiguated into rate-limit vs. exhausted credits from `X-Credits-Remaining`; `403` reports the missing scope; `404` is documented as "not found **or** not in your account", since tenancy is enforced by 404 rather than 403.
- **Admiralty handling is different from every other lookup**: Liberty91 emits ratings natively (per-source reliability `A`–`F`, per-occurrence credibility `1`–`6`, plus a verification stage and per-report stance). The skill instructs agents to pass those through verbatim rather than re-deriving them; the frontmatter `B2` is only the fallback, with `B6` for unscored occurrences.
- **Wiring** — `/lookup-liberty91` added to the `/cti-orchestrator` lookup catalog, the parallel batch of all four investigation skills (`ip`/`domain`/`hash`/`url-investigation`), all five `ioc-enrichment-workflow` routing tables (as order 0 — first-party before third-party quota) plus its credibility, rate-limit and push-back sections, `indicator-pivoting` (routing-by-goal table), `malware-analysis` (canonical family record + dated ATT&CK), `threat-actor-profiling` (canonical actor resolution by name or vendor alias), `campaign-tracking` (timeline seeding from occurrences + publish path), and `vulnerability-intelligence` (exploitation-in-the-wild evidence: an occurrence classed `security-incident` rather than `vulnerability` means a named victim was hit).
- Registry (catalog row + Python CLI table), `scripts/setup.sh` (env vars, `--liberty91`/`--liberty91-url` flags, dry-run verify case), `cti-setup` services table, `.env.example`, and README (lookup list + key table) updated.
- **Deployment note** — validated live against `https://api.liberty91.com` with an `l91_test_` key: auth, quota headers, `ioc-lookup`, `events` and pagination all work. The v2.0 occurrence layer (`/threat-events/`, `/search/`, `/searches/`, `/threat-library/`) is **not yet deployed** on that host and returns `404`, while the pre-2.0 `/threats/` path is still live. The CLI targets the documented v2.0 contract and needs no change when it ships; until then `quota` reports `occurrence_layer_available: false` and the skill instructs agents to fall back to `events` + `iocs` and to say plainly that deduplication is unavailable rather than passing report counts off as occurrence counts.

### 1.10.0 — 2026-07-02
- Added `lookup-opencti` skill — the second write-capable lookup in the pack (after `lookup-misp`) and the first GraphQL integration. Two-way bridge to an OpenCTI instance: **read** (`version` connectivity check, `lookup` — observables AND indicators for a raw IOC value in one call, global `search` across all entity types, filtered `list` of 10 entity types with FilterGroup filters + cursor pagination, `get` with relationship fan-out, `connectors` health) and **write** (`create-indicator` with auto-generated STIX pattern + companion observable, `create-observable`, `add-label` with auto-create label resolution, `add-marking` for TLP, `update` fieldPatch, `create-relationship`, `upload-stix` for STIX 2.1 bundle import with bypassValidation/analyst-workbench semantics, and a guarded `delete`). Stdlib-only Python CLI at `tools/clis/opencti.py` targeting OpenCTI ≥ 6.x. Reads `$OPENCTI_URL` + `$OPENCTI_TOKEN` (+ optional `$OPENCTI_PROXY`). Self-signed-cert support via `--insecure`; every command supports `--dry-run`. Source reliability defaults to B2, rated per the entity's `createdBy` feed/author.
- **Wiring** — `/lookup-opencti` added to the `/cti-orchestrator` lookup catalog, the credentials-conditional parallel batch of all four investigation skills (`ip`/`domain`/`hash`/`url-investigation`), all five `ioc-enrichment-workflow` routing tables (+ enrichment-record block, rate-limit table, and push-back step alongside MISP), `indicator-pivoting` (hash tree, actor tree, routing-by-goal table), `malware-analysis` (internal correlation), `threat-actor-profiling` (internal knowledge-base check before rebuilding a profile), `campaign-tracking` (publish path), and `stix-bundle` (OpenCTI imports bundles as-is — no MISP-style TLP marking surgery). Auditor `EXTRA_COVERAGE` now enforces the composite references.
- Registry (catalog row + Python CLI table), `scripts/setup.sh` (env vars, `--opencti-url`/`--opencti` flags, dry-run verify case), `cti-setup` services table, `.env.example`, README (catalog + key table), and CREDITS updated. README/CLAUDE.md stale skill counts corrected to 72.
- Validated live against an OpenCTI 7.x instance (7.260701.0). Two bugs the live run surfaced are fixed: `get`'s relationship query typed the `fromOrToId` variable as `StixRef` where the 7.x schema wants `String` (and the failure sank the whole command — it now degrades to entity-without-relationships with a `relationships_note`); and `get`'s field selection lacked `Identity`/`Location`/`Tool` fragments, so targeted sectors, countries, and tools resolved without names.
- Added `lookup-crowdstrike` skill wrapping the CrowdStrike Falcon Intelligence (Intel) API. Unlike the IOC-reputation lookups, it spans two use cases: (a) **indicator** reputation for IP/domain/hash/URL (malicious confidence, linked actors + malware families, report refs), and (b) **finished/actor intelligence** — `actor` (adversary profile: origins, target countries/industries, motivations, capability, aliases), `actors` (search by origin/target/motivation via FQL), `reports` (finished reporting by actor / free-text / latest, plus PDF download), and `ttps` (MITRE ATT&CK technique set for an actor). Plus `indicators` — browse/sweep the indicator feed for the latest malicious IOCs, filterable by confidence/type/actor/malware/recency (newest-first). SDK-backed Python CLI at `tools/clis/crowdstrike.py` with self-bootstrapping venv around `crowdstrike-falconpy`. Reads `$CROWDSTRIKE_CLIENT_ID` + `$CROWDSTRIKE_CLIENT_SECRET` (+ optional `$CROWDSTRIKE_BASE_URL` for non-US-1 clouds); FalconPy handles the OAuth2 client-credentials token exchange. Source reliability defaults to A2 with B3 downgrade rules for low/unverified indicators and sparse actor records. Added companion `crowdstrike-api` reference skill (non-invokable) holding the full Intel operation catalogue and FQL primer.
- **IOC-path wiring** — `/lookup-crowdstrike indicator` added to `/cti-orchestrator` lookup catalog (A2, "use when configured"), the always-parallel batch of all four investigation skills (`ip`/`domain`/`hash`/`url-investigation`), all four `ioc-enrichment-workflow` routing tables, and `malware-analysis` (vendor actor attribution + ATT&CK).
- **Actor-path wiring** — added `actor`/`ttps`/`reports` references to `threat-actor-profiling` (primary vendor feed for state-sponsored actors) and a "Live enrichment" section to each regional espionage cell (`iran`/`russia`/`china`/`dprk-cyber-espionage`) with region-appropriate actor examples, so questions like "what TTPs does Charming Kitten use?", "which actors operate from Russia?", and "latest report on Mustang Panda" auto-include a CrowdStrike response when credentials are configured.
- Registry, `scripts/setup.sh` (env vars + flags + dry-run verify case), and `cti-setup` services table updated for the new credentials. No Node CLI — CrowdStrike has no upstream Node SDK and auth requires the OAuth2 exchange the FalconPy SDK handles.

### 1.8.0 — 2026-05-14
- Promoted `/lookup-reversinglabs` from "Optionally add — ONLY when you have ReversingLabs" to "**Add to the same parallel batch if credentials are configured**" across the four investigation skills (`ip-investigation` 1.1.0, `domain-investigation` 1.2.0, `hash-investigation` 1.1.0, `url-investigation` 1.1.0). Prior phrasing biased agents toward skipping RL even when credentials were available; the new framing makes RL the default-when-configured peer of VT/OTX in the always-parallel block. Heavy / fan-out operations (RL `ip --pivot`, RL `submit-url`, RL `report --detailed`) stay in a separate escalation block.
- `malware-analysis` 1.1.0 — first-class integration with `/lookup-reversinglabs report --detailed` for MITRE ATT&CK auto-mapping, TitaniumCore static analysis, sandbox results, and `networkthreatintelligence` C2 extraction. Added a "Tooling for the sections above" callout pointing the reader at the RL report as the single richest pre-fill source for the static/dynamic/MITRE/IOC sections of the analysis output template. RL added to the "Related skills" section alongside VT relationships.
- `ioc-enrichment-workflow` 2.1.0 — added `/lookup-reversinglabs` to the header invokes line, to all four routing tables (IP, domain, URL, hash), to the rate-limit awareness table (429 + Retry-After, no public per-minute quota), and to the related-skills index. For hashes RL sits at position 2 right after VT as the strongest single-source verdict; for IP/domain/URL it's marked "**Run when configured**" so the reader doesn't treat it as last-resort.
- `yara-writing` 1.1.0 — added "Validation against a real corpus" section pointing at `/lookup-reversinglabs yara-matches` (operational telemetry from deployed rules), `search 'threatname:<family>'` (sample collection for test suites), and `containers`/`extracted` (parent-child rule coverage). Added a "Related skills" section.
- **Driver:** an agent running `/hash-investigation` on a WannaCry SHA-256 ran VT + OTX from the always-parallel block and skipped RL even with credentials configured, because the procedure buried RL under "ONLY when you have…" language. The fix is doctrinal, not API-level: when RL credentials are present, RL is part of the default lookup batch — not an escalation.

### 1.7.0 — 2026-05-08
- Added `lookup-reversinglabs` skill wrapping the ReversingLabs Spectra Analyze (A1000) API. Covers hash classification, detailed reports (incl. MITRE ATT&CK mapping, TitaniumCore static analysis, sandbox results), file/URL submission with optional polling, network threat intelligence for URLs/domains/IPs, advanced search for pivoting by threatname/AV-signature/family, parent-container and extracted-file relationships, and read-only YARA-ruleset matches. SDK-backed Python CLI at `tools/clis/reversinglabs.py` with self-bootstrapping venv. Reads `$REVERSINGLABS_USER` + `$REVERSINGLABS_PASSWORD` (+ optional `$REVERSINGLABS_HOST`); SDK auto-exchanges credentials for a token via `/api-token-auth/`. Source reliability defaults to A2 with B3 downgrade rules for `unknown`/`suspicious` verdicts and very fresh samples. Added companion `reversinglabs-api` reference skill (non-invokable). Cross-referenced from `/ip-investigation`, `/domain-investigation`, `/hash-investigation`, `/url-investigation`, and `/indicator-pivoting`. No Node CLI — RL has no upstream Node SDK and auth requires the token exchange.

### 1.6.0 — 2026-04-29
- Backfilled trigger phrases in 34 user-invocable skill descriptions that pre-dated the [`CONTRIBUTING.md`](CONTRIBUTING.md) line-44 convention. Affected: `campaign-tracking`, `carding-financial-fraud`, `china-cyber-espionage`, `confidence-levels`, `cti-hyperloop`, `dprk-cyber-espionage`, `hacktivism`, `horizon-scanning`, `infostealers`, `initial-access-brokers`, `intelligence-sharing`, `intelligence-writing`, `iran-cyber-espionage`, `key-assumptions-check`, `kql-writing`, `likelihood-language`, `malware-analysis`, `maturity-assessment`, `phishing-social-engineering`, `pir-management`, `ransomware-ecosystem`, `red-team-analysis`, `russia-cyber-espionage`, `sigma-writing`, `sops`, `source-assessment`, `stakeholder-management`, `structured-analytic-techniques`, `supply-chain-threats`, `threat-actor-profiling`, `tlp-guide`, `vulnerability-intelligence`, `writing-assessments`, `yara-writing`. Each description now starts with "Use when…" or contains "when the user…" so an orchestrator can match user intent against the frontmatter. No version bump per skill (description-only edit), but adds an 11th check to the auditor — `description-trigger` — that warns on user-invocable skills missing a trigger phrase. Skips `user-invocable: false` (library / pipeline skills loaded by other skills, not surfaced to user routing). Auditor reports 0 FAIL / 0 WARN at end of release.

### 1.5.0 — 2026-04-28
- Added `tools/audit-integrations.py` — stdlib auditor that parses `tools/REGISTRY.md` as the source of truth and runs ten checks across the codebase (registry/disk consistency, integration-guide presence, CLI presence, `VERSIONS.md` coverage, dead `*-agent` references, unknown `/lookup-*` references, `cti-setup` env-var coverage, `scripts/setup.sh` env-var coverage, composite-skill cross-reference coverage, and "the N services" cardinality drift). Wired into `validate-skills.sh` as a non-fatal step. Documented the add/update/remove integration workflow in `CONTRIBUTING.md`. Sweep-cleanup driven by the auditor in this same release: `ioc-enrichment-workflow` 2.0.0 (18 retired `*-agent` references replaced with `/lookup-*` skill names; expanded routing tables; added `lookup-misp` and `lookup-ransomwarelive` correlation steps); `ip-investigation` / `domain-investigation` / `hash-investigation` / `url-investigation` now cross-reference `/lookup-misp` for internal-correlation; `osint-methodology`, `campaign-tracking`, `vulnerability-intelligence`, `threat-actor-profiling`, and `malware-analysis` gained "Related skills" sections that route into the current `/lookup-*` set, `/indicator-pivoting`, and `/darkweb-collection`. Auditor reports 0 FAIL / 0 WARN at end of release.

### 1.4.0 — 2026-04-28
- `indicator-pivoting` 2.0.0 — overhauled to use the current `/lookup-*` skills (the prior version routed to the retired `*-agent` agents) and to include concrete CLI invocations per pivot type. Added decision trees + commands for four new starting indicator types: URL, TLS certificate (SHA-256/CN), registrant email/org, and actor/family/campaign label. Added a Telegram-handle / .onion starting point that hands off to `/darkweb-collection`. New "Pivot routing — by goal" table maps every common pivot to its first-/second-choice lookup. Added a five-hop worked example (phish URL → APT cluster) with real CLI commands and per-hop confidence scoring. Refreshed pivot-quality table (added JARM, JA3, MITRE-technique-overlap caveats) and pivot-documentation template. MAJOR bump because the routing table and frontmatter description changed in ways that prior callers should re-read.

### 1.3.0 — 2026-04-28
- `darkweb-collection` 2.0.0 — substantial expansion. Restructured into `SKILL.md` + `references/` + `scripts/` (first skill in the pack to use the subdir layout). New material: 37 sourced underground forums across 8 categories (`references/forums.md`), 34 sourced Telegram channels across 6 categories (`references/telegram-channels.md`), vendor-first access matrix covering 13 commercial CTI vendors plus a DIY Tails/Whonix/Tor/Telethon playbook (`references/access-methods.md`), handler-side OPSEC primer including persona separation, stylometry, mental-health framing, and explicit out-of-scope statement for CSAM/terrorism/violent-extremist content (`references/opsec.md`), and passive-monitoring strategy with selector taxonomy + cadence table + storage schema (`references/passive-monitoring.md`). Three new stdlib-only Python CLIs under `scripts/`: `onion_search.py` (clearnet search of Ahmia + dark.fail + IntelligenceX onion indexers), `telegram_monitor.py` (read-only Telethon channel monitor; light dep), `keyword_match.py` (local regex/keyword scanner over collected JSONL). Reads `INTELX_API_KEY` (optional, freemium) and `TELEGRAM_API_ID`/`TELEGRAM_API_HASH`/`TELEGRAM_SESSION` (for Telegram monitor). MAJOR bump because the skill's frontmatter description, file layout, and recommended posture all changed; prior callers relying on the v1 single-file shape need to re-read.

### 1.2.0 — 2026-04-26
- `domain-investigation` 1.1.0 — chains `/lookup-ransomwarelive search` against an org-candidate derived from the domain's apex, surfaces `ransomware_status` in the consolidated output, and adds a "Ransomware-claim hits" handling section covering name-collision risk and the metadata-vs-description credibility split.
- Added `lookup-ransomwarelive` skill wrapping ransomware.live's PRO API. Covers victim search/recent/detail (27k+ leak-site claims across 330+ groups), group listings + rich `group-profile` (description, TTPs, tools, leak-site `.onion` infra, vulnerabilities), per-group IOC dumps, YARA rules with full content, ransom-note samples, negotiation chats, press archive, sector reference, and country CSIRT contacts. Stdlib-only Python CLI at `tools/clis/ransomwarelive.py`. Reads `$RANSOMWARE_LIVE`. Source reliability defaults to B2 with credibility nuance: metadata is B2, criminal-written `description` field is B3–B4 (often inflated). Total skill count: 67 (66 active + `stix-bundle` reference).

### 1.1.0 — 2026-04-26
- Added `lookup-misp` skill with two-way MISP integration (the first write-capable lookup skill in the pack). Covers query (`search-events`, `search-attributes`, `search-objects`, `get-event`, `list-tags`) and write (`add-attribute`, `create-event`, `upload-stix`, `tag-event`, `publish-event`). Supports STIX 2 round-tripping — `upload-stix` consumes bundles produced by `/stix-bundle`, and `search-events --returnFormat stix2` exports MISP events as STIX. Stdlib-only Python CLI at `tools/clis/misp.py`. Reads `$MISP_URL` and `$MISP_API_KEY`. Self-signed-cert support via `--insecure`. Total skill count: 65 active + 1 reference (`stix-bundle`).

### 1.0.0 — 2026-04-20
- Initial versioned release
- 52 skills across analytical techniques, CTI tradecraft, knowledge cells, production, management, and tool APIs
- Phase B: 7 new `lookup-*` skills wrap each external threat-intel API (VirusTotal, OTX, URLScan, Shodan, AbuseIPDB, GreyNoise, Censys). Paired with zero-dep Node CLIs under `tools/clis/` and integration docs under `tools/integrations/`. The 7 legacy tool-API agents (`.claude/agents/*-agent.md`) moved to `archive/agents/`.
- Phase C: new `cti-orchestrator` skill as the default entry point. Four investigation skills (`ip-investigation`, `domain-investigation`, `hash-investigation`, `url-investigation`) compose lookups, auto-apply rigor pipeline (source-assessment, tlp-guide, confidence-levels, likelihood-language), and prioritize follow-up IOCs. All 64 skills flattened from `.claude/skills/<category>/<name>/` to top-level `skills/<name>/` (Agent Skills spec layout). Old `cti-orchestrator` agent archived; 6 remaining agents (analyst, report-writer, quality-reviewer, osint-researcher, ioc-processor, detection-engineer) kept in `.claude/agents/` as optional Claude-Code-specific specialist subagents.
- Phase D (partial): added `package.json` + `bin/cti-skills.js` so `npx github:Liberty91LTD/cti-skills` installs the pack into any directory. Subcommands: `install` (default), `add <skill>`, `list`, `update`, `help`. Accepts `--target <dir>`.
- Repo transferred from `renzejongman/cti-agentic-skills` to `Liberty91LTD/cti-skills`
- Added MIT LICENSE, plugin manifest, skill validator, cross-agent AGENTS.md
