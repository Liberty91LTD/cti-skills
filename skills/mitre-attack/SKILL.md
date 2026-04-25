---
name: mitre-attack
description: MITRE ATT&CK local dataset reference. Query techniques, groups, software, and mitigations from the local enterprise-attack.json.
user-invocable: false
metadata:
  version: 1.0.0
---

# MITRE ATT&CK Local Reference

## Dataset
Local file: `mitre-attack/enterprise-attack.json` (~45 MB STIX 2.1 bundle).

**First use — if the file is missing**, run the bundled download script before any query:

```bash
./scripts/download-mitre.sh
```

The script is idempotent (skips if the file is already present) and supports `--force` for refresh. If `scripts/download-mitre.sh` is not present in the install (e.g. for plugin-only deployments), fall back to:

```bash
mkdir -p mitre-attack
curl -fsSL https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json \
  -o mitre-attack/enterprise-attack.json
```

This yields a STIX 2.1 bundle containing all Enterprise ATT&CK objects.

## Querying the Dataset

The dataset is a JSON file with a `objects` array. Each object has a `type` field.

### Find a technique by ID
```bash
cat mitre-attack/enterprise-attack.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
tid = 'T1566'  # Change as needed
for obj in data['objects']:
    refs = obj.get('external_references', [])
    for ref in refs:
        if ref.get('external_id') == tid:
            print(json.dumps(obj, indent=2))
            break
"
```

### List all techniques for a tactic
Tactics are mapped via `kill_chain_phases[].phase_name`:
- `reconnaissance`, `resource-development`, `initial-access`, `execution`, `persistence`
- `privilege-escalation`, `defense-evasion`, `credential-access`, `discovery`
- `lateral-movement`, `collection`, `command-and-control`, `exfiltration`, `impact`

### Find a threat group
```bash
# Groups have type "intrusion-set"
cat mitre-attack/enterprise-attack.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
name = 'APT28'  # Change as needed
for obj in data['objects']:
    if obj.get('type') == 'intrusion-set':
        aliases = obj.get('aliases', [])
        if name in aliases or obj.get('name') == name:
            print(json.dumps(obj, indent=2))
"
```

### Map group to techniques
Groups link to techniques via `relationship` objects with `relationship_type: "uses"`.

### Find software/malware
Software objects have type `malware` or `tool`.

## Key Object Types

| Type | ATT&CK Concept | Key Fields |
|------|----------------|-----------|
| `attack-pattern` | Technique | name, description, kill_chain_phases, external_references (technique ID) |
| `intrusion-set` | Group | name, aliases, description |
| `malware` | Malware | name, description, labels |
| `tool` | Tool | name, description |
| `course-of-action` | Mitigation | name, description |
| `relationship` | Links objects | source_ref, target_ref, relationship_type |
| `x-mitre-tactic` | Tactic | name, x_mitre_shortname |

## Common ATT&CK Technique References

| ID | Name | Common Use |
|----|------|-----------|
| T1566 | Phishing | Initial access via email |
| T1566.001 | Spearphishing Attachment | Malicious attachment |
| T1566.002 | Spearphishing Link | Malicious URL |
| T1059 | Command and Scripting Interpreter | Execution via scripts |
| T1059.001 | PowerShell | PowerShell execution |
| T1078 | Valid Accounts | Using legitimate credentials |
| T1071 | Application Layer Protocol | C2 over HTTP/HTTPS/DNS |
| T1055 | Process Injection | Code injection for evasion |
| T1053 | Scheduled Task/Job | Persistence via scheduled tasks |
| T1547 | Boot or Logon Autostart | Persistence via autostart |
| T1562 | Impair Defenses | Disabling security tools |
| T1486 | Data Encrypted for Impact | Ransomware encryption |
| T1190 | Exploit Public-Facing Application | Vulnerability exploitation |

## Usage in Analysis
- Map observed TTPs to ATT&CK technique IDs
- Cross-reference threat actor profiles with known ATT&CK groups
- Identify detection coverage gaps by comparing ATT&CK heatmap to detection rules
- Use ATT&CK Navigator for visual TTP mapping
