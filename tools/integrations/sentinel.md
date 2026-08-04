# Microsoft Sentinel integration

[Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/overview) is Microsoft's cloud-native SIEM, built on an Azure **Log Analytics workspace**. This integration queries that workspace with KQL — IOC sweeps, ATT&CK TTP hunts, and table discovery — through the Log Analytics Query API. It is **read-only**: nothing in this pack writes to the workspace, creates analytics rules, or changes incidents.

The defining constraint: **no two Sentinel workspaces have the same tables.** Which tables exist depends on which data connectors and agents the organisation has deployed (Defender for Endpoint brings the `Device*` tables, the Entra ID connector brings `SigninLogs`, the AMA/CEF path brings `CommonSecurityLog`, and so on). The CLI therefore leads with discovery commands, and `skills/lookup-sentinel/SKILL.md` requires every generated query to be restricted to tables verified present.

## Getting credentials

You need **four values**, all from the Azure portal. The access model is an Entra ID *app registration* (a service principal) granted a read-only role on the workspace.

### 1. Create an app registration

1. Azure portal → **Microsoft Entra ID** → **App registrations** → **New registration**.
2. Name it something identifiable, e.g. `cti-skills-sentinel-readonly`. Leave redirect URI empty (this is a daemon flow, no sign-in UI).
3. On the app's **Overview** blade, copy:
   - **Application (client) ID** → `SENTINEL_CLIENT_ID`
   - **Directory (tenant) ID** → `SENTINEL_TENANT_ID`

### 2. Create a client secret

1. In the app registration → **Certificates & secrets** → **Client secrets** → **New client secret**.
2. Set a description (`cti-skills CLI`) and an expiry — pick the shortest that fits your rotation policy; Azure defaults to 180 days.
3. Copy the secret **Value** (not the Secret ID) immediately — it is shown once → `SENTINEL_CLIENT_SECRET`.

### 3. Grant the app read access to the workspace

1. Go to the **Log Analytics workspace** that backs your Sentinel instance (Azure portal → Microsoft Sentinel → your workspace → **Settings → Workspace settings**, or find the workspace directly).
2. **Access control (IAM)** → **Add** → **Add role assignment**.
3. Role: **Log Analytics Reader** (query access to all tables in the workspace). **Microsoft Sentinel Reader** also works and additionally covers Sentinel resources; either is sufficient for this CLI. Do **not** grant Contributor/Responder roles — nothing here needs write access.
4. Members → **User, group, or service principal** → search for the app registration by name → select it → **Review + assign**.

Role assignments can take a few minutes to propagate; a fresh assignment returning `403` briefly is normal.

### 4. Find the workspace ID

On the Log Analytics workspace **Overview** blade, copy **Workspace ID** (a GUID — not the workspace *name*, not the Azure resource ID) → `SENTINEL_WORKSPACE_ID`.

### 5. Configure

Add via `./scripts/setup.sh`, `/cti-setup` in Claude Code, or export directly:

```bash
export SENTINEL_TENANT_ID=00000000-0000-0000-0000-000000000000
export SENTINEL_CLIENT_ID=00000000-0000-0000-0000-000000000000
export SENTINEL_CLIENT_SECRET='<the secret value>'
export SENTINEL_WORKSPACE_ID=00000000-0000-0000-0000-000000000000
```

The CLI also accepts the standard `AZURE_TENANT_ID` / `AZURE_CLIENT_ID` / `AZURE_CLIENT_SECRET` names as fallbacks, so an existing service-principal environment works without duplication. `SENTINEL_WORKSPACE_ID` has no fallback — it must be set explicitly.

## Authentication flow

OAuth2 client credentials, handled by the CLI:

```
POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
  grant_type=client_credentials
  scope=https://api.loganalytics.io/.default
```

The returned bearer token is sent on every query. Tokens are fetched per invocation and never cached to disk.

## Endpoints used

The CLI (`tools/clis/sentinel.py`) touches exactly three URLs:

| Verb | Path | CLI subcommand |
|---|---|---|
| POST | `login.microsoftonline.com/{tenant}/oauth2/v2.0/token` | all (token) |
| POST | `api.loganalytics.io/v1/workspaces/{workspaceId}/query` | `check`, `ingestion`, `probe`, `schema`, `query` |
| GET  | `api.loganalytics.io/v1/workspaces/{workspaceId}/metadata` | `tables` |

The query body is `{"query": "<kql>", "timespan": "<ISO8601 duration>"}`. The server intersects the timespan with any `ago()` filters inside the query, so there is no unbounded query path through this CLI.

## Sovereign / government clouds

Default endpoints are the Azure public cloud. Override both bases together for other clouds:

| Cloud | `SENTINEL_LOGIN_BASE` | `SENTINEL_API_BASE` |
|---|---|---|
| Public (default) | `https://login.microsoftonline.com` | `https://api.loganalytics.io` |
| US Government | `https://login.microsoftonline.us` | `https://api.loganalytics.us` |
| Azure China (21Vianet) | `https://login.chinacloudapi.cn` | `https://api.loganalytics.azure.cn` |

## Which tables exist where — the adaptive premise

Table availability follows connectors. The common mappings:

| Connector / product | Tables it brings |
|---|---|
| Microsoft Defender for Endpoint (or Defender XDR connector) | `DeviceProcessEvents`, `DeviceNetworkEvents`, `DeviceFileEvents`, `DeviceRegistryEvents`, `DeviceLogonEvents`, `DeviceImageLoadEvents`, `DeviceEvents`, `DeviceInfo`, `DeviceNetworkInfo`, `DeviceFileCertificateInfo` |
| Defender for Office 365 (via Defender XDR connector) | `EmailEvents`, `EmailAttachmentInfo`, `EmailUrlInfo`, `EmailPostDeliveryEvents`, `UrlClickEvents` |
| Defender XDR alerts | `AlertInfo`, `AlertEvidence` (Sentinel's own `SecurityAlert` / `SecurityIncident` exist regardless) |
| Defender for Identity | `IdentityLogonEvents`, `IdentityQueryEvents`, `IdentityDirectoryEvents`, `IdentityInfo` |
| Defender for Cloud Apps | `CloudAppEvents`, `BehaviorInfo`/`BehaviorEntities` (preview) |
| Microsoft Entra ID | `SigninLogs`, `AuditLogs`, `AADNonInteractiveUserSignInLogs`, `AADServicePrincipalSignInLogs` |
| Office 365 (management activity) | `OfficeActivity` |
| Azure Activity | `AzureActivity` |
| Windows Security Events (AMA) | `SecurityEvent` |
| Syslog / CEF via AMA | `Syslog`, `CommonSecurityLog` (firewalls, proxies, most third-party appliances) |
| DNS (legacy agent / AMA preview) | `DnsEvents` / `ASimDnsActivityLogs` |
| Threat intelligence connectors | `ThreatIntelligenceIndicator` (newer: `ThreatIntelIndicators`) |
| Defender Vulnerability Management | `DeviceTvmSoftwareVulnerabilities`, `DeviceTvmSecureConfigurationAssessment`, + `*KB` tables |
| Custom / API ingestion | `*_CL` tables (organisation-specific) |

The authoritative catalogue of the Defender XDR advanced-hunting tables (with per-table column references) is Microsoft's schema page: <https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-schema-tables>. Note two naming generations exist for Entra sign-in data in advanced hunting (`AADSignInEventsBeta` → `EntraIdSignInEvents`); in Sentinel workspaces the connector-delivered names are `SigninLogs` / `AADNonInteractiveUserSignInLogs`. When in doubt, trust `tables`/`probe` output over any list — including this one.

Two more discovery caveats:

- **Schema-known ≠ populated.** The `metadata` endpoint (CLI `tables`) lists every table the workspace schema knows, including ones that have never received a row. Cross-check with `ingestion` (Usage-based, billable tables only) or `probe` (ground truth per table).
- **Retention differs per table.** Workspaces commonly keep 90 days interactive retention (Sentinel default) but individual tables can be configured down to 4 days basic-tier or up to years of archive. A zero-hit sweep over 30 days on a table retaining 7 is a retention artefact, not an all-clear.

## Rate limits and query caps

Documented Log Analytics query API limits (public cloud):

- **200 requests per 30 seconds** per client — comfortably above anything this pack does; `probe` over a 20-table list is 20 requests.
- Response capped at **500,000 rows / ~64 MB** per query — always aggregate (`summarize`, `count`) or `take`/`project` in hunts; never pull raw tables.
- Default server-side query timeout **3 minutes** (extendable to 10 with a Prefer header the CLI does not set — restructure the query instead).
- Queries themselves are free at query time on analytics-tier tables; **basic-tier tables bill per GB scanned**. Keep timespans tight.
- `429` responses carry `Retry-After`; the CLI surfaces it.

## Admiralty defaults (for `/score-source`)

**Source reliability: A** — this is your own organisation's telemetry, collected by your own pipeline: a primary source, not a vendor's judgement.

**Information credibility: 2** as a default, not 1, for two structural reasons:

1. **Absence is not evidence of absence.** A miss can mean the table isn't onboarded, the connector was down, retention already dropped the window, or the activity simply wasn't logged at that layer. Report misses as "not observed in collected telemetry over <window>", never "did not occur".
2. **Logs are a target.** Defence evasion (ATT&CK T1070, T1562) includes tampering with exactly this evidence. A sophisticated-intrusion investigation should treat gaps in expected telemetry as a finding.

A *positive* hit corroborated across independent tables (e.g. the same C2 IP in `DeviceNetworkEvents` and `CommonSecurityLog`) can reasonably be raised to A1.

## Testing your credentials

```bash
python3 tools/clis/sentinel.py check
```

A JSON `status: ok` means the token was issued and the workspace answered a query. Failure hints are printed per status code: `401` = bad/expired secret or wrong tenant/client id; `403` = role assignment missing (or not yet propagated); `404` = wrong workspace GUID.

Raw curl equivalent:

```bash
TOKEN=$(curl -s -X POST "https://login.microsoftonline.com/$SENTINEL_TENANT_ID/oauth2/v2.0/token" \
  -d "client_id=$SENTINEL_CLIENT_ID&client_secret=$SENTINEL_CLIENT_SECRET&grant_type=client_credentials&scope=https://api.loganalytics.io/.default" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
curl -s -X POST "https://api.loganalytics.io/v1/workspaces/$SENTINEL_WORKSPACE_ID/query" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"query":"print 1","timespan":"PT5M"}'
```

## Security notes

- **Least privilege is a Reader role.** Nothing in this pack needs Sentinel Contributor, Responder, or workspace write permissions. If a reviewer asks what the app can do: run read queries, list schema — that's all.
- **Scope the role to the workspace**, not the subscription or resource group, unless you intend the app to query every workspace beneath.
- **Secrets expire.** A previously working setup failing with `401` is most often an expired client secret — create a new one and re-run `/cti-setup`.
- Log Analytics query results can contain personal data (UPNs, IPs, hostnames). Anything you copy into a report inherits your organisation's data-handling obligations — apply `/apply-tlp` before sharing, and default to AMBER.

## See also

- Lookup skill: `skills/lookup-sentinel/SKILL.md`
- Python CLI source: `tools/clis/sentinel.py`
- KQL authoring conventions: `skills/kql-writing/SKILL.md`
- Log Analytics REST API: <https://learn.microsoft.com/en-us/rest/api/loganalytics/>
- Defender XDR advanced-hunting schema tables: <https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-schema-tables>
- Sentinel data connectors reference: <https://learn.microsoft.com/en-us/azure/sentinel/data-connectors-reference>
