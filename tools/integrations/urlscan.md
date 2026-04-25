# URLScan.io integration

[URLScan.io](https://urlscan.io/) is a service that loads URLs in an instrumented sandbox browser and records the full page-load behavior: redirects, contacted domains/IPs, resources loaded, certificates, screenshots, and verdicts.

## Getting an API key

1. Sign up at https://urlscan.io/user/signup (free)
2. Settings → API Keys → create a key
3. Set `URLSCAN_API_KEY` in your environment or via `./scripts/setup.sh`

## Rate limits

| Tier | Scans/day | Searches/month |
|---|---|---|
| Free | 100 | 5,000 |
| Pro | 10,000 | unlimited |
| Enterprise | unlimited | unlimited |

The CLI handles polling with exponential-style retry (30s initial wait, up to 5 × 10s retries) for scan result availability.

## Supported indicators

- URLs
- Domains (searches existing scans; optionally submits a new scan for the domain's homepage)

## Endpoints used

The **Node CLI** (`tools/clis/urlscan.js`) handles a single submit-and-poll flow plus simple domain search:
- `POST /api/v1/scan/` — submit URL
- `GET /api/v1/result/{uuid}/` — retrieve scan result
- `GET /api/v1/search/?q=domain:<domain>` — basic domain search

The **Python CLI** (`tools/clis/urlscan.py`) covers the full public API:
- `POST /api/v1/scan/` — submit (with country/tags/UA/referer/visibility flags, optional wait-and-poll)
- `GET /api/v1/result/{uuid}/` — retrieve a scan
- `GET /api/v1/search/` — full Lucene query search (the killer feature for pivoting)
- `GET /api/v1/quotas/` — current quota across search/retrieve/scan dimensions
- `GET https://urlscan.io/screenshots/{uuid}.png` — screenshot download
- `GET /api/v1/dom/{uuid}/` — captured DOM/HTML download

Authentication header: `API-Key: $URLSCAN_API_KEY`.

## Lucene query reference (selection)

Common fields against which you can search:

| Field | Example | Use |
|---|---|---|
| `page.domain` | `page.domain:malicious.example` | Domain-level pivots |
| `page.url` | `page.url:*login*` | Substring URL match |
| `page.ip` | `page.ip:185.220.101.45` | All scans hitting this IP |
| `page.country` | `page.country:RU` | Geographic filter |
| `page.asn` | `page.asn:AS13335` | ASN-level pivots |
| `task.tags` | `task.tags:phishing` | Tagged categories |
| `task.url` | `task.url:*paypal*` | What was requested (pre-redirect) |
| `verdicts.overall.malicious` | `verdicts.overall.malicious:true` | Only malicious results |
| `hash` | `hash:<sha256>` | Resource hash (favicon, JS, etc.) — strong fingerprint |
| `filename` | `filename:*.exe` | Downloaded filename |
| `date` | `date:>now-7d` | Time window |

Combine with `AND`, `OR`, `NOT`, parentheses, wildcards (`*`).

Full search query reference: https://urlscan.io/search/

## Visibility

URLScan submissions can be **public**, **unlisted**, or **private** (Pro).

**The CLI defaults to `unlisted`.** Public submissions expose the indicator to everyone on URLScan's global feed — this can tip off threat actors that you're investigating them. Only use `--visibility public` when the user explicitly asks.

## Admiralty defaults (for `/score-source`)

**Source reliability:** B (usually reliable) — live-scan evidence is empirical.
**Information credibility:** 2 (probably true) — verdicts can be noisy.

**Downgrades:**
- Verdict is ambiguous or indicator is edge-case (JS-obfuscated content, short session) → **C3**

**Upgrades:**
- Verdict is "malicious" + behavior shows clear malicious actions (credential form, drive-by download, etc.) → **A1**

## Testing your key

```bash
curl -s "https://urlscan.io/api/v1/search/?q=domain:example.com&size=1" \
  -H "API-Key: $URLSCAN_API_KEY" | head -c 200
```

## Privacy notes

- Default `unlisted` means the scan is not listed in public search, but the UUID URL is still accessible to anyone who has it.
- For truly private scans, use Pro tier's private visibility.

## See also

- API docs: https://docs.urlscan.io/apis/urlscan-openapi/live-scanning
- Search syntax: https://urlscan.io/search/
- Lookup skill: `skills/lookup-urlscan/SKILL.md`
- Node CLI source: `tools/clis/urlscan.js`
- Python CLI source: `tools/clis/urlscan.py`
