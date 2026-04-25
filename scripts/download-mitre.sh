#!/usr/bin/env bash
# Download the MITRE ATT&CK Enterprise STIX bundle into mitre-attack/.
# Standalone — invoked by setup.sh, by the /mitre-attack skill on first use,
# or directly by the user.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ATTACK_FILE="$REPO_ROOT/mitre-attack/enterprise-attack.json"
ATTACK_URL="https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

FORCE=0
for arg in "$@"; do
  case "$arg" in
    -f|--force) FORCE=1 ;;
    -h|--help)
      echo "Usage: $0 [--force]"
      echo "  Downloads MITRE ATT&CK Enterprise dataset (~45 MB) to $ATTACK_FILE"
      echo "  Use --force to re-download even if the file exists."
      exit 0
      ;;
    *) echo "Unknown argument: $arg" >&2; exit 2 ;;
  esac
done

if [ -f "$ATTACK_FILE" ] && [ "$FORCE" -eq 0 ]; then
  echo "MITRE ATT&CK data already present at $ATTACK_FILE"
  echo "Use --force to re-download."
  exit 0
fi

mkdir -p "$(dirname "$ATTACK_FILE")"

echo "Downloading MITRE ATT&CK Enterprise dataset (~45 MB)..."
if curl -fsSL "$ATTACK_URL" -o "$ATTACK_FILE.tmp"; then
  mv "$ATTACK_FILE.tmp" "$ATTACK_FILE"
  size=$(wc -c < "$ATTACK_FILE" | tr -d ' ')
  echo "✓ Saved $size bytes to $ATTACK_FILE"
else
  rm -f "$ATTACK_FILE.tmp"
  echo "✗ Download failed. Fetch manually from:" >&2
  echo "  $ATTACK_URL" >&2
  exit 1
fi
