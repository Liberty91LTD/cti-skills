# GreyNoise integration

[GreyNoise](https://www.greynoise.io/) classifies internet-wide scanning and background noise. Their honeypots observe opportunistic scanning activity, and they flag IPs as either "noise" (mass scanning, not targeting you specifically) or "RIOT" (rule-it-out: known-benign common services like CDNs, search engines, ISPs).

## Getting an API key

1. Sign up at https://www.greynoise.io/ (free community access)
2. Account → API keys → copy
3. Set `GREYNOISE_API_KEY` in your environment or via `./scripts/setup.sh`

## Rate limits

| Tier | Queries/day | Endpoints |
|---|---|---|
| Community (free) | 50 | `/community/{ip}` |
| Enterprise | higher | `/noise/context/{ip}`, search, pivots |

The CLI tries `/community/{ip}` first; falls back to `/noise/context/{ip}` if the key has enterprise access.

## Supported indicators

- IPv4 addresses

**IP only.** The CLI rejects non-IP inputs.

## Endpoints used

- `GET /v3/community/{ip}` (community, free)
- `GET /v2/noise/context/{ip}` (enterprise)

Authentication header: `key: $GREYNOISE_API_KEY`.

## Admiralty defaults (for `/score-source`)

**Source reliability:** B (usually reliable) — empirical honeypot observations.
**Information credibility:** 2 (probably true) — GreyNoise has strong data hygiene.

**Operational signal interpretation:**
- `noise: true` → IP is mass-scanning the internet. Strong evidence it is NOT a targeted threat to you specifically. Downgrade the severity of any detection.
- `riot: true` → IP is a known-benign common service (Googlebot, CDN, etc.). Likely a false positive if flagged by other tools.
- `classification: malicious` + `noise: true` → opportunistic scanner with known-bad intent (exploit scanner, credential stuffer). Still not targeted, but worth blocking.
- `classification: malicious` + `noise: false` → potential targeted activity. Investigate further.
- Unknown / no record → GreyNoise has not observed this IP in background noise. Does NOT mean clean — check other sources.

## Testing your key

```bash
curl -s "https://api.greynoise.io/v3/community/8.8.8.8" \
  -H "key: $GREYNOISE_API_KEY" | head -c 200
```

## See also

- API docs: https://docs.greynoise.io/
- Lookup skill: `skills/lookup-greynoise/SKILL.md`
- CLI source: `tools/clis/greynoise.js`
