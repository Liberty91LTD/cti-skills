---
name: lookup-sentinel
description: Use when you need to hunt in the organisation's own Microsoft Sentinel workspace — sweep the logs for IOC hits (IP, domain, hash, URL, account), hunt behavioural TTPs from MITRE ATT&CK techniques, run KQL against live data, or check which tables the workspace actually ingests. Discovers available tables first and only generates KQL for tables that verifiably exist, so hunts adapt to each environment's connectors. Commonly chained by the /*-investigation skills to answer "were we exposed?". Reads $SENTINEL_TENANT_ID, $SENTINEL_CLIENT_ID, $SENTINEL_CLIENT_SECRET, $SENTINEL_WORKSPACE_ID. Read-only.
metadata:
  version: 1.0.0
  tags: [lookup, hunting, kql, sentinel, telemetry, mitre-attack]
  api: sentinel
  default_source_reliability: A
  default_information_credibility: 2
---

# lookup-sentinel

Query bridge to the organisation's own Microsoft Sentinel (Azure Log Analytics) workspace. Every other lookup in this pack asks the world about an indicator; this one asks **your own telemetry**: *has this indicator been seen in our environment? Is this ATT&CK technique's behaviour present in our logs?* It is scoping/exposure-checking, not enrichment — chain it **after** external lookups have told you what an indicator is, to establish whether it touched you.

Read-only. The CLI can only run queries and list schema — it cannot modify the workspace, close incidents, or create analytics rules.

## The cardinal rule: discover before you query

**No two Sentinel workspaces have the same tables.** Table availability follows deployed connectors (Defender for Endpoint brings `Device*`, Entra ID brings `SigninLogs`, AMA/CEF brings `CommonSecurityLog`, …). A query referencing an absent table fails outright; worse, a hunt written for tables the environment doesn't ingest silently proves nothing.

So, in every session, before generating any hunt KQL:

1. Run `tables` (schema-known) and/or `ingestion` (actually receiving data) once, and reuse the result for the rest of the session.
2. `probe` the specific candidate tables for the hunt — schema-known tables can be empty.
3. Generate KQL **only against tables the probe confirmed populated**. When a preferred table is missing, walk the fallback ladder (below). When *no* suitable table exists, report the telemetry gap as a finding — do not fabricate a query, and do not quietly substitute a table that can't answer the question.

## When to invoke

- An investigation skill (`/ip-investigation` etc.) produced a malicious/suspicious verdict and you need the exposure answer: was it seen here?
- The user asks to hunt for an ATT&CK technique, actor TTP set, or behaviour ("hunt for T1059 PowerShell abuse", "look for Kerberoasting")
- The user has IOCs (from a report, a feed, `/ioc-enrichment-workflow`) and wants them swept across the environment
- The user asks what telemetry/tables the Sentinel workspace has, or whether a planned detection would even have data
- The user asks to run or adapt a KQL query against live logs

**Do NOT invoke for:**
- Writing portable detection rules for later deployment — that's `/kql-writing` (author) and `/sigma-writing` (vendor-neutral). This skill *runs* queries; compose with `/kql-writing` for authoring conventions.
- External reputation questions ("is this IP bad?") — that's the other `lookup-*` skills.
- Anything write-shaped (closing incidents, adding analytics rules, updating watchlists) — out of scope by design.

## How to invoke

Single Python CLI (stdlib only — no install). Credentials setup: `tools/integrations/sentinel.md`.

```bash
# Connectivity + auth check (run once per session)
python3 tools/clis/sentinel.py check

# Discovery
python3 tools/clis/sentinel.py tables                       # all schema-known tables
python3 tools/clis/sentinel.py tables --filter Device       # filter by substring
python3 tools/clis/sentinel.py ingestion --days 30          # which tables actually received data (with volume)
python3 tools/clis/sentinel.py probe DeviceNetworkEvents,SigninLogs,CommonSecurityLog --days 7
python3 tools/clis/sentinel.py schema DeviceNetworkEvents   # column names + types

# Hunting — arbitrary KQL, always bounded by a server-side timespan
python3 tools/clis/sentinel.py query 'DeviceNetworkEvents | where RemoteIP == "203.0.113.42" | summarize hits=count(), first=min(TimeGenerated), last=max(TimeGenerated) by DeviceName' --timespan P30D
python3 tools/clis/sentinel.py query --file data/detection-rules/kql/t1059-encoded-powershell.kql --timespan P7D --max-rows 50
```

All commands accept `--dry-run`. The CLI exits 2 if any of the four env vars is unset (when not in dry-run) — report missing credentials and offer `/cti-setup`; do not fabricate results.

## Workflow

```
intent (IOC sweep | TTP hunt | freeform query | table inventory)
  ↓
check  →  tables / ingestion (once per session)  →  probe candidates
  ↓
generate KQL per /kql-writing conventions, restricted to confirmed tables
  ↓
run: summarize-first pass (counts per device/user) → drill into hits only
  ↓
interpret → hits feed /*-investigation + rigor pipeline; misses reported with window + tables searched; gaps reported as findings
```

Query discipline: start with `summarize`/`count` per entity rather than raw rows; keep timespans as tight as the question allows (P7D default, widen deliberately); `take`/`project` when you do pull rows. Results are capped (500k rows / 64 MB server-side; `--max-rows` client-side, reported as `truncated`) — treat a truncated result as a signal to aggregate, not paginate.

## IOC sweep — table candidates by indicator type

Probe in listed order; use every confirmed table, via `union` where sensible. Use `let`-bound `dynamic` lists for multi-IOC sweeps (see `/kql-writing`).

| IOC type | Preferred (EDR-rich) | Fallbacks | Match columns |
|---|---|---|---|
| IP | `DeviceNetworkEvents` | `CommonSecurityLog`, `SigninLogs` + `AADNonInteractiveUserSignInLogs`, `AzureActivity`, `W3CIISLog`, `Syslog` | `RemoteIP`/`LocalIP`; `SourceIP`/`DestinationIP`; `IPAddress`; `CallerIpAddress`; `cIP` |
| Domain | `DeviceNetworkEvents` | `DnsEvents`/`ASimDnsActivityLogs`, `CommonSecurityLog`, `EmailUrlInfo` | `RemoteUrl has`; `Name`/`DnsQuery`; `RequestURL`/`DestinationHostName`; `UrlDomain` |
| File hash | `DeviceFileEvents`, `DeviceProcessEvents` | `DeviceImageLoadEvents`, `EmailAttachmentInfo`, `DeviceEvents` | `SHA256`/`SHA1`/`MD5`, `InitiatingProcessSHA256` |
| URL | `DeviceNetworkEvents` | `EmailUrlInfo`, `UrlClickEvents`, `CommonSecurityLog` | `RemoteUrl`; `Url`; `RequestURL` |
| Account/UPN | `SigninLogs` | `IdentityLogonEvents`, `DeviceLogonEvents`, `SecurityEvent` (4624/4625), `OfficeActivity`, `AuditLogs` | `UserPrincipalName`; `AccountUpn`; `AccountName`; `TargetUserName`; `UserId` |
| Sender/email | `EmailEvents` | `EmailPostDeliveryEvents`, `OfficeActivity` | `SenderFromAddress`, `SenderMailFromAddress`; `RecipientEmailAddress` |

Also probe `ThreatIntelligenceIndicator` (or newer `ThreatIntelIndicators`) — if a TI connector feeds the workspace, the IOC may already be matched by built-in analytics; check `SecurityAlert` for prior alerts on the same indicator before declaring a novel finding.

Report every sweep with: tables searched, tables unavailable, window, and per-table hit counts. **A miss means "not observed in collected telemetry over the window" — never "not compromised".** Retention differs per table; note the window explicitly.

## TTP hunt — mapping techniques to tables

For technique details and detection guidance, first resolve the technique via `/mitre-attack` (local dataset — data sources per technique). Then map data sources to this workspace's confirmed tables:

| Behaviour family (example techniques) | Preferred | Fallbacks when EDR absent |
|---|---|---|
| Process execution/command-line (T1059, T1047, T1204) | `DeviceProcessEvents` | `SecurityEvent` EventID 4688 (needs command-line auditing enabled), `Syslog` auditd `execve` |
| Persistence via registry (T1547, T1112) | `DeviceRegistryEvents` | `SecurityEvent` 4657 (needs SACL auditing) — often absent; report the gap |
| Lateral movement (T1021, T1570) | `DeviceLogonEvents` + `DeviceProcessEvents` | `SecurityEvent` 4624 LogonType 3/10, `IdentityLogonEvents` |
| Credential access (T1110, T1558) | `IdentityLogonEvents` | `SigninLogs` (ResultType != 0 bursts), `SecurityEvent` 4625/4768/4769 |
| C2 / exfil network activity (T1071, T1041, T1567) | `DeviceNetworkEvents` | `CommonSecurityLog` (proxy/firewall), `DnsEvents`, `AzureNetworkAnalytics` |
| Cloud/identity abuse (T1078.004, T1098, T1136) | `AuditLogs` + `SigninLogs` | `AzureActivity`, `CloudAppEvents`, `OfficeActivity` |
| Email initial access (T1566) | `EmailEvents` + `EmailUrlInfo` + `EmailAttachmentInfo` | `UrlClickEvents`, `OfficeActivity` |
| Defense evasion / log tampering (T1070, T1562) | `DeviceEvents`, `SecurityEvent` 1102 | *the gap itself is the signal* — sudden per-table ingestion drops in `Usage` |

`/kql-writing` holds the concrete query patterns for the common techniques — reuse them, then **adapt the table references to what this workspace confirmed**. When neither preferred nor fallback tables exist, the deliverable is the sentence "this environment cannot currently observe technique X because tables Y/Z are not ingested" — a telemetry-gap finding worth more than a query that runs on nothing.

## Response format

```yaml
source: sentinel
operation: check | tables | ingestion | probe | schema | query
workspace_id: <GUID>
query_time: <ISO8601>
# for hunts, the skill wraps CLI output as:
hunt:
  intent: ioc-sweep | ttp-hunt | freeform
  window: <timespan>
  tables_searched: [<confirmed tables>]
  tables_unavailable: [<candidates that were missing/empty>]
  kql: <the query as run>
  hits: <row_count, per-table counts, distilled rows>
  truncated: <bool>
telemetry_gaps: [<behaviours this workspace cannot currently observe, and why>]
```

## Source reliability (Admiralty default)

**A2** — your own organisation's primary telemetry, so reliability A; credibility defaults to 2 rather than 1 because (a) absence of a hit is bounded by connector coverage, retention, and logging depth, and (b) logs are themselves an adversary target (T1070/T1562). Corroborated positive hits across independent tables can be raised to A1. Full reasoning: `tools/integrations/sentinel.md`.

## Operational notes

- **Session-cache the discovery.** `tables`/`ingestion` once per session; `probe` per hunt. Don't re-discover before every query.
- **Rate limit is generous** (200 requests/30s) but basic-tier tables bill per GB scanned — tight timespans are a cost control, not just hygiene.
- **Custom tables (`*_CL`) are first-class.** Organisations route firewall, proxy, or SaaS logs into custom tables; if discovery shows a well-populated `*_CL` table whose name suggests relevant telemetry, `schema` it and consider it in sweeps.
- **Results may contain personal data** (UPNs, IPs, hostnames). Products built on them default to TLP:AMBER — apply `/apply-tlp` before sharing.
- **Prior art check.** Before hunting, a quick `SecurityAlert | where ...` for the same indicator/technique avoids re-discovering what an analytics rule already alerted on.

## Related skills

- `/kql-writing` — query authoring conventions and per-technique patterns; this skill runs what that skill writes
- `/mitre-attack` — resolve technique → data sources before the table mapping
- `/ip-investigation`, `/domain-investigation`, `/hash-investigation`, `/url-investigation` — establish what an indicator *is*; this skill establishes whether it *touched you*; hits feed back into them for pivoting
- `/ioc-enrichment-workflow` — bulk IOC lists; sweep the high-confidence subset here
- `/sigma-writing` — a hunt that proves out here can graduate into a portable rule
- `/score-source`, `/apply-tlp`, `/confidence-language` — rigor pipeline on hunt products

## See also

- Integration setup (app registration walkthrough, roles, sovereign clouds): `tools/integrations/sentinel.md`
- Python CLI source: `tools/clis/sentinel.py`
- Defender XDR advanced-hunting schema tables: https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-schema-tables
- Sentinel data connectors reference: https://learn.microsoft.com/en-us/azure/sentinel/data-connectors-reference
- KQL language reference: https://learn.microsoft.com/en-us/kusto/query/
