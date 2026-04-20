#!/usr/bin/env node
// tools/clis/abuseipdb.js — AbuseIPDB IP check (zero deps, Node >= 18)
// Usage: node abuseipdb.js ip <ip> [--dry-run]

const https = require('https');

const API_KEY = process.env.ABUSEIPDB_API_KEY;
const API_BASE = 'https://api.abuseipdb.com/api/v2';

function die(msg, code = 1) {
  process.stderr.write(`error: ${msg}\n`);
  process.exit(code);
}

function usage() {
  process.stderr.write(
    'usage: abuseipdb.js ip <ip> [--dry-run]\n\n' +
    'Env: ABUSEIPDB_API_KEY required (unless --dry-run). IP only.\n'
  );
  process.exit(3);
}

function get(url, headers) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers }, (res) => {
      let body = '';
      res.on('data', (c) => (body += c));
      res.on('end', () => {
        if (res.statusCode >= 400) return reject(new Error(`HTTP ${res.statusCode}: ${body.slice(0, 300)}`));
        try { resolve(JSON.parse(body)); } catch { reject(new Error(`invalid JSON: ${body.slice(0, 300)}`)); }
      });
    }).on('error', reject);
  });
}

function isIP(s) {
  // simple IPv4/IPv6 check
  return /^(\d{1,3}\.){3}\d{1,3}$/.test(s) || /^[0-9a-fA-F:]+$/.test(s) && s.includes(':');
}

async function main() {
  const argv = process.argv.slice(2);
  const dryRun = argv.includes('--dry-run');
  const args = argv.filter((a) => !a.startsWith('--'));
  if (args.length < 2 || args[0] !== 'ip') usage();
  const value = args[1];
  if (!isIP(value)) die(`not an IP address: ${value}`, 3);

  const url = `${API_BASE}/check?ipAddress=${encodeURIComponent(value)}&maxAgeInDays=90`;
  const headers = { Key: API_KEY || '', Accept: 'application/json' };

  if (dryRun) {
    console.log(JSON.stringify({ dry_run: true, method: 'GET', url, headers: { Key: API_KEY ? '<redacted>' : '<unset>' } }, null, 2));
    return;
  }
  if (!API_KEY) die('ABUSEIPDB_API_KEY not set.', 2);

  const resp = await get(url, headers);
  const d = resp.data || {};

  const out = {
    source: 'abuseipdb',
    indicator: value,
    type: 'ip',
    query_time: new Date().toISOString(),
    abuse_confidence: d.abuseConfidenceScore,
    total_reports: d.totalReports,
    distinct_reporters: d.numDistinctUsers,
    last_reported: d.lastReportedAt,
    isp: d.isp,
    usage_type: d.usageType,
    country: d.countryCode,
    is_tor: d.isTor,
    is_whitelisted: d.isWhitelisted,
    domain: d.domain,
    hostnames: d.hostnames,
  };

  console.log(JSON.stringify(out, null, 2));
}

main().catch((e) => die(e.message));
