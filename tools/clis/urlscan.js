#!/usr/bin/env node
// tools/clis/urlscan.js — URLScan.io scan + retrieve (zero deps, Node >= 18)
// Usage:
//   node urlscan.js url "<url>" [--visibility unlisted|public] [--dry-run]
//   node urlscan.js domain <domain> [--dry-run]

const https = require('https');

const API_KEY = process.env.URLSCAN_API_KEY;
const API_BASE = 'https://urlscan.io/api/v1';

function die(msg, code = 1) {
  process.stderr.write(`error: ${msg}\n`);
  process.exit(code);
}

function usage() {
  process.stderr.write(
    'usage: urlscan.js <url|domain> <value> [--visibility unlisted|public] [--dry-run]\n\n' +
    'Env: URLSCAN_API_KEY required (unless --dry-run).\n' +
    'Default visibility: unlisted.\n'
  );
  process.exit(3);
}

function req(method, url, headers, body) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const opts = { method, hostname: u.hostname, path: u.pathname + u.search, headers };
    const r = https.request(opts, (res) => {
      let data = '';
      res.on('data', (c) => (data += c));
      res.on('end', () => {
        if (res.statusCode >= 400) return reject(new Error(`HTTP ${res.statusCode}: ${data.slice(0, 300)}`));
        try { resolve(JSON.parse(data)); } catch { reject(new Error(`invalid JSON: ${data.slice(0, 300)}`)); }
      });
    });
    r.on('error', reject);
    if (body) r.write(body);
    r.end();
  });
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function submitScan(value, visibility) {
  const url = `${API_BASE}/scan/`;
  const body = JSON.stringify({ url: value, visibility });
  const headers = {
    'API-Key': API_KEY,
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(body),
    Accept: 'application/json',
  };
  return req('POST', url, headers, body);
}

async function pollResult(uuid) {
  const url = `${API_BASE}/result/${uuid}/`;
  const headers = { 'API-Key': API_KEY, Accept: 'application/json' };
  for (let i = 0; i < 6; i++) {
    try { return await req('GET', url, headers); }
    catch (e) {
      if (i === 5) throw e;
      await sleep(10_000);
    }
  }
}

async function searchDomain(domain) {
  const url = `${API_BASE}/search/?q=domain:${encodeURIComponent(domain)}&size=5`;
  const headers = { 'API-Key': API_KEY, Accept: 'application/json' };
  return req('GET', url, headers);
}

async function main() {
  const argv = process.argv.slice(2);
  const dryRun = argv.includes('--dry-run');
  const visIdx = argv.indexOf('--visibility');
  const visibility = visIdx >= 0 ? argv[visIdx + 1] : 'unlisted';
  const args = argv.filter((a, i) => !a.startsWith('--') && argv[i - 1] !== '--visibility');
  if (args.length < 2) usage();
  const [type, value] = args;
  if (!['url', 'domain'].includes(type)) usage();

  if (dryRun) {
    const out = {
      dry_run: true,
      method: type === 'url' ? 'POST+GET' : 'GET',
      url: type === 'url' ? `${API_BASE}/scan/ (then /result/{uuid}/)` : `${API_BASE}/search/?q=domain:${value}`,
      body: type === 'url' ? { url: value, visibility } : undefined,
      headers: { 'API-Key': API_KEY ? '<redacted>' : '<unset>' },
    };
    console.log(JSON.stringify(out, null, 2));
    return;
  }
  if (!API_KEY) die('URLSCAN_API_KEY not set.', 2);

  let scan;
  if (type === 'url') {
    const submit = await submitScan(value, visibility);
    await sleep(30_000); // initial wait for scan processing
    scan = await pollResult(submit.uuid);
  } else {
    const search = await searchDomain(value);
    if (!search.results?.length) {
      console.log(JSON.stringify({ source: 'urlscan', indicator: value, type, no_results: true }, null, 2));
      return;
    }
    scan = search.results[0];
  }

  const page = scan.page || {};
  const task = scan.task || {};
  const verdicts = scan.verdicts?.overall || {};
  const lists = scan.lists || {};
  const stats = scan.stats || {};

  const out = {
    source: 'urlscan',
    indicator: value,
    type,
    query_time: new Date().toISOString(),
    verdict: verdicts.malicious ? 'malicious' : verdicts.hasVerdicts ? 'suspicious' : 'clean',
    final_url: page.url,
    ip: page.ip,
    country: page.country,
    server: page.server,
    domains_contacted: lists.domains?.slice(0, 20),
    ips_contacted: lists.ips?.slice(0, 20),
    screenshot_url: task.screenshotURL,
    scan_url: task.reportURL,
    key_findings: verdicts.tags || [],
    stats,
  };

  console.log(JSON.stringify(out, null, 2));
}

main().catch((e) => die(e.message));
