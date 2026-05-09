---
name: reversinglabs-api
description: ReversingLabs Spectra Analyze (A1000) API reference. File hash classification, detailed reports, dynamic analysis, network indicator reputation, advanced search, YARA, container relationships.
user-invocable: false
metadata:
  version: 1.0.0
---

# ReversingLabs Spectra Analyze (A1000) API

This is reference documentation. The agent-invokable lookup skill is `/lookup-reversinglabs`; the runtime CLI is `tools/clis/reversinglabs.py`. Read this file when the lookup skill's options are not enough and you need to know which raw endpoint to hit, what fields a response carries, or how to construct a query the SDK does not expose directly.

## Base URL

Default: `https://a1000.reversinglabs.com`. Override with `REVERSINGLABS_HOST` for on-prem or alternate-tenant appliances. The path prefix is `/api/`.

## Authentication

Token-based. Two paths:

1. **Username + password** (configured pattern): `POST /api-token-auth/` with form-encoded `username` and `password`. The endpoint returns `{"token": "<value>"}`. The SDK does this automatically at `A1000(...)` init when given `username=` and `password=`.
2. **Token directly**: pass `token=` to the SDK or set the header manually.

All subsequent requests carry: `Authorization: Token <token_value>` (note: `Token`, not `Bearer`, not `Basic`).

```bash
# Manual token exchange
TOKEN=$(curl -s -X POST "https://a1000.reversinglabs.com/api-token-auth/" \
  -d "username=$REVERSINGLABS_USER&password=$REVERSINGLABS_PASSWORD" | jq -r .token)

# Subsequent call
curl -s "https://a1000.reversinglabs.com/api/samples/v3/<hash>/classification/" \
  -H "Authorization: Token $TOKEN"
```

If the env vars are unset, inform the user to run `/cti-setup` or `./scripts/setup.sh`.

## Rate limits

No per-minute/day quota is publicly documented for A1000. The API returns **HTTP 429** with a `Retry-After: <seconds>` header when limits are exceeded. The SDK polls submission endpoints at 2-second intervals for up to 10 retries before raising.

## Capability map

| Group | Notable endpoint(s) | SDK methods |
|---|---|---|
| Tokens | `POST /api-token-auth/` | (init flow) |
| Submission | `POST /api/uploads/` | `submit_file_from_path`, `submit_file_from_handle`, `submit_url`, `submit_file_and_get_*`, `submit_url_and_get_report` |
| Processing status | `GET /api/samples/status/` | `file_analysis_status`, `check_submitted_url_status` |
| Reports | `POST /api/samples/v2/list/`, `POST /api/samples/v2/list/details/` | `get_summary_report_v2`, `get_detailed_report_v2`, `get_titanium_core_report_v2`, `get_submitted_url_report` |
| Dynamic analysis | `POST/GET /api/rl_dynamic_analysis/...` | `create_dynamic_analysis_report`, `check_dynamic_analysis_report_status`, `download_dynamic_analysis_report` |
| PDF reports | `POST/GET /api/pdf_report/...` | `create_pdf_report`, `check_pdf_report_creation`, `download_pdf_report` |
| Classification | `GET /api/samples/v3/<hash>/classification/` | `get_classification_v3`, `set_classification`, `delete_classification` |
| Reanalysis | `POST /api/samples/v2/reanalyze_bulk/` | `reanalyze_samples_v2` |
| Extracted files | `GET /api/samples/v2/<hash>/extracted-files/` | `list_extracted_files_v2`, `list_extracted_files_v2_aggregated`, `download_extracted_files` |
| Sample admin | `GET /api/samples/<hash>/download/`, `DELETE /api/samples/v2/delete/` | `download_sample`, `delete_samples`, `check_sample_removal_status_v2` |
| User tags | `GET/POST/DELETE /api/tag/<hash>/` | `get_user_tags`, `post_user_tags`, `delete_user_tags` |
| YARA rulesets | `/api/yara/v2/...` | `get_yara_rulesets_on_the_appliance_v2`, `get_yara_ruleset_contents`, `get_yara_ruleset_matches_v2`, `create_or_update_yara_ruleset`, `delete_yara_ruleset`, `enable_or_disable_yara_ruleset` |
| YARA retro-hunt | `/api/yara/retro/...` | `start_or_stop_yara_local_retro_scan`, `get_yara_local_retro_scan_status`, `start_or_stop_yara_cloud_retro_scan`, `get_yara_cloud_retro_scan_status` |
| YARA repo (GitHub sources) | `/api/yara/repositories/...` | `get_yara_repositories`, `create_yara_repository`, `update_yara_repository`, `delete_yara_repository` |
| Advanced search | `POST /api/samples/v2/advanced_search/` | `advanced_search_v3`, `advanced_search_v3_aggregated` |
| Containers | `POST /api/samples/containers/` | `list_containers_for_hashes` |
| Network threat intel | `/api/network-threat-intel/...` | `network_url_report`, `network_domain_report`, `network_ip_addr_report`, `network_ip_to_domain[_aggregated]`, `network_urls_from_ip[_aggregated]`, `network_files_from_ip[_aggregated]` |

## Key endpoints — examples

### Hash classification

```bash
curl -s "https://a1000.reversinglabs.com/api/samples/v3/<hash>/classification/?localOnly=false&av_scanners=true" \
  -H "Authorization: Token $TOKEN"
```

Response highlights: `classification` (malicious/suspicious/goodware/unknown), `riskscore` (0–10), `classification_origin`, `av_scanners.scanner_match`.

### Detailed report

```bash
curl -s -X POST "https://a1000.reversinglabs.com/api/samples/v2/list/details/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hash_values": ["<hash>"], "fields": ["classification","riskscore","attack","tags","ticore","networkthreatintelligence"]}'
```

Useful response fields:

| Field | Content |
|---|---|
| `classification` | Verdict |
| `classification_result` | Threat-name string (e.g. `Win32.Backdoor.Prorat`) |
| `riskscore` | 0–10 |
| `ticore` | TitaniumCore static analysis: format, headers, imports, strings, anomalies |
| `av_scanners` / `av_scanners_summary` | Per-engine + aggregate AV results |
| `tags` | Analyst + system tags |
| `ticloud` | Spectra Intelligence (TitaniumCloud) reputation when available |
| `attack` | MITRE ATT&CK tactics + techniques (objects with `tactic_id`, `technique_id`, `technique_name`) |
| `rl_cloud_sandbox` | Dynamic analysis output |
| `cape` / `cuckoo` / `joe` / `vmray_tcbase` / `fireeye` / `cisco_secure_malware_analytics` | Sandbox results per engine if configured |
| `networkthreatintelligence` | Network indicators extracted from the sample |
| `domainthreatintelligence` | Domain-level intel from network activity |
| `extracted_file_count` | Number of embedded/extracted files |
| `sources` / `aliases` | Sample provenance + filenames |

### Advanced search

```bash
curl -s -X POST "https://a1000.reversinglabs.com/api/samples/v2/advanced_search/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "threatname:Lockbit classification:malicious", "ticloud": false, "page": 1, "records_per_page": 100}'
```

Searchable fields include: `classification`, `av-detection`, `type` (sampletype), `positives`, `firstseen`, `lastseen`, `threatname`, `sampletype`, `filecount`, `size`, `sha1`, `sha256`, `md5`, `tlsh`, `ssdeep`, `imphash`, `tag`, `family`. Combine with implicit AND. Comparison operators: `>`, `>=`, `<`, `<=`, ranges with `:>2025-01-01`.

### Network threat intelligence

```bash
# IP reputation
curl -s "https://a1000.reversinglabs.com/api/network-threat-intel/ip/8.8.8.8/report/" \
  -H "Authorization: Token $TOKEN"

# Files seen on an IP
curl -s "https://a1000.reversinglabs.com/api/network-threat-intel/ip/8.8.8.8/downloaded_files/?extended=true" \
  -H "Authorization: Token $TOKEN"

# Domain reputation
curl -s "https://a1000.reversinglabs.com/api/network-threat-intel/domain/example.com/" \
  -H "Authorization: Token $TOKEN"

# URL reputation
curl -s -X POST "https://a1000.reversinglabs.com/api/network-threat-intel/url/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/path"}'
```

### Containers + extracted files (parent / child pivot)

```bash
# What containers spawned this hash?
curl -s -X POST "https://a1000.reversinglabs.com/api/samples/containers/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hash_values": ["<child-hash>"]}'

# What files came out of this hash?
curl -s "https://a1000.reversinglabs.com/api/samples/v2/<parent-hash>/extracted-files/?page_size=100&page=1" \
  -H "Authorization: Token $TOKEN"
```

## Spectra Intelligence vs Spectra Analyze

Spectra Intelligence (formerly TitaniumCloud) is a **separate cloud product** with separate credentials, exposed via `from ReversingLabs.SDK.ticloud import ...`. A1000 can query it as enrichment:

- `get_classification_v3(..., local_only=False)`
- `advanced_search_v3(..., ticloud=True)`
- `ticloud` field in detailed reports

These flags use the appliance's own TitaniumCloud license — they do **not** require additional credentials from the calling user. To query Spectra Intelligence directly (e.g. `RHA1FunctionalSimilarity` for fuzzy-hash sample search), separate `TICLOUD_USER` / `TICLOUD_PASSWORD` would be required and a separate skill would be needed; that is out of scope here.

## Response shape

The lookup skill emits a normalised envelope. See `skills/lookup-reversinglabs/SKILL.md` § Response format.
