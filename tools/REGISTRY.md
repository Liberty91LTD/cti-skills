# Tool Registry

External threat-intelligence integrations in the `cti-skills` pack. Each has:
- A **lookup skill** (`skills/lookup-<api>/SKILL.md`) — the agent-invokable interface
- An **integration guide** (`tools/integrations/<api>.md`) — auth setup, rate limits, Admiralty defaults
- A **CLI** (`tools/clis/<api>.js`) — zero-dependency Node.js wrapper the skill shells out to

All Node CLIs share the same invocation pattern: `node tools/clis/<api>.js <type> <value> [--dry-run]`. They read API keys from environment variables (set via `./scripts/setup.sh` or your shell rc). _Exception: ReversingLabs and CrowdStrike ship Python-only — their auth requires a token exchange the official SDK handles (ReversingLabs token / CrowdStrike OAuth2), and there is no upstream Node SDK._

**Python CLIs with richer endpoint coverage** are now provided for every integration:

| Integration | Python CLI | Pattern | Adds beyond Node CLI |
|---|---|---|---|
| AbuseIPDB | `tools/clis/abuseipdb.py` | stdlib | `reports`, `check-block`, `blacklist` endpoints |
| AlienVault OTX | `tools/clis/otx.py` | OTXv2 SDK + venv | full-section indicator details, pulse search, pulse get, subscribed pulses |
| Censys | `tools/clis/censys.py` | censys-sdk + venv | **free aggregations**, certificate search/view, multi-page cursor, account info |
| CrowdStrike | `tools/clis/crowdstrike.py` | crowdstrike-falconpy + venv | **actor + finished intel** — IOC reputation, threat-actor profiles, origin/target actor search, MITRE ATT&CK TTPs, intel reports + PDF |
| GreyNoise | `tools/clis/greynoise.py` | pygreynoise SDK + venv | context, RIOT, similarity, timeline, GNQL search & stats, bulk quick |
| MISP | `tools/clis/misp.py` | stdlib | **two-way** — query events/attributes/objects + write attributes, create events, upload STIX 2 bundles, tag, publish |
| OpenCTI | `tools/clis/opencti.py` | stdlib | **two-way** — GraphQL query (lookup/search/list/get/connectors) + write indicators/observables, label, TLP-mark, relate, import STIX 2.1 bundles, guarded delete |
| Ransomware.live | `tools/clis/ransomwarelive.py` | stdlib | leak-site victim claims, **group profiles** (TTPs, leak-site infra), per-group IOCs + YARA, ransom notes, negotiations, CSIRT contacts |
| ReversingLabs | `tools/clis/reversinglabs.py` | reversinglabs-sdk-py3 + venv | hash classification, detailed/sandbox reports, advanced search, network URL/domain/IP intel, container/extracted-file pivot |
| Shodan | `tools/clis/shodan.py` | shodan-python SDK + venv | search, count, facets, DNS reverse/domain, account, ports/services |
| URLScan | `tools/clis/urlscan.py` | stdlib | Lucene search, quota, screenshot/DOM download, full submit options |
| VirusTotal | `tools/clis/virustotal.py` | stdlib | **relationship traversal** (the pivoting feature), URL submit, comments, Intel search |

Patterns:
- **stdlib** — no install, no venv, just `python3 tools/clis/<name>.py`.
- **SDK + venv** — self-bootstrapping venv at `tools/clis/.venv-<name>/` on first invocation. Private to that CLI; no global pollution; PEP-668-safe on Homebrew Python. Venv dirs are gitignored.

The Node and Python CLIs are complementary — Node for fast inline lookups in investigation chains, Python when you need the deeper API surface. Both read the same env-var keys.

## Catalog

| API | Skill | Env variable(s) | Indicators | Rate limit (free) | Admiralty default |
|---|---|---|---|---|---|
| [VirusTotal](integrations/virustotal.md) | `/lookup-virustotal` | `VIRUSTOTAL_API_KEY` | IP, domain, hash, URL | 4 req/min, 500/day | B2 |
| [AlienVault OTX](integrations/otx.md) | `/lookup-otx` | `OTX_API_KEY` | IP, domain, hash, URL | 10k req/hour | C3 |
| [URLScan.io](integrations/urlscan.md) | `/lookup-urlscan` | `URLSCAN_API_KEY` | URL, domain | 100 scans/day | B2 |
| [Shodan](integrations/shodan.md) | `/lookup-shodan` | `SHODAN_API_KEY` | IP, domain | 1 req/sec | B2 |
| [AbuseIPDB](integrations/abuseipdb.md) | `/lookup-abuseipdb` | `ABUSEIPDB_API_KEY` | IP only | 1000 checks/day | C3 |
| [GreyNoise](integrations/greynoise.md) | `/lookup-greynoise` | `GREYNOISE_API_KEY` | IP only | 50 req/day (community) | B2 |
| [Censys](integrations/censys.md) | `/lookup-censys` | `CENSYS_PAT` (Platform) / `CENSYS_API_ID`+`CENSYS_API_SECRET` (legacy) | IP, search query, certs | 250/month | A2 |
| [MISP](integrations/misp.md) | `/lookup-misp` | `MISP_URL` + `MISP_API_KEY` | events, attributes, objects, STIX 2 bundles | host-bound (no public limit) | B2 (varies by Org) |
| [OpenCTI](integrations/opencti.md) | `/lookup-opencti` | `OPENCTI_URL` + `OPENCTI_TOKEN` | entities, observables, STIX 2 bundles | host-bound (no public limit) | B2 (varies by feed/author) |
| [Ransomware.live](integrations/ransomwarelive.md) | `/lookup-ransomwarelive` | `RANSOMWARE_LIVE` | victim, group, sector, country, IOCs, YARA | 3000/day (PRO) | B2 (descriptions B3–B4) |
| [ReversingLabs A1000](integrations/reversinglabs.md) | `/lookup-reversinglabs` | `REVERSINGLABS_USER` + `REVERSINGLABS_PASSWORD` (+ optional `REVERSINGLABS_HOST`) | hash, url, domain, ip | undocumented; 429 + Retry-After | A2 |
| [CrowdStrike Falcon Intelligence](integrations/crowdstrike.md) | `/lookup-crowdstrike` | `CROWDSTRIKE_CLIENT_ID` + `CROWDSTRIKE_CLIENT_SECRET` (+ optional `CROWDSTRIKE_BASE_URL`) | ip, domain, hash, url, actor, report, MITRE | per-tenant; 429 + Retry-After | A2 |

Plus one local reference:

| Dataset | Skill | Source |
|---|---|---|
| MITRE ATT&CK Enterprise | `/mitre-attack` | bundled at `mitre-attack/` (see `scripts/setup.sh` for refresh) |

## Add a new integration

1. Create `skills/lookup-<name>/SKILL.md` with Agent Skills frontmatter, trigger phrases in description, and CLI invocation instructions
2. Create `tools/integrations/<name>.md` with auth setup, rate limits, and default Admiralty ratings
3. Create `tools/clis/<name>.js` — zero-dep Node CLI following the common pattern (see existing ones)
4. Add a row to the catalog table above
5. Bump `VERSIONS.md` and open a PR

## Common CLI behavior

All CLIs in `tools/clis/` implement:
- `--dry-run` — print the HTTP request that would be made, exit 0 without calling the API
- Exit code 0 on success, 1 on network/API error, 2 on missing API key, 3 on bad arguments
- JSON on stdout; human messages on stderr
- Normalized indicator types: `ip` (IPv4/IPv6), `domain`, `hash` (md5/sha1/sha256), `url`
