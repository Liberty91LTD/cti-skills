# Tool Registry

External threat-intelligence integrations in the `cti-skills` pack. Each has:
- A **lookup skill** (`skills/lookup-<api>/SKILL.md`) — the agent-invokable interface
- An **integration guide** (`tools/integrations/<api>.md`) — auth setup, rate limits, Admiralty defaults
- A **CLI** (`tools/clis/<api>.js`) — zero-dependency Node.js wrapper the skill shells out to

All CLIs share the same invocation pattern: `node tools/clis/<api>.js <type> <value> [--dry-run]`. They read API keys from environment variables (set via `./scripts/setup.sh` or your shell rc).

## Catalog

| API | Skill | Env variable(s) | Indicators | Rate limit (free) | Admiralty default |
|---|---|---|---|---|---|
| [VirusTotal](integrations/virustotal.md) | `/lookup-virustotal` | `VIRUSTOTAL_API_KEY` | IP, domain, hash, URL | 4 req/min, 500/day | B2 |
| [AlienVault OTX](integrations/otx.md) | `/lookup-otx` | `OTX_API_KEY` | IP, domain, hash, URL | 10k req/hour | C3 |
| [URLScan.io](integrations/urlscan.md) | `/lookup-urlscan` | `URLSCAN_API_KEY` | URL, domain | 100 scans/day | B2 |
| [Shodan](integrations/shodan.md) | `/lookup-shodan` | `SHODAN_API_KEY` | IP, domain | 1 req/sec | B2 |
| [AbuseIPDB](integrations/abuseipdb.md) | `/lookup-abuseipdb` | `ABUSEIPDB_API_KEY` | IP only | 1000 checks/day | C3 |
| [GreyNoise](integrations/greynoise.md) | `/lookup-greynoise` | `GREYNOISE_API_KEY` | IP only | 50 req/day (community) | B2 |
| [Censys](integrations/censys.md) | `/lookup-censys` | `CENSYS_API_ID` + `CENSYS_API_SECRET` | IP, search query | 250/month | A2 |

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
