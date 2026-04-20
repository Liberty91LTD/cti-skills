#!/usr/bin/env node
// tools/clis/otx.js — AlienVault OTX lookup (zero deps, Node >= 18)
// Usage: node otx.js <ip|domain|hash|url> <value> [--dry-run]

const https = require('https');

const API_KEY = process.env.OTX_API_KEY;
const API_BASE = 'https://otx.alienvault.com/api/v1';

function die(msg, code = 1) {
  process.stderr.write(`error: ${msg}\n`);
  process.exit(code);
}

function usage() {
  process.stderr.write(
    'usage: otx.js <ip|domain|hash|url> <value> [--dry-run]\n\n' +
    'Env: OTX_API_KEY required (unless --dry-run).\n'
  );
  process.exit(3);
}

function get(url, headers) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers }, (res) => {
      let body = '';
      res.on('data', (c) => (body += c));
      res.on('end', () => {
        if (res.statusCode === 429) return reject(new Error('rate limited (429)'));
        if (res.statusCode >= 400) return reject(new Error(`HTTP ${res.statusCode}: ${body.slice(0, 300)}`));
        try { resolve(JSON.parse(body)); } catch { reject(new Error(`invalid JSON: ${body.slice(0, 300)}`)); }
      });
    }).on('error', reject);
  });
}

function pathFor(type, value) {
  const enc = encodeURIComponent(value);
  if (type === 'ip') return `/indicators/IPv4/${enc}/general`;
  if (type === 'domain') return `/indicators/domain/${enc}/general`;
  if (type === 'hash') return `/indicators/file/${enc}/general`;
  if (type === 'url') return `/indicators/url/${enc}/general`;
  usage();
}

async function main() {
  const argv = process.argv.slice(2);
  const dryRun = argv.includes('--dry-run');
  const args = argv.filter((a) => !a.startsWith('--'));
  if (args.length < 2) usage();
  const [type, value] = args;
  if (!['ip', 'domain', 'hash', 'url'].includes(type)) usage();

  const url = API_BASE + pathFor(type, value);
  const headers = { 'X-OTX-API-KEY': API_KEY || '', Accept: 'application/json' };

  if (dryRun) {
    console.log(JSON.stringify({ dry_run: true, method: 'GET', url, headers: { 'X-OTX-API-KEY': API_KEY ? '<redacted>' : '<unset>' } }, null, 2));
    return;
  }
  if (!API_KEY) die('OTX_API_KEY not set. Run ./scripts/setup.sh or export the key.', 2);

  const resp = await get(url, headers);
  const pulses = resp.pulse_info?.pulses || [];

  const out = {
    source: 'otx',
    indicator: value,
    type,
    query_time: new Date().toISOString(),
    pulse_count: pulses.length,
    key_pulses: pulses.slice(0, 10).map((p) => ({
      name: p.name,
      tags: p.tags,
      created: p.created,
      tlp: p.tlp,
      author: p.author?.username || p.author_name,
      malware_families: p.malware_families?.map((m) => m.display_name),
      attack_ids: p.attack_ids,
    })),
    related_indicators: resp.pulse_info?.related || [],
    passive_dns: resp.passive_dns?.slice(0, 10) || [],
    whois: resp.whois,
    base_indicator: resp.base_indicator,
  };

  console.log(JSON.stringify(out, null, 2));
}

main().catch((e) => die(e.message));
