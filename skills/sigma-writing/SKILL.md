---
name: sigma-writing
description: Use when the user asks for a SIGMA detection rule, "write a SIGMA rule for X", or `/hash-investigation` / `/malware-analysis` surfaces behaviour worth a vendor-agnostic detection. Format spec + writing guide.
user-invocable: true
metadata:
  version: 1.0.0
---

# SIGMA Rule Writing Guide

SIGMA rules are vendor-agnostic detection rules written in YAML. They can be converted to platform-specific query languages (Splunk SPL, Elastic KQL, Microsoft Sentinel KQL, etc.).

## Rule Structure

```yaml
title: Descriptive title of the detection
id: <UUID>                          # Generate a unique UUID
status: experimental|test|stable
description: >
    Detailed description of what this rule detects and why.
references:
    - https://reference-url.com     # Source intelligence, blog posts, CVE
author: CTI Platform
date: YYYY/MM/DD
modified: YYYY/MM/DD
tags:
    - attack.initial_access         # ATT&CK tactic (lowercase, dots)
    - attack.t1566.001              # ATT&CK technique
    - cve.2024.12345                # CVE if applicable
logsource:
    category: process_creation      # Log category
    product: windows                # OS/product
    service:                        # Optional: specific service
detection:
    selection:
        FieldName|modifier:
            - 'value1'
            - 'value2'
    filter_known_good:
        FieldName: 'legitimate_value'
    condition: selection and not filter_known_good
falsepositives:
    - Description of known false positive scenario
level: critical|high|medium|low|informational
```

## Log Source Categories

| Category | Description | Common fields |
|----------|-------------|---------------|
| `process_creation` | New process started | Image, CommandLine, ParentImage, User |
| `network_connection` | Network connection initiated | DestinationIp, DestinationPort, SourceIp |
| `file_event` | File created/modified/deleted | TargetFilename, Image |
| `registry_event` | Registry key/value change | TargetObject, Details |
| `dns_query` | DNS resolution | QueryName, QueryType |
| `image_load` | DLL/module loaded | ImageLoaded, Image |
| `pipe_created` | Named pipe created | PipeName |
| `ps_script` | PowerShell script execution | ScriptBlockText |
| `webserver` | Web server access logs | cs-uri-query, c-ip |
| `firewall` | Firewall logs | src-ip, dst-ip, dst-port, action |

## Field Modifiers

| Modifier | Description | Example |
|----------|-------------|---------|
| `contains` | Substring match | `CommandLine\|contains: '-enc'` |
| `startswith` | Starts with | `Image\|startswith: 'C:\Temp'` |
| `endswith` | Ends with | `Image\|endswith: '\powershell.exe'` |
| `re` | Regex match | `CommandLine\|re: '.*-e(nc)?.*'` |
| `base64offset` | Base64 encoded content | `CommandLine\|base64offset: 'IEX'` |
| `all` | All values must match | `CommandLine\|contains\|all:` |
| `cidr` | CIDR range match | `DestinationIp\|cidr: '10.0.0.0/8'` |

## Detection Logic

### Condition operators
- `and` — All conditions must match
- `or` — Any condition must match
- `not` — Negate a condition
- `1 of selection*` — Any of the named selections matching `selection*`
- `all of selection*` — All named selections must match

### Common patterns

**Process execution with specific arguments:**
```yaml
detection:
    selection:
        Image|endswith: '\cmd.exe'
        CommandLine|contains:
            - '/c whoami'
            - '/c ipconfig'
            - '/c net user'
    condition: selection
```

**Suspicious parent-child relationship:**
```yaml
detection:
    selection:
        ParentImage|endswith: '\outlook.exe'
        Image|endswith:
            - '\cmd.exe'
            - '\powershell.exe'
            - '\wscript.exe'
    condition: selection
```

**Network connection to suspicious destination:**
```yaml
detection:
    selection:
        DestinationIp|cidr:
            - '185.220.0.0/16'
    filter_internal:
        SourceIp|cidr: '10.0.0.0/8'
    condition: selection and not filter_internal
```

## MITRE ATT&CK Tag Format

```yaml
tags:
    - attack.tactic_name           # e.g., attack.initial_access
    - attack.tXXXX                 # e.g., attack.t1566
    - attack.tXXXX.XXX            # e.g., attack.t1566.001 (sub-technique)
```

Common tactic tags: `attack.initial_access`, `attack.execution`, `attack.persistence`, `attack.privilege_escalation`, `attack.defense_evasion`, `attack.credential_access`, `attack.discovery`, `attack.lateral_movement`, `attack.collection`, `attack.command_and_control`, `attack.exfiltration`, `attack.impact`

## Quality Checklist

- [ ] Unique UUID generated for `id` field
- [ ] ATT&CK technique(s) mapped in tags
- [ ] False positives documented
- [ ] Level accurately reflects severity
- [ ] Log source correctly specified
- [ ] Detection logic tested against known-good and known-bad scenarios
- [ ] References link to source intelligence
- [ ] Description explains WHAT is detected and WHY it matters

## Output Location

Write SIGMA rules to: `data/detection-rules/sigma/<technique-id>-<slug>.yml`
