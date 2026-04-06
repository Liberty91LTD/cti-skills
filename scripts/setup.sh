#!/bin/bash
# CTI Agentic Skills Platform — First-run setup
# Prompts for API keys and writes .claude/settings.local.json

set -e

SETTINGS_FILE=".claude/settings.local.json"
ATTACK_FILE="mitre-attack/enterprise-attack.json"

echo "================================================"
echo "  CTI Agentic Skills Platform — Setup"
echo "================================================"
echo ""

# Check if settings already exist
if [ -f "$SETTINGS_FILE" ]; then
    echo "Found existing $SETTINGS_FILE"
    read -p "Overwrite? (y/N): " overwrite
    if [ "$overwrite" != "y" ] && [ "$overwrite" != "Y" ]; then
        echo "Keeping existing settings."
        exit 0
    fi
fi

echo "Enter your API keys (press Enter to skip any):"
echo ""

read -p "VirusTotal API key: " VT_KEY
read -p "URLScan.io API key: " URLSCAN_KEY
read -p "Shodan API key: " SHODAN_KEY
read -p "AbuseIPDB API key: " ABUSEIPDB_KEY
read -p "GreyNoise API key: " GREYNOISE_KEY
read -p "AlienVault OTX API key: " OTX_KEY
read -p "Censys API ID: " CENSYS_ID
read -p "Censys API Secret: " CENSYS_SECRET

# Build the settings file
cat > "$SETTINGS_FILE" << EOF
{
  "env": {
    "VIRUSTOTAL_API_KEY": "${VT_KEY}",
    "URLSCAN_API_KEY": "${URLSCAN_KEY}",
    "SHODAN_API_KEY": "${SHODAN_KEY}",
    "ABUSEIPDB_API_KEY": "${ABUSEIPDB_KEY}",
    "GREYNOISE_API_KEY": "${GREYNOISE_KEY}",
    "OTX_API_KEY": "${OTX_KEY}",
    "CENSYS_API_ID": "${CENSYS_ID}",
    "CENSYS_API_SECRET": "${CENSYS_SECRET}"
  }
}
EOF

echo ""
echo "API keys written to $SETTINGS_FILE"
echo "(This file is gitignored — your keys stay local.)"

# Download MITRE ATT&CK data if not present
if [ ! -f "$ATTACK_FILE" ]; then
    echo ""
    echo "Downloading MITRE ATT&CK Enterprise dataset..."
    curl -sL "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json" -o "$ATTACK_FILE"
    echo "Downloaded to $ATTACK_FILE"
else
    echo ""
    echo "MITRE ATT&CK data already present at $ATTACK_FILE"
fi

echo ""
echo "Setup complete. Run 'claude' in this directory to start."
