# ReversingLabs integration

[ReversingLabs Spectra Analyze](https://docs.reversinglabs.com/SpectraAnalyze/) (the A1000 appliance) is a malware analysis platform combining static decomposition (TitaniumCore), AV multi-scanning, dynamic sandbox detonation, and threat-name classification with optional Spectra Intelligence (TitaniumCloud) reputation enrichment. It is a licensed product — credentials are issued to customer accounts, not signed up for online.

## Getting credentials

1. Customer-side: obtain or request a Spectra Analyze user account from your RL administrator or RL account team. There is no public sign-up.
2. Note the appliance host (e.g. `https://a1000.reversinglabs.com` for the vendor-hosted tenant; on-prem deployments use a customer-controlled FQDN).
3. Set the env vars (or run `./scripts/setup.sh`):
   ```bash
   export REVERSINGLABS_USER="<username>"
   export REVERSINGLABS_PASSWORD="<password>"
   export REVERSINGLABS_HOST="https://a1000.reversinglabs.com"   # optional; default shown
   ```

The CLI's first invocation bootstraps a private Python venv at `tools/clis/.venv-reversinglabs/` and installs `reversinglabs-sdk-py3`. No global pip install.

## Authentication flow

Token-based, with auto-exchange:

1. SDK sends `POST /api-token-auth/` with form-encoded `username` + `password` at init.
2. Server returns `{"token": "<value>"}`.
3. SDK puts `Authorization: Token <value>` on every subsequent request.

You can also bypass the exchange by passing a token directly to `A1000(token=...)`. The CLI uses the username/password path.

## Rate limits

ReversingLabs does not publicly publish per-minute or per-day quotas for A1000. Empirically:

- The API returns **HTTP 429** with a `Retry-After: <seconds>` header when limits are exceeded.
- Submission endpoints poll status at 2-second intervals for up to 10 retries (SDK defaults `wait_time_seconds=2`, `retries=10`).
- Throttling is typically generous on customer appliances; pace concerns mostly apply to fan-out work (many `--pivot` calls in one investigation).

If you hit 429 repeatedly, back off, then split your fan-out across more time, or reduce `--max-results`.

## Supported indicators

| Type | CLI subcommand | Notes |
|---|---|---|
| File hash (MD5 / SHA-1 / SHA-256) | `hash`, `report`, `containers`, `extracted` | SHA-256 preferred |
| File (local path) | `submit-file` | Static + dynamic analysis on upload |
| URL | `submit-url`, `url` | `submit-url` triggers a crawl; `url` reads existing intel |
| Domain | `domain` | Network threat intelligence from RL corpus |
| IPv4 / IPv6 | `ip` | Optional pivots to files / domains / URLs seen on the IP |
| YARA ruleset name | `yara-matches` | Read-only — list samples that matched |
| Search query | `search` | Field-based search across the appliance corpus |

## Endpoints used

| CLI subcommand | REST endpoint | SDK method |
|---|---|---|
| `hash` | `GET /api/samples/v3/<hash>/classification/` | `get_classification_v3` |
| `report --summary` | `POST /api/samples/v2/list/` | `get_summary_report_v2` |
| `report --detailed` | `POST /api/samples/v2/list/details/` | `get_detailed_report_v2` |
| `submit-file` | `POST /api/uploads/` | `submit_file_from_path` / `submit_file_and_get_detailed_report` |
| `submit-url` | `POST /api/uploads/url` | `submit_url` / `submit_url_and_get_report` |
| `url` | `POST /api/network-threat-intel/url/` | `network_url_report` |
| `domain` | `GET /api/network-threat-intel/domain/<domain>/` | `network_domain_report` |
| `ip` | `GET /api/network-threat-intel/ip/<ip>/report/` (+ pivots) | `network_ip_addr_report` (+ `network_files_from_ip_aggregated` etc.) |
| `search` | `POST /api/samples/v2/advanced_search/` | `advanced_search_v3_aggregated` |
| `containers` | `POST /api/samples/containers/` | `list_containers_for_hashes` |
| `extracted` | `GET /api/samples/v2/<hash>/extracted-files/` | `list_extracted_files_v2_aggregated` |
| `yara-matches` | `GET /api/yara/v2/ruleset/<name>/matches/` | `get_yara_ruleset_matches_v2` |

Authentication header on every call: `Authorization: Token <token>` (handled by the SDK).

## Admiralty defaults (for `/score-source`)

**Source reliability:** A (completely reliable) — vendor-authoritative static + dynamic analysis pipeline.
**Information credibility:** 2 (probably true) — well validated against ground truth, but `unknown` / `suspicious` verdicts and very fresh samples warrant analyst verification.

**Downgrades:**
- `classification == unknown` → **B3**
- `classification == suspicious` and `av_scanners_summary.scanner_match < 3` → **B3**
- Sample first-seen <24h ago and `rl_cloud_sandbox` is empty → **B3** (sandbox detonation may have been incomplete)

**Upgrades:**
- `classification == malicious`, `av_scanners_summary.scanner_match >= 5`, sandbox produced behavioural evidence, threat name maps to a publicly-reported family → **A1**

## Privacy notes

- A1000 is single-tenant. Samples uploaded with `submit-file` enter that appliance's corpus; whether they propagate to Spectra Intelligence depends on the customer's TitaniumCloud contribution settings (off by default for most enterprise customers).
- Not a public-research service — do not assume content is shareable beyond your organisation.
- Tokens issued via `/api-token-auth/` are reusable. Treat them as long-lived secrets if you cache the token rather than re-exchanging on each session.

## Testing your credentials

```bash
# Token round-trip
curl -s -X POST "$REVERSINGLABS_HOST/api-token-auth/" \
  -d "username=$REVERSINGLABS_USER&password=$REVERSINGLABS_PASSWORD" | head -c 200

# Or use the CLI's dry-run path (no network call):
python3 tools/clis/reversinglabs.py hash 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 --dry-run

# Real round-trip (uses one API call):
python3 tools/clis/reversinglabs.py hash 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
```

## See also

- API reference (companion skill): `skills/reversinglabs-api/SKILL.md`
- Lookup skill: `skills/lookup-reversinglabs/SKILL.md`
- Python CLI source: `tools/clis/reversinglabs.py`
- Official product docs: https://docs.reversinglabs.com/SpectraAnalyze/
- SDK source: https://github.com/reversinglabs/reversinglabs-sdk-py3
