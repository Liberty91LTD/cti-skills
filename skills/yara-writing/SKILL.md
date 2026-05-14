---
name: yara-writing
description: Use when the user asks for a YARA rule, "write YARA for this sample/family", or `/hash-investigation` / `/malware-analysis` surfaces a sample worth a static-content rule. Pattern-matching rules for identifying malicious files.
user-invocable: true
metadata:
  version: 1.1.0
---

# YARA Rule Writing Guide

YARA rules identify and classify malware by matching byte patterns, strings, and conditions in files.

## Rule Structure

```yara
rule RuleName : tag1 tag2 {
    meta:
        author = "CTI Platform"
        date = "YYYY-MM-DD"
        description = "Description of what this rule detects"
        reference = "https://source-reference.com"
        tlp = "GREEN"
        mitre_attack = "T1566"
        hash = "sha256_of_sample"
        confidence = "high"

    strings:
        $text1 = "suspicious string" ascii wide
        $hex1 = { 4D 5A 90 00 03 00 00 00 }
        $regex1 = /https?:\/\/[a-z0-9\-\.]+\.onion/

    condition:
        uint16(0) == 0x5A4D and
        filesize < 5MB and
        (2 of ($text*) or $hex1) and
        $regex1
}
```

## String Types

### Text strings
```yara
$s1 = "CreateRemoteThread"          # Exact ASCII match
$s2 = "kernel32.dll" ascii wide     # Match both ASCII and UTF-16
$s3 = "password" nocase             # Case-insensitive
$s4 = "cmd /c" ascii wide nocase    # Combined modifiers
$s5 = "C:\\Windows\\Temp\\"         # Escaped backslashes
```

### Hex strings
```yara
$h1 = { 4D 5A 90 00 }              # Exact bytes (PE header)
$h2 = { 4D 5A ?? ?? 03 00 }        # Wildcards (?? = any byte)
$h3 = { 4D 5A [2-4] 03 00 }        # Jump (2-4 bytes between)
$h4 = { 4D 5A ( 90 00 | 00 00 ) }  # Alternation (OR)
```

### Regular expressions
```yara
$r1 = /https?:\/\/[\w\-\.]+/       # URL pattern
$r2 = /[A-Za-z0-9+\/]{50,}={0,2}/  # Base64 encoded content
$r3 = /(\d{1,3}\.){3}\d{1,3}/      # IP address pattern
```

## Conditions

### File properties
```yara
uint16(0) == 0x5A4D                 # PE file (MZ header)
uint32(0) == 0x464C457F             # ELF file
uint32(0) == 0xBEBAFECA             # Mach-O fat binary
filesize < 10MB                     # File size limit
```

### String matching
```yara
all of them                         # All strings must match
any of them                         # At least one string
2 of ($text*)                       # At least 2 of $text group
3 of ($s1, $s2, $s3, $s4)          # 3 of these 4 strings
$s1 at 0                            # $s1 at offset 0
$s1 in (0..1024)                    # $s1 in first 1KB
#s1 > 3                             # $s1 occurs more than 3 times
```

### PE module (Windows executables)
```yara
import "pe"

pe.number_of_sections > 5
pe.imports("kernel32.dll", "VirtualAlloc")
pe.exports("DllRegisterServer")
pe.is_dll()
pe.timestamp > 1704067200           # Compiled after 2024-01-01
```

## Best Practices

### Do
- Start with a PE/ELF/file type check to limit scope
- Add a filesize constraint to avoid scanning large files
- Use unique strings — prefer byte sequences or specific API combinations over generic strings
- Combine multiple indicators (string + structure + behavior)
- Include metadata with reference to source intelligence
- Test against both malicious samples AND clean files (false positive testing)

### Don't
- Match on single, common strings (e.g., just "http://" or "cmd.exe")
- Create rules without file type constraints (performance killer)
- Use overly broad regex patterns
- Forget to escape special characters in hex patterns
- Write rules that match on packer/crypter artifacts only (will match unrelated packed software)

## Common Malware Patterns

### Encoded PowerShell
```yara
rule Encoded_PowerShell_Execution {
    meta:
        description = "Detects base64 encoded PowerShell commands"
        mitre_attack = "T1059.001"
    strings:
        $enc1 = "-EncodedCommand" ascii nocase
        $enc2 = "-enc " ascii nocase
        $enc3 = "FromBase64String" ascii nocase
        $b64 = /[A-Za-z0-9+\/]{100,}={0,2}/ ascii
    condition:
        any of ($enc*) and $b64
}
```

### Suspicious PE imports
```yara
import "pe"
rule Suspicious_Injection_Imports {
    meta:
        description = "PE with process injection API imports"
        mitre_attack = "T1055"
    condition:
        pe.imports("kernel32.dll", "VirtualAllocEx") and
        pe.imports("kernel32.dll", "WriteProcessMemory") and
        pe.imports("kernel32.dll", "CreateRemoteThread")
}
```

## Naming Convention

- `APT_<GroupName>_<MalwareName>.yar` — For attributed malware
- `MAL_<MalwareName>_<Variant>.yar` — For named malware families
- `SUSP_<Behavior>_<Context>.yar` — For suspicious behavior patterns
- `HUNT_<Target>_<Technique>.yar` — For threat hunting queries

## Output Location

Write YARA rules to: `data/detection-rules/yara/<malware-name>.yar`

## Validation against a real corpus

Before deploying a rule beyond your test set, validate it against a broader sample collection. When ReversingLabs Spectra Analyze is available:

- `/lookup-reversinglabs yara-matches <ruleset_name>` — for a rule you have already deployed to RL, list the samples it has matched in the continuous-scanning corpus. Useful to confirm the rule isn't firing on goodware and to discover new variants caught by the same logic.
- `/lookup-reversinglabs search 'threatname:<family> classification:malicious' --max-results 100` — before writing a family rule, retrieve a candidate sample set to test against. Then pull each sample's hashes for inclusion in your test suite.
- `/lookup-reversinglabs containers <hash>` and `extracted <hash>` — find parents/children of a known sample to ensure the rule fires across the dropper-payload chain, not just on one layer.

Without RL access, fall back to retro-hunting via `/lookup-virustotal` (premium) and `/lookup-otx` pulse traversal.

## Related skills

- `/hash-investigation`, `/malware-analysis` — produce the structural and behavioural intel that informs the rule
- `/lookup-reversinglabs` — corpus validation, family pivots, parent/child relationships
- `/lookup-virustotal`, `/lookup-otx` — community detection signals and pulse-driven sample collection
- `/sigma-writing` — behavioural-detection counterpart for log telemetry
