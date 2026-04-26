#!/usr/bin/env bash
# CTI Agentic Skills — first-run setup
# Merges API keys into .claude/settings.local.json without clobbering existing fields.
#
# Usage:
#   ./scripts/setup.sh                                # interactive (default)
#   ./scripts/setup.sh --non-interactive              # read keys from env vars
#   ./scripts/setup.sh --virustotal=XXX --shodan=YYY  # flag input
#   ./scripts/setup.sh --verify                       # test each configured key
#   ./scripts/setup.sh --skip-mitre                   # skip MITRE ATT&CK download
#   ./scripts/setup.sh --help
#
# Recognised env vars (also used at runtime by the CLIs):
#   VIRUSTOTAL_API_KEY URLSCAN_API_KEY SHODAN_API_KEY ABUSEIPDB_API_KEY
#   GREYNOISE_API_KEY OTX_API_KEY CENSYS_PAT

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SETTINGS_FILE="$REPO_ROOT/.claude/settings.local.json"
ATTACK_FILE="$REPO_ROOT/mitre-attack/enterprise-attack.json"
ATTACK_URL="https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

# --- arg parsing -----------------------------------------------------------

NON_INTERACTIVE=0
VERIFY=0
SKIP_MITRE=0

# Flag-provided keys override env vars; both override prompts.
# Stored as plain shell vars FLAG_<ENVVAR> for bash 3.2 compatibility.
FLAG_VIRUSTOTAL_API_KEY=""
FLAG_URLSCAN_API_KEY=""
FLAG_SHODAN_API_KEY=""
FLAG_ABUSEIPDB_API_KEY=""
FLAG_GREYNOISE_API_KEY=""
FLAG_OTX_API_KEY=""
FLAG_CENSYS_PAT=""

show_help() {
  sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

for arg in "$@"; do
  case "$arg" in
    -h|--help) show_help ;;
    --non-interactive) NON_INTERACTIVE=1 ;;
    --verify) VERIFY=1 ;;
    --skip-mitre) SKIP_MITRE=1 ;;
    --virustotal=*)    FLAG_VIRUSTOTAL_API_KEY="${arg#*=}" ;;
    --urlscan=*)       FLAG_URLSCAN_API_KEY="${arg#*=}" ;;
    --shodan=*)        FLAG_SHODAN_API_KEY="${arg#*=}" ;;
    --abuseipdb=*)     FLAG_ABUSEIPDB_API_KEY="${arg#*=}" ;;
    --greynoise=*)     FLAG_GREYNOISE_API_KEY="${arg#*=}" ;;
    --otx=*)           FLAG_OTX_API_KEY="${arg#*=}" ;;
    --censys=*)        FLAG_CENSYS_PAT="${arg#*=}" ;;
    *) echo "Unknown argument: $arg" >&2; echo "Run with --help for usage." >&2; exit 2 ;;
  esac
done

# --- helpers ---------------------------------------------------------------

# Service definitions: env_var | label | optional_hint
SERVICES=(
  "VIRUSTOTAL_API_KEY|VirusTotal|free 500/day at virustotal.com"
  "URLSCAN_API_KEY|URLScan.io|free 100 scans/day at urlscan.io"
  "SHODAN_API_KEY|Shodan|free tier at account.shodan.io"
  "ABUSEIPDB_API_KEY|AbuseIPDB|free 1000/day at abuseipdb.com"
  "GREYNOISE_API_KEY|GreyNoise|community tier at viz.greynoise.io"
  "OTX_API_KEY|AlienVault OTX|free 10k/hr at otx.alienvault.com"
  "CENSYS_PAT|Censys PAT|Personal Access Token at accounts.censys.io/settings/personal-access-tokens"
)

read_secret() {
  # $1 = prompt
  local val
  if [ -t 0 ] && [ -t 1 ]; then
    read -rsp "$1" val
    echo >&2
  else
    read -r val
  fi
  printf '%s' "$val"
}

# Read existing settings.local.json (if present) and emit it on stdout.
# Falls back to "{}" on missing or invalid file.
load_settings() {
  if [ ! -f "$SETTINGS_FILE" ]; then
    echo "{}"
    return
  fi
  node -e "
    const fs = require('fs');
    try {
      const txt = fs.readFileSync('$SETTINGS_FILE', 'utf8').trim() || '{}';
      JSON.parse(txt);  // validate
      process.stdout.write(txt);
    } catch (e) {
      process.stderr.write('warn: settings.local.json is not valid JSON, treating as empty\n');
      process.stdout.write('{}');
    }
  "
}

# Merge env block into settings JSON. Stdin = current JSON; env KEYS_TO_MERGE
# is space-separated KEY=VAL pairs; stdout = merged JSON.
merge_env() {
  local pairs="$1"
  node -e "
    let txt = '';
    process.stdin.on('data', (b) => txt += b);
    process.stdin.on('end', () => {
      const cur = JSON.parse(txt);
      cur.env = cur.env || {};
      const pairs = process.argv[1].split('\\n').filter(Boolean);
      for (const p of pairs) {
        const i = p.indexOf('=');
        const k = p.slice(0, i), v = p.slice(i + 1);
        if (v.length) cur.env[k] = v;
      }
      process.stdout.write(JSON.stringify(cur, null, 2) + '\\n');
    });
  " "$pairs"
}

resolve_key() {
  # Precedence: flag > env > prompt (interactive only)
  local key="$1" label="$2" hint="$3"
  local flag_var="FLAG_$key"
  local flag_val="${!flag_var:-}"
  if [ -n "$flag_val" ]; then
    printf '%s' "$flag_val"
    return
  fi
  if [ -n "${!key:-}" ]; then
    printf '%s' "${!key}"
    return
  fi
  if [ "$NON_INTERACTIVE" -eq 1 ]; then
    return  # empty
  fi
  read_secret "$label key (optional — $hint, Enter to skip): "
}

verify_key() {
  # $1 = env var, $2 = label
  local key="$1" label="$2" cli="" args=""
  case "$key" in
    VIRUSTOTAL_API_KEY) cli="virustotal"; args="ip 8.8.8.8" ;;
    URLSCAN_API_KEY)    cli="urlscan";    args="domain example.com" ;;
    SHODAN_API_KEY)     cli="shodan";     args="ip 8.8.8.8" ;;
    ABUSEIPDB_API_KEY)  cli="abuseipdb";  args="ip 8.8.8.8" ;;
    GREYNOISE_API_KEY)  cli="greynoise";  args="ip 8.8.8.8" ;;
    OTX_API_KEY)        cli="otx";        args="ip 8.8.8.8" ;;
    CENSYS_PAT) return ;;  # platform SDK validates at runtime; no dry-run CLI yet
  esac
  local cli_path="$REPO_ROOT/tools/clis/$cli.js"
  if [ ! -f "$cli_path" ]; then
    printf '  · %-15s skipped (CLI not found)\n' "$label"
    return
  fi
  if node "$cli_path" $args --dry-run >/dev/null 2>&1; then
    printf '  ✓ %-15s key present, CLI invocation OK (dry-run)\n' "$label"
  else
    printf '  ✗ %-15s CLI dry-run failed\n' "$label"
  fi
}

# --- main ------------------------------------------------------------------

echo "================================================"
echo "  CTI Agentic Skills — Setup"
echo "================================================"
echo ""

mkdir -p "$(dirname "$SETTINGS_FILE")"

if [ "$VERIFY" -eq 1 ]; then
  echo "Verifying configured keys (dry-run, no API calls)..."
  echo ""
  # Load env block from settings file into shell so verify_key sees them
  if [ -f "$SETTINGS_FILE" ]; then
    while IFS='=' read -r k v; do
      [ -n "$k" ] && export "$k=$v"
    done < <(node -e "
      const fs = require('fs');
      const j = JSON.parse(fs.readFileSync('$SETTINGS_FILE', 'utf8') || '{}');
      for (const [k, v] of Object.entries(j.env || {})) {
        if (v) console.log(k + '=' + v);
      }
    ")
  fi
  for svc in "${SERVICES[@]}"; do
    IFS='|' read -r key label _ <<< "$svc"
    if [ -n "${!key:-}" ]; then
      verify_key "$key" "$label"
    else
      printf '  · %-15s not configured\n' "$label"
    fi
  done
  echo ""
  echo "Verification complete."
  exit 0
fi

if [ "$NON_INTERACTIVE" -eq 0 ] && [ -f "$SETTINGS_FILE" ]; then
  echo "Found existing $SETTINGS_FILE — keys will be merged in (other fields preserved)."
  echo ""
fi

echo "Enter API keys. All are optional — press Enter to skip any you don't have."
echo ""

# Collect keys (newline-separated KEY=VALUE pairs for the merge_env helper)
PAIRS=""
for svc in "${SERVICES[@]}"; do
  IFS='|' read -r key label hint <<< "$svc"
  val="$(resolve_key "$key" "$label" "$hint")"
  if [ -n "$val" ]; then
    PAIRS+="$key=$val"$'\n'
  fi
done

if [ -z "$PAIRS" ]; then
  echo ""
  echo "No keys provided. The pack will still work, but skills that need external"
  echo "lookups will skip those steps. Re-run this script anytime to add keys."
else
  CURRENT="$(load_settings)"
  MERGED="$(printf '%s' "$CURRENT" | merge_env "$PAIRS")"
  printf '%s' "$MERGED" > "$SETTINGS_FILE"
  echo ""
  echo "✓ Merged keys into $SETTINGS_FILE (gitignored)."
fi

# --- MITRE ATT&CK dataset --------------------------------------------------

if [ "$SKIP_MITRE" -eq 0 ] && [ ! -f "$ATTACK_FILE" ]; then
  echo ""
  if [ -x "$REPO_ROOT/scripts/download-mitre.sh" ]; then
    "$REPO_ROOT/scripts/download-mitre.sh" || true
  else
    echo "Downloading MITRE ATT&CK Enterprise dataset (~45 MB)..."
    mkdir -p "$(dirname "$ATTACK_FILE")"
    curl -fsSL "$ATTACK_URL" -o "$ATTACK_FILE" \
      && echo "✓ Saved to $ATTACK_FILE" \
      || echo "✗ Download failed. Fetch manually from $ATTACK_URL"
  fi
fi

echo ""
echo "Setup complete."
echo ""
echo "Next steps:"
echo "  1. Start Claude Code in this directory:  claude"
echo "  2. Try an investigation:                 investigate 8.8.8.8"
echo "  3. Verify keys later:                    ./scripts/setup.sh --verify"
echo ""
