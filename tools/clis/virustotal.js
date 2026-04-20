#!/usr/bin/env node
// tools/clis/virustotal.js — VirusTotal API v3 lookup (zero deps, Node >= 18)
// Usage: node virustotal.js <ip|domain|hash|url> <value> [--dry-run]

const https = require('https');

const API_KEY = process.env.VIRUSTOTAL_API_KEY;
const API_BASE = 'https://www.virustotal.com/api/v3';

function die(msg, code = 1) {
  process.stderr.write(`error: ${msg}\n`);
  process.exit(code);
}

function usage() {
  process.stderr.write(
    'usage: virustotal.js <ip|domain|hash|url> <value> [--dry-run]\n\n' +
    'Env: VIRUSTOTAL_API_KEY required (unless --dry-run).\n'
  );
  process.exit(3);
}

function get(url, headers) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers }, (res) => {
      let body = '';
      res.on('data', (c) => (body += c));
      res.on('end', () => {
        if (res.statusCode === 429) return reject(new Error('rate limited (429). Back off and retry.'));
        if (res.statusCode >= 400) return reject(new Error(`HTTP ${res.statusCode}: ${body.slice(0, 300)}`));
        try { resolve(JSON.parse(body)); } catch { reject(new Error(`invalid JSON: ${body.slice(0, 300)}`)); }
      });
    }).on('error', reject);
  });
}

function pathFor(type, value) {
  if (type === 'ip') return `/ip_addresses/${encodeURIComponent(value)}`;
  if (type === 'domain') return `/domains/${encodeURIComponent(value)}`;
  if (type === 'hash') return `/files/${encodeURIComponent(value)}`;
  if (type === 'url') {
    const urlId = Buffer.from(value).toString('base64').replace(/=+$/, '').replace(/\+/g, '-').replace(/\//g, '_');
    return `/urls/${urlId}`;
  }
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
  const headers = { 'x-apikey': API_KEY || '', Accept: 'application/json' };

  if (dryRun) {
    console.log(JSON.stringify({ dry_run: true, method: 'GET', url, headers: { 'x-apikey': API_KEY ? '<redacted>' : '<unset>' } }, null, 2));
    return;
  }
  if (!API_KEY) die('VIRUSTOTAL_API_KEY not set. Run ./scripts/setup.sh or export the key.', 2);

  const resp = await get(url, headers);
  const attrs = resp.data?.attributes || {};
  const stats = attrs.last_analysis_stats || {};
  const total = Object.values(stats).reduce((a, b) => a + b, 0);
  const malicious = stats.malicious || 0;
  const suspicious = stats.suspicious || 0;

  let verdict = 'unknown';
  if (malicious >= 5) verdict = 'malicious';
  else if (malicious >= 1 || suspicious >= 2) verdict = 'suspicious';
  else if (total >= 10) verdict = 'clean';

  const out = {
    source: 'virustotal',
    indicator: value,
    type,
    query_time: new Date().toISOString(),
    detection_ratio: `${malicious}/${total}`,
    community_score: attrs.reputation ?? null,
    verdict,
    key_findings: [],
    additional_context: {
      as_owner: attrs.as_owner,
      country: attrs.country,
      names: Array.isArray(attrs.names) ? attrs.names.slice(0, 5) : undefined,
      type_description: attrs.type_description,
      popular_threat_classification: attrs.popular_threat_classification?.suggested_threat_label,
      registrar: attrs.registrar,
      creation_date: attrs.creation_date,
      tags: attrs.tags,
    },
  };

  console.log(JSON.stringify(out, null, 2));
}

main().catch((e) => die(e.message));
