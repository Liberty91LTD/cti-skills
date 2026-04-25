# AbuseIPDB integration

[AbuseIPDB](https://www.abuseipdb.com/) is a community database of IPs reported for abusive behavior (brute-force, scanning, spam, fraud, DDoS, etc.). Each IP has a confidence-of-abuse score derived from report volume, reporter diversity, and recency.

## Getting an API key

1. Sign up at https://www.abuseipdb.com/register
2. Account → API → Create Key
3. Set `ABUSEIPDB_API_KEY` in your environment or via `./scripts/setup.sh`

## Rate limits

| Tier | Checks/day | Reports/day |
|---|---|---|
| Free | 1,000 | 3,000 |
| Basic Subscriber | 3,000 | 5,000 |
| Premium | 10,000 | 10,000 |
| Webmaster | 5,000 | 5,000 |

## Supported indicators

- IPv4 addresses
- IPv6 addresses

**IP only.** The CLI rejects non-IP inputs.

## Endpoints used

The **Node CLI** (`tools/clis/abuseipdb.js`) hits only:
- `GET /api/v2/check?ipAddress={ip}&maxAgeInDays=90` — IP reputation

The **Python CLI** (`tools/clis/abuseipdb.py`) covers four read-only endpoints:
- `GET /api/v2/check` — IP reputation (with optional `verbose=` flag for full report list)
- `GET /api/v2/reports` — paginated report history for an IP
- `GET /api/v2/check-block` — reputation summary for a CIDR network range
- `GET /api/v2/blacklist` — bulk download of high-confidence blacklisted IPs

Authentication header: `Key: $ABUSEIPDB_API_KEY`.

## Write endpoints (not exposed by either CLI)

Per [the official docs](https://docs.abuseipdb.com/), AbuseIPDB also offers:
- `POST /api/v2/report` — submit a single report
- `POST /api/v2/bulk-report` — submit a CSV of reports
- `DELETE /api/v2/clear-address` — clear your own reports for an IP

These are intentionally not wired into the lookup CLIs to prevent accidental writes. To contribute reports back, use the AbuseIPDB dashboard or write a separate, deliberately-confirmed script.

## Admiralty defaults (for `/score-source`)

**Source reliability:** C (fairly reliable) — community-reported, false positives possible.
**Information credibility:** 3 (possibly true) — report quality varies.

**Upgrades:**
- `distinct_reporters` >10 AND `abuse_confidence` >75 → **B2**
- Consistent recent reports across categories (brute-force + scanning + spam) → **B2**

**Downgrades:**
- Single reporter, generic category → **D4**
- `abuse_confidence` <15 (near-clean) → treat as no-signal, not negative evidence

## Report categories (for reference)

1 DNS Compromise · 2 DNS Poisoning · 3 Fraud Orders · 4 DDoS · 5 FTP Brute-Force · 6 Ping of Death · 7 Phishing · 8 Fraud VoIP · 9 Open Proxy · 10 Web Spam · 11 Email Spam · 12 Blog Spam · 13 VPN IP · 14 Port Scan · 15 Hacking · 16 SQL Injection · 17 Spoofing · 18 Brute-Force · 19 Bad Web Bot · 20 Exploited Host · 21 Web App Attack · 22 SSH · 23 IoT Targeted

## Testing your key

```bash
curl -s "https://api.abuseipdb.com/api/v2/check?ipAddress=8.8.8.8" \
  -H "Key: $ABUSEIPDB_API_KEY" -H "Accept: application/json" | head -c 200
```

## See also

- API docs: https://docs.abuseipdb.com/
- Lookup skill: `skills/lookup-abuseipdb/SKILL.md`
- Node CLI source: `tools/clis/abuseipdb.js`
- Python CLI source: `tools/clis/abuseipdb.py`
