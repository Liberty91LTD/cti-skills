---
name: cti-setup
description: Use when the user wants to configure API keys for the CTI skills pack, asks "how do I set up keys", "configure VirusTotal", "add my Shodan key", or runs /cti-setup. Walks through API key configuration inside Claude Code without needing to run a shell script. Also handles re-running setup, adding individual keys, and verifying that configured keys work.
metadata:
  version: 1.0.0
  tags: [setup, configuration, onboarding]
---

# cti-setup

In-chat configuration of API keys for the threat-intel integrations bundled with this pack. Use this when the user is in Claude Code and doesn't want to drop to a shell to run `./scripts/setup.sh`.

## When to invoke

- User asks "how do I set up keys", "configure my API keys", "add a VirusTotal key", etc.
- User runs `/cti-setup`
- A `lookup-*` skill failed because a key is missing and you want to offer to add it
- After install via `/plugin marketplace add` or `npx` (no shell setup ran)

## What you do

1. **Check current state.** Read `.claude/settings.local.json`. If it's missing or has no `env` block, the user has zero keys configured. If it has some, list which are present and which are missing.
2. **Tell the user the menu.** Present the services in a table with: name, env variable, free-tier limit, signup URL. Make clear all are optional and that the pack degrades gracefully.
3. **Ask which to configure.** Let the user provide one, several, or all. Don't force them through every prompt.
4. **Receive the keys.** When the user shares a key, treat it as sensitive — do not echo it back in plain text in your response (refer to it as `your VirusTotal key` or the masked tail `…<last 4 chars>`).
5. **Write the merged file.** Use the non-destructive merge below — preserve every other field in `settings.local.json`.
6. **Offer to verify.** Ask if they want you to dry-run each configured key against its CLI to confirm it's wired up.
7. **Tell them what's next.** "Try `/ip-investigation 8.8.8.8`" or similar concrete next command.

## The services

| Service | Env variable | Free tier | Signup |
|---|---|---|---|
| Liberty91 (first-party) | `LIBERTY91_API_KEY` (optional `LIBERTY91_API_URL`) | per-key rate limit + monthly credits on your plan | Liberty91 platform → user menu → API Access (Owner/Admin only; the secret is shown once) |
| VirusTotal | `VIRUSTOTAL_API_KEY` | 4/min, 500/day | virustotal.com → profile → API key |
| URLScan.io | `URLSCAN_API_KEY` | 100 scans/day | urlscan.io → user settings |
| Shodan | `SHODAN_API_KEY` | 1 req/sec | account.shodan.io |
| AbuseIPDB | `ABUSEIPDB_API_KEY` | 1000 checks/day | abuseipdb.com → account → API |
| GreyNoise | `GREYNOISE_API_KEY` | 50 req/day (community) | viz.greynoise.io → account |
| AlienVault OTX | `OTX_API_KEY` | 10k req/hour | otx.alienvault.com → settings |
| Censys | `CENSYS_PAT` | 250 queries/month | accounts.censys.io → settings → personal-access-tokens |
| MISP | `MISP_URL` + `MISP_API_KEY` | self-hosted / org-provided | your MISP instance → My Profile → Auth keys |
| OpenCTI | `OPENCTI_URL` + `OPENCTI_TOKEN` | self-hosted / org-provided | your OpenCTI instance → profile → API access (token) |
| Ransomware.live | `RANSOMWARE_LIVE` | 3000 req/day (PRO) | my.ransomware.live → free PRO key |
| ReversingLabs A1000 | `REVERSINGLABS_USER` + `REVERSINGLABS_PASSWORD` (optional `REVERSINGLABS_HOST`) | undocumented; 429+Retry-After | licensed product — issued by your RL admin or RL account team |
| CrowdStrike Falcon Intelligence | `CROWDSTRIKE_CLIENT_ID` + `CROWDSTRIKE_CLIENT_SECRET` (optional `CROWDSTRIKE_BASE_URL`) | per-tenant; 429+Retry-After | licensed product — Falcon console → Support and resources → API clients and keys (assign Intel read scopes) |

If the user has a Liberty91 account, configure `LIBERTY91_API_KEY` first — it is the pack's first-party source and `/lookup-liberty91` runs before third-party lookups, so it saves other services' quota. Keys are `l91_live_` (production) or `l91_test_` (development); an empty scope list on the key grants all read scopes, which is the right default for enrichment. Set `LIBERTY91_API_URL` only to point at a non-production host.

A starter set of **VirusTotal + OTX + URLScan + AbuseIPDB** covers most IP/domain/URL/hash investigations. Shodan and GreyNoise add value for IP-focused work. Censys is optional (very tight rate limit). MISP requires both a base URL and an auth key — point it at your org's instance. OpenCTI likewise takes a base URL plus an API token and powers `/lookup-opencti` (two-way: query your knowledge base + push vetted intel back). Ransomware.live powers the `lookup-ransomwarelive` and `ransomware-ecosystem` skills (victim/group tracking). ReversingLabs is a licensed product — only configure if your organisation has a Spectra Analyze (A1000) account. CrowdStrike Falcon Intelligence is a licensed subscription — it powers `/lookup-crowdstrike` for IOC reputation AND threat-actor / TTP / report intelligence; configure if your org has a Falcon Intelligence licence with Intel API scopes.

## How to write the file

The file is `.claude/settings.local.json`. It is gitignored. **Do not overwrite it** — read, merge the `env` block, write back. Use the bundled setup script which handles this safely:

```bash
./scripts/setup.sh --non-interactive \
  --liberty91=USER_PROVIDED_KEY \
  --virustotal=USER_PROVIDED_KEY \
  --shodan=USER_PROVIDED_KEY \
  --misp-url=https://misp.example.org \
  --misp=USER_PROVIDED_KEY \
  --opencti-url=https://opencti.example.org \
  --opencti=USER_PROVIDED_TOKEN \
  --ransomwarelive=USER_PROVIDED_KEY \
  --reversinglabs-user=USER_PROVIDED_USERNAME \
  --reversinglabs-password=USER_PROVIDED_PASSWORD \
  --reversinglabs-host=https://a1000.reversinglabs.com
```

(Pass only the flags for keys the user actually shared. Available flags: `--liberty91`, `--liberty91-url`, `--virustotal`, `--urlscan`, `--shodan`, `--abuseipdb`, `--greynoise`, `--otx`, `--censys`, `--misp-url`, `--misp`, `--opencti-url`, `--opencti`, `--ransomwarelive`, `--reversinglabs-user`, `--reversinglabs-password`, `--reversinglabs-host`, `--crowdstrike-client-id`, `--crowdstrike-client-secret`, `--crowdstrike-base-url`.)

If `scripts/setup.sh` is not present (e.g. plugin-only install), do the merge yourself with this Node one-liner. Replace `KEY=VAL` pairs with the user's input:

```bash
node -e "
  const fs = require('fs');
  const path = '.claude/settings.local.json';
  let cur = {};
  try { cur = JSON.parse(fs.readFileSync(path, 'utf8')); } catch(e) {}
  cur.env = cur.env || {};
  Object.assign(cur.env, {
    VIRUSTOTAL_API_KEY: 'USER_PROVIDED_KEY',
    SHODAN_API_KEY: 'USER_PROVIDED_KEY',
  });
  fs.mkdirSync('.claude', { recursive: true });
  fs.writeFileSync(path, JSON.stringify(cur, null, 2) + '\n');
"
```

After writing, confirm to the user:
- which keys were added (by service name, not the key value)
- which keys are still unconfigured
- that the file is gitignored

## Verifying keys

If the user wants to verify, run:

```bash
./scripts/setup.sh --verify
```

This dry-runs each lookup CLI and reports OK/fail per service without making a real API call. If `setup.sh` is unavailable, dry-run each CLI individually:

```bash
node tools/clis/virustotal.js ip 8.8.8.8 --dry-run
```

Exit code 0 = key present and CLI invocation OK. Exit code 2 = missing key.

## Removing or rotating a key

To remove a key, edit `.claude/settings.local.json` and delete the entry from the `env` block (or set its value to `""`). To rotate, just re-run setup with the new value — the merge overwrites that key only.

## Security notes

- Never commit `.claude/settings.local.json` (already gitignored at repo root).
- Never echo the full key value back to the user in chat — they shared it once; mask thereafter.
- Don't write keys to logs, screenshots, or other artefacts.
- If the user accidentally pastes a key into a public channel, advise them to rotate it on the provider's site and re-run `/cti-setup` with the new value.

## What this does NOT do

- Does not call the threat-intel APIs (only `--dry-run` invocations of the local CLIs).
- Does not download MITRE ATT&CK data — for that, run `./scripts/download-mitre.sh` (the `/mitre-attack` skill self-heals on first use).
- Does not configure permissions, hooks, or other Claude Code settings — only the `env` block of `settings.local.json`.
