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

- `POST /api/v1/scan/` — submit URL
- `GET /api/v1/result/{uuid}/` — retrieve scan result
- `GET /api/v1/search/?q=domain:<domain>` — search existing scans

Authentication header: `API-Key: $URLSCAN_API_KEY`.

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

- API docs: https://urlscan.io/docs/api/
- Lookup skill: `skills/lookup-urlscan/SKILL.md`
- CLI source: `tools/clis/urlscan.js`
