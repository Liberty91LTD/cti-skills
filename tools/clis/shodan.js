#!/usr/bin/env node
// tools/clis/shodan.js — Shodan host lookup (zero deps, Node >= 18)
// Usage: node shodan.js <ip|domain> <value> [--dry-run]

const https = require('https');

const API_KEY = process.env.SHODAN_API_KEY;
const API_BASE = 'https://api.shodan.io';

function die(msg, code = 1) {
  process.stderr.write(`error: ${msg}\n`);
  process.exit(code);
}

function usage() {
  process.stderr.write(
    'usage: shodan.js <ip|domain> <value> [--dry-run]\n\n' +
    'Env: SHODAN_API_KEY required (unless --dry-run).\n'
  );
  process.exit(3);
}

function get(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let body = '';
      res.on('data', (c) => (body += c));
      res.on('end', () => {
        if (res.statusCode >= 400) return reject(new Error(`HTTP ${res.statusCode}: ${body.slice(0, 300)}`));
        try { resolve(JSON.parse(body)); } catch { reject(new Error(`invalid JSON: ${body.slice(0, 300)}`)); }
      });
    }).on('error', reject);
  });
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function resolveDomain(domain) {
  const url = `${API_BASE}/dns/resolve?hostnames=${encodeURIComponent(domain)}&key=${API_KEY}`;
  const resp = await get(url);
  return resp[domain];
}

async function hostInfo(ip) {
  const url = `${API_BASE}/shodan/host/${encodeURIComponent(ip)}?key=${API_KEY}`;
  return get(url);
}

async function main() {
  const argv = process.argv.slice(2);
  const dryRun = argv.includes('--dry-run');
  const args = argv.filter((a) => !a.startsWith('--'));
  if (args.length < 2) usage();
  const [type, value] = args;
  if (!['ip', 'domain'].includes(type)) usage();

  if (dryRun) {
    const url = type === 'ip'
      ? `${API_BASE}/shodan/host/${value}?key=<redacted>`
      : `${API_BASE}/dns/resolve?hostnames=${value} (then /shodan/host/{ip})`;
    console.log(JSON.stringify({ dry_run: true, method: 'GET', url }, null, 2));
    return;
  }
  if (!API_KEY) die('SHODAN_API_KEY not set.', 2);

  let ip = value;
  let resolvedIp = null;
  if (type === 'domain') {
    resolvedIp = await resolveDomain(value);
    if (!resolvedIp) die(`could not resolve ${value}`);
    ip = resolvedIp;
    await sleep(1000); // throttle
  }

  const data = await hostInfo(ip);

  const out = {
    source: 'shodan',
    indicator: value,
    resolved_ip: type === 'domain' ? resolvedIp : undefined,
    type,
    query_time: new Date().toISOString(),
    hostnames: data.hostnames,
    org: data.org,
    isp: data.isp,
    country: data.country_name,
    os: data.os,
    open_ports: data.ports,
    services: (data.data || []).slice(0, 20).map((svc) => ({
      port: svc.port,
      transport: svc.transport,
      product: svc.product,
      version: svc.version,
      banner: typeof svc.data === 'string' ? svc.data.slice(0, 400) : undefined,
    })),
    vulnerabilities: data.vulns,
    last_update: data.last_update,
  };

  console.log(JSON.stringify(out, null, 2));
}

main().catch((e) => die(e.message));
