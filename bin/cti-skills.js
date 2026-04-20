#!/usr/bin/env node
// bin/cti-skills.js — install cti-skills into a project (zero deps, Node >= 18)

const fs = require('fs');
const path = require('path');

const SCRIPT_DIR = __dirname;
const ROOT = path.resolve(SCRIPT_DIR, '..');
const CWD = process.cwd();

const argv = process.argv.slice(2);

// Short-circuit for help flags before anything else
if (argv.includes('--help') || argv.includes('-h') || argv[0] === 'help') {
  showHelp();
  process.exit(0);
}

// --target <dir> is the only non-help flag; everything else after is positional
const args = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--target') { i++; continue; } // consume value too
  if (argv[i].startsWith('--')) continue;        // ignore unknown flags
  args.push(argv[i]);
}
const cmd = args[0] || 'install';

const command = {
  install: installAll,
  add: addSkill,
  list: listSkills,
  update: installAll,
}[cmd];

if (!command) {
  process.stderr.write(`Unknown command: ${cmd}\n\n`);
  showHelp();
  process.exit(1);
}

command();

// ---------------------------------------------------------------------------

function installAll() {
  const target = targetFromFlags() || CWD;
  header(`Installing @liberty91/cti-skills into ${target}`);

  const skillsCount = countSkills();

  copyTree(path.join(ROOT, 'skills'), path.join(target, 'skills'));
  log(`✓ ${skillsCount} skills → ${path.join(target, 'skills')}/`);

  copyTree(path.join(ROOT, 'tools'), path.join(target, 'tools'));
  log(`✓ Tool integrations + CLIs → ${path.join(target, 'tools')}/`);

  // Plugin manifest — only drop if the user doesn't already have one
  const pluginSrc = path.join(ROOT, '.claude-plugin');
  const pluginDst = path.join(target, '.claude-plugin');
  if (fs.existsSync(pluginSrc) && !fs.existsSync(pluginDst)) {
    copyTree(pluginSrc, pluginDst);
    log(`✓ Plugin manifest → ${pluginDst}/`);
  } else if (fs.existsSync(pluginDst)) {
    log(`· Plugin manifest already present at ${pluginDst}/ (not overwritten)`);
  }

  // Standalone docs — only copy if absent (don't stomp user's README/CLAUDE.md)
  for (const doc of ['AGENTS.md']) {
    const src = path.join(ROOT, doc);
    const dst = path.join(target, doc);
    if (fs.existsSync(src) && !fs.existsSync(dst)) {
      fs.copyFileSync(src, dst);
      log(`✓ ${doc}`);
    }
  }

  log('');
  log('Next steps:');
  log('  1. (optional) set threat-intel API keys — see tools/integrations/*.md');
  log('  2. start Claude Code in this directory:  claude');
  log('  3. try an investigation:  investigate 8.8.8.8');
  log('  4. list all skills:  npx @liberty91/cti-skills list');
  log('');
}

function addSkill() {
  const name = args[1];
  if (!name) die('usage: cti-skills add <skill-name>');
  const src = path.join(ROOT, 'skills', name);
  if (!fs.existsSync(src)) {
    die(`skill not found: ${name}\n  run 'cti-skills list' to see available skills`);
  }
  const target = targetFromFlags() || CWD;
  const dst = path.join(target, 'skills', name);
  copyTree(src, dst);
  log(`✓ installed skill: ${name} → ${dst}/`);
}

function listSkills() {
  const skillsDir = path.join(ROOT, 'skills');
  if (!fs.existsSync(skillsDir)) die('skills/ directory not found in package');
  const skills = fs.readdirSync(skillsDir, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name)
    .sort();

  // Group for readability
  const groups = {
    'Entry point': ['cti-orchestrator'],
    'Investigation': ['ip-investigation', 'domain-investigation', 'hash-investigation', 'url-investigation'],
    'Lookup': skills.filter((s) => s.startsWith('lookup-')),
    'Knowledge cells': skills.filter((s) =>
      ['china-cyber-espionage', 'russia-cyber-espionage', 'iran-cyber-espionage', 'dprk-cyber-espionage',
       'ransomware-ecosystem', 'carding-financial-fraud', 'infostealers', 'phishing-social-engineering',
       'supply-chain-threats', 'hacktivism', 'initial-access-brokers'].includes(s)),
    'Analytical': skills.filter((s) =>
      ['ach', 'horizon-scanning', 'key-assumptions-check', 'red-team-analysis', 'source-assessment',
       'structured-analytic-techniques', 'threat-assessment', 'threat-actor-profiling', 'campaign-tracking',
       'malware-analysis', 'indicator-pivoting', 'vulnerability-intelligence'].includes(s)),
    'Production': skills.filter((s) =>
      ['intelligence-writing', 'writing-assessments', 'quality-control', 'stix-bundle', 'ioc-export',
       'ioc-enrichment-workflow', 'tlp-guide', 'confidence-levels', 'likelihood-language'].includes(s)),
    'Detection': ['sigma-writing', 'yara-writing', 'kql-writing'],
    'Management': ['pir-management', 'stakeholder-management', 'feedback-loops', 'sops',
      'maturity-assessment', 'intelligence-sharing'],
    'OSINT': ['osint-methodology', 'darkweb-collection'],
    'Methodology': ['cti-hyperloop'],
  };

  log(`${skills.length} skills available:\n`);
  const seen = new Set();
  for (const [group, members] of Object.entries(groups)) {
    const present = members.filter((m) => skills.includes(m));
    if (!present.length) continue;
    log(`  ${group}`);
    for (const s of present) {
      log(`    /${s}`);
      seen.add(s);
    }
    log('');
  }
  const other = skills.filter((s) => !seen.has(s));
  if (other.length) {
    log('  Other');
    for (const s of other) log(`    /${s}`);
  }
}

function showHelp() {
  log(`@liberty91/cti-skills — Cyber Threat Intelligence skills for Claude Code and AI agents

Usage:
  npx @liberty91/cti-skills <command> [options]
  npx github:Liberty91LTD/cti-skills <command> [options]    (install from git)

Commands:
  install          Install all skills + tools into the current directory (default)
  add <skill>      Install a single skill by name
  list             List all available skills, grouped by category
  update           Re-install (overwrites existing copies)
  help             Show this help

Options:
  --target <dir>   Install into <dir> instead of the current directory

Examples:
  npx github:Liberty91LTD/cti-skills
  npx github:Liberty91LTD/cti-skills list
  npx github:Liberty91LTD/cti-skills add threat-actor-profiling
  npx github:Liberty91LTD/cti-skills install --target ~/cti-pack

After install:
  - Skills land in ./skills/
  - Tool integrations + CLIs in ./tools/
  - Start Claude Code:  claude
  - Try:  investigate 8.8.8.8

Docs:  https://github.com/Liberty91LTD/cti-skills
`);
}

// ---------------------------------------------------------------------------

function targetFromFlags() {
  const i = argv.indexOf('--target');
  if (i >= 0 && argv[i + 1]) return path.resolve(argv[i + 1]);
  return null;
}

function countSkills() {
  const skillsDir = path.join(ROOT, 'skills');
  if (!fs.existsSync(skillsDir)) return 0;
  return fs.readdirSync(skillsDir, { withFileTypes: true }).filter((d) => d.isDirectory()).length;
}

function copyTree(src, dst) {
  if (!fs.existsSync(src)) return;
  fs.mkdirSync(dst, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dst, entry.name);
    if (entry.isDirectory()) copyTree(s, d);
    else if (entry.isFile()) fs.copyFileSync(s, d);
  }
}

function header(msg) { log(`\n${msg}\n${'─'.repeat(Math.min(msg.length, 80))}`); }
function log(msg) { process.stdout.write(`${msg}\n`); }
function die(msg) { process.stderr.write(`error: ${msg}\n`); process.exit(1); }
