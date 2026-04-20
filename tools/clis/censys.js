#!/usr/bin/env node
// tools/clis/censys.js — Censys host / search lookup (zero deps, Node >= 18)
// Usage:
//   node censys.js ip <ip> [--dry-run]
//   node censys.js search "<censys query>" [--dry-run]

const https = require('https');

const API_ID = process.env.CENSYS_API_ID;
const API_SECRET = process.env.CENSYS_API_SECRET;
const API_BASE = 'https://search.censys.io/api/v2';

function die(msg, code = 1) {
  process.stderr.write(`error: ${msg}\n`);
  process.exit(code);
}

function usage() {
  process.stderr.write(
    'usage:\n' +
    '  censys.js ip <ip> [--dry-run]\n' +
    '  censys.js search "<censys query>" [--dry-run]\n\n' +
    'Env: CENSYS_API_ID + CENSYS_API_SECRET required (unless --dry-run).\n' +
    'Quota: free tier 250 queries/month — use --dry-run when testing.\n'
  );
  process.exit(3);
}

function get(url) {
  const auth = 'Basic ' + Buffer.from(`${API_ID}:${API_SECRET}`).toString('base64');
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { Authorization: auth, Accept: 'application/json' } }, (res) => {
      let body = '';
      res.on('data', (c) => (body += c));
      res.on('end', () => {
        if (res.statusCode >= 400) return reject(new Error(`HTTP ${res.statusCode}: ${body.slice(0, 300)}`));
        try { resolve(JSON.parse(body)); } catch { reject(new Error(`invalid JSON: ${body.slice(0, 300)}`)); }
      });
    }).on('error', reject);
  });
}

async function main() {
  const argv = process.argv.slice(2);
  const dryRun = argv.includes('--dry-run');
  const args = argv.filter((a) => !a.startsWith('--'));
  if (args.length < 2) usage();
  const [type, value] = args;
  if (!['ip', 'search'].includes(type)) usage();

  const url = type === 'ip'
    ? `${API_BASE}/hosts/${encodeURIComponent(value)}`
    : `${API_BASE}/hosts/search?q=${encodeURIComponent(value)}&per_page=5`;

  if (dryRun) {
    console.log(JSON.stringify({
      dry_run: true,
      method: 'GET',
      url,
      headers: { Authorization: API_ID && API_SECRET ? 'Basic <redacted>' : '<unset>' },
    }, null, 2));
    return;
  }
  if (!API_ID || !API_SECRET) die('CENSYS_API_ID and CENSYS_API_SECRET required.', 2);

  const resp = await get(url);

  if (type === 'ip') {
    const host = resp.result || {};
    const out = {
      source: 'censys',
      indicator: value,
      type: 'ip',
      query_time: new Date().toISOString(),
      services: (host.services || []).slice(0, 20).map((s) => ({
        port: s.port,
        service: s.service_name,
        banner: typeof s.banner === 'string' ? s.banner.slice(0, 400) : undefined,
        software: s.software?.map((sw) => `${sw.product} ${sw.version || ''}`.trim()),
      })),
      certificates: (host.services || [])
        .filter((s) => s.tls?.certificates?.leaf_data)
        .map((s) => ({
          port: s.port,
          subject_cn: s.tls.certificates.leaf_data.subject?.common_name?.[0],
          issuer: s.tls.certificates.leaf_data.issuer?.common_name?.[0],
          sha256: s.tls.certificates.leaf_data.fingerprint,
        })),
      autonomous_system: host.autonomous_system
        ? { asn: host.autonomous_system.asn, name: host.autonomous_system.name }
        : null,
      location: host.location
        ? { country: host.location.country_code, city: host.location.city }
        : null,
      last_updated: host.last_updated_at,
    };
    console.log(JSON.stringify(out, null, 2));
  } else {
    const hits = resp.result?.hits || [];
    const out = {
      source: 'censys',
      indicator: value,
      type: 'search',
      query_time: new Date().toISOString(),
      total: resp.result?.total,
      hits: hits.slice(0, 5).map((h) => ({
        ip: h.ip,
        services: h.services?.map((s) => `${s.service_name}/${s.port}`),
        autonomous_system: h.autonomous_system?.name,
        location: h.location?.country_code,
      })),
    };
    console.log(JSON.stringify(out, null, 2));
  }
}

main().catch((e) => die(e.message));
