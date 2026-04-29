---
name: kql-writing
description: Use when the user asks for a KQL query, a Microsoft Sentinel / Defender / Azure Log Analytics detection or hunt, or wants to translate a finding from `/hash-investigation` / `/malware-analysis` into KQL. Format spec + writing guide.
user-invocable: true
metadata:
  version: 1.0.0
---

# KQL Writing Guide — Microsoft Sentinel

KQL (Kusto Query Language) is used in Microsoft Sentinel, Microsoft Defender, and Azure Data Explorer for querying security logs and building detection rules.

## Core Syntax

### Table references
```kql
SecurityEvent                        // Windows Security Events
DeviceProcessEvents                  // Defender for Endpoint
DeviceNetworkEvents                  // Network connections
DeviceFileEvents                     // File operations
EmailEvents                         // Defender for Office 365
SigninLogs                           // Azure AD sign-ins
AuditLogs                           // Azure AD audit
CommonSecurityLog                   // CEF/Syslog
ThreatIntelligenceIndicator         // TI feed indicators
```

### Operators
```kql
| where TimeGenerated > ago(24h)     // Time filter
| where EventID == 4688              // Exact match
| where ProcessCommandLine contains "-enc"  // Substring
| where ProcessCommandLine matches regex @".*-e(nc)?.*"  // Regex
| where SourceIP !in ("10.0.0.1", "10.0.0.2")  // Not in list
| where isnotempty(AccountName)       // Not null/empty
| extend NewColumn = extract(@"pattern", 1, SourceField)  // Extract
| project TimeGenerated, Account, Computer  // Select columns
| summarize count() by bin(TimeGenerated, 1h), Account  // Aggregate
| sort by TimeGenerated desc          // Sort
| take 100                            // Limit results
| join kind=inner (OtherTable) on CommonField  // Join
```

### String operators
| Operator | Description | Case-sensitive |
|----------|-------------|---------------|
| `==` | Exact match | Yes |
| `=~` | Exact match | No |
| `contains` | Substring | No |
| `contains_cs` | Substring | Yes |
| `startswith` | Starts with | No |
| `endswith` | Ends with | No |
| `matches regex` | Regex match | Yes |
| `has` | Word boundary match | No |
| `in` | In list | Yes |
| `in~` | In list | No |

## Common Detection Patterns

### Suspicious process execution (T1059)
```kql
DeviceProcessEvents
| where TimeGenerated > ago(24h)
| where FileName in~ ("powershell.exe", "cmd.exe", "wscript.exe", "cscript.exe")
| where ProcessCommandLine contains_cs "-enc"
    or ProcessCommandLine contains "bypass"
    or ProcessCommandLine contains "downloadstring"
| project TimeGenerated, DeviceName, AccountName, FileName, ProcessCommandLine, InitiatingProcessFileName
```

### Suspicious parent-child (T1566.001)
```kql
DeviceProcessEvents
| where TimeGenerated > ago(24h)
| where InitiatingProcessFileName in~ ("outlook.exe", "winword.exe", "excel.exe", "powerpnt.exe")
| where FileName in~ ("cmd.exe", "powershell.exe", "wscript.exe", "mshta.exe", "certutil.exe")
| project TimeGenerated, DeviceName, AccountName, InitiatingProcessFileName, FileName, ProcessCommandLine
```

### Outbound connection to IOC (C2)
```kql
let IOC_IPs = dynamic(["203.0.113.42", "198.51.100.10"]);
let IOC_Domains = dynamic(["evil.example.com", "c2.badactor.net"]);
DeviceNetworkEvents
| where TimeGenerated > ago(7d)
| where RemoteIP in (IOC_IPs) or RemoteUrl has_any (IOC_Domains)
| project TimeGenerated, DeviceName, RemoteIP, RemoteUrl, RemotePort, InitiatingProcessFileName
```

### Failed sign-in brute force (T1110)
```kql
SigninLogs
| where TimeGenerated > ago(24h)
| where ResultType != "0"
| summarize FailedAttempts = count(), DistinctAccounts = dcount(UserPrincipalName)
    by IPAddress, bin(TimeGenerated, 15m)
| where FailedAttempts > 10
| sort by FailedAttempts desc
```

### Lateral movement — PsExec (T1570)
```kql
DeviceProcessEvents
| where TimeGenerated > ago(24h)
| where FileName =~ "psexesvc.exe"
    or (FileName =~ "cmd.exe" and ProcessCommandLine contains "\\\\")
    or ProcessCommandLine contains "-accepteula -s cmd"
| project TimeGenerated, DeviceName, AccountName, FileName, ProcessCommandLine
```

### DNS query for suspicious domain (T1071.004)
```kql
DeviceEvents
| where TimeGenerated > ago(24h)
| where ActionType == "DnsQueryResponse"
| extend DnsQuery = extractjson("$.DnsQueryString", AdditionalFields)
| where DnsQuery endswith ".onion.ws"
    or DnsQuery endswith ".tor2web.io"
    or DnsQuery matches regex @"^[a-z0-9]{20,}\."
| project TimeGenerated, DeviceName, DnsQuery
```

## Sentinel Analytics Rule Format

```kql
// Rule name: [Descriptive title]
// Description: [What this detects and why]
// MITRE ATT&CK: [Technique IDs]
// Severity: High|Medium|Low|Informational
// Tactics: [InitialAccess, Execution, etc.]

// Query:
[KQL query here]
```

## Best Practices

- Always include a time filter (`ago()`) to limit query scope
- Use `has` instead of `contains` when searching for whole words (faster)
- Prefer `in~` over multiple `or` conditions for case-insensitive list matching
- Use `let` statements for IOC lists to keep queries readable
- Add `project` to select only needed columns (reduces result size)
- Test queries on small time windows first before expanding
- Include comments explaining detection logic

## Output Location

Write KQL queries to: `data/detection-rules/kql/<technique-id>-<slug>.kql`
