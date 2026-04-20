#!/usr/bin/env node
// tools/clis/greynoise.js — GreyNoise IP classification (zero deps, Node >= 18)
// Usage: node greynoise.js ip <ip> [--dry-run]

const https = require('https');

const API_KEY = process.env.GREYNOISE_API_KEY;
const API_BASE = 'https://api.greynoise.io';

function die(msg, code = 1) {
  process.stderr.write(`error: ${msg}\n`);
  process.exit(code);
}

function usage() {
  process.stderr.write(
    'usage: greynoise.js ip <ip> [--dry-run]\n\n' +
    'Env: GREYNOISE_API_KEY required (unless --dry-run). IP only.\n'
  );
  process.exit(3);
}

function get(url, headers) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers }, (res) => {
      let body = '';
      res.on('data', (c) => (body += c));
      res.on('end', () => {
        if (res.statusCode === 404) return resolve({ _not_found: true });
        if (res.statusCode >= 400) return reject(new Error(`HTTP ${res.statusCode}: ${body.slice(0, 300)}`));
        try { resolve(JSON.parse(body)); } catch { reject(new Error(`invalid JSON: ${body.slice(0, 300)}`)); }
      });
    }).on('error', reject);
  });
}

function isIP(s) {
  return /^(\d{1,3}\.){3}\d{1,3}$/.test(s) || (/^[0-9a-fA-F:]+$/.test(s) && s.includes(':'));
}

async function main() {
  const argv = process.argv.slice(2);
  const dryRun = argv.includes('--dry-run');
  const args = argv.filter((a) => !a.startsWith('--'));
  if (args.length < 2 || args[0] !== 'ip') usage();
  const value = args[1];
  if (!isIP(value)) die(`not an IP address: ${value}`, 3);

  const url = `${API_BASE}/v3/community/${encodeURIComponent(value)}`;
  const headers = { key: API_KEY || '', Accept: 'application/json' };

  if (dryRun) {
    console.log(JSON.stringify({ dry_run: true, method: 'GET', url, headers: { key: API_KEY ? '<redacted>' : '<unset>' } }, null, 2));
    return;
  }
  if (!API_KEY) die('GREYNOISE_API_KEY not set.', 2);

  const resp = await get(url, headers);

  if (resp._not_found) {
    const out = {
      source: 'greynoise',
      indicator: value,
      type: 'ip',
      query_time: new Date().toISOString(),
      observed: false,
      message: 'GreyNoise has not observed this IP in background noise',
    };
    console.log(JSON.stringify(out, null, 2));
    return;
  }

  const out = {
    source: 'greynoise',
    indicator: value,
    type: 'ip',
    query_time: new Date().toISOString(),
    observed: true,
    noise: resp.noise,
    riot: resp.riot,
    classification: resp.classification,
    name: resp.name,
    last_seen: resp.last_seen,
    message: resp.message,
    link: resp.link,
  };

  console.log(JSON.stringify(out, null, 2));
}

main().catch((e) => die(e.message));
