# VirusTotal integration

[VirusTotal](https://www.virustotal.com/) aggregates reputation signals from 70+ antivirus engines and URL scanners, plus community comments, file behavior sandboxes, and passive DNS.

## Getting an API key

1. Sign up at https://www.virustotal.com/gui/join-us (free account)
2. Profile → API key → copy
3. Set `VIRUSTOTAL_API_KEY` in your environment or add it to `.claude/settings.local.json` via `./scripts/setup.sh`

## Rate limits

| Tier | Requests/min | Requests/day | Notes |
|---|---|---|---|
| Free (public) | 4 | 500 | 15,500/month cap |
| Premium | 1000 | — | Contact sales |
| Enterprise Intelligence | unlimited | — | Includes `/intelligence/search` |

The CLI respects 429 responses and reports rate-limit hits to stderr. Back off and retry later.

## Supported indicators

- IPv4 / IPv6 addresses
- Domains
- File hashes: MD5, SHA-1, SHA-256
- URLs (base64-encoded internally; the CLI handles encoding)

## Endpoints used

- `GET /api/v3/ip_addresses/{ip}`
- `GET /api/v3/ip_addresses/{ip}/communicating_files?limit=10` (optional pivot)
- `GET /api/v3/domains/{domain}`
- `GET /api/v3/files/{hash}`
- `GET /api/v3/files/{hash}/behaviours` (optional behavior analysis)
- `GET /api/v3/urls/{url_id}` (url_id = base64url(url) minus `=` padding)

Authentication header: `x-apikey: $VIRUSTOTAL_API_KEY`.

## Admiralty defaults (for `/score-source`)

**Source reliability:** B (usually reliable) — VirusTotal is an aggregator, not a primary researcher. Underlying engine signals vary in quality.
**Information credibility:** 2 (probably true) — widely corroborated by community activity.

**Downgrades:**
- Only 1–2 engines detect → drop to **C3** (single-engine signals are often false positives)
- Indicator is an old hash in a generic packer → **C3**

**Upgrades:**
- 30+ engines detect + behavior analysis shows clearly malicious actions → **A1**

## Testing your key

```bash
curl -s "https://www.virustotal.com/api/v3/ip_addresses/8.8.8.8" \
  -H "x-apikey: $VIRUSTOTAL_API_KEY" | head -c 200
```

## Privacy notes

- VirusTotal is **not private**. Hashes and URLs you submit may become visible to other VirusTotal users (especially premium).
- Do not upload files unless you're prepared for them to be distributed.
- For sensitive investigations, use `/intelligence/search` (premium) or private VT tenants.

## See also

- API docs: https://docs.virustotal.com/reference/overview
- Lookup skill: `skills/lookup-virustotal/SKILL.md`
- CLI source: `tools/clis/virustotal.js`
